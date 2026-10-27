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
| 27 Oct | **Six-persona mobile walkthrough (360×740) + fixes**: compact mobile services block, hamburger tap target | `artifacts/walkthrough.py`, `index.html` |

Test state: **168 tests, OK** (`python3 -I -m unittest discover -s tests`). Browser verification
scripts: `artifacts/verify_ui2.py` (cards/finder/filters/nudge), `artifacts/verify_platforms.py`
(platforms/URL/error state). Nothing deployed — local preview only.

## Walkthrough findings (27 Oct, heuristic pass at 360×740 — not real user research)

Measured before → after:

| Signal | Before | After |
|---|---|---|
| Search bar position, mobile | y=1,831 = **2.5 screens** | y=1,222 = **1.7 screens** |
| First job card, mobile | y=2,318 = 3.1 screens | y=1,708 = 2.3 screens |
| Services block height, mobile | 1,088px | **495px** (package cards hidden ≤640px; still shown on desktop) |
| Hamburger tap target | 32×35px | **43×46px** |

Per persona: **A first-time** — value prop + free/paid line + trust stats all above the fold; **B urgent** — search reachable in 1.7 screens (was 2.5), "customer support" → 74 matches, "no experience" → 38, card shows pills + absolute date + source in one line; **C skeptic** — per-card source/date/pills carry the trust story, `How We Verify` is one tap from the hamburger and the verify section sits at the page end with the platforms section after it; **D services prospect** — block CTAs, per-card CV button and the post-40-listings nudge all present; **E returning** — filter state now round-trips through the URL; **F distracted mobile** — focus order is logical (nav → disclaimer → services → search → filters), dark mode renders correct tokens, no horizontal overflow, all primary buttons ≥44px.

Deferred with reasons: toolbar stickiness stays `static` (deliberate since commit `bfe7617`; the expanded toolbar is ~400px on mobile and ~350px on desktop, so sticking it would eat a third of the screen); level chips at 34px pass WCAG 2.2 AA target size (24px) so they were left alone; footer links are inline text (exempt from target-size); desktop search sits ~1,182px down — noted, not changed (desktop layout untouched this round).

## Baseline (pulled from the GoatCounter API, 27 Oct 2026 — the numbers to beat)

Access: API key in `.env` as `GOATCOUNTER_API_KEY` (git-ignored; read-only usage). All-time since 1 Sep:

- **144 pageviews, 12 events.** Last 30 days: **68 views, 12 events**; busiest day 26 Oct (11).
- Pages: `/` 121, `/services` 8, `/services?pay=test` 2, `/verify` 1.
- Events: `filter-field` 3, `filter-country` 2, `services-click-pay-professional` 2, `service-nudge` 1, `cv-click-job-cv-button` 1, `apply-click` 1, `filter-level` 1, `services-click-pricing-professional` 1.
- **`conversion-*` never fired: zero form submissions ever** (signup, free-check, order).

Caveats that change how this is read: (a) several of those events line up exactly with our own
browser-verification sessions, so genuine human engagement may be near zero; (b) local preview
visits also ping the counter; (c) at these volumes nothing is statistically meaningful — the
numbers describe the plumbing, not visitor behaviour.
**Reading:** the funnel is instrumented end-to-end but has never carried traffic. Distribution
(WhatsApp kit posts, the weekly digest) is the binding constraint before any optimisation can be
measured. Re-run the same queries after deploy; `platform-*`, `guide-finder`, `services-click-home/*`
and `services-click-nudge-*` appear only then.

## Next priorities (in order)

1. **Read the funnel data once real traffic exists** (26 Oct baseline above; watch list:
   `drafts/kt-todo.md` §4). Expect the first weekly digest on Tue 27 Oct to start moving it.2. ~~Mobile user-flow walkthrough (six personas)~~ — **done 27 Oct**, see "Walkthrough findings" above; next is a real usability test with actual people, which cannot be done from this environment.
3. **Copy audit against `drafts/voice-and-copy-guide.md`** — the guide says the website copy has *not* been reviewed against it yet. Homepage hero, empty states, filter labels, services blurb.
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