# Board issues spotted by the social agency

For the job-board session and KT. The social session never edits the site, `scripts/`, `data/` or `jobs.json`; it only reports here and keeps affected jobs out of posts (`social/data/exclude_jobs.json`).

## 26 Nov 2026 (found while checking roles for the week of 1 Dec)
Checked against the live postings in a real browser on 26 Nov 2026.

| # | Job | Board says | Posting says | Class | Suggested fix (job-board session, with the quality rule: fixture, fix, QA rule, old-vs-new) |
|---|---|---|---|---|---|
| 1 | `jf86468317e` Wistia, Staff Product Design Lead, Hosting ([posting](https://jobs.ashbyhq.com/wistia/23542c6c-90d9-4958-b47b-3a4de4721ee5)) | **Worldwide** | "Fully remote, work from anywhere in the contiguous United States" (the classifier quoted this line in its own evidence) | "anywhere in <country>" read as worldwide | Treat "anywhere in (the contiguous/continental)? <country>" as that country. Add to `tests/fixtures/regressions.json`. |
| 2 | `j63a0b6fc93` Box, "Let's stay in touch. Join our Talent Community!" | **Worldwide** job | Not a job: a talent-community sign-up | Non-job posting | Drop titles like "talent community", "stay in touch", "general application". |
| 3 | `jb19e156074` Netlify, Talent Partner ([posting](https://job-boards.greenhouse.io/netlify/jobs/8919217002)) | **Worldwide** | Location only "Remote". Evidence is company-level: "a remote-first, globally distributed company with 120+ employees working across 13 countries". Pay: "$97,000 - $150,000 for most US-based locations and $95,000 - $143,000 CAD for most Canada-based locations" (opened 26 Nov) | Company-level wording counted as proof (CLAUDE.md says it must not); pay ranges name only the US and Canada | Classify as "Location not specified" (or US/Canada if pay ranges are taken as a signal); the board's card shows only the CAD range, which also understates the US range. |
| 4 | `j724aa7d5d9` Canonical, Enterprise Account Executive - Federal ([posting](https://job-boards.greenhouse.io/canonical/jobs/8416556)) | **Americas** | "Current or previous U.S. government security clearance, particularly for roles supporting defense, intelligence or other federal government customers" | A US-government role shown as region-wide | Flag postings that ask for US citizenship or a US security clearance as US-only (or add a card note). |

Scale: 19 jobs are labelled Worldwide today; 3 of them (16%) are wrong or doubtful. Worldwide roles are exactly what the social posts feature, so this matters more for us than its share of the board suggests.

## Question for KT (not a data bug)
- The board's apply button reads **"Apply on employer site"** (`index.html`, job card). CLAUDE.md bans "straight to the employer" and "the employer's own posting/page" because links open the hiring-system page. "Employer site" is close to that wording; the button's tooltip already says "Opens the original posting on the company's hiring page". Worth a look under the copy-change rule; the social posts use "Apply on the original posting".

## Status (26 Nov 2026, 13:25 UTC)
- Rows 1-4 are fixed in **PR #82**, merged by KT's instruction on 26 Nov 2026 with #81 and #83 (main 91b0d62; tests pass). Box's talent community and Truelogic's "Open Application" will be held back as non-jobs.
- Also merged: **#81** adds 50 employers that hire outside the US; **#83** keeps jobs open outside the US first under the caps (simulated: 1,221 of 2,000 jobs open outside the US, against 693 now; 39 worldwide, against 27).
- `social/data/exclude_jobs.json` stays as it is until the first feed refresh after the merge. Then re-check these jobs on the live feed and remove the entries that are fixed.

## 27 Nov 2026: card labels and pay that contradict the employer's own data (found by the social-qa agent, confirmed via the employers' public feeds)
| Job id | Company | Board shows | Employer's own data | Class of bug |
|---|---|---|---|---|
| j3837f4403a, j16645dc320, j6b2e4703c7, j91e5680f17 | Trafilea | Worldwide | Recruitee `locations[]`: Argentina, Brazil, Chile (location text only says "Remote job") | Classifier ignores Recruitee `locations[]` |
| j8424dc775e | Airwallex | EMEA | Ashby location "UK - Manchester", secondary "UK - Birmingham"; label flipped from "Eligibility unclear" (26 Nov) to EMEA (27 Nov) and the conflict note was emptied | Body text overrides structured locations |
| j0665e514b8 | Fastly | North America | US places only | Same |
| jcee32b0502, j012bfcb29d | Customer.io | Pay: Not stated | "Starting salary for this role is $105k–$122k" / "$170k–$200k" | Pay extraction misses "Starting salary … $Xk–$Yk" in Greenhouse content |
| TransPerfect (4 rows) | TransPerfect | Worldwide | Not checkable from a public feed | Unverifiable source |
Effect on the board: the "Worldwide" count is 35, but only 27 survive the check. The social tools now feature only roles that pass `social/tools/verify_source.py` and count only those. All rows above are in `social/data/exclude_jobs.json` until the board is fixed. Per CLAUDE.md's quality rule, the fix needs regression fixtures (`tests/fixtures/regressions.json`), a QA rule in `scripts/qa_checks.py` comparing labels with structured locations, and an old-versus-new comparison.
