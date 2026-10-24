# 07 · Contact, consent and event data model

Status: PROPOSED (Phases 7 and 8 deliverable). No code or data created. Labels: **Verified**, **Recommendation**, **Assumption**.

## Option A or B

There is no database (Verified, 01). The brief asks us to compare two realistic options.

- **A. Forms go straight to Brevo.** Browser posts to Brevo-hosted forms (as today). Brevo is the only contact store. The only extra persistence is a small **register** (a spreadsheet or CSV that KT already effectively keeps in `client-data-log-template.csv`) holding orders and consent notes.
- **B. A website database** (for example a serverless function on Vercel plus a hosted database) stores contacts, consent and events, and syncs to Brevo.

| Criterion | A: forms → Brevo + register | B: website DB + sync |
|---|---|---|
| Cost | £0 | Database and hosting free-tier probably, but effort cost is large (**Assumption**: several days of build plus ongoing maintenance) |
| Complexity | Very low | A server, schema, sync, retries, auth, backups |
| Privacy | Fewer systems hold contact data | One more system with personal data and one more processor to list |
| Reliability | As reliable as Brevo forms | Two systems to keep in sync; failure modes multiply |
| Data ownership | In Brevo; exportable | Ours, but we maintain it |
| Deduplication | Brevo dedupes by email | We must implement it |
| Auditability | Brevo contact timeline plus register notes | Full event history in our control |
| Fit with how orders happen | Orders happen on **WhatsApp and Gmail** and are confirmed by a person. A database would still be fed by hand | Same hand-feeding, plus an admin screen to build |
| Future needs | Limited event automation | Needed for Whop webhooks, preference centre, high volume |
| IP allow-list conflict | None (no server calls Brevo) | A Vercel function calling Brevo meets Brevo's IP blocking (F21) |
| Time to launch | Days of configuration | Weeks |

**Recommendation: A**, because the events that matter (order agreed, payment confirmed, delivered, completed) are produced by a person, not by the website, so a database would be filled by hand anyway. It satisfies the brief's "simplest architecture that satisfies demonstrated requirements".

**Gate to move to B (Stage 2).** Re-decide when **any** is true: card checkout goes live with webhooks; orders exceed about 15 a month (**Assumption**: hand-keeping starts to cause mistakes around there); a preference centre is needed beyond Brevo's; or an audit shows consent records cannot be reconstructed from Brevo plus the register.

## The register (the minimum persistence)

One row per person per order or request. Kept in the same Google account as the mailbox (spreadsheet) or the existing CSV; access limited to KT. **Never** contains CVs or documents.

| Column | Meaning |
|---|---|
| `email` (lowercased) | Identity key |
| `first_name` | For emails |
| `request_type` | `check`, `order`, `growth` |
| `request_id` | `CHK-2026-0001`, `ORD-2026-0001` |
| `received_at` | When the request or order arrived |
| `source` | Form id or WhatsApp code (`from:tips-3`) |
| `package`, `addons` | As ordered |
| `payment_confirmed_at`, `payment_method`, `payment_ref` | **Only a real confirmation** (bank, crypto, Whop receipt) |
| `onboarding_complete_at`, `delivered_at`, `completed_at` | Service stage dates |
| `delete_by` | 30 days (check, no order) or 90 days after completion |
| `deleted_on` | When files were deleted |
| `tips_consent` | `yes`, `no`, or `unknown` |
| `tips_consent_at`, `tips_consent_src` | Copied from the form submission |
| `brevo_synced` | `yes` after KT adds the contact and sets attributes |
| `notes` | Free text, no sensitive data |

Retention: follows the privacy page (30 days for checks, 90 days after completion, 12 months for non-buyer enquiries).

## Identity and uniqueness

- Key: lowercased, trimmed email. One Brevo contact per email.
- Duplicate form submissions update the same contact; Brevo's default is no new contact. Test T9.
- Never merge records without KT looking.

## Consent model (Phase 8 rules, applied)

### Purposes

