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
| 27 Oct | **GoatCounter access + baseline** (see Baseline section) — key in `.env`, read-only | `.env` (git-ignored), `drafts/analytics/GC-2026-10-27.md` |
| 27 Oct | **Weekly analytics snapshot**: `scripts/gc_snapshot.py` pulls totals/pages/events via the API and writes `drafts/analytics/GC-<date>.md` with deltas against the previous snapshot; 5 offline tests; first snapshot generated | `scripts/gc_snapshot.py`, `tests/test_gc_snapshot.py` |
| 27 Oct | **Copy audit vs the voice guide**: hero paragraph, results count (thousands separators, dropped the duplicate total, one mention of “on the board”), the three empty/error states (contractions, no “we refuse”), and the subscribe block’s duplicated weekly-email line replaced with a distinct fact | `index.html` |
| 27 Oct | **Search relevance**: matching and ranking pulled out into `search.js` (normalised query, light stemming, weighted field ranking); 12 node tests over the real `jobs.json` + a Python runner | `search.js`, `index.html`, `tests/node/search.test.js`, `tests/test_search.py` |
| 27 Oct | **Pay understated on 11+ published cards**: the extractor now looks 400 chars for the pay word (employers list zones under a heading), keeps the currency the employer wrote, never merges two currencies, and rejects a range labelled as equity; old-vs-new on the 982 published listings — 20 gain, 0 lose | `scripts/pay_text.py`, `tests/test_pay_text.py` |

Test state: **174 tests, OK** (`python3 -I -m unittest discover -s tests`, which includes the 12
node tests for `search.js`). Browser verification scripts: `artifacts/verify_ui2.py`
(cards/finder/filters/nudge), `artifacts/verify_platforms.py` (platforms/URL/error state),
`artifacts/verify_search.py` (ranking/precision/filters/console). Nothing deployed — local preview only.

## Search relevance (27 Oct 2026)

**What was wrong** (`artifacts/search_relevance.py` replays the old rule over `jobs.json`):

1. **No ranking at all.** Results kept feed order, so for `software engineer` only **33% of page 1**
   named the role — the rest merely mentioned it somewhere in the description. Same for `sales` (33%),
   `marketing manager` (45%), `analyst` (97%).
2. **Substring false positives.** `hr` returned **119 listings** because “hr” sits inside *their*,
   *through*, *charts*.
3. **Punctuation and inflection killed recall.** `customer-support` → 0 results; `nurses` / `nursing` →
   0; `developers` never found a title reading “Software Developer” (only descriptions containing
   the plural).

**What changed** — `search.js`, used by `applyFilters()` and unit-tested directly:

| | before | after |
|---|---|---|
| `software engineer` — share of page 1 naming the role | 0.33 | **1.00** (40 of 40) |
| `sales` / `analyst` / `account executive` | 0.33 / 0.97 / 0.93 | **1.00 / 1.00 / 1.00** |
| `marketing manager` | 0.45 | 0.80 |
| `hr` | 119 hits, 0.03 | **6 hits**, 0.67 |
| `customer-support` | 0 hits | 74 hits |
| `developers` | 71 hits, 0.07 | 157 hits, 0.65 (all 26 title matches on page 1) |
| queries whose title matches were all buried off page 1 | 3 | **0** |

Rules now: the query is normalised (hyphens/case/punctuation → spaces); every term must match
somewhere in the listing (the original AND rule, unchanged); a term matches a word by prefix, by
shared root (one plural, one -ies/-es/-ing/-er/-or, one silent -e — applied to both sides), or as a
**weaker 0.5-weight** “longer form” hit so *Business Development* ranks below *Software Developer* for
`developers`. Ranking weights: title 8, company 4, category 3, location 2, description 1, with ties
keeping feed order (newest first).

**Deliberately not done:** no synonym expansion (`web developer` still returns 0 — the board has no
such titles; inventing a mapping would be guessing at intent), no stopword list (it would change
result counts for phrases like “no experience”), no relevance tuning against clicks (there is no
click data yet — GoatCounter has never carried traffic).

Two bugs I caught in my own first draft, both with tests now: a reverse-prefix rule let a single-letter
word (“t”) satisfy `translator` (104 bogus hits), and letting a short stem satisfy a longer query made
`accountant` match every “account” (164 hits instead of 5). Both regressions are pinned in
`tests/node/search.test.js`.

Cost: filter + rank over all 1,002 listings is **24–33 ms**, inside the 120 ms search debounce.

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

## 28 Oct: filters remembered, and the copy pass finished

**Search persistence (backlog item 5).** The board now remembers a returning visitor's filters on
their own device: the filter state that `syncURL()` already writes to the address bar is also saved
to `localStorage` (`yf-filters`, filter values only, never anything else), and a *plain* visit —
no query string — restores it through the exact same `applyParams()` validator the URL uses, so a
stale or hand-edited value can never set a bad state.

**Precedence rule (this is why URL state is not broken):** if the URL carries *any* filter key, the
URL wins and the saved state is ignored entirely — so the kit's `?level=early` deep links, shared
filtered links and campaign parameters behave exactly as they did. `resetAll()` ("Clear filters")
empties both the URL and the storage. No second filtering path was added: `state` +
`readURL`/`syncURL` remain the only ones.

**Copy audit of `/services` and `/verify` (backlog item 3).** Findings and what changed:
- `/verify` stated its publishing rules **three times** (6 trust rules, 7 check cards, then a 9-item
  checklist that restated 7 of those cards). The checklist is now 4 lines covering only what the
  cards did *not* say (source credit, closed-role wording, commission-only, 30 days, "none of the
  checks came back with a problem"). Intro's "what we promise" dropped — the trust rules already
  carry the promises. Also fixed a missing `</p>` on the "Every experience level" card.
- `/services` "How do I pay?" was one 200-word block stacking card, WhatsApp, exchange rate,
  currency-conversion and anti-fraud copy. Split into 5 short paragraphs with the same facts
  (nothing added or removed — fees, exchange rate and the wrong-details warning all stay, as the
  voice guide requires). Fixed the broken sentence "Please do not pay to details you received from
  anyone else" → "…pay using details…".
- Not changed, deliberately: prices, package names, revision limits, delivery times, the 90/30-day
  deletion promises and the refund wording (all pinned by `tests/test_services_terms.py`,
  `tests/test_site_forms.py` and `scripts/site_monitor.py`).
- Verified in a browser at 1440 and 360: 179 tests OK, zero console errors, no horizontal overflow
  on `/`, `/verify` or `/services`. Harness: `artifacts/verify_persistence.py`.

## Next priorities (in order)

1. **Read the funnel data once real traffic exists** (26 Oct baseline above; watch list:
   `drafts/kt-todo.md` §4). Expect the first weekly digest on Tue 27 Oct to start moving it.2. ~~Mobile user-flow walkthrough (six personas)~~ — **done 27 Oct**, see "Walkthrough findings" above; next is a real usability test with actual people, which cannot be done from this environment.
3. ~~Copy audit against `drafts/voice-and-copy-guide.md`~~ — **done**: homepage 27 Oct, `/services` and
   `/verify` 28 Oct (above). Nothing on the site is now unreviewed against the guide.
4. ~~Search relevance / result quality~~ — **done 27 Oct**, see “Search relevance” above. Remaining
   gap is coverage, not matching: queries the board genuinely has no listings for (`web developer`,
   `graphic designer`, `nurse`) still return nothing, which is the inventory speaking, not the search.
5. ~~Retention: search persistence across visits~~ — **done 28 Oct** (above). Still open: weekly-email
   CTA prominence.
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