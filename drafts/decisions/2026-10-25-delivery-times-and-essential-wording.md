# Decision: delivery times and Essential wording (KT, 25 Oct 2026)

Status: DECIDED by KT, the evening before launch. Supersedes the "5 working days" lines in `2026-10-18-pricing-and-offer-structure.md`.

| Item | Before | Now |
|---|---|---|
| Essential delivery | 5 working days | **2 working days** |
| Professional delivery | 5 working days | **3 working days** |
| Priority delivery add-on ($15, price unchanged) | "48-hour priority": first drafts in 2 working days instead of 5 | **Documents within 1 working day** (instead of 2 for Essential, 3 for Professional) |
| Executive | CV and cover letter 2 working days, LinkedIn profile setup 5 | **Unchanged** (see open point) |

All timing is still counted from when onboarding is complete. Essential's description was rewritten: tagline "A professionally written CV", polished description, "Delivered within 2 working days of completing onboarding". Prices, revision limits and package names are unchanged.

**Open point for KT:** Professional now includes LinkedIn profile setup within 3 working days, while Executive (which includes everything in Professional) still says LinkedIn profile setup within 5. Either Executive moves to 3, or the page explains why it differs. Left as it was until KT decides.

**Risk to keep in view (judgement):** 2 and 3 working days are faster promises than the 5 the service ran on. They only hold if onboarding information arrives complete and orders stay small; the "counted from when onboarding is complete" line carries that. Watch the first orders and tell Claude if the dates slip.

Where changed: `services.html` (cards, comparison table, add-on row, FAQ), `index.html` teaser, `drafts/whatsapp-messages.md` and the generated setup kit (catalog), CLAUDE.md. Guarded by `tests/test_services_terms.py`.

## Update, 29 Oct 2026: Executive LinkedIn setup now 3 working days
The open point is closed: Executive includes everything in Professional, and Professional's LinkedIn setup is within 3 working days, so Executive's LinkedIn setup moved from 5 to 3 to match (KT: "fix everything"). CV and cover letter stay at 2. Changed on the services page (card, table, timeline, FAQ) and the WhatsApp inclusions. Revert by restoring "5" in those places and in `tests/test_services_terms.py`.
