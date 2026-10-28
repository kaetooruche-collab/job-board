# Continuous optimization — setup, access and operating rhythm

Created 28 Oct 2026 from the master prompt for the ongoing optimization agent. Everything below was
**checked in this environment today**, not assumed. Status labels: **[OK]** works now ·
**[MISSING]** unavailable, with the practical fix · **[APPROVAL]** needs KT's yes first.

## 1. Access matrix (verified 28 Oct)

| Capability | State | Evidence / what it means |
|---|---|---|
| Git repository (read, commit, push to `main`) | **[OK]** | Pushed twice today (`228ab51`, `2fa6a6c`) via authenticated tool; plain `git push` has no local credentials |
| GitHub Actions **runs** | **[OK]** | `fetch-jobs.yml` cron `15 */6 * * *`, `site-monitor.yml` cron `40 */3 * * *`; live data confirmed 6.0 h old today |
| GitHub Actions **logs / manual dispatch** | **[MISSING]** | `gh` CLI is unauthenticated. Fix: `gh auth login` or paste a fine-grained PAT as `GH_TOKEN`; until then, Action outcomes are inferred from the live site, not read from logs |
| Vercel deployment | **[OK], indirect** | Push to `main` redeploys (verified today: markers appeared on the first poll). No Vercel CLI/token, so build logs are not readable — failures would show up as the live site going stale or the monitor failing |
| GoatCounter analytics | **[OK]** | `GOATCOUNTER_API_KEY` in `.env` (git-ignored, never printed); `scripts/gc_snapshot.py` returned 152 pageviews / 14 events today |
| Brevo email (create campaign, schedule, send) | **[MISSING]** | No API key in this environment and no browser session. Digest **files** generate fine (`data/weekly_digest.{txt,html}`, 299 jobs, UTM + unsubscribe intact). Practical fix: KT keeps the Tuesday send-by-hand ritual, or adds a Brevo key as a repo/Vercel secret — **[APPROVAL]** either way, since any real send is gated on KT's initial authorisation |
| Payments (Whop) | **[APPROVAL] / off** | `SITE.checkout.mode = 'off'`. Nothing to optimise; going live needs `drafts/whop-go-live-checklist.md` + KT's yes + a linked payout account |
| Headless browser (rendered UI review) | **[OK]** | Playwright + system libs installed locally; used for the 1440/360 passes today |
| Background execution **inside this chat** | **[MISSING]** | Not possible — a prompt does not create background jobs. Practical fix: GitHub Actions cron, which is real infrastructure already used twice in this repo |

## 2. What is scheduled today, and the gap

- Every 3 h: live-site monitor (pages, freshness, tracking, forbidden wording, prices, apply links).
- Every 6 h: job feed refresh + QA gates.
- **Nothing** schedules: the analytics snapshot, the weekly digest refresh, or the weekly report —
  all three depended on someone remembering.

**Added this session:** `.github/workflows/weekly-snapshot.yml` — Tuesdays 05:00 UTC (08:00
Istanbul, KT's Tuesday-morning slot) plus manual dispatch, runs `gc_snapshot.py` and commits the
dated file to `drafts/analytics/`. **[MISSING until one step is done]** it needs the key as a
repository secret: GitHub → Settings → Secrets and variables → Actions → add
`GOATCOUNTER_API_KEY`. Without it the job fails with an explicit error rather than writing nothing.
I cannot trigger it from here (`gh` unauthenticated), so its first real proof is either KT pressing
"Run workflow" or next Tuesday's run.

## 3. Operating rhythm (mapped to infrastructure that actually exists)

| Cadence | Task | Runs where | Output |
|---|---|---|---|
| Every 3 h (automatic) | Live health, freshness, wording, prices, apply links | `site-monitor.yml` | failure surfaces as a stale site; `scripts/site_monitor.py` also runnable by hand |
| Every 6 h (automatic) | Feed refresh + QA BLOCK/WARN gates | `fetch-jobs.yml` | `data/qa_report.md`, `jobs.json` |
| **Daily (agent session)** | Run tests + monitor, check for regressions, fix low-risk UI defects, log work | this chat | green suite, `drafts/ux-optimization-log.md` |
| **Weekly (agent session)** | Snapshot funnel, review desktop+mobile, reprioritise the backlog, ship the top item, prepare the email, write the report | this chat + `weekly-snapshot.yml` | `drafts/analytics/GC-*.md`, `drafts/optimization/backlog.md`, report |
| **Weekly (KT)** | Send Tuesday email, post from `/kit`, check replies | Brevo + WhatsApp (by hand) | audience growth |
| **Monthly (agent session)** | Monetisation/packaging/retention/technical-debt/data-quality review | this chat | decision doc in `drafts/decisions/` |

## 4. Approval boundaries (from CLAUDE.md + the master prompt)

**I do without asking:** audits, analytics reads, drafts, tests, low-risk UI and copy fixes,
reversible changes on the branch, monitoring, logging, backlog maintenance.
**I ask first:** prices and payment changes, hard paywalls, business-model or service-scope
changes, new personal-data collection, privacy/consent changes, new payment integrations,
high-risk architecture, **any marketing send before initial authorisation**, and **pushing to
`main`** (project rule) — though KT approved today's two pushes explicitly.

## 5. Rollback

Every change ships as a commit to `main`. Rolling back = `git revert <sha>` and push, which
redeploys the previous behaviour; Vercel keeps prior deployments. Data files (`jobs.json`) are
regenerated every 6 h and should never be hand-edited to "fix" anything.

## 6. Baseline set today (for later comparison)

- Traffic: 152 all-time pageviews, 14 events, **0 form submissions ever** (GoatCounter, 28 Oct).
- Inventory: 968 listings, 154→? employers, 43.6% senior+, 1.7% worldwide, 25% unclear eligibility.
- Health: 179 tests green, monitor exit 0, 12/12 sampled apply links open.
- Truth layer: spot-check 11/12 correct (the 12th was the pay bug, since fixed).
- Distribution: **zero** kit posts sent, **zero** emails sent — this, not the funnel, is the binding
  constraint on every conversion metric.