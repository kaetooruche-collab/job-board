# Business and conversion strategy for Yireh Careers

Date: 26 October 2026
Status: **PROPOSED** — nothing here has been approved or implemented.
Author: Buffy (Claude Code), at KT's request.
Master prompt used: `drafts/master-prompt-business-conversion.md`.
Scope: research and diagnosis only. No site code, prices, pages or copy were changed while producing this.

**Approval asked for:** the three Phase 0 changes in Part VIII (service block position, `/free-check` → `/services`, mobile filter discovery). Everything else waits for its own gate.

---

## How to read this document

Every claim carries one of five labels:

| Label | Meaning |
|---|---|
| **[EVIDENCE]** | Backed by a cited source or by something measured in this repository. |
| **[OBSERVATION]** | Directly observed on the live site or in the code on 26 Oct 2026. |
| **[INFERENCE]** | A reasoned conclusion from the above. Not proof. |
| **[HYPOTHESIS]** | A prediction that must be tested before it is believed or built on. |
| **[ASSUMPTION]** | Something the project currently assumes without data. |

Nothing in this document is a forecast of revenue. Where a number would be invented, it says *not measured*.

---

# PART I — Executive diagnosis

## I.1 What Yireh Careers already does well

These are real assets, not padding. Any redesign must preserve them.

1. **A differentiated product truth.** [OBSERVATION] The board classifies every listing as confirmed remote / restricted / not confirmed, and states geographic eligibility in the employer's own words. Nothing else in the remote-job-board category does this as a primary feature. This is the whole positioning and it is defensible, because it is expensive to copy honestly.
2. **A quality system that is unusual for its size.** [OBSERVATION] Four layers: unit tests (`tests/`, 159 tests), classifier-independent QA rules inside every refresh (`scripts/qa_checks.py`), a live-site monitor every three hours (`scripts/site_monitor.py`), and a manual spot-check (`scripts/spot_check.py` + `drafts/weekly-audit-prompt.md`). Most small job boards have none of these.
3. **Honest money.** [OBSERVATION] No applicant fees, no commission-only roles, no "no work permit needed", no invented salaries, no guarantee language. These are enforced by tests, not by intention.
4. **A real, priced, deliverable service menu** with stated delivery times and an email-verified free CV check as the top of the funnel (`drafts/decisions/2026-10-18-pricing-and-offer-structure.md`, `2026-10-25-delivery-times-and-essential-wording.md`).
5. **Compliance already thought about.** No dark patterns, no fake urgency, a real deletion promise, consent wording versioned and dated.

## I.2 The commercial problem, stated plainly

**[INFERENCE, high confidence] Yireh Careers is currently a free utility with a paid service catalogue attached, and almost nothing connects the two.**

The chain of measured facts:

- The home page is long. On mobile it renders **26,284px** of content; the paid-services block begins at **y ≈ 24,500px** — *below all 40 rendered listings*. A visitor must scroll roughly 68 phone-screens past the free value to reach a single paid offer. [OBSERVATION]
- On desktop the same block sits **1,573px** below a 900px fold. [OBSERVATION]
- `/free-check` — the warmest, most high-intent page in the product, where a person has already decided to send their CV — contains **no link to `/services` at all**. Its only cross-links are to `/privacy` and WhatsApp. [OBSERVATION]
- `/order` collects a package choice but its only back-reference is the wordmark, and the home page has no link to `/order` that this audit could find. [OBSERVATION]
- So the funnel has three unconnected islands: **browse → (nothing) → free check → (nothing) → order**.

**[INFERENCE, high confidence]** This is a discoverability defect, not a persuasion defect. No amount of copy testing will matter until the pages are connected.

## I.3 What is *not* proven

- [ASSUMPTION] That visitors want to pay for a CV at all. Zero purchase data exists. There is no checkout event in the analytics taxonomy (Part VII).
- [ASSUMPTION] That the traffic exists to convert. GoatCounter was not accessible from this environment; volume and sources are unknown.
- [ASSUMPTION] That the "experienced non-executive professional" hypothesis in `2026-10-24-board-strategy-icp-inventory-seniority.md` describes the paying customer. It is still labelled PROPOSED in that file, and no validation data has been collected.
- [ASSUMPTION] That the free CV check converts to orders. Anecdote only (KT reported one convert).

## I.4 The five highest-priority opportunities

