# Decision review: job board UI changes from Arshia's notes (27 Oct 2026)

**Status: implemented on branch `freebuff/eef7defc2f751b126b46605f`, awaiting KT's approval before merge.**
Scope: presentation and filtering only. No listing, classification, eligibility label, price, link,
tracking parameter or data source changed. `jobs.json`, `scripts/`, `data/` untouched.

Arshia's raw notes and KT's "alright" are the brief. This records what was built, what was
deliberately not built, and the one judgement call that touches KT's honesty rules.

## 1. What changed (all in `index.html`)

| Arshia note | What shipped |
|---|---|
| "AI default basic design" | Cards rebuilt as a five-row hierarchy: monogram + title + company/location → status pills and posted date → uncertainty note → one quiet icon meta line (absolute date · job type · level · source) → separated action row. Icons on pills (✓ Remote, ? unclear, globe, pin) so status reads by shape as well as colour. |
| "Job cards are populated, can be more organised; button placement, icons" | The four competing chip rows became one meta line; buttons keep their text and gain icons; "Why this label?" stays right-aligned on desktop, stacked on mobile. |
| "Field filter needs lots of x-axis scroll on mobile" | Field chips and the experience row now **wrap into a 2-column grid** on phones — no sideways scrolling (measured: `scrollWidth == clientWidth == 360`). Plus a step-by-step finder (below). |
| Step-by-step questions | "Not sure where to look? Answer 3 quick questions" (phones only) opens a native `<dialog>`: field with live counts → experience stage → country/region. It writes the **existing** filter state, so the normal chips appear and clear as usual. No filtering logic is duplicated or invented. |
| "Filter by salary range is missing" | Under More filters: "Salary stated" and "Minimum salary" with USD/EUR/GBP. See §2. |
| Experience years | "Experience asked for": none stated / up to 2 / 2–4 / 5+. Straight from the `yearsExperienceMin` field the pipeline already records. |
| Micro-payment hook and where it appears | One offer block placed **after** the listings (below the "Show more" button), dismissible permanently via `localStorage`, tracked as `service-nudge`. See §3 — including why the half-information paywall was **not** built. |

New GoatCounter events: `service-nudge`, `service-nudge-dismiss`, `guide-finder`, `filter-years`,
`filter-minsal`.

## 2. The honesty question: salary filtering (judgement call)

CLAUDE.md: never invent or estimate pay figures. A cross-currency minimum filter cannot be done
without converting, so the rule applied is:

- **The card always shows `salaryText` exactly as the employer wrote it.** Conversion happens only
  inside the filter, using rounded approximate rates stored in `FX` (index.html).
- The filter label and active-filter chip both say the figure is approximate ("Min ~USD 60,000").
- Listings with **no stated pay are excluded** whenever a minimum is set — never silently included.
  Verified: 548 of 1,002 match "≥ 60k", 0 of the rendered cards lack a stated figure.
- Hourly and monthly pay is annualised (×2,080 / ×12) for filtering only; the card keeps the
  employer's "per hour" wording.
- **Risk:** the FX table will drift. If more currencies appear in the feed, either refresh the table
  or drop the minimum filter and keep "Salary stated" only.

Alternative considered and rejected: filtering on the raw number regardless of currency (dishonest
across £/€/$), and excluding non-USD listings when a minimum is chosen (silently hides jobs).

## 3. The micro-payment hook: what was built and what was refused

**Built:** after the reader has been served 40 listings, one quiet block offers the two real,
already-approved next steps — "See what each package includes" → `/services`, "Get a free CV check"
→ `/free-check`. It sits *after* the content, never inside or above it, hides nothing, is one tap to
dismiss forever, and does not reappear once dismissed (verified in the browser).

**Not built, on purpose — Arshia's "half of the info then ask to pay" idea.** Reasons:
1. The strategy report lists manufactured obstruction under "tactics to avoid"; trust is the stated
   differentiator of this board (why the old board came down).
2. Withholding listing or eligibility information would contradict the listing standard in CLAUDE.md
   (every claim visible and linked).
3. There is no small-ticket product to charge for yet: card checkout is built but `mode: 'off'`, so
   a payment hook cannot actually take money without KT going through
   `drafts/whop-go-live-checklist.md` first.

If KT wants a paid tier later, the honest version is a genuinely larger deliverable at a small
price — a decision review first, not a UI toggle.

## 4. What was deliberately left alone

- All remote/eligibility classifications, labels, evidence quotes and "Why this label?" content.
- Filter behaviour: every existing filter, combination, chip, clear path and URL `?level=` entry.
- Prices, package names, revision limits, WhatsApp/email links, consent wording, analytics IDs.
- The disclaimer (KT: leave it as it is), the services block above the toolbar, `/free-check` and
  `/order` links from the previous pass.

## 5. Verification actually run (27 Oct 2026)

- `python3 -I -m unittest discover -s tests` → **159 tests, OK** (before and after the final edit).
- Headless Chromium at 360×740 and 1440×900 (`artifacts/verify_ui2.py`):
  40 cards render with monogram/status/meta/actions; exactly one `#services` block; apply and CV
  buttons present on all 40; salary parser spot-checked on five real strings; min-salary filter →
  548 matches, 0 cards without stated pay; "none stated" experience → 364 matches (equals the data
  count); guided finder opens, steps forward and back, applies field + level + country producing
  three clearable chips and 4 matches; **no horizontal overflow at 360px**; field chips and level row
  no longer scroll sideways; nudge appears, dismisses and persists; **zero console errors**.
- Screenshots reviewed: `artifacts/ui-desktop-cards.png`, `ui-mobile-card.png`, `ui-guide-step1.png`,
  `ui-guide-step3.png`, `ui-nudge.png`.
- Not tested: live site (`site_monitor.py` runs on the deployed build), keyboard-only pass of the
  dialog beyond native `<dialog>` behaviour, Safari/Firefox (`:has()` selection highlight degrades
  gracefully to the native radio).

## 6. Open items for KT

1. Approve or reject the salary-approximation approach in §2 (delete the minimum filter if rejected).
2. Decide whether the offer block after the listings stays (it is the only new paid-path prompt).
3. Arshia's paywall idea: recorded as declined-with-reason in §3; reopen only with a real
   small-ticket product and a decision review.