#!/usr/bin/env python3
"""Render image and carousel posts (1080x1350) from the LIVE feed, in the site's look.

    python3 social/tools/render_posts.py social/calendar/2026-12-01.posts.json            # all image/carousel posts
    python3 social/tools/render_posts.py social/calendar/2026-12-01.posts.json --only w49-p2
    python3 social/tools/render_posts.py ... --feed jobs.json --out /tmp/x                 # offline / elsewhere

Each post in the calendar carries a "render" block:
    {"slides": [
        {"t": "cover", "kicker": "...", "title": "...", "sub": "..."},
        {"t": "jobs", "count": 3},           # filled from the live feed: roles open to our audience
        {"t": "job", "id": "jabc123"},       # a specific job (fails if it has left the feed)
        {"t": "tip", "n": "1", "title": "...", "body": "..."},
        {"t": "cta", "title": "...", "sub": "..."}
    ]}
Output: social/output/<date>/<post-id>/NN.jpg plus manifest.json (the jobs used, with their posting links, for the
"still open" check: node social/tools/verify-open.js <manifest>). Numbers and the date line come from the feed
at render time, so render on the post day.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import feed  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
TOOLS = Path(__file__).resolve().parent
W, H = 1080, 1350

MARK = ("<svg viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'><defs><linearGradient id='t' x1='0' y1='0' "
        "x2='1' y2='1'><stop offset='0' stop-color='#3b82f6'/><stop offset='1' stop-color='#1d4ed8'/></linearGradient>"
        "</defs><rect width='100' height='100' rx='22' fill='url(#t)'/><g fill='none' stroke-width='12' "
        "stroke-linecap='round' stroke-linejoin='round'><path d='M25 31 L48 56' stroke='#fff'/><path d='M48 56 L48 82' "
        "stroke='#fff'/><path d='M48 56 L83 17' stroke='#bfdbfe'/></g></svg>")

CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:%(w)dpx;height:%(h)dpx}
body{font-family:'Inter',sans-serif;color:#fff;background:linear-gradient(135deg,#131c35 0%%,#0f2a4d 58%%,#17407a 100%%);
 position:relative;overflow:hidden;-webkit-font-smoothing:antialiased}
.wrap{position:absolute;inset:0;padding:84px 84px 0;display:flex;flex-direction:column}
.brand{display:flex;align-items:center;gap:20px;font-weight:700;font-size:34px;letter-spacing:-.01em}
.brand svg{width:64px;height:64px}
.count{margin-left:auto;font-weight:600;font-size:26px;color:#a9ccff}
.main{flex:1;display:flex;flex-direction:column;justify-content:center;padding-bottom:150px}
.kicker{font-size:32px;font-weight:700;color:#7cb3ff;text-transform:uppercase;letter-spacing:.08em}
h1{margin-top:30px;font-size:104px;line-height:1.04;font-weight:800;letter-spacing:-.03em;text-wrap:balance}
h1 em{font-style:normal;color:#7cb3ff}
.sub{margin-top:44px;font-size:44px;line-height:1.35;color:#dbe7ff;font-weight:500;text-wrap:pretty}
.foot{position:absolute;left:84px;right:84px;bottom:64px;display:flex;justify-content:space-between;align-items:flex-end;
 font-size:24px;color:#a9ccff;font-weight:500}
.foot b{color:#fff;font-weight:700}
.card{background:#fff;color:#1a1a2e;border-radius:28px;padding:60px 56px;box-shadow:0 24px 60px rgba(0,0,0,.35)}
.pills{display:flex;flex-wrap:wrap;gap:14px}
.pill{font-size:30px;font-weight:600;padding:10px 24px;border-radius:999px;line-height:1.3}
.pill-world{background:#f0fdfa;color:#0d9488}.pill-region{background:#eff6ff;color:#2563eb}
.pill-quiet{background:#f1f3f5;color:#5f6368;font-weight:500}
.title{margin-top:38px;font-size:68px;line-height:1.1;font-weight:800;letter-spacing:-.02em;text-wrap:balance}
.co{margin-top:20px;font-size:40px;color:#5f6368;font-weight:600}
.rows{margin-top:44px;border-top:2px solid #e2e5e9;padding-top:30px;display:grid;grid-template-columns:auto 1fr;gap:20px 32px;font-size:34px}
.rows dt{color:#5f6368;font-weight:500}.rows dd{font-weight:600}
.btn{margin-top:48px;display:inline-block;background:#2563eb;color:#fff;font-weight:700;font-size:32px;padding:22px 38px;border-radius:14px}
.tipn{width:132px;height:132px;border-radius:30px;background:#2563eb;display:flex;align-items:center;
 justify-content:center;font-size:64px;font-weight:800}
.big{margin-top:44px;font-size:96px}
.url{margin-top:54px;display:inline-block;background:#fff;color:#1d4ed8;font-weight:800;font-size:44px;padding:24px 40px;border-radius:18px}
""" % {"w": W, "h": H}


def esc(s) -> str:
    """HTML-escape, with typographic apostrophes so straight and curly quotes never mix on a slide."""
    return html.escape(re.sub(r"(?<=\w)'(?=\w)", "\u2019", str(s or "")), quote=True)


def page(inner: str, idx: int, total: int, date_line: str) -> str:
    count = f"<span class='count'>{idx} / {total}</span>" if total > 1 else ""
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='wrap'>"
            f"<div class='brand'>{MARK}<span>Yireh Careers</span>{count}</div><div class='main'>{inner}</div></div>"
            f"<div class='foot'><span>{esc(date_line)}</span><span><b>Link in bio</b></span></div></body></html>")


