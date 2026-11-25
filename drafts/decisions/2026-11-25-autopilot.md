# Decision: run the board on autopilot (25 Nov 2026)

Status: DONE by Claude on KT's instruction of 25 Nov 2026 ("I want everything to run seamlessly, continuously, without me ever touching it again ... you decide"). Runbook: `drafts/operations/autopilot.md`.

## What happened (established)
- The 6-hourly refresh failed on every run from 21 Nov to 25 Nov (28 runs, earliest checked 21 Nov 06:58 UTC; the last good data was 18 Nov 20:26 UTC). Cause: a test that reads the live `jobs.json` failed after the 18 Nov data arrived ("marketplace" counted as half of "marketing", so a weak title match ranked below description-only results), and the refresh runs all tests before fetching. Data that broke a test could never be replaced: a deadlock.
- The live-site monitor reported "the refresh may be stuck" on every 3-hourly run from 22 Nov. No person or routine acted on it: a red mark in the Actions tab notifies no one who acts.
- The Tuesday email routine ran on 24 Nov from 7-day-old data, scheduled campaign 106, and could not push its record because it had no repository access.

## What was decided, and why
1. **Data can never block the refresh again.** Tests that read live data are skipped inside the refresh (`YC_SKIP_LIVE_DATA=1`) and run daily in `ci.yml`. Alternative rejected: deleting the real-data tests (they caught a real search bug). The search rule the test checked now holds by construction (title matches rank first), not by luck with the data.
2. **Failures reach someone.** `scripts/gh_alert.py` keeps one GitHub issue per failing workflow (GitHub emails the owner once, the doctor reads it). Alternatives rejected: email from the workflow (needs SMTP credentials in GitHub, a new secret to manage); Slack or WhatsApp (not connected; WhatsApp automation needs a paid API).
3. **A daily Claude doctor fixes things.** GitHub Actions can only report; diagnosing a new failure needs judgment. A Claude scheduled task runs `scripts/health_check.py` and the runbook. It may merge pipeline fixes alone (the PR-and-squash-merge pattern KT approved); copy, prices, sending, Brevo, new source types and money still need KT (runbook section 3). Risk: an automated merge introduces a bug. Mitigation: full test suite plus the `test` check on the pull request before every merge, the drift guard, and the health check the next day.
4. **The employer list grows and prunes itself** (`scripts/discover_boards.py`, weekly). Source of candidates: the Remote In Tech directory (ISC licence; 876 companies on 25 Nov, 397 marked worldwide). Only Greenhouse, Lever and Ashby, whose public feeds were checked for this use (`2026-10-31-ats-terms-check.md`). Dry run on 25 Nov: 60 candidates probed, 9 boards found, 4 would add listings (Articulate, Brave, Canonical, Chainguard; all worldwide in the directory). Expected over about five weeks: roughly 50 new employers, mostly worldwide-hiring (inference from the dry-run rate). Safety caps: 40 adds and 15 retirements per run, an outage guard, a 90-day re-probe window, a removal blocklist, and every listing still passes the classifier and QA.

## Considered and NOT done (each needs KT or more evidence)
- **More hiring systems (SmartRecruiters, Workable, Recruitee, Personio).** They publish public feeds too, but their terms are not checked. CLAUDE.md: "other systems only after checking". This is the next step if KT wants more variety. It is the strategic review's real supply question (roles open outside the US), and more US boards of the same three systems will not fix that alone.
- **Scraping job sites or using paid data providers (Firecrawl's Indeed, Glassdoor and LinkedIn providers, TheirStack).** Not done: republication rights are unverified, the cost is per call, and the project rule bans scraping sites whose terms forbid it.
- **Replacing the HTTP link check with "still in the employer's feed".** A job present in the live feed is open by definition, so the 403 throttling would stop mattering. Deferred: the checker is healthy now (3.1% unreachable on 25 Nov), and changing what "verified" means touches the trust copy on /verify.

## How we know it works
- 25 Nov: refresh dispatched after the fix and green; 1,036 listings published, 3.1% of links unreachable.
- Tests: 220+ pass in full mode and in refresh mode. The health check reads the 18-25 Nov outage as RED in its tests.
- Brex fix: regression fixture plus a QA rule; old versus new compared on every posting in the feeds (numbers in the pull request).
