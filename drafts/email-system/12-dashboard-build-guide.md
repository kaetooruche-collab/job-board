# 12 · What KT does in the Brevo dashboard (step by step)

Updated 24 Oct 2026 after Claude ran the tests (`14-test-results.md`). Brevo's API has **no endpoints for automations, forms or segments**, so these are the only things left that need your hands. Menu names may differ slightly on your screen: if one doesn't match, tell Claude what you see and the step is adjusted. Nothing here sends email to anyone.

**Decided by KT, 24 Oct:** no domain for now. Emails go out from the one Brevo sender (**Yireh Careers, yirehcareers@gmail.com**, sender id 4). All 12 templates already use it and show "Yireh Careers" as the From name (checked). You accepted the deliverability risk (RK-1, RK-23); the watch-points are in Part G.

## Done already
- Automations #3, #9, #10 deleted (by you). Lists, attributes, 12 templates, tests T1, T5, T6, T7, T9 (Claude).
- **Not deletable through the API** (Claude tried): the 8 automation step templates 54-61, and the sent test campaign 86 ("TEST T7 delete me"). If you can see them in Brevo (Campaigns, and Templates), delete them. If you can't see templates 54-61 anywhere, they are orphans and harmless.

## Part A · One decision first: double opt-in on the signup form
**What the test found (T5):** if someone unsubscribes or is blocklisted and anyone then types their address into the signup form, **the form switches them back on.** That means a stranger, or a bot, can reverse an opt-out. **Double opt-in** (the person must click a confirmation link in an email before anything changes) is Brevo's standard fix and also filters typos and bots. Cost: one extra step for each new subscriber.

**Claude's recommendation: switch double opt-in ON for the signup form.** Your earlier decision (single opt-in, 24 Oct) was made before this test result. Reply "DOI yes" or "single stays" and Claude records it. If you say yes, set it in Part C, form 1. If single stays, the risk is recorded as accepted (RK-27).

## Part B · Segments (10 minutes)
Brevo: **Contacts, Segments, Create a segment**. Build three. In each: give the name, **Add condition**, pick the condition type shown, and **Save**. Conditions are combined with AND.

| Segment name | Conditions |
|---|---|
| `Tips eligible` | Contact is in list **Career tips**; AND contact attribute **CONSENT_TIPS_AT** is not empty; AND email is not blocklisted |
| `Dormant` | Contact is in list **Job alerts**; AND no link clicked in any email in the last **90 days**; AND contact was added more than **90 days** ago |
| `Needs consent audit` | Contact is in list **Career tips**; AND contact attribute **CONSENT_TIPS_AT** is empty |

Segments are for sending and checking only. They are never proof of consent. `Needs consent audit` should always be empty. If you can't find a condition type, tell Claude its name and the step is adapted.

## Part C · Forms (about 1 hour)
Brevo: **Contacts, Forms** (or Marketing, Forms), **Create a form, Subscription form**. For each form: Content (fields), Design (any, it is only used if you share the hosted link; the site draws its own), Settings (list, sign-up process, messages), then **Share** to get the link. **Do not edit templates or forms to add a logo or colours; Claude's site pages do the look.**

**Rules for all three:** no pre-ticked boxes; the tips box is a separate, **unticked** choice that adds the person to **Career tips** only when ticked; keep the honeypot or CAPTCHA option if offered; success message text: "Thanks, you're on the list."

### Form 1 · Signup (edit the one that exists)
The existing form is still named **"RemoteNC Job Alerts Signup"** and is email-only. Edit it (so the site keeps working while you do) and rename it `Yireh Careers: job alerts signup`.
1. **Fields:** Email (required). Add **First name** (optional). Add a drop-down **"I'm looking for"** (optional) with options *Starting out*, *Mid-level*, *Senior and leadership*, saved to the attribute **LEVEL_INTEREST**.
2. **Tips box:** add a block that lets visitors choose a list (a single checkbox), labelled exactly: *Also send me occasional CV and LinkedIn tips, and Yireh Careers service offers. Roughly twice a month at most. You can unsubscribe in any email. This is separate from the weekly job email.* It must add the person to **Career tips**, unticked by default.
3. **Settings:** the main list is **Job alerts**. Sign-up process: **Double opt-in** if you said yes in Part A, with the confirmation email below and "after confirming, redirect to" `https://yirehcareers.vercel.app/subscribed` (the page already exists on the site). Otherwise single opt-in.
4. If you can, set a **hidden/default value** for `CONSENT_JOBS_SRC` = `signup-v1` (this is test T2; tell Claude whether the form allows it).
5. **Share:** copy the form link (it starts `https://…sibforms.com/…`). **Send it to Claude.** Claude reads the form's fields, wires them into the site (the tips checkbox, the level drop-down, real success and error messages are already in place) and updates the privacy page.

