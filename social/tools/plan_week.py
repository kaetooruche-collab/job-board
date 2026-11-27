#!/usr/bin/env python3
"""Draft a week's posts (Tue to Mon) as social/calendar/<tuesday>.posts.json, from the live feed, the hook bank and
the tip library. The Monday session finishes anything marked needs_writing, then the checker and the calendar page run.

    python3 social/tools/plan_week.py 2026-12-15            # the Tuesday that starts the week
    python3 social/tools/plan_week.py 2026-12-15 --feed jobs.json --force

Slots follow the format plan (social/research/2026-11-27-formats-and-colour.md). Until state.json says
formats_plan_approved, every post goes to all three platforms as one file, as in weeks 1 and 2.
Nothing here schedules or publishes.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_post  # noqa: E402
import feed  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
CAL = ROOT / "social" / "calendar"
DATA = ROOT / "social" / "data"
PLATFORMS = ["instagram", "tiktok", "facebook"]
TAGS = {"roles": "#remotejobs #remotework #jobsearch #hiring", "video": "#remotejobs #remotework #jobsearch #workfromhome"}
GOALS = {
    "weekly-video": ("awareness", "2-second hold rate and profile visits (TikTok Studio, Instagram Insights)"),
    "roles-carousel": ("consideration", "board visits from the bio link (GoatCounter by utm_source) and saves"),
    "role-single": ("consideration", "board visits from the bio link (GoatCounter by utm_source)"),
    "tips": ("awareness", "saves and shares (Buffer, platform insights)"),
    "safety": ("awareness", "saves and shares (Buffer, platform insights)"),
}
# Day offset from Tuesday, series. Sunday is left empty (research/2026-11-26-posting-times.md).
SLOTS = [(0, "weekly-video"), (1, "roles-carousel"), (2, "tips"), (3, "role-single"), (4, "roles-carousel"), (6, "safety")]


def history(exclude: str | None = None) -> list[dict]:
    """Every planned post, plus everything published outside the calendars (social/post-log.csv)."""
    import csv
    out = [p for f in sorted(CAL.glob("*.posts.json")) if f.name != exclude for p in check_post.load_posts(f)]
    log = ROOT / "social" / "post-log.csv"
    if log.exists():
        for r in csv.DictReader(log.open(encoding="utf-8")):
            if r.get("hook") and r.get("published_at_utc"):
                out.append({"id": r["post_id"], "date": r["published_at_utc"][:10], "hook": r["hook"], "series": r.get("series")})
    return out


def pick_hook(series: str, date: str, used: list[dict], stats: dict) -> str | None:
    """Least recently used line from the bank that is not like any hook used in the last 60 days."""
    bank = json.loads((DATA / "hook_bank.json").read_text(encoding="utf-8")).get(series, [])
    d = dt.date.fromisoformat(date)
    recent = [check_post._norm_hook(p) for p in used
              if p.get("date") and abs((d - dt.date.fromisoformat(p["date"])).days) <= 60]
    def last_use(line):
        dates = [p["date"] for p in used if SequenceMatcher(None, check_post._norm_hook({"hook": line}), check_post._norm_hook(p)).ratio() >= 0.8]
        return max(dates) if dates else ""
    for line in sorted(bank, key=last_use):
        try:
            filled = line.format(**stats)
        except (KeyError, IndexError):
            filled = line
        n = check_post._norm_hook({"hook": filled})
        if all(SequenceMatcher(None, n, r).ratio() < 0.8 for r in recent):
            return filled
    return None


def pick_tip_set(series: str, used: list[dict]) -> tuple[str, dict] | None:
    sets = json.loads((DATA / "tip_sets.json").read_text(encoding="utf-8"))["sets"]
    usage = {k: max([p["date"] for p in used if p.get("tip_set") == k] + [v.get("first_used", "")]) for k, v in sets.items()}
    cands = sorted((k for k, v in sets.items() if v["series"] == series), key=lambda k: usage[k])
    return (cands[0], sets[cands[0]]) if cands else None


def roles_post(pid, date, series, hook, count, stats):
    plain = series == "role-single"
    slides = ([{"t": "jobs", "count": 1, "worldwide_only": True}] if plain else [
        {"t": "cover", "kicker": "Open beyond one country", "title": hook.rstrip("."), "sub": "Each is open worldwide, or across a whole region. Swipe for the details."},
        {"t": "jobs", "count": count},
        {"t": "cta", "title": "Find yours on the board", "sub": "Type where you live and see only the jobs open to you."}])
    body = ("Where you can apply from, the posted date and the pay (if the posting states it) are on the card. The original posting is one tap away on the board."
            if plain else "Each is open worldwide or across a whole region, and we opened every posting today to check it's still live. Swipe for where you can apply from, the posted date and the pay, if stated.")
    caption = f"{hook}\n\n{body}\n\nLink in bio. Check each employer's rules for your country before you apply.\n\n{TAGS['roles']}"
    return {"id": pid, "date": date, "pillar": "jobs", "format": "image" if plain else "carousel", "series": series,
            "title": f"Real roles ({'single image' if plain else 'carousel'})", "hook": hook, "caption": caption,
            "visuals": "Role cards picked on the day from the live feed (renderer rules).", "render": {"slides": slides},
            "variable": "Hook wording (rotated from the bank).", "featured_jobs": [], "measured_on": stats["measured_on"],
            "number_dated_on_screen": True}


def build(tuesday: str, jobs: list[dict], state: dict) -> dict:
    t = dt.date.fromisoformat(tuesday)
    if t.weekday() != 1:
        raise SystemExit(f"{tuesday} is not a Tuesday")
    stats = feed.stats(jobs)
    used = history(exclude=f"{tuesday}.posts.json")
    wk = f"w{t.isocalendar()[1]}"
    posts = []
    for n, (offset, series) in enumerate(SLOTS, 1):
        date = (t + dt.timedelta(days=offset)).isoformat()
        pid = f"{wk}-p{n}"
        hook = pick_hook(series, date, used + posts, stats)
        if series in ("roles-carousel", "role-single"):
            p = roles_post(pid, date, series, hook or "Remote roles open beyond one country.", 3, stats)
            if not hook:
                p["needs_writing"] = "hook bank exhausted for this series: write a new hook and add it to hook_bank.json"
        elif series in ("tips", "safety"):
            ts = pick_tip_set(series, used + posts)
            if not ts:
                p = {"id": pid, "date": date, "series": series, "needs_writing": "no tip set for this series: write one"}
            else:
                key, s = ts
                h = hook or s["slides"][0].get("title", "")
                s = json.loads(json.dumps(s))
                if s["slides"] and s["slides"][0].get("t") == "cover":
                    s["slides"][0]["title"] = h.rstrip(".")   # the image's first slide carries the new hook too
                p = {"id": pid, "date": date, "pillar": "tips", "format": "carousel", "series": series, "tip_set": key,
                     "title": f"Tip: {key.replace('-', ' ')}", "hook": h,
                     "caption": f"{h}\n\n{s['caption_body']}\n\n{s['hashtags']}",
                     "visuals": "Tip carousel from the library.", "variable": "Hook wording on a reused tip set.",
                     "render": {"date_line": "Yireh Careers tips", "slides": s["slides"]}}
        else:  # weekly video
            p = {"id": pid, "date": date, "pillar": "proof", "format": "video", "series": series, "hook": hook or "",
                 "title": "Weekly video", "ai_presenter": True, "ai_voice": True, "ai_label": True,
                 "needs_writing": "script, on-screen lines and caption (Monday session, video recipe); or the free screen-only version",
                 "caption": "", "script": "", "on_screen": [], "visuals": "Presenter hook and close, live-board footage in the middle.",
                 "variable": "Opening line.", "measured_on": stats["measured_on"], "number_dated_on_screen": True}
        p.setdefault("platforms", PLATFORMS)
        p.setdefault("time_utc", state.get("posting_time_utc", "15:00"))
        p["day"] = dt.date.fromisoformat(date).strftime("%a")
        p.setdefault("funnel", GOALS[series][0])
        p.setdefault("goal_metric", GOALS[series][1])
        posts.append(p)
    return {"week": tuesday, "title": f"Week of Tuesday {t.day} {t:%B %Y}",
            "status": f"DRAFT by plan_week.py ({dt.date.today().isoformat()}). Mode: {state.get('mode')}. Posts marked needs_writing are finished in the Monday session.",
            "measured_on": stats["measured_on"], "test": "Hook wording per series (rotated); see each post.", "posts": posts}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("tuesday")
    ap.add_argument("--feed")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args(argv)
    out = CAL / f"{a.tuesday}.posts.json"
    if out.exists() and not a.force:
        raise SystemExit(f"{out.name} exists (use --force to replace a draft)")
    state = json.loads((ROOT / "social" / "state.json").read_text(encoding="utf-8"))
    week = build(a.tuesday, feed.load(a.feed), state)
    out.write_text(json.dumps(week, indent=2, ensure_ascii=False), encoding="utf-8")
    todo = [p["id"] for p in week["posts"] if p.get("needs_writing")]
    print(out, f"{len(week['posts'])} posts;", "needs writing: " + (", ".join(todo) if todo else "none"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
