#!/usr/bin/env python3
"""The publishing gate. Builds the exact Buffer `create_post` arguments for a day's posts, or refuses and says why.

    python3 social/tools/buffer_payloads.py social/calendar/2026-12-01.posts.json --date 2026-12-02
    python3 social/tools/buffer_payloads.py ... --date 2026-12-02 --dry-run      # explain the gate without the mode check

The session then calls the Buffer MCP tool `create_post` once per payload, exactly as printed, and records each
returned post id with `--record <post_id>:<platform>:<buffer_id>` (appends to social/post-log.csv).
Refuses when: state.json mode is drafts-only or hold, or approve-week without KT's recorded yes for this week;
check_post.py fails in schedule mode; numbers were not measured on the post day; a featured role was not
re-opened that day; or any image URL is not publicly reachable (push the branch first).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import sys
import urllib.request
from pathlib import Path
from zoneinfo import ZoneInfo

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_post  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RAW = "https://raw.githubusercontent.com/kaetooruche-collab/job-board/claude/social-agency/"
CHANNELS = {"facebook": "6b0931cb8541f09ecbbe07af", "tiktok": "6b092ffc8541f09ecbbdfa1d",
            "instagram": "6b092f368541f09ecbbdf3ab"}
ACCOUNT_TZ = ZoneInfo("Europe/Istanbul")   # Buffer account time zone (get_account, 27 Nov 2026)


class Refused(Exception):
    pass


def approval_deadline(week: str) -> dt.datetime:
    """23:00 Istanbul on the Monday before the week's Tuesday. After it, with no answer from KT, only KT-approved
    material may go out (backup.py; KT, 27 Nov 2026: "I need to check and approve ... if I can't check, a good
    back-up solution should exist")."""
    t = dt.date.fromisoformat(week)
    return dt.datetime.combine(t - dt.timedelta(days=1), dt.time(23, 0), tzinfo=ACCOUNT_TZ)


def week_status(state: dict, week: str, now: dt.datetime | None = None) -> str:
    """'yes' (KT said yes), 'no' (KT said no), 'backup' (deadline passed, no answer: approved material only), 'waiting'."""
    kt = [a for a in state.get("approvals", []) if a.get("week") == week and a.get("by") == "KT" and "post" not in a]
    if any(a.get("decision") == "no" for a in kt):
        return "no"
    if kt:
        return "yes"
    now = now or dt.datetime.now(ACCOUNT_TZ)
    if state.get("backup_after_deadline") == "approved-material-only" and now >= approval_deadline(week):
        return "backup"
    return "waiting"


def gate_mode(state: dict, week: str, now: dt.datetime | None = None) -> None:
    mode = state.get("mode")
    if mode in ("drafts-only", "hold", None):
        raise Refused(f"state.json mode is '{mode}': nothing may be scheduled")
    if mode in ("approve-week", "autopilot"):
        st = week_status(state, week, now)
        if st == "no":
            raise Refused(f"KT said no to week {week}")
        if mode == "approve-week" and st == "waiting":
            raise Refused(f"week {week}: waiting for KT's yes; after {approval_deadline(week).isoformat()} only approved material may go out")


def alt_text(slide_path: Path, manifest: dict, i: int) -> str:
    jobs = manifest.get("jobs") or []
    return f"Yireh Careers post, slide {i}" + (f": {jobs[0]['title']} at {jobs[0]['company']}" if len(jobs) == 1 else "")


def url_ok(url: str) -> bool:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, method="HEAD"), timeout=20) as r:
            return r.status == 200
    except Exception:
        return False


BOARD = "https://yirehcareers.vercel.app/"
STORY_SERIES = ("roles-carousel",)   # format plan: an Instagram Story with a link sticker on roles days


