# Source research, 25 Nov 2026: the stored data

Gathered in one pass before any analysis or building (KT, 25 Nov: "first, think, store data in bulk, analyze after, create a plan and a checklist then execute"). The analysis and plan built on it are in `drafts/decisions/2026-11-25-sources-beyond-three-and-junior-plan.md`.

| File | What it holds | How it was made |
|---|---|---|
| `feed_funnel.csv.gz` | All 20,863 postings in the 285 current feeds, one row each: source, company, title, location, age, decision, reason, arrangement, level, eligibility (no descriptions) | every feed fetched, every posting classified with `scripts/classify.py` |
| `careers_page_fingerprints.json.gz` | The 876 Remote In Tech companies: careers page status and which hiring systems appear in its HTML | one GET per careers page, pattern match on 37 hiring systems |
| `probe_sources.py`, `probe_results.json`, `probes/` | 75 candidate sources (16 hiring systems, 23 boards, 13 aggregators, 10 public employment services, 6 non-profit boards, 8 early-career lists): reachable?, items, date and location fields present, junior and senior title counts; first 20 KB of each raw response | `python3 research/sources-2026-11/probe_sources.py` |
| `robots_checks.json` | robots.txt verdict for 20 endpoint hosts | Python `urllib.robotparser` |
| `simplify_summary.json` | SimplifyJobs new-grad and internship lists: totals, active, last 30 days, remote, which hiring systems the remote ones use | the lists' public JSON |
| `board_seeds.json` | Employer board names per hiring system found in both seed sources (careers pages, early-career lists), with where each came from | URL patterns |
| `yield_sample.json` | 150 random early-career employers on Greenhouse/Lever/Ashby run through the real pipeline; 40 Workable boards (all answered HTTP 429) | `scripts/discover_boards.py` functions plus `fetch_jobs.process` |
| `terms_findings.md` | What each shortlisted source's own pages say, quoted, with the verdict | Firecrawl, read 25 Nov 2026 |
