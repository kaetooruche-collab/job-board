# Whop checkout integration: Phase 1 inspection and proposed plan (23 Oct 2026)

Status: PROPOSAL. No site files were modified. Implementation waits for KT's answers in section 7.

## 1. What the project actually is (verified by inspection)
- **Static HTML site**, no framework: `index.html`, `services.html`, `verify.html`, `privacy.html`, `site-config.js`, `jobs.json`, `data/`. No `package.json`, no lockfile, no build step.
- **Hosting:** Vercel static (`vercel.json`: `outputDirectory "."`, `cleanUrls true`; `.vercelignore` excludes `research`, `drafts`, `jobsearch`). No `api/` folder, so no serverless functions exist today. Preview deployments already work for branches.
- **Backend, database, authentication:** none on the site. The only server-side code is Python scripts run by GitHub Actions (`scripts/`, `.github/workflows/`) that write `jobs.json` and `data/` and commit them.
- **Existing payment code:** none. Payhip was removed on 17 Oct. The services page says in three places that there is no online checkout.
- **Secrets in the repo:** none (a grep for key/secret/webhook words found only comments and copy). Public IDs only (Brevo form URL, GoatCounter).
- **Where a customer starts a purchase today** (`services.html`, all `wa.me/905338225854?text=...` links): package buttons for Essential (line ~1021), Professional (~1037), Executive (~1054) with "Questions? Chat first" links; add-ons CTA (~1106); LinkedIn Growth CTA (~1113); free CV check (hero, mid-page, final, sticky); founder CTA. `index.html`: services strip and the "Get a CV for this role" job-card button. Tracking: GoatCounter events via `trackClick(...)`.
- **Other things that mention payment and would break or need changing:** `scripts/site_monitor.py` fails if `/services` contains the word "checkout" (apart from "no online checkout"); CLAUDE.md "Not part of this build"; the "How do I pay?" FAQ, step 1 and step 2 of "How it works", the terms; the privacy policy (no payment processor listed); `drafts/whatsapp-messages.md`.

## 2. Is a backend needed? (Phase 2 decision)
Fulfilment is manual: KT delivers CVs and LinkedIn work by email after onboarding. There is no payment-dependent access, no automated delivery, and no order database. So the brief's own rule applies: **use Whop-hosted checkout links.** No server, no webhook endpoint, no API key, no new dependency.
Whop checkout links (dashboard > Checkout links) support: one-time and recurring plans; description; "ask questions before checkout" (can collect target role etc.); redirect after checkout; stock limits; payment methods (card, ACH, PayPal, crypto, financing). https://docs.whop.com/payments/create-checkout-link.md
Reconciliation without webhooks: Whop dashboard payments list and notification emails (enable in Whop settings), matched by the buyer's email and the checkout answers. Acceptable at low volume; it is the main limitation.

**If automation is wanted later** (automatic onboarding emails, order records, refunds tracking), the minimum extra infrastructure is: one Vercel serverless function (for example `api/whop-webhook.js`), the official `@whop/sdk` webhook verification, secrets in Vercel environment variables (API key, webhook signing secret), and persistent storage (a managed database or key-value store) so webhook retries are idempotent and orders can be checked for payment, amount, currency and plan before anything is marked paid. In-memory or file storage on Vercel is not acceptable. Not proposed now.

