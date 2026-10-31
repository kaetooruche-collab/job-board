#!/usr/bin/env python3
"""Weekly GoatCounter snapshot.

Pulls the funnel numbers through the GoatCounter API and writes a dated
markdown file to drafts/analytics/GC-YYYY-MM-DD.md, so the baseline in
drafts/ux-optimization-log.md can be compared week over week.

    python3 scripts/gc_snapshot.py            # snapshot for today
    python3 scripts/gc_snapshot.py --date 2026-11-03

The API key is read from the environment or the project's .env file as
GOATCOUNTER_API_KEY. It is never printed and never written anywhere.
Exit status is 0 on success, 1 when the data could not be fetched.
"""
import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
API = "https://kayzglobal.goatcounter.com/api/v0"
SINCE = "2026-09-01T00:00:00Z"          # the site's own history starts here
OUT_DIR = ROOT / "drafts" / "analytics"


def load_key():
    key = os.environ.get("GOATCOUNTER_API_KEY", "").strip()
    if key:
        return key
    env = ROOT / ".env"
    if env.exists():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("GOATCOUNTER_API_KEY="):
                value = line.split("=", 1)[1].strip().strip('"').strip("'")
                if value:
                    return value
    return None


def get(path, key, tries=3):
    """GET an API path. Retries the transient statuses the API is known to return."""
    req = urllib.request.Request(
        API + path,
        headers={"Content-Type": "application/json", "Authorization": "Bearer " + key},
    )
    for attempt in range(tries):
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                return json.loads(resp.read().decode())
        except urllib.error.HTTPError as exc:
            if exc.code in (404, 429, 503) and attempt < tries - 1:
                time.sleep(1.5)
                continue
            raise RuntimeError(f"{path} -> HTTP {exc.code}: {exc.read().decode()[:120]}")
        except Exception:
            if attempt < tries - 1:
                time.sleep(1.5)
                continue
            raise RuntimeError(f"{path} -> network error")
    raise RuntimeError(f"{path} -> retries exhausted")


def fetch(key, start, end):
    total = get(f"/stats/total?start={start}&end={end}", key)
    hits = get(f"/stats/hits?start={start}&end={end}&limit=100", key)  # default is 20 rows: funnel counts would silently miss events
    rows = (hits or {}).get("hits", []) if isinstance(hits, dict) else []
    try:  # referrers are a bonus: never fail the snapshot over them
        refs_raw = get(f"/stats/toprefs?start={start}&end={end}", key)
        refs = [r for r in ((refs_raw or {}).get("stats") or []) if isinstance(r, dict)]
    except RuntimeError:
        refs = None
    return {
        "refs": refs,
        "views": total.get("total", 0),
        "events": total.get("total_events", 0),
        "pages": sorted((r for r in rows if not r.get("event")), key=lambda r: -(r.get("count") or 0)),
        "event_rows": sorted((r for r in rows if r.get("event")), key=lambda r: -(r.get("count") or 0)),
    }


def previous_totals():
    """Machine-readable totals left at the foot of the newest existing snapshot."""
    if not OUT_DIR.exists():
        return None
    files = sorted(OUT_DIR.glob("GC-*.md"))
    if not files:
        return None
    match = re.search(r"<!-- totals: views=(\d+) events=(\d+)", files[-1].read_text(encoding="utf-8"))
    if not match:
        return None
    return {"views": int(match.group(1)), "events": int(match.group(2)), "file": files[-1].name}


def delta(now, prev, key):
    if not prev:
        return "(first snapshot)"
    step = now - prev[key]
    if step == 0:
        return "no change"
    return f"{'+' if step > 0 else ''}{step} since {prev['file']}"


# The visitor's path through the site, in order. Each stage counts GoatCounter events whose name starts with
# one of the prefixes (exact name when it has no trailing dash). Counts are clicks and form submits, not people.
FUNNEL = [
    ("Looked at jobs (home page views)", None),
    ("Clicked Apply on a job", ("apply-click",)),
    ("Joined the weekly email (form sent)", ("conversion-signup",)),
    ("Opened WhatsApp about a CV or free check", ("cv-click-",)),
    ("Asked for a free CV check (form sent)", ("conversion-check",)),
    ("Reached the 'email us your CV' step", ("free-check-open-email", "free-check-copy-address")),
    ("Looked at prices or pay buttons", ("services-click-pay-", "services-click-pricing-")),
    ("Sent an order form", ("conversion-order",)),
]
NOT_MEASURED = ("CVs received by email, free checks answered and paid orders are not in GoatCounter. "
                "Log them by hand (drafts/kt-todo.md, free-check log) and compare with the rows above.")


