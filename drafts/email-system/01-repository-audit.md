# 01 · Repository and business audit

Status: PROPOSED (Phase 1 deliverable). Read-only audit, 24 Oct 2026, branch `claude/optimistic-hopper-nv0qun`. Every row cites a file or a live Brevo read. "Verified" means I opened the file or called the Brevo read endpoint in this session; it does not mean the feature works end to end.

## Repository map (what exists)

| Area | Finding | Evidence |
|---|---|---|
| Stack | Static HTML/CSS/JS site. No framework, no `package.json`, no `api/` folder, no server-side code of any kind. | `ls` of repo root; `vercel.json` has only headers and one redirect |
| Hosting | Vercel project `north_cyprus_remote_job_board`, public address yirehcareers.vercel.app; every commit to `main` redeploys. | `vercel.json`, `CLAUDE.md` |
| Data pipeline | Python 3.12, run by GitHub Actions: `fetch-jobs.yml` every 6 h (bot commits `jobs.json` to `main`), `site-monitor.yml` every 3 h. | `.github/workflows/`, `scripts/` |
| Tests | 119 `unittest` tests covering classifier, QA rules, pay text, brand names, checkout config, digest. None cover consent, forms or email. | `tests/` |
| Analytics | GoatCounter (cookieless), events for apply and CV clicks. No cookie banner. | `index.html`, `site-config.js` |
| Contact store | None on our side. The only contact store is Brevo. | no database files anywhere |

## A. Existing and verified

| # | Item | Evidence |
|---|---|---|
| A1 | Job-alert signup is a Brevo-hosted form posted straight from the browser: email only, honeypot field `email_address_check`, notice text "By subscribing you agree to receive our weekly job email. You can unsubscribe at any time." | `index.html:942-951`, `site-config.js:17` |
| A2 | Single opt-in. The privacy page says so: "When you sign up through our form we do not currently ask you to confirm your address by a second email." | `privacy.html:446` |
| A3 | Privacy page names Brevo (newsletter), gives lawful basis (consent for newsletter), and retention: free-check CV 30 days if no order, 90 days after completion, non-buyer enquiries 12 months, newsletter until unsubscribe. | `privacy.html:380-418` |
| A4 | Services are sold and negotiated on WhatsApp via prefilled `wa.me` links. Documents travel by email only. | `services.html` (free check, orders), `drafts/client-data-handling.md` |
| A5 | Prices on the site match the brief: Essential $29, Professional $49, Executive $149, LinkedIn Growth $99/month, add-ons $15/$25/$10/$15/$15/$29. | `services.html:982-1115` |
| A6 | The site promises: free CV check is one per person, "We review a limited number each week; if we are full, we will say so", CV emailed (not WhatsApp), deleted within 30 days if no order. | `services.html:1375, 1510` |
| A7 | Customer emails are sent by hand from yirehcareers@gmail.com using Gmail templates; client files are tracked by Gmail label plus a CSV log. | `drafts/gmail-customer-emails.md`, `drafts/client-data-handling.md`, `drafts/client-data-log-template.csv` |
| A8 | Card checkout (Whop) is built but OFF; no payment webhook exists. | `site-config.js` (`checkout.mode`), `drafts/whop-go-live-checklist.md` |
| A9 | A weekly digest generator exists (picks up to 6 remote roles posted within 7 days, one per company). | `scripts/make_digest.py`, `tests/test_digest.py` |
| A10 | Brevo account (read live via the Brevo connector): plan **Free**, marketing automation **enabled**, 284 send credits left in the current period (period 20 Oct to 20 Nov 2026), company label "KAYZ Global Ltd", 7 lists, **0 segments**, only default plus three loose custom attributes (`LEAD_SOURCE`, `AWARENESS_STAGE`, `ENGAGEMENT_SCORE`) and an ambiguous boolean `OPT_IN`. | Brevo `accounts_get_account`, `lists_get_lists`, `segments_get_segments`, `attributes_get_attributes` |
| A11 | Brevo contents: list 11 "Job alert subscribers" has 3 contacts (KT plus two others created 14 and 18 Sept); lists 12-17 are empty; senders: id 4 "Yireh Careers" (yirehcareers@gmail.com), id 1 older; no authenticated domain. Templates: 26, including 11 from the first rebuild (63-73, old copy) and 8 step templates (54-61) created today by Brevo's AI builder for automations KT started; I cannot see those automations. | Brevo reads |

