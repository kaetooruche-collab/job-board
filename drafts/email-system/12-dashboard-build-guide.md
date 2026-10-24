# 12 · What KT does in the Brevo dashboard (step by step)

Updated 24 Oct 2026 after Claude ran the tests (`14-test-results.md`). Brevo's API has **no endpoints for automations, forms or segments**, so these are the only things left that need your hands. Menu names may differ slightly on your screen: if one doesn't match, tell Claude what you see and the step is adjusted. Nothing here sends email to anyone.

**Decided by KT, 24 Oct:** no domain for now. Emails go out from the one Brevo sender (**Yireh Careers, yirehcareers@gmail.com**, sender id 4). All 12 templates already use it and show "Yireh Careers" as the From name (checked). You accepted the deliverability risk (RK-1, RK-23); the watch-points are in Part G.

## Done already
- Automations #3, #9, #10 deleted (by you). Lists, attributes, 12 templates, tests T1, T5, T6, T7, T9 (Claude).
- **Not deletable through the API** (Claude tried): the 8 automation step templates 54-61, and the sent test campaign 86 ("TEST T7 delete me"). If you can see them in Brevo (Campaigns, and Templates), delete them. If you can't see templates 54-61 anywhere, they are orphans and harmless.

## What changed: no forms for you to build
KT asked "why am I building forms in Brevo?" and approved a better design (`drafts/decisions/2026-10-24-signup-function.md`). The site's forms now call a small function (`api/subscribe.js`) that holds the Brevo key in Vercel and does the consent bookkeeping itself. **Claude built the signup, free-check and order forms and wired them to it; you build none.** Double opt-in is no longer needed to protect unsubscribes (the function never touches a blocklisted contact), so decision D-11 is closed: single opt-in stays.

**You must keep Brevo's "Block unknown IP addresses" switched OFF** (Vercel's addresses change; blocking would stop every form). Keep the Brevo key active: the website now uses it.

## Part B · Segments (optional, 10 minutes)
Only for your own checking; the audit script already covers the same questions, so skip these if you like. Brevo: **Contacts, Segments, Create a segment**.

| Segment name | Conditions |
|---|---|
| `Tips eligible` | In list **Career tips**; AND attribute **CONSENT_TIPS_AT** is not empty; AND email is not blocklisted |
| `Dormant` | In list **Job alerts**; AND no link clicked in any email in the last 90 days; AND added more than 90 days ago |
| `Needs consent audit` | In list **Career tips**; AND **CONSENT_TIPS_AT** is empty (always empty by design) |

## Part D · Automations (about 45 minutes)
Brevo: **Automations, Create an automation**. Two ways: build by hand, or open **the AI builder** and paste the sentence in quotes, then check each step matches the table. Every automation: leave Brevo's default of skipping blocklisted contacts. Template numbers are fixed; **do not edit templates in Brevo's editor** (Claude updates them).

| # | Name | Trigger | Steps |
|---|---|---|---|
| AU-1 | `YC2 AU-1 Job alerts welcome` | Contact added to list **Job alerts** | Send template **74** now. End. |
| AU-2 | `YC2 AU-2 Tips series` | Contact added to list **Career tips** | **Wait 1 day.** Send **75**. Wait **7 days**. Send **76**. Wait **9 days**. Send **77**. End. |
| AU-3 | `YC2 AU-3 Free-check follow-up` | Contact added to list **Check result sent** | Wait **4 days**. Condition: contact is in list **Career tips** AND not in list **Order completed**. If yes, send **82**. End. |
| AU-4 | `YC2 AU-4 After the order` | Contact added to list **Order completed** | Wait **21 days**. Condition: in **Career tips**. If yes: if attribute **LAST_PACKAGE** is *essential* send **83**; if *professional* send **84**; if *executive* skip. Wait **39 days**. Condition: in **Career tips**. If yes, send **85**. End. |

AI-builder sentences (paste one at a time):
- AU-1: "When a contact is added to the list Job alerts, send the template YC2 | JA-1 Job alerts welcome, then end."
- AU-2: "When a contact is added to the list Career tips, wait 1 day, send template YC2 | CT-1, wait 7 days, send template YC2 | CT-2, wait 9 days, send template YC2 | CT-3, then end."
- AU-3: "When a contact is added to the list Check result sent, wait 4 days, then if the contact is in the list Career tips and not in the list Order completed, send template YC2 | FC-1, then end."
- AU-4: "When a contact is added to the list Order completed, wait 21 days, then if the contact is in the list Career tips and the attribute LAST_PACKAGE is essential send template YC2 | CU-1-ES, or if it is professional send template YC2 | CU-1-PRO. Then wait 39 days and, if the contact is in the list Career tips, send template YC2 | CU-2, then end."

**Leave all four switched OFF** (draft/paused) until Claude has run the tests that need them (T3, T4) with test addresses and tells you they pass. Claude does those tests; you only tell Claude when an automation is saved. If a condition step doesn't exist (T4), tell Claude and the design is changed.

Hand-sent campaigns (no automation): **78** JA-R (quarterly "still want these?"), **79 / 80 / 81** monthly tips, and the weekly digest (Claude generates it and creates the draft campaign; you schedule it).

