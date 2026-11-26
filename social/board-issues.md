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
- Rows 1-4 are fixed in **PR #82** (open, waiting for KT's merge). Box's talent community and Truelogic's "Open Application" will be held back as non-jobs.
- Related open PRs: **#81** adds 50 employers that hire outside the US; **#83** keeps jobs open outside the US first under the caps (simulated: 1,221 of 2,000 jobs open outside the US, against 693 now; 39 worldwide, against 27).
- `social/data/exclude_jobs.json` stays as it is until the first feed refresh after the merge. Then re-check these jobs on the live feed and remove the entries that are fixed.
