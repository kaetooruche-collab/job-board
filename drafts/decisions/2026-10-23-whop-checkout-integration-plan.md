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

## 8. Sandbox test results (23 Oct 2026, run by Claude in a headless browser against the sandbox product page)
Environment: `https://sandbox.whop.com/northcyprusremotejobboard/essential-cv-package/` (business "Kaeto Career Services (test)"). Sandbox only; no real money. Product-page URLs, not checkout-link URLs (checkout links with questions are not created yet).

**Verified by running it**
| Test | Result |
|---|---|
| Buyer without a Whop account | Works: guest checkout, email plus card plus billing details, no sign-in. |
| Price shown in checkout | $29.00, "One-time payment." Matches the plan. |
| Success card 4242 4242 4242 4242, full billing details | "Payment complete" page at `sandbox.whop.com/checkout/return/?session=chs_...`; says a receipt is on its way. |
| Decline card 4000 0000 0000 0002 | Clear red message "This payment could not be processed right now. Please try a different payment method, or contact your bank"; buyer stays at checkout; no success page. |
| Incomplete billing details | Blocked with "Please complete the highlighted fields" (address, city, ZIP and state are required for a US billing country). |
| Mobile (390 px) | Checkout opens as a bottom sheet, readable, Apple Pay button, card fields. |
| Close with Escape key | Checkout stays open (no cancel via Escape). Not a bug, but a buyer closes it with the page's own back or close control. |

**Findings that need action before any live launch**
1. The submit button says **"Join"**, not "Pay $29". Misleading for a one-time service. Check the product type, product page and checkout settings in Whop for a button-label or product-type setting; if it cannot be changed, the site copy next to the button must say "You will see a Join button; it completes your $29 payment."
2. The product pages show a **fake compare-at price** ($36.25 struck through, "Save 20%" for Essential; $61.25 for Professional). This is a reference price we never charged. Remove it in the product pricing, because it breaks the site's no-misleading-claims standard.
3. After payment the buyer lands on a Whop page asking for a **6-digit code to create a Whop account** ("to open what you bought"). Our service is delivered by email, so this is confusing. Test a checkout link with a redirect URL to our `/thanks` page, and explain on the checkout description that no Whop account is needed.
4. Checkout also offers **ACH, crypto and WeChat Pay** besides card and Apple Pay. KT decides which to keep; card only is recommended for the first pilot (matches the earlier plan).
5. Pre-checkout questions (target role, have CV yes or no) work only on checkout links, not on product-page checkout; still untested.

**Not run, and why**
- 3-D Secure card (5385 3083 6013 5181): not run.
- Apple Pay: needs a real device; the QR code appeared but was not completed.
- Redirect to our `/thanks` page, direct visit to `/thanks`, and the pre-checkout questions: need the checkout links and the `thanks.html` page (not built yet).
- Receipt email contents and the business name/address buyers see: the receipt goes to the buyer's inbox; only a real test purchase with an inbox KT controls can show it.
- Payout, refund and dispute flow: sandbox has no payouts.
- Webhook tests: not applicable (hosted links, no backend).

## 9. Build and second round of tests (23 Oct 2026; sandbox key supplied by KT as an environment secret)
Built on `claude/optimistic-hopper-nv0qun` (not merged). Files: `site-config.js` (checkout config), `services.html` (pay buttons, copy), `thanks.html` (new, noindex), `vercel.json` (noindex header for /thanks), `privacy.html` (Whop paragraph; needs KT review), `scripts/site_monitor.py` (checkout rule, /thanks checks), `tests/test_checkout_config.py` (11 new tests; 103 tests pass), `CLAUDE.md`, `drafts/whatsapp-messages.md` (message 25), `drafts/whop-go-live-checklist.md`. No new dependencies. No secrets in the repo.

Done through the sandbox API (key scoped to "Kaeto Career Services (test)", read and create only): set the three checkout questions and card-only payment on both plans; changed the button label from "Join" to "Purchase" on both products; created two checkout links with a redirect to the thanks page.

Verified by running it
| Test | Result |
|---|---|
| Checkout shows the 3 questions and card only | Yes (no Apple Pay, ACH, crypto or WeChat Pay). |
| Button label | "Purchase". |
| Full purchase, Essential and Professional (test card 4242) | Payment status `paid` and `succeeded` in the API: $29.00 and $49.00; our order tag (`package: essential` or `professional`) and billing address recorded. |
| Redirect after payment | The buyer is sent to our `/thanks` page with `receipt_id`, `payment_id`, `checkout_status=success` in the URL. |
| Pay buttons on the site | Hidden by default; visible with `?pay=test` plus a TEST banner; WhatsApp demoted to a link; the Professional button opens the sandbox checkout. |
| Mobile (390px) and thanks page | No horizontal scroll; thanks page renders and has `noindex`. |
| Tests | 103 pass, including monitor rule tests with fake responses. |

