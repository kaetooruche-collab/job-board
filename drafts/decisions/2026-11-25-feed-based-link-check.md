# The employer's live feed decides whether a job is open; pages are a sample (25 Nov 2026)

Approved by KT on 25 Nov 2026 ("Yes, fix the link checker that way").

## Why
- Opening every apply page at every refresh gets throttled by the hiring systems (HTTP 403). On 25 Nov, after many refreshes, 27.6% of pages "could not be checked": 375 new jobs were held back, 120 were kept on older checks, and the workflow went red (issue #74). The board's freshness depended on a page check that the hosts block, not on whether the jobs were open.
- **Established (25 Nov):** a hand sample of 150 jobs then in their employers' feeds: 149 pages opened normally, 0 were gone, 0 showed "closed" wording; the one exception (Carvana) blocks all automated visitors. Employers' hiring systems remove a role from the public feed when it closes.

## What changed
1. Every listing in this refresh's feeds is verified at this refresh. A role that leaves the feed leaves the board at the next refresh. Each card's "Where this comes from" panel now shows "Last seen in the employer's job feed", which makes trust rule 4 ("Every listing shows ... when we last checked it") true per card; before, only a board-wide "Last updated" was shown.
2. A sample of 60 pages is opened per refresh, gently (4 at a time), new listings first and then the longest unchecked. A page that is really gone (404, 410, Greenhouse's error redirect) removes the listing and keeps it off for 7 days even if the feed still lists it; "could not open" (403, timeouts) changes nothing.
3. The alarm now fires on what matters: more than a quarter of the sampled pages gone (first set at 10%; the first live run found 7 of 55 = 12.7%, five of them one employer, Wing, whose careers site returns 404, all removed automatically, so the line was raised to systemic problems only) although the feed lists them, two refreshes in a row (`mismatchStreak` in `data/link_state.json`; the workflow step and `scripts/health_check.py` read it). Throttling is no longer an alarm.

## Public wording corrected in the same change
- /verify described the old rule ("If a page can't be reached ... re-checked ... for up to about 18 hours") and promised "unclear" labels; both rewritten to describe what now happens.
- "Updated every 6 hours" appeared on the home page (share text and signup line), /verify, the post kit and the share image. Measured 18-25 Nov: GitHub ran the "6-hourly" refresh every 10-16 hours. All now say "updated daily", which is true; `tests/test_source_claims.py` fails if "every 6 hours" returns.

## Risk and how it is watched
A feed could list a role whose page is gone (a broken posting). The page sample catches this; a repeat pattern raises the alarm. The Monday truth audit by the board doctor still opens 15 random postings.
