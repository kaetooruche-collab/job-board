# Link checker incident (31 Oct 2026) and the system that stops it recurring

Status: built, tested, merged after this record. Evidence labels: [Established] measured; [Inference] reasoned.

## What happened [Established]
- Refresh run 79 (31 Oct 21:29 UTC) published 826 listings against 1,038 four hours earlier. The raw feed was unchanged (21,055 candidates against 21,057), so the jobs were still open.
- `brokenLinksDropped` jumped from 34 to 229 (normal 34 to 51 over the previous five runs). Every extra removal was a Greenhouse job (Greenhouse 549 -> 341; Ashby and Lever unchanged); 21 whole companies disappeared (Dropbox, Discord, Lyft, Netlify and others).
- A manual refresh at 01:56 UTC restored 1,001 listings with 48 dropped. The board was short for about 4.5 hours.

## Cause
- [Established] The old checker counted any timeout, connection error, 403, 429 or 5xx as a dead link; there was no difference between "page gone" and "could not check", and no memory between runs.
- [Established] The only safety net was "stop the run if listings fall by more than 40%". The drop was 20.5%, so it passed.
- [Inference] The checker was blocked or rate-limited from the GitHub runner for part of that run. The run log does not keep per-link reasons, so this cannot be proved; the fix does not depend on the exact reason.

## The system now (three layers; `scripts/link_check.py`, `tests/test_link_check.py`)
1. **Three verdicts.** ALIVE, DEAD (404, 410 or Greenhouse's "error=true" redirect: definitely gone), UNKNOWN (everything else). Only DEAD removes a listing at once.
2. **Grace for UNKNOWN.** A listing published last run that cannot be checked stays for up to 3 refreshes in a row (about 18 hours) and shows its real last-checked time. A new listing that cannot be checked is not published yet and is retried next run. Memory is in `data/link_state.json`.
3. **Circuit breaker.** If failures are above 12% of links and above 2.5 times the recent median, the checker is treated as blocked: nothing published last run is dropped (even 404-looking failures), the grace counters do not advance, and the Actions log shows a warning. After 4 such runs in a row (about 24 hours) the workflow turns red.
4. **Tighter drift guard.** A drop of more than 15% (was 40%) stops the run and keeps the previous data. Normal refresh-to-refresh moves were 0.1% to 1.5% over the last six runs. To avoid freezing the board on a real, lasting drop, the hold ends after 3 runs in a row and the lower count is accepted. A source losing more than 20% (was 70%) is flagged in the quality report.
5. The commit step now runs even when a run stops, so the hold counters are saved.

## Evidence the fix works
- Incident replay (1,038 published, 229 failing): 1,038 stay published, whether the failures look like timeouts or like 404s. With the circuit breaker removed, 4 tests fail (checked on purpose).
- Real postings: 120 random current listings checked with the new checker: 120 open, same as the old logic (the old logic and the new agree on healthy links).
- End-to-end run on the real feed: 1,001 published; 12 gone, 51 could not be checked (mostly Carvana and Coinbase pages that block automated requests); of those 15 were kept on their older check time and 36 new ones held until checkable.

## Known limits
- A persistently bot-blocked employer page (Carvana today) will fall off after 3 runs, as it did before; it is not silently "verified".
- The listing standard says the link passed a check at the last run. It now reads: passed a check within the last 3 runs (about 18 hours), with the real time shown. The feed itself only lists open roles, which is the stronger evidence.
