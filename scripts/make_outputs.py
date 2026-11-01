"""Writes data/whatsapp_post.txt: the weekly WhatsApp post, 3-5 listings from the last 7 days.

Run after fetch_jobs.py. KT posts it by hand (Tuesday, after the weekly email goes out).
Only listings that read as remote are used (not "remote unclear"), at most one per company,
and the eligibility label is shown as the employer states it. Listings open to applicants
anywhere come first, because most of the board is restricted to one country or region.
Posting dates are the source's original posting date, in UTC.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_URL = "https://yirehcareers.vercel.app/"
MAX_ITEMS = 5
MIN_ITEMS = 3
MAX_AGE_HOURS = 72
WEEKLY_AGE_HOURS = 168
MAX_PER_CATEGORY = 2
LEVEL_LABEL = {
    "internship": "Internship", "entry": "Entry level", "junior": "Junior", "mid": "Mid level",
    "senior": "Senior", "leadership": "Leadership", "unspecified": "Level not stated",
}


def _parse(ts):
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def _open_to_all(r):
    el = r.get("eligibility") or {}
    return el.get("type") == "worldwide" or (el.get("label") or "").strip().lower() == "worldwide"


def pick(rows, now=None, max_age_hours=MAX_AGE_HOURS):
    now = now or datetime.now(timezone.utc)
    fresh = []
    for r in rows:
        if r.get("workArrangement") not in ("fully_remote", "remote_geo_restricted"):
            continue
        try:
            age = (now - _parse(r["postedAt"])).total_seconds() / 3600
        except (KeyError, ValueError):
            continue
        if 0 <= age <= max_age_hours:
            fresh.append(r)
    fresh.sort(key=lambda r: r["postedAt"], reverse=True)
    fresh.sort(key=lambda r: not _open_to_all(r))  # stable: open-to-all first, newest first within each group
    chosen, companies, cats = [], set(), {}
    # one early-career listing first when there is one, then the rest in the order above
    early = [r for r in fresh if r.get("level") in ("internship", "entry", "junior")]
    for r in early[:1] + fresh:
        c = r["company"].strip().lower()
        cat = r.get("category") or ""
        if c in companies or cats.get(cat, 0) >= MAX_PER_CATEGORY or r in chosen:
            continue
        chosen.append(r)
        companies.add(c)
        cats[cat] = cats.get(cat, 0) + 1
        if len(chosen) == MAX_ITEMS:
            break
    chosen.sort(key=lambda r: r["postedAt"], reverse=True)
    return chosen


def render(items, now=None):
    now = now or datetime.now(timezone.utc)
    lines = [f"*Remote jobs this week* ({now.strftime('%d %b %Y')})", ""]
    for i, r in enumerate(items, 1):
        posted = _parse(r["postedAt"]).astimezone(timezone.utc).strftime("%d %b")
        elig = (r.get("eligibility") or {}).get("label") or "Eligibility unclear"
        pay = r.get("salaryText")
        lines.append(f"{i}. *{r['title']}* at {r['company']}")
        lines.append(f"   Who can apply: {elig}")
        lines.append(f"   {LEVEL_LABEL.get(r.get('level'), 'Level not stated')} · {r.get('jobType') or 'Type not stated'}"
                     + (f" · Pay: {pay}" if pay else " · Pay: not stated"))
        lines.append(f"   Posted {posted} on {r['sourceName']}")
        lines.append(f"   {r['sourceUrl']}")
        lines.append("")
    lines.append(f"More jobs, with filters: {SITE_URL}?utm_source=whatsapp&utm_medium=channel&utm_campaign=weekly")
    lines.append("")
    lines.append("Every link goes to the original posting. Please check each employer's eligibility rules before you apply. We never charge you to apply.")
    return "\n".join(lines) + "\n"


def main():
    rows = json.loads((ROOT / "jobs.json").read_text(encoding="utf-8"))
    items = pick(rows, max_age_hours=WEEKLY_AGE_HOURS)
    out = ROOT / "data" / "whatsapp_post.txt"
    if len(items) < MIN_ITEMS:
        out.write_text(f"Not enough fresh listings for a post (found {len(items)}, need {MIN_ITEMS}).\n", encoding="utf-8")
        print(f"whatsapp_post: only {len(items)} fresh listings; wrote a note instead")
        return 0
    out.write_text(render(items), encoding="utf-8")
    print(f"whatsapp_post: wrote {len(items)} listings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