def facebook_text(post: dict) -> str:
    """Facebook captions can carry a clickable link (assets and a link card can't be combined in Buffer), so the
    'link in bio' line becomes a tagged link to the board: per-post clicks in GoatCounter."""
    url = f"{BOARD}?utm_source=facebook&utm_campaign={post['id']}"
    text = post["caption"]
    for old in ("Link in bio.", "More on the board: link in bio.", "link in bio."):
        if old in text:
            new = text.replace(old, f"See them on the board: {url}" if post.get("pillar") == "jobs" else f"On the board: {url}", 1)
            return new.replace(f"{url} ", f"{url}\n\n", 1)   # keep the link on its own line
    return text + f"\n\n{url}"


def story_image(src: Path) -> Path:
    """Slide 1 (1080x1350) padded onto a 1080x1920 navy canvas for a Story."""
    import subprocess
    out = src.parent / "story.jpg"
    if not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vf",
                        "pad=1080:1920:0:285:color=0x131c35", "-q:v", "3", str(out)], check=True)
    return out


def payloads_for(post: dict, today: str, check_urls: bool = True, formats: bool = False, backup_only: list | None = None) -> list[dict]:
    if backup_only is not None:
        import backup
        if not backup.is_approved_material(post, backup_only):
            raise Refused(f"{post['id']}: KT hasn't approved this week and this post isn't approved material (run backup.py)")
    fs = [f for f in check_post.check_post(post, "schedule") if f.level == check_post.BLOCK]
    if fs:
        raise Refused(f"{post['id']}: " + "; ".join(str(f) for f in fs))
    d = ROOT / "social" / "output" / post["date"] / post["id"]
    images = sorted(d.glob("[0-9][0-9].jpg"))
    videos = sorted(d.glob("*.mp4"))
    manifest = json.loads((d / "manifest.json").read_text(encoding="utf-8")) if (d / "manifest.json").exists() else {}
    if post.get("render") and not images:
        raise Refused(f"{post['id']}: no rendered images in {d.relative_to(ROOT)}")
    if formats and post.get("series") == "role-single" and not videos:
        raise Refused(f"{post['id']}: format plan: the single-role post goes out as a short video (run slides_to_video.py)")
    if post.get("format") == "video" and not videos:
        raise Refused(f"{post['id']}: no video file in {d.relative_to(ROOT)}")
    for j in manifest.get("jobs", []):
        c = j.get("check") or {}
        if not c.get("ok") or c.get("checked_open_on") != today:
            raise Refused(f"{post['id']}: featured role {j['id']} not confirmed open today (run verify-open.js)")
        sc = j.get("source_check") or {}
        if not sc.get("ok") or sc.get("checked_on") != today:
            raise Refused(f"{post['id']}: featured role {j['id']} not matched to the employer's own data today "
                          f"(verify_source.py): {sc.get('reason', 'not checked')}")
    media = [("video", v) for v in videos] or [("image", im) for im in images]
    story = story_image(images[0]) if (formats and post.get("series") in STORY_SERIES and images
                                       and "instagram" in post["platforms"]) else None
    urls = [RAW + str(p.relative_to(ROOT)) for _, p in media]
    if story:
        urls_story = RAW + str(story.relative_to(ROOT))
    if check_urls:
        bad = [u for u in urls + ([urls_story] if story else []) if not url_ok(u)]
        if bad:
            raise Refused(f"{post['id']}: not publicly reachable yet (commit and push first): {bad[0]}")
    hh, mm = map(int, post.get("time_utc", "15:00").split(":"))
    due = dt.datetime.fromisoformat(post["date"]).replace(hour=hh, minute=mm, tzinfo=dt.timezone.utc).astimezone(ACCOUNT_TZ)
    if due <= dt.datetime.now(ACCOUNT_TZ) + dt.timedelta(hours=2):
        raise Refused(f"{post['id']}: due {due.isoformat()} is less than 2 hours away (skill rule)")
    ai = bool(post.get("ai_presenter") or post.get("ai_voice"))
    out = []
    for plat in post["platforms"]:
        assets = []
        for i, ((kind, p), u) in enumerate(zip(media, urls), 1):
            assets.append({"video": {"url": u}} if kind == "video" else
                          {"image": {"url": u, "metadata": {"altText": alt_text(p, manifest, i)}}})
        meta: dict = {}
        if plat == "instagram":
            meta["instagram"] = {"type": "reel" if videos else "post", "shouldShareToFeed": True}
            if ai and videos:
                meta["instagram"]["isAiGenerated"] = True
        elif plat == "facebook":
            if ai and videos:
                raise Refused(f"{post['id']}: Buffer cannot set Facebook's AI label; post the screen-only version to Facebook or let KT tick 'AI info'")
            meta["facebook"] = {"type": "reel" if videos else "post"}
        elif plat == "tiktok":
            meta["tiktok"] = {"isAiGenerated": True} if (ai and videos) else {}
        text = facebook_text(post) if (formats and plat == "facebook") else post["caption"]
        out.append({"_post": post["id"], "_platform": plat, "channelId": CHANNELS[plat], "schedulingType": "automatic",
                    "mode": "customScheduled", "dueAt": due.isoformat(), "text": text, "assets": assets,
                    "metadata": meta})
    if story:
        out.append({"_post": post["id"], "_platform": "instagram_story", "channelId": CHANNELS["instagram"],
                    "schedulingType": "automatic", "mode": "customScheduled",
                    "dueAt": (due + dt.timedelta(minutes=30)).isoformat(), "text": "",
                    "assets": [{"image": {"url": urls_story, "metadata": {"altText": alt_text(story, manifest, 1)}}}],
                    "metadata": {"instagram": {"type": "story", "shouldShareToFeed": False,
                                               "link": f"{BOARD}?utm_source=instagram_story&utm_campaign={post['id']}"}}})
    return out


