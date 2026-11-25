"""Is each listing still open? The employer's live feed decides; a sample of pages is a second opinion.

History. Until 25 Nov 2026 every apply page was opened at every refresh. Hiring-system pages throttle automated
visitors (HTTP 403), so on busy days a quarter to a third of pages "could not be checked": on 25 Nov 375 new jobs
were held back and 120 were kept on old checks, and the workflow went red. Yet a sample of 150 in-feed jobs opened
by hand that day: 149 opened normally, 0 were gone, 0 said "closed" (the one exception blocks all automated visitors).
Employers' hiring systems remove a role from the public feed when it closes, so the feed is the source of truth.
KT approved checking this way on 25 Nov 2026 (decision: drafts/decisions/2026-11-25-feed-based-link-check.md).

Rules now:
1. Every listing in this run's feed is verified at this run (its card shows when we last saw it in the feed).
   A role that leaves the feed leaves the board at the next refresh.
2. A sample of pages is opened each run (PAGE_SAMPLE, new listings first, then the longest unchecked), gently.
   DEAD (404, 410, or the "error=true" redirect Greenhouse uses for a closed role) removes that listing and keeps it
   off for DEAD_RECHECK_DAYS even if the feed still lists it. UNKNOWN (403, timeouts) changes nothing.
3. Alarm: if more than MISMATCH_SHARE of the sampled pages are dead, the feed and the pages disagree; after
   MAX_MISMATCH_RUNS such runs in a row the workflow fails loudly so someone looks.
The state lives in data/link_state.json.
"""
import json
import statistics
from collections import Counter
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

ALIVE, DEAD, UNKNOWN = "alive", "dead", "unknown"
DEAD_STATUSES = (404, 410)
PAGE_SAMPLE = 60              # pages opened per run
PAGE_WORKERS = 4              # gently: a few at a time
DEAD_RECHECK_DAYS = 7         # a page found gone stays off this long, then is opened again
MISMATCH_SHARE = 0.10         # dead share of the sample above which the feed and pages disagree
MIN_SAMPLE_FOR_ALARM = 20
MAX_MISMATCH_RUNS = 2
MAX_DRIFT_ABORTS = 3          # the "listings fell sharply" guard may hold the data for at most this many runs in a row
RATE_HISTORY = 10
RETRY_DELAY_SECONDS = 8       # pause before the second pass
RETRY_WORKERS = 3             # and only a few requests at a time


def link_verdict(url, session, timeout=15, sleep=time.sleep, reasons=None):
    """ALIVE, DEAD or UNKNOWN for one apply link. Never raises. `reasons` (a Counter) collects why a link was UNKNOWN,
    so the next incident can be diagnosed from data/metrics.json instead of guessed (the 31 Oct cause could not be proved)."""
    verdict, why = UNKNOWN, "unknown"
    for attempt in range(2):
        try:
            resp = session.head(url, timeout=timeout, allow_redirects=True)
            if resp.status_code in (403, 405, 501):
                resp = session.get(url, timeout=timeout, allow_redirects=True, stream=True)
                resp.close()
            if "error=true" in str(resp.url):
                return DEAD
            code = resp.status_code
            if code < 400:
                return ALIVE
            if code in DEAD_STATUSES:
                return DEAD
            verdict, why = UNKNOWN, f"http-{code}"      # 400, 401, 403, 429, 5xx: cannot tell whether the posting is open
        except requests.Timeout:
            verdict, why = UNKNOWN, "timeout"
        except requests.RequestException:
            verdict, why = UNKNOWN, "connection-error"
        if attempt == 0:
            sleep(1)
    if reasons is not None and verdict == UNKNOWN:
        reasons[why] += 1
    return verdict


def load_state(path):
    try:
        s = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(s, dict):
            s.setdefault("unknown", {}); s.setdefault("failRates", []); s.setdefault("degradedStreak", 0); s.setdefault("driftAborts", 0)
            return s
    except (OSError, ValueError):
        pass
    return {"unknown": {}, "failRates": [], "degradedStreak": 0, "driftAborts": 0}


def save_state(path, state):
    state = dict(state)
    state["failRates"] = state.get("failRates", [])[-RATE_HISTORY:]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, indent=1, sort_keys=True), encoding="utf-8")


def _days_since(iso, now):
    from datetime import datetime
    try:
        return (now - datetime.fromisoformat(iso.replace("Z", "+00:00"))).total_seconds() / 86400
    except (AttributeError, ValueError):
        return 1e9


