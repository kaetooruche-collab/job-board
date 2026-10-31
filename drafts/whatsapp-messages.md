# WhatsApp message library (Yireh Careers)

How to use: every stage of an order is handled on WhatsApp, with documents only by email. Save these in the **WhatsApp Business app** (already linked to +90 533 822 5854) as quick replies (type "/" and the shortcut), and as the greeting and away messages. The ready-to-paste version, in app-menu order with the profile text, is `drafts/whatsapp-business-setup.md` (built from this file by `drafts/build_whatsapp_setup.py`).

Voice: short, warm, plain, one next step per message. Rules and the research behind them are in `drafts/voice-and-copy-guide.md`. Rewritten 24 Oct 2026 after KT's feedback that the first versions were too stiff.

Conventions: `[Square brackets]` = fill in. `*bold*` is WhatsApp bold. Prices, timings and terms match the services page; do not change them in a chat without updating the page first. Messages that say "I" are fine in a 1:1 chat; emails say "we".

---
## 0. Profile (set once)
See `drafts/whatsapp-business-setup.md` (name, category, about, description, email, links, picture).

## 1. Pre-filled message (already on the website buttons)
> Hello, I would like to order the *Essential* package ($29). Could you please confirm the next steps?

(The same wording is used for Professional ($49) and Executive ($149). The free CV check and job-page buttons open messages of their own: see messages 20 and 22.)

## 2. Greeting (automatic, first message from a new contact)
> Hi, thanks for messaging Yireh Careers.
> What can we help with? A free quick CV check, or one of our packages (Essential $29, Professional $49, Executive $149)? Tell us a little about the roles you're going for and we'll reply as soon as we can.
> Want the free CV check? The quickest way is this form: https://yirehcareers.vercel.app/free-check

## 3. Away message (automatic, outside your hours)
> Thanks for your message. We're away at the moment, but we'll reply as soon as we're back. [We usually reply within X hours on weekdays.]
> In the meantime, you can see what's in each package here: [services page link]

## 4. Confirm the package and ask how they'd like to pay
Shortcut `/package`
> Hi [First name], great choice. The *[Package]* package is $[price].
>
> *What you get:* [see inclusions below]
> *When:* [timing], counted from when we have everything we need from you.
>
> How would you like to pay: bank transfer (USD, EUR, GBP or TL) or cryptocurrency? Tell me and I'll send the details.
>
> While you decide, this short form tells us where to send your documents: https://yirehcareers.vercel.app/order?package=[essential / professional / executive]

Inclusions to paste:
- Essential: a professionally written or rewritten CV, tailored to your industry and target roles; ATS-friendly structure and role-relevant keywords; Word and PDF; up to 2 revision rounds. Timing: within 2 working days.
- Professional: everything in Essential, plus a targeted cover letter and LinkedIn profile setup; up to 3 revision rounds. Timing: within 3 working days.
- Executive: everything in Professional, plus a personal branding strategy, 12 LinkedIn posts written and published over 30 days, and targeted connection building by hand each week of the 30-day service, within LinkedIn's limits, aiming to move you towards 500+ total connections (or 100 new relevant connections if you already have 500+). Timing: CV and cover letter within 2 working days; LinkedIn profile setup within 3 working days; the 30-day service period starts when onboarding is complete.

## 5. Payment details: bank transfer
Shortcut `/bank`
> Thanks, [First name]. Here are the details for your *[Package]* package:
>
> *Amount:* [amount and currency]
> *Account name:* [account holder name]
> *Bank:* [bank name]
> *IBAN / account number:* [number]
> *SWIFT / BIC:* [code]
> *Reference:* [reference, for example TR-1042]
>
> If you're paying in a currency other than USD, the amount depends on the exchange rate on the day, so I'll confirm the exact figure here before you send anything.
>
> Please add the reference to your transfer, and cover any bank fees on your side so the full amount reaches us. When it's sent, a screenshot of the receipt helps me spot it quickly.
>
> One safety note: we only ever send payment details from this number. If anyone else sends you different details, please don't pay them.

