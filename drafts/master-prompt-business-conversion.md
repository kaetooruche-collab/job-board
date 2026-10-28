# MASTER PROMPT — Yireh Careers: Business & Conversion Strategy
### (repo-calibrated · research and planning only · no implementation)

**ROLE**
Act as a principal product strategist, senior UI/UX designer, CRO specialist, behavioral
researcher, consumer psychologist and digital business model consultant with 10+ years of
equivalent expertise in consumer behavior, freemium monetization, career services,
mobile-first design, pricing and landing pages. Critically challenge assumptions — including
the ones already recorded in this repository's decision files. Do not merely agree with
existing decisions, and do not soften a recommendation to be agreeable.

---

## 0. GROUND TRUTH — read before forming any opinion

This is a live product with an explicit rulebook, not a greenfield brief. Read, in order:

1. `CLAUDE.md` — the project constitution. **Where it conflicts with this prompt, CLAUDE.md wins.**
2. `drafts/kt-todo.md` — what KT must currently decide or do.
3. `drafts/voice-and-copy-guide.md` — mandatory tone rules for any copy you write.
4. Decision files in `drafts/decisions/`, especially:
   - `2026-10-24-board-strategy-icp-inventory-seniority.md` — status PROPOSED; contains
     the *hypothesis* that experienced non-executive professionals are the primary paying
     customer and that the real supply gap is roles open to non-US readers. Treat every claim
     in it as established / hypothesis / assumption and challenge it with evidence.
   - `2026-10-18-pricing-and-offer-structure.md`, `2026-10-19-whop-payments.md`,
     `2026-10-23-whop-checkout-integration-plan.md`, `2026-10-24-email-marketing-system.md`,
     `2026-10-24-signup-function.md`.
5. The product surface: `index.html`, `services.html`, `verify.html`, `privacy.html`,
   `free-check.html`, `order.html`, `thanks.html`, `site-config.js`, `site-forms.js`,
   `api/subscribe.js`, `platforms.json`, `jobs.json` (sample ~1002 rows).
6. The quality system: `scripts/qa_checks.py`, `scripts/site_monitor.py`, `scripts/spot_check.py`,
   `drafts/weekly-audit-prompt.md`, `tests/` (159 Python tests), `.github/workflows/*`.

**Verified architecture facts (re-confirm, do not rediscover):**
- Static HTML/CSS/JS, no framework, no `package.json`, no build step. Page styles are inline
  per file; `index.html` holds the board UI, rendering script and design tokens.
- Hosted on Vercel (`yirehcareers.vercel.app`); one serverless function, `api/subscribe.js`
  (Brevo, key in Vercel env `BREVO_API_KEY`). No database, no user accounts, no sessions.
- Data: Python pipeline on GitHub Actions — refresh every 6h (`fetch-jobs.yml`),
  live-site monitor every 3h (`site-monitor.yml`). Classifier + QA layers in `scripts/`.
- Analytics: GoatCounter (`kayzglobal.goatcounter.com`), cookieless. Existing events in code:
  `apply-click`, `cv-click-*`, `filter-field`, `filter-level`, `filter-country`.
- Revenue today: WhatsApp hand orders (+90 533 822 5854). Published packages:
  Essential $29, Professional $49, Executive $149, LinkedIn Growth $99/mo, add-ons
  ($15 cover letter, $25 LinkedIn setup, $10 extra revision, $15 second CV, $15 priority,
  $29 interview sheet), free quick CV check (one per person).
- Card checkout is built but **OFF** (`SITE.checkout.mode = 'off'`, Whop). Going live needs
  KT's explicit approval + `drafts/whop-go-live-checklist.md`. **No payment provider other
  than Whop may ever be proposed.**
- Recent UI work (uncommitted at time of writing): spacing/hierarchy tokens, compact
  uncertainty notes, collapsible Fields group, active-filter chips. Audit the *current*
  state in the repo; do not re-propose what is already done.

---

## 1. ACCESS, EVIDENCE DISCLOSURE AND BLOCKERS

**Available to you:** the GitHub repository (being made public), the live site over HTTP,
a local preview + headless browser for screenshots at 360 / 768 / 1440 px in dark and light,
and full web research.

**Not available unless KT hands you access — mark every dependent number `BLOCKED-KT`:**
- GoatCounter dashboard → **no traffic, no conversion rate, no funnel baseline exists for you.**
- Google Search Console, Vercel dashboard, Brevo account, Whop account, order/revenue history,
  customer emails, refund history.

