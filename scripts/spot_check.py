"""Prints N random published listings with everything needed to check each card against its real posting.

Usage: python -I scripts/spot_check.py [N] [seed]
For each listing: open the URL, then compare title, company, where applicants may live, remote or not,
level, pay and posting date with what the card says. Record any mismatch in data/audit_log.md.
"""
import json
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
n = int(sys.argv[1]) if len(sys.argv) > 1 else 10
seed = sys.argv[2] if len(sys.argv) > 2 else None
rows = json.loads((ROOT / "jobs.json").read_text(encoding="utf-8"))
rnd = random.Random(seed)
for i, r in enumerate(rnd.sample(rows, min(n, len(rows))), 1):
    e = r["eligibility"]
    print(f"{i}. {r['title']} | {r['company']} | source {r['sourceName']}")
    print(f"   URL: {r['sourceUrl']}")
    print(f"   Card says: {r['workArrangementLabel']}; who can apply: {e['label']}; level: {r['level']}; type: {r['jobType']}; pay: {r['salaryText'] or 'not stated'}; posted: {r['postedAt']}")
    if e.get("notes"):
        print(f"   Notes shown: {' / '.join(e['notes'])}")
    print()
