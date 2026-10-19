# Handoff: job board and Kaeto Career Services (state on 19 Oct 2026)

Use this to continue in any new chat or on a local computer. `CLAUDE.md` (project brief and rules) and `drafts/kt-todo.md` (what KT must do) are the two files to read first; this file is the short "where we are".

## Live now (https://northcyprusremotejobboard.vercel.app)
- Job board: about 1,030 verified remote listings, refreshed every 6 hours by GitHub Actions (`.github/workflows/fetch-jobs.yml`); live-site monitor every 3 hours. Quality layers are described in CLAUDE.md. 92 tests pass.
- Services page (rebuilt and merged 18 Oct): Essential $29, Professional $49 (Recommended), Executive $149 (bounded 30-day scope), LinkedIn Growth $99/month, add-ons, free CV check, "Get a CV for this role" button on job cards. All buttons open WhatsApp (+90 533 822 5854). No payment on the site.
- Privacy policy live; refund wording published; payments are arranged on WhatsApp (bank transfer in USD/EUR/GBP/TL, or BTC/USDT).

## Open decisions and work
1. **Whop card payments (19 Oct):** research and a tax-page screenshot are in `drafts/decisions/2026-10-19-whop-payments.md`. KT asked whether payment should go on the site now that Whop exists. Proposed flow: pay-first on the site for Essential and Professional (onboarding by email after payment, full refund before onboarding is complete); chat-first only for Executive and LinkedIn Growth; free CV check stays the main button; WhatsApp with bank/crypto remains for people Whop cannot serve. Not built. Waiting for KT's answers (see below) and Whop account checks (Verifications, Balances/payout fee, Payments, Risk, Legal, Checkout, top of Tax). Then: a $29 test purchase and a test withdrawal before any site button. Building would change the 15 Oct "no payments on the site" decision, so CLAUDE.md, the privacy policy, services terms and `scripts/site_monitor.py` must be updated with it.
2. **Jobicy dates (Claude's item):** two agents found Jobicy shows old postings as new (Elation Jul/Aug, Maven Sept, PointClickCare 9 Jul, H1 31 Jul, Bayesian Nov 2025, shown as 14-18 Oct). Compare every Jobicy listing with the employer's own date, report the real number, fix the pipeline. Affects the 30-day rule.
3. Google job-posting structured data: check Google's current rules for listings we do not own; tell KT.
4. Testimonials: add the first real client quotes to the services page when KT has them.
5. Weekly independent spot-check of listings: needs KT's approval (`drafts/weekly-audit-prompt.md`). Last results: second check 8 of 12 right first time, 2 wrong (fixed), 2 understated.
6. Decisions pending: newsletter single vs double opt-in; name and domain (the web address contains a place name); old link redirect; legal review of the policies.

## KT's tasks (full list in `drafts/kt-todo.md`)
Phone test of the WhatsApp buttons; payment accounts (bank per currency, BTC, USDT test); WhatsApp Business quick replies (messages 1-24 in `drafts/whatsapp-messages.md`); Brevo (switch welcome automation to template 33, delete old templates 20-26, test signup to list #11); GoatCounter check.

## Not here
The pharmacy job search is a separate project in `jobsearch/` with its own chat and files (`jobsearch/CLAUDE.md`, `HANDOFF.md`).

## Practical notes for a new session
- Branch work: the cloud session worked on `claude/optimistic-hopper-nv0qun`; PRs 3-12 were merged to `main`. Anything after PR 12 (kt-todo, handoffs, pharmacy folder, Whop notes) is on that branch until merged.
- Do not use `pkill -f` with patterns matching your own command (it kills the shell); long waits belong in background commands.
- Brevo rule: before any Brevo action call `accounts_get_account` and confirm `KAYZ Global Ltd`.
- KT is a marketing professional: plain language, one step at a time, ask only for logins, approvals and decisions.