| # | Opportunity | Type of claim | Evidence strength | Effort |
|---|---|---|---|---|
| 1 | **Connect the funnel**: move the service block above the listings on the home page; link `/free-check` → `/services`; link `/order` back. | Discoverability defect | Direct measurement, [OBSERVATION] | ~2 hours |
| 2 | **Run the validation plan before spending anything**: the 50 free CV checks are already the willingness-to-pay research. Instrument and log them. | Process | The plan already exists and has no data | KT's time |
| 3 | **Make the eligibility promise the headline**, not a card-level detail. | Positioning | [INFERENCE] strong, but unvalidated | ~1 day |
| 4 | **Fix the mobile field filter** (65+ chips in a horizontal scroller) with progressive disclosure, not a wizard. | Usability | Measured, [OBSERVATION] | ~3 hours |
| 5 | **Add a checkout / purchase event** to the analytics taxonomy. | Measurement | Absence confirmed in code | ~1 hour |

## I.5 Decisions that genuinely need more evidence

1. Whether **contextual offers inside the board** (a "Get a CV for this role" affordance at the moment of viewing a job) raise or destroy trust. [HYPOTHESIS] — must be tested with interviews before building.
2. Whether **years-of-experience filtering** is worth adding (`yearsExperienceMin` exists on 638 of 1,002 listings, 64% coverage).
3. Whether a **paid micro-product** (Arshia's £3–5 idea) is compatible with the trust promise. The technical answer is yes; the strategic answer is untested.
4. Which of the two positioning directions in Part V wins.

---

# PART II — Behavioural research, freemium evidence, competitor analysis

## II.1 The research base (four strands completed)

Four independent research strands were run on 26 Oct 2026. Summary of what they established, with the limits of each. Source URLs are in the evidence table (Part IX).

### Strand A — behavioural evidence

| Principle | What the evidence actually shows | Relevance here | Limitations | Contrary evidence | Testable hypothesis |
|---|---|---|---|---|---|
| Loss aversion (Kahneman & Tversky 1979; Thaler 1980) | Losses weigh roughly 1.5–2.5× equivalent gains in mixed-gain/loss choices. | A job seeker who has *received* a free CV check has something to lose. Framing matters. | Lab-based; the 1.5–2× figure does not generalise cleanly to field marketing. Tversky & Kahneman 1991 found loss aversion **absent** for gains-only choices. | Tversky & Kahneman (1991) "Loss Aversion in Riskless Choice"; later work questioning the generality of the ratio. | H1: A page that shows the user their *received* check result ("your report is ready") converts better than one that only describes what they would get. |
| Endowment effect / IKEA effect | People value what they helped create more highly; the IKEA effect requires *effort plus completion* of a physical/functional assembly. | A free tool that produces a personalised output should outperform a brochure. | The IKEA effect studies are about physical assembly and design tasks; generalising to "typed three filter answers" is weak. | Norton, Mochon & Ariely found the effect **disappears** when the assembly is incomplete or the user is unskilled. | H2: A tool that generates an artefact (e.g. an eligibility summary for *their* target role) raises WhatsApp clicks more than the same content shown as static copy. |
| Commitment & consistency (Cialdini) | Small, voluntary, written commitments increase later compliance. | A 3-question "help me choose" filter is a public-ish, voluntary commitment. | Classic studies are donations and door-to-door sales, not subscription funnels. | Freedman & Fraser (1966) replication issues; effect sizes vary hugely by context. | H3: Users who complete the guided filter proceed to a service page at a higher rate than those who only browse. |
| Social proof | Descriptive norms influence behaviour, strongest under uncertainty and with similar-others. | Job seekers are highly uncertain; testimonials would be strong. | **This project has zero testimonials and none may be invented.** Practically unusable until real customers exist. | Cialdini's own 2009 "defensive attribution" work: descriptive norms can backfire ("1 in 4 drivers *don't* wear seatbelts" increased non-compliance). | H4: Real, consented customer outcomes (even three) placed on `/services` raise order-page visits. Requires real customers first. |
| Choice overload (Iyengar & Lepper 2000) | 24–30 options reduced selections versus 6. | The home page shows 65+ field chips on mobile. | Scheibehenne et al. (2010) meta-analysis found **near-zero average effect**; the boundary conditions are contested. Greifer & Sugiyama (2023) found people often prefer *more* choices. | Iyengar's own later work qualifies the effect to high-preference clarity, not raw count. | H5: Collapsing the field list behind a disclosure control with a visible count ("65 fields") does not reduce selections but reduces drop-off. Measure before/after. |
| Present bias & deadlines | Hyperbolic discounting is robust; arbitrary deadlines are discounted by users. | Cannot be used here — fake urgency is forbidden by this project's own rules. | n/a | n/a | None proposed. **Rejected on principle.** |
| Web credibility (Stanford Credibility Project; Fogg) | Perceived design quality, information currency and verifiability are among the strongest credibility cues users actually apply. | This is the strongest academic support for doing the UI work at all. | 2002-era study; self-report. | Later work (e.g. on the "credibility halo" of big brands) suggests design cues matter most for *unknown* brands — which is exactly this one. | H6: First-impression tests ("Does this look like a real company? Would you send your CV here?") improve after the UI refinement. |

### Strand B — freemium and paywall patterns

Observed pattern across CV products: **free is a scan, a limited build, or a limited download; paid is the export, the removal of a limit, or the human.** The trigger is nearly always *after the user has invested effort* (built a resume, scanned a job description), never before. [OBSERVATION, several live pricing pages]

The directly relevant finding: **remote job boards mostly do not charge seekers at all.** Remote OK, We Work Remotely, Himalayas and Working Nomads monetise employers or accept advertising; a seeker-paid tier is the exception, not the norm. This is a finding, not a gap — it means (a) the board cannot be expected to earn directly, and (b) the monetisation has to sit where those competitors do not compete: a human service attached to a trust-branded board. [INFERENCE, moderate-to-high confidence]

### Strand C — substitutes for a $29–$149 human CV

Three substitute classes compete for the same need: **AI rewriting** (near-zero cost, unverifiable quality), **freelance CV writers** (typically well below $29 on gig marketplaces, with wide variance), and **free institutional help** (university career services, government employment services — free but often slow and geographically bound). [OBSERVATION]

**[INFERENCE, high confidence]** Yireh Careers cannot win on price against any of the three, and should not try. It can only win on *specificity*: a CV that is actually written for the roles and countries the person is targeting, plus eligibility judgement that no gig writer provides. If the services page reads as "we write CVs", it loses to Fiverr on price and to ChatGPT on speed. If it reads as "we make your CV work for remote roles open to where you can legally work", it competes with neither. **This is the single most important commercial conclusion in Part II and it drives the positioning in Part V.**

### Strand D — validating willingness to pay at low traffic

- **A/B testing is not available.** Sample size scales as `16·σ²/δ²` per variant; at a few hundred visitors per month with any realistic effect size, a valid test runs for years. [EVIDENCE, standard formula; Evan Miller / Optimizely documentation]
- Therefore the toolkit is: problem interviews (5 participants per persona, per Nielsen Norman Group; saturation, not statistical power), task-based usability tests, **pre-sales and concierge validation**, and fake-door tests that must be ethically designed (no deceptive content).
- **[INFERENCE, high confidence] this project already runs the correct low-traffic validation method and is not harvesting it.** The free CV check is a concierge MVP: a person hands over a real CV, KT does real work, and the moment of highest intent is captured. What is missing is a structured log — not a database, a spreadsheet — recording for each check: source (how they found us), target role and country, what they said they'd tried, and whether they ordered. Ten to fifteen of those is worth more than any A/B test available to this site.

## II.2 Competitor summary (selected, verified 26 Oct 2026)

| Competitor | Free | Paid | Price observed | Trigger | What it teaches us |
|---|---|---|---|---|---|
| Teal | Scan, limited resumes | Full toolkit subscription | Monthly, tiered | After a scan shows a deficiency | **Sell the diagnosis, then the cure.** |
| Rezi | Limited resumes | Subscription, AI rewriting | Monthly/annual | After building a resume | Effort-then-offer sequencing. |
| Resume.io | Very limited free | Single "trial" flow, aggressive | Low headline, then recurring | At download | The pattern this site must **avoid** — it is the industry's trust sink. |
| Huntr | Job tracker free | Career suite | Monthly | After tracking several jobs | Attach the offer to the *search*, not to a CV abstractly. |
| LinkedIn Premium Career | Profile free | Premium | Monthly | Applied to a job / viewed profile | The offer appears at the application moment. Directly supports the contextual-offer idea. |
| FlexJobs | Nothing (paywalled listings) | Subscription | Weekly/annual | Up-front gate | The anti-pattern for this product. Gating listings would destroy the differentiator. |
| Remote OK / WWR / Himalayas / Working Nomads | Full board free | Employer-side or ads | n/a | n/a | Seeker-paid boards are the exception. Our monetisation is elsewhere. |

**Limitation:** [INFERENCE] None of these prove profitability, and their pricing is not automatically transferable to a one-person, WhatsApp-delivered service.

---

# PART III — Segments, jobs to be done, and the free/paid boundary

## III.1 Jobs to be done

The functional job: *"Help me find work I can actually do from where I am, and help me get it."*
The emotional job: *"Reduce the anxiety that I am applying into a void."*
The social job: *"Look like a serious candidate when I do apply."*

## III.2 Segment assessment

| Segment | JTBD intensity | Willingness to pay | Cost to serve | Verdict |
|---|---|---|---|---|
| **Active applicants, mid-career, cross-border** (the PROPOSED ICP) | High | Hypothesised moderate–high | Moderate | **[HYPOTHESIS] Primary. Validate with the free-check log.** |
| Early-career / graduates | High, but price-sensitive | Low | High (more explanation needed) | Audience-building, not revenue. Already the correct policy in the post kit. |
| Executives | Very high | High | Very high | **Inbound only.** Correct today; do not pursue. |
| Casual browsers | Low | Very low | Low | Serve with free utility and email capture. |
| Freelancers / career changers | Moderate | Moderate | Moderate | Secondary; worth a landing page later, not now. |

**Segments deliberately not targeted now:** anyone seeking a guaranteed outcome, anyone outside the delivery capability, and any market served only by English-language copy.

## III.3 The free/paid boundary — the recommendation

> **Free: everything that helps a person decide where to apply. Paid: everything that helps them win the application.**

Specifically:

| Free, forever, ungated | Paid |
|---|---|
| Every listing, every source link, every eligibility label, every date | Essential / Professional / Executive CV packages |
| Search, all filters, "new this week" | LinkedIn packages and the 30-day Executive commitment |
| "How we verify" and the correction promise | Add-ons |
| The weekly digest and career tips (with consent) | LinkedIn Growth $99/month |
| **One free CV check per person** (a genuine diagnostic, not a teaser) | Everything after the diagnostic |

**[EVIDENCE-based reasoning]** This boundary is chosen because (a) gating listings would destroy the only real differentiator and every competitor already gives listings away free; (b) the diagnostic-then-cure funnel is the one pattern verified across the CV-tool category; (c) it requires no new product, no new payment surface and no new trust cost.

**Explicitly rejected:**
- **Progressive gating of listings** (Arshia's "half the info, then pay"). Rejected on the project's own rules *and* on commercial grounds: the differentiator is the free eligibility information, so selling it removes the reason to visit. What may be added instead is a free *personalised* layer (Part IV, the guided filter) — the user gives a little, gets something back, and the paid offer can then be specific. That is the honest version of the same instinct. [INFERENCE, high confidence]
- **Hard paywalls of any kind.**
- **Fabricated scarcity, countdowns, or "X people are viewing".** Forbidden and unnecessary.

---

# PART IV — Architecture, navigation, service discovery, paywall logic

## IV.1 Recommended sitemap

```
/                     Home: hero → eligibility promise → SEARCH+FILTERS → listings
                      (paid-services block moved ABOVE the listings)
/services             All packages, prices, delivery times, what you get
/services/cv          (anchor or page) Essential / Professional / Executive
/services/linkedin    LinkedIn packages + Growth plan
/free-check           Free diagnostic (exists)
/verify               How we verify (exists — should be linked from every card's context)
/privacy              (exists)
/order                Order details (exists, noindex)
/thanks               Post-submit info (exists, noindex)
/platforms            "Platforms you can sign up to" (exists as a section)
```

No new top-level pages are required. **[INFERENCE]** The site does not need a "pricing" page separate from `/services`; splitting them would create a maintenance and monitoring burden for no discovery gain.

## IV.2 Navigation

- **Desktop header:** Jobs · Free CV check · Services · How we verify · [Get a CV — blue button]
- **Mobile header:** same items inside the existing menu; the header's primary action must be visible without opening the menu.
- **Sticky element on the board:** one small, dismissible bar or nothing. It must not cover card actions at 360px. [OBSERVATION] The current `.sticky-wa` treatment and the TEST banner must not overlap card buttons — a known risk on narrow screens.

## IV.3 Service-discovery paths (all four should exist)

1. **Global** — header link to `/services`, on every page. *(Missing today.)*
2. **Above the fold on home** — one line under the hero: what is free, what is paid, with a link. *(Missing.)*
3. **Contextual on the board** — the existing "Get a CV for this role" per-card WhatsApp button, which is genuinely good: it is tied to a specific job, so the offer is specific. [OBSERVATION] Keep, and make sure its analytics event exists (Part VII).
4. **Post-diagnostic** — on `/free-check`, after submit and in the page body: "Ready for a full rewrite? See the packages." *(Missing — the highest-value gap.)*

## IV.4 Mobile specifics

- Services block above listings on home (same as desktop, shorter copy).
- Field filter collapsed behind a disclosure control showing the active count.
- No horizontal-scroll-dependent control may be the only way to reach a filter.
- Any sticky CTA ≤ 56px tall, dismissible, and never overlapping the per-card WhatsApp button.

## IV.5 Paywall logic

There is no paywall. The *offer* logic is:

| Trigger | Offer | Surface |
|---|---|---|
| Visitor reads 3+ listings | Free CV check | In-feed line after N cards, or post-scroll |
| Visitor clicks "Get a CV for this role" | Essential/Professional | WhatsApp, pre-filled with the job title |
| Visitor completes the free check | "See the packages" | Confirmation screen + follow-up email |
| Visitor orders | Order details | `/order?package=` (already works) |

**[INFERENCE]** The weakest link in this table today is the third row: it does not exist.

---

# PART V — Positioning, landing page, copy

## V.1 Two positioning directions

### Direction A — "The eligibility expert"
> *Know whether a remote job is actually open to you — before you spend an evening on the application.*

- Hero promise: remote jobs with honest eligibility, verified, dated, sourced.
- Services framed as: "when you have found the right role, we make sure your application is the one they read."
- Trade-off: distinctive, ownable, but the paid offer must bridge a conceptual gap (from "information" to "my CV").

### Direction B — "The honest job finder"
> *Real remote jobs, checked daily, with the restrictions shown.*

- Softer, more immediately legible, closer to the current copy.
- Trade-off: indistinguishable from every other honest board; the paid services look bolted on.

**Recommendation: Direction A, expressed with Direction B's plainness.** [INFERENCE, high confidence]
Reasons: (1) it is the only claim competitors do not make; (2) it makes the paid services *coherent* rather than bolted-on, because eligibility uncertainty is exactly what a CV service can resolve ("your CV says you need sponsorship; here is how to say it"); (3) it matches the project's own trust rules. Risk: the phrase needs testing because "eligibility" may not be the word stressed job seekers use. [HYPOTHESIS]

## V.2 Draft copy (ready to test, not yet applied)

Voice rules from `drafts/voice-and-copy-guide.md` were followed: contractions, one idea per sentence, warm, no stacked disclaimers, no guarantees.

**Home hero (Direction A):**
> **Remote jobs, with the restrictions shown.**
> Every listing links to the employer's own posting, carries its real posting date, and says plainly who can apply — "worldwide", a named region, or "eligibility unclear". Nothing is dressed up as open to you when it isn't.
> *[Search jobs]* · *[How we verify]*

**Sub-hero line (new):**
> The job board is free and always will be. When you have found the right role, our paid CV and LinkedIn services make sure your application reads like it belongs there. [See the packages](/services)

**Free CV check page, new closing block:**
> **Ready for a full rewrite?**
> If you would rather we did the whole thing, see [what each package includes](/services) — Essential from $29, delivered within 2 working days of receiving your details.

**"Get a CV for this role" card button (keep, tighten label):**
> Get a CV for this role → *(already good; do not change the WhatsApp prefill)*

**Services page, opening paragraph:**
> You already have the hard part: knowing which jobs are worth your evening. These packages are the rest — a CV and, if you want it, a LinkedIn profile written for the roles you are actually applying for, wherever you are.

**What must not be written (enforced by `scripts/site_monitor.py` and `tests/`):** "guaranteed", "no work permit needed", "the only job board", any promise to continue until a number is reached, any outcome claim.

## V.3 Page-by-page content plan

| Page | Section order | Purpose |
|---|---|---|
| Home | Hero → one-line free/paid statement → search+filters → results → services block → platforms → verify strip | Free value first, paid visible early |
| `/services` | Opening framing → three packages with delivery times → add-ons → Growth plan → free check as the low-commitment entry → FAQ (refunds, timing, what you must send) | Comprehend in 20 seconds on a phone |
| `/free-check` | What you get → form → what happens next → **link to packages** → privacy line | Convert the warmest lead |
| `/verify` | Six trust rules → how the four quality layers work → the correction promise | The credibility asset; link to it from the header |

---

# PART VI — Offer design, pricing, checkout, onboarding, trust

## VI.1 Pricing

**Do not change prices.** [EVIDENCE] The prices were approved by KT on 18 Oct (`2026-10-18-pricing-and-offer-structure.md`) and delivery times on 25 Oct. There is no willingness-to-pay data of any kind, so any change would be a coin flip.

**[INFERENCE] One structural observation worth recording:** the gap between the $49 Professional and the $149 Executive is bridged only by a $15 add-on and a $10 revision. A user choosing between two options with a large gap often anchors on neither. A **[HYPOTHESIS]** worth *testing* (not implementing) is a single intermediate option or a bundle — but only after twenty real order conversations tell us what people actually hesitate over.

## VI.2 The free CV check is the offer engine

[OBSERVATION] It is currently the only free diagnostic, it is well-written, and it is invisible from every other page except its own WhatsApp mentions.

Required, cheap changes: link to it from the header, from `/services`, and from the post-scroll point on the board; and log every check in a spreadsheet with source, target role, target country, stated blocker, and outcome.

## VI.3 Checkout and onboarding

- Checkout is WhatsApp (card checkout is built but **OFF**, `SITE.checkout.mode = 'off'`). **Keep it off** until the Whop checklist is completed. [EVIDENCE: CLAUDE.md v4]
- Onboarding friction is real but small: the customer must email their CV. `/free-check` already explains why (privacy) — that explanation should be reused on `/services` so the objection is handled before it forms.
- **[ASSUMPTION]** Refund and approval terms are undecided. Publishing them is KT's call; not publishing them is a known conversion cost.

## VI.4 Trust and support

The trust story already exists and is stronger than the site admits. **[INFERENCE]** `/verify` should be linked from the header and referenced on the services page, because the objection "why would I pay these people?" is answered by the four-layer quality system, not by testimonials.

---

# PART VII — Analytics, funnel definitions, experiments

## VII.1 Current state

[OBSERVATION] GoatCounter page counting plus `data-*` click events on apply links and the per-card WhatsApp button. **There is no event for: service-section visibility, service page view from the board, checkout initiation, order submit, or repeat purchase.** GoatCounter is not a funnel tool; it is a privacy-respecting page counter with a custom-event endpoint.

**[INFERENCE]** A realistic measurement design for this traffic level is: *named events + a weekly manual read*, not a dashboard.

## VII.2 Event taxonomy (proposed names, to be wired later)

| Event | Fired when | Type |
|---|---|---|
| `board_view` | Board renders | Diagnostic |
| `filter_used` | Any filter changes (with the group name) | Diagnostic |
| `job_open` | Card title/link to listing page clicked | Diagnostic |
| `apply_click` | Employer apply link clicked (exists) | **Primary outcome** |
| `cv_service_click` | "Get a CV for this role" clicked (exists) | **Primary outcome** |
| `services_view` | `/services` loaded | Diagnostic |
| `free_check_submit` | `/free-check` form submitted | **Primary outcome** |
| `order_submit` | `/order` form submitted | **Primary outcome (revenue proxy)** |
| `wa_click` | Any WhatsApp link clicked | Diagnostic |
| Guardrail: `report_listing` | Report link used | Guardrail |
| Guardrail: `monitor_fail` | Site monitor fails (already logged) | Guardrail |

**Funnel definitions:** visitor→apply click; visitor→`cv_service_click`; visitor→`/services`; `/services`→`order_submit`; visitor→`free_check_submit`; `free_check_submit`→order within 30 days (tracked in the spreadsheet, not the analytics).

**Primary outcome:** `order_submit` and `free_check_submit`. **Guardrails:** apply-click rate (a monetisation change that reduces applications has failed), page weight, monitor pass rate, `removed.log` volume.

## VII.3 Experiment roadmap (low-traffic honest version)

Because A/B testing is unavailable [EVIDENCE: sample-size math], these are **sequential before/after comparisons with a stated minimum period and a diary note of confounds** — not significance tests.

| # | Change | Hypothesis | Primary metric | Guardrail | Decision rule |
|---|---|---|---|---|---|
| E1 | Move services block above listings on home | H: service-block CTR rises from ~0 | `services_view` per board view | Apply clicks unchanged | Keep if apply clicks do not fall and services views rise |
| E2 | Add `/free-check` → `/services` link | H: warm leads continue | `/services` visits from `/free-check` | Check completion rate does not fall | Keep unless completion drops |
| E3 | Collapsed field filters on mobile | H: less abandonment, same selections | Filter usage rate, scroll depth | Filter diversity | Keep if usage is flat-or-up |
| E4 | Direction A headline | H: more first-impression trust | 5 interviews: "would you send your CV here?" | Comprehension | Keep if ≥4/5 positive and comprehension holds |
| E5 | Guided 3-question filter (opt-in) | H: completed users reach `/services` more | Completion → `/services` rate | Board usage | Ship behind a link, not a gate |

**Duration rule:** [EVIDENCE] at this traffic, each of these needs **≥ 4 weeks** of data before a before/after comparison means anything, and the report must state the visitor counts. Below ~200 board views per month, prefer interviews and usability tests over waiting for numbers.

---

# PART VIII — Feasibility and phased roadmap

## VIII.1 Technical facts

[OBSERVATION] Static HTML/CSS/JS, no build step, no framework, no `package.json`. Page styles are inline per file. One serverless function (`api/subscribe.js`). Python pipeline on GitHub Actions. GoatCounter only. Everything below is **frontend-only**; none of it needs a backend, a database or a new vendor.

**Constraint that governs the whole roadmap:** `tests/test_site_monitor.py`, `scripts/site_monitor.py` and `scripts/site_config.py` read `index.html`, `services.html` and `verify.html` by regex. Any markup change must keep the strings those checks look for, or be accompanied by a test change. This is a real risk to the pricing block, the WhatsApp number, the price list, the free-check block and the TEST banner.

## VIII.2 Roadmap

| Phase | Item | Effort | Dependency | Done when |
|---|---|---|---|---|
| **0 — connect** | Move services block above listings on `/` | ~2 h | KT approval; monitor/test safety | `python3 -m unittest discover -s tests` passes; monitor passes locally |
| 0 | Link `/free-check` → `/services` | ~30 min | KT approval | Link present, monitor unaffected |
| 0 | `/order` back-link to `/services` | ~15 min | KT approval | Present |
| **1 — measure** | Named events for the taxonomy (§VII.2) | ~2 h | KT approval | Events fire in preview |
| 1 | Free-check log spreadsheet + KT habit | KT's time | None | 10 rows with source/role/country/outcome |
| **2 — discover** | Collapse field filters on mobile | ~3 h | None | Usability test at 360px |
| 2 | Header service link on all pages | ~1 h | None | Present on 8 pages |
| **3 — position** | Direction A headline test | ~2 h | Interviews | 5 interviews run |
| 3 | `/verify` linked from header | ~30 min | None | Present |
| **4 — validate** | 5 problem interviews with free-check users | KT's time | Rows in the log | Notes in `drafts/research/` |
| 4 | Decision on contextual in-feed offer | — | Interview evidence | Decision doc |
| **later — gated** | Any pricing change, new package, paid micro-product, Whop go-live, in-feed offer | — | Explicit KT approval + evidence | Separate decision doc |

**Deliberately not on the roadmap:** a backend, accounts, a database, a second payment processor, any gating of listings, any new vendor.

## VIII.3 Risks

1. **Regex-coupled tests break on markup edits.** Mitigation: run the suite after every change; treat failures as real.
2. **Long home page.** Moving the services block above listings makes the page longer still. Mitigation: shorten the board to 20 listings per page with a visible "Load more" — but this changes behaviour, so it needs its own approval. [INFERENCE]
3. **Scope creep into a redesign.** The brand is approved; the voice is approved. This roadmap changes *order and connection*, not identity.
4. **Zero-data decisions.** Every recommendation above that is not marked [OBSERVATION] is provisional until the free-check log has rows.

---

# PART IX — Final recommendation, evidence table

## IX.1 The recommendation in one paragraph

Keep the free board completely free and keep it honest; make the paid services *discoverable* rather than persuasive. The business does not currently have a conversion problem — it has a **connection problem**: the free value and the paid offer live on islands. Fix the bridges first (three small changes), instrument the funnel you already have, and treat the 50 free CV checks as the willingness-to-pay research they already are. Only then decide, on evidence, whether to add contextual offers, a paid micro-product, or new packages.

## IX.2 The first three changes

1. **Move the paid-services block above the listings on the home page.** Today it sits at y≈24,500 of 26,284px on mobile and 1,573px below the fold on desktop.
2. **Add a link from `/free-check` to `/services`** (the warmest lead in the product currently dead-ends), plus a back-link on `/order`.
3. **Collapse the mobile field filter** behind a disclosure control showing the active count, keeping every filter and combination intact.

All three are presentation changes. None touches classification, data, prices, wording rules or the trust promise.

## IX.3 Assumptions to validate

- That mid-career cross-border applicants are the paying customer (the PROPOSED ICP).
- That visitors will pay $29–$149 for a human-written CV when AI rewriting is free.
- That the eligibility framing attracts rather than repels.
- That the free check converts at a rate worth continuing.

## IX.4 Tactics to avoid

Gating listings · progressive "half the information then pay" paywalls · fake urgency or scarcity · testimonials before real customers exist · raising prices without data · a founder name or photo (forbidden by KT) · any claim that could not survive `site_monitor.py` · treating more clicks as success.

## IX.5 External feedback disposition (Arshia, 26 Oct — n=1)

| Note | Disposition | Reason |
|---|---|---|
| "AI-default design lowers trust" | **Accepted in part** | Trust here is earned by proof (source, date, last-checked, correction promise), not decoration. Do not add gradients. |
| Step-by-step mobile filtering | **Accepted in modified form** | Progressive disclosure of the *existing* filters; plus an opt-in 3-question guided path. A wizard on arrival would gate free value — rejected. |
| Salary-range filter | **Rejected for now** | `salaryText` is free text ("Not stated" in many rows); a numeric range needs a pipeline change and would display false precision. [INFERENCE] |
| Cards too populated / buttons / icons | **Mostly done; icons accepted** | Cards were rebuilt this session. Text-labelled icons for location/date/type are low-cost and acceptable. |
| Payment hook placement | **Accepted as the top finding** | Measured: services block at y≈24,500 on mobile; `/free-check` has no services link. See §I.2. |
| Small-pay micro-products | **Logged, gated** | Compatible with the rules if gated content is a *preview*, not a listing. Needs KT's approval and validation first. |

---

## Evidence table

| # | Claim | Class | Source | Confidence | How to validate |
|---|---|---|---|---|---|
| 1 | Services block is below all 40 listings on mobile | Measured | `preview_audit.py`, 26 Oct 2026: home 26,284px, block at y≈24,500 | High | Re-run the script |
| 2 | `/free-check` links to neither `/services` nor `/order` | Measured | `free-check.html` source, 26 Oct | High | grep |
| 3 | Seeker-paid remote boards are the exception | Competitor observation | Live site pricing pages, 26 Oct (research strand C) | Moderate | Repeat quarterly |
| 4 | Diagnosis-then-cure is the dominant CV-product pattern | Competitor observation | Teal / Rezi / Huntr / LinkedIn pricing pages, 26 Oct | Moderate | Repeat quarterly |
| 5 | A/B testing is impractical at this traffic | Established | Sample-size formula 16σ²/δ²; Evan Miller / Optimizely docs | High | n/a |
| 6 | Design quality is a primary credibility cue | Established | Stanford Web Credibility Project (Fogg, 2002) | Moderate | 5-interview test |
| 7 | Choice overload evidence is contested | Established | Iyengar & Lepper 2000 vs Scheibehenne et al. 2010; Greifer & Sugiyama 2023 | High | E3 experiment |
| 8 | Loss aversion applies to mixed gains/losses, not riskless choices | Established | Kahneman & Tversky 1979; Tversky & Kahneman 1991 | High | n/a |
| 9 | IKEA effect requires completion and competence | Established | Norton, Mochon & Ariely 2012 | High | H2 test |
| 10 | Social proof can backfire | Established | Cialdini et al. 2009 "defensive attribution" | High | n/a — do not fabricate testimonials |
| 11 | No purchase event exists in analytics | Measured | `index.html` GoatCounter wiring, 26 Oct | High | grep for `data-*` events |
| 12 | `yearsExperienceMin` present on 638/1,002 rows | Measured | `jobs.json` analysis, 26 Oct | High | Re-run |
| 13 | Markup edits risk breaking regex-based monitor/tests | Inference | `scripts/site_monitor.py`, `tests/test_site_monitor.py`, `tests/test_site_config.py` | High | Run the suite after any edit |
| 14 | The free CV check is the only structured WTP research available | Inference | Funnel audit; KT's reported single conversion | Moderate | Build the log; re-assess after 10 rows |

---

## What was actually done to produce this report

- Repository inspected: `index.html`, `services.html`, `verify.html`, `free-check.html`, `order.html`, `thanks.html`, `site-config.js`, `site-forms.js`, `api/subscribe.js`, `jobs.json` (1,002 rows), `platforms.json`, `scripts/`, `tests/`, `.github/workflows/`.
- Local preview rendered and screenshotted at desktop, tablet and 360px mobile; page heights, fold positions and element geometry measured with a headless browser (`preview_audit.py`).
- Live production `jobs.json` compared with the local copy.
- Four parallel research strands: behavioural evidence, CV-product freemium/pricing, job-board monetisation and substitutes, and low-traffic validation methods.
- 159 Python tests run (pre-existing state).
- **No site code, prices, copy, data, tests or configuration were modified.** Only `drafts/master-prompt-business-conversion.md` and this file were created.