## B. Partially implemented

| # | Item | Gap |
|---|---|---|
| B1 | Sender identity | Sender id 4 is a Gmail address. Brevo cannot authenticate a Gmail address, so mail goes out through Brevo's own sending identity. Google's rules for all senders require SPF or DKIM; our From domain (gmail.com) is not one we can sign for (see 02, F10). |
| B2 | Consent record | The form stores a submission and a timestamp inside Brevo, but the wording version, form id and source page are not stored as contact attributes. Provenance of the two non-KT contacts is unknown. |
| B3 | Free CV check | Works as a WhatsApp conversation plus a manual email reply. There is no intake form, so there is no email address, consent record or weekly quota count until someone writes it down. |
| B4 | Unsubscribe | Brevo adds an unsubscribe link and its unsubscribe page to campaigns. How our two purposes would unsubscribe separately has not been tested. |
| B5 | Digest | Generated by a script, but pasted into Brevo and scheduled by hand. Fine at this size. |

## C. Missing

1. A free-check intake form (email, target role, consent evidence, quota counter).
2. An order or consent register that is more than a CSV template; today there is no record that links "paid" to "opted in to tips".
3. A second, separate consent for CV-service tips and offers (the only consent on file is for the weekly job email).
4. A preferences path (change level, leave one list but stay on the other).
5. Any sending domain (SPF, DKIM, DMARC) and a mailbox on it.
6. Any server-side endpoint, admin tool, webhook receiver or error logging for the signup.
7. Event capture for order stages (they happen in WhatsApp and Gmail, not on the site).
8. Tests for consent, suppression, copy rules and eligibility.

## D. Unknown, needs verification (none of these can be settled from the repository)

| # | Unknown | Why it matters | How to settle |
|---|---|---|---|
| D1 | Who the two non-KT subscribers are and how they consented | Unclear consent defaults to ineligible for promotion (rule in 07) | KT checks Brevo contact timeline; if no form record, treat as job-alert-only or remove |
| D2 | Brevo form settings: does it have double opt-in, CAPTCHA, hidden fields? | Decides how consent evidence is stored | Open the form in Brevo (KT) or test with a sandbox contact |
| D3 | Whether "Contact added to list" fires for form sign-ups, API adds and manual adds | All automations rely on it | Sandbox test (06, test T3) |
| D4 | What happens when a blocklisted person submits the form again | Suppression must never be silently reversed | Sandbox test (06, test T5) |
| D5 | Real enquiry volume and free-check volume per week | Decides whether any automation beyond a welcome is worth building | KT counts for 4 weeks (09) |
| D6 | Which law governs the operator | Brevo shows the address as "Kyrenia - North Cyprus"; the Republic of Cyprus rules and the EU acquis may not apply to a business there, but GDPR and UK GDPR still reach people in the EU and UK who are targeted | Local legal advice (08, RK-14) |
| D7 | Brevo's 2,000-contact automation limit: window and counting | Only secondary sources state it | Read Brevo's plan page logged in; the public page returns no text to this tool |

## Defects found during the audit (to fix in Phase 12)

1. **`handleSignup()` shows "You're in! Check your inbox." before Brevo has answered** (`index.html:1349-1355`). If the submission fails or the address is already blocklisted, the visitor is told they are subscribed. This is a trust defect and a consent-evidence defect.
2. **Scarcity claim on the free check** ("a limited number each week") has no stated number. `drafts/client-data-handling.md` says "about 10 a week". The claim is fine only if a real cap exists and is applied. See 08, RK-11.
3. **Stale documents**: `drafts/client-data-handling.md` still refers to Payhip order numbers and "TR" template ids; `CLAUDE.md` says Brevo templates 40-52 exist (KT deleted them). Update after approval.
4. **Website copy** repeats "We cannot promise ..." five times on `services.html` (lines 1107, 1115, 1424, 1429, 1436). KT flagged this as a later open problem; it is out of scope for the email build but affects consistency.