Observed, not explained: in one of three full runs the checkout stayed on a "Your payment is on its way... Check again" screen although the payment was already `paid` in the API; the other two redirected within 5 seconds. A live buyer who sees this screen can still close it; the receipt email arrives either way. To be watched in the live test.

Not verified
- The three answers (target role, has CV, WhatsApp) are not in the payment, membership or member API objects, and not on the payment page. UPDATE: KT confirmed they ARE shown on the customer profile in the Whop dashboard (Customers, the customer, Custom fields): target role and the CV yes/no were visible for the test purchases. The optional WhatsApp field was left blank in the tests and is untested. The answers are only readable in the dashboard, not through the API this key could reach.
- Receipt email content, buyer-visible business name and address, 3-D Secure, Apple Pay, refunds, disputes and payouts: need KT or live conditions.
- The sandbox product page (not linked from our site) still shows a "$36.25 Save 20%" strike-through that is not in any API field, promo code or plan field; checkout pages show only $29.00. It looks like a Whop product-page display; KT to check the product pricing settings.
- The preview deployment is behind Vercel login, so the redirect target could not be opened by the test browser; the public production domain is not protected (checked only through the earlier live-site monitor).
- GoatCounter: `/thanks` page views are a rough proxy for completed payments only; the page cannot prove a payment. GoatCounter may keep the query string (it contains a payment ID); to be checked in the GoatCounter settings before going live.

## 10. Phone test by KT (23 Oct 2026, iPhone, Türkiye)
- Pay buttons, secondary WhatsApp links and Executive (WhatsApp) looked right on the phone in dark mode. The TEST banner was too low on the page; it is now pinned under the top bar.
- Found: checkout showed **TRY 2,485.38** for the $49 package (about 50.7 TRY per USD) because adaptive pricing was on. Claude first switched it off to match the page wording "All prices are in USD"; KT objected, correctly: copy should follow what is best for the buyer, not the reverse. Per Whop's docs (docs.whop.com/payments-and-billing/fees/adaptive-pricing): free for sellers, processed as domestic (replaces the international card and FX fees), higher bank acceptance, buyers can switch back to the original currency, and the buyer's local price includes a small conversion fee; one-time payments only. DECISION (KT, 23 Oct): keep adaptive pricing ON. Adaptive pricing is back on for both sandbox plans and the page copy now says prices are listed in USD and card checkout may show the buyer's own currency. Not verified: whether the fee shown on a real non-US purchase is actually lower (sandbox test buyer was in the US); rate drift means the local amount changes day to day; vendor statements about conversion and acceptance are Whop's claims, not measured by us.
- Checkout defaulted the billing country to Türkiye, the question fields and the "Purchase" button showed as set up.

## 11. Real purchase from KT's iPhone in Türkiye and the receipt email (23 Oct 2026, 4:10 PM, sandbox)
Verified from KT's screenshots
- The payment completed on iPhone: Professional Package, charged in lira, **TRY 2,485.38** (subtotal and total identical, so no separate fee line shown to the buyer), Visa ending 4242, billing address as typed.
- The buyer gets a Whop "Order Confirmation" email: sender "Kaeto Career Services (test) via Whop", "Business on Whop", invoice number and date, product name, total, billing address, payment method, a "Manage purchase" button and "Need help? contact our support team".
- The seller's own street address is not shown in the email.

Findings
1. The receipt gives no next step (it never says to email the CV and target roles). Claude set a customer-visible plan description with those instructions and the already-approved refund sentence on both plans. It shows in the checkout "Details" panel before payment (verified in a browser). NOT verified: whether it also appears in the receipt email (the email KT received predates the change).
2. "Need help? contact our support team" points to Whop's support, not ours. KT to look for a support-email setting in Whop (Settings) and set it to trueremote.jobs@gmail.com; not yet checked whether the setting exists.
3. The receipt shows the lira amount only, no USD figure. For refunds and bookkeeping KT will see the USD value in the Whop dashboard.
4. Not yet received from KT: where the buyer landed after paying, the Whop fee breakdown for this non-US payment (needed to test Whop's claim that adaptive pricing lowers fees), and whether the optional WhatsApp number appears under Custom fields.