**Rules of disclosure:** never invent a baseline, sample size, lift or revenue figure.
If a recommendation depends on a number you don't have, state the number needed, who can
provide it, and what you'd do under two different plausible values.
Repository being public does **not** expose secrets: `BREVO_API_KEY` lives in Vercel env;
never read, print, commit or reference real credentials.

---

## 2. HARD OPERATING RULES (non-negotiable, inherited from CLAUDE.md)

- **Research ≠ implementation.** Do not edit site code, data, scripts, tests, configs or
  workflows. Do not commit, push, deploy, or trigger the refresh pipeline.
  **The only permitted write is this report file** (see Delivery).
- No actions in Brevo (create/change/send). No money spent. No accounts created.
- Never invent prices, testimonials, credentials, statistics, outcomes or employer claims.
- Never write: "no work permit needed", "guaranteed", "the only job board", or claims that a
  role suits a degree/background unless the posting says so. No promises of jobs, interviews
  or results. No country/city names in site copy, code identifiers or page titles
  (exception: the privacy page's operator location).
- No personal name, face or photo anywhere on the brand (KT's rule).
- Job seekers are never charged to apply or to see an apply link, and listings are never
  paywalled. Commission-only and applicant-fee roles stay excluded.
- Consent wording on forms is fixed and tested; privacy page changes need KT approval.
- Consequential or irreversible actions require KT's explicit approval; KT may OVERRIDE any rule.

---

## 3. RESEARCH (behavioral + freemium)

For each concept you use — perceived value, loss aversion, effort justification, endowment
effect, commitment/consistency, cognitive load, trust, social proof, present bias, choice
architecture, WTP, transparency effects — report: **evidence base → relevance to a free job
board selling human CV services → product implication → limitations → testable hypothesis.**
Classify each as `[ESTABLISHED]`, `[POPULAR-INTERPRETATION]`, `[COMPETITOR-OBSERVATION]`,
`[INFERENCE]` or `[HYPOTHESIS]`. Include contrary evidence for every strong claim
(e.g. scarcity/dark-pattern backfire, warning-label fatigue, discount anchoring effects).

Freemium/paywall survey across CV builders, job boards, career platforms and service
businesses: what is free, what is paid, when the offer appears, deliverables, pricing model,
upgrade messaging, and observed abandonment/distrust risk. **Distinguish observed fact from
interpretation, and never infer profitability from the existence of a paid product.**

Competitor comparison with **verified current features and prices, each with URL and access
date**: Teal, Rezi, Resume.io, Huntr, Kickresume, Zety/ResumeGenius, LinkedIn Premium Career,
FlexJobs, Remote OK, We Work Remotely, Working Nomads, Himalayas, Otta/Wellfound, Simplify —
plus non-obvious substitutes that actually compete for the same need: ChatGPT/Canva,
university career services, freelance CV writers (Fiverr/Upwork), and free government/NGO
employment services. (The Remotive API is excluded by project policy; do not recommend it.)

---

## 4. PRODUCT AUDIT (evidence-first, desktop and mobile separately)

Walk the real journey: landing → search/filter → eligibility interpretation → job engagement →
apply handoff → service discovery → service detail → contact/checkout → return visit.
Use the local preview and take screenshots as evidence. For each major issue report:
**evidence (screenshot/URL/DOM) → likely cause → business impact (qualified) → confidence →
correction → validation metric.** Separate usability observations from unverified revenue
hypotheses.

Audit at minimum:
- Above-the-fold economics: hero length, the "How these listings work" panel, filter wall,
  and how far the first listing sits from the fold on 360px.
- Eligibility system honesty vs scannability (pills, uncertainty notes, "Why this label?").
- **Service discoverability**: nav "Get Job-Ready", hamburger on mobile, homepage services
  section, per-job "Get a CV for this role", `/free-check`, `/services`. Quantify how many
  steps and scrolls each path takes on mobile.
- Offer comprehension on `services.html`: 3 packages + add-ons + LinkedIn Growth —
  choice overload, price anchoring, revision/delivery clarity, missing refund terms.
- WhatsApp handoff friction (no checkout; how many taps; what the prefilled message says).
- Trust assets (verify page, source/date/last-checked on cards, report-a-listing) and whether
  they are mobilised as conversion assets or merely present.
- Known data-quality issues that could undercut eligibility trust (~26 doubtful early-career
  labels, 103 location variants, 8 employer sites not visibly showing the posting).
- Copy compliance with `drafts/voice-and-copy-guide.md` (website copy has NOT been reviewed
  against it yet — this is a required audit item).

---

## 5. SEGMENTS AND JOBS TO BE DONE

Segments to test (not assume): casual browsers, active applicants, early-career candidates,
experienced professionals, cross-border applicants needing eligibility clarity, people needing
CV/LinkedIn help, career changers, freelancers. Reconcile with the PROPOSED strategy doc's ICP
hypothesis and with the site's stated audience (students → specialists). For each priority
segment: desired outcome, problem, current alternatives, friction, WTP hypothesis, purchase
trigger, objections, best-fit service, best offer timing. **Recommend priority segments and
explicitly name segments not worth targeting initially.** Label each conclusion with its
evidence class.

---

## 6. FREE-TO-PAID STRATEGY

Compare five models on a scored table — revenue potential, acquisition, trust risk,
implementation effort, support burden, repeat purchase, mobile conversion, operational
requirements, fit with KT's current solo resources:
A. Free discovery + paid career services.
B. Free discovery + contextual offers.
C. Freemium career tools with meaningful paid upgrades.
D. Premium job-search features, core discovery stays free.
E. Service-led hybrid: individual services, bundles, validated add-ons.

Constraints any model must satisfy: listings and apply links stay free forever; no applicant
fees; Whop-only payments (currently OFF); WhatsApp-based ordering; privacy/GDPR; low and
unmeasured traffic.

**Recommend a primary model, a fallback, and explicit conditions that would switch the decision.**

For every candidate paywall/offer specify: trigger · user problem · value already delivered ·
free functionality retained · paid offer · exact copy/CTA · pricing hypothesis (evidence-backed
or labelled hypothesis) · objections · disruption risk · validation experiment.
Consider contextual offers, inline upgrades, dedicated service pages — and say plainly when a
hard paywall is the wrong answer. **Monetize meaningful value, never manufactured frustration:
no bait-and-switch, fake scarcity, countdowns, hidden restrictions or obstructive navigation.**

---

## 7. WEBSITE ARCHITECTURE

Deliver a sitemap for a static Vercel site (routes must be real HTML files or clean redirects;
today: `/`, `/services`, `/verify`, `/privacy`, `/thanks`, `/free-check`, `/order`,
`/subscribed`, plus unlisted `/kit` and `/mail`). Evaluate adding: pricing page, individual
service pages, FAQ, job-alert page, post-purchase onboarding.
Define desktop and mobile navigation separately, and **solve mobile service discoverability
directly** (persistent service nav, contextual CTAs, service cards, sticky CTA, post-action
recommendations) with a global-vs-contextual matrix.
Provide: sitemap diagram (Mermaid), primary user-flow diagrams (Mermaid + ASCII fallback),
conversion-point map, and paywall/offer logic diagram. Flag SEO dependencies (JobPosting
structured data is an unresolved open question — check Google's current rules before
recommending it; OG tags and canonical behaviour already exist).

---

## 8. LANDING PAGE AND COPY

Two positioning directions, trade-off comparison, one chosen direction with reasoning.
Then an **actual page-by-page content plan**: section order, purpose, headline, body, CTA,
trust signal, objection handled, offer, mobile-specific change — for home, services landing,
at least two individual service pages, verify, free-check, and job-card microcopy.
Write **real draft copy**, not descriptions of copy. It must state who Yireh Careers serves,
the remote-eligibility problem it solves, what is free, what is paid, and why the services may
be worth buying — in the voice defined by `drafts/voice-and-copy-guide.md`
(short, warm, plain, contractions, one next step, legal point said once where it matters).
No generic promises, no guarantees of employment/interviews/success, no founder name or photo.

---

## 9. CAREER SERVICE OFFER DESIGN

Evaluate — do not assume — individual CV services, LinkedIn services, bundles, CV reviews,
personalised assistance, and genuinely useful free diagnostics as candidate offers.
For each recommended offer: audience · problem · deliverables · scope · difference from free
alternatives (including free alternatives like ChatGPT) · pricing-validation method ·
value proposition · CTA · objections · delivery requirements · revisions · refunds · support load.
Existing published packages are the baseline; changing prices, package names, revision limits,
the 12-post/30-day Executive commitment or delivery times requires KT's explicit approval, and
refund terms have **not** been decided — flag that as a decision, don't invent it.
Validate willingness to pay (pre-sales on WhatsApp, interviews, smoke tests) before any
unproven offer is built.

---

## 10. MOBILE-FIRST EXPERIENCE

ASCII wireframes at 360px for: landing page, job board, career-services page.
Evaluate above-the-fold budget (56px sticky nav + hero + disclosure + filter wall vs first
listing), navigation, job access, service discovery, CTA hierarchy, service-card choice
overload, sticky controls, and the contact/checkout flow.
Conversion elements must be discoverable without obstructing content; respect existing
touch-target minimums (44px buttons, 32px chips) and `prefers-reduced-motion`.
Do not solve this by shrinking the desktop layout.

---

## 11. ANALYTICS AND EXPERIMENTS

Start from the **existing** GoatCounter taxonomy in `index.html` and extend it in the same
naming style: landing views, searches, filter use, job engagement, apply clicks, service
impressions/clicks, service views, checkout initiation (only meaningful once Whop mode is
live), purchases, refunds, repeat purchases.
Define: visitor→service-page, service→checkout, checkout completion, visitor→customer,
revenue per visitor, refunds, engagement, retention, application CTR.
Classify metrics as primary outcomes / diagnostic / guardrails. Guardrails must include trust
signals: report-a-listing rate, unsubscribe rate, QA pass rate, "wrong listing" complaints.

Build a prioritized experiment roadmap (copy, CTA placement, mobile navigation, packaging,
pricing, offer timing). Each experiment: hypothesis · control · variant · primary metric ·
guardrails · decision rule. **No invented baselines, sample sizes or expected lifts.**
Explain how traffic and minimum detectable effect determine sample size and duration, and
state plainly that with today's unmeasured, likely low traffic, interviews, usability tests
and WhatsApp pre-sales validation beat A/B tests.

---

## 12. TECHNICAL AND OPERATIONAL FEASIBILITY

Classify every recommendation as: `FRONTEND-STATIC` / `SERVERLESS-FUNCTION` /
`THIRD-PARTY-CONFIG` / `NEW-OPERATIONS` / `REQUIRES-KT-APPROVAL`.
Cover framework, routes, data sources, integrations, analytics, performance (measure
`jobs.json` payload and render cost), checkout requirements, onboarding, service delivery
capacity (KT delivers by hand), privacy/GDPR, maintenance and debt (single-file inline CSS/JS,
no component system, Python-only tests, `tests/node` without a package.json).
**Do not assume any tool or payment provider is configured. Do not implement anything in
this phase.**

---

## 13. EVIDENCE STANDARDS

Priority: original academic research, systematic reviews, official product docs and live
competitor experiences, credible industry reports, well-documented case studies.
Cite factual claims with direct links + access date. Classify every major recommendation as
`[ESTABLISHED]`, `[COMPETITOR-OBSERVATION]`, `[INFERENCE]`, `[HYPOTHESIS]`.
Include contrary evidence. No fabricated statistics or causal claims. Where evidence is thin,
say so and propose the cheapest way to learn.

---

## 14. REQUIRED REPORT

**Part I** Executive diagnosis · existing strengths · weaknesses · five highest-priority
opportunities · decisions requiring more evidence.
**Part II** Behavioral research · freemium/paywall evidence · competitor analysis (with dated
prices) · product implications.
**Part III** Segments · JTBD · free/paid allocation · five-model comparison · recommendation
with fallback and switch conditions.
**Part IV** Sitemap · desktop/mobile navigation · user flows · service-discovery map ·
conversion points · offer/paywall logic.
**Part V** Positioning options · chosen direction · landing-page specification · real copy and
CTAs · job-board and service-page copy · mobile variants.
**Part VI** Service packages · pricing hypotheses and validation plan · checkout · onboarding ·
trust · refunds and support (flag undecided terms).
**Part VII** Event taxonomy · funnel definitions · experiments · guardrail metrics.
**Part VIII** Phased roadmap: priority, dependency, effort, risk, measurable completion criteria.
**Part IX** Final recommendation · free-to-paid boundary · first three changes (each
implementation-ready: exact files, exact copy, acceptance criteria) · assumptions to validate ·
tactics to avoid.
**Evidence table**: recommendation · source link · evidence class · confidence · validation method.
**Appendices**: screenshots, "BLOCKED-KT" list, "questions for KT", and an explicit list of
anything you could not verify.

---

## DELIVERY AND GATE

Write the report to
`drafts/decisions/2026-MM-DD-business-and-conversion-strategy.md` with `Status: PROPOSED`
(that is the only file you may create or change), then summarise it in chat in plain language.
Stop there. **No implementation, no commits, no deploys until KT explicitly approves.**
Implementation happens in a separate session against this report.

## ACCEPTANCE CRITERIA FOR THE REPORT ITSELF
- Every factual claim is cited or explicitly labelled as inference/hypothesis.
- No invented traffic, revenue, price, testimonial or lift numbers; blockers listed.
- Competitor prices dated and sourced; substitutes included.
- Mobile wireframes and at least two positioning directions present.
- Copy is actual copy, compliant with CLAUDE.md's forbidden-wording and voice rules.
- Every recommendation names the file/route it touches and how it would be validated.
- Nothing proposed violates CLAUDE.md; any tension with an existing decision is called out,
  not quietly resolved.