**Double opt-in confirmation email (paste into Brevo's confirmation template):**
- Subject: `One tap to confirm`
- Body: *Hi, you asked for the Yireh Careers weekly job email. Tap below to confirm it's you. If you didn't ask, ignore this email and nothing happens.*
- Button: `Yes, send me the weekly job email`

### Form 2 · Free CV check
New subscription form named `Yireh Careers: free CV check`.
1. **Fields:** Email (required), First name (required), and the same unticked **tips box** as above.
2. **Settings:** **no main list** (the check itself must not enrol anyone; if Brevo insists on a list, leave it empty and tell Claude). Sign-up process: single opt-in (they asked for a service, not for marketing).
3. **Notice text on the form or site:** *We'll use your details to review your CV and send you the result. If you don't order anything, we delete your CV within 30 days.*
4. Success message: *Thanks. Now email your CV to yirehcareers@gmail.com and we'll send you three things to fix first.*
5. Share and **send Claude the link**.

### Form 3 · Order intake (private link you send a customer)
New subscription form named `Yireh Careers: order intake`.
1. **Fields:** Email, First name, Package (drop-down: Essential, Professional, Executive), "Roles you're aiming for" (text), and the same unticked **tips box**.
2. **Settings:** no main list; single opt-in. Notice: *We'll use these details to do your order and email you about it. We delete your files within 90 days of finishing.*
3. Share and **send Claude the link**.

**While building, tell Claude:** (T2) can a form set hidden or default values? (T4 later) does the form builder let you add a list-choice checkbox?

## Part D · Automations (about 45 minutes)
Brevo: **Automations, Create an automation**. Two ways: build by hand, or open **the AI builder** and paste the sentence in quotes, then check each step matches the table. Every automation: leave Brevo's default of skipping blocklisted contacts. Template numbers are fixed; **do not edit templates in Brevo's editor** (Claude updates them).

| # | Name | Trigger | Steps |
|---|---|---|---|
| AU-1 | `YC2 AU-1 Job alerts welcome` | Contact added to list **Job alerts** | Send template **74** now. End. |
| AU-2 | `YC2 AU-2 Tips series` | Contact added to list **Career tips** | Send **75**. Wait **7 days**. Send **76**. Wait **9 days**. Send **77**. End. |
| AU-3 | `YC2 AU-3 Free-check follow-up` | Contact added to list **Check result sent** | Wait **4 days**. Condition: contact is in list **Career tips** AND not in list **Order completed**. If yes, send **82**. End. |
| AU-4 | `YC2 AU-4 After the order` | Contact added to list **Order completed** | Wait **21 days**. Condition: in **Career tips**. If yes: if attribute **LAST_PACKAGE** is *essential* send **83**; if *professional* send **84**; if *executive* skip. Wait **39 days**. Condition: in **Career tips**. If yes, send **85**. End. |

AI-builder sentences (paste one at a time):
- AU-1: "When a contact is added to the list Job alerts, send the template YC2 | JA-1 Job alerts welcome, then end."
- AU-2: "When a contact is added to the list Career tips, send template YC2 | CT-1, wait 7 days, send template YC2 | CT-2, wait 9 days, send template YC2 | CT-3, then end."
- AU-3: "When a contact is added to the list Check result sent, wait 4 days, then if the contact is in the list Career tips and not in the list Order completed, send template YC2 | FC-1, then end."
- AU-4: "When a contact is added to the list Order completed, wait 21 days, then if the contact is in the list Career tips and the attribute LAST_PACKAGE is essential send template YC2 | CU-1-ES, or if it is professional send template YC2 | CU-1-PRO. Then wait 39 days and, if the contact is in the list Career tips, send template YC2 | CU-2, then end."

**Leave all four switched OFF** (draft/paused) until Claude has run the tests that need them (T3, T4) with test addresses and tells you they pass. Claude does those tests; you only tell Claude when an automation is saved. If a condition step doesn't exist (T4), tell Claude and the design is changed.

Hand-sent campaigns (no automation): **78** JA-R (quarterly "still want these?"), **79 / 80 / 81** monthly tips, and the weekly digest (Claude generates it and creates the draft campaign; you schedule it).

## Part E · How a customer moves through (so the markers make sense)
1. Free check done: you reply by email, then add the person to list **Check result sent** (only if they ticked tips; the automation checks).
2. Order done: you set `LAST_PACKAGE` and `COMPLETED_ON`, then add them to **Order completed** last. Claude can do these small updates for you through the API when you say "X finished Essential" while the key is active.

## Part F · After you send Claude the form links
Claude wires the three forms into the site, updates the privacy page (new purpose, forms, Brevo link tracking), adds the free-check and order pages, runs the tests that need them (T1 with tips box, T2, T3, T4, T5 again with double opt-in), and tells you when it is safe to switch the automations on.

## Part G · Sending from a Gmail sender: what to watch
You accepted this risk on 24 Oct. The tests show the mail is authenticated as Brevo's own sending domain (DKIM, SPF and DMARC pass) with replies to yirehcareers@gmail.com, so the practical risk is lower than feared, but inbox placement is not guaranteed. Keep to: small consent-only list, short emails, no image-heavy design, complaint and bounce watching in Brevo (Statistics) after every send, and stop and review if complaints reach 0.1% of a send. A domain remains the proper fix when you can afford one.

## What stays blocked until you say go
No email to anyone but you; automations stay off; no form is live on the site until you've sent the links and Claude's wiring is merged; no contact import.
