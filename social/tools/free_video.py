#!/usr/bin/env python3
"""The free weekly video: no presenter, no AI voice, no credits. Used when KT hasn't said yes to a BHuman render.

    python3 social/tools/free_video.py social/calendar/2026-12-01.posts.json w49-p1

Builds text slides (blue theme) from the post's approved on-screen lines, live-board footage in the middle
(record-board-footage.js, worldwide demo, no country shown), and a closing slide; writes
social/output/<date>/<id>/video.mp4. A number line is refreshed from today's feed and dated on screen. Lines that
are only about the AI presenter are dropped, and the post's AI flags are cleared (nothing AI is shown or heard).
Wording is not changed beyond that: the on-screen lines are the ones KT approved.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parents[1]
sys.path.insert(0, str(TOOLS))
import feed  # noqa: E402
import render_posts  # noqa: E402


def slides_from(lines: list[str], stats: dict) -> tuple[list[dict], int, str | None]:
    keep = [l for l in lines if "ai-generated" not in l.lower() and l.strip().lower() != "link in bio"
            and not l.lower().startswith("from our live board")]
    out = []
    date_line = None
    for l in keep:
        if re.search(r"\d", l):
            if "anywhere" in l.lower() or "worldwide" in l.lower():
                out.append({"t": "cover", "kicker": "From our live board", "title": re.sub(r"\d[\d,]*", str(stats["worldwide"]), l, count=1),
                            "sub": f"Counted on {dt.date.fromisoformat(stats['measured_on']):%-d %b %Y}"})
                date_line = f"From our live board, {dt.date.fromisoformat(stats['measured_on']):%-d %b %Y}"
            continue   # any other number can't be refreshed safely: leave it out
        out.append({"t": "cover", "kicker": "Yireh Careers" if not out else "", "title": l, "sub": ""})
    if len(out) >= 2 and not out[1]["kicker"] and not out[0]["sub"]:
        out[0]["sub"], out = out[1]["title"], [out[0]] + out[2:]   # hook + its follow-up on one slide
    out.append({"t": "cta", "title": "Link in bio", "sub": "yirehcareers.vercel.app"})
    return out, 1 if out else 0, date_line


def main(argv=None) -> int:
    argv = argv or sys.argv[1:]
    posts_file, pid = Path(argv[0]), argv[1]
    data = json.loads(posts_file.read_text(encoding="utf-8"))
    post = next(p for p in data["posts"] if p["id"] == pid)
    jobs = feed.load(None)
    stats = feed.stats(jobs)
    slides, footage_after, date_line = slides_from(post.get("on_screen") or [post.get("hook", "")], stats)
    tmp = dict(post, render={"theme": "blue", "date_line": date_line or "Yireh Careers", "slides": slides})
    made = render_posts.build([tmp], jobs, ROOT / "social" / "output", {pid}, dt.datetime.now(dt.timezone.utc))
    d = made[0]
    fdir = d / "footage"
    subprocess.run(["node", str(TOOLS / "record-board-footage.js"), "--out", str(fdir), "--seconds", "10"], check=True)
    meta = json.loads((fdir / "meta.json").read_text(encoding="utf-8"))
    fps = meta.get("fps", 10)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps), "-i", str(fdir / "frames" / "f%05d.jpg"),
                    "-vf", "scale=1080:1920,format=yuv420p", "-c:v", "libx264", str(fdir / "board.mp4")], check=True)
    subprocess.run([sys.executable, str(TOOLS / "slides_to_video.py"), str(d), "--seconds", "3",
                    "--footage", str(fdir / "board.mp4"), "--footage-after", str(footage_after)], check=True)
    import shutil
    shutil.rmtree(fdir / "frames", ignore_errors=True)
    for k in ("ai_presenter", "ai_voice", "ai_label"):
        post[k] = False
    post["free_version"] = f"Built {stats['measured_on']} without a presenter (no BHuman render approved)."
    post["measured_on"] = stats["measured_on"]
    posts_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(d / "video.mp4")
    return 0


if __name__ == "__main__":
    sys.exit(main())