def record(arg: str, posts: dict) -> None:
    pid, plat, bid = arg.split(":")
    p = posts[pid]
    path = ROOT / "social" / "post-log.csv"
    hdr = path.read_text(encoding="utf-8").splitlines()[0].split(",")
    with path.open("a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=hdr).writerow({k: "" for k in hdr} | {
            "post_id": pid, "platform": plat, "published_at_utc": f"{p['date']}T{p.get('time_utc', '15:00')}:00Z (scheduled)",
            "buffer_post_id": bid, "series": p.get("series", ""), "funnel": p.get("funnel", ""),
            "goal_metric": p.get("goal_metric", ""), "hook": p.get("hook", "")})
    print("recorded", pid, plat, bid)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("posts")
    ap.add_argument("--date", help="post day (YYYY-MM-DD); also the day numbers and roles must have been checked")
    ap.add_argument("--dry-run", action="store_true", help="skip the mode check and URL check; still apply every other rule")
    ap.add_argument("--record", action="append", default=[])
    a = ap.parse_args(argv)
    data = json.loads(Path(a.posts).read_text(encoding="utf-8"))
    posts = {p["id"]: p for p in data["posts"]}
    if a.record:
        for r in a.record:
            record(r, posts)
        return 0
    state = json.loads((ROOT / "social" / "state.json").read_text(encoding="utf-8"))
    today = dt.date.today().isoformat()
    try:
        if not a.dry_run:
            gate_mode(state, data["week"])
        todays = [p for p in data["posts"] if p["date"] == a.date]
        if not todays:
            raise Refused(f"no posts dated {a.date} in {a.posts}")
        fmt = bool(state.get("formats_plan_approved"))
        lib = None
        if not a.dry_run and week_status(state, data["week"]) == "backup":
            import backup
            lib = backup.approved_posts(state)
        out = [x for p in todays for x in payloads_for(p, today, check_urls=not a.dry_run, formats=fmt, backup_only=lib)]
    except Refused as e:
        print(json.dumps({"refused": str(e)}, indent=2))
        return 1
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
