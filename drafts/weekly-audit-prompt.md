# Weekly independent audit (prompt for a scheduled Claude Code task; NOT scheduled yet, needs KT's approval)

Purpose: the automatic checks (`scripts/qa_checks.py`, `scripts/site_monitor.py`) catch contradictions and drift. They cannot tell whether a card is TRUE. Only opening the real posting can. This weekly task does that on a random sample and reports.

Prompt:
> You are auditing the job board in the repository kaetooruche-collab/job-board (read-only: change no files, push nothing, change nothing in Brevo).
> 1. Pull the latest `main`. Run `python3 -I scripts/spot_check.py 15`.
> 2. For each listing, open its URL with the Firecrawl scrape tool and compare the card with the real posting: title, company, whether the role is really remote (any hybrid/on-site/office days?), who may apply (countries or regions, employer's own words), experience level asked for, pay (only if the posting states it), and that the posting is still open.
> 3. Read `data/qa_report.md` and the last 8 entries of `data/qa_history.json`.
> 4. Write a short report: how many of 15 cards were fully correct; every mismatch with the exact quote from the posting; whether the same mistake pattern appears more than once; anything odd in the quality report. Do not guess: say "could not open" when a page is blocked.
> 5. If one pattern appears twice or more, state it as a candidate bug class with two example URLs. Do not fix it.
> Never claim to have opened a page you did not open.

When a pattern is confirmed by KT or Claude in an interactive session: (1) add the real text to `tests/fixtures/regressions.json`, (2) fix the classifier, (3) if it is a class of bug, add a rule to `scripts/qa_checks.py` with tests, (4) compare old and new behaviour on a few hundred real postings before shipping.
