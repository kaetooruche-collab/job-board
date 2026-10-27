# Yireh Careers — optimization implementation record

Running log for the autonomous UX/conversion/retention brief (started 27 Oct 2026). Kept short so a
session can resume without redoing the investigation. Decision details live in
`drafts/decisions/`, not here.

## Done

| When | What | Where |
|---|---|---|
| 26 Oct | Phase 0 funnel bridges (services block above the toolbar, `/free-check` → `/services`, `/order` → `/services`), card/filter hierarchy pass | commits `eaa76c4`, `7967248`, `6df6ddd` |
| 27 Oct | Arshia notes: card rebuild (monogram, icon meta line, status-pill icons), mobile field chips wrap instead of x-scroll, 3-question guided finder, salary + years filters, dismissible service offer after the listings | commit `b0eb4e4`, decision `2026-10-27-board-ui-arshia-notes.md` |
| 27 Oct | **Priority 0 — platforms section**: kept, demoted out of the nav to the footer, moved after signup + trust sections, board/marketplace badges, copy states we don't verify their listings, `platform-view`/`platform-click` events | decision `2026-10-27-platforms-section.md` |
| 27 Oct | **Backlog 1 — analytics gaps**: `services-click-home-packages`, `-nudge-packages`, `-nudge-free-check`, `-freecheck-packages`, `-order-packages` (all previously unmeasured) | `index.html`, `free-check.html`, `order.html`, `site-forms.js` (`trackEvt`) |
| 27 Oct | **Backlog 2 — honest load-error state**: failed `jobs.json` fetch now says the load failed instead of claiming an empty feed; hero counters show "—" | `index.html` |
| 27 Oct | **Backlog 3 — filter state in the URL**: `readURL`/`syncURL`, campaign params preserved, canonical link so filtered URLs don't fan out pageviews; `?level=` deep links unchanged | `index.html`, `tests/test_platforms.py` |

Test state: **168 tests, OK** (`python3 -I -m unittest discover -s tests`). Browser verification
scripts: `artifacts/verify_ui2.py` (cards/finder/filters/nudge), `artifacts/verify_platforms.py`
(platforms/URL/error state). Nothing deployed — local preview only.

## Next priorities (in order)

1. **Read the funnel data once traffic exists** (GoatCounter login is KT's; Claude has no data —
   this blocks every "is it better?" question). Watch list: `drafts/kt-todo.md` §4.
2. **Mobile user-flow walkthrough (six personas)** — heuristic pass over the live preview at 360px,
   per §5 of the brief: first-time visitor, urgent seeker, skeptic, services prospect, returning
   visitor, distracted mobile user. Output: concrete defects with evidence, then fix them.
3. **Copy audit against `drafts/voice-and-copy-guide.md`** — the guide says the website copy has
   *not* been reviewed against it yet. Homepage hero, empty states, filter labels, services blurb.
4. **Search relevance / result quality** — search currently matches raw substring across title,
   company, description; check recall on real queries ("customer support", "nurse", "no experience").
5. **Retention**: search persistence across visits (URL state now makes this shareable; localStorage
   restore for returning visitors is the cheap next step), weekly-email CTA prominence.
6. **Competitive differentiator test** (§6 of the brief): does the eligibility labelling show up
   above the fold on mobile, and do users understand "Remote: not confirmed"? Needs real users or a
   guerrilla test — cannot be settled from code.

## Blockers / constraints

- **No GoatCounter access** → no baselines, no experiment readouts. KT: log in or share an export.
- **Toptal unreachable from this machine** (403 to every automated client) → its link is unverified;
  re-check from a normal browser before relying on it.
- **Checkout is `mode: 'off'`** → no payment-flow work is possible until KT runs
  `drafts/whop-go-live-checklist.md`.
- **Deployment/merge needs explicit KT approval**; everything here sits on the branch.

## Conventions used (keep following)

- Events: `services-click-*`, `cv-click-*`, `apply-click`, `conversion-*`, `filter-*`,
  `platform-*`, `guide-finder`, `service-nudge`. Counts only, no personal data.
- Filters live in `state` + `readURL`/`syncURL`; never a second filtering path.
- Every change: `python3 -I -m unittest discover -s tests` + one headless browser pass at 360 and 1440.