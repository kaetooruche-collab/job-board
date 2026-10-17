# Launch checklist (17 October 2026)

Owner: C = Claude, K = KT. Status is what was verified, not what was hoped.

## A. Site and pipeline (Claude)
- [x] Services page, WhatsApp-only ordering, email-based documents merged to main (PR 3) and deployed to production (Vercel deployment for commit 16ef673 READY; live page fetched and checked).
- [x] 57 -> 63 tests pass; pages load with no console errors at 1280px and 360px dark (local server).
- [x] Classifier bug fixed (false "cannot hire in: United States" on 47 listings) with regression tests (PR 4).
- [x] WhatsApp post generator added; runs in the 6-hourly workflow.
- [ ] Manual pipeline run after the fix: confirm success and that `data/whatsapp_post.txt` is committed.
- [ ] Privacy page published and linked in the footers (needs the answers in section C).

## B. Things only KT can do
- [ ] WhatsApp Business app: profile, greeting, away message, quick replies from `drafts/whatsapp-messages.md` (about 20 minutes).
- [ ] Brevo: switch the sign-up/welcome automation to template 33 (old welcome id 12 and campaigns 17/18 contain claims we do not make).
- [ ] Brevo: test sign-up on the live site with your own email; confirm it lands in list #11.
- [ ] GoatCounter: open the live site, then check the dashboard shows the visit.
- [ ] Payment details ready for at least one currency (and the decisions in `drafts/whatsapp-messages.md`, last section).
- [ ] Delete the old Brevo templates 20-26 (the corrected set is 27-33). In the welcome automation use 33.

## C. Answers needed for the privacy page and templates
1. Entity shown: KAYZ Global Ltd (default). Right?
2. Location shown: "Kyrenia, Northern Cyprus" (town only) in client emails and privacy page. Right? Full postal address only in the newsletter?
3. Privacy contact email: trueremote@gmail.com (the site's) or trueremote.jobs@gmail.com (the one on client emails)? Both are monitored?
4. Do you use any AI tool on client documents? (The policy must say so if yes.)
5. Is two-step sign-in on for the Gmail account?
6. Sign-up emails: keep the current single step, or turn on a confirmation email (recommended by Brevo)?

## D. Announce (after A and B)
- [ ] Post `data/whatsapp_post.txt` (fresh from the latest run) in your channel/groups.
- [ ] Pin a short message with the services page link and your payment-safety line.