## 6. Payment details: cryptocurrency
Shortcut `/crypto`
> Thanks, [First name]. Here are the details for paying with crypto. I take Bitcoin (BTC) on the Bitcoin network and USDT on the Tron (TRC-20) network.
>
> *Amount:* [amount] [BTC or USDT]
> *Network:* [Bitcoin network for BTC / Tron (TRC-20) for USDT]
> *Wallet address:* [address]
>
> The amount depends on the exchange rate at the time you pay, so I'll confirm the exact figure here before you send. Please cover any network or exchange fees on your side so the full amount arrives.
>
> Please double-check the network. A transfer on the wrong one can be lost for good, and we can't recover or refund it. Copying the address (rather than typing it) and sending a small test first is a good idea.
>
> Once it's sent, share the transaction ID or a screenshot here.

## 7. Payment received: what happens next
Shortcut `/received`
> Payment received, thank you [First name]. Your order is confirmed.
>
> *Next step:* I've emailed you from yirehcareers@gmail.com. Just reply to that email with your CV and anything else you'd like us to see. We take documents by email only, so they stay private and in one place.
> Can't see the email? Check Promotions and Spam.
>
> Your delivery time starts once we have everything we need. By sending your documents, you're asking us to start work straight away.

## 8. Payment not yet received (gentle follow-up, after 24 hours)
Shortcut `/awaiting`
> Hi [First name], I haven't seen the payment for your *[Package]* package yet. Transfers can take a little while. If you've already sent it, a screenshot of the receipt will help me find it. And if you have any questions about paying, just ask.

## 9. Email not received
Shortcut `/spam`
> No problem. Please check Promotions and Spam, and search for "Yireh Careers". If it's there, move it to your main inbox. If not, tell me which email address to use and I'll resend it.

## 10. Documents sent on WhatsApp by mistake
Shortcut `/docs`
> Thanks, [First name]. To keep your documents private and in one place, we only take them by email. Could you send it to yirehcareers@gmail.com? Once it arrives, I'll delete it from this chat.

## 11. Onboarding reminder (if nothing received after 3 days)
Shortcut `/onboard`
> Hi [First name], just a gentle nudge: I'm ready to start your *[Package]* as soon as I have your CV and answers. Your delivery time only starts once I have them, so there's no rush.

## 12. Onboarding complete: your timeline starts
Shortcut `/started`
> Thanks, [First name]. We have what we need and we've started on your *[Package]*.
>
> *Started:* [date]
> *Expected delivery:* [date] (working days)
>
> We'll email your documents when they're ready. If we need to check anything first, we'll ask.

