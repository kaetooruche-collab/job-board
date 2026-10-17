# Launch checklist (17 October 2026)

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

## B. Things only KT can do
- [ ] GoatCounter: open the live site, then confirm the dashboard shows the visit.
- [ ] Brevo: switch the sign-up/welcome automation to template 33 (the old welcome id 12 and campaigns 17/18 contain claims we do not make).
- [ ] Brevo: delete the old templates 20-26 (replaced by 27-33).
- [ ] Brevo: test sign-up on the live site with your own email; confirm it lands in list #11.
- [ ] WhatsApp Business app: profile, greeting, away message, quick replies from `drafts/whatsapp-messages.md`.
- [ ] Payment accounts ready: a bank account per currency you will offer, a BTC wallet and a USDT wallet (choose the USDT network).
- [ ] Post `data/whatsapp_post.txt` from the latest run in your channel.

## C. Decisions waiting for KT (nothing below is published)
- [ ] Refund wording: `drafts/decisions/2026-10-17-refunds-and-500-offer.md`
- [ ] Executive offer for clients already at 500+ connections (recommendation: 100 new relevant connections).
- [ ] Whether to cap the open-ended "until 500+" promise.
- [ ] USDT network, BTC quote validity time.
