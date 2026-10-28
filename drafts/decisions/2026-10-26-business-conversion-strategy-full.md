# Yireh Careers — Business & Conversion Strategy

Status: **PROPOSED** · Written 26 Oct 2026 · Buffy (Claude Code) for KT
Master prompt: `drafts/master-prompt-business-conversion.md`
Deliverable of the master prompt. **Research and planning only — no implementation, no commits, no deploys.**

**How to read the labels:** `[ESTABLISHED]` measured here or cited from a named source · `[OBSERVATION]` seen on the live site or in the repo on 26 Oct 2026 · `[INFERENCE]` reasoned conclusion · `[HYPOTHESIS]` must be tested before it is believed · `[POPULAR-INTERPRETATION]` widely repeated marketing belief, weak or contested evidence · `[COMPETITOR-OBSERVATION]` seen on a competitor's live page, dated · `BLOCKED-KT` a number only KT can supply.

This report **supersedes** the earlier partial `2026-10-26-business-and-conversion-strategy.md` (Parts I–III, IX). It is the complete deliverable and corrects two claims in that draft (see Part IX, "corrections").

---

## Part I — Executive diagnosis

### I.1 Strengths (preserve all of these)

1. **A differentiated product truth** `[OBSERVATION]`. Every listing is classified confirmed-remote / restricted / not-confirmed, and eligibility is shown in the employer's own words. This is the one thing no competitor in this price and size class does as a primary feature. It is expensive to copy honestly.
2. **A four-layer quality system** `[OBSERVATION]` unusual for a solo product: unit tests (159), classifier-independent QA rules in every refresh (`scripts/qa_checks.py`), a live-site monitor every 3h (`scripts/site_monitor.py`), and a manual spot-check (`scripts/spot_check.py`).
3. **Honest money** `[OBSERVATION]`: no applicant fees, no commission-only roles, no invented salaries, no "no work permit needed" / "guaranteed". Enforced by tests, not by intention.
4. **A complete, priced, deliverable service ladder** with delivery times, add-ons, and a free diagnostic (`drafts/decisions/2026-10-18-pricing-and-offer-structure.md`, `2026-10-25-delivery-times-and-essential-wording.md`).
5. **A conversion event taxonomy that already exists** `[OBSERVATION]`: `apply-click`, `cv-click-*`, `services-click-*`, and — importantly — `conversion-check` and `conversion-order` fired by `site-forms.js`. The funnel is more measurable than a site this size usually is.

### I.2 The commercial problem, in measured facts

- **Mobile home page is 26,284px tall.** The paid-services block sits at **y ≈ 24,500px — below all 40 rendered listings** `[OBSERVATION]` (`preview_audit.py`, 26 Oct). A visitor scrolls ~68 phone-screens past free value to reach one paid offer.
- On desktop the services block sits **1,573px below a 900px fold** `[OBSERVATION]`.
- **`/free-check` links to neither `/services` nor `/order`** `[OBSERVATION]`. Its only cross-links are `/privacy` and WhatsApp. This is the warmest page in the product and it dead-ends.
- **`/order` links back only via the wordmark** `[OBSERVATION]`.
- **Diagnosis** `[INFERENCE, high]`: this is a **connection** problem, not a persuasion problem. Three islands — browse → free check → order — with no bridges. Copy tests cannot matter until the bridges exist.

### I.3 What is genuinely unknown

`BLOCKED-KT` — no traffic, conversion, or revenue baseline exists for this analysis. `BLOCKED-KT` — no order history, refund history, buyer countries, or WhatsApp enquiry volume. Consequences: (1) `jobs.json` is 251 KB gzipped and fetched on every board load `[OBSERVATION]`, so mobile load cost is real but its *business* impact is unmeasured; (2) the ICP hypothesis is unvalidated; (3) whether the free CV check converts is a single anecdote (one convert reported by KT).

### I.4 Five highest-priority opportunities

| # | Opportunity | Class | Evidence | Effort |
|---|---|---|---|---|
| 1 | **Bridge the funnel**: move services block above listings on home; link `/free-check`→`/services`; back-link `/order` | `[INFERENCE]` | Direct measurement | ~2 h |
| 2 | **Instrument + harvest the free CV check** as the willingness-to-pay research it already is | `[INFERENCE]` | Concierge MVP already running | KT's time |
| 3 | **Make eligibility the headline**, not a card detail | `[INFERENCE]` | Positioning gap | ~1 day |
| 4 | **Fix mobile filter discovery** (progressive disclosure, not a wizard) | `[OBSERVATION]` | 65+ chips in a scroller | ~3 h |
| 5 | **Report the existing funnel** — 15+ events fire but nothing reads them | `[OBSERVATION]` | Events in code | 30 min/week |

