# 10 · Implementation roadmap, cost, decision log and unresolved decisions

Status: PROPOSED (Phase 11 deliverables 12 and 13, plus the decision log). Nothing here is approved. **Phase 12 starts only when KT approves, item by item.**

## Ranking of proposed work

Scores are judgements: Impact (value to the business), Confidence (evidence behind it), Effort (Claude sessions and KT time), Cost (cash), Risk (if done wrong).

| Rank | Work | Impact | Confidence | Effort | Cost | Risk | Depends on |
|---|---|---|---|---|---|---|---|
| 1 | Fix the signup false-success message; add error state | M | High (verified defect) | S | 0 | L | none |
| 2 | Buy and authenticate a sending domain; mailbox plan | H | Medium | S (KT) | Domain: typically about $10-20 a year (**unverified**; check at purchase). Mailbox: free forwarding or paid (**unverified**) | L | D-04 |
| 3 | Consent-aware forms: signup (+ tips box, level), free check, order intake | H | High (regulators) | M | 0 | M | 2 for public use; Brevo form editing by KT |
| 4 | Brevo setup: rename list 11, create lists, attributes; delete the old system (needs separate approval) | M | High | S | 0 | M (deletes) | D-01, API or KT by hand |
| 5 | Operational email set in Gmail templates (rewritten copy) | H | Medium | S | 0 | L | none |
| 6 | Weekly digest in the new design and wording | M | Medium | S | 0 | L | 2 for public sending |
| 7 | AU-1 welcome and AU-2 tips series | M | Low | M (KT builds automations) | 0 | L | 3, 4 |
| 8 | AU-3 free-check follow-up, AU-4 after-completion | L-M | Low | M | 0 | M | 3, 4, T3, T4 |
| 9 | Register and weekly checklist; copy linter; Brevo audit script (read-only) | M | Medium | M | 0 | L | 4 |
| 10 | Privacy page update for the new purpose and forms | H | High | S | 0 | L (counsel to read) | 3 |
| 11 | Dormant sweep (quarterly, manual) | L | Low | S | 0 | L | 6 |
| 12 | Stage 2: website DB, webhooks, preference centre | Unknown | Low | L | Unknown | H | Triggers in 09 |

## Stages with exit criteria

| Stage | Contents | Exit criteria |
|---|---|---|
| **S0 Approval** | KT approves or edits this blueprint; decisions D-01 to D-12 | Written yes/no per decision |
| **S1 Foundations** (no emails to the public) | Items 1, 2, 4, 5; sandbox tests T1-T9 to the extent possible | Tests pass or are documented; domain authenticated; old system deleted per the list |
| **S2 Capture** | Items 3, 10 | Forms live with unticked box; privacy page updated; register in use |
| **S3 Send** | Items 6, 7 (welcome and tips only), digest to consented list | First send to tester addresses, then to real consented contacts after KT's explicit authorisation |
| **S4 Follow-ups** | Items 8, 9, 11 | Audit shows zero unconsented promotional sends |
| **S5 Review** | 09 monthly review; decide on Stage 2 | KT's call |

Effort and cost summary: no cash cost except the domain (and any paid mailbox or Brevo upgrade, none required now). KT time: about 2 to 3 hours of one-off dashboard work (forms, four automations) following click-by-click steps from me, then 10 minutes a week.

## Decision log (what was decided and why)

| ID | Decision | Why | Source |
|---|---|---|---|
| L-1 | Rebuild the Brevo system from scratch | KT's instruction, 24 Oct | KT |
| L-2 | Voice: short, warm, plain; one next step | KT's feedback that first emails were long and abrasive | `drafts/voice-and-copy-guide.md` |
| L-3 | Single opt-in for job alerts | KT's decision, 24 Oct | `CLAUDE.md` |
| L-4 | Brand: Yireh Careers; no personal name, face or founder line; signed as the team | KT's rules | `CLAUDE.md` |
| L-5 | Not described as a registered company | KT's rule | `CLAUDE.md` |
| L-6 | Option A (forms → Brevo, plus register) | 07 | this blueprint |
| L-7 | Operational emails stay in Gmail, by hand | Orders are manual; attachments; threads; no consent entanglement | 07 |
| L-8 | Two marketing purposes, separate consent | F12, F14, F16 | 07 |
| L-9 | No opt-in-request emails to existing contacts | F13, F14 | 07 |
| L-10 | Customers join promotions only by an unticked box at order intake | Brief rule plus F12 | 07 |
| L-11 | Brevo blocklist is the only suppression record; no "Do not send" list | One source of truth | 06 |
| L-12 | No incomplete-enquiry follow-up | Not observable; consent unclear | 05 |

## Unresolved decisions for KT (each with my recommended default)

| ID | Decision | Options | Recommendation | Why it matters |
|---|---|---|---|---|
| **D-01** | Approve this blueprint and the architecture (Option A) | Approve / change | Approve | Everything depends on it |
| **D-02** | Approve deleting the old Brevo objects listed in 06 | Yes / no / by hand | Yes, exact list in 06; sent campaigns kept | Needs API access or KT by hand |
| **D-03** | The two non-KT contacts: check their Brevo timeline | Keep as job-alert only / remove | Check first; if no consent source, remove | Rule C-3 |
| **D-04** | Domain and mailbox | Buy a domain now / wait | Buy before any public send; choose the name; mailbox by forwarding to Gmail at first | Deliverability gate: no public send until done |
| **D-05** | Add "tips and offers" unticked box to the signup form | Yes / no | Yes; keeps the two purposes clean | Without it the tips list grows only from other forms |
| **D-06** | Free-check weekly cap and turnaround time | A number | KT picks (docs suggest about 10 a week); publish both | RK-11 |
| **D-07** | Free-check form: build it | Yes / keep WhatsApp-only | Yes: it captures email, consent and the quota count | Without it, no consent record for check requesters |
| **D-08** | Order intake form: build it | Yes / keep WhatsApp onboarding | Yes: gives structured details and the consent box | Same |
| **D-09** | Lead magnet (a one-page "10-minute CV self-check" on the site) | Approve / skip | Optional, after S3; no attachment, a web page | Brief lists it as "if approved" |
| **D-10** | Level field on the signup form (optional, one select) | Yes / no | Yes; used to weight the digest; never inferred | Personalisation without sensitive inference |
| **D-11** | Double opt-in | Keep single / add | Keep single now; revisit at 2% bounce or after domain | KT's earlier decision stands |
| **D-12** | Counsel review before the first public send | Yes / no / budget | Yes, a one-hour review of the RK items in 08 | Not legal advice from me |
| **D-13** | Brevo API key | Keep / revoke | Not needed after one-off setup; revoke afterwards; restore IP allow-list | RK-15 |
| **D-14** | Who builds the four automations and three forms in the Brevo dashboard | KT with my click-by-click steps / I guide live | KT with steps | No API for automations (F22) |
| **D-15** | Quote the free-check "three fixes" promise as written on the site | Keep / change | Keep | Consistency |
| **D-16** | Server function to create contacts through the API instead of Brevo forms | Keep forms / build the function | Keep forms for launch; revisit after tests T2 and T5 (see `13-brevo-api-capabilities.md`) | A full-access key on Vercel and IP blocking off permanently |

## What I did not do

No changes to Brevo (read-only reads only), no contact import or export, no email sent, no forms or site code changed, no cost incurred. The earlier lifecycle templates and the old setup guide are superseded; I have not deleted them from the repository yet so you can compare.
