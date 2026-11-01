"""Link checking that tells "the page is gone" from "we could not check".

Why this exists (31 Oct 2026): one refresh run saw 229 apply links fail, against a normal 34 to 50, and removed
208 open Greenhouse jobs from the board for about four hours. The old checker treated every timeout, 403, 429 and 5xx
as a dead link, and the only safety net (stop the run if listings fall by more than 40%) did not fire at 20%.
The raw feed was unchanged (about 21,000 candidates), so the jobs were open; only our checker was being blocked.

Rules now:
1. Three verdicts. ALIVE (opens). DEAD (the page is definitely gone: 404, 410, or the "error=true" redirect Greenhouse
   uses for a closed role). UNKNOWN (timeout, connection error, 401/403/429/5xx: we could not tell).
2. Only DEAD removes a listing straight away. A listing that was published last run and comes back UNKNOWN is kept
   for up to MAX_UNKNOWN_RUNS refreshes in a row (about 18 hours) and shows its real last-checked time.
   A NEW listing that comes back UNKNOWN is simply not published yet; it is retried next run.
3. Circuit breaker: if the share of failing links is far above normal (above DEGRADED_MIN_RATE and above
   DEGRADED_MULTIPLE times the recent median), the checker is assumed blocked. Nothing published last run is dropped
   for a failed check, and nobody's unknown count goes up. After MAX_DEGRADED_RUNS such runs in a row the workflow
   fails loudly (the feed is still the source of truth for open roles; the checker is what is broken).
The state lives in data/link_state.json so these rules survive between runs.
"""
import json
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

ALIVE, DEAD, UNKNOWN = "alive", "dead", "unknown"
DEAD_STATUSES = (404, 410)
MAX_UNKNOWN_RUNS = 3
DEGRADED_MIN_RATE = 0.12      # a normal run fails 3% to 5% of links
DEGRADED_MULTIPLE = 2.5
MAX_DEGRADED_RUNS = 4
MAX_DRIFT_ABORTS = 3          # the "listings fell sharply" guard may hold the data for at most this many runs in a row
RATE_HISTORY = 10


def link_verdict(url, session, timeout=15, sleep=time.sleep):
    """ALIVE, DEAD or UNKNOWN for one apply link. Never raises."""
    verdict = UNKNOWN
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
            verdict = UNKNOWN          # 400, 401, 403, 429, 5xx: cannot tell whether the posting is open
        except requests.RequestException:
            verdict = UNKNOWN
        if attempt == 0:
            sleep(1)
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


def check_links(items, session, state, published_before, removed, verdict_fn=None, workers=24):
    """items: listing dicts with "url". published_before: {url: lastVerifiedAt} from the previous jobs.json.
    Returns (listings to publish, stats, new state). Carried listings get j["verifiedAt"] = their old check time."""
    verdict_fn = verdict_fn or (lambda u: link_verdict(u, session))
    verdicts = {}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        fmap = {ex.submit(verdict_fn, j["url"]): j for j in items}
        for f in as_completed(fmap):
            try:
                verdicts[fmap[f]["url"]] = f.result()
            except Exception:
                verdicts[fmap[f]["url"]] = UNKNOWN

    n = len(items)
    dead = sum(1 for v in verdicts.values() if v == DEAD)
    unknown = sum(1 for v in verdicts.values() if v == UNKNOWN)
    fail_rate = (dead + unknown) / n if n else 0.0
    rates = [r for r in state.get("failRates", []) if isinstance(r, (int, float))]
    baseline = statistics.median(rates[-5:]) if rates else None
    threshold = max(DEGRADED_MIN_RATE, DEGRADED_MULTIPLE * baseline) if baseline is not None else DEGRADED_MIN_RATE
    degraded = n >= 50 and fail_rate > threshold

    ok, new_unknown = [], {}
    carried = held_new = dropped_dead = dropped_unverifiable = 0
    for j in items:
        url, v = j["url"], verdicts.get(j["url"], UNKNOWN)
        if v == ALIVE:
            ok.append(j)
            continue
        was_published = url in published_before
        count = state.get("unknown", {}).get(url, 0)
        if degraded:
            if was_published:
                j["verifiedAt"] = published_before[url]; ok.append(j); carried += 1
                new_unknown[url] = count                      # a blocked checker does not age anything
            else:
                held_new += 1
            continue
        if v == DEAD:
            dropped_dead += 1
            removed.append(f"link-dead | {j['title']} | {j['company']} | {url}")
        elif was_published and count + 1 <= MAX_UNKNOWN_RUNS:
            j["verifiedAt"] = published_before[url]; ok.append(j); carried += 1
            new_unknown[url] = count + 1
        elif was_published:
            dropped_unverifiable += 1
            removed.append(f"link-unverifiable-{MAX_UNKNOWN_RUNS}-runs | {j['title']} | {j['company']} | {url}")
        else:
            held_new += 1                                     # new listing we could not check: try again next run

    streak = state.get("degradedStreak", 0) + 1 if degraded else 0
    new_state = dict(state)
    new_state.update({"unknown": new_unknown, "degradedStreak": streak,
                      "failRates": state.get("failRates", []) if degraded else (rates + [round(fail_rate, 4)])})
    stats = {"checked": n, "alive": n - dead - unknown, "dead": dead, "unknown": unknown, "failRate": round(fail_rate, 4),
             "baselineRate": None if baseline is None else round(baseline, 4), "degraded": degraded, "degradedStreak": streak,
             "carriedOnOldCheck": carried, "newHeldUntilChecked": held_new,
             "droppedDead": dropped_dead, "droppedUnverifiable": dropped_unverifiable}
    return ok, stats, new_state
