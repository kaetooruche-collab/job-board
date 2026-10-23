# Decision review: KT's pharmacy job-search system (proportionate)

Status: STARTED 18 Oct 2026 on KT's request. Personal project, separate from the public job board.

## Request
KT (MPharm, graduated 2024, not a registered pharmacist) wants an extensive LIST (not a board) of active pharmacy and pharmacy-adjacent jobs posted within the last week, target 50, found without the job board's pattern classifier, and a repeatable system: source the job, read the posting, map its requirements to KT's background, design a tailored CV and cover letter, find the relevant published contact email, and tick off a checklist per job, continuously.

## Decisions
- **Method:** reading, not pattern-matching. Candidates come from (a) public employer job-board feeds (Greenhouse, Lever, Ashby) and (b) dated web searches for each role family, each posting then opened and read in full by a research agent and re-checked by a script. Seven role families: pharmacovigilance, medical information, regulatory/quality, clinical operations, health-tech operations/implementation/customer success/clinical product, pharmacy operations, pharmacist roles open to unlicensed or overseas graduates.
- **Fit is rated honestly** (A meets the stated minimum, B a stretch with one gap, C not realistic). KT's own framing is that pharmacy experience overlaps with many unfamiliar titles, which is true for several families; it is not true for roles that legally need a licence, 5+ years or a PhD. C roles are listed with reasons, not hidden and not padded into the count.
- **Freshness:** posted within 7 days, date taken from the posting or the employer's data, page shows an open application, link re-checked by script.
- **Eligibility is the main filter KT cares about** (many roles require residence in the employer's country). Each record carries the posting's own residency, work-authorisation, language and licence wording.
- **Contacts:** only emails the employer published, with the page where it was found. No guessing, no scraping of people.
- **Not used:** LinkedIn, Indeed, Glassdoor and similar (their terms forbid automated access). KT can search them by hand and paste links; those jobs are then read and checked the same way.
- **Personal data:** KT's CV and tailored documents live in `jobsearch/private/` in the private repository, excluded from the deployed website by `.vercelignore`. Nothing is sent to anyone without KT's approval; Claude only drafts emails.
- **No invented content:** CVs and letters use only what KT's CV and answers support.

## Risks and limits
- Large pharma and CROs often block automatic checks; those links are marked "verified by opening the page" and should be re-opened by KT before applying.
- Seven days is a short window and many strong roles are country-locked; reaching 50 AND being eligible for most of them may not be possible. The list reports how many survive an eligibility test once KT states their eligibility.
- Entry-level pharmacovigilance, medical information and regulatory roles are the most realistic families; clinical strategy and product roles usually ask for experience.
- Weekly refresh needs a recurring task (KT approval) or a manual re-run.

## Inputs needed from KT
Master CV; country of residence and any passport/work-authorisation facts; willingness to relocate; languages; target pay floor; contract or part-time acceptable; whether to include roles needing relocation; any registration status or licensing steps in progress; any work or placement experience worth naming (pre-reg year, internships, projects).
