# KT's to-do list (the single master list)

Last updated: 18 October 2026. Claude: when KT asks "what do I need to get done?", show the OPEN items below, most urgent first, in plain language. Update this file every time something is done, added or decided. `drafts/launch-checklist.md` is the older history; this file wins.

Legend: [ ] open, [x] done. "Only KT" means nobody else can do it (logins, accounts, money, approvals).

## 1. Before the first customer messages you (do these first)
- [ ] **Test the live page on your phone.** Open https://northcyprusremotejobboard.vercel.app/services and tap Get started on each package, the free CV check button and Ask about add-ons. Confirm WhatsApp opens with the right message. Also try on an iPhone/Safari if you can (not tested by Claude). Only KT.
- [ ] **Payment accounts ready.** A bank account for each currency you will offer (USD, EUR, GBP, TL), a Bitcoin wallet and a USDT wallet on the Tron (TRC-20) network. Send yourself a small test payment to each. Only KT. (Payment details are never stored in the repo.)
- [ ] **WhatsApp Business setup** on +90 533 822 5854: business profile, greeting message, away message, and quick replies from `drafts/whatsapp-messages.md` (messages 1-24: confirm package, bank details, crypto details, payment received, onboarding, delivery, revision, free CV check 20-21, job-page 22, add-ons 23, LinkedIn Growth 24). Only KT.
- [ ] **Whop: the account you showed is a connected account of 'Chatwait' (23 Oct).** Tell Claude what Chatwait is and whether you own it. If not, create your own stand-alone Whop business (the + next to the account switcher), named Kaeto Career Services or KAYZ Global Ltd, and use that one. Only KT.
- [ ] **Whop card option (research done 19 Oct; Tax page screenshot received, see the update at the end of the decision doc; still needed: Verifications, Payments, Risk, Legal, Checkout and Balances screenshots; confirm the tax setting and the address shown to buyers; `drafts/decisions/2026-10-19-whop-payments.md`).** Check the 6 items in its checklist in your Whop account (KYC, payout method and fee, any holds, business classification, tax mode, account owner) and send Claude the answers or screenshots; then decide whether to pilot Whop as a card link sent in WhatsApp (not on the site). Only KT (needs your login; the Chrome extension was not connected to the cloud session).
- [ ] **Decide the BTC quote validity** (suggestion: 30 minutes) and put it in message 6. Only KT.
- [ ] **Brevo: switch the signup welcome automation to template 33** (the old welcome template 12 and campaigns 17/18 contain claims we do not make). Only KT. Claude can check the account is KAYZ Global before any Brevo action.
- [ ] **Brevo: delete old templates 20-26** (replaced by 27-33). Only KT (Claude cannot delete templates).
- [ ] **Test the newsletter signup with your own email** on the live site and confirm it lands in Brevo list #11. Only KT.
- [ ] **GoatCounter:** log in, open the dashboard, confirm it shows your visit and the click events (names in section 4). Only KT (needs the login).

## 1b. Pharmacy job search
Moved to its own chat and its own list: `jobsearch/TODO.md`. Not tracked here.

## 2. Routines once orders start
- [ ] **Free CV check promise:** one per person, about 10 a week; the client emails the CV (never WhatsApp); reply with the three things to fix first; delete the CV within 30 days if they do not order. Log each one with a delete-by date (`drafts/client-data-handling.md`, `drafts/client-data-log-template.csv`). Only KT.
- [ ] **Delete client files within 90 days** after each service is completed (privacy policy promise).
- [ ] **Time your first two orders** (real hours per package, including messages and revisions). The $149 Executive price assumes about 18 hours; Essential about 3.5 h, Professional about 7 h. Tell Claude the real numbers and the price will be reviewed.
- [ ] **Note buyer countries** (GoatCounter Locations plus who messages you). The price levels were set without this.
- [ ] **Ask every client for a one-sentence testimonial** and permission to publish it. Real quotes only; Claude will add them to the page.
- [ ] **Review Essential $29 and Professional $49 after about 20 orders** (agreed plan).
- [ ] **Post the WhatsApp job message** from `data/whatsapp_post.txt` (refreshed every 6 hours) in your channel/groups, as often as you like. Only KT posts.
- [ ] **Weekly newsletter:** the ready-to-paste Brevo email from the pipeline, if you decide to send one weekly. Only KT sends.