**Heads-up (found 24 Oct):** Brevo's builder copies each template into the automation (step templates 87-94), so the automation sends the *copy*, not templates 74-85. Claude checked all eight copies: text, links, subject and sender match the originals. The catch: if the wording is ever changed in `scripts/email_data.py`, the API can update 74-85 but **cannot** update the copies, so you would re-pick the email inside the automation. Map: 87=JA-1, 88=CT-1, 89=CT-2, 90=CT-3, 91=FC-1, 92=CU-1-ES, 93=CU-1-PRO, 94=CU-2.

## Part E · How a customer moves through (so the markers make sense)
1. Free check done: you reply by email, then add the person to list **Check result sent** (only if they ticked tips; the automation checks).
2. Order done: you set `LAST_PACKAGE` and `COMPLETED_ON`, then add them to **Order completed** last. Claude can do these small updates for you through the API when you say "X finished Essential" while the key is active.

## Part F · Tests that need your automations
When you tell Claude an automation is saved (still switched OFF), Claude runs T3 and T4 with test addresses and tells you when it is safe to switch it on.

## Part G · Sending from a Gmail sender: what to watch
You accepted this risk on 24 Oct. The tests show the mail is authenticated as Brevo's own sending domain (DKIM, SPF and DMARC pass) with replies to yirehcareers@gmail.com, so the practical risk is lower than feared, but inbox placement is not guaranteed. Keep to: small consent-only list, short emails, no image-heavy design, complaint and bounce watching in Brevo (Statistics) after every send, and stop and review if complaints reach 0.1% of a send. A domain remains the proper fix when you can afford one.

## What stays blocked until you say go
No email to anyone but you; automations stay off; no form is live on the site until you've sent the links and Claude's wiring is merged; no contact import.

## Part H · Put the logo into the four automations (re-pick the eight emails; about 20 minutes)
Added 25 Oct 2026. Claude re-pushed the 12 templates (74-85) with the YC logo header. The automations send their own copies (87-94, named like `YC2 AU-2 Tips series_step_#4`), which the API cannot edit, so they still go out without the logo. To fix, inside each automation you point each Send-email step at the matching template. Nothing else about the automations changes. I cannot see your screen, so menu names may differ a little; if one does not match, tell me what you see.

**When:** AU-1 any time (nobody is waiting in it). Do AU-2, AU-3 and AU-4 **after 25 Oct, 15:20 UTC**, when Claude has finished the AU-2 check and deleted the three test contacts, so nobody is waiting inside while you edit. No real customer is in AU-2, AU-3 or AU-4 yet.

**For every email below (same moves each time):**
1. Brevo: **Automations**, open the automation. If Brevo says it must be paused before editing, pause it (it keeps its settings).
2. Click the **Send an email** step with the number shown in the table (the number is in the step's old name: `..._step_#4` means step 4).
3. Choose **Edit** or **Change email**, then **Choose a template** (or "Select an existing template").
4. Find the template by the **exact name in the last column** and select it. Do **not** pick one whose name ends in `_step_#`.
5. Check the subject and the sender before saving: the sender must say **Yireh Careers** (yirehcareers@gmail.com). Save the step.
6. After the last step in that automation: **Save**, then switch the automation back on if you paused it. Check **re-entry** is still the setting you chose earlier.

| Automation | Step | Sends now (no logo) | Replace with this template (name to search) | Subject you should see |
|---|---|---|---|---|
| AU-1 Job alerts welcome | #2 | 87 | **74** `YC2 \| JA-1 Job alerts welcome` | You're in. Here's what to expect |
| AU-2 Tips series | #2 (after the 1-day wait) | 88 | **75** `YC2 \| CT-1 Tips: one thing to check tonight` | One thing to check on your CV tonight |
| AU-2 Tips series | #4 | 89 | **76** `YC2 \| CT-2 Tips: using AI for your CV` | Using AI for your CV? Check these four things |
| AU-2 Tips series | #6 | 90 | **77** `YC2 \| CT-3 Tips: what we do, don't do, cost` | What we do, what we don't, and what it costs |
| AU-3 Free-check follow-up | #4 (inside the "yes" branch of the condition) | 91 | **82** `YC2 \| FC-1 Free check: did the fixes make sense?` | Did the three fixes make sense? |
| AU-4 After the order | #4 (Essential branch) | 92 | **83** `YC2 \| CU-1-ES After Essential: what comes next` | Three weeks on: how's the CV working? |
| AU-4 After the order | #6 (Professional branch) | 93 | **84** `YC2 \| CU-1-PRO After Professional: what comes next` | Three weeks on: how's the search going? |
| AU-4 After the order | #10 (day-60 email) | 94 | **85** `YC2 \| CU-2 After any order: two months on` | Two months on: how's it going? |

Leave alone: the Wait steps, the Condition steps and the end steps. The Executive branch of AU-4 sends nothing at the first email; keep it that way.

**Tell Claude when it is done.** Claude then reads the automation's new step templates through the API (they get new numbers from 95 up), checks each one has the logo, the right subject and sender Yireh Careers, and updates `brevo-manifest.json` with the new map.
