# Review of everything published (31 Oct 2026)

Evidence labels: **[Data]** measured on the live site or repo today; **[Doc]** from a cited source; **[Hypothesis]** reasoned, untested. Traffic is tiny (227 pageviews all time, 0 form submissions), so nothing below is proven by our own conversion data.

## 1. The optimal conversion goal
Revenue comes only from paid CV, cover letter and LinkedIn services; the board is the free acquisition and trust engine. The chain is: visit, find a role (apply click), join the email list, request the free CV check, buy a package.
- **Primary conversion: a completed free CV check request.** It is the only step that turns an anonymous visitor into a named person who has shown the exact problem we sell a solution to, it costs them nothing, and the strategy review already calls it the concierge MVP and "offer engine" (`2026-10-26-business-and-conversion-strategy.md`).
- **Secondary: weekly email signup.** The owned audience that compounds; also the retention loop for the board.
- **Guardrail: apply clicks per visitor.** If services pressure lowers it, the board stops being useful and acquisition dies.
- **Revenue event: paid order.** Too rare to optimise directly at current traffic, and currently blocked by payment friction (below).

## 2. Highest-impact findings
| # | Finding | Evidence | Verdict |
|---|---|---|---|
| 1 | **No online payment.** Card checkout is built but OFF; customers can only pay by bank transfer (USD/EUR/GBP/TL) or crypto, arranged by chat. | [Data] `site-config.js` mode off | Hurts the revenue event most. Needs KT's decision (a payout account for Whop, or another method). Cannot be fixed in code alone. |
| 2 | **The free check is a two-app flow.** The form, then "now email us your CV" in a different app. The recorded "conversion" is intent, not a received CV. | [Data] `free-check.html` | Hurts completion. Quick fix: a prominent "Open my email" button with the subject and a short body prefilled, a copy-address button, and a WhatsApp fallback. |
| 3 | **No search surface.** No per-job pages, no `robots.txt`, no `sitemap.xml`, no canonical on services, no structured data. For job boards, organic search is typically the main free traffic source; ours is manual posting. | [Data] robots/sitemap 404; 1 canonical; 0 JSON-LD | Hurts growth. Google's rules for aggregators are unclear (`drafts/google-job-posting-rules-2026-10-28.md`). Better first step: crawl basics now, then data-driven "remote jobs open to applicants in [country]" list pages (our unique data, no JobPosting markup needed). |
| 4 | **Supply versus a global audience.** 71% of listings are limited to named countries, 1.4% worldwide, 25% unclear. | [Data] jobs.json | Threatens retention: many visitors will find few matches. The weekly email is not personalised by country (only level is collected). |
| 5 | **Trust assets are thin.** No testimonials or reviews; examples are fictional (honestly labelled); a `vercel.app` address and a Gmail-authenticated sender. | [Data] | Mild hurt. Founder block now added. A domain would help credibility and email deliverability; KT deferred it for cost. |
| 6 | **Measurement is partial.** WhatsApp "free check" clicks, form submits and CVs received are three separate things; the enquiry log has not been started. | [Data] GC report | Cannot learn what converts. Build one weekly funnel line. |
| 7 | **Legal gap: no record that the Greenhouse, Lever and Ashby terms on aggregation were read** (a Phase 0 requirement). Listings are republished as short snippets with the source link. | [Data] no decision doc | Unknown risk. A one-hour terms check is cheap insurance. | **Resolved 31 Oct: read the vendors' own pages, no restriction found; see `drafts/decisions/2026-10-31-ats-terms-check.md`.**
| 8 | **Pipeline resilience.** One data-dependent search test blocked every refresh for ~20 hours (fixed 31 Oct). | [Data] Actions | Decouple data publishing from heuristic tests. |

## 3. Element by element
Verdicts: **Helps / Neutral / Hurts** the primary goal. Action: **Keep / Change / Replace**. "Best for now?" is my judgement.

