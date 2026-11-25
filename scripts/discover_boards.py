#!/usr/bin/env python3
"""Keeps the employer list growing and healthy without anyone editing data/boards.json by hand.

Runs weekly in .github/workflows/discover-boards.yml. Two passes:

1. PRUNE. Every board in data/boards.json is read once. A board whose feed is gone (HTTP 404) for 3 weekly
   checks in a row, or that has had nothing publishable for 8 weekly checks in a row, is retired: removed
   from boards.json and kept in data/board_discovery.json with the reason. Safety: if more than 30% of boards
   fail in one run it is treated as an outage and nothing is counted; at most 15 boards are retired per run.

2. DISCOVER. Candidates come from the Remote In Tech directory (github.com/remoteintech/remote-jobs, ISC
   licence: one file per company with `careers_url`, `region`, `remote_policy`), plus any entries in
   data/board_candidates.json. Worldwide, fully remote companies are tried first, because roles open to
   readers outside one country are the board's real gap (17 of 1,026 listings were worldwide on 24 Oct 2026).
   The board is found from the stated careers link when it points at Greenhouse, Lever or Ashby, otherwise by
   guessing the board name; a guessed board must prove it is the same company (Greenhouse returns its name;
   for Lever and Ashby the company name must appear in its own postings). A board is added only if the real
   pipeline (fetch_jobs.process: dates, 30-day window, classifier) would publish at least one listing from it
   today. At most 40 boards are added per run; each candidate is probed at most once every 90 days.

Only the three hiring systems whose public feeds were checked for this use are touched
(drafts/decisions/2026-10-31-ats-terms-check.md). Companies in data/board_blocklist.json (removal requests)
are never added back. Every listing from a new board still passes the classifier and scripts/qa_checks.py.

    python3 scripts/discover_boards.py --remoteintech /path/to/remote-jobs [--max-probes 200] [--max-adds 40] [--dry-run]
"""
import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

BOARDS = ROOT / "data" / "boards.json"
STATE = ROOT / "data" / "board_discovery.json"
BLOCKLIST = ROOT / "data" / "board_blocklist.json"
CANDIDATES = ROOT / "data" / "board_candidates.json"
REPORT = ROOT / "data" / "discovery_report.md"

KINDS = ("greenhouse", "lever", "ashby", "recruitee", "personio")  # the last two switched on 25 Nov 2026
DEAD_WEEKS_TO_RETIRE = 3
EMPTY_WEEKS_TO_RETIRE = 8
MAX_RETIRE_PER_RUN = 15
OUTAGE_SHARE = 0.30
REPROBE_DAYS = 90
MIN_PUBLISHABLE = 1
MAX_LIVE_LISTINGS = 2000   # stop adding boards while this many listings are live; equals fetch_jobs.MAX_LISTINGS
EARLY_CAREER_LISTS = [     # SimplifyJobs public lists: used ONLY to learn which employer boards hire early-career people
    "https://raw.githubusercontent.com/SimplifyJobs/New-Grad-Positions/dev/.github/scripts/listings.json",
    "https://raw.githubusercontent.com/SimplifyJobs/Summer2026-Internships/dev/.github/scripts/listings.json",
]

ATS_URL_RE = [
    ("greenhouse", re.compile(r"(?:boards|job-boards)(?:\.eu)?\.greenhouse\.io/(?:embed/job_board\?for=)?([A-Za-z0-9_-]+)", re.I)),
    ("greenhouse", re.compile(r"boards-api\.greenhouse\.io/v1/boards/([A-Za-z0-9_-]+)", re.I)),
    ("lever", re.compile(r"jobs(?:\.eu)?\.lever\.co/([A-Za-z0-9_.-]+)", re.I)),
    ("ashby", re.compile(r"jobs\.ashbyhq\.com/([A-Za-z0-9_.%-]+)", re.I)),
    ("ashby", re.compile(r"api\.ashbyhq\.com/posting-api/job-board/([A-Za-z0-9_.%-]+)", re.I)),
    ("recruitee", re.compile(r"//([a-z0-9][a-z0-9-]+)\.recruitee\.com", re.I)),
    ("personio", re.compile(r"//([a-z0-9][a-z0-9-]+)\.jobs\.personio\.(?:de|com)", re.I)),
]
NOT_SLUGS = {"www", "app", "embed", "jobs", "job_board", "v1", "api", "careers", "search"}


