#!/usr/bin/env python3
"""Builds drafts/fable/context-pack.md: one file holding everything Fable needs to read, plus fresh numbers.

Run it on the day of the Fable run so the numbers are current:  python3 scripts/build_fable_context.py
The output is git-ignored (it goes stale fast). It prints a rough token count (characters / 4; the API's count_tokens is exact).
Order matters: the brief comes first, then the facts, then the long history."""
import collections
import json
import pathlib
import urllib.parse
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "drafts" / "fable" / "context-pack.md"

FILES = [
    "drafts/fable/brief.md",
    "drafts/fable/kt-inputs.md",
    "drafts/fable/inputs/external-facts-2026-11-16.md",
    "CLAUDE.md",
    "drafts/site-inventory.md",
    "drafts/kt-todo.md",
    "research/job-sources-100.md",
    "drafts/marketing/audience-research-and-icp.md",
    "drafts/marketing/outreach-hooks-and-copy-by-platform.md",
    "drafts/voice-and-copy-guide.md",
    "data/qa_report.md",
]


def fresh_numbers():
    rows = json.loads((ROOT / "jobs.json").read_text(encoding="utf-8"))
    m = json.loads((ROOT / "data" / "metrics.json").read_text(encoding="utf-8"))
    comp = collections.Counter(r["company"] for r in rows)
    hosts = collections.Counter(urllib.parse.urlparse(r["sourceUrl"]).netloc for r in rows)
    lc = m.get("linkCheck", {})
    lines = [
        f"Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} from jobs.json and data/metrics.json.",
        f"- Published listings: {len(rows)} from {len(comp)} companies. Top 10 companies hold {sum(v for _, v in comp.most_common(10)) * 100 / len(rows):.1f}% of listings.",
        f"- By source: {dict(collections.Counter(r['sourceName'] for r in rows))}. By apply-link host: {dict(hosts.most_common(6))}.",
        f"- Eligibility: {dict(collections.Counter((r.get('eligibility') or {}).get('type') for r in rows))}.",
        f"- Level: {dict(collections.Counter(r['level'] for r in rows))}.",
        f"- Category (top 10): {collections.Counter(r['category'] for r in rows).most_common(10)}.",
        f"- Pay stated on {sum(1 for r in rows if r.get('salaryText'))} listings.",
        f"- Raw candidates read from the feeds: {m.get('rawCandidates')}.",
        f"- Newest link check: fail rate {lc.get('failRate')}, unreachable {lc.get('unknown')}, kept on an older check {lc.get('carriedOnOldCheck')}, reasons {lc.get('unknownReasons')}.",
    ]
    return "\n".join(lines)


def main():
    parts = ["# Context pack for the Fable run\n", "Contents, in order: " + ", ".join(f"`{f}`" for f in FILES) +
             ", fresh numbers, the two newest analytics snapshots, every decision record. The country list is a separate file: `drafts/fable/inputs/country-job-boards-unverified.csv`.\n"]
    for f in FILES:
        p = ROOT / f
        parts.append(f"\n\n---\n\n## FILE: {f}\n\n" + (p.read_text(encoding="utf-8") if p.exists() else "(missing)"))
    parts.append("\n\n---\n\n## FRESH NUMBERS\n\n" + fresh_numbers())
    for p in sorted((ROOT / "drafts" / "analytics").glob("GC-*.md"))[-2:]:
        parts.append(f"\n\n---\n\n## FILE: drafts/analytics/{p.name}\n\n" + p.read_text(encoding="utf-8"))
    for p in sorted((ROOT / "drafts" / "decisions").glob("*.md")):
        parts.append(f"\n\n---\n\n## FILE: drafts/decisions/{p.name}\n\n" + p.read_text(encoding="utf-8"))
    text = "".join(parts)
    OUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(text):,} characters, about {len(text) // 4:,} tokens (1M-token context)")


if __name__ == "__main__":
    main()