## 3. Decisions waiting for KT
- [ ] **Approve the weekly independent audit** (a scheduled Claude task that opens random listings and compares them with the real postings; `drafts/weekly-audit-prompt.md`). Yes or no.
- [ ] **Newsletter consent:** the signup is one step (single opt-in). Brevo recommends double opt-in for GDPR. You chose one step; confirm it stays, or switch.
- [ ] **Legal check (recommended, not required):** have a qualified adviser read the privacy policy, the refund/cooling-off wording and the free-check terms for the countries you sell to. Claude's reading is not legal advice.
- [ ] **Name and domain:** the placeholder is TrueRemote; the web address still contains a place name (northcyprusremotejobboard.vercel.app), which breaks the "no place names" rule. Decide the name, buy the domain, then Claude switches everything in one change (site name and email live in `site-config.js`). When the domain changes, the old link in WhatsApp groups needs a redirect.
- [ ] **Old Vercel project / old link:** decide whether the old link is redirected to the new site or retired (it is in old WhatsApp posts).
- [ ] **Concierge tier** (application-only, from $499): not built; only if clients ask for a longer programme.
- [ ] **Raise Executive to $199 or add a "two payments" option** only if buyers hesitate or pay without hesitation (see `drafts/decisions/2026-10-18-pricing-and-offer-structure.md`).

## 4. GoatCounter events to watch (after about 2 weeks of traffic)
`services-click-hero-free-check`, `services-click-mid-free-check`, `services-click-sticky-free-check`, `services-click-final-free-check`, `services-click-pricing-essential`, `-professional`, `-executive`, `services-click-addons`, `services-click-growth`, `cv-click-job-cv-button`, `cv-click-home-free-check`, `apply-click`. Visitors x enquiry rate x close rate is the lever; these show the middle number.

## 5. Claude's open items (so you can see what is not on you)
- [ ] Re-run the random spot-check on a fresh sample of listings (last result: 8 of 12 right first time, 2 wrong and fixed, 2 understated) and report the real number.
- [ ] Google job-posting structured data: check Google's current rules for listings we do not own, then tell KT.
- [ ] Brevo template versions that mention the Executive offer (if any are used) need new versions, since templates cannot be edited.
- [ ] Add the first real testimonials to the services page when you have them.
- [ ] **Check Jobicy dates on the public job board.** Two research agents found Jobicy shows old postings as new (Elation 2 Jul, Maven Sept, PointClickCare 9 Jul, H1 31 Jul, Bayesian Nov 2025, all shown as 14-18 Oct). Compare every Jobicy listing with the employer's own date, report the real number, and fix the pipeline (use the employer's date or drop Jobicy listings that cannot be dated). This affects the board's 30-day rule.
- [ ] Keep this file updated.

## 6. Done (for reference)
- [x] Job board live: 1,030 listings, quality checks every 6 hours, live-site monitor every 3 hours (passing).
- [x] Services page rebuilt and live (18 Oct): Essential $29, Professional $49 (Recommended), Executive $149, LinkedIn Growth $99/month, add-ons, free CV check, "Get a CV for this role" button on job cards.
- [x] Privacy policy live, updated 18 Oct (free check, Executive completion, LinkedIn Growth).
- [x] Refund wording approved and published; no on-site payment; WhatsApp-arranged bank/crypto payments.
- [x] Sender trueremote.jobs@gmail.com verified in Brevo; templates 27-33 created.
- [x] Pricing and offer review approved (all five decisions as recommended).
