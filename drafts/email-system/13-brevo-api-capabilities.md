# 13 · What a Brevo API key lets Claude do, and what it cannot

Status: written 24 Oct 2026 from Brevo's current API index (https://developers.brevo.com/llms.txt) and the pages cited. **No key has been tested yet:** the key visible in this session returns `401 Key not found`. Brevo's documentation does not describe per-key permission scopes for API keys (only user-level permissions: SMTP, API Keys, Authorized IPs), so I treat a v3 key as full access to the account and will use only the operations below.

## What I can do with a working key (and will, in this order)

| # | Job | Endpoint family | Notes |
|---|---|---|---|
| 1 | Check the account, then create the 3 new lists and rename list 11 | Lists | Account check first (company label KAYZ Global Ltd) |
| 2 | Create the 8 attributes | Attributes | Names in `06-brevo-architecture.md` |
| 3 | Delete the old objects on the approved list | Lists, templates, campaigns | **Templates can only be deleted when inactive**: I set them inactive first, then delete. Never touches templates 1, 2, 5-16, lists 6-10, sender 1 |
| 4 | Create the 8 remaining templates and keep all 12 in step with the repo | Templates | HTML only, so they cannot be edited in Brevo's drag-and-drop editor |
| 5 | Draft the weekly digest campaign (no recipients, no schedule) and send tests to you | Email campaigns | Sending to real contacts needs your separate go-ahead |
| 6 | Create the sending domain in Brevo, read its DNS records, add them in Vercel DNS, then authenticate | Domains and senders | Needs you to buy the domain; DNS records go in through the Vercel connection; authenticate is one API call |
| 7 | Create a sender on the new domain (Brevo emails a code to the mailbox to confirm it) | Senders | You read me the code |
| 8 | Read-only audit: lists, counts, contacts on "Career tips" without consent dates, blocklisted contacts, unsent drafts | Contacts, lists, campaigns, account activity logs | Runs on demand |
| 9 | Record an order stage when you tell me ("Maria paid Essential"): update attributes and add the marker list **last** | Contacts | Never writes to a blocklisted contact; shows you the change first |
| 10 | Delete a contact or unblock one on a verified request | Contacts, blocklist | Per request, with your yes |
| 11 | Fire custom events to start an automation (for example `order_completed`) | Events | Optional alternative to marker lists |

Also available but **not planned**: contact import (not without your approval and a consent check), webhooks (not needed), consent groups (the endpoint says it works only if that feature is enabled on the account; not confirmed), WhatsApp, SMS, CRM, loyalty, ecommerce and sub-account functions.

## What no key can do (so you do it in the dashboard)

| Job | Why | Your step |
|---|---|---|
| Create, edit, activate, pause or delete **automations** | There is no automation endpoint in Brevo's API index | Build them in Automations. Steps in `12-dashboard-build-guide.md`, Part F |
| Create or edit **forms** | No forms endpoint | Build the 3 forms in Brevo (Part E) and send me each form's embed link |
| Create or edit **segments** | Only "Get all segments" exists | Build the 3 segments by hand if you want them (optional at this size) |
| Switch IP blocking on or off | The IP security docs describe the setting only as a dashboard option | See "Creating the key" below |
| Buy the domain, press Authenticate in the DNS step if the API call fails, read the sender code emailed to the mailbox | Money, login and mailbox | Part H |
| Log in, change plan, pay | Outside the API | You |

## One idea that would remove the forms step, and why I do not recommend it yet

A small server function on Vercel could create the contact through the API: it would set the consent dates and wording version itself, refuse to touch a blocklisted contact, and show a true success or error message. That solves the hidden-field question, the blocklist question and the false-success problem in one go. The price: a **full-access key stored on Vercel**, **IP blocking switched off for good** (Vercel's outgoing addresses change), a new public endpoint to defend against abuse, and code to maintain. The blueprint's rule was "simplest architecture that meets demonstrated needs", and three Brevo forms meet them. **Recommendation: keep Brevo forms for launch; revisit this if form-building proves painful or a test shows forms cannot store consent evidence (test T2/T5).** Decision D-16 in `10-roadmap-and-decisions.md`.

## Creating the key (about 10 minutes)

1. In Brevo, open the account menu, then **SMTP & API**, then **API keys**, **Generate a new API key**. Name it `claude-yireh-oct24`. Copy it once. **Do not paste it into any chat.**
2. In Brevo, **Security**, **Authorised IPs** (https://app.brevo.com/security/authorised_ips): turn **Block unknown IP addresses** **off** for the week. Reason: Claude's cloud sessions use changing addresses. Turn it back on when we finish.
3. In the cloud environment settings for this project, set the environment variable `BREVO_API_KEY` to the new key (replace the old value), exactly as before. Environment variables are read **only when a session starts**, so the running session will not see the new value.
4. **Start a new session** on this repository and send "key is ready". The new session reads `CLAUDE.md` and the files in `drafts/email-system/`, tests the key, and then does items 1-8 above without asking again, because the blueprint is approved and the exact deletion list is in `06-brevo-architecture.md`.
5. When the week is over: delete the key in Brevo, remove the variable, and switch IP blocking back on.

## Why I cannot test a new key in this session

The shell here has the old value (89 characters, starts `xkeysib-`, returns `Key not found`). A key you create now will not appear until a new session starts.
