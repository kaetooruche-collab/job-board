#!/usr/bin/env python3
"""Catalogue every piece of social content in one place: social/CATALOG.csv (full) and social/CATALOG.md (readable).

    python3 social/tools/catalog.py

One row per post (and per moved-out or held post), from the calendars, proposals, rendered output, video briefs and
social/post-log.csv (Buffer ids and results). Status:
  draft / needs-writing   planned, not finished
  ready                   media exists (slides or video.mp4) and the checker passes in draft mode
  scheduled / published   recorded in post-log.csv with a Buffer id (published when metrics are logged)
  moved-out / held        replaced in its week, or held for KT
Run it after any planning, production or publishing step (the runbooks do).
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "social" / "tools"))
import check_post  # noqa: E402

FIELDS = ["post_id", "week", "date", "day", "status", "series", "pillar", "format", "platforms", "funnel", "goal_metric",
          "hook", "variable", "presenter", "assets", "brief", "approved", "buffer_ids", "results", "source_file", "notes"]


def media(post: dict) -> list[str]:
    d = ROOT / "social" / "output" / post.get("date", "") / post.get("id", "")
    if not d.is_dir():
        return []
    return [str(p.relative_to(ROOT)) for p in sorted(d.glob("*")) if p.suffix in (".jpg", ".mp4")]


def main() -> int:
    state = json.loads((ROOT / "social" / "state.json").read_text(encoding="utf-8"))
    approved_weeks = {a["week"] for a in state.get("approvals", []) if a.get("by") == "KT" and a.get("decision", "yes") == "yes" and "post" not in a and "week" in a}
    approved_posts = {a["post"] for a in state.get("approvals", []) if "post" in a}
    log = list(csv.DictReader((ROOT / "social" / "post-log.csv").open(encoding="utf-8")))
    rows = []
    files = sorted((ROOT / "social" / "calendar").glob("*.posts.json")) + sorted((ROOT / "social" / "calendar" / "proposals").glob("*.json"))
    for f in files:
        data = json.loads(f.read_text(encoding="utf-8"))
        week = data.get("week", "")
        groups = [(p, None) for p in data.get("posts", [])] + [(p, "moved-out") for p in data.get("moved_out", [])] + \
                 [(p, "held") for p in data.get("held", [])]
        for p, forced in groups:
            assets = media(p) if not forced else []
            logged = [r for r in log if r.get("post_id") == p.get("id")]
            if forced:
                status = forced
            elif logged:
                status = "published" if any(r.get("metrics_source") for r in logged) else "scheduled"
            elif p.get("needs_writing"):
                status = "needs-writing"
            elif assets and not [x for x in check_post.check_post(p, "draft") if x.level == check_post.BLOCK]:
                status = "ready"
            else:
                status = "draft"
            if "proposals" in f.parts and status not in ("moved-out", "held"):
                status = "proposal-" + status
            res = "; ".join(f"{r['platform']}: {r.get('impressions_or_reach') or '-'}"
                            + (f", avg watch {r['avg_watch_s']}s" if r.get("avg_watch_s") else "") for r in logged)
            rows.append({
                "post_id": p.get("id", ""), "week": week, "date": p.get("date", ""), "day": p.get("day", ""), "status": status,
                "series": p.get("series", ""), "pillar": p.get("pillar", ""), "format": p.get("format", ""),
                "platforms": " ".join(p.get("platforms", [])), "funnel": p.get("funnel", ""), "goal_metric": p.get("goal_metric", ""),
                "hook": p.get("hook", ""), "variable": p.get("variable", ""), "presenter": (p.get("cast") or {}).get("presenter", ""),
                "assets": " ".join(assets), "brief": p.get("brief", ""),
                "approved": "yes" if (week in approved_weeks or p.get("id") in approved_posts) and "proposals" not in f.parts else "",
                "buffer_ids": " ".join(r.get("buffer_post_id", "") for r in logged if r.get("buffer_post_id")),
                "results": res, "source_file": str(f.relative_to(ROOT)),
                "notes": p.get("moved_out") or p.get("pending_swap") or p.get("note") or p.get("needs_writing") or ""})
    # posts published outside the calendars (before the agency, or by KT by hand)
    known = {r["post_id"] for r in rows}
    for r in log:
        if r["post_id"] not in known:
            rows.append({k: "" for k in FIELDS} | {"post_id": r["post_id"], "date": r.get("published_at_utc", "")[:10],
                        "status": "published", "series": r.get("series", ""), "hook": r.get("hook", ""),
                        "platforms": r.get("platform", ""), "buffer_ids": r.get("buffer_post_id", ""),
                        "results": f"{r.get('impressions_or_reach') or '-'}" + (f", avg watch {r['avg_watch_s']}s" if r.get("avg_watch_s") else ""),
                        "source_file": "social/post-log.csv", "notes": r.get("notes", "")})
    out = ROOT / "social" / "CATALOG.csv"
    with out.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    md = ["# Content catalogue (generated by `social/tools/catalog.py`; do not edit by hand)", "",
          f"{len(rows)} pieces. Full columns in `CATALOG.csv`.", "",
          "| Date | Post | Status | Format | Platforms | Hook | Approved | Results |", "|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["date"], r["post_id"])):
        md.append(f"| {r['date']} | {r['post_id']} | {r['status']} | {r['format']} | {r['platforms']} | {r['hook'][:60]} | {r['approved']} | {r['results'][:60]} |")
    (ROOT / "social" / "CATALOG.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    from collections import Counter
    print(out, len(rows), "pieces;", dict(Counter(r["status"] for r in rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
