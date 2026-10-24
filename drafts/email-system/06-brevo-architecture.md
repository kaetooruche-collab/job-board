# 06 · Brevo architecture and account requirements

Status: PROPOSED (Phase 6 deliverable). Nothing in this file has been created in Brevo. Sources: F18-F25 in `02-research-and-sources.md` and live reads of the account on 24 Oct 2026.

## Plan entitlements: what is verified and what is not

| Capability | Status | Evidence |
|---|---|---|
| Plan | **Verified: Free** | Account read: plan type `free`, Marketing vertical active |
| Marketing automation | **Verified enabled** on this account | Account read: `marketingAutomation.enabled = true` |
| Daily sending cap | **Verified 300/day** (284 credits left this period) | Help article F18; account read |
| Campaign to more than 300 contacts | Verified: sends 300 on the day, rest must be requeued | F18 |
| Test sends count toward the cap | Verified | F18 |
| Contacts into automations: 2,000 | **Unverified** (secondary sources only; window disputed) | F19 |
| Segments | Unverified on Free (the segments read returned none; creation not tested) | to test |
| Automation conditions (if/else step) and "Contact added to list" trigger | Trigger verified present in the editor (your screenshots); conditions and behaviour for form/API/manual adds **to test** | T3, T4 |
| Webhooks | Documented for all plans (F20); not needed in the recommended design | F20 |
| Brevo logo in emails, A/B testing on Free | Unverified | read the plan comparison page logged in |
| Paid plan prices | **Not verified** (page returned no text to my tools) | KT to read brevo.com/pricing logged in |
| API from a cloud session | Blocked by Brevo IP security (401 unrecognised IP) | F21; child session test |

## What each tool can do (so we know who does what)

| Task | Brevo connector (this session) | Brevo API (key) | Dashboard (KT) |
|---|---|---|---|
| Read lists, contacts, attributes, campaigns, templates | Yes | Yes | Yes |
| Create and edit email templates and draft campaigns, send tests | Yes | Yes | Yes |
| Create lists, attributes, segments | **No** | Lists and attributes: yes | Yes |
| Delete lists, templates, campaigns | **No** | Yes | Yes |
| Create, edit or activate an automation | **No** | **No documented endpoint** (F22) | **Yes (only place)** |
| Create or edit forms | No | No | Yes |
| Authenticate a sending domain | Read only | Yes (domains) | Yes |

Consequence: **KT builds the four automations and the three forms in the dashboard**, following click-by-click steps that I write after approval. The API key is only needed for creating attributes and lists and for deleting the old system, a one-off job. It is not needed for the ongoing design, so the key can be revoked afterwards and the IP-security problem does not become a permanent dependency.

## Contact taxonomy

Principles from the brief: small, explicit, no list membership treated as proof of consent.

### Lists (4)

| List | Purpose | Contains | Consent meaning |
|---|---|---|---|
| **Job alerts** (rename existing list 11) | Weekly job email | Everyone who signed up for it | Consent for job alerts only |
| **Career tips** | CV and LinkedIn tips, relevant follow-ups, offers | Only people who ticked the separate box | Consent for tips and offers |
| **Check result sent** | Marker to trigger AU-3 | People whose free-check result was sent | **None** |
| **Order completed** | Marker to trigger AU-4 | People whose order is complete | **None** |

Old lists 12-17 (Free CV check requested, Customers: Essential/Professional/Executive, LinkedIn Growth: active, Do not send) are **retired**: customer state is an attribute and a register row, not a list; "Do not send" duplicates Brevo's blocklist and creates a second source of truth.

### Attributes (8 new; reuse 3 existing; leave the rest alone)

| Attribute | Type | Values / meaning | Set by | Why it exists |
|---|---|---|---|---|
| `CONSENT_JOBS_AT` | date | when job-alert consent was given | form (automatically) or manual with note | Evidence |
| `CONSENT_JOBS_SRC` | text | form id and wording version, e.g. `signup-v1` | form hidden field if available; else manual | Evidence |
| `CONSENT_TIPS_AT` | date | when tips-and-offers consent was given | form or manual | Evidence |
| `CONSENT_TIPS_SRC` | text | form id and wording version, e.g. `check-v1` | form or manual | Evidence |
| `LEVEL_INTEREST` | text | `early`, `mid`, `senior` (what they chose, optional) | signup form field | Digest weighting; never inferred |
| `STAGE` | text | `subscriber`, `check_requested`, `check_sent`, `customer` | KT by hand | Eligibility and counting |
| `LAST_PACKAGE` | text | `essential`, `professional`, `executive`, or empty | KT by hand | Which CU-1 variant |
| `COMPLETED_ON` | date | service completion date | KT by hand | AU-4 timing and exclusions |

Reused: `FIRSTNAME`, `LEAD_SOURCE` (source form or page, set by hidden field), the system attributes. Not used: `OPT_IN` (boolean, ambiguous meaning), `ENGAGEMENT_SCORE`, `AWARENESS_STAGE` (inferred states we do not want), `LASTNAME`, phone fields (data minimisation: we do not need them in Brevo).

If hidden form fields are not supported (T2), consent source and version are recorded by creating a separate Brevo form per wording version and noting its id in the register; attributes are then set by KT when auditing.