| Purpose | Basis (as stated in the privacy page or proposed) | Record | Withdraw by |
|---|---|---|---|
| **P1 Job alerts** | Consent (privacy page, today) | `CONSENT_JOBS_AT`, `CONSENT_JOBS_SRC` | Unsubscribe link in every digest; reply "stop" |
| **P2 CV tips and offers** | Consent, **new**, separate | `CONSENT_TIPS_AT`, `CONSENT_TIPS_SRC` | Unsubscribe link in every tips email; reply "stop" |
| **P3 Service communications** | Contract, or steps before a contract (privacy page row for free check) | Register row | n/a; stops when service ends |

### Rules (each is a test target)

- **C-1** An email address alone is never marketing consent.
- **C-2** A job-board signup is P1 only. It never enrols anyone in P2.
- **C-3** Unclear, missing, old or unverified consent defaults to **ineligible for promotion**. This includes the two existing non-KT contacts until their source is confirmed.
- **C-4** A free-check request authorises P3 emails for that request only.
- **C-5** A purchase authorises P3 only. It never activates P2. Customers join P2 only via the unticked box on the order intake form (or a later signup form).
- **C-6** We do **not** email existing contacts asking them to opt in (F13, F14). Consent is collected at the form, once.
- **C-7** Service emails carry no promotion (F15, F12). Where a single sentence follows published terms (day-30 Growth continuation), it is flagged for review (RK-6).
- **C-8** Suppression is applied within 2 days (target same day) and is never reversed by an import or script. **Test T5 (24 Oct) showed the current signup form DOES reverse a blocklist when someone re-submits an address (RK-27); fix: double opt-in on the form, decision pending (D-11).** (F11, F15, F23)
- **C-9** Withdrawing from P2 should not withdraw from P1. **Test T7 (24 Oct) showed Brevo's default unsubscribe page is global: one click blocklists the contact for everything (RK-28).** Design change: promotional emails offer a manual 'reply jobs only' route to stop tips only; the unsubscribe link says plainly that it stops all emails.
- **C-10** Double opt-in is **not** a substitute for explaining the purpose.

### Wording v1 (for the three forms)

Unticked checkbox, shown on the signup, free-check and order-intake forms:

> **Also send me occasional CV and LinkedIn tips, and Yireh Careers service offers.** Roughly twice a month at most. You can unsubscribe in any email. This is separate from the weekly job email.

Signup form main notice (button reads "Send me the weekly job email"):

> We'll send you the weekly job email. One tap to unsubscribe. See our [privacy policy](/privacy).

Free-check form notice:

> We'll use your details to review your CV and send you the result. If you don't order anything, we delete your CV within 30 days. See our [privacy policy](/privacy).

Order-intake notice:

> We'll use these details to do your order and email you about it. We delete your files within 90 days of finishing. See our [privacy policy](/privacy).

The forms keep the honeypot. A visible error replaces the current false success message.

### Double opt-in

