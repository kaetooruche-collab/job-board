#!/usr/bin/env python3
"""Board visits that came from our social posts, by platform, for the Friday review.

    python3 social/tools/social_metrics.py --days 7          # writes social/metrics/<today>.md, prints a summary

GoatCounter records a link's utm_source as the referrer and utm_campaign as the campaign
(goatcounter.com/help/campaigns, read 27 Nov 2026). Our links use utm_source=tiktok|instagram|facebook|instagram_story
and utm_campaign=bio or the post id, so both are counted here. Platform numbers (views, likes, saves) come from Buffer
in the session (get_aggregated_post_metrics / get_post) and are added to social/post-log.csv by the review runbook.

The API key: GOATCOUNTER_API_KEY or the proxy's injected credential for kayzglobal.goatcounter.com (then any
placeholder value works). Exit 1 when the data could not be fetched; the review then says so instead of guessing.
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
import gc_snapshot as gc  # noqa: E402

SOCIAL = ("tiktok", "instagram", "instagram_story", "facebook", "fb", "ig", "l.instagram.com", "lm.facebook.com",
          "m.facebook.com", "www.facebook.com", "www.tiktok.com", "tiktok.com")


def platform(ref: str) -> str | None:
    r = (ref or "").lower()
    for name in ("instagram_story", "instagram", "tiktok", "facebook"):
        if name in r:
            return name
    if r in ("ig", "l.instagram.com"):
        return "instagram"
    if r in ("fb",) or "facebook" in r:
        return "facebook"
    return None


def collect(days: int, key: str) -> dict:
    end = dt.datetime.now(dt.timezone.utc).replace(microsecond=0)
    start = end - dt.timedelta(days=days)
    s, e = start.strftime("%Y-%m-%dT%H:%M:%SZ"), end.strftime("%Y-%m-%dT%H:%M:%SZ")
    refs = (gc.get(f"/stats/toprefs?start={s}&end={e}&limit=100", key) or {}).get("stats") or []
    camps = (gc.get(f"/stats/campaigns?start={s}&end={e}&limit=100", key) or {}).get("stats") or []
    total = gc.get(f"/stats/total?start={s}&end={e}", key) or {}
    by = {}
    for r in refs:
        p = platform(r.get("name", ""))
        if p:
            by[p] = by.get(p, 0) + int(r.get("count") or 0)
    return {"start": s, "end": e, "views": total.get("total", 0), "by_platform": by,
            "campaigns": [(c.get("name"), c.get("count")) for c in camps]}


def render(d: dict) -> str:
    lines = [f"# Board visits from social ({d['start'][:10]} to {d['end'][:10]})", "",
             f"All board views in the window: {d['views']}", "", "| Platform (utm_source / referrer) | Visits |", "|---|---|"]
    for k, v in sorted(d["by_platform"].items(), key=lambda kv: -kv[1]) or [("none recorded", 0)]:
        lines.append(f"| {k} | {v} |")
    lines += ["", "| Campaign (utm_campaign) | Visits |", "|---|---|"]
    for k, v in d["campaigns"] or [("none recorded", 0)]:
        lines.append(f"| {k} | {v} |")
    lines += ["", "Source: GoatCounter API (kayzglobal). Small numbers: no conclusions under the agency's ~1,000-views-per-variant rule."]
    return "\n".join(lines) + "\n"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    a = ap.parse_args(argv)
    key = gc.load_key() or "proxy-injected"
    try:
        d = collect(a.days, key)
    except RuntimeError as exc:
        print(f"GoatCounter not reachable: {exc}. Needs a credential for kayzglobal.goatcounter.com.", file=sys.stderr)
        return 1
    out = ROOT / "social" / "metrics" / f"{dt.date.today().isoformat()}.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(d), encoding="utf-8")
    print(out)
    print(d["by_platform"] or "no social visits recorded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
