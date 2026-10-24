# 08 · Privacy, compliance and deliverability risk register

Status: PROPOSED (Phase 11 deliverable 10). Likelihood and impact are **judgements** (L low, M medium, H high), not measured. "Counsel" means a qualified lawyer; none has reviewed this. This register does not declare the system legally compliant.

| ID | Risk | L | I | Mitigation in the design | Owner | Status after approval |
|---|---|---|---|---|---|---|
| RK-1 | Marketing from a Gmail-based identity that Brevo cannot sign lands in spam or is throttled (F10; inference). **Tested 24 Oct: DKIM, SPF and DMARC pass for Brevo's own domain; first emails reached the Gmail inbox (Updates and Promotions). KT accepted the residual risk and has no domain for now.** | L | H | Buy and authenticate a domain before any public send (06); test headers (T6); no public campaign until done | KT | Open: needs D-04 |
| RK-2 | 300 emails a day cap hit by tests plus digest plus automations (F18) | L now, M later | M | Count tests; trigger to upgrade or stagger (09); never requeue in a hurry | KT | Monitor |
| RK-3 | Plan limits assumed wrongly (2,000 automation contacts unverified, F19; Free-plan features) | M | M | Read the plan page logged in before building; tests T3, T4 | KT + Claude | Open |
| RK-4 | The two non-KT contacts have no recorded consent source | H | M | Rule C-3: no digest or promotion until KT confirms source; otherwise remove | KT | Open: needs KT check |
| RK-5 | A "please opt in" email to existing contacts is itself unlawful marketing (F13, F14; secondary sources) | M | H | Rule C-6: never send one; consent only at forms; read primary texts (Gap 1 in 02) | Claude | Designed out |
| RK-6 | Promotion creeps into service emails, or a "feedback request" or the day-30 sentence about LinkedIn Growth is judged marketing (F15, F12; ICO page silent on service messages) | M | H | Class O has a lint rule: no prices, no offers, no CTA to buy; the one Growth sentence and the feedback line use published terms and service-quality framing; counsel review before use | Claude + counsel | Open |
| RK-7 | Signup page shows "You're in!" even when Brevo failed or the address is blocklisted (verified defect, `index.html:1349`) | H | M | Fix in Phase 12: show success only on a confirmed response; visible error otherwise; test | Claude | To fix |
| RK-8 | A form, import or script re-subscribes a blocklisted contact (F23) | M | H | Test T5; scripts read the flag first and refuse; no bulk imports; imports need explicit approval | Claude | Open: needs T5 |
| RK-9 | A promotional campaign goes to the wrong audience (for example the job-alert list) | M | H | Promotional campaigns target only the "Tips eligible" segment; copy lint flags class P; KT sends a test first; two-person rule not available, so a checklist at send time | KT | Designed in |
| RK-10 | Automation fires twice or for the wrong person (marker list added by mistake) | M | M | Entry conditions require "Career tips"; marker add is the last step; one-send-per-contact setting where Brevo offers it; weekly audit | KT | Open: needs T4 |
| RK-11 | Free-check page says "a limited number each week" with no real number (F9: false scarcity) | M | M | Set a real weekly cap (KT picks it; docs suggest about 10), count it in the register, say "full" when full (OP-13) | KT | Open: needs D-06 |
| RK-12 | Fabricated or edited testimonials, before-and-afters or outcome claims | L | H | None used until real and permitted; first name only; no outcome claims; lint bans outcome words | Claude + KT | Designed in |
| RK-13 | AI-positioning copy overstates (for example "AI gets facts wrong" as a universal claim) | M | M | Copy says what a careful person checks, not what AI "always" does; no statistics without a source | Claude | Designed in |
| RK-14 | Which law governs the operator is unclear (address "North Cyprus"); GDPR and UK GDPR still reach targeted EU and UK people; keeping a suppression entry after an erasure request needs a lawful wording | M | H | Counsel to confirm; design follows the stricter regimes; suppression-retention sentence reviewed | KT + counsel | Open |
| RK-15 | Brevo API key expires or is blocked (IP security, F21); keys pasted in chat or committed | M | M | Design does not depend on the API after the one-off setup; key never in repo; revoke after use; IP allow-list restored | KT | Open |
| RK-16 | Manual steps are skipped (deletion at 90 days, register updates, "stop" replies) | H | M | Weekly 10-minute checklist; register has `delete_by`; audit script lists overdue deletions | KT | Open |
| RK-17 | CVs travel by email (not end-to-end encrypted) and may be pasted into AI tools | M | H | Existing rules in `drafts/client-data-handling.md` (no ID or bank details, tool settings, deletion); keep CVs out of Brevo | KT | Existing |
| RK-18 | Account suspended for complaints or low-quality list on a Free plan | L | H | Consent-only list; low volume; watch complaint rate; keep exports | KT | Monitor |
| RK-19 | Bounces from typos or bots under single opt-in | M | M | Honeypot kept; welcome email as a de-facto check; hard bounces auto-suppressed; revisit double opt-in at 2% bounce (07) | KT | Monitor |
| RK-20 | Referral incentives raise consumer-law or disclosure issues | L | M | No incentives offered; invitation only | Claude | Designed out |
| RK-21 | Data-processing terms for Brevo, Google, Meta, Vercel, GoatCounter, Whop not reviewed | M | M | Read each vendor's DPA page; list processors in the privacy page | KT + Claude | Open |
| RK-22 | UK rules are changing (DUAA 2025; ICO guidance under review) | M | M | Re-check ICO page before first public send and again at 6 months | Claude | Open |
| RK-23 | Sender domain never bought; the system launches without it | M | H | Hard gate: no public send until done (10, D-04) | KT | Open |
| RK-24 | System becomes too complex for one person to run | M | M | Option A, four lists, eight attributes, four automations; weekly checklist | Claude | Designed in |
| RK-25 | Messaging people first on WhatsApp breaks the platform's policy (not verified here) | L | M | No design depends on business-initiated WhatsApp messages | Claude | Designed out |
| RK-27 | **MITIGATED 24 Oct by api/subscribe.js (never writes to a blocklisted contact; re-tested live).** Was: the signup form re-subscribes a blocklisted address when anyone re-submits it (**confirmed by test T5**), so a stranger or bot can undo an opt-out or complaint | H | H | Double opt-in on the signup form (decision D-11); never script a blocklist change; weekly audit lists blocklisted contacts | KT | Open: needs KT's yes |
| RK-28 | Brevo's unsubscribe is global (**confirmed by test T7**): unsubscribing from tips also stops the weekly job email | H | M | Footer says so; manual 'jobs only' reply route; no per-list link promised | Claude | Designed in |
| RK-26 | Site-wide copy (for example "We cannot promise ..." five times) contradicts the new voice | H | L | Later review against `voice-and-copy-guide.md` (flagged by KT) | Claude | Deferred |