## 3. Proposed implementation
- **Buttons:** on `services.html`, add a "Pay securely" button to the Essential and Professional cards that opens that package's Whop checkout link; keep "Questions? Chat first" and the free CV check. Executive, add-ons and LinkedIn Growth stay chat-first (see risks 4 and 5).
- **Single source of truth:** checkout URLs live in `site-config.js` (placeholders until KT supplies them) and are copied into static `href`s so the page works without JavaScript; a unit test checks that the hrefs match the config and that no placeholder reaches production.
- **New `thanks.html`** (Whop's "redirect after checkout" target): information only. It never says payment is confirmed and grants nothing. Text: "If you have just paid, here is what to send us" (email your CV and target roles; check Promotions and Spam), with `noindex` (meta plus a `vercel.json` header). Direct visits without payment are harmless by design.
- **Copy changes:** replace "There is no online checkout" lines, step 1/2, "How do I pay?" FAQ (card option via Whop, bank/crypto still by WhatsApp), terms (distance-selling wording: right to withdraw before work begins, consent to start work), and add Whop to the privacy policy as payment processor.
- **Monitor and tests:** update `scripts/site_monitor.py` (drop the blanket "checkout" ban; require that any payment link goes only to `whop.com/checkout/...` URLs listed in the config; keep the forbidden-words list; check `/thanks` is noindex). Add tests for link consistency and placeholders.
- **Files (proposed):** modify `services.html`, `site-config.js`, `privacy.html`, `vercel.json`, `scripts/site_monitor.py`, `CLAUDE.md`, `drafts/whatsapp-messages.md`, `drafts/kt-todo.md`; create `thanks.html`, a link-consistency test in `tests/`, and a go-live checklist in `drafts/`. **Dependencies: none.** **Environment variables: none** for hosted links.

## 4. Whop configuration (what KT does in the dashboard; no IDs are invented)
1. Sandbox first: create an account at https://sandbox.whop.com (separate from production), create the same business/products there. Sandbox supports cards only and has no payouts. https://docs.whop.com/developer/guides/sandbox.md
2. Create one product per service (Essential, Professional) with a one-time USD plan at the published price. Description: what is included, delivery time, "email your CV after payment", and the refund wording.
3. Create a checkout link per plan. Settings per link: ask before checkout (target roles; do you already have a CV; optional WhatsApp number; never ask for a CV file or sensitive IDs), redirect to `https://northcyprusremotejobboard.vercel.app/thanks`, payment methods (card; decide on PayPal and crypto), stock unlimited.
4. Copy each checkout URL (format `https://whop.com/checkout/plan_XXXXXXXX`, a public link) and the plan and product IDs into the site config. Placeholders until then.
5. Settings: notifications for each payment; Checkout branding; Legal (company name and what address buyers see); Tax (see risks).
6. Payout eligibility before launch: Verifications (identity), Balances (payout method and the fee shown at Withdraw), Risk (holds/reserves).

## 5. Testing plan, and what I can and cannot run
- **I can run (headless browser against a branch preview):** each service button opens the correct URL; the price text on the page matches the plan; mobile layout and existing pages unaffected; direct visit to `/thanks` without payment shows no payment claim; missing/placeholder config is rejected by the test; production build (static) and deployment config; the sandbox checkout itself with test card 4242 4242 4242 4242 and the declined card 4000 0000 0000 0002, **if KT supplies the sandbox checkout URLs** (they are public links, no secrets) and the checkout works without a Whop login.
- **Cannot run, and will be reported as not run:** anything needing KT's logins; payout tests (sandbox has no payouts, so the first real payout needs a controlled live test).
- **Not applicable to hosted links, and reported as such:** forged, replayed and duplicate webhooks; wrong order association; missing server-side environment variables; Whop API errors. These apply only if the webhook path in section 2 is built later.
- Cancellation and return navigation: tested in the sandbox checkout (back/cancel) and on `/thanks`.

## 6. Risks (critical first)
1. **Payout and account risk (unverified):** KYC status, payout method and fee, holds and classification have not been seen. Do not launch until a controlled live purchase reaches KT's bank.
2. **Tax:** the Whop account has US sales-tax collection switched on for all states and no UK VAT or EU OSS registration. KT should have an accountant decide what applies to CV services before live prices change.
3. **Business address:** the Whop account holds a full street address in Kyrenia; check whether buyers see it on receipts.
4. **Recurring plan conflicts with published wording:** LinkedIn Growth currently says "nothing is charged automatically". A Whop recurring plan would charge automatically. Keep it chat-first, or change the wording, terms and cancellation process first.
5. **Small add-ons ($10 to $29) lose 6 to 15 percent to the fixed $0.30 plus percentage fees;** keep them chat-first.
6. **Buyer friction unverified:** whether Whop checkout needs a Whop account for the buyer, and what the buyer sees, must be tested in the sandbox before building.
7. **Chargebacks:** $15 each plus loss of funds; keep chat and email records; refund promptly before work starts.
8. **Policy reversal:** this overturns the 15 Oct "no payment on the site" decision (KT said the reason was not having Whop). CLAUDE.md must be updated with the change.
9. **No automated reconciliation** at the start (manual matching in the Whop dashboard).

## 7. Decisions and inputs needed from KT
1. Which services get a "Pay securely" button: recommended Essential and Professional only. Executive ($149), add-ons and LinkedIn Growth stay chat-first.
2. Confirm hosted checkout links with manual fulfilment (no backend, no webhooks) is acceptable for now.
3. Keep "Questions? Chat first" and the free CV check beside the pay button (recommended).
4. Create the sandbox business and products and send the sandbox checkout URLs; then the production URLs after the sandbox tests pass.
5. Tax and address decisions (accountant), and the Whop account checks from `2026-10-19-whop-payments.md`.