- Job alerts stay **single opt-in** (KT's decision on 24 Oct, kept; F16 does not require double opt-in).
- Re-evaluate when a domain exists, if bounce rate exceeds 2%, or if odd signups appear. Brevo's double opt-in endpoint and template exist (F22).
- Tips (P2): single opt-in at launch, because the person has just done a clear act on a labelled, unticked box. A confirmation email adds friction and is itself a message; we revisit with data.

### Legal map by audience (a map, not a compliance declaration)

| Recipients | Rule family | What we do |
|---|---|---|
| EU and UK individuals | GDPR and UK GDPR, ePrivacy rules (UK: PECR) | Specific consent for marketing; opt-out in every email; soft opt-in not relied on |
| US individuals | CAN-SPAM | Accurate headers and subjects, ad identification where promotional, postal address, honour opt-out within 10 business days (we do 2 days) |
| Others | Not researched | Treated like EU standard as the conservative baseline |
| Operator | Brevo shows "Kyrenia - North Cyprus". Which law governs the operator is a legal question (D6) | Counsel to confirm |

### Privacy page changes needed (draft after approval)

1. Add purpose P2 (tips and offers) with its own basis and withdrawal route.
2. State what the order intake and free-check forms collect.
3. Brevo is already named; add that it holds names, emails and consent records.
4. Describe the register and its retention in plain words.
5. Keep the instruction "send documents by email".

### Data minimisation, access and vendors

- Brevo holds: email, first name, source, consent timestamps, a few stage fields. **Never** CVs, phone numbers or documents.
- Access: one owner (KT), Brevo login with 2-step verification; mailbox with 2-step verification (already recommended in `drafts/client-data-handling.md`).
- Processors: Brevo, Google (Gmail), WhatsApp (Meta), Vercel (hosting), GoatCounter (cookieless analytics), Whop (when live). Data-processing terms for each: **not verified in this pass**.
- Deletion: on request or at the retention date, delete from Gmail, the laptop, WhatsApp, the register and Brevo. **Exception we should keep and say so:** a suppression entry (the email address on the blocklist) so we do not email someone who asked us to stop. Legal review to confirm the wording (RK-14).
- CVs are employment-related personal data. They stay in Gmail and on the laptop only, deleted per the privacy page. AI tool rules: `drafts/client-data-handling.md` section 8.

## Suppression and deletion

1. Unsubscribe click, complaint or hard bounce: Brevo blocklists automatically (verify, T5, T7).
2. A "stop" reply on email or WhatsApp: KT blocklists the contact in Brevo and notes it in the register within 2 days.
3. Deletion request: acknowledge within the privacy page's stated period (OP-12), complete in one month, keep only the suppression entry and payment records the law requires.
4. Every script and form obeys: if blocklisted, do nothing.

## Canonical event taxonomy

Under option A, Brevo does not receive custom events. The taxonomy is still defined now as the single vocabulary for the register, for the audit script, and for **Stage 2** if option B is chosen (then `POST /v3/events` can carry it; event names meet Brevo's limits, F22).

**Final names, source, and whether the event is observable today:**

| Event | Who creates it | Observable today? | Notes |
|---|---|---|---|
| `newsletter_signup_submitted` | Brevo form | Yes (Brevo timeline) | Job alerts |
| `job_alert_preferences_updated` | Brevo form (level field) | Optional | Only if the level field is added |
| `cv_check_requested` | Free-check form | **Not yet** (form to build) | |
| `marketing_consent_granted` | A form with the box ticked | Yes once forms exist | Carries purpose and wording version |
| `marketing_consent_withdrawn` | Unsubscribe or reply "stop" | Yes (Brevo) / manual | Purpose-specific |
| `order_agreed` | KT | **Manual** | Row in the register |
| `payment_confirmed` | KT, after a real confirmation | **Manual** | Never inferred from chat |
| `onboarding_completed` | KT | **Manual** | Starts the Executive 30 days |
| `deliverable_sent` | KT | **Manual** | |
| `revision_requested` | Customer reply | **Manual** | |
| `service_completed` | KT | **Manual** | Sets `COMPLETED_ON`, `delete_by` |
| `linkedin_growth_started` | KT | **Manual** | By arrangement |
| `lead_magnet_requested` | n/a | **No** (no lead magnet) | Dropped unless approved (10, D-09) |
| `service_enquiry_submitted` | n/a | **No** (happens on WhatsApp) | Dropped from automation; optional enquiry log |
| `customer_referral_submitted` | n/a | **No** (no mechanism) | Deferred |

### Event record (if and when events are recorded in a system)

```json
{
  "event_id": "sha256(email|event|request_id|occurred_at_date)",
  "event": "payment_confirmed",
  "occurred_at": "2026-11-02T09:41:00Z",
  "email": "person@example.com",
  "request_id": "ORD-2026-0007",
  "source": "manual:register",
  "properties": { "package": "professional", "payment_method": "bank" },
  "recorded_by": "kt"
}
```

Idempotency: the same `event_id` can be applied twice with no second effect (checked before any automation-triggering change). Logging: every applied event is appended to a log file, never edited. Recovery: replaying the log reproduces the state. Under A this is a convention for the register and the audit script; it becomes code only in Stage 2.

## Synchronisation (under option A)

KT performs two steps per stage, described in the order checklist:
1. Update the register row.
2. Update the Brevo contact only where Brevo needs it: `STAGE`, `LAST_PACKAGE`, `COMPLETED_ON`, adding to a marker list. Add to the marker list **last**, because that fires the automation.

Failure path: if step 2 is forgotten, the customer gets no promotional email (safe failure). If a marker add happens by mistake, AU-3 and AU-4 entry conditions (also in "Career tips") stop the email for non-opted-in contacts (to verify in T4).