def funnel_counts(window):
    """[(label, count)] for one window of fetch() data. The first stage is views of '/'."""
    window = window or {}
    home = sum(r.get("count", 0) for r in window.get("pages", []) if str(r.get("path")) in ("/", ""))
    out = [(FUNNEL[0][0], home)]
    for label, prefixes in FUNNEL[1:]:
        n = 0
        for r in window.get("event_rows", []):
            name = str(r.get("path") or "").lstrip("/")
            if any(name == p or (p.endswith("-") and name.startswith(p)) for p in prefixes):
                n += r.get("count", 0)
        out.append((label, n))
    return out


def render_funnel(data):
    lines = ["", "## Funnel (clicks and form submits, not people)", ""]
    wins = [w for w in ("Last 7 days", "All time") if w in data]
    lines += ["| Step | " + " | ".join(wins) + " |", "|---|" + "---|" * len(wins)]
    counts = {w: funnel_counts(data[w]) for w in wins}
    for i, (label, _) in enumerate(FUNNEL):
        lines.append(f"| {label} | " + " | ".join(str(counts[w][i][1]) for w in wins) + " |")
    for w in wins:
        home, signups = counts[w][0][1], counts[w][2][1]
        checks = counts[w][4][1] + counts[w][3][1]
        if home:
            lines.append("")
            lines.append(f"- {w}: {signups} email signups and {checks} free-check or CV contacts per {home} home page views "
                         f"({signups * 100 / home:.1f} and {checks * 100 / home:.1f} per 100). Page views, not visitors.")
    lines += ["", NOT_MEASURED]
    return lines


def render(date, data, prev):
    lines = [
        f"# GoatCounter snapshot — {date}",
        "",
        "Generated by `scripts/gc_snapshot.py`. Counts only; part of any single day may be",
        "our own preview or verification traffic (see drafts/ux-optimization-log.md).",
        "",
        "## Totals",
        "",
        "| Window | Pageviews | Events |",
        "|---|---|---|",
    ]
    for name, d in data.items():
        lines.append(f"| {name} | {d['views']} | {d['events']} |")
    all_time = data["All time"]
    lines += [
        "",
        f"- All-time pageviews: **{all_time['views']}** — {delta(all_time['views'], prev, 'views') if prev else 'first snapshot'}",
        f"- All-time events: **{all_time['events']}** — {delta(all_time['events'], prev, 'events') if prev else 'first snapshot'}",
        "",
        "## Pages (all time)",
        "",
        "| Views | Path |",
        "|---|---|",
    ]
    lines += [f"| {r.get('count')} | `{r.get('path')}` |" for r in all_time["pages"]] or ["| — | no data |"]
    lines += ["", "## Events (all time)", "", "| Count | Event | Last title sent |", "|---|---|---|"]
    lines += [
        f"| {r.get('count')} | `{r.get('path')}` | {r.get('title', '')[:60]} |"
        for r in all_time["event_rows"]
    ] or ["| — | no data |"]
    conv = [r for r in all_time["event_rows"] if "conversion" in str(r.get("path"))]
    for window in ("Last 7 days", "All time"):
        refs = (data.get(window) or {}).get("refs")
        lines += ["", f"## Where visitors came from ({window.lower()})", ""]
        if refs is None:
            lines.append("Referrer data could not be fetched this time.")
        elif not refs:
            lines.append("No referrer recorded (direct visits, or visitors whose browser sends none).")
        else:
            lines += ["| Visitors | Referrer or tagged source |", "|---|---|"]
            lines += [f"| {r.get('count', 0)} | {str(r.get('name') or '(direct)')[:60]} |" for r in refs[:15]]
    lines += render_funnel(data)
    lines += [
        "",
        f"Form submissions (conversion-*): **{sum(r.get('count', 0) for r in conv)}**",
        "",
        f"<!-- totals: views={all_time['views']} events={all_time['events']} date={date} -->",
        "",
    ]
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--date", help="snapshot date, YYYY-MM-DD (default: today)")
    args = parser.parse_args(argv)
    date = args.date or dt.date.today().isoformat()
    try:
        parsed = dt.date.fromisoformat(date)
    except ValueError:
        print("error: --date must be YYYY-MM-DD", file=sys.stderr)
        return 1
    key = load_key()
    if not key:
        print("error: GOATCOUNTER_API_KEY not set (environment or .env)", file=sys.stderr)
        return 1
    end = (parsed + dt.timedelta(days=1)).isoformat() + "T00:00:00Z"
    week = (parsed - dt.timedelta(days=6)).isoformat() + "T00:00:00Z"
    month = (parsed - dt.timedelta(days=29)).isoformat() + "T00:00:00Z"
    try:
        data = {
            "Last 7 days": fetch(key, week, end),
            "Last 30 days": fetch(key, month, end),
            "All time": fetch(key, SINCE, end),
        }
    except RuntimeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"GC-{date}.md"
    out.write_text(render(date, data, previous_totals()), encoding="utf-8")
    at = data["All time"]
    print(f"wrote {out.relative_to(ROOT)} — all time: {at['views']} pageviews, {at['events']} events")
    return 0


if __name__ == "__main__":
    sys.exit(main())