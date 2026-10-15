#!/usr/bin/env python3
"""Discover, interpret, verify and publish remote job listings.

Stages: discover (permitted public feeds and employer ATS endpoints) ->
extract (full description, location, posting date) -> classify (work
arrangement, geographic eligibility, level, category; see classify.py) ->
quality gates (age, duplicates, suspicious wording, working link) ->
publish eligible listings with transparent uncertainty labels.

Listings that are hybrid, on-site, contradictory or low quality are not
published; the reason is written to data/removed.log and contradictions go
to data/review_queue.json for a human look.
"""

import hashlib
import html
import json
import os
import re
import sys
import time
import unicodedata
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
from pathlib import Path

import requests

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

import classify as C  # noqa: E402
REPO_ROOT = SCRIPT_DIR.parent
OUTPUT_FILE = REPO_ROOT / "jobs.json"
REMOVED_LOG = REPO_ROOT / "data" / "removed.log"
REVIEW_FILE = REPO_ROOT / "data" / "review_queue.json"
METRICS_FILE = REPO_ROOT / "data" / "metrics.json"
BOARDS_FILE = REPO_ROOT / "data" / "boards.json"

MAX_AGE_DAYS = 30
MAX_PER_COMPANY = 15
MAX_LISTINGS = 1200
LOG_SAMPLE = 40
REVIEW_LIMIT = 150

S = requests.Session()
S.headers.update({"User-Agent": "JobBoard/1.0 (remote job board; contact via site)"})
CA_BUNDLE = os.environ.get("CA_BUNDLE_PATH", "/root/.ccr/ca-bundle.crt")
if os.path.exists(CA_BUNDLE):
    S.verify = CA_BUNDLE

NOW = datetime.now(timezone.utc)
OLDEST = NOW - timedelta(days=MAX_AGE_DAYS)

SEARCH_URL_RE = re.compile(r"/jobs/search\b|/search\?|/careers\?.*q=", re.I)
NON_ENGLISH_RE = re.compile(
    r"\(m/[fwd]/[dw]\)|\b(und|für|oder|bei|mit|über)\b|"
    r"\b(y|del|los|las|para|como|desde|hacia|entre|sobre|según|diagnóstico|mecánico|presupuesto|automotriz)\b", re.I)


def is_non_english(title):
    if NON_ENGLISH_RE.search(title):
        return True
    try:
        title.encode("ascii")
    except UnicodeEncodeError:
        return sum(1 for ch in title if ord(ch) > 127) > 2
    return False


def norm_key(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "", s)


def parse_dt(value):
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None
    return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def load_boards():
    return json.loads(BOARDS_FILE.read_text(encoding="utf-8"))


def get_json(url, **kw):
    try:
        r = S.get(url, timeout=kw.pop("timeout", 25), **kw)
        if r.status_code == 200:
            return r.json()
    except (requests.RequestException, ValueError):
        pass
    return None


# ── Sources ───────────────────────────────────────────────────────────
# Every source returns raw listings: title, company, url, location, description
# (full text), hint (structured work-arrangement field if the source has one),
# posted (original posting date), source, employment, salary, remote_feed.

def gh_canonical_url(slug, job):
    url = job.get("absolute_url", "") or ""
    if "greenhouse.io" in url and not SEARCH_URL_RE.search(url):
        return url
    return f"https://job-boards.greenhouse.io/{slug}/jobs/{job.get('id')}"


def fetch_greenhouse_board(board):
    data = get_json(f"https://boards-api.greenhouse.io/v1/boards/{board['slug']}/jobs", params={"content": "true"}, timeout=40)
    out = []
    for j in (data or {}).get("jobs", []):
        posted = parse_dt(j.get("first_published"))
        out.append({
            "title": j.get("title", ""), "company": board["company"],
            "url": gh_canonical_url(board["slug"], j),
            "location": (j.get("location") or {}).get("name", ""),
            "description": j.get("content", ""), "hint": None, "posted": posted,
            "source": "Greenhouse", "employment": None, "salary": None, "remote_feed": False,
        })
    return out


