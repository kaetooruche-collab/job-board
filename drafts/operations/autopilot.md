# Autopilot: how the job board runs without KT

Written 25 Nov 2026 after the board froze for 7 days (18 to 25 Nov) and nobody noticed. This is the runbook for the daily Claude "doctor" routine and the one page that explains the whole system. KT's instruction (25 Nov 2026): "I want everything to run seamlessly, continuously, without me ever touching it again."

## 1. What runs, when, and what it does

| What | When (UTC) | Where | Job |
|---|---|---|---|
| Refresh job listings (`fetch-jobs.yml`) | every 6 h at :15 | GitHub Actions | Read 285+ employer feeds, classify, QA, check links, publish `jobs.json`; Vercel redeploys on the commit |
| Watch the live site (`site-monitor.yml`) | every 3 h at :40 | GitHub Actions | Pages load, data fresh, prices and contact details right, forbidden wording absent, sample of apply links open |
| Tests (`ci.yml`) | daily 04:05, and on every code change | GitHub Actions | Full test suite, including tests that read live data |
| Discover and prune boards (`discover-boards.yml`) | Sundays 02:35 | GitHub Actions | Retire dead or empty boards; add up to 100 new Greenhouse, Lever or Ashby boards a week: worldwide-hiring companies (Remote In Tech directory) first, then employers from the SimplifyJobs early-career lists; stops adding while 2,500 or more listings are live |
| Weekly analytics snapshot (`weekly-snapshot.yml`) | Tuesdays | GitHub Actions | GoatCounter numbers and funnel into `drafts/analytics/` |
| Board doctor (Claude scheduled task) | daily 10:10 Istanbul | Claude, one persistent session with the repository attached (`session_01Q41EjsB4isNkvh3EEkLuzg`) | This runbook: health check, diagnose, fix, verify, report |
| Tuesday weekly job email (Claude scheduled task) | Tuesdays 08:20 Istanbul | Claude, fresh session | Build the digest, safety checks, schedule for 09:30 Istanbul |

Any GitHub workflow that fails opens one issue titled "Autopilot: <workflow> is failing" (`scripts/gh_alert.py`). GitHub emails KT once when it opens; it is updated, not duplicated, and closed automatically when the workflow passes again.

GitHub runs scheduled workflows best-effort: measured 18-25 Nov 2026, the refresh really ran every 10-16 hours (about twice a day) and the monitor every 6-12. That is enough for listings up to 30 days old; `scripts/health_check.py` only alarms past 26 hours without fresh data.

## 2. The doctor's checklist (do it in this order, every day)

1. Run `python3 scripts/health_check.py`. GREEN everywhere: go to step 6.
2. For each RED or AMBER line, and each open `autopilot` issue, find the cause from the evidence, not a guess: the failed run's log (`gh api repos/kaetooruche-collab/job-board/actions/runs/<id>/jobs`, then `.../actions/jobs/<job_id>/logs`), `data/qa_report.md`, `data/metrics.json`, `data/discovery_report.md`.
3. Fix it on a branch with a test that fails before and passes after (the CLAUDE.md quality rule: real text into `tests/fixtures/regressions.json` for classifier bugs, a QA rule for a class of bug, an old-versus-new comparison on real postings before a classifier or QA change ships).
4. Run `python3 -m unittest discover -s tests` (and `YC_SKIP_LIVE_DATA=1` for the refresh's view). Open a pull request, wait for the `test` check, squash-merge (the approved pattern), then dispatch the workflow that failed and watch it go green.
5. Comment on the autopilot issue what was wrong and what changed. The next green run closes it.
6. On Mondays, the truth audit: `python3 scripts/spot_check.py` on 15 random listings, following `drafts/weekly-audit-prompt.md`; report real numbers ("14 of 15 correct"). Every wrong listing is a bug: fixture, fix, rule, comparison.
7. Report to KT only when something happened: what broke, what was fixed, what (if anything) needs KT. A green day with nothing done sends nothing.

## 3. What the doctor may fix alone, and what needs KT

May fix and merge alone (pipeline upkeep): failing tests and workflows, classifier and QA bugs found by evidence, link-checker and feed problems, a board that moved hiring systems, dependency and GitHub Actions version updates, re-enabling a workflow GitHub disabled for inactivity, docs in `drafts/operations/`.

Must stop and ask KT: any change to public copy (CLAUDE.md copy-change rule), prices, packages or service terms; anything that sends email or messages to real people outside the approved Tuesday routine; Brevo lists, contacts or automations; adding a new kind of source (a hiring system or site whose terms are not checked); spending money; removing more than 15 boards or more than 15% of listings in one change; anything that needs a login only KT has.

## 4. Known failure modes and the fix for each

| Symptom | Likely cause | Fix |
|---|---|---|
| Refresh red at "Run classifier tests" | a code change broke a test | fix the code or the test; never skip or delete a test to get green |
| Refresh red at "Fetch and verify listings", drift abort | a big source returned far fewer jobs | the guard holds for up to 3 runs, then accepts; check the source in the run log |
| "Tests" red, refresh green | new data broke a live-data test (the 18 Nov case) | fix the code so the rule holds by construction, add a fixture test |
| Link checker blocked streak | Greenhouse throttling the runner (HTTP 403) | listings are kept on older checks for 3 runs; if it persists, lower `workers` in `scripts/link_check.py` |
| Live site stale but refresh green | Vercel deploy failed | Vercel connector `list_deployments` for project `north_cyprus_remote_job_board` |
| A workflow shows `disabled_inactivity` | GitHub stops schedules after 60 days without repository activity | `gh api -X PUT repos/kaetooruche-collab/job-board/actions/workflows/<file>/enable` |
| Discovery adds a wrong company | a guessed board passed the identity check | remove it from `data/boards.json`, add it to `data/board_blocklist.json`, add a test |
| `jobs.json` above 4 MB (health check amber) | the board grew past what phones load quickly | lower `MAX_LIVE_LISTINGS` in `scripts/discover_boards.py` or `MAX_PER_COMPANY` in `scripts/fetch_jobs.py` |
| The doctor's session is gone or archived | sessions can be archived | create a new session with the repository attached (create_session with source_url) and point a new daily task at it with `persistent_session_id`; delete the old task |
| A company asks to be removed | removal request (CLAUDE.md) | delete it from `data/boards.json` and add it to `data/board_blocklist.json` in one commit; reply within a day |

## 5. Quality layers (unchanged, now watched)

1. `tests/` and `tests/fixtures/regressions.json`. 2. `scripts/qa_checks.py` inside every refresh (BLOCK and WARN rules, drift guard). 3. `scripts/site_monitor.py` on the live site. 4. The Monday truth audit (the only layer that tests truth). 5. `scripts/health_check.py`, the doctor's view across all of them.

## 6. What only KT can do

- Logins and approvals: re-authorise a Claude connector when a scheduled task reports ACCESS_DENIED (claude.ai, Settings, Connectors), the GoatCounter and Vercel dashboards.
- Decisions listed in section 3.
- Nothing else. If KT is asked for anything not on this list, the system failed.
