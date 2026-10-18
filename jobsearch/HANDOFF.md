# Handoff: KT's pharmacy job search (started 18 Oct 2026 in the job-board chat)

## Who and what
KT: MPharm graduate (2024), NOT a registered/licensed pharmacist. Wants pharmacy and pharmacy-adjacent jobs: pharmacist roles, healthcare operations, clinical strategy, implementation, medical information, drug safety (pharmacovigilance), regulatory affairs, clinical operations, product, customer success. Do not rule a job out for an unfamiliar title: read what it asks the person to do. Many roles require residence in the employer's country, which is KT's main obstacle. Wanted: a LIST (not a board) of active jobs posted within 7 days, target 50, each read in full; then, per chosen job: map requirements to KT's background, a tailored CV, a cover letter if needed, the published contact email, and a checklist, continuously.

## What exists (all in `jobsearch/`)
- `pharmacy-jobs.xlsx` (also `.md`, `.csv`, `.json`): 38 active jobs (10 A, 28 B), posted 11 to 18 Oct 2026, each with requirements, duties, eligibility quotes, CV keywords, MPharm overlap, gaps, apply link, contact (none published on any posting so far), and check-off columns. Second sheet: 41 ruled out (C) with reasons. Built by `verify_and_build.py` from `raw/*.json` (five role-family files) plus `corrections.json`.
- Honest result: 38, not 50. Short because 7 days is tight and nearly all remote entry-level roles are tied to one country or ask for experience.
- Quality: an independent audit of 10 random records found 9 of 10 fully correct on date, status, location, requirements and pay (error: a wrong extra location on an Ergomed role, fixed). The auditor thought 4 ratings too generous; a stricter standard (v2, in `AGENT_BRIEF.md`) was applied to the whole list, moving 7 roles from B to C. Details: `audit_result.md`, `corrections.json`.
- Tools: `find_jobs.py` + `discover_boards.py` (public Greenhouse/Lever/Ashby feeds of health/pharma employers; `companies.json`, `candidates.json`), `AGENT_BRIEF.md` (rules for research agents), `verify_and_build.py` (merge, dedupe, re-check links, build files), `templates/` (CV tailoring rules, cover letter, application email).
- Method notes: strongest sources were employer ATS data: Workday tenant JSON (Thermo Fisher/PPD, IQVIA, ICON, Parexel, Fortrea, Labcorp, AstraZeneca, Novartis, GSK, MSD, Amgen, Medtronic and others), SmartRecruiters (Ergomed, PSI), Greenhouse, Lever, Ashby. Aggregators (Himalayas, Remote Rocketship, DailyRemote) are for discovery only. Jobicy re-dates old postings: ignore its dates. Firecrawl search sometimes rate-limits (429): run searches one at a time. Workable returns 429 to scripts. Phenom career pages (e.g. Cencora) contain a hidden "no longer available" template; the link check ignores it.
- Parallel research agents worked well: one per role family with `AGENT_BRIEF.md`, then an independent audit agent on a random sample.

## Strongest current matches (A)
ICON Study Start Up Associate (Sydney; and Barcelona), Thermo Fisher Assistant CRA (Johannesburg), Thermo Fisher Clinical Trial Coordinator I and Country Approval Associate (Mexico), Thermo Fisher Associate Safety Specialist (remote, India), Thermo Fisher Regulatory Affairs Specialist II (Mexico City; closes 30 Oct), MSD Global Submissions Publishing (Hyderabad), AstraZeneca Global Study Associate (Warsaw; closes 28 Oct), Amgen Medical Information Specialist (Istanbul, hybrid, asks for a pharmacy graduate). Almost none states whether non-residents may apply.

## What is missing (needs KT; see TODO.md)
1. KT's master CV (put in `private/` or paste). Nothing can be tailored without it.
2. Eligibility: where KT lives, citizenship and work-permit facts, relocation, languages, registration steps in progress, pay floor, contract/part-time. (KT's WhatsApp number is +90 and KT is linked to the job-board business in Cyprus; do not assume the passport or work rights.)
3. Which 5 to 10 jobs to start with (suggest the A roles that close soonest).
4. Approval for a weekly refresh (recurring task).
5. Optional: KT searches LinkedIn by hand and pastes links; read and verify them the same way.

## Next steps once KT answers
- Filter the list by KT's real eligibility and re-rate; report how many are truly open to KT.
- For each chosen job: requirement-to-evidence map (only from KT's CV and answers), tailored CV (`templates/cv-tailoring-rules.md`), cover letter if wanted, application email draft only if the employer published an address, tick the check-off columns.
- Chase unverified leads: Viatris Associate Regulatory Affairs Executive (Lisbon), ICON Graduate PV Associate (Mexico City; 10 Oct, just outside the window; jid-54436). Widen the search with new queries and employers; rerun `verify_and_build.py`.
- Never send anything on KT's behalf without explicit approval.

## Boundary
The job board and Kaeto Career Services page are handled in a different chat. Do not edit board files (`index.html`, `services.html`, `scripts/`, `data/`, `.github/`). Only touch `jobsearch/` and this project's lines in `drafts/` if KT asks.