def _salary_text(currency, interval, lo, hi):
    if not (lo or hi):
        return None
    cur = currency or ""
    per = {"year": "/yr", "month": "/mo", "hour": "/hr", "week": "/wk", "day": "/day"}.get((interval or "").lower().replace("per-", "").replace("per ", ""), "")
    if lo and hi:
        return f"{cur} {int(lo):,}–{int(hi):,}{per}".strip()
    return f"{cur} {int(lo or hi):,}{per}".strip()


def fetch_lever_board(board):
    data = get_json(f"https://api.lever.co/v0/postings/{board['slug']}", params={"mode": "json"}, timeout=40)
    out = []
    if not isinstance(data, list):
        return out
    for j in data:
        cats = j.get("categories") or {}
        extra = []
        for blk in j.get("lists") or []:
            extra.append((blk.get("text") or "") + " " + C.clean_text(blk.get("content") or ""))
        desc = "\n".join([j.get("descriptionPlain") or "", *extra, j.get("additionalPlain") or ""])
        ms = j.get("createdAt")
        posted = datetime.fromtimestamp(ms / 1000, tz=timezone.utc) if ms else None
        loc = cats.get("location") or ""
        all_locs = cats.get("allLocations") or []
        if len(all_locs) > 1:
            loc = "; ".join(all_locs)
        sr = j.get("salaryRange") or {}
        out.append({
            "title": j.get("text", ""), "company": board["company"], "url": j.get("hostedUrl", ""),
            "location": loc, "description": desc, "hint": j.get("workplaceType"), "posted": posted,
            "source": "Lever", "employment": cats.get("commitment"),
            "salary": _salary_text(sr.get("currency"), sr.get("interval"), sr.get("min"), sr.get("max")),
            "remote_feed": False,
        })
    return out


def fetch_ashby_board(board):
    data = get_json(f"https://api.ashbyhq.com/posting-api/job-board/{board['slug']}", params={"includeCompensation": "true"}, timeout=40)
    out = []
    for j in (data or {}).get("jobs", []):
        if j.get("isListed") is False:
            continue
        loc = j.get("location") or ""
        sec = [s.get("location") if isinstance(s, dict) else str(s) for s in (j.get("secondaryLocations") or [])]
        if sec:
            loc = "; ".join([loc] + [s for s in sec if s])
        hint = j.get("workplaceType") or ("remote" if j.get("isRemote") else None)
        comp = (j.get("compensation") or {})
        out.append({
            "title": j.get("title", ""), "company": board["company"], "url": j.get("jobUrl", ""),
            "location": loc, "description": j.get("descriptionPlain") or j.get("descriptionHtml") or "",
            "hint": hint, "posted": parse_dt(j.get("publishedAt")),
            "source": "Ashby", "employment": j.get("employmentType"),
            "salary": comp.get("scrapeableCompensationSalarySummary") or comp.get("compensationTierSummary"),
            "remote_feed": False,
        })
    return out


JOBICY_INDUSTRIES = ["", "supporting", "admin-support", "accounting-finance", "marketing", "copywriting",
                     "business", "hr", "data-science", "design-multimedia", "management"]


def fetch_jobicy():
    out = []
    for ind in JOBICY_INDUSTRIES:
        params = {"count": 50}
        if ind:
            params["industry"] = ind
        data = get_json("https://jobicy.com/api/v2/remote-jobs", params=params, timeout=30)
        for j in (data or {}).get("jobs", []):
            geo = j.get("jobGeo") or ""
            smin, smax = j.get("salaryMin"), j.get("salaryMax")
            out.append({
                "title": j.get("jobTitle", ""), "company": j.get("companyName", ""), "url": j.get("url", ""),
                "location": geo or "Anywhere", "description": j.get("jobDescription", ""), "hint": None,
                "posted": parse_dt((j.get("pubDate") or "").replace(" ", "T")),
                "source": "Jobicy", "employment": ", ".join(j.get("jobType") or []) or None,
                "salary": _salary_text(j.get("salaryCurrency"), j.get("salaryPeriod"), smin, smax),
                "remote_feed": True,
            })
        time.sleep(0.6)
    return out


