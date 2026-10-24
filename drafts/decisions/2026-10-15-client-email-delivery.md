# Decision review: client emails and the "check spam / Promotions" reminder

Status: DECIDED by KT (2026-10-15): proceed with Brevo using the Gmail sender. KT tested Brevo and clients receive emails in their inbox. Improving deliverability (custom domain, DKIM/DMARC) is deferred, not rejected. Templates 20-26 created. Revisit when the domain is bought, or if clients report missing emails.

## Question
(1) Where should the "check Promotions and Spam" reminder live? (2) Should the client emails (order, onboarding, delivery, completion) be sent from Brevo templates with sender "True Remote <yirehcareers@gmail.com>"?

## Evidence (read 2026-10-15)
- Brevo, "Comply with Gmail, Yahoo and Microsoft's requirements": sending from a free address (@gmail.com) "will cause your emails to be rejected or filtered to spam". If you send from a free address, "Brevo temporarily replaces your sender address with a compliant one ... a stopgap measure ... not a permanent solution. Recipients may not recognize the replaced address and mark your emails as spam." Brevo replaces free addresses "regardless of the recipients". Example replacement: `name@<number>.t-sender-sib.com` (transactional), `@<number>.brevosend.com` (marketing). https://help.brevo.com/hc/en-us/articles/14925263522578
- Google, "Email sender guidelines": do not impersonate Gmail From headers; Gmail will apply a DMARC quarantine policy to them; the From domain must align with the SPF or DKIM domain. https://support.google.com/mail/answer/81126
- Payhip, "Email Receipts": the seller can set a custom subject and message in the receipt email, same for all products. https://help.payhip.com/article/100-email-receipts
- Brevo showing the sender "True Remote" as active (sender id 3) confirms the mailbox, not deliverability. Not tested: an actual send and where it lands.

## Assessment
- A spam reminder inside an email cannot help when that email is in Spam. The highest-risk email is the first one (TR-01), sent by a new, unknown, rewritten sender. So the reminder must also live where the buyer is before and while they wait.
- The services page alone is read days before the wait begins and is not where a buyer looks when an email is missing. It still helps as an expectation-setter and FAQ.
- The root cause is the free-mail sender, not missing reminders. A reminder is mitigation.

## Options
A. Send client emails from Gmail by hand (copy of the templates as Gmail templates); keep Brevo for the newsletter only. No cost; replies thread naturally; best inbox placement at low volume. Cost: manual work; does not scale.
B. Buy the domain now, authenticate it in Brevo (DKIM/DMARC), use a domain address, then create templates. Best long-term; costs money (domain price quoted earlier: $11.25/yr, mailbox hosting extra and not yet researched) and reverses KT's earlier decision to defer the domain.
C. Brevo with the Gmail sender as it is. Free and automatic, but Brevo will rewrite the sender and Brevo and Google both warn about filtering. Not recommended for emails clients must receive.

## Proposed placement of the reminder (cheap, reversible)
1. Services page: one line in Step 2 and one FAQ ("I haven't received your email").
2. Payhip email receipt custom message (KT sets in Payhip settings; draft wording supplied).
3. KT's first WhatsApp reply after purchase.
4. One line in the emails sent after the first (not the only defence).

## Open items for KT
Expected orders per week; A, B or C; approval of the placement above; approval to commit the drafts.
