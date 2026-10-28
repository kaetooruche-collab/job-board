# Feed-shape drift check against the strategy review

28 Oct 2026. Compares the current feed with the audit in
`drafts/decisions/2026-10-24-board-strategy-icp-inventory-seniority.md` (pulled 23 Oct 21:21 UTC,
1,026 listings, 160 employers). Everything below is **[Established]** — counted from `jobs.json` and
`data/metrics.json`, not estimated.

**Snapshot caveat:** this branch's `jobs.json` was last written by the 26 Oct 12:52 UTC refresh; the
scheduled fetch commits to `main`, and this working branch has not been updated since. The live site
was separately confirmed fresh by `scripts/site_monitor.py` on 28 Oct (newest listing 3.1 h old), so
the production board is current — the figures below are up to two days behind it, which affects
"recent" counts but not the structural shares.

## Headline: the feed has not drifted

| Measure | Strategy doc (23 Oct, n=1,026) | Now (26 Oct, n=1,002) | Drift |
|---|---|---|---|
| Listings | 1,026 | 1,002 | −24 (normal churn) |
| Employers | 160 | 154 | −6 |
| Senior + leadership | 448 = 43.7% | 437 = **43.6%** | −0.1 pp |
| Early career (entry + junior + internship) | 96 = 9.4% | 94 = **9.4%** | 0.0 pp |
| Level not stated | 146 = 14.2% | 145 = 14.5% | +0.3 pp |
| Eligibility **unclear** | 264 = 25.7% | 250 = **25.0%** | −0.7 pp |
| **Worldwide** | 17 = 1.7% | 17 = **1.7%** | 0 listings changed |
| Region-only | 21 | 21 | 0 |
| US-only | 41.7% | 42.0% | +0.3 pp |
| Eligibility stated | 74.3% | 75.0% | +0.7 pp |
| Confirmed remote | 91.2% | 91.0% | −0.2 pp |
| Pay stated on the card | 601 = 58.6% | 593 = 59.2% | +0.6 pp |
| Location-variant rows | 103 of 1,026 | 102 of 1,002 | unchanged pattern |

Distinct roles are counted differently here (title + company, lower-cased and whitespace-collapsed:
900 distinct of 1,002) than in the strategy doc (793 of 1,026), so the two distinct-role figures are
not directly comparable; the variant-row counts are, and those match.

## What this means for the strategy review

1. **Every structural finding still stands, to the decimal.** The three numbers that drove the review —
   43.6% senior+, 1.7% worldwide, ~25% unclear — are unchanged five days later. The review's status
   stays PROPOSED and its recommendation (option D: fix and relabel now, source only to fill a proven
   gap) is not weakened or strengthened by new data.
2. **The supply gap is real and stable, not a snapshot artefact.** Worldwide openings stayed at exactly
   17 while the rest of the feed turned over by 24 listings. More Greenhouse/Ashby/Lever boards of
   US-based scaleups will still not move it — the sourcing brief has to target employers that hire in
   many countries, with the curated company list for KT's approval.
3. **The senior-heavy shape is a property of the sources, not of a default.** With senior + leadership
   at 43.6% and early career at 9.4%, any global "early career" default would hide most of the board.
   The decision to keep all levels visible and segment by link (`?level=early`) is confirmed, not
   overturned.
4. **Watch item — inflow is slowing.** Median listing age rose from 7.5 days (23 Oct) to 11 days (26
   Oct), and listings posted within the last 7 days fell from 469/1,026 (45.7%) to 399/1,002 (39.8%).
   Part of that is the two-day snapshot gap; if it persists on a fresher pull it means the source
   feeds are producing fewer new roles, which is the Gate-1 question in disguise. Re-measure from a
   current pull before acting.
5. **30-day rule is enforced by the refresh, not by this snapshot.** Two rows in the 26 Oct snapshot
   are now older than 30 days (Wrike, 30.1 d; ClassDojo, 31.6 d) because no refresh has run on this
   branch since. They would be dropped on the next fetch; the live site monitor confirms live data is
   3.1 h old.

## What was not checked

- No traffic or click data (GoatCounter needs KT's login), so nothing here says whether the shape is
  good for the business — only that it is unchanged.
- The doubtful early-career labels (~26) and the 8 host pages that did not show their posting were not
  re-audited; those remain open in the strategy review's roadmap.