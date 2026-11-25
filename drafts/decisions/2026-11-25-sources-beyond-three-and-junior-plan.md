# Sources beyond Greenhouse, Lever and Ashby, more junior roles, and hands-off running (25 Nov 2026)

KT's request (25 Nov 2026): why are we limited to Greenhouse, Ashby and Lever; how can the whole board run without KT touching it; find remote junior and entry-level jobs; find ways to source outside the three systems, "pour through hundreds of options". Order KT set: think, store data in bulk, analyse, plan and checklist, then execute.

Data (stored first, before any analysis): `research/sources-2026-11/` (inventory in its README). Labels: **Established** = measured or read first-hand on 25 Nov 2026; **Inference** = reasoned from the data; **Assumption** = not checked.

## 1. Why the board used only three systems
- **Established:** the limit was a rule, not a technical wall. CLAUDE.md says "other systems only after checking" their terms, bans scraping sites whose terms forbid it, and bans sources whose dates are not original (Jobicy) or whose terms forbid signups (Remotive). Greenhouse, Lever and Ashby were the only systems checked (31 Oct).
- **Established:** the three systems run half of the remote-first employers whose hiring system could be seen: 115 of 229 careers pages (876 companies read). Workable 21, Workday 20, Recruitee 8, SmartRecruiters 6, JazzHR 6, Teamtailor 5, BambooHR 5, Rippling 4, Breezy 4, Personio 4 make up most of the rest; 543 pages showed no recognisable system.

## 2. What the data says about junior roles
- **Established: junior roles exist but are mostly office jobs.** Of 8,186 postings under 30 days old in the 285 current feeds, 1,166 (14%) are entry, junior or internship level, and 87% of those are on-site or hybrid. I checked the exclusions: none of the 725 excluded "on-site" junior roles mentions remote in its location, and a random sample is genuinely on-site (Carvana lot attendants, Stripe in-office internships). The classifier is not throwing remote junior work away.
- **Established: even lists built for graduates are rarely remote.** SimplifyJobs' new-grad list has 900 roles from the last 30 days, 82 of them remote (9%); its internship list has 1,592, 47 remote (3%).
- **Established: 63 publishable junior roles are lost after classification.** 149 junior roles pass the remote rules; 86 are live. The losses are location duplicates and the limit of 15 listings per company, which keeps each employer's newest 15 and ignores level.
- **Established: early-career employers are the largest untapped pool, on the systems already cleared.** The early-career lists link to 1,819 Greenhouse, Lever and Ashby boards not on the board (791, 314, 714). In a random sample of 150 of them, run through the real pipeline: 138 live, 6,157 postings, 157 publishable, **14 junior, entry or internship**; 38 boards had at least one publishable listing, 9 at least one junior one.
- **Inference:** adding the productive part of those 1,819 boards would add roughly 1,900 listings and roughly 170 publishable junior roles, about double today's junior supply. Most would be US or country-restricted; it does not fix the worldwide gap (16 of 1,076 live listings are worldwide).

