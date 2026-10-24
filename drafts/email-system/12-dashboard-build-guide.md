# 12 · Brevo dashboard build guide (for KT)

Status: approved 24 Oct 2026 ("approve all"). Brevo's connection to Claude cannot create lists, attributes, forms or automations or delete anything, and the API key in the cloud environment returns "Key not found" (it is invalid or revoked), so these steps are done by you in the dashboard. Menu names can differ slightly from Brevo's current screens: if one doesn't match, tell Claude what you see and the steps are adjusted. **Total: about 2 to 3 hours, in the order below. Stop after any part.** Nothing here sends email to anyone.

## Part A · Make it safe (10 minutes, do first)
1. **Automations:** open Brevo, then **Automations**. Find **#3, #9 and #10** (the ones the AI builder made today). If any shows *Active*, switch it to *Paused*. Reason: they could email subscribers the old wording.
2. **The two other contacts:** **Contacts**, then list **11**. Open each contact that is not yours and read its timeline. If it shows a form signup, tell Claude "contact X has a form signup on <date>". If not, tell Claude "no record". (Without a record they receive nothing promotional.)

## Part B · Tidy the old build (15 minutes)
Delete only what is listed. **Do not touch** templates 1, 2, 5-16, lists 6-10, or sender id 1 (other projects).
1. **Contacts, Lists:** delete lists **12, 13, 14, 15, 16, 17** (all empty). **Rename list 11** to `Job alerts`.
2. **Campaigns:** delete the two drafts **19** and **53**. Keep the sent campaigns 17 and 18.
3. **Templates (Campaigns, Templates or Transactional, Templates):** delete templates **63 to 73** (names start `YC |`). The new ones are named `YC2 |`.
4. **Your automation step templates 54 to 61** (`Yireh MKT Welcome Series #9...`, `Automation #10...`, `Yireh MKT Essential Customers #3...`): delete the automations #3, #9, #10 first (Part A showed them), then these templates.

## Part C · Lists (5 minutes)
In Contacts, Lists, create three lists in the same folder as `Job alerts`:
- `Career tips` (consent: CV and LinkedIn tips and offers)
- `Check result sent` (marker only; add this description: "Marker. Means nothing about consent.")
- `Order completed` (marker only; same description)

Send Claude the new list numbers.

## Part D · Contact attributes (10 minutes)
Contacts, Settings, Contact attributes, Add. Create these eight, **exactly** these names (capitals, underscores):

| Name | Type |
|---|---|
| `CONSENT_JOBS_AT` | Date |
| `CONSENT_JOBS_SRC` | Text |
| `CONSENT_TIPS_AT` | Date |
| `CONSENT_TIPS_SRC` | Text |
| `LEVEL_INTEREST` | Text |
| `STAGE` | Text |
| `LAST_PACKAGE` | Text |
| `COMPLETED_ON` | Date |

Leave `OPT_IN`, `ENGAGEMENT_SCORE` and `AWARENESS_STAGE` alone and unused.

## Part E · Forms (about 1 hour; this is what makes consent real)
In Brevo, Contacts, Forms (or Marketing, Forms), build **three subscription forms**. For each, use the wording in `07-data-consent-event-model.md` (Wording v1). Rules for all three: **single opt-in, no pre-ticked boxes**, the tips box adds the person to `Career tips` **only when ticked**, keep a honeypot or CAPTCHA if Brevo offers one.

1. **Signup form** (edit the existing one; the site already posts to it): fields Email (required), First name (optional), "I'm looking for" (optional choice: Starting out, Mid-level, Senior and leadership; saves to `LEVEL_INTEREST`), then the unticked box *"Also send me occasional CV and LinkedIn tips, and Yireh Careers service offers. Roughly twice a month at most. You can unsubscribe in any email. This is separate from the weekly job email."* Main list: `Job alerts`.
2. **Free CV check form** (new): Email (required), First name (required), "Which role are you aiming for?" (text, goes into a note field if Brevo offers one; otherwise skip), the same unticked tips box. **Do not add any list for the check itself.** Notice text: *"We'll use your details to review your CV and send you the result. If you don't order anything, we delete your CV within 30 days."*
3. **Order intake form** (new, private link you send to a customer): Email, First name, Package (choice), "Roles you're aiming for" (text), the same unticked tips box. Notice: *"We'll use these details to do your order and email you about it. We delete your files within 90 days of finishing."*

