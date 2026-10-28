# Optimization backlog — prioritised

Owned by the continuous-optimization agent; reviewed weekly. Priority = evidence × impact ÷ effort,
with distribution weighting: **nothing in the funnel can be measured until people arrive.**
Evidence labels: **[M]** measured here · **[D]** documented elsewhere in this repo · **[H]** hypothesis.

| # | Pri | Item | Evidence | Hypothesis / why | Primary metric | Guardrail | Effort | State |
|---|---|---|---|---|---|---|---|---|
| 1 | **P0** | Send the first weekly email (KT) | [M] 0 emails ever sent; 0 form submissions ever | The audience is empty because nothing has gone out; distribution precedes every optimisation | `utm_campaign=ja-d` sessions → `conversion-signup` | unsubscribes, complaints | KT: 15 min | **Blocked on KT** — campaign package ready (`campaign-2026-w44.md`) |
| 2 | **P0** | Post daily from `/kit` for a week (KT) | [M] kit has never been used; `utm_source` tagging already in place | First real traffic source; also the only way to learn which channel works | sessions by `utm_source` | — | KT: 10 min/day | **Blocked on KT** |
| 3 | **P0** | Add `GOATCOUNTER_API_KEY` as a repo secret (KT) | [M] workflow written today, secret absent | Without it the weekly snapshot never runs, so reporting stays manual | weekly snapshot file exists | — | KT: 2 min | Infra done, **one paste away** |
| 4 | P1 | Country-first eligibility prompt (strategy review §6.1) | [M] 70% of rows country-limited, 25% unclear, 1.7% worldwide | Asking "where can you work?" once and ranking by it is the highest-value UX change for every segment, especially international readers [H] | `filter-country` usage → apply clicks | no rise in bounces; results still honest | M–L | Not started — needs design + KT's yes on placement |
| 5 | P1 | Search coverage: `web developer`, `nurse`, `graphic designer` return 0 | [M] search-relevance harness 27 Oct | Some are inventory gaps (do not fake them); some may be vocabulary gaps a synonym map would honestly fix [H] | zero-result query rate | no irrelevant results appear (recall guard stays) | S–M | Open — decide per-query: synonym vs "we don't have it" |
| 6 | P1 | Group location variants ("6 locations") so the count stays honest | [D] 102 of 1,002 rows are the same role elsewhere; headline overstates choice by ~25% | Honest counting raises trust and stops the count being wrong on the one number we advertise [H] | distinct-role count; no drop in apply clicks | must not hide roles | M | Not started — strategy doc already recommends it |
| 7 | P2 | Weekly-email CTA prominence (backlog item 5 remainder) | [D] log 27 Oct | The email's job is a return visit; one clear CTA beats two weak ones [H] | click on the `ja-d` link | open/CTR not the goal — sessions are | S | Waiting on first send data |
| 8 | P2 | 8 employer hosts whose pages don't show the posting (31 listings) | [D] strategy audit 23 Oct | A reader landing on a generic careers page loses trust; either warn or drop the link | spot-check score; broken-path complaints | don't drop good listings | S–M | Open |
| 9 | P2 | ~26 doubtful early-career labels → human read → classifier fixtures | [D] strategy audit; CLAUDE.md quality rule | Wrong labels make the `?level=early` filter (and every early-career post) untrustworthy | label accuracy in spot-check | no false demotions | M | Open — needs a human read first |
| 10 | P3 | Per-job pages + JobPosting markup | [M] rules checked 28 Oct; no markup anywhere; single-page board | Only worth it once traffic suggests organic job search matters [H] | organic sessions | manual-action risk if markup wrong | L | **Deferred by decision** — re-evaluate after 2 weeks of real traffic |
| 11 | P3 | Whop checkout live | [D] `mode:'off'`, no payout account | Card payment may raise conversion for Essential/Professional [H] | checkout completions | compliance + privacy review | KT-gated | Blocked on `whop-go-live-checklist.md` |
| 12 | P3 | Device / source segmentation in reporting | [M] GoatCounter gives referrers + locations; device is not exposed natively | Mobile vs desktop behaviour differs enough to matter [H] | segmented funnel | privacy: counts only, no personal data | S | Deferred — needs traffic first |

**Actively out of scope (do not reopen without new evidence):** price changes (no buyer data),
hard paywalls on listings (hurts the free utility the board is built on), decoy tiers, scarcity
tactics (banned by the trust standard), scraping new sources (strategy review: gap cannot be
fixed that way), fabricated synonyms that invent coverage we don't have.

**Experiments (§4 format — one row each, updated when a result exists):**

| # | Evidence | Hypothesis | Segment | Control | Variant | Primary metric | Guardrail | Effort / risk | Result |
|---|---|---|---|---|---|---|---|---|---|
| E1 (28 Oct) | Live measurement: first job card sits 1,181px below the desktop fold and the hero had no links at all | A one-tap route to the listings gets browsers to jobs without costing the services block its reach **[H]** | All visitors, first session | Hero without a jobs link (state until 28 Oct) | Hero with “Browse the jobs ↓” → `#jobs` | `jobs-hero-jump` events (phone/desktop split) | `services-click-home-*` must not fall; no new console errors | S / low — one anchor, revert is one line | Shipped 28 Oct; **awaiting traffic** — needs ~2 weeks of real visits before any reading |

**Failed or superseded — do not repeat:** none yet; this is the first backlog. Anything tried gets
its result recorded here with sample size and uncertainty, and removed if it did not work.