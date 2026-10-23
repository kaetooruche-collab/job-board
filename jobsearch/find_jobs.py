"""Pulls current openings from the public job-board APIs of the companies in companies.json (plus the main board's list),
keeps those posted in the last 7 days whose title looks like one of the target role families, and writes
candidates.json for a human-style read. This is a plain keyword search; it does NOT use the job board's classifier.
Run: python3 jobsearch/find_jobs.py"""
import json, re, sys, time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
import fetch_jobs as F  # only its source fetchers are reused

MAX_AGE_DAYS = 7
NOW = datetime.now(timezone.utc)
CUTOFF = NOW - timedelta(days=MAX_AGE_DAYS)

FAMILIES = {
  "Pharmacist / pharmacy": r"pharmacist|pharmacy|pharmacology|pharmaceutical (?:care|operations)|medication|formulary|drug information|prior auth|\bpbm\b|dispens",
  "Drug safety / pharmacovigilance": r"pharmacovigilance|drug safety|\bsafety (?:scientist|associate|specialist|physician|case|operations)|case (?:processing|intake)|\bpv\b|adverse event|safety (?:data|reporting)|risk management",
  "Medical information": r"medical information|medical (?:affairs|communications|review|content|writer|writing)|\bmsl\b|medical science liaison|scientific (?:communications|content)|medical education",
  "Regulatory affairs / quality": r"regulatory|labell?ing|\bqa\b|quality (?:assurance|specialist|associate|systems)|\bgxp\b|compliance (?:specialist|associate|analyst)|submission",
  "Clinical operations / research": r"clinical (?:trial|operations|research|data|study|project|supply)|\bcra\b|\bcta\b|trial (?:manager|coordinator|assistant)|study (?:start|coordinator|manager)|site (?:activation|management)|clinical (?:program|programme)",
  "Healthcare operations / implementation": r"healthcare operations|clinical operations|implementation (?:specialist|manager|consultant|lead|analyst)|onboarding specialist|program (?:manager|coordinator)|operations (?:associate|analyst|specialist|manager)|care (?:operations|coordinator|navigator)|patient (?:support|access|advocate|services|operations)|provider (?:support|operations|success)",
  "Clinical strategy / product": r"clinical (?:strategy|product|content|informatics|specialist|analyst|lead|consultant)|product (?:specialist|manager|owner|analyst) .*(?:clinical|health)|health (?:economics|outcomes)|\bheor\b|market access|medical (?:strategy|policy)|evidence",
  "Customer success (health)": r"customer success|customer support|client success|account (?:manager|specialist)|technical support",
}
FAMILY_RES = {k: re.compile(v, re.I) for k, v in FAMILIES.items()}
HEALTH_CONTEXT = re.compile(r"health|clinic|pharma|patient|medic|drug|therap|biotech|life science|clinical trial|care\b|hospital|provider|payer|genom|diagnos", re.I)
EXCLUDE_TITLE = re.compile(r"software engineer|backend|frontend|full[- ]stack|devops|data engineer|machine learning|security engineer|recruiter|sales development|account executive|designer|accountant|\bsdr\b|\bbdr\b", re.I)

def board_list():
    rows = []
    try:
        rows += json.loads((HERE / "companies.json").read_text())
    except FileNotFoundError:
        pass
    main = json.loads((HERE.parent / "data" / "boards.json").read_text())
    for ats in ("greenhouse", "lever", "ashby"):
        for b in main.get(ats, []):
            rows.append({"ats": ats, "slug": b["slug"], "company": b["company"]})
    seen, out = set(), []
    for r in rows:
        k = (r["ats"], r["slug"])
        if k not in seen:
            seen.add(k); out.append(r)
    return out

FETCH = {"greenhouse": F.fetch_greenhouse_board, "lever": F.fetch_lever_board, "ashby": F.fetch_ashby_board}

def pull(row):
    try:
        items = FETCH[row["ats"]]({"slug": row["slug"], "company": row["company"]})
    except Exception as e:  # noqa: BLE001
        return []
    out = []
    for j in items:
        p = j.get("posted")
        if not p or p < CUTOFF:
            continue
        title = j.get("title", "")
        fams = [k for k, rx in FAMILY_RES.items() if rx.search(title)]
        if not fams or EXCLUDE_TITLE.search(title):
            continue
        text = (title + " " + F.C.clean_text(j.get("description", "")))[:6000]
        if not HEALTH_CONTEXT.search(text):
            continue
        j = dict(j); j["families"] = fams; j["ats"] = row["ats"]; j["slug"] = row["slug"]
        j["posted"] = p.isoformat()
        j["description"] = F.C.clean_text(j.get("description", ""))
        out.append(j)
    return out

def main():
    boards = board_list()
    print(len(boards), "boards", file=sys.stderr)
    cands = []
    with ThreadPoolExecutor(6) as ex:
        for res in ex.map(pull, boards):
            cands += res
    # Jobicy remote feed (public API) as an extra remote-only source
    try:
        for q in ({"tag": "pharmacist"}, {"tag": "pharmacy"}, {"tag": "clinical"}, {"tag": "healthcare"}, {"tag": "pharmacovigilance"}, {"tag": "regulatory"}, {"tag": "medical"}, {"industry": "healthcare"}):
            data = F.get_json("https://jobicy.com/api/v2/remote-jobs", params={"count": 50, **q}, timeout=30)
            for j in (data or {}).get("jobs", []):
                r = F._jobicy_record(j)
                p = r.get("posted")
                if not p or p < CUTOFF:
                    continue
                fams = [k for k, rx in FAMILY_RES.items() if rx.search(r["title"])]
                if not fams:
                    continue
                r["families"] = fams; r["ats"] = "jobicy"; r["slug"] = ""; r["posted"] = p.isoformat()
                r["description"] = F.C.clean_text(r["description"])
                cands.append(r)
            time.sleep(0.6)
    except Exception as e:  # noqa: BLE001
        print("jobicy failed", e, file=sys.stderr)
    uniq = {}
    for c in cands:
        uniq[c["url"]] = c
    cands = sorted(uniq.values(), key=lambda c: c["posted"], reverse=True)
    for c in cands:
        c.pop("hint", None)
    (HERE / "candidates.json").write_text(json.dumps(cands, indent=1, default=str), encoding="utf-8")
    print(len(cands), "candidates in last", MAX_AGE_DAYS, "days")

if __name__ == "__main__":
    main()
