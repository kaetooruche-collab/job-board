# Yireh Careers: Brevo build and automations

Built 24 Oct 2026 (rebuild, replaces `drafts/brevo-setup-guide.md`). Account checked first: KAYZ Global Ltd (label only), Free plan, Marketing Automation enabled, sender "Yireh Careers" (id 4).

## The one rule that keeps this simple
**Being on a list = the person said yes to that kind of email.** KT only adds someone to a list after a recorded yes. Why this matters: the operator is in Cyprus, where marketing email to individuals needs prior consent, and the Cyprus Commissioner's April 2024 notice says an email that only asks for marketing consent is itself against the law (secondary sources, Harris Kyriakides and Chambers; not legal advice, a lawyer should confirm). So we never email people to "please opt in". Consent is collected at the moment they hand over their details.

| List | Who is on it | How they get there | What they receive |
|---|---|---|---|
| 11 Job alert subscribers | Signed up on the site for the weekly jobs email | Website form (single opt-in) | Welcome A1, A2, weekly digest, S1. **No promotion.** |
| NEW "CV tips: opted in" | Ticked the second box on the form, or said yes on WhatsApp | Form checkbox (see Step 1) | M1, M2, monthly tip |
| 12 Free CV check requested (rename: "Free CV check: follow-up OK") | Had a free check AND said yes to a follow-up | KT adds on the day the result is sent | F1, F2 |
| 13 / 14 / 15 Customers: Essential / Professional / Executive | Customer who said yes to follow-up notes at order completion | KT adds at completion (Executive: when onboarding is complete) | U1 / U2 / U3, then R1 |
| 16 LinkedIn Growth: active | Paying monthly | KT adds by hand | Nothing automatic. Used to stop upsells. |
| 17 Do not send | Asked us to stop, complained, bounced, or went quiet | KT / sunset automation | Excluded from every campaign and every automation |

Order, delivery and "how's your CV" emails are not marketing. They go from yirehcareers@gmail.com using the Gmail templates (`drafts/gmail-customer-emails.md`), not Brevo.

## Templates now in Brevo (all active, sender Yireh Careers, nothing sends until an automation uses them)
| ID | Name | Subject |
|---|---|---|
| 63 | YC \| A1 Job alerts: welcome | You're in. Here's your first move |
| 64 | YC \| A2 Job alerts: check before you apply | The 30-second check that saves hours |
| 65 | YC \| M1 CV tips: free CV check offer | Applying and hearing nothing? |
| 66 | YC \| M2 CV tips: one fix tonight | One CV fix you can make tonight |
| 67 | YC \| F1 Free check: follow-up day 3 | Did the three fixes help? |
| 68 | YC \| F2 Free check: follow-up day 8 | Still thinking it over? |
| 69 | YC \| U1 Customer: Essential add-ons day 21 | Want a cover letter and LinkedIn to match? |
| 70 | YC \| U2 Customer: Professional LinkedIn Growth day 21 | Keep your LinkedIn working while you search |
| 71 | YC \| U3 Customer: Executive keep going day 30 | Want to keep the momentum going? |
| 72 | YC \| R1 Customer: two months on | How's the search going? |
| 73 | YC \| S1 Job alerts: still want these? | Still want these job emails? |

Each footer says why they are getting it, has the address and a one-click unsubscribe. Source files: `drafts/emails/brevo-set/` (copy: `drafts/email-copy-review.md`). Tests of 63 and 70 were sent to kaetooruche@gmail.com.

## Step 1: lists and form (KT, about 10 minutes; Brevo's connection cannot create these)
1. Create list **CV tips: opted in**.
2. Rename list 12 to **Free CV check: follow-up OK**.
3. Edit the sign-up form: keep the email box and the line about the weekly job email. Add a second **unticked** checkbox: "Also send me CV tips and occasional offers." Make it add the contact to **CV tips: opted in** (in addition to list 11).
4. Delete old items: campaign 19 (old claims, old sender) and template 61 (leftover automation step). Keep campaign 53 (sample digest) until the first real digest is sent. Do not touch the Hibarr templates (hundreds, other project).

## Step 2: seven automations (Brevo > Automations > Create)
Every automation: **exit if the contact is on list 17 Do not send**. Use the AI builder with the sentence in quotes, then check the steps match.

1. **YC | Job alerts welcome**. Trigger: contact added to list 11. Send 63 now. Wait 3 days. Send 64. End.
   "When a contact is added to list 11, send template 63, wait 3 days, send template 64."
2. **YC | CV tips**. Trigger: added to CV tips: opted in. Send 65 now. Wait 7 days. Send 66. End. (Afterwards one tip a month by campaign.)
3. **YC | Free check follow-up**. Trigger: added to list 12. Wait 3 days. If the contact is on list 13, 14 or 15, exit. Send 67. Wait 5 days. Same exit check. Send 68. End.
4. **YC | Essential customer**. Trigger: added to list 13. Wait 21 days. Send 69. Wait 39 days. Send 72. End.
5. **YC | Professional customer**. Trigger: added to list 14. Wait 21 days. If on list 16, skip to the last step. Send 70. Wait 39 days. Send 72. End.
6. **YC | Executive customer**. Trigger: added to list 15 (on the day onboarding is complete, since the 30 days start then). Wait 30 days. If on list 16, skip. Send 71. Wait 30 days. Send 72. End.
7. **YC | Job alerts sunset**. Trigger: matches custom filters: on list 11, added more than 60 days ago, no link clicked in 60 days. Send 73. Wait 14 days. If still no click, add to list 17 and remove from list 11. End.

Weekly digest stays a campaign, not an automation: KT says "weekly email", Claude runs `python3 scripts/make_digest.py`, creates a draft to list 11 (exclude 17), KT schedules it. No promotion inside it.

## Checks before turning each automation on
- Add KT's own address (kaetooruche@gmail.com) to the trigger list and confirm the first email arrives, then remove it.
- The first three automations are the only ones with real subscribers behind them. Leave 4 to 6 until the first customer says yes to follow-up notes.
- Free plan: 300 emails a day (test sends count). Contacts into automations are capped at 2,000 on Free per secondary sources; Brevo's own page did not confirm the counting window.

## Honest limits (read these)
- **No domain yet.** Brevo cannot authenticate a Gmail sender, so mail goes out through Brevo's own sending identity with Gmail as reply-to. Google's sender guidelines (support.google.com/a/answer/81126) say all senders need SPF or DKIM, TLS and a spam rate under 0.3%; the stricter bulk rules start at 5,000 a day, which we are nowhere near. Fine for a few dozen people. Buy a domain and authenticate it before the list reaches about 100 or before real promotion.
- **Consent record.** Brevo should not be the only proof. In the enquiry log add three columns: marketing OK (yes/no), date, how they said it (form box, WhatsApp message, reply).
- **Not legal advice.** Cyprus, UK and US rules were read from official pages and law-firm summaries, not reviewed by a lawyer. Get terms and the consent wording checked before the company is registered.
- **Website:** `handleSignup()` in `index.html` shows "You're in!" even when the sign-up fails. Fix it before sending traffic. The "We cannot promise..." copy on the services page is still the open copy problem.
- **Evidence:** this build rests on the voice guide, not on proven results. Judge it by replies and clicks after real use, not opens.