def fetch_all(boards):
    raw, counts = [], Counter()
    jobs = [("greenhouse", b, fetch_greenhouse_board) for b in boards.get("greenhouse", [])]
    jobs += [("lever", b, fetch_lever_board) for b in boards.get("lever", [])]
    jobs += [("ashby", b, fetch_ashby_board) for b in boards.get("ashby", [])]
    with ThreadPoolExecutor(max_workers=12) as ex:
        futs = {ex.submit(fn, b): (kind, b) for kind, b, fn in jobs}
        for f in as_completed(futs):
            kind, b = futs[f]
            try:
                res = f.result()
            except Exception as e:  # one broken board must not stop the run
                print(f"  {kind}/{b['slug']} failed: {e}")
                continue
            counts[kind] += len(res)
            raw.extend(res)
    print(f"  ATS boards: {dict(counts)}")
    jobicy = fetch_jobicy()
    print(f"  Jobicy: {len(jobicy)}")
    raw.extend(jobicy)
    return raw


# ── Link check ────────────────────────────────────────────────────────

def verify_link(url, timeout=15):
    for attempt in range(2):
        try:
            resp = S.head(url, timeout=timeout, allow_redirects=True)
            if resp.status_code in (403, 405, 501):
                resp = S.get(url, timeout=timeout, allow_redirects=True, stream=True)
                resp.close()
            if "error=true" in resp.url:
                return False
            return resp.status_code < 400
        except requests.RequestException:
            time.sleep(1)
    return False


# ── Processing ────────────────────────────────────────────────────────

ARRANGEMENT_LABEL = {
    C.FULLY_REMOTE: "Fully remote",
    C.REMOTE_RESTRICTED: "Remote with location restrictions",
    C.REMOTE_UNCLEAR: "Remote: arrangement not confirmed",
}


def process(raw, removed, review):
    """Apply gates and classification. Returns publishable records."""
    keep, seen_urls = [], set()
    drops = Counter()
    for j in raw:
        url = (j.get("url") or "").strip()
        title = (j.get("title") or "").strip()
        tag = f"{title} | {j.get('company')} | {url}"
        if not url or not title:
            drops["missing-url-or-title"] += 1
            continue
        if SEARCH_URL_RE.search(url):
            drops["search-url"] += 1; removed.append(f"search-url | {tag}"); continue
        posted = j.get("posted")
        if not posted:
            drops["no-posted-date"] += 1; removed.append(f"no-posted-date | {tag}"); continue
        if posted < OLDEST:
            drops["older-than-30-days"] += 1; continue
        if posted > NOW + timedelta(days=1):
            drops["future-date"] += 1; removed.append(f"future-date | {tag}"); continue
        if is_non_english(title):
            drops["non-english"] += 1; removed.append(f"non-english | {tag}"); continue
        key = url.rstrip("/")
        if key in seen_urls:
            drops["duplicate-url"] += 1; continue
        seen_urls.add(key)

        res = C.classify_listing(title, j.get("location", ""), j.get("description", ""),
                                 hint=j.get("hint"), declared_type=j.get("employment"),
                                 remote_feed=j.get("remote_feed", False))
        decision, why = C.feed_decision(res)
        if decision == "exclude":
            drops[f"excluded: {why}"] += 1
            if why.startswith(("hybrid", "on-site")):
                if drops[f"excluded: {why}"] <= LOG_SAMPLE:
                    removed.append(f"{why} (sample) | {tag}")
            else:
                removed.append(f"{why} | {tag}")
            continue
        if decision == "review":
            drops["sent-to-review"] += 1
            removed.append(f"review: {why} | {tag}")
            review.append({
                "title": title, "company": j["company"], "url": url, "location": j.get("location"),
                "reason": why, "scores": res["scores"], "evidence": res["evidence"][:4],
                "unresolved": res["unresolvedQuestions"], "source": j["source"],
            })
            continue
        j["result"] = res
        keep.append(j)
    print("  Gate summary:")
    for k, v in drops.most_common():
        print(f"    {k}: {v}")
    return keep