### I.5 Decisions that need more evidence before acting

Whether contextual in-feed offers raise or destroy trust (interview first); whether years-of-experience filtering is wanted (`yearsExperienceMin` on 638/1,002 rows); whether a paid micro-product fits the trust promise; which positioning direction wins; any price change.

---

## Part II — Behavioural research, freemium evidence, competitor analysis

### II.1 Behavioural principles (evidence → relevance → implication → limitation → contrary → hypothesis)

**Loss aversion** `[ESTABLISHED]`. Kahneman & Tversky (1979) prospect theory; Thaler (1980) mental accounting. Losses weigh ~1.5–2.5× equivalent gains in mixed choices. *Relevance:* someone who has *received* a free CV check holds something to lose. *Implication:* show the user their own received result, don't just describe a future one. *Limitation:* lab-based; the ratio does not generalise cleanly to field marketing. *Contrary:* Tversky & Kahneman (1991) found loss aversion **absent** in riskless gain-only choice. *Hypothesis H1:* a "your report is ready" surface converts better than a brochure description.

**Effort justification / IKEA effect** `[ESTABLISHED]`. Norton, Mochon & Ariely (2012): people value things more after assembling them, **but only when assembly completes and they feel competent**. *Relevance:* a free tool producing a personalised artefact should beat static copy. *Limitation:* studied on physical/design assembly; generalising to "answered 3 filter questions" is weak. *Contrary:* the effect **disappears** for incomplete or unskilled assembly. *Hypothesis H2:* a tool generating a personalised eligibility summary raises WhatsApp clicks more than the same text shown statically.

**Endowment effect** `[ESTABLISHED]`. Thaler (1980); Kahneman, Knetsch & Thaler (1990). People value owned/obtained items more. *Relevance:* the diagnostic result is "theirs". *Limitation:* strongest for objects, weaker for services. *Hypothesis:* framing the check output as the user's own artefact increases follow-through.

**Commitment & consistency** `[ESTABLISHED]`. Cialdini; Freedman & Fraser (1966) foot-in-the-door. *Relevance:* a small voluntary commitment (3-question guide) can raise later action. *Limitation:* effect sizes vary by context; classic studies are donations/door-to-door. *Hypothesis H3:* users who complete the guide reach `/services` more than browsers.

**Social proof** `[ESTABLISHED]` but **practically unusable now**. Descriptive norms act under uncertainty. *Contrary:* Cialdini et al. (2009) defensive attribution — descriptive norms can **backfire**. *Constraint:* no testimonials may be invented, and none exist yet. *Action:* only after real, consented customer quotes exist.

**Choice overload** `[POPULAR-INTERPRETATION — contested]`. Iyengar & Lepper (2000): 24–30 options cut selection. **But** Scheibehenne et al. (2010) meta-analysis found a near-zero average effect; Greifer & Sugiyama (2023) found people often prefer *more* choices. *Relevance:* 65+ field chips on mobile. *Implication:* collapse for *findability*, not on the belief that fewer choices boost conversion. *Hypothesis H5:* a disclosure control with a visible count ("65 fields") keeps selection rate flat but reduces abandonment. Measure before/after.

**Present bias / urgency** `[ESTABLISHED]` hyperbolic discounting — **not usable here**. Arbitrary deadlines are forbidden by this project's own rules and are discounted by users anyway. No experiment proposed.

**Trust / web credibility** `[ESTABLISHED]`. Stanford Web Credibility Project (Fogg, 2002): design quality, information currency and verifiability are top cues. *Relevance:* strongest academic support for the UI work itself; Yireh is an unknown brand where design cues matter most. *Limitation:* 2002, self-report. *Hypothesis H6:* first-impression interviews improve after the refinement.

**Transparency effects** `[ESTABLISHED]`. Voluntary disclosure (source, date, last-checked, correction promise) builds trust; forced disclosure under suspicion backfires. *Relevance:* this is Yireh's core asset and it should be *mobilised as a conversion asset*, not merely present.

### II.2 Freemium / paywall survey `[COMPETITOR-OBSERVATION]`, live pages 26 Oct 2026