**Test T2 while building:** see if a form can set a hidden or default value for `CONSENT_JOBS_SRC` / `CONSENT_TIPS_SRC` (for example `signup-v1`). If yes, set it. If no, tell Claude; the fallback is one form per wording version.

When each form is built, send Claude its **embed link or the HTML/form action URL**. Claude then wires it into the site (new free-check and order pages, the tips box on the signup) and updates the privacy page, which is the last step before anything goes live.

## Part F · Automations (about 45 minutes)
Templates are already in Brevo (sender Yireh Careers, reply-to yirehcareers@gmail.com). Build in Automations, Create. Each one: **exit the workflow if the contact is blocklisted** (Brevo does this by default; do not override it).

| Name | Trigger | Steps |
|---|---|---|
| `YC2 | AU-1 Job alerts welcome` | Contact added to list `Job alerts` | Send template **74** now. End. |
| `YC2 | AU-2 Tips series` | Contact added to list `Career tips` | Send **75** now. Wait 7 days. Send **76**. Wait 9 days. Send **77**. End. |

After the first two run clean in the tests below, tell Claude and it creates the templates for AU-3 (free-check follow-up) and AU-4 (after-completion), which need the marker lists from Part C. **Test T4 first:** in the automation editor, is there a condition step ("if contact is in list `Career tips`")? AU-3 and AU-4 need it. If not, tell Claude.

Template numbers: 74 JA-1, 75 CT-1, 76 CT-2, 77 CT-3. Do not edit them in Brevo's editor; Claude edits the source and updates them, so the wording and the repo stay in step.

## Part G · Tests with your own addresses (30 minutes)
Use `kaetooruche@gmail.com` and, if you have one, a non-Google address. Add test contacts by hand first, then delete them after. **Write down what you see; Claude wants the results, not "it worked".**

| Test | Do this | Expect |
|---|---|---|
| T1 | Submit the signup form once with the tips box unticked, once ticked (different test address) | First: on `Job alerts` only. Second: on both |
| T3 | Add a contact to `Career tips` by hand; submit the form; (later) add via API | Does AU-2 start each time? |
| T5 | Unsubscribe a test contact (or blocklist it), then submit the form again with its address | Does it stay blocklisted? Tell Claude exactly what changed |
| T6 | Open a received email in Gmail, three dots, **Show original** | Look for `List-Unsubscribe` and `List-Unsubscribe-Post`. Tell Claude if present, and whether SPF/DKIM show PASS |
| T7 | Unsubscribe from a tips email only | Still on `Job alerts`? |
| T9 | Submit the form twice quickly | One contact, one welcome email |

## Part H · Domain (before any public send)
1. Pick the name (short, plain; it appears in email addresses). Buy it in Vercel (Domains), where the site already lives. Tell Claude the name.
2. In Brevo: Senders, Domains and Dedicated IPs, Domains, **Add a domain**. Brevo shows DNS records (a verification code, DKIM, and a DMARC suggestion). Send Claude those records; Claude adds them in Vercel DNS through the connection, you click **Authenticate** in Brevo.
3. Create the sender `hello@<domain>` (or similar) with a mailbox or forwarding to yirehcareers@gmail.com, and switch the templates' sender to it. Then the first **public** send is allowed, with your separate go-ahead.

## What stays blocked until you say go
No email goes to anyone but you; no form is live on the site; the privacy page is not changed; no contact is imported. Those happen in the stages in `10-roadmap-and-decisions.md`, each with your go-ahead.