## 3. The options, weighed (75 sources probed, terms read for the shortlist)
Full table with quotes: `research/sources-2026-11/terms_findings.md`.
- **Use:** Recruitee (its terms call the careers site public), Personio (vendor-documented public XML feed). Both carry original posting dates and specific links. Small yield today: 15 and 4 employer boards found in the seeds.
- **Use after a test from GitHub's servers:** Workable (terms silent; public embed endpoint; 261 employer boards in the seeds, and the biggest host of remote junior roles in the early-career lists: 47 of 129). Every request from this environment got HTTP 429, so whether it works from GitHub's runner is unknown.
- **Hold:** Breezy (vendor docs not read), JazzHR (no date in the feed; one page fetch per job), Rippling (terms not read; date only per job), Workday (dates are relative, "Posted 16 Days Ago"; per-employer hosts), We Work Remotely (unchanged), ReliefWeb (needs an app name requested from KT's email).
- **No:** BambooHR (its terms forbid robots and spiders copying content), Teamtailor, SmartRecruiters, Pinpoint, Landing.jobs (robots.txt disallows), Himalayas ("pubDate: when the job was last updated", not the original date; also forbids passing jobs to Google), Remote OK (dates cannot be verified: 0 of 100 latest jobs link to an employer page), Arbeitnow (re-serves systems that block us), The Muse (blocks automated clients), paid data vendors (cost; resale of Google, LinkedIn and Indeed data), scraping other boards' websites (CLAUDE.md "Do not"), national employment services (local-language, local jobs, few remote).
- **Public-claim consequence (Established):** `/verify` says "We read the public job pages that companies publish through Greenhouse, Lever and Ashby". Showing Recruitee, Personio or Workable listings makes that false, so under the copy-change rule the new systems stay switched OFF until KT approves the new wording (options in section 6).

## 4. Hands-off running: what is left
- **Established:** the GitHub side runs alone (refresh, monitor, tests, discovery, failure issues). The Claude doctor reads but cannot push: a scheduled task created from a session cannot attach a repository (tested 25 Nov).
- **Option to remove the KT step (Inference, to be tested):** create a Claude session that has the repository attached from the start and point the doctor's schedule at that session (`persistent_session_id`). If a test push succeeds, KT never has to edit the task. If it fails, KT's 2-minute step stays.
- **New risk from growth (Established):** `jobs.json` is 1.9 MB for 1,067 listings and the home page loads all of it. About 3,000 listings would be about 5.5 MB. Growth needs a ceiling and a size alarm.

## 5. Plan and checklist (in order; each item has its acceptance test)
- [ ] **A1. Doctor push access without KT.** Session with the repository attached; doctor schedule points at it; test-fire. *Accept:* `git push --dry-run` succeeds from the scheduled run. *Else:* keep KT's step in the to-do list.
- [ ] **A2. Size alarm.** `health_check.py`: amber above 4 MB, red above 6 MB for `jobs.json`. *Accept:* tests.
- [ ] **B1. Fix the thread-unsafe print silencing in `discover_boards.py`** (found during research: it can swallow output). *Accept:* a quiet flag on `fetch_jobs.process`; tests pass.
- [ ] **B2. Early-career seeds in discovery.** The weekly workflow reads the SimplifyJobs lists, keeps only each link's hiring system and board name, and offers those boards first; the board name comes from the employer's own posting link, so it is the right company. The lists' content is never stored or shown. *Accept:* unit tests; a dry run finds boards.
- [ ] **B3. Growth limits.** Weekly adds 40 → 100; discovery stops adding while 2,500 or more listings are live. *Accept:* tests.
- [ ] **B4. Junior roles keep their place under the per-company limit.** Within an employer's 15, entry, junior and internship roles are kept first, then the newest. *Accept:* old versus new on the real feed: more junior roles live, total unchanged, nothing else lost.
- [ ] **B5. One-time backfill run** (dispatch with larger limits), then a refresh. *Accept:* junior, entry and internship listings live rise from 86; QA report normal; `jobs.json` under 4 MB.
- [ ] **C1. Recruitee and Personio readers, switched OFF.** Built, tested on real boards, held behind `ENABLED_SYSTEMS` until KT approves the `/verify` wording. *Accept:* unit tests; old versus new shows zero change while off.
- [ ] **C2. Workable test from GitHub's servers** (a manual workflow that reads 5 boards and reports the status codes). *Accept:* the report decides whether a Workable reader is worth building.
- [ ] **D. Records.** Update `drafts/operations/autopilot.md`, `drafts/kt-todo.md` and CLAUDE.md's sourcing facts.

## 6. Needs KT (nothing below is done without a yes)
1. **Switch on Recruitee and Personio** (and Workable if C2 passes). The `/verify` sentence would change. Options:
   - (a) "We read the public job pages that companies publish through their hiring systems (mostly Greenhouse, Lever and Ashby, plus Recruitee and Personio)."
   - (b) "We read the public job pages companies publish through the hiring systems they use, such as Greenhouse, Lever, Ashby, Recruitee and Personio."
   - (c) Keep today's sentence and stay on three systems.
   Recommendation: (b). It stays true as systems are added, names the main ones, and keeps "we don't copy from other job boards", which is still true. The home page's "(usually Greenhouse, Lever or Ashby)" stays true either way.
2. **ReliefWeb app name** (humanitarian jobs, some home-based): only worth it if KT wants that niche.