## Deliverability controls checklist (Phase 12 acceptance)

1. Domain authenticated in Brevo (SPF, DKIM, DMARC at least `p=none`) and From address on it (F10, F11).
2. `List-Unsubscribe` and `List-Unsubscribe-Post` headers present (T6).
3. One-click unsubscribe works and unsubscribes only the intended purpose (T7).
4. Postal address and clear sender identity in every P and S email (F15).
5. Plain-text version present; images optional; alt text on any image.
6. Unsubscribe honoured within 2 days; complaint and bounce suppression automatic (T5).
7. Spam complaint rate watched; stop-and-review thresholds below Google's 0.30% line: **0.10%** (Google's own monitoring target, F10).
8. Test sends reach Gmail, Outlook and Apple Mail inboxes, not Promotions or Spam where avoidable (T8). The Promotions tab is normal for marketing email and is not a failure.

## Items that need qualified legal review before the first public send

1. Which law governs the operator and which audiences you actually reach (RK-14).
2. Whether the free-check result email may suggest a package (privacy page says it may).
3. The single Growth sentence in OP-10 and the feedback line in OP-7 (RK-6).
4. The suppression-retention sentence for erasure requests (RK-14).
5. Whether to rely on the soft opt-in for customers at all (design says no).
6. Terms: refund and cooling-off wording stay unpublished until KT decides (project rule).
