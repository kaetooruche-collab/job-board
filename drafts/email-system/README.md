# Yireh Careers email system: blueprint for approval

Status: **PROPOSED. Waiting for KT's explicit approval (Phase 11 gate).** Written 24 Oct 2026 on branch `claude/optimistic-hopper-nv0qun`, not merged. Nothing was changed in Brevo or on the live site; nothing was sent.

## The design in one paragraph

Two kinds of email, kept apart. **Service emails** (order, delivery, revisions, privacy, Executive updates) stay in Gmail, sent by hand, and carry no promotion. **Brevo** sends only two things, each with its own consent: the weekly job email (consent for job alerts) and CV and LinkedIn tips and offers (a separate, unticked box on the signup, free-check and order forms). Nobody is enrolled in tips because they bought something or asked for a free check. There is no website database: the forms go straight to Brevo and a small register records orders and consent notes, because the events that matter (payment confirmed, delivered) are made by a person on WhatsApp, not by the site. A sending domain comes before any public send.

## Read in this order (about 25 minutes)

1. `10-roadmap-and-decisions.md`: the 15 decisions you need to make, with my recommendation for each, and the ranked work.
2. `05-lifecycle-and-funnel-map.md`: the whole system on one diagram, and what is deliberately not built.
3. `04-positioning-and-value-ladder.md`: why $29 and not AI, honestly.
4. `preview/index.html` (open in a browser) and `copy/05-operational.md`: the actual emails.
5. `08-risk-register.md`: what could go wrong and what needs a lawyer.

## All deliverables

| # | Deliverable (brief item) | File |
|---|---|---|
| 1 | Repository audit | `01-repository-audit.md` |
| 2 | Research report and source register, evidence matrix | `02-research-and-sources.md` |
| 3 | ICP comparison matrix | `03-icps-and-journeys.md` |
| 4 | Value proposition and objection analysis | `04-positioning-and-value-ladder.md` |
| 5 | Customer lifecycle visualisation | `03-icps-and-journeys.md`, `05-lifecycle-and-funnel-map.md` |
| 6 | Funnel and automation map | `05-lifecycle-and-funnel-map.md` |
| 7 | Brevo architecture and account requirements | `06-brevo-architecture.md` |
| 8 | Contact, consent and event data model | `07-data-consent-event-model.md` |
| 9 | Email inventory and complete copy library | `11-email-inventory.md`, `copy/`, `preview/` |
| 10 | Risk register | `08-risk-register.md` |
| 11 | Measurement and experimentation plan | `09-measurement-and-experiments.md` |
| 12 | Roadmap, dependencies, effort, cost | `10-roadmap-and-decisions.md` |
| 13 | Unresolved decisions | `10-roadmap-and-decisions.md` |

Builders and tests: `email_data.py` (all copy), `build_library.py` (regenerates inventory, copy files, previews), `tests/test_email_library.py` (copy and consent rules). `automation-build.md` and `drafts/brevo-setup-guide.md` are superseded.

## What is verified and what is not

- **Verified (opened or called in this session):** site and repo facts in 01, the live Brevo account state, the Google, Yahoo, ICO, FTC and Brevo pages cited as official in 02, the rendering of the 13 Brevo emails in Chromium.
- **Not verified:** how real inboxes render the emails; Brevo's 2,000-contact automation limit and paid prices; primary texts of the Cyprus and ICO consent-request rulings (secondary summaries only); whether Cyprus law applies to a business in North Cyprus; whether Brevo forms can store hidden consent fields; behaviour of blocklisted contacts re-submitting a form. Each is a test or a legal question with an owner in 06 and 08.
- **No legal advice.** 08 lists what a qualified lawyer should read before the first public send.

## Two things for KT before anything else

1. **Open Brevo → Automations and look at #3, #9 and #10** (made today with Brevo's AI builder). If any is switched on and triggered by list 11 or similar, it can email subscribers with the old wording. Pause them until the new design is approved.
2. **Check the two non-KT contacts on list 11** (created 14 and 18 Sept): does the contact timeline show a form signup? If not, they get nothing promotional (rule C-3).

## How to approve

Reply with the decisions, for example "approve D-01, D-02 (delete the listed objects), D-04 (I'll buy a domain), D-05 to D-11 as recommended, D-12 later". Phase 12 then runs in the stages in `10-roadmap-and-decisions.md`, and nothing goes to real contacts without a separate go-ahead.