def fmt_day(d: dt.datetime) -> str:
    return f"{d.day} {d:%b %Y}"


def job_slide(j: dict) -> str:
    af = feed.apply_from(j) or "Location not specified"
    cls = "pill-world" if af == "Worldwide" else "pill-region"
    lead = "" if af in ("Worldwide", "Location not specified") else "Apply from: "
    pay = j.get("salaryText") or "Not stated"
    jt = j.get("jobType") or ""
    return ("<div class='card'>"
            f"<div class='pills'><span class='pill {cls}'>{esc(lead + af)}</span><span class='pill pill-quiet'>Remote</span>"
            + (f"<span class='pill pill-quiet'>{esc(jt)}</span>" if jt else "") + "</div>"
            f"<div class='title'>{esc(j['title'].strip())}</div><div class='co'>{esc(j['company'].strip())}</div>"
            "<dl class='rows'>"
            f"<dt>Posted</dt><dd>{esc(fmt_day(feed.posted(j)))}</dd>"
            f"<dt>Pay</dt><dd>{esc(pay)}</dd>"
            "<dt>Source</dt><dd>The company&rsquo;s hiring page</dd></dl>"
            "<span class='btn'>Apply on the original posting</span></div>")


def cover(s: dict) -> str:
    return (f"<div class='kicker'>{esc(s.get('kicker'))}</div><h1>{s.get('title_html') or esc(s.get('title'))}</h1>"
            f"<div class='sub'>{esc(s.get('sub'))}</div>")


def tip(s: dict) -> str:
    return (f"<div class='tipn'>{esc(s.get('n'))}</div><h1 class='big'>{esc(s.get('title'))}</h1>"
            f"<div class='sub'>{esc(s.get('body'))}</div>")


def cta(s: dict) -> str:
    return (f"<div class='kicker'>{esc(s.get('kicker', 'Your next step'))}</div><h1>{esc(s.get('title'))}</h1>"
            f"<div class='sub'>{esc(s.get('sub'))}</div><span class='url'>yirehcareers.vercel.app</span>")


def fill(text: str, st: dict) -> str:
    """Numbers in slide text come from the feed at render time: {worldwide}, {jobs}, {companies}, ..."""
    try:
        return text.format(**st)
    except (KeyError, IndexError, ValueError):
        return text


def build(posts: list[dict], jobs: list[dict], out_root: Path, only: set[str] | None, now: dt.datetime) -> list[Path]:
    st = feed.stats(jobs, now)
    by_id = {j["id"]: j for j in jobs}
    used: set[str] = set()
    pool = feed.wide(jobs, now, limit=40)
    ww_pool = feed.wide(jobs, now, limit=40, worldwide_only=True)
    made = []
    for p in posts:
        r = p.get("render")
        if not r or (only and p["id"] not in only):
            continue
        slides, manifest_jobs = [], []
        date_line = r.get("date_line") or f"From our live board, {fmt_day(now)}"
        for s in r["slides"]:
            s = {k: (fill(v, st) if isinstance(v, str) else v) for k, v in s.items()}
            if s["t"] == "jobs":
                src = ww_pool if s.get("worldwide_only") else pool
                picks = [j for j in src if j["id"] not in used][: s.get("count", 3)]
                if len(picks) < s.get("count", 3):
                    print(f"WARNING {p['id']}: only {len(picks)} roles open to the audience are available", file=sys.stderr)
                for j in picks:
                    used.add(j["id"])
                    slides.append(job_slide(j))
                    manifest_jobs.append(j)
            elif s["t"] == "job":
                j = by_id.get(s["id"])
                if not j:
                    raise SystemExit(f"{p['id']}: job {s['id']} is no longer on the live feed; re-pick it")
                used.add(j["id"])
                slides.append(job_slide(j))
                manifest_jobs.append(j)
            else:
                slides.append({"cover": cover, "tip": tip, "cta": cta}[s["t"]](s))
        d = out_root / p["date"] / p["id"]
        d.mkdir(parents=True, exist_ok=True)
        for old in list(d.glob("*.png")) + list(d.glob("*.jpg")):
            old.unlink()
        for i, inner in enumerate(slides, 1):
            (d / f"{i:02d}.html").write_text(page(inner, i, len(slides), date_line), encoding="utf-8")
        (d / "manifest.json").write_text(json.dumps({
            "post": p["id"], "rendered_at": st["measured_at"], "stats": st,
            "jobs": [{"id": j["id"], "title": j["title"].strip(), "company": j["company"].strip(),
                      "apply_from": feed.apply_from(j), "postedAt": j["postedAt"], "salaryText": j.get("salaryText"),
                      "sourceUrl": j["sourceUrl"]} for j in manifest_jobs]}, indent=2), encoding="utf-8")
        made.append(d)
    if made:
        subprocess.run(["node", str(TOOLS / "shoot.js"), *map(str, made)], check=True)
        for d in made:
            for f in d.glob("*.html"):
                f.unlink()
    return made


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("posts")
    ap.add_argument("--feed", help="local jobs.json (default: the live feed)")
    ap.add_argument("--out", default=str(ROOT / "social" / "output"))
    ap.add_argument("--only", nargs="*")
    a = ap.parse_args(argv)
    sys.path.insert(0, str(TOOLS))
    import check_post
    posts = check_post.load_posts(Path(a.posts))
    jobs = feed.load(a.feed)
    made = build(posts, jobs, Path(a.out), set(a.only) if a.only else None, dt.datetime.now(dt.timezone.utc))
    for d in made:
        print(d, len(list(d.glob("*.jpg"))), "slides")
    return 0


if __name__ == "__main__":
    sys.exit(main())