Pattern across CV products: **free is a scan / limited build / limited download; paid is the export or the human; the trigger appears only after the user has invested effort** — never before. This is the single most transferable pattern.

### II.3 Competitor comparison (prices dated 26 Oct 2026)

| Competitor | Free | Paid | Price (observed 26 Oct) | Trigger | Mobile UX | What it teaches |
|---|---|---|---|---|---|---|
| Teal (tealhq.com) | Scan, limited resumes | Full toolkit | Subscription, tiered | After a scan shows a gap | Good | Sell diagnosis, then cure |
| Rezi (rezi.ai) | Limited resumes | AI rewrite, subscription | Monthly/annual | After building | OK | Effort-then-offer |
| Resume.io | Very limited | Aggressive "trial"→recurring | Low headline then recurring | At download | Pushy | **Avoid** — industry trust sink |
| Huntr (huntr.co) | Job tracker | Career suite | Monthly | After tracking jobs | Good | Attach offer to the search |
| Kickresume | Limited | Subscription | Monthly | At download | OK | Template-led |
| Zety / ResumeGenius | Preview | Per-download "trial" | Low headline, recurring | At download | Aggressive | Deceptive pattern to avoid |
| LinkedIn Premium Career | Profile free | Premium | Monthly | At apply/viewing profile | Native | Offer at the application moment |
| FlexJobs | Nothing (gated listings) | Subscription | Weekly/annual | Up-front | OK | **Anti-pattern** for us — gating listings kills the differentiator |
| Remote OK / WWR / Working Nomads / Himalayas | Full board free | Employer-side / ads | n/a | n/a | OK | Seeker-paid boards are the **exception** |

**Substitutes** `[COMPETITOR-OBSERVATION]`: AI rewriting (ChatGPT/Canva — near-zero cost, unverifiable quality); freelance CV writers on Fiverr/Upwork (commonly well below $29, wide variance); free institutional help (university career services, government/NGO employment services — free, often slow and geographically bound).

**Key inference** `[INFERENCE, high]`: Yireh cannot win on price against any substitute and must not try. It can only win on **specificity** — a CV written for the roles and countries the person can actually work in, plus eligibility judgement no gig writer offers. If `/services` reads "we write CVs", it loses to Fiverr on price and ChatGPT on speed. If it reads "we make your CV work for remote roles open to where you can legally work", it competes with neither. **This drives the positioning in Part V.**

*Never infer profitability from the existence of a paid product.* No competitor's revenue is known.

---

## Part III — Segments, JTBD, free/paid allocation, five-model comparison

### I.1 Jobs to be done
Functional: *"Help me find work I can actually do from where I am, and help me get it."* Emotional: *"Stop feeling like I'm applying into a void."* Social: *"Look like a serious candidate."*

### III.2 Segments

| Segment | JTBD intensity | WTP | Cost to serve | Verdict |
|---|---|---|---|---|
| Active mid-career cross-border applicants (the PROPOSED ICP) | High | Hypothesised moderate–high | Moderate | **Primary — `[HYPOTHESIS]`, validate via free-check log** |
| Early-career / graduates | High, price-sensitive | Low | High | Audience-building only (correct current policy) |
| Executives | Very high | High | Very high | Inbound only; do not build for |
| Casual browsers | Low | Very low | Low | Serve free + email capture |
| Career changers / freelancers | Moderate | Moderate | Moderate | Secondary; a landing page later, not now |

**Challenge to the ICP** `[INFERENCE]`: the PROPOSED strategy doc itself flags the tension — professional resume help is used by only **3.7%** of US adults (Novoresume 2026, a seller, so indicative), AI substitution is strongest among the young, and Yireh's **own channels may be student-heavy** (KT's stated assumption). So "experienced professionals are the paying customer" is plausible on budget and AI-substitution grounds but **contradicted by the likely channel composition**. This is the top thing to resolve, and it resolves in the free-check log and 10 interviews, not in analysis.

### III.3 Free/paid boundary — recommendation

> **Free forever: everything that helps a person decide where to apply. Paid: everything that helps them win the application.**

| Free, ungated | Paid |
|---|---|
| Every listing, source link, eligibility label, date | Essential $29 / Professional $49 / Executive $149 |
| Search, all filters, "new this week" | LinkedIn packages; Growth $99/mo |
| How we verify + correction promise | Add-ons |
| Weekly digest + tips (with consent) | Interview sheet $29 |
| **One free CV check per person** | Everything after the diagnostic |