def dedupe(items, removed):
    """Cross-source duplicates by company + title (+ location). Prefer ATS, keep earliest date."""
    priority = {"Greenhouse": 0, "Lever": 0, "Ashby": 0, "Jobicy": 1}
    items.sort(key=lambda x: (priority.get(x["source"], 2), x["posted"]))
    seen, out = {}, []
    for j in items:
        k = (norm_key(j["company"]), norm_key(j["title"]), norm_key(j.get("location", "")))
        if k in seen:
            first = seen[k]
            if j["posted"] < first["posted"]:
                first["posted"] = j["posted"]
            removed.append(f"duplicate | {j['title']} | {j['company']} | {j['url']}")
            continue
        seen[k] = j
        out.append(j)
    print(f"  After cross-source dedupe: {len(out)}")
    return out


capped_out = [0]


def cap_per_company(items, removed):
    items.sort(key=lambda x: x["posted"], reverse=True)
    counts, out = Counter(), []
    for j in items:
        c = norm_key(j["company"])
        if counts[c] < MAX_PER_COMPANY:
            counts[c] += 1
            out.append(j)
        else:
            capped_out[0] += 1
    return out


def check_links(items, removed):
    ok = []
    with ThreadPoolExecutor(max_workers=24) as ex:
        fmap = {ex.submit(verify_link, j["url"]): j for j in items}
        for f in as_completed(fmap):
            j = fmap[f]
            try:
                good = f.result()
            except Exception:
                good = False
            if good:
                ok.append(j)
            else:
                removed.append(f"link-dead | {j['title']} | {j['company']} | {j['url']}")
    return ok


def load_previous():
    try:
        prev = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
        return {p["sourceUrl"]: p.get("firstSeenAt") for p in prev if p.get("sourceUrl")}
    except (OSError, ValueError, KeyError, TypeError):
        return {}


def to_record(j, first_seen):
    r = j["result"]
    el = r["eligibility"]
    desc = C.clean_text(j.get("description", ""))
    return {
        "id": "j" + hashlib.sha1(j["url"].encode()).hexdigest()[:10],
        "title": html.unescape(j["title"]),
        "company": html.unescape(j["company"]),
        "category": r["primaryCategory"],
        "categories": r["categories"],
        "jobType": ", ".join(r["employmentTypes"]),
        "level": r["experience"]["level"],
        "yearsExperienceMin": r["experience"]["yearsMin"],
        "equivalentExperienceAccepted": r["experience"]["equivalentExperienceAccepted"],
        "qualificationsMentioned": r["experience"]["qualificationsMentioned"],
        "regionAsStated": j.get("location") or "Remote",
        "workArrangement": r["workArrangement"],
        "workArrangementLabel": ARRANGEMENT_LABEL.get(r["workArrangement"], r["workArrangement"]),
        "officeAttendance": r["officeAttendance"],
        "classificationConfidence": r["confidence"],
        "unresolvedQuestions": r["unresolvedQuestions"],
        "evidence": [{"signal": e["signal"], "text": e["text"], "effect": e["effect"]} for e in r["evidence"][:3]],
        "eligibility": {
            "type": el["type"], "label": el["label"], "countries": [] if el["type"] == "region" else el["countries"], "regions": el["regions"],
            "authorizationRequired": el["authorizationRequired"], "contractorNote": el["contractorNote"],
            "confidence": el["confidence"], "notes": el["notes"][:3],
        },
        "salaryText": j.get("salary"),
        "postedAt": j["posted"].isoformat(),
        "applyBefore": None,
        "sourceName": j["source"],
        "sourceUrl": j["url"],
        "firstSeenAt": first_seen or NOW.isoformat(),
        "lastVerifiedAt": NOW.isoformat(),
        "flags": r["quality"]["flags"] + r["flags"],
        "description": desc[:300],
    }