# ---------- pure helpers (tested in tests/test_discover_boards.py) ----------

def parse_frontmatter(text):
    """The `key: value` lines between the first two `---` lines. Lists and nested keys are ignored."""
    m = re.match(r"\s*---\s*\n(.*?)\n---", text or "", re.S)
    out = {}
    for line in (m.group(1) if m else "").splitlines():
        kv = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if kv and kv.group(2).strip():
            out[kv.group(1)] = kv.group(2).strip().strip('"').strip("'")
    return out


def ats_from_url(url):
    for kind, rx in ATS_URL_RE:
        m = rx.search(url or "")
        if m and m.group(1).lower() not in NOT_SLUGS:
            return kind, m.group(1)
    return None


def norm(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def slug_guesses(entry):
    title = entry.get("title") or ""
    site = re.sub(r"^https?://(?:www\.)?", "", entry.get("website") or "").split("/")[0].split(".")[0]
    seen, out = set(), []
    for g in (entry.get("slug"), norm(title), re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-"), site):
        g = (g or "").strip().lower()
        if len(g) >= 3 and g not in seen:
            seen.add(g)
            out.append(g)
    return out[:3]


COMPANY_SUFFIXES = {"inc", "llc", "ltd", "limited", "co", "corp", "corporation", "company", "gmbh", "ag", "sa", "bv",
                    "plc", "pty", "technologies", "technology", "labs", "lab", "hq", "group", "holdings", "software",
                    "careers", "jobs", "io", "ai", "app", "the"}


def company_key(name):
    """'GitLab Inc.' -> 'gitlab', 'The Browser Company' -> 'browser'; legal and generic words only."""
    ws = re.findall(r"[a-z0-9]+", (name or "").lower())
    while ws and ws[-1] in COMPANY_SUFFIXES:
        ws.pop()
    while ws and ws[0] == "the":
        ws.pop(0)
    return "".join(ws)


def same_company(a, b):
    """Same employer once legal and generic words are removed; never a prefix match
    ('Doist' must not match 'Doist Plumbing LLC')."""
    a, b = company_key(a), company_key(b)
    return bool(a) and a == b


def priority(entry):
    """Lower sorts first: worldwide directory companies (the board's biggest gap), then early-career employers
    (the best yield per probe: 38 of 138 sampled boards had a publishable listing, 25 Nov 2026), then the rest;
    within a group, fully remote before remote-friendly."""
    region = (entry.get("region") or "").lower()
    policy = (entry.get("remote_policy") or "").lower()
    group = 0 if "worldwide" in region else 1 if entry.get("origin") == "early-career list" else 2
    return (group, 0 if "fully" in policy else 1, norm(entry.get("title")))


def probe_key(entry):
    known = entry.get("known")
    return f"{known[0]}/{known[1].lower()}" if known else norm(entry.get("title"))


def early_career_seeds(lists):
    """(company, hiring system, board name) from each listing's own link. Nothing else from the lists is kept,
    stored or shown: they are a pointer to employers, and every listing comes from the employer's own feed."""
    out, seen = [], set()
    for rows in lists:
        for x in rows or []:
            found = ats_from_url(x.get("url"))
            if not found or found[0] not in KINDS or not x.get("company_name"):
                continue
            key = (found[0], found[1].lower())
            if key not in seen:
                seen.add(key)
                out.append({"title": x["company_name"], "known": key, "origin": "early-career list"})
    return out


def update_health(rec, status, publishable):
    """status: 'ok' | 'dead' | 'error'. Returns (new record, retire_reason or None)."""
    rec = dict(rec or {})
    if status == "error":
        return rec, None
    rec["deadWeeks"] = rec.get("deadWeeks", 0) + 1 if status == "dead" else 0
    if status == "ok":
        rec["emptyWeeks"] = 0 if publishable >= MIN_PUBLISHABLE else rec.get("emptyWeeks", 0) + 1
        rec["lastPublishable"] = publishable
    if rec["deadWeeks"] >= DEAD_WEEKS_TO_RETIRE:
        return rec, f"feed gone (404) for {rec['deadWeeks']} weekly checks"
    if rec.get("emptyWeeks", 0) >= EMPTY_WEEKS_TO_RETIRE:
        return rec, f"nothing publishable for {rec['emptyWeeks']} weekly checks"
    return rec, None


def due_for_probe(state, key, today):
    last = (state.get("probed") or {}).get(key, {}).get("at")
    return not last or (today - datetime.fromisoformat(last).date()).days >= REPROBE_DAYS


# ---------- network ----------

def _session():
    import requests
    s = requests.Session()
    s.headers["User-Agent"] = "YirehCareersBoardDiscovery/1.0 (+https://yirehcareers.vercel.app/verify)"
    return s


SESSION = None


def http_get(url, **kw):
    global SESSION
    SESSION = SESSION or _session()
    return SESSION.get(url, timeout=kw.pop("timeout", 20), **kw)


def probe(kind, slug, get=http_get):
    """Returns (status, name_or_None). status: 'ok' | 'dead' | 'error'."""
    url = {"greenhouse": f"https://boards-api.greenhouse.io/v1/boards/{slug}",
           "lever": f"https://api.lever.co/v0/postings/{slug}?mode=json&limit=1",
           "ashby": f"https://api.ashbyhq.com/posting-api/job-board/{slug}",
           "recruitee": f"https://{slug}.recruitee.com/api/offers/",
           "personio": f"https://{slug}.jobs.personio.de/xml"}[kind]
    try:
        r = get(url)
    except Exception:
        return "error", None
    if r.status_code == 404:
        return "dead", None
    if r.status_code != 200:
        return "error", None
    if kind == "personio":  # an XML feed, not JSON
        return ("ok", None) if "<workzag-jobs" in r.text else ("error", None)
    try:
        data = r.json()
    except ValueError:
        return "error", None
    return "ok", (data.get("name") if kind == "greenhouse" and isinstance(data, dict) else None)


def board_items(kind, board):
    import fetch_jobs as F
    fn = {"greenhouse": F.fetch_greenhouse_board, "lever": F.fetch_lever_board, "ashby": F.fetch_ashby_board, **F.EXTRA_READERS}[kind]
    return fn(board)


def publishable_count(items):
    """How many of these raw postings the real pipeline would publish today (before the per-company cap)."""
    import fetch_jobs as F
    # quiet=True, not contextlib.redirect_stdout: redirecting swaps sys.stdout for the whole process, so inside
    # the thread pool it raced and swallowed other threads' output (found 25 Nov 2026)
    return len(F.process(list(items), [], [], quiet=True))


def read_board(kind, board, get=http_get):
    """('ok', publishable, items) | ('dead', 0, []) | ('error', 0, []).
    The status comes from a probe first: fetch_jobs.get_json returns nothing for a missing board AND for a
    network error, and only a real 404 may count towards retiring a board."""
    status, _ = probe(kind, board["slug"], get)
    if status != "ok":
        return status, 0, []
    try:
        items = board_items(kind, board)
    except Exception:
        return "error", 0, []
    return "ok", publishable_count(items), items


# ---------- candidates ----------

def load_remoteintech(path):
    if not path:
        return []
    folder = Path(path) / "src" / "companies"
    out = []
    for f in sorted(folder.glob("*.md")):
        fm = parse_frontmatter(f.read_text(encoding="utf-8", errors="replace"))
        if fm.get("title"):
            fm.setdefault("slug", f.stem)
            fm["origin"] = "remoteintech"
            out.append(fm)
    return out


def load_json(path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def identify(entry, get=http_get, items_fn=board_items):
    """Find the entry's board. Returns (kind, slug, company_name, how) or None."""
    if entry.get("known"):  # the board name came from one of the employer's own posting links
        kind, slug = entry["known"]
        status, name = probe(kind, slug, get)
        return (kind, slug, name or entry["title"], "early-career list link") if status == "ok" else None
    stated = ats_from_url(entry.get("careers_url")) or ats_from_url(entry.get("website"))
    if stated:
        kind, slug = stated
        status, name = probe(kind, slug, get)
        if status == "ok":
            return kind, slug, name or entry["title"], "careers link"
        return None
    for slug in slug_guesses(entry):
        for kind in KINDS:
            status, name = probe(kind, slug, get)
            if status != "ok":
                continue
            if kind == "greenhouse":
                if same_company(name, entry["title"]):
                    return kind, slug, name, "board name matches"
                continue
            try:
                items = items_fn(kind, {"slug": slug, "company": entry["title"]})[:8]
            except Exception:
                continue
            text = " ".join(re.sub(r"<[^>]+>", " ", i.get("description") or "") for i in items).lower()
            if items and entry["title"].lower() in text:
                return kind, slug, entry["title"], "company named in its own postings"
    return None


# ---------- main ----------

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--remoteintech", help="path to a clone of remoteintech/remote-jobs")
    ap.add_argument("--max-probes", type=int, default=200)
    ap.add_argument("--max-adds", type=int, default=100)
    ap.add_argument("--max-live", type=int, default=MAX_LIVE_LISTINGS)
    ap.add_argument("--early-career", action="store_true", help="also take employers from the early-career lists")
    ap.add_argument("--skip-prune", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)

    now = datetime.now(timezone.utc)
    today = now.date()
    boards = load_json(BOARDS, {})
    state = load_json(STATE, {"note": "Written by scripts/discover_boards.py. health: weekly counters per board; probed: last probe per candidate; retired and added: history.", "health": {}, "probed": {}, "retired": [], "added": []})
    block = load_json(BLOCKLIST, {"companies": [], "boards": []})
    blocked_names = {norm(c) for c in block.get("companies", [])}
    blocked_boards = {b.lower() for b in block.get("boards", [])}
    lines = [f"# Board discovery report, {now.strftime('%Y-%m-%d %H:%M UTC')}", ""]

    # 1. prune
    retired_now = []
    if not a.skip_prune:
        current = [(k, b) for k in KINDS for b in boards.get(k, [])]
        with ThreadPoolExecutor(max_workers=8) as ex:
            results = list(ex.map(lambda kb: read_board(*kb), current))
        bad = sum(1 for r in results if r[0] != "ok")
        lines.append(f"## Health of the {len(current)} current boards")
        if current and bad / len(current) > OUTAGE_SHARE:
            lines.append(f"- {bad} of {len(current)} boards failed in this run: treated as an outage, no counters changed.")
        else:
            productive = 0
            for (kind, b), (status, pub, _) in zip(current, results):
                key = f"{kind}/{b['slug']}"
                rec, why = update_health(state["health"].get(key), status, pub)
                state["health"][key] = rec
                productive += 1 if pub >= MIN_PUBLISHABLE else 0
                if why and len(retired_now) < MAX_RETIRE_PER_RUN:
                    retired_now.append((kind, b, why))
            for kind, b, why in retired_now:
                boards[kind] = [x for x in boards[kind] if x["slug"] != b["slug"]]
                state["health"].pop(f"{kind}/{b['slug']}", None)
                state["retired"].append({"kind": kind, "slug": b["slug"], "company": b["company"], "reason": why, "at": today.isoformat()})
            lines.append(f"- {productive} boards have at least one publishable listing today; {bad} could not be read.")
            lines.append(f"- Retired this run: {len(retired_now)}" + "".join(f"\n  - {b['company']} ({k}/{b['slug']}): {w}" for k, b, w in retired_now))
        lines.append("")

    # 2. discover
    have_names = {norm(b["company"]) for k in KINDS for b in boards.get(k, [])}
    have_boards = {f"{k}/{b['slug'].lower()}" for k in KINDS for b in boards.get(k, [])}
    retired_keys = {f"{r['kind']}/{r['slug'].lower()}" for r in state["retired"]
                    if (today - datetime.fromisoformat(r["at"]).date()).days < REPROBE_DAYS}
    cands = load_remoteintech(a.remoteintech) + [dict(c, origin="board_candidates.json") for c in load_json(CANDIDATES, {"companies": []}).get("companies", [])]
    if a.early_career:
        lists = []
        for u in EARLY_CAREER_LISTS:
            try:
                lists.append(http_get(u, timeout=60).json())
            except Exception as e:  # a missing list must not stop the run
                lines.append(f"- Early-career list unavailable ({u.rsplit('/', 5)[1]}): {type(e).__name__}")
        cands += early_career_seeds(lists)
    cands = [c for c in cands if norm(c["title"]) not in have_names and norm(c["title"]) not in blocked_names
             and not (c.get("known") and f"{c['known'][0]}/{c['known'][1]}" in have_boards)]
    cands.sort(key=priority)
    todo = [c for c in cands if due_for_probe(state, probe_key(c), today)][: a.max_probes]
    try:
        live = len(json.loads((ROOT / "jobs.json").read_text(encoding="utf-8")))
    except (OSError, ValueError):
        live = 0
    room = a.max_adds if live < a.max_live else 0
    if not room:
        todo = []
        lines.append(f"- {live} listings are live (limit {a.max_live}): no boards added this run, only pruning.")

    def check(c):
        found = identify(c)
        if not found:
            return c, None, 0
        kind, slug, name, how = found
        key = f"{kind}/{slug.lower()}"
        if key in have_boards or key in retired_keys or slug.lower() in blocked_boards or norm(name) in blocked_names:
            return c, None, 0
        status, pub, _ = read_board(kind, {"slug": slug, "company": name})
        return c, (kind, slug, name, how), (pub if status == "ok" else 0)

    with ThreadPoolExecutor(max_workers=6) as ex:
        checked = list(ex.map(check, todo))
    added = []
    for c, found, pub in checked:
        state["probed"][probe_key(c)] = {"at": today.isoformat(), "found": f"{found[0]}/{found[1]}" if found else None, "publishable": pub}
        if found and pub >= MIN_PUBLISHABLE and len(added) < room:
            kind, slug, name, how = found
            if f"{kind}/{slug.lower()}" in have_boards:
                continue
            have_boards.add(f"{kind}/{slug.lower()}")
            boards.setdefault(kind, []).append({"slug": slug, "company": name})
            added.append((kind, slug, name, how, pub, c.get("region", ""), c["origin"]))
            state["added"].append({"kind": kind, "slug": slug, "company": name, "at": today.isoformat(), "how": how, "publishable": pub, "origin": c["origin"]})
    found_n = sum(1 for _, f, _ in checked if f)
    lines += [f"## Discovery", f"- Candidates not yet on the board: {len(cands)}; probed this run: {len(todo)}; board found: {found_n}; added: {len(added)}."]
    lines += [f"  - {n} ({k}/{s}): {p} publishable now, found by {h}" + (f", region in directory: {r}" if r else "") for k, s, n, h, p, r, _ in added]
    lines.append("")
    lines.append("Every listing from an added board still passes the classifier and the QA rules before it is shown. "
                 "To remove a company for good, add it to data/board_blocklist.json.")

    for k in KINDS:
        boards[k] = sorted(boards.get(k, []), key=lambda b: b["company"].lower())
    report = "\n".join(lines) + "\n"
    print(report)
    if not a.dry_run:
        BOARDS.write_text(json.dumps(boards, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        REPORT.write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
