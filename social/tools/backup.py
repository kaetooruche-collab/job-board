#!/usr/bin/env python3
"""The backup when KT can't check a week (KT, 27 Nov 2026: "I need to check and approve before it goes out, and if
I can't check, a good back-up solution should exist").

Past the approval deadline with no answer, only KT-approved material may go out. A post is "approved material" when its
hook and caption body (numbers masked) appeared in a week KT said yes to, it has no AI presenter or voice, and it is not a
service post. Anything else is swapped for an approved post of the same series, or dropped. Live roles, numbers and
dates are still re-checked on the day; that is data, not new wording.

    python3 social/tools/backup.py social/calendar/2026-12-08.posts.json --date 2026-12-09   # rewrite that day's posts
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CAL = ROOT / "social" / "calendar"
NEVER = ("service",)
SWAP_SERIES = {"weekly-video": "roles-carousel"}   # an unapproved video becomes an approved roles post


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"\d[\d,.]*", "#", (text or "").lower())).strip()


def _body(caption: str, hook: str) -> str:
    return _norm((caption or "").replace(hook or "", "", 1))


def approved_posts(state: dict) -> list[dict]:
    weeks = {a["week"] for a in state.get("approvals", []) if a.get("by") == "KT" and a.get("decision", "yes") == "yes"}
    out = []
    for w in sorted(weeks):
        f = CAL / f"{w}.posts.json"
        if f.exists():
            out += json.loads(f.read_text(encoding="utf-8"))["posts"]
    return out


def is_approved_material(post: dict, approved: list[dict]) -> bool:
    if post.get("series") in NEVER or post.get("ai_presenter") or post.get("ai_voice") or post.get("needs_writing"):
        return False
    h, b = _norm(post.get("hook")), _body(post.get("caption"), post.get("hook"))
    return any(_norm(a.get("hook")) == h and _body(a.get("caption"), a.get("hook")) == b for a in approved)


def substitute(post: dict, approved: list[dict], used_ids: set) -> dict | None:
    want = SWAP_SERIES.get(post.get("series"), post.get("series"))
    cands = [a for a in approved if a.get("series") == want and a["id"] not in used_ids
             and is_approved_material(a, approved)]
    if not cands:
        return None
    src = cands[0]
    new = json.loads(json.dumps(src))
    for k in ("id", "date", "day", "time_utc", "platforms", "measured_on"):
        if k in post:
            new[k] = post[k]
    new["featured_jobs"] = []
    new["backup_of"] = {"original": post["id"], "replaced_with_approved": src["id"],
                        "reason": "KT did not answer before the deadline; only approved wording may go out"}
    return new


def apply(posts_file: Path, date: str, state: dict) -> list[str]:
    data = json.loads(posts_file.read_text(encoding="utf-8"))
    approved = approved_posts(state)
    used = {p.get("backup_of", {}).get("replaced_with_approved") for p in data["posts"]}
    notes, keep = [], []
    for p in data["posts"]:
        if p["date"] != date or is_approved_material(p, approved):
            keep.append(p)
            continue
        sub = substitute(p, approved, used)
        if sub:
            used.add(sub["backup_of"]["replaced_with_approved"])
            keep.append(sub)
            notes.append(f"{p['id']}: swapped for approved {sub['backup_of']['replaced_with_approved']}")
        else:
            data.setdefault("held", []).append(p)
            notes.append(f"{p['id']}: held (no approved substitute); it waits for KT")
    data["posts"] = keep
    posts_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return notes


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("posts")
    ap.add_argument("--date", required=True)
    a = ap.parse_args(argv)
    state = json.loads((ROOT / "social" / "state.json").read_text(encoding="utf-8"))
    for n in apply(Path(a.posts), a.date, state) or ["nothing to swap"]:
        print(n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
