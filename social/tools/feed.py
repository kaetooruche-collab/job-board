#!/usr/bin/env python3
"""Read the LIVE job feed, measure it, and pick roles for posts.

Facts about jobs come only from https://yirehcareers.vercel.app/jobs.json, fetched the day a post is made
(skill: Boundaries). Nothing here writes to the site or the pipeline.

    python3 social/tools/feed.py stats            # today's numbers, as JSON
    python3 social/tools/feed.py wide --limit 10  # roles open to many countries, newest first
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.request
from pathlib import Path

FEED_URL = "https://yirehcareers.vercel.app/jobs.json"
SITE = "https://yirehcareers.vercel.app/"

# Audience scope. KT decided 26 Nov 2026: "people outside the US, wherever they live" (drafts/decisions/
# 2026-11-26-who-to-target.md). "africa_asia" (the first brief) stays available via YC_SOCIAL_SCOPE.
import os
SCOPES = {
    "africa_asia": {"EMEA", "Africa", "APAC", "Asia", "Asia Pacific", "Europe, Middle East, Africa"},
    "outside_us": {"EMEA", "Africa", "APAC", "Asia", "Asia Pacific", "Europe, Middle East, Africa", "Europe",
                   "European Union", "Latin America", "South America", "Caribbean", "Middle East", "ANZ", "Americas", "North America"},
}
SCOPE = os.environ.get("YC_SOCIAL_SCOPE", "outside_us")
AUDIENCE_REGIONS = SCOPES[SCOPE]
# Companies whose names are hiring systems: never featured (no post names a hiring system).
SKIP_COMPANIES = {"ashby", "greenhouse", "lever", "workable", "personio", "recruitee", "workday"}
EXCLUDE_FILE = Path(__file__).resolve().parents[1] / "data" / "exclude_jobs.json"


def excluded() -> dict:
    try:
        return json.loads(EXCLUDE_FILE.read_text(encoding="utf-8")).get("jobs", {})
    except (OSError, json.JSONDecodeError):
        return {}


NOT_A_JOB = re.compile(r"talent (?:community|pool|network)|stay in touch|general application|open application", re.I)


def load(path: str | None = None) -> list[dict]:
    if path:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    else:
        req = urllib.request.Request(FEED_URL, headers={"User-Agent": "Mozilla/5.0 (YirehSocial)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read().decode("utf-8"))
    return data["jobs"] if isinstance(data, dict) else data


def apply_from(job: dict) -> str | None:
    """Mirror of card-text.js applyFrom(): the site's own words for where you can apply from."""
    el = job.get("eligibility") or {}
    if el.get("type") == "worldwide":
        return "Worldwide"
    if el.get("type") == "unclear" or not el.get("label"):
        return None
    return re.sub(r" only$", "", el["label"])


def posted(job: dict) -> dt.datetime:
    return dt.datetime.fromisoformat(job["postedAt"].replace("Z", "+00:00"))


def is_audience_open(job: dict) -> bool:
    el = job.get("eligibility") or {}
    if el.get("type") == "worldwide":
        return True
    if el.get("type") == "region":
        return bool(set(el.get("regions") or []) & AUDIENCE_REGIONS)
    return False


def featurable(job: dict, now: dt.datetime, max_age_days: int = 14) -> bool:
    if job.get("id") in excluded():
        return False
    if not is_audience_open(job):
        return False
    if NOT_A_JOB.search(job.get("title", "")):
        return False
    if job.get("company", "").strip().lower() in SKIP_COMPANIES:
        return False
    notes = " ".join((job.get("eligibility") or {}).get("notes") or []) + " " + " ".join(job.get("unresolvedQuestions") or [])
    if re.search(r"cannot hire in|office or in-person|in-person onboarding", notes, re.I):
        return False
    return (now - posted(job)).days <= max_age_days


def wide(jobs: list[dict], now: dt.datetime | None = None, limit: int = 10, max_age_days: int = 14,
         spread: bool = True, worldwide_only: bool = False) -> list[dict]:
    """Roles open to our audience, newest first; with spread, at most 2 per company and categories mixed."""
    now = now or dt.datetime.now(dt.timezone.utc)
    pool = sorted((j for j in jobs if featurable(j, now, max_age_days)
                   and (not worldwide_only or (j.get("eligibility") or {}).get("type") == "worldwide")),
                  key=posted, reverse=True)
    if not spread:
        return pool[:limit]
    out, per_co, seen_cat = [], {}, {}
    for rnd in range(3):  # first pass favours new categories, later passes fill
        for j in pool:
            if j in out or len(out) >= limit:
                continue
            co = j["company"].strip()
            if per_co.get(co, 0) >= 2:
                continue
            if rnd == 0 and seen_cat.get(j["category"], 0) >= 1:
                continue
            out.append(j)
            per_co[co] = per_co.get(co, 0) + 1
            seen_cat[j["category"]] = seen_cat.get(j["category"], 0) + 1
    return sorted(out, key=posted, reverse=True)


def stats(jobs: list[dict], now: dt.datetime | None = None) -> dict:
    now = now or dt.datetime.now(dt.timezone.utc)
    el = [j.get("eligibility") or {} for j in jobs]
    us_only = sum(1 for e in el if e.get("label") == "United States only")
    return {
        "measured_at": now.strftime("%Y-%m-%d %H:%M UTC"),
        "measured_on": now.strftime("%Y-%m-%d"),
        "jobs": len(jobs),
        "companies": len({j["company"].strip() for j in jobs}),
        "posted_last_7_days": sum(1 for j in jobs if (now - posted(j)).days < 7),
        "worldwide": sum(1 for e in el if e.get("type") == "worldwide"),
        "region_wide": sum(1 for e in el if e.get("type") == "region"),
        "open_to_audience_regions": sum(1 for j in jobs if is_audience_open(j)),
        "location_not_specified": sum(1 for e in el if e.get("type") == "unclear"),
        "single_country": sum(1 for e in el if e.get("type") == "countries" and len(e.get("countries") or []) == 1),
        "us_only": us_only,
        "us_only_pct": round(100 * us_only / len(jobs), 1) if jobs else 0,
        "single_country_pct": round(100 * sum(1 for e in el if e.get("type") == "countries" and len(e.get("countries") or []) == 1) / len(jobs)) if jobs else 0,
        "pay_stated": sum(1 for j in jobs if j.get("salaryText")),
        "entry_or_junior": sum(1 for j in jobs if j.get("level") in ("entry", "junior", "internship")),
    }


def utm(platform: str, campaign: str, extra: str = "") -> str:
    return f"{SITE}{extra}?utm_source={platform}&utm_campaign={campaign}"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["stats", "wide"])
    ap.add_argument("--feed", help="local copy of jobs.json (default: fetch the live feed)")
    ap.add_argument("--limit", type=int, default=10)
    a = ap.parse_args(argv)
    jobs = load(a.feed)
    if a.cmd == "stats":
        print(json.dumps(stats(jobs), indent=2))
    else:
        for j in wide(jobs, limit=a.limit):
            print(f"{j['id']}  {posted(j):%d %b}  {apply_from(j):<28} {j['title'].strip()[:55]:<55} {j['company'].strip()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