def check_links(items, session, state, published_before, removed, verdict_fn=None, workers=PAGE_WORKERS,
                retry_delay=RETRY_DELAY_SECONDS, retry_workers=RETRY_WORKERS, sleep=time.sleep, now=None, sample_size=PAGE_SAMPLE):
    """items: listing dicts with "url", all read from this run's live feeds. published_before: {url: lastVerifiedAt}.
    Returns (listings to publish, stats, new state). Every returned listing is verified now (seen in the live feed)."""
    from datetime import datetime, timezone
    now = now or datetime.now(timezone.utc)
    reasons = Counter()
    verdict_fn = verdict_fn or (lambda u: link_verdict(u, session, sleep=sleep, reasons=reasons))
    urls = {j["url"] for j in items}
    dead_before = {u: t for u, t in (state.get("dead") or {}).items() if u in urls}
    checked_at = {u: t for u, t in (state.get("pageChecked") or {}).items() if u in urls}

    # the sample: dead pages due a re-check, then new listings, then the ones whose page was opened longest ago
    due_dead = [j for j in items if j["url"] in dead_before and _days_since(dead_before[j["url"]], now) >= DEAD_RECHECK_DAYS]
    fresh = [j for j in items if j["url"] not in published_before and j["url"] not in dead_before]
    rest = sorted((j for j in items if j["url"] in published_before and j["url"] not in dead_before),
                  key=lambda j: checked_at.get(j["url"], ""))
    sample, seen = [], set()
    for j in due_dead + fresh + rest:
        if len(sample) >= sample_size:
            break
        if j["url"] not in seen:
            seen.add(j["url"]); sample.append(j)

    verdicts = {}
    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        fmap = {ex.submit(verdict_fn, j["url"]): j for j in sample}
        for f in as_completed(fmap):
            try:
                verdicts[fmap[f]["url"]] = f.result()
            except Exception:
                verdicts[fmap[f]["url"]] = UNKNOWN
    first_pass_unknown = [j for j in sample if verdicts.get(j["url"]) == UNKNOWN]
    recovered = 0
    if first_pass_unknown and retry_workers:
        sleep(retry_delay)
        with ThreadPoolExecutor(max_workers=retry_workers) as ex:
            fmap = {ex.submit(verdict_fn, j["url"]): j for j in first_pass_unknown}
            for f in as_completed(fmap):
                try:
                    v = f.result()
                except Exception:
                    v = UNKNOWN
                if v != UNKNOWN:
                    verdicts[fmap[f]["url"]] = v
                    recovered += 1

    stamp = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    new_dead = dict(dead_before)
    ok, dropped_dead = [], 0
    for j in items:
        url, v = j["url"], verdicts.get(j["url"])
        if v is not None and v != UNKNOWN:
            checked_at[url] = stamp
        if v == DEAD:
            new_dead[url] = stamp
        elif v == ALIVE:
            new_dead.pop(url, None)
        if url in new_dead:
            dropped_dead += 1
            removed.append(f"link-dead | {j['title']} | {j['company']} | {url}")
            continue
        ok.append(j)

    n = len(sample)
    dead = sum(1 for v in verdicts.values() if v == DEAD)
    unknown = sum(1 for v in verdicts.values() if v == UNKNOWN)
    answered = n - unknown
    dead_share = dead / answered if answered else 0.0
    mismatch = answered >= MIN_SAMPLE_FOR_ALARM and dead_share > MISMATCH_SHARE
    streak = state.get("mismatchStreak", 0) + 1 if mismatch else 0
    new_state = {k: v for k, v in state.items() if k not in ("unknown", "failRates", "degradedStreak")}
    new_state.update({"dead": new_dead, "pageChecked": checked_at, "mismatchStreak": streak})
    stats = {"verifiedBy": "employer feed", "inFeed": len(items), "checked": n, "alive": n - dead - unknown, "dead": dead,
             "unknown": unknown, "deadShare": round(dead_share, 4), "failRate": round((dead + unknown) / n, 4) if n else 0.0,
             "baselineRate": None, "degraded": False, "degradedStreak": 0, "mismatch": mismatch, "mismatchStreak": streak,
             "carriedOnOldCheck": 0, "newHeldUntilChecked": 0, "droppedDead": dropped_dead, "droppedUnverifiable": 0,
             "firstPassUnknown": len(first_pass_unknown), "recoveredOnRetry": recovered,
             "unknownReasons": dict(reasons.most_common())}
    return ok, stats, new_state