### Segments (3; created after lists exist; not consent evidence)

| Segment | Definition | Use |
|---|---|---|
| Tips eligible | In "Career tips" AND not blocklisted AND `CONSENT_TIPS_AT` is set | Sending any P campaign (belt and braces with the list) |
| Dormant | In "Job alerts" AND no link click in 90 days AND created over 90 days ago | JA-R quarterly sweep |
| Needs consent audit | In "Career tips" AND `CONSENT_TIPS_AT` is empty | Weekly check; target is zero members |

### Suppression

- **Brevo's blocklist flag is the single suppression record.** Unsubscribes, complaints and hard bounces set it automatically; our own "stop" replies are applied by KT within 2 days.
- No "Do not send" list.
- **Never** write to a contact that is blocklisted (no import, API upsert or form that clears it). The audit script (below) reads the flag first and refuses.
- A person who truly wants back on submits the form again *after* we have confirmed Brevo's behaviour (T5), and that resubscription is itself a recorded new consent.

## Sender, domain and deliverability

1. **Today:** sender id 4 "Yireh Careers" at yirehcareers@gmail.com. Brevo cannot sign Gmail addresses, so mail goes through Brevo's own sending identity. Google's rules for all senders require SPF or DKIM aligned with the From domain (F10); a gmail.com From through a third party cannot be aligned. That is an **inference** about inbox placement, not something the Google page states.
2. **Recommendation:** buy a domain and authenticate it in Brevo (SPF, DKIM, DMARC at least `p=none`) **before the first send to anyone outside your own addresses and a few known friends**. Until then: no campaigns to the public list; welcome email only, tested to your own Gmail and one outside provider.
3. **Mailbox on the domain:** needed so replies land somewhere and the From address is real. Options (cost not verified here): forwarding to the existing Gmail inbox; a paid mailbox service. KT decides (10, D-04).
4. **Deliverability safeguards:** one-click unsubscribe (verify Brevo adds the header, T6); physical address in every marketing email (verified requirement, F15); plain-text part; no link shorteners; consistent From name; small, consent-based list; complaint rate watched against Google's thresholds (0.10% to stay clear, 0.30% hard line, F10).
5. **Sending limits:** 300 a day total across digests, tests, tips and automation emails. At the current list size this is not a constraint; at about 200 weekly digest recipients plus automations it starts to be (09, trigger).

## Tests to run in a sandbox before any real send (the "verify, do not assume" list)

Use only addresses KT owns (for example kaetooruche@gmail.com plus plus-aliases, and one non-Google address if KT has one).

| ID | Test | Pass means |
|---|---|---|
| T1 | Submit the signup form with an unticked and a ticked tips box | Contact lands on the right lists; attributes set |
| T2 | Can a hidden field set `CONSENT_*_SRC`? | Yes, or fall back to one form per wording version |
| T3 | Does "contact added to list" fire for form submission, manual add and API add? | All three, or we know which not |
| T4 | Is there an entry condition or if/else step on Free? | Yes (needed to enforce "also in Career tips") |
| T5 | Blocklist a test contact, then submit the form again | The contact stays blocklisted, or we know exactly what changes |
| T6 | Inspect a received test email's full headers | `List-Unsubscribe` and `List-Unsubscribe-Post` present; DKIM result noted |
| T7 | Unsubscribe from the tips email only | Job-alert subscription unaffected (or we know the setting that gives this) |
| T8 | Send the test digest and tips emails to Gmail, Outlook and Apple Mail (phone and desktop, light and dark) | Renders correctly (I check my rendered previews first; you check the real inboxes) |
| T9 | Two quick form submissions of the same email | One contact, no duplicate sends |

## Brevo-side verification tooling (Phase 12, read-only first)

A small script (`scripts/email_audit.py`, to be written after approval) reading Brevo through the API from a machine whose IP is authorised, never writing without `--apply` and approval:
1. Reports lists and counts against the taxonomy above.
2. Lists contacts on "Career tips" with no `CONSENT_TIPS_AT`.
3. Lists contacts on any list who are blocklisted.
4. Confirms the old lists and templates are gone.
5. `--dry-run` default; every change logged; no secrets in output.

Also a local **copy linter** (`scripts/email_lint.py`): word counts, banned phrases, unsubscribe and address present in P and S emails, UTM links, no promotion in O emails. Tests live in `tests/`.

## Deleting the old system: done on 24 Oct 2026 (KT approved D-02)

Done through the API and verified by reading back: lists 12-17 (empty), draft campaigns 19 and 53, templates 63-73 deleted; list 11 renamed Job alerts and kept with its 3 contacts. **Left for KT:** automations #3, #9, #10 and their step templates 54-61 (the API has no automation endpoints). Not touched: sent campaigns 17 and 18, templates 1, 2, 5-16, lists 6-10. Full record: `brevo-manifest.json`; what the API can and cannot do: `13-api-capabilities.md`.

The three existing contacts: KT's own, plus two created 14 and 18 Sept with no recorded consent source (the API shows no source field). **Until KT checks their timeline, they receive no promotional email and no digest** (07, rule C-3).