def pct(n, d):
    return round(100 * n / d, 1) if d else 0.0


def build_metrics(records, raw_count, removed_count, dead_links, reviewed):
    n = len(records)
    confirmed = sum(1 for r in records if r["workArrangement"] in (C.FULLY_REMOTE, C.REMOTE_RESTRICTED) and r["classificationConfidence"] != "low")
    stated = sum(1 for r in records if r["eligibility"]["type"] != "unclear")
    return {
        "generatedAt": NOW.isoformat(),
        "activeListings": n,
        "rawCandidates": raw_count,
        "sentToReview": reviewed,
        "brokenLinksDropped": dead_links,
        "percentConfirmedRemote": pct(confirmed, n),
        "percentWithStatedEligibility": pct(stated, n),
        "byArrangement": dict(Counter(r["workArrangement"] for r in records)),
        "byEligibilityType": dict(Counter(r["eligibility"]["type"] for r in records)),
        "byLevel": dict(Counter(r["level"] for r in records)),
        "byCategory": dict(Counter(r["category"] for r in records)),
        "bySource": dict(Counter(r["sourceName"] for r in records)),
        "uniqueCompanies": len({r["company"] for r in records}),
        "note": "Search-to-apply click-through and user engagement come from GoatCounter, not this file.",
    }


def main():
    removed, review = [], []
    boards = load_boards()
    print("=== Discover ===")
    raw = fetch_all(boards)
    print(f"  Raw candidates: {len(raw)}")

    print("=== Classify and gate ===")
    keep = process(raw, removed, review)
    print(f"  Eligible after classification: {len(keep)}")
    keep = dedupe(keep, removed)
    keep = cap_per_company(keep, removed)
    print(f"  After per-company cap: {len(keep)}")

    print("=== Verify links ===")
    before = len(keep)
    keep = check_links(keep, removed)
    dead = before - len(keep)
    print(f"  Links OK: {len(keep)} (dropped {dead})")

    keep.sort(key=lambda x: x["posted"], reverse=True)
    keep = keep[:MAX_LISTINGS]
    prev = load_previous()
    records = [to_record(j, prev.get(j["url"])) for j in keep]

    OUTPUT_FILE.write_text("[\n" + ",\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n]\n", encoding="utf-8")
    REVIEW_FILE.write_text(json.dumps(review[:REVIEW_LIMIT], indent=1, ensure_ascii=False), encoding="utf-8")
    metrics = build_metrics(records, len(raw), len(removed), dead, len(review))
    METRICS_FILE.write_text(json.dumps(metrics, indent=1), encoding="utf-8")
    REMOVED_LOG.parent.mkdir(parents=True, exist_ok=True)
    header = [f"# Removed listings, {NOW.isoformat()}",
              f"# Routine exclusions are counted, not listed: hybrid/on-site/no remote evidence and company-cap ({capped_out[0]} over the per-company cap).",
              f"# Up to {LOG_SAMPLE} sample lines are kept for each hybrid/on-site reason so the reasoning can be checked."]
    REMOVED_LOG.write_text("\n".join(header + removed) + "\n", encoding="utf-8")

    print(f"\nPublished {len(records)} listings, {len(review)} sent to review, {len(removed)} removal entries.")
    for k in ("byArrangement", "byEligibilityType", "byLevel", "byCategory"):
        print(f"  {k}: {metrics[k]}")


if __name__ == "__main__":
    main()
