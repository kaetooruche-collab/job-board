# 12 · What KT does in the Brevo dashboard (updated after the API build)

Status: 24 Oct 2026. With the new API key, Claude built everything the API allows (see `13-api-capabilities.md`). What is left can only be done in the dashboard, because Brevo's API has **no endpoints for automations, forms or segments**. Menu names may differ slightly from Brevo's current screens: if one doesn't match, tell Claude what you see and the step is adjusted. Nothing here sends email to anyone.

## Already done by Claude (verified by reading back)
- List 11 renamed **Job alerts** (3 contacts kept). New lists: **18 Career tips**, **19 Check result sent**, **20 Order completed**.
- 8 attributes created: `CONSENT_JOBS_AT`, `CONSENT_JOBS_SRC`, `CONSENT_TIPS_AT`, `CONSENT_TIPS_SRC`, `LEVEL_INTEREST`, `STAGE`, `LAST_PACKAGE`, `COMPLETED_ON`.
- 12 templates created (all `YC2 | ...`, sender Yireh Careers): see the table in Part F.
- Deleted: old lists 12-17, draft campaigns 19 and 53, old templates 63-73.

## Part A · Make it safe (10 minutes, do first)
1. **Automations:** Brevo, **Automations**. Open **#3, #9 and #10** (made today with the AI builder). If any is *Active*, set it to *Paused*; then delete all three. Reason: they could email subscribers the old wording.
2. **Templates 54 to 61** (named `Yireh MKT ...` and `Automation #10 ...`) belong to those automations. Once the automations are deleted, deactivate and delete the templates (Brevo only allows deleting inactive ones). Tell Claude if you'd rather Claude deletes them through the API: it can, once you confirm.
3. **The two older contacts on list 11** (created 14 and 18 Sept): open each one's timeline. If it shows a form signup, tell Claude "contact X has a form signup on <date>". If not, tell Claude "no record". The API cannot read this.

## Part B · Segments (10 minutes)
Contacts, Segments, create three (the API can't):
- `Tips eligible`: in list **Career tips** AND not blocklisted AND `CONSENT_TIPS_AT` is set.
- `Dormant`: in list **Job alerts** AND no link click in the last 90 days AND added more than 90 days ago.
- `Needs consent audit`: in list **Career tips** AND `CONSENT_TIPS_AT` is empty. (Target: always zero.)

## Part C · Forms (about 1 hour; this is what makes consent real)
In Brevo, Contacts (or Marketing), Forms: build **three subscription forms**. Wording is in `07-data-consent-event-model.md` (Wording v1). Rules for all three: **single opt-in, no pre-ticked boxes**, the tips box adds the person to **Career tips** *only when ticked*, keep a CAPTCHA or honeypot if offered.

1. **Signup form** (edit the existing one; the site already posts to it). Fields: Email (required); First name (optional); "I'm looking for" (optional choice: Starting out, Mid-level, Senior and leadership, saved to `LEVEL_INTEREST`); then the **unticked** box *"Also send me occasional CV and LinkedIn tips, and Yireh Careers service offers. Roughly twice a month at most. You can unsubscribe in any email. This is separate from the weekly job email."* Main list: Job alerts.
2. **Free CV check form** (new). Email (required), First name (required), the same unticked tips box. **No list for the check itself.** Notice: *"We'll use your details to review your CV and send you the result. If you don't order anything, we delete your CV within 30 days."*
3. **Order intake form** (new, a private link you send a customer). Email, First name, Package (choice), "Roles you're aiming for" (text), the same unticked tips box. Notice: *"We'll use these details to do your order and email you about it. We delete your files within 90 days of finishing."*

**While building, test T2:** can a form set a hidden or default value for `CONSENT_JOBS_SRC` / `CONSENT_TIPS_SRC` (for example `signup-v1`) and the consent date? If yes, set them. If not, tell Claude: the fallback is one form per wording version, and Claude fills the dates later through the API.

When each form is built, send Claude its **embed link or the form's action URL**. Claude wires it into the site (free-check page, order page, the tips box on the signup) and updates the privacy page, which is the last step before anything goes live.

## Part D · Automations (about 45 minutes; the only place they can be built)
Every automation: stop for blocklisted contacts (Brevo's default; don't override). Template numbers are fixed; do not edit templates in Brevo's editor (Claude updates them from the source through the API).

| Automation | Trigger | Steps |
|---|---|---|
| `YC2 \| AU-1 Job alerts welcome` | Contact added to list **Job alerts** | Send **74** now. End. |
| `YC2 \| AU-2 Tips series` | Contact added to list **Career tips** | Send **75** now. Wait 7 days. Send **76**. Wait 9 days. Send **77**. End. |
| `YC2 \| AU-3 Free-check follow-up` | Contact added to list **Check result sent** | Wait 4 days. If the contact is in **Career tips** and not in **Order completed**: send **82**. End. |
| `YC2 \| AU-4 After the order` | Contact added to list **Order completed** | Wait 21 days. If in **Career tips**: if `LAST_PACKAGE` = essential send **83**, if professional send **84** (executive: skip). Wait 39 days. If in **Career tips**: send **85**. End. |

**Test T4 first:** does the editor offer a condition step ("if contact is in list ...")? AU-3 and AU-4 need it. If not, tell Claude.

Other templates (campaigns you send by hand): **78** JA-R (quarterly "still want these?"), **79 / 80 / 81** CT-M1 / M2 / M3 (monthly tips, rotate). The weekly digest is generated by `python3 scripts/make_digest.py`.

## Part E · Tests with your own addresses (30 minutes)
Use `kaetooruche@gmail.com` and, if you have one, a non-Google address. Add test contacts by hand; delete them afterwards. Report what you *see*.

| Test | Do this | Expect |
|---|---|---|
| T1 | Submit the signup form with the tips box unticked, then (another test address) ticked | First: Job alerts only. Second: both lists |
| T3 | Add a contact to Career tips by hand, then by form | Does AU-2 start both times? |
| T5 | Blocklist a test contact, then submit the form with its address | Does it stay blocklisted? Tell Claude exactly what changed |
| T6 | In Gmail, three dots, **Show original** on a received Brevo email | Look for `List-Unsubscribe` and `List-Unsubscribe-Post`, and SPF/DKIM results |
| T7 | Unsubscribe from a tips email only | Still on Job alerts? |
| T9 | Submit the form twice quickly | One contact, one welcome |

Claude can read the contacts back through the API after each test and tell you what happened.

## Part F · Domain (before any public send)
1. Pick a short, plain name and buy it in Vercel (Domains). Tell Claude the name.
2. Claude creates the domain in Brevo through the API and reads the DNS records Brevo needs, adds them in Vercel DNS, and asks you to click **Authenticate** in Brevo (or does it through the API).
3. Create the sender (for example `hello@<domain>`), forward its mail to yirehcareers@gmail.com, and Claude switches the 12 templates and the digest to that sender. Then the first **public** send is allowed, with your separate go-ahead.

## What stays blocked until you say go
No email to anyone but you; no form live on the site; privacy page unchanged; no contact import.