**Rejected:** gating listings (destroys the differentiator; every competitor gives listings free); "half the info then pay" progressive gating (violates the project's rules *and* commercial sense — the free eligibility info *is* the reason to visit); hard paywalls; fake scarcity/countdowns.

### III.4 Five-model comparison (scored 1–5, 5 = best for Yireh now)

| Criterion | A. Free discovery + paid services | B. Free + contextual offers | C. Freemium tools + upgrades | D. Premium job features | E. Service-led hybrid |
|---|---|---|---|---|---|
| Revenue potential | 3 | 4 | 3 | 2 | 4 |
| Acquisition | 4 | 4 | 4 | 3 | 3 |
| Trust risk (lower=better) | 4 | 3 | 3 | 2 | 4 |
| Implementation effort (higher=fit) | 5 | 4 | 2 | 2 | 3 |
| Support burden (higher=fit) | 4 | 4 | 2 | 3 | 3 |
| Repeat purchase | 3 | 4 | 3 | 2 | 4 |
| Mobile conversion | 3 | 4 | 3 | 3 | 3 |
| Solo-operability | 5 | 4 | 2 | 3 | 3 |
| **Total** | **31** | **31** | **22** | **21** | **27** |

**Primary model: A (free discovery + paid career services), with B layered as the delivery mechanism** — contextual offers are *where* model A's offer is placed, not a separate business. **Fallback: E (service-led hybrid)** if interviews show buyers want bespoke/longer programmes. **Switch conditions:** if 10+ interviews show willingness for guided tools with a paid export, move toward C; if board traffic is real but conversion stays ~0 after bridging, the problem is the offer, not the funnel — revisit with E; if traffic never materialises, no model works and the lever is distribution, not monetisation.

### III.5 Candidate offers (trigger → problem → value given free → offer → copy → objection → risk → validation)

| Trigger | User problem | Free value given | Paid offer | Copy/CTA | Objection | Disruption risk | Validation |
|---|---|---|---|---|---|---|---|
| Read 3+ listings | "Which of these can I actually get?" | Full eligibility labels | Free CV check | "Applying to roles like these? Get three specific fixes to your CV, free." | "Is it a sales trap?" | Low | Log source + outcome |
| Clicks "Get a CV for this role" | "My CV isn't tailored" | The job + its eligibility | Essential/Professional | "Get a CV for this role →" (WhatsApp, prefilled) | "Price" | Low | Event `cv-click-*` exists |
| Completes free check | "Now what?" | Three fixes | Any package | "Ready for a full rewrite? See the packages." | "More cost" | Low | `/free-check`→`/services` link |
| Orders | Needs delivery | — | Order form | `/order?package=` | Trust | None | `conversion-order` exists |

**Hard paywalls are the wrong answer here** — stated plainly. Monetise delivered value, never manufactured frustration.

---

## Part IV — Architecture, navigation, service discovery, paywall logic

### IV.1 Sitemap (static Vercel routes)

```
/                 home: hero → free/paid line → SEARCH+FILTERS → listings
                  (services block MOVED above listings)
/services         packages, prices, delivery, add-ons, Growth, free-check entry
/verify           how we verify (link from header — currently not in nav)
/privacy          (exists)
/free-check       free diagnostic
/order            order details (noindex)
/thanks           post-submit (noindex)
/subscribed       (exists)
/kit /mail        unlisted, noindex (must stay out of nav — tests enforce no analytics on /kit)
```

**No new top-level pages needed.** A separate `/pricing` page would duplicate `/services` and add monitoring burden for no discovery gain `[INFERENCE]`. Individual service pages and an FAQ are optional later; the FAQ content belongs on `/services` today.

### IV.2 Navigation

- **Desktop header:** Jobs · Free CV check · Services · How we verify · [Get a CV] (blue button).
- **Mobile header:** same items in the existing menu; the primary action must be reachable without opening the menu `[OBSERVATION]` — currently "Get Job-Ready" is in the hamburger, which is a discoverability cost.

### IV.3 Service-discovery map (global vs contextual)

| Element | Global / Contextual | Status today |
|---|---|---|
| Header link to `/services` | Global | **Missing** |
| One-line free/paid statement above the fold | Global | **Missing** |
| Services block on home | Contextual | Present but at y≈24,500 mobile — too low |
| "Get a CV for this role" per card | Contextual | Present, good; event exists |
| Post-diagnostic "see the packages" | Contextual | **Missing** (`/free-check` has no `/services` link) |

**Mobile service discoverability, solved directly:** (1) put a compact service block above the listings, not below; (2) one header-level action; (3) keep the per-card button; (4) add the post-diagnostic link. A sticky CTA is optional and **must be ≤56px, dismissible, and must not overlap the per-card WhatsApp button** `[OBSERVATION]` — on a 360px screen `.sticky-wa` and card buttons compete for the same pixels.

### IV.4 Conversion-point map and offer logic (ASCII)

```
LAND (home)
  │  free value: search + filters + eligible labels
  ├─► [services block, above listings] ──► /services ──► /order ──► WhatsApp order
  │                                              ▲
  ├─► card "Get a CV for this role" ──► WhatsApp ┘
  └─► /free-check (diagnostic) ──► 3 fixes ──► [NEW: /services link] ──► /order
Offer logic:  browse N listings → free check → packages → order. NO paywall anywhere.
```

### IV.5 SEO dependencies
OG tags and canonical exist `[OBSERVATION]`. JobPosting structured data is an **open question** — Google's current rules for listings you do not own must be checked before adding it (already a Claude open item in `drafts/kt-todo.md`). Not recommended in this report; flagged, not resolved.

---

## Part V — Landing page and copy

### V.1 Two positioning directions

**A — "The eligibility expert."** *"Know whether a remote job is actually open to you — before you spend an evening on the application."* Distinctive, ownable, and makes the paid offer coherent (eligibility uncertainty is exactly what a CV can fix). Trade-off: "eligibility" may not be the words stressed seekers use — needs a 5-person test. **Recommended.**

**B — "The honest job finder."** *"Real remote jobs, checked daily, restrictions shown."* Immediately legible, closest to current copy. Trade-off: indistinguishable from other honest boards; services look bolted on.

**Chosen: A, expressed with B's plainness** `[INFERENCE, high]`. It is the only claim competitors don't make, it justifies the paid services, and it matches the trust rules. Risk mitigated by interview testing the phrase.

### V.2 Page-by-page content plan + real draft copy

Voice per `drafts/voice-and-copy-guide.md`: contractions, bottom line first, one next step, warm and plain, no hype, no guarantees, no founder name/face, sign as "the Yireh Careers team".

**Home — hero**
> **Remote jobs, with the restrictions shown.**
> Every listing links to the employer's own posting, carries its real posting date, and says plainly who can apply — "worldwide", a named region, or "eligibility unclear". Nothing is dressed up as open to you when it isn't.
> *[Search jobs]* · *[How we verify]*

**Home — free/paid line (new, directly under hero)**
> The job board is free, and it stays free. When you've found the right role, our paid CV and LinkedIn services help your application read like it belongs there. [See the packages](/services)

**Services — opening**
> You've already done the hard part: knowing which jobs are worth your evening. These packages are the rest — a CV, and a LinkedIn profile if you want it, written for the roles you're actually applying for, wherever you can legally work.

**Free CV check — new closing block (the missing bridge)**
> **Ready for a full rewrite?**
> If you'd rather we did the whole thing, [see what each package includes](/services). Essential is $29 and lands within 2 working days of getting your details.

**Card microcopy (keep the WhatsApp prefill, tighten label):** `Get a CV for this role →`

**Do not write** (enforced by `scripts/site_monitor.py` + tests): "guaranteed", "no work permit needed", "the only job board", any promise to continue until a number is reached, any outcome claim, any "for students/graduates" claim about a role.

---

## Part VI — Service packages, pricing, checkout, onboarding, trust, refunds

**Pricing: do not change.** `[INFERENCE]` The ladder was approved 18 Oct with delivery times 25 Oct. There is **zero** willingness-to-pay data, so any change is a coin flip. One structural note worth *testing later*: the $49→$149 gap is large with only a $15 add-on between; a middle option is a hypothesis, not a change to make now.

**The free CV check is the offer engine** `[INFERENCE]`: it is the only free diagnostic, it is well-written, and it is invisible from every other page. Link it from the header and `/services`; log every check (source, target role, target country, blocker, ordered y/n).

**Checkout:** WhatsApp (card checkout built but **OFF**; Whop-only; keep off until the go-live checklist and KT's explicit approval). Onboarding friction — emailing the CV — is real but small; reuse `/free-check`'s privacy explanation on `/services` so the objection is handled before it forms.

**Undecided terms (flagged, not invented):** refund and cooling-off terms were approved in the pricing doc but the free-check and Executive terms should be reviewed by a qualified adviser before a company is registered (`drafts/kt-todo.md`). This is a **decision for KT**, not a gap to fill with invented copy.

**Trust:** mobilise `/verify` (four-layer quality system, correction promise) as a conversion asset on `/services` — it answers "why pay these people?" better than testimonials would, and no testimonials may be invented.

---

## Part VII — Analytics and experiments

### VII.1 Current taxonomy `[OBSERVATION]`
Already firing: `apply-click`, `cv-click-*`, `services-click-hero/mid/sticky/final-free-check`, `services-click-pricing-essential/professional/executive`, `services-click-addons`, `services-click-growth`, and **`conversion-check` / `conversion-order`** (`site-forms.js`). *Correction to my earlier draft: the funnel events largely exist; what's missing is reading them, plus a `services-view` page-view event and job-engagement depth.*

### VII.2 Extend (same naming style)
Add: `services-view`, `search-used`, `job-open` (listing link out), `guide-complete` (if the 3-question guide ships), `wa-click` (generic).

### VII.3 Metric classes
- **Primary outcomes:** `conversion-order`, `conversion-check`, `apply-click`.
- **Diagnostic:** `services-view`, `cv-click-*`, `services-click-*`, `search-used`, `job-open`.
- **Guardrails (trust):** report-a-listing rate, unsubscribe rate, QA pass rate, `removed.log` volume, apply-click rate (a monetisation change that cuts applications has failed), `jobs.json` load size.

### VII.4 Funnel definitions
visitor→`services-view`; `services-view`→`conversion-order`; visitor→`conversion-check`; `conversion-check`→order within 30 days (tracked in the free-check log, not analytics); application CTR (`apply-click`/visitor).

### VII.5 Experiment roadmap (interviews/usability/pre-sales beat A/B here)

`BLOCKED-KT`: no baseline traffic exists. Sample size for an A/B test scales as `16·σ²/δ²` per variant; at an unmeasured, likely few-hundred-visitors/month level, any realistic effect needs a multi-year test. **State plainly: A/B testing is not available. Use sequential before/after with ≥4 weeks and reported counts, plus interviews.**

| # | Change | Hypothesis | Primary | Guardrail | Decision rule |
|---|---|---|---|---|---|
| E1 | Services block above listings | service CTR rises from ~0 | `services-view`/board view | apply-click flat | keep if apply-click flat & services-view up |
| E2 | `/free-check`→`/services` link | warm leads continue | `/services` from `/free-check` | check completion flat | keep unless completion drops |
| E3 | Collapse mobile fields | less abandonment, same selections | filter usage | filter diversity | keep if usage flat/up |
| E4 | Direction A headline | more first-impression trust | 5 interviews | comprehension | keep if ≥4/5 positive |
| E5 | 3-question guide | completers reach `/services` more | guide→`/services` | board usage | ship as opt-in, never a gate |

**Report numbers as counts** ("3 enquiries from 120 visits"), never as trends, until volume exists.

---

## Part VIII — Technical & operational feasibility

**Framework:** static HTML/CSS/JS, no build step, no `package.json`. Page styles inline per file. One serverless function `api/subscribe.js`. Python pipeline on GitHub Actions. **All Part IX recommendations are `FRONTEND-STATIC`** except analytics wiring (`THIRD-PARTY-CONFIG`, GoatCounter already configured) and the free-check log (`NEW-OPERATIONS`, KT's spreadsheet).

**Measured facts** `[OBSERVATION]`: `index.html` 65 KB (inline CSS ~29.6 KB, inline JS ~21.7 KB); `services.html` 83 KB; **`jobs.json` 1.8 MB raw / 251 KB gzipped, fetched on every board load** (`fetch('./jobs.json')` at `index.html:1249`); 40 cards per page (`PAGE_SIZE = 40`, "Show more"). The 251 KB fetch is the main mobile-performance cost and a real, if unquantified, conversion risk on slow connections.

**Maintenance debt** `[OBSERVATION]`: single-file inline CSS/JS with no component system; `scripts/site_monitor.py` and `tests/test_site_monitor.py`/`test_site_config.py` **parse pages by regex**, so any markup edit can break them (real risk to the pricing block, WhatsApp number, free-check block, TEST banner). `tests/node` exists without a package.json. Any implementation session must run `python3 -I -m unittest discover -s tests` (159 tests) after every markup change and treat failures as real.

**Privacy/GDPR:** forms use fixed, tested consent wording; privacy-page changes need KT approval; the signup is single opt-in (KT's decision, pending double-opt-in decision D-11). No recommendation here touches consent.

**Delivery capacity:** KT delivers by hand; Essential ~3.5h, Professional ~7h, Executive ~18h (estimates, unvalidated). Any offer that increases volume must respect this solo capacity — a reason to favour the diagnostic-then-package funnel over high-volume low-ticket products.

---

## Part IX — Final recommendation, free-to-paid boundary, first three changes

### IX.1 Recommendation
Keep the board completely free and honest; make the paid services **discoverable**, not intrusive. This is a **connection problem**, not a persuasion problem. Bridge the three islands, harvest the free CV check as willingness-to-pay research, and only then decide — on evidence — about contextual offers, a paid micro-product, or new packages.

### IX.2 Free-to-paid boundary
Free = decide where to apply. Paid = win the application. Listings and apply links never gated.

### IX.3 First three changes (implementation-ready)

**Change 1 — move the services block above the listings on home.**
- *File:* `index.html` (the services `<section>` and the listings container).
- *Copy:* unchanged; the free/paid one-liner from Part V.2 added above the listings.
- *Acceptance:* services block renders above `.job-list`/results container; all 15+ events still fire; `python3 -I -m unittest discover -s tests` passes; `services-click-*` and `conversion-*` events unchanged in name.

**Change 2 — bridge `/free-check` and `/order`.**
- *File:* `free-check.html` — add a link to `/services` after the "Next: email us your CV" block (copy in Part V.2). *File:* `order.html` — add a "back to packages" link to `/services`.
- *Acceptance:* both links present; no change to form behaviour, consent wording, or `conversion-check`/`conversion-order` events; brand test still passes.

**Change 3 — collapse the mobile field filter behind a disclosure control.**
- *File:* `index.html` (Fields group + media query).
- *Acceptance:* every filter and combination preserved; disclosure shows active count; keyboard-accessible with correct expanded state; `filter-field` event still fires; verified at 360px with no horizontal-scroll-dependent control.

### IX.4 Assumptions to validate
Mid-career cross-border applicants are the paying customer (vs. student-heavy channels) · visitors will pay $29–149 when AI rewriting is free · eligibility framing attracts rather than repels · the free check converts.

### IX.5 Tactics to avoid
Gating listings · "half info then pay" · fake urgency/scarcity · invented testimonials · price changes without data · founder name/photo · any claim that fails `site_monitor.py` · treating clicks as success.

### IX.6 Corrections to the earlier partial draft
1. **"No service-discovery event exists"** was wrong — 15+ events including `conversion-check`/`conversion-order` already fire. The gap is *reading* them, plus a `services-view` page event.
2. **Mobile payload** was unstated; measured at 251 KB gzipped for `jobs.json` per board load.

---

## Evidence table

| # | Recommendation / claim | Source link | Class | Confidence | Validation |
|---|---|---|---|---|---|
| 1 | Services block below all listings on mobile (y≈24,500 of 26,284px) | `preview_audit.py`, 26 Oct | `[OBSERVATION]` | High | Re-run script |
| 2 | `/free-check` has no `/services` link | `free-check.html` source | `[OBSERVATION]` | High | grep |
| 3 | Seeker-paid remote boards are the exception | Live boards, 26 Oct | `[COMPETITOR-OBSERVATION]` | Moderate | Re-check quarterly |
| 4 | Diagnosis-then-cure dominates CV products | Teal/Rezi/Huntr/LinkedIn, 26 Oct | `[COMPETITOR-OBSERVATION]` | Moderate | Re-check quarterly |
| 5 | A/B testing impractical at this traffic | 16σ²/δ²; Evan Miller/Optimizely | `[ESTABLISHED]` | High | n/a |
| 6 | Design quality is a primary credibility cue | Stanford Web Credibility Project (Fogg 2002) | `[ESTABLISHED]` | Moderate | 5-interview test |
| 7 | Choice overload evidence contested | Iyengar & Lepper 2000 vs Scheibehenne 2010, Greifer 2023 | `[ESTABLISHED]` | High | E3 |
| 8 | Loss aversion absent in riskless choice | Tversky & Kahneman 1991 | `[ESTABLISHED]` | High | n/a |
| 9 | IKEA effect needs completion + competence | Norton, Mochon & Ariely 2012 | `[ESTABLISHED]` | High | H2 |
| 10 | Social proof can backfire | Cialdini et al. 2009 | `[ESTABLISHED]` | High | n/a — no fake testimonials |
| 11 | 15+ conversion events already fire | `index.html`, `site-forms.js` | `[OBSERVATION]` | High | Read GoatCounter `BLOCKED-KT` |
| 12 | `jobs.json` = 251 KB gzipped per board load | `gzip -c jobs.json`, 26 Oct | `[OBSERVATION]` | High | Re-measure |
| 13 | Markup edits risk breaking regex monitor/tests | `scripts/site_monitor.py`, `tests/*` | `[INFERENCE]` | High | Run suite after any edit |
| 14 | Professional CV help used by only 3.7% of US adults | Novoresume Resume Report 2026 (seller, indicative) | `[ESTABLISHED]`(weak source) | Low–Mod | Interviews |
| 15 | Free CV check is the only WTP research available | Funnel audit; 1 reported convert | `[INFERENCE]` | Moderate | Build the log; re-assess after 10 rows |

---

## Appendices

### A. `BLOCKED-KT` list (numbers only KT can provide)
GoatCounter dashboard (visitors, countries, referrers, apply-click rate) · Google Search Console · Vercel analytics · Brevo (list growth, open/click) · Whop (nothing live) · order/revenue history · refund history · WhatsApp enquiry volume · buyer countries · real delivery hours per package.

Under two plausible traffic values, the recommendation **does not change**: at low traffic the answer is bridging + interviews; at higher traffic it is bridging + reading the now-existing funnel events. Both paths start with the same three Phase 0 changes.

### B. Questions for KT
1. Who is actually in your channels — students, graduates, or working professionals? (Decides the ICP.)
2. Can you start the free-check log this week? (Highest-value evidence source.)
3. Do you want the services block above the listings on the home page? (Needs your yes.)
4. Refund/cooling-off terms: do you want a qualified adviser to review them before a company exists?

### C. Could not verify
GoatCounter, Vercel, Brevo, Whop dashboards (all `BLOCKED-KT`) · current Google JobPosting rules for third-party listings (open item) · whether the live production `index.html` matches this worktree's uncommitted UI changes · competitor profitability (never inferable) · exact current prices behind any geo-gated competitor page.

### D. Mobile wireframes (360px)

```
HOME (360px)                     SERVICES (360px)
┌──────────────────┐             ┌──────────────────┐
│ YC  ☰            │             │ YC  ☰            │
├──────────────────┤             ├──────────────────┤
│ Remote jobs, with│             │ You've done the  │
│ the restrictions │             │ hard part...     │
│ shown.           │             ├──────────────────┤
│ [Search jobs]    │             │ ESSENTIAL  $29   │
│ How we verify →  │             │ ──────────────── │
├──────────────────┤             │ PROFESSIONAL $49 │
│ The board is     │  ◄NEW       │ (Recommended)    │
│ free. When you've│             │ EXECUTIVE  $149  │
│ found the role,  │             │ ──────────────── │
│ see the packages.│             │ Add-ons          │
├──────────────────┤             │ Growth $99/mo    │
│ [Search] [Filters│             │ [Get a CV]       │
│  ▸ Fields (65+)  │ ◄collapsed  │ Free CV check →  │
├──────────────────┤             │ Ready for a full │
│ Result: 40 of 1002│            │ rewrite? packages│
│ ┌──────────────┐ │             └──────────────────┘
│ │ Job title    │ │
│ │ Company · loc│ │
│ │ [remote][elig]│ │
│ │ date · meta  │ │
│ │──────────────│ │
│ │[Apply][CV]44px│ │
│ └──────────────┘ │
│ 28px gap         │
└──────────────────┘
```
```
JOB BOARD fold budget (360px), current
56px sticky nav + hero (~180px) + "How these listings work" panel + filter wall
→ first listing currently far below fold. Collapsing Fields (Change 3) pulls the
first card up; that is the measurable win of E3.
```

### E. Screenshots / evidence artefacts
Local preview rendered at 360/768/1440px via headless browser (`preview_shots.py`, `preview_audit.py`); page heights and element geometry measured 26 Oct 2026.

### F. Test / build commands run
`python3 -I -m unittest discover -s tests` → **159 tests, OK** (pre-existing state; no site files modified to produce this report).