## 13. Delivery notice
Shortcut `/delivered`
> Hi [First name], your documents are in your inbox (from yirehcareers@gmail.com; check Promotions or Spam if you can't see them).
>
> Take your time reading them and check that every date, job title and name is right. You have [2 or 3] rounds of changes: send everything together in one email reply and that counts as one round.

## 14. Revision acknowledged
Shortcut `/revision`
> Thanks, [First name], I've got your changes. The updated version will be in your inbox by [date]. That was round [1 / 2 / 3] of [2 / 3].

## 15. Executive: branding strategy ready for approval
Shortcut `/branding`
> Hi [First name], your personal branding plan is in your inbox for review. Please check that every detail about your experience and qualifications is right, since it goes out under your name. We won't publish anything or send any connection requests until you approve it by email.

## 16. Executive: progress update (day 30)
Shortcut `/progress`
> Hi [First name], here's your update. Your 30 days [ends / ended] on [date].
> *Connections:* [number] now, up from [starting number]. Our aim was to move you towards 500+ total [or: 100 new relevant ones].
> *Posts published:* [number] of 12.
> [If they want to keep going:] LinkedIn Growth carries on the same work for $99 a month: 12 posts and weekly targeted connection requests, month to month. You pay each month here on WhatsApp, nothing is automatic, and you can stop before any month starts. Would you like me to continue?

## 17. Order complete and information deletion
Shortcut `/complete`
> All done, [First name]. Thank you for trusting us with your career documents.
>
> Please keep your own copies of the final files. We'll delete your documents and details from our email, devices and WhatsApp within 90 days. If you'd like that sooner, or a copy of what we hold, just ask.
>
> Good luck with your search. One tip: check each employer's rules for your country before you apply.

## 18. Cancellation or refund request: first reply
Shortcut `/refund`
> Thanks for telling me, [First name], and I'm sorry it hasn't worked out. Here's how it works: if we haven't started yet (before onboarding is complete), you can have a full refund. If work has started, a refund depends on how much has been done and what you've already received.
> Tell me what happened and where we are, and I'll come back with your options.

## 19. Request about personal information
Shortcut `/privacy`
> Thanks, [First name]. I've got your request about your personal information and I'll reply within one month, free of charge. I may ask you to confirm it's you, but I'll only ask for what's needed.

## 20. Free quick CV check: first reply
Shortcut `/check`
(Opens from the "Get a free CV check" buttons and the bio links. The button text is: "Hello, I would like a free quick CV check. Please tell me how to send my CV.")
> Hi [First name], thanks for asking. The quickest way is our short form: https://yirehcareers.vercel.app/free-check
> Then email your CV to yirehcareers@gmail.com (not here on WhatsApp) and tell me the roles you're going for. I'll reply with the three things I'd fix first, within 2 working days.
> It's one free check per person. I only use your CV for the check, and I delete it within 30 days if you don't order.

## 20b. Free CV check: we're full this week
Shortcut `/full`
> Hi [First name], thanks for your patience. We review about 10 CVs a week and this week's spots are taken. If you'd still like a check, send the form again next week: https://yirehcareers.vercel.app/free-check
> In the meantime, the job board is open to everyone: https://yirehcareers.vercel.app

## 20c. Free CV check: form done, CV not received
Shortcut `/nocv`
> Hi [First name], I got your form, thank you. I haven't seen your CV yet. Could you email it to yirehcareers@gmail.com? Once it's there, I'll reply within 2 working days.

## 21. Free CV check: result and next step
Shortcut `/checked`
> Hi [First name], I've emailed you the three things I'd fix first. If you'd like us to do the full job, *[Essential $29 / Professional $49]* looks like the right fit for what you've described. We can add a cover letter or LinkedIn setup to Essential too. Shall I get you started?

## 22. Job-page button: first reply
Shortcut `/role`
(Opens from "Get a CV for this role" on a job card. The button text is: "Hello, I would like a CV for this role: [title] at [company]. Could you tell me which package to choose?")
> Hi [First name], thanks for getting in touch. Where are you in your search (and, if you're happy to say, which country are you in)?
> If you already have a CV, the quickest start is the free check: email it to yirehcareers@gmail.com and I'll tell you the three things I'd fix first. For a full package, *Essential ($29)* is a professionally written CV, delivered within 2 working days, and *Professional ($49)* adds a cover letter and LinkedIn setup, delivered within 3.
> One tip: check the employer's rules for your location before you apply.

## 23. Add-ons menu
Shortcut `/addons`
> Here's what we can add to an order (USD):
> Cover letter for an Essential order: $15
> LinkedIn profile setup for an Essential order: $25
> Extra revision round: $10
> Second CV for another target role: $15
> Priority delivery (your documents within 1 working day instead of 2 or 3): $15
> Interview preparation sheet: $29 (likely questions and answer outlines for one target role, built from your CV)
> Which would you like? I'll confirm the total before you pay.

## 24. LinkedIn Growth (monthly) offer and monthly reminder
Shortcut `/growth`
> LinkedIn Growth is $99 a month: 12 curated posts written and published for you, plus targeted connection requests sent by hand each week, within LinkedIn's limits. It's month to month. You pay each month here on WhatsApp, nothing is charged automatically, and you can stop before any month starts. Shall I start it from [date]?

## 24b. LinkedIn Growth: monthly reminder
Shortcut `/growth2`
> Hi [First name], your LinkedIn Growth month ends on [date]. Would you like to continue for another month ($99), or stop here?

## Decisions (updated 17 October 2026)
Decided by KT:
1. **Fees:** the client pays all bank, network and conversion fees. This is now on the services page FAQ and in messages 5 and 6.
2. **Exchange rate:** the rate on the day and time of payment. Messages 5 and 6 say the exact amount is confirmed in the chat before sending.
3. **Crypto:** Bitcoin (BTC) and USDT.

Still open:
- ~~USDT network~~ decided 17 Oct: Tron (TRC-20) for USDT, Bitcoin network for BTC (wallet addresses are kept out of the repository; paste them into the `/crypto` quick reply).
- **How long a quoted BTC amount stays valid.** Suggestion: 30 minutes, because Bitcoin's price moves.
- **Account details:** the account holder name must match the name clients see, and details should be sent from this number only (and optionally also by email, so clients can cross-check).
- **Receipts:** a short receipt or invoice by email once payment is confirmed.
- **Refunds:** wording approved by KT on 17 Oct and published on the services page. The cooling-off line is in message 7.


## Update 18 October 2026
KT approved the pricing review: Executive is $149 with a 30-day service (12 posts, weekly targeted connection building, no open-ended promise); LinkedIn Growth $99 a month; add-ons; free quick CV check; "Get a CV for this role" button. Messages 1, 2, 4 and 16 were updated and messages 20-24 added. Set up quick replies for 20-24 as well.


## Update 23 October 2026: card payment option (Essential and Professional only)
Not live until KT approves the go-live checklist (`drafts/whop-go-live-checklist.md`). Replace [LIVE LINK] with the live Whop checkout link from `site-config.js` for that package.

### 25. Card payment link (send only if the customer chooses card, Essential or Professional)
Shortcut `/card`
> Here's your secure card payment link for the *[Package]* package ([price]): [LIVE LINK]
>
> You'll see three quick questions first: your target role, whether you already have a CV, and an optional WhatsApp number. Our payment provider handles your card details, so we never see them.
>
> After you've paid, email your current CV and target roles to yirehcareers@gmail.com (not here on WhatsApp) and we'll take it from there.
>
> One safety note: the only card link we use is the one on our website or the one sent from this number.

## Update 24 Oct 2026: brand is now Yireh Careers
Replaces "True Remote" and "Kaeto Career Services" everywhere in this library. Messages that say "I" are fine in a 1:1 chat. The email address is now yirehcareers@gmail.com (created 24 Oct); set its Gmail display name to "Yireh Careers". The WhatsApp Business display name change may need approval from WhatsApp.

## Update 24 Oct 2026 (b): forms, weekly post and stop requests
The site now has a free-check form (`/free-check`) and a private order form (`/order`). Both post to the same small function as the signup box. Each sends a notice to yirehcareers@gmail.com, so you do not need to copy details by hand. Brevo sends nothing about the free check or an order until you add the person to a list yourself.

### 26. Order form link (when someone has agreed a package)
Shortcut `/orderform`
> Great, [First name]. To get started, please fill in this short form so we have the right email and package on file: https://yirehcareers.vercel.app/order?package=[essential / professional / executive]
> Then email your CV and answers to yirehcareers@gmail.com. Your delivery time starts once we have everything.

### 27. Weekly job email: how to get it
Shortcut `/weekly`
> Our weekly job email goes out on Tuesday mornings: a short list of recent remote jobs with a link to each employer's own posting. You can sign up with just your email at https://yirehcareers.vercel.app/#subscribe and unsubscribe with one tap whenever you like.

### 28. Someone asks us to stop emailing or messaging them
Shortcut `/stop`
> Of course, [First name]. I've noted it and we won't contact you again. Emails stop within 2 days. If you only want to stop the CV tips and keep the weekly job email, just say "jobs only" and I'll do that instead.
(After you send this: in Brevo, open the contact and blocklist them for all emails, or for "jobs only" remove them from the Career tips list. Then add a line to your do-not-contact note.)

## WhatsApp rules (KT and Claude, 24 Oct 2026)
1. **Never message first with an offer.** Reply to people who message you. Do not send promotions to numbers you collected another way. WhatsApp's own policy for business accounts is not something I could verify here, so keep it simple.
2. **Do not ask for email consent in WhatsApp.** The signup box on the website, and the unticked tips box on the forms, are where consent is recorded. A "yes" in a chat is not recorded anywhere.
3. **No documents on WhatsApp.** The free check and orders use email only (messages 10 and 20).
4. **The weekly channel post** is written by `scripts/make_outputs.py` into `data/whatsapp_post.txt` (and by the post kit at `/kit`). Post it on Tuesday after the weekly email goes out, once you have opened two of its links to check they work. If it says there are not enough fresh listings, skip the week; do not pad it.
5. **Stop requests:** reply with `/stop`, then blocklist in Brevo within 2 days.
6. **Student or graduate:** the free check no longer asks. If someone volunteers it, fine; do not claim a role suits a background.
