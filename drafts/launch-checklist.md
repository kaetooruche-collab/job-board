# Launch checklist (17 October 2026)

> Superseded by `drafts/kt-todo.md` (the single master list). Kept as history.

Owner: C = Claude, K = KT. Status is what was verified, not what was hoped.

## A. Site and pipeline (Claude)
- [x] Services page, WhatsApp-only ordering, email-based documents: merged to main and live (live page fetched and checked).
- [x] Privacy policy live at /privacy (entity KAYZ Global Ltd, one contact email, AI-tool disclosure, bank/crypto payments); footer links on all pages; consent line under the newsletter form. Live page fetched and read.
- [x] Single contact email everywhere: trueremote.jobs@gmail.com (no old address left in served files).
- [x] Payment terms on the services page: client pays all fees; exchange rate at the time of payment (exact amount confirmed in chat); Bitcoin and USDT.
- [x] Tests: 67 pass. Pages load with no console errors at 1280px and 360px dark (local server).
- [x] Classifier fixes found in launch QA: false "cannot hire in: United States" (47 listings); senior/lead/manager titles shown as junior (11 listings). Both have regression tests.
- [x] WhatsApp post generator added; first pipeline run after the first fix succeeded (run 21).
- [ ] Pipeline run after the second fix (started after merge of PR 7): confirm success.
- [x] Brevo v2 templates created in the KAYZ Global account after checking the connected account (ids 27-33).
- [ ] GoatCounter counting: script is on every live page; counting not verifiable from here.

## A2. Quality system (added 17 Oct, night)
- [x] Independent per-listing checks (`scripts/qa_checks.py`) run in every refresh; failing listings are held back and logged; sudden drops stop the run and keep the previous data.
- [x] Live-site monitor (`scripts/site_monitor.py`, every 3 hours): passed on the live site; proven to fail on a deliberately broken copy.
- [x] First random spot-check of 10 listings against their real postings: only about 2 of 10 fully matched (pay shown as "not stated" when the posting states pay in 6 of 10; wrong "who can apply" label in 2; one borderline level). Fixed and re-tested; a re-check after the fixes is pending.
- [ ] Weekly independent audit by a scheduled Claude task: drafted in `drafts/weekly-audit-prompt.md`, needs KT's approval to schedule.

## B. Things only KT can do
- [ ] GoatCounter: open the live site, then confirm the dashboard shows the visit.
- [ ] Brevo: switch the sign-up/welcome automation to template 33 (the old welcome id 12 and campaigns 17/18 contain claims we do not make).
- [ ] Brevo: delete the old templates 20-26 (replaced by 27-33).
- [ ] Brevo: test sign-up on the live site with your own email; confirm it lands in list #11.
- [ ] WhatsApp Business is already linked to +90 533 822 5854. Remaining: greeting, away message and quick replies from `drafts/whatsapp-messages.md`.
- [ ] Payment accounts ready: a bank account per currency you will offer, a BTC wallet and a USDT wallet (choose the USDT network).
- [ ] Post `data/whatsapp_post.txt` from the latest run in your channel.

## C. Decisions waiting for KT (nothing below is published)
- [x] Refund wording: approved by KT and published (services page FAQ and terms).
- [x] Executive offer for clients already at 500+ connections: 100 new relevant connections (approved 18 Oct, on the page).
- [x] Open-ended "until 500+" promise: removed; day-30 continuation is the paid LinkedIn Growth plan, $99 a month (approved 18 Oct).
- [ ] BTC quote validity time (suggestion: 30 minutes). USDT network decided: Tron (TRC-20).

## D. After the 18 Oct pricing change (KT)
- [ ] Add WhatsApp Business quick replies 20-24 from `drafts/whatsapp-messages.md` (free check, add-ons, LinkedIn Growth).
- [ ] Be ready to answer the free CV check: one per person, about 10 a week, delete the CV within 30 days if no order.
- [ ] Time your first two orders (hours per package) and note buyer countries; review Essential/Professional prices after about 20 orders.
- [ ] Ask each client for a one-sentence testimonial and permission to publish it.
- [ ] GoatCounter events to watch: `services-click-hero-free-check`, `services-click-mid-free-check`, `services-click-sticky-free-check`, `services-click-pricing-*`, `services-click-addons`, `services-click-growth`, `cv-click-job-cv-button`, `cv-click-home-free-check`.