### Job board home
| Element | Why published | Effect | Action | Best for now? |
|---|---|---|---|---|
| Hero "Remote jobs that show who can apply" + counts + "What 'verified' means" | Lead with the one thing competitors blur (eligibility); honest definition of "verified" | Helps; headline untested [Hypothesis] | Keep; test against "Find remote jobs. Know where you can apply." once traffic allows | Yes |
| Search + "Where can you work from?" selector | Eligibility is the differentiator; 71% country-limited | Helps | Keep; also collect country at email signup | Yes |
| Level chips incl. "Level not stated" | Counts now add up | Neutral to helps; adds a row on phones | Keep; consider folding into More filters | Mostly |
| Fields and More filters (collapsed) | Remove the wall above the jobs | Helps (first job 692px from 2,199px on desktop) | Keep | Yes |
| Guided finder ("3 quick questions") | Alternative path for unsure visitors | Unknown; large dashed button on phones | Measure `guide-finder` use; cut if unused | Unproven |
| "How these listings work" box above search | Required eligibility reminder | Neutral; costs ~80px | Move below the results head | Okay |
| Job cards + eligibility pill ("Apply from:") | Core value | Helps | Keep | Yes |
| "Get a CV for this role" on every card | Intent-moment offer | Mixed: 3 clicks vs 4 apply clicks [Data, tiny n]; repeated 40 times | Keep one per card, but test showing it only after the first apply or as a quieter text link | Test |
| Inline email card after 6th listing | Capture where reading | Helps [Hypothesis] | Keep; add optional country | Yes |
| Bottom signup + packages block (below jobs) | Offer after value | Neutral | Keep | Yes |
| Nav "Get Job-Ready" -> /services | Path to paid | Vague label; sends to the pricing page, not the primary conversion | Replace with "Free CV check" -> /free-check | Better exists |
| Footer, report-a-listing link | Trust rule 6 | Helps | Keep | Yes |

### Services page
| Element | Effect | Action |
|---|---|---|
| Hero ("Stop applying in silence...") + trust row | Helps; claim-safe | Keep |
| Package cards, best-for, comparison table | Helps; Professional badged "Recommended" without purchase data | Keep; explain the rationale (done) |
| Executive section (open) | Helps; 3 packages share equal weight while strategy says executives are inbound-only | Keep for now |
| Add-ons, LinkedIn Growth | Neutral; adds choices | Keep; fold below the fold |
| Before/after examples (labelled fictional) | Helps credibility less than real proof | Replace with one real, permissioned example when available |
| Founder block (photo, name, story) | Helps [Doc: Stanford guideline 4; four comparable providers] | Keep |
| Free-check strip + sticky WhatsApp button | Helps; but two entry paths (form vs WhatsApp) split measurement | Keep both; log both |
| FAQ (19 items), terms, "what we promise" | Helps objections; long | Keep |
| Final CTA | Helps | Keep |

### Other pages
| Page | Effect | Action |
|---|---|---|
| /verify (definition, six rules) | Helps trust | Keep |
| /privacy | Required; honest | Keep; counsel review pending |
| /free-check | Core conversion; no sample of what you get; two-step follow-up | Change: add an example result (labelled), the open-email button |
| /order, /subscribed, /thanks | Operational; /thanks unused while card is off | Keep; no action |
| /kit, /mail | Internal tools, noindex, unlisted | Keep |

### Email, WhatsApp, social
| Element | Effect | Action |
|---|---|---|
| Welcome email, tips series, free-check follow-up, customer follow-ups (Brevo) | Helps if the list grows; consent design is sound; sent from a Gmail sender with no domain | Keep; the domain is the real fix |
| Weekly digest | Helps retention; most roles shown are US-only for a global list | Change: personalise by level and country |
| Service emails (/mail templates) | Neutral to helps (saves time) | Keep |
| WhatsApp channel, profile, quick replies, weekly post | Helps; manual | Keep |
| 30-day outreach plan, Facebook and Reddit copy | Facebook sent ~59 visitors, 0 signups [Data]; Reddit not yet tried; group rejections | Change: tailor the landing view by group (country preselected via URL) |
| Logo, favicon, og-image | Helps trust | Keep |

### Infrastructure
Refresh, site monitor, snapshot, routines, signup function: **Keep**. Add: crawl basics, funnel line in the weekly report, test decoupling.

## 4. Self-criticism (my own work)
- The new hero headline and the "Recommended" badge are untested hypotheses.
- I removed dark mode on the public pages; some visitors lose a comfort option.
- The extra country selector and chip moved the first phone listing from about 890px to about 985px.
- "Delivered within 2 and 3 working days" is a promise made without capacity data.
- The outreach plan assumed groups would accept link posts; most did not.

## 5. Recommended order
1. Free-check follow-up button, nav label to "Free CV check", robots.txt, sitemap, canonical on all pages (small).
2. Country field at signup and country-aware weekly email (medium).
3. Weekly funnel line: form submits, WhatsApp check clicks, CVs received (small).
4. Decoupled data publishing from heuristic tests (small).
5. ATS-feed terms check (one hour, mostly reading).
6. Programmatic "remote jobs open to applicants in [country]" pages (large; test with 3 countries first).
KT decisions: payment method; domain when affordable; testimonials after the first orders.
