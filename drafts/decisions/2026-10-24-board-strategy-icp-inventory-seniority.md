# Strategic review: customer profile, inventory, seniority mix, journey, metrics

Status: PROPOSED, for KT's decision. Nothing here has been implemented, committed or merged. The board and kit changes from the previous step are on the branch only (not on main).
Written 24 Oct 2026. Evidence labels: **[Established]** = measured by us or cited from a named source; **[Hypothesis]** = reasoned, testable; **[Assumption]** = needs customer validation.

## 0. Limits of the evidence (read first)
- **No traffic data.** GoatCounter returns a login redirect (HTTP 303), so I could not see visitors, countries, clicks or enquiries. Every claim about "who arrives" is an assumption until that is read.
- **No customer data.** There are no buyers, enquiries or interviews yet.
- **Market research is thin and mostly vendor-sourced.** I found one survey with a share of people who hired a professional (Novoresume, a seller of resume tools). I found no independent data on willingness to pay by segment, and no published conversion rates for job-board-to-resume-service funnels. Firecrawl credits ran out mid-session, so research used the built-in web search only.
- The audit of our own listings is first-hand (all 1,026 records, all apply links re-opened).

## 1. Executive recommendation
1. **Do not scrape a new batch yet, and do not shrink the board.** The audit finds the inventory is trustworthy but narrow, and its main gap (jobs a non-US reader can apply to) cannot be closed by scraping more of the same sources.
2. **Immediate priority: find out who is actually arriving, and fix label and link problems on the existing inventory.** Both are cheap, reversible and useful whichever customer segment wins.
3. **Working hypothesis for the paying customer: experienced non-executive professionals (about 2-10 years) actively applying for remote roles, often in a transition.** Students and graduates are best treated as audience-building (reach, referrals, free CV check), not as the main revenue engine. Executives are an opportunistic top tier. All of this is a hypothesis until the validation in section 8 is done. I earlier said mid and senior visitors were "likelier buyers"; that was reasoning, not evidence.
4. **Do not apply one global seniority default.** Show every level, make the level one tap, and let each post link to the level that fits the group it goes to (already built, section 5).

## 2. Customer profile (ICP) analysis
### What is established
- Professional help is rare. In a May 2026 survey of 2,000 US adults aged 18-64, **3.7%** used a professional resume writer or coach; 57.1% used a template, 13.6% AI tools, 10.1% a friend or family member (Novoresume Resume Report 2026; the publisher sells resume tools, so treat as indicative).
- AI substitution is strongest among the young: any AI use on the latest resume was Gen Z 55.8%, Millennials 47.6%, Gen X 34.1%, Boomers 24.5% (same survey). A separate 2024 survey of 2,921 US 18-27 year-olds found 22% used ChatGPT for a resume or cover letter (ResumeTemplates, also a seller).
- Students and recent graduates have a free alternative: resume review is the most-used and most-helpful university career-centre service in NACE surveys (70.1% of users in 2010; same ranking in the Class of 2017 survey). Dated, and only for enrolled students or graduates of those schools.
- Market price points: budget freelancers about $15-$150; established services from about $149-$179 for entry level up to $349-$699+ for executive tiers (TopResume, via review sites). Our $29/$49/$149 sit well below this. The standard funnel is a **free review that leads to paid tiers** (TopResume), which matches our free quick CV check.
- Recruiter use of LinkedIn is very high (sources range from 72% to 97%, mostly secondary), so a LinkedIn profile matters to people applying to employers, but the claimed uplift figures (for example "71% more interviews") have no primary source. Do not repeat them.

### What vendors claim but nobody measured
Sellers name career changers, mid-career managers and executives as their core clients. No survey of client mix by seniority was found (professional bodies publish none).

### Segment comparison (judgements marked [H] hypothesis or [A] assumption)
| Segment | Purchasing power | Urgency | Alternatives | Fit with our board |
|---|---|---|---|---|
| Students, graduates, early career | Low [H] | High, but "any job" urgency | Free career centre, AI, templates, friends [Established] | Thin supply: 70 plausible early roles, 30 posted in 7 days, 30 US-only (section 3) |
| Mid-career, advancing or changing field | Moderate to good [H] | High when laid off or stuck [H]; layoff sentiment is weak (NY Fed: perceived re-employment chance 44.9%, lowest since 2013, via a secondary post) | Templates, AI, paid writers from $149 | Best supply: 336 mid roles (272 distinct) plus senior |
| Senior and executive | High [H] | Medium, often employed and passive | Specialist writers at $349-$699+, recruiters, referrals [Established prices] | 448 senior and leadership roles, but 52% of leadership roles are US-only; buyers usually pick a writer on named credibility, which conflicts with the no-founder-name rule [H] |
| International remote seekers (any level) | Varies; $29-49 may be meaningful relative to local income [A] | Very high for USD-paying remote roles [H] | Marketplace sellers, many from their own region [Established, anecdotal] | **Worst supply**: Nigeria 32 listings, Philippines 26, Pakistan 20, Kenya 33 of 1,026 |

### Recommendation
- **Primary (hypothesis H1):** experienced non-executive professionals applying for remote roles, especially in a transition. Reasons: highest budget-to-price ratio at our price points, lower substitution by AI than the young, best match with the inventory we actually have. Against it: the 3.7% base rate, no reviews or testimonials yet, and unknown reach (our channels may not contain them).
- **Secondary:** (a) international remote seekers, which may overlap H1 but needs different inventory; (b) graduates and early career as a growth and referral channel, with the free CV check as entry and the lower-priced add-ons; (c) senior and executive as inbound-only, not built for.
- **KT's working assumption that the first users are students and recent graduates** is plausible given the channels, but it is not established. It decides where to aim posts, not who pays.

## 3. Audit of the existing inventory (1,026 listings, 160 employers, pulled 23 Oct 21:21 UTC)
**Freshness and openness [Established]**
- All 1,026 are within 30 days; median age 7.5 days; 469 within 7 days. Listings come from employers' own Greenhouse (544), Ashby (336) and Lever (146) feeds, refreshed every 6 hours, so a listing that disappears from the employer's feed drops from the board.
- I re-opened all 1,026 apply links independently: **1,020 returned 200; 6 returned 403** (Carvana, bot-blocked, so unverified by us). Two Axiom pages matched my "closed" wording, but the rendered page showed no closed notice (false positive).
- A page that loads does not prove the role is open; the strongest evidence is the 6-hourly employer feed.
- **Specific-posting check (listing standard #1):** 205 Greenhouse links (20%) redirect to the employer's own careers site. In a real browser, one listing per employer host (28 hosts): 20 showed the specific job; **8 hosts did not visibly show it** (generic careers page or blank page): Talkspace (timed out), Billtrust, Stitch Fix, Elation Health, Suki, Thrive Market, Lokalise, Lattice. These hosts carry **31 listings (3%)**. This is not proof they are closed; it is proof a reader may land on a page that does not show the job. Only one listing per host was tested, so the real count could differ.

**Remote and eligibility [Established]**
- 91.2% confirmed remote; 8.8% "remote unclear" (labelled on the card).
- Eligibility stated for 74.3%; **264 (25.7%) unclear** plus 6 time-zone only.
- **41.7% US-only.** Only **17 (1.7%)** are open worldwide, and 21 more to a region.
- Listings a person can verifiably apply to by country (all levels / early-career): United States 488 / 47, Canada 110 / 7, United Kingdom 104 / 2, India 44 / 9, Nigeria 32 / 2, Philippines 26 / 1, Kenya 33 / 2, South Africa 35 / 2, Pakistan 20 / 0.

**Seniority labels [Established unless noted]**
- Level mix: early career 96 (9.4%), mid 336, senior 328, leadership 120, level not stated 146.
- The "junior" label is mechanical: 76 junior listings, 75 of which ask for exactly 1 (19) or 2 (56) years. "Mid" means mostly 3-5 years asked.
- **About 26 of the 96 early-career labels are doubtful:** licensed or clinical roles (6 mental health therapists by state, physician reviewer, general practitioner, legal counsel, SIU investigator), engineer and account-executive roles asking 2 years with pay of roughly $115K-$260K, a "Senior Program Manager" asking 6 years labelled entry, and "Technical Recruiter, Early Career" (asks 3 years; the "early career" is the people being recruited). My rule was crude, so the true figure is approximate; it needs a human read.
- That leaves about **70 plausible early-career roles, 63 distinct once location variants are merged, at 39 employers; 30 posted in the last 7 days; 30 are US-only, 22 limited to another country, 18 unclear.**
- Possible under-labelling: up to about 14 "level not stated" sales-development, business-development and support-specialist roles look early-career-compatible; this needs a human read. Three Smartsheet roles show "20 years" (likely a parsing slip) and are labelled senior.
- Early-career roles are thin in the fields graduates search: Marketing 4, Finance 2, Data 2, Product 0 (counts among all 96 labelled early-career roles).

**Duplication and concentration [Established]**
- 793 distinct title-and-company roles in 1,026 rows: 103 rows are the same role in another location (for example 6 therapist listings, one per state). The headline "1,026 jobs" overstates distinct opportunities by about a quarter.
- Employer concentration is low (top 10 employers = 15%); employers are well-known funded companies, so credibility is high and relevance is narrow (software 21%, sales 14%).
- Pay stated on 601 (58.6%). Held back by the quality rules this run: 4; warnings: 13.

**Disposition**
| Action | What | Count (approx.) |
|---|---|---|
| Keep | Everything that passes the 30-day, link and remote checks, including senior roles | about 1,000 |
| Verify by hand | 8 employer hosts whose pages did not show the job; 6 Carvana links | 31 + 6 |
| Relabel (human read, then fix the classifier with regression fixtures) | Doubtful early-career labels; possible under-labelled early roles; the "20 years" parse | about 26 + up to 14 + 3 |
| Merge for display | Same role in several locations shown once with a "N locations" note | 103 rows |
| Supplement | Roles open to non-US readers and early-career roles in marketing, finance, data, product, support | to be sized after section 8, step 1 |
| Remove | Nothing needs removing on current evidence | 0 |

## 4. Listing strategy: options compared
| Option | User value | Effort | Maintenance | Freshness and breadth | Lead potential |
|---|---|---|---|---|---|
| A. Keep and improve | Good for US/CA/UK/EU mid-career; poor for international and early career | Low | Low | Already fresh every 6h | Good if H1 holds |
| B. Scrape fresh batch now | Unknown, because we do not yet know the gap | Medium, plus vendor-term checks and a company list KT must approve | Higher | More of the same sources adds breadth, not the missing eligibility | Unknown |
| C. Shrink to a curated set | Higher trust per listing, but the board would hold about 550-580 roles if seniors were cut and look thin to everyone | Low | Low | Loses breadth and search coverage | Probably lower |
| D. Hybrid | Fix and relabel now, source only to fill gaps the data proves | Low now, medium later | Medium | Best | Best |

**Recommendation: D, sequenced as A now, targeted sourcing later.** The hybrid is only worth doing once we know the gap, so the first step is A. A gap we can already see is *different in kind*: employers that hire in many countries or are open worldwide. More Greenhouse/Ashby/Lever boards of US-based scaleups will not fix it. If sourcing is approved later it must be a curated company list that KT approves (CLAUDE.md), with a documented decision first.
- "Reduce" should mean merging location variants for honest counting, not cutting roles to look curated.

## 5. Seniority mix
Two separate questions:
1. **What makes the board useful?** Whatever the audience can apply to. For a US/Canada/UK reader, current inventory is good across levels. For a reader in Nigeria, India or the Philippines at any level, there are 20-44 roles in total.
2. **Who buys?** H1 (mid-career) first, unproven.

Recommendation: **no target percentages.** Keep all levels on the board. Make level one tap (built: Experience chips; counts All 1,026 / Early 96 / Mid 336 / Senior and leadership 448). Segment by link, not by default: posts to a group that is mostly students link to `/?level=early`; posts to general or professional groups link to all levels. The post kit already defaults to entry-level and junior and has a group-country filter. A global default of "Early career" would show a reader about 96 rows (63 distinct plausible roles after merging), about 45% of them US-only, and would hide the roles most likely to match H1. Decide the home default after two weeks of click data by level.
- Do not use the phrase "for students" or "for graduates" in posts: the brief's copy rule forbids claiming a role suits a background. "Entry-level and junior" is the compliant wording (already used).

## 6. User experience priorities (journey: discover, find, trust, apply, return, buy)
1. **Where do you live?** The biggest friction is eligibility: about 70% of rows are limited to specific countries, and 26% are unclear. Ask once for country (remember it on the device), show "N roles you can apply to" and rank by eligibility. This is the most valuable change for every segment and matters most for international readers. [Hypothesis: it raises apply clicks; test it.]
2. **Make the count honest.** Group location variants ("6 locations") so 1,026 does not overstate real choice.
3. **Fix level labels** (section 3) so the early-career and senior filters can be trusted.
4. **Handle the 8-host landing problem:** where an employer site does not show the posting, say "opens the employer's careers page; look for the role" or replace the link.
5. **Return reasons:** the weekly email already exists; extend signup to field and level so the digest is relevant. (Brevo field changes need KT's approval per CLAUDE.md.)
6. **Per-job pages** are in the original brief (structured data for Google job search) but not built; the board is one page of cards. This is the main route to organic search traffic from people actively searching, and it needs Google's current job-posting rules checked first. Defer until the audience is known.

## 7. Conversion strategy (natural path from job to service)
- **Today:** a "Get a CV for this role" button on every one of 1,026 cards, a services block on the home page, a nav button, and a free quick CV check. Labelled as ours and not part of the employer's application.
- **Risk:** a button on every card can read as an ad. **Hypothesis to test:** show it only after a user opens a listing or clicks apply, and keep a single free-check offer on the page. Evidence either way needs traffic; GoatCounter events exist for this (`cv-click-*`, `apply-click`).
- **Value proposition at the moment of need:** "Applying to this role? Get three specific fixes to your CV, free." That is the free CV check, framed around the job, with no claim the CV will win the job. It fits the standard funnel (free review leading to paid tiers).
- **Price fit:** $29/$49 are well under market. If H1 is right, test whether buyers hesitate at the low price (does low price signal low quality?) before changing anything.
- **Executives:** a tension to decide, not to resolve now: the no-founder-name rule helps trust with job seekers generally but probably hurts the top tier, where buyers choose on a named writer's credibility [H].
- Never trade trust for conversion: no urgency claims, no "most popular", no outcome promises (already enforced by tests).

## 8. Validation plan (highest-impact unknowns first)
| # | Question | Method | Decision it unlocks |
|---|---|---|---|
| 1 | Who is in KT's channels (country, stage, size)? | KT lists the groups and pages and who is in them; read GoatCounter countries and referrers after 7 days | Which segment we are really reaching; whether sourcing for non-US readers is needed |
| 2 | Do posts aimed at early career vs all levels draw different clicks? | Same group types, two weeks, `utm_campaign` and `level` param; one variable at a time | Home default; kit default |
| 3 | Who asks for the free CV check? | Add one question to the WhatsApp reply: career stage and country; log in a sheet | Primary ICP evidence |
| 4 | Will people pay, and how much? | 10 short conversations (5 mid-career, 5 graduate or international): what did you last pay for CV help? | Price tiers; ICP |
| 5 | Are level and eligibility labels right? | `scripts/spot_check.py`: 50 random listings opened and compared; report the real score | Classifier fixes |
| 6 | Is the supply gap real for our audience? | After step 1: count roles the typical member can apply to; threshold to decide, set in advance (suggest: fewer than about 50) | Whether to source new employers |

## 9. Success metrics
**Measurable now (events already in the code, GoatCounter login needed):** visits by country and referrer (`utm_source`), `apply-click` per listing, `cv-click-*`, `filter-level` and `filter-country`, services page visits. Also from the repo: % links returning 200 (99.4% this run; 6 unverifiable), % with eligibility stated (74.3%), age of listings, and spot-check accuracy.
**Needs a small addition:** WhatsApp enquiries and free-check requests logged by hand with stage and country; orders by segment.
**Needs volume (a few hundred visitors a week or more):** search-to-apply rate, return visits, funnel conversion by segment. Below that, rates are noise: use counts and conversations, not percentages.
Report small numbers as counts ("3 enquiries from 120 visits"), never as a trend.

## 10. Implementation roadmap
**Now (no segment decision needed; reversible):**
1. Human read of the doubtful and possibly under-labelled levels, then fix the classifier with regression fixtures and tests (CLAUDE.md quality rule).
2. Verify the 8 hosts and 6 Carvana links; decide link treatment.
3. Spot-check 50 listings and report the score.
4. Add the stage and country question to the free-check reply and start the enquiry log.
5. Hold or merge the existing branch (Experience chips plus kit audience and country filters) on KT's say-so. It does not commit us to a segment.
**After about two weeks of data:** country-first prompt and variant grouping; decide home default, CV-button placement test, sourcing brief (company list for KT's approval), per-job pages and structured data.
**Wait for evidence:** price changes by segment, an executive-specific offer, local-currency pricing, any new paid line.

## Sources
- Novoresume Resume Report 2026: https://novoresume.com/career-blog/resume-report-2026
- ResumeTemplates Gen Z survey: https://www.resumetemplates.com/only-22-of-gen-z-use-chatgpt-for-their-resume-nearly-all-land-jobs-and-higher-salaries/
- NACE (career-centre resume help usage, via Bucknell summary and NACE pages): https://careerinsider.blogs.bucknell.edu/2010/06/28/research-says-use-career-services-to-increase-likelihood-of-job-offers/
- TopResume pricing and free review (review sites): https://www.moneycrashers.com/topresume-review/ , https://300hours.com/topresume-review/
- Virtual Vocations remote seeker demographics: https://www.virtualvocations.com/blog/annual-statistical-remote-work-reports/remote-work-demographics-survey-results-2024/ (the sample is from their own site's users)
- Earlier price table: `drafts/decisions/2026-10-18-pricing-and-offer-structure.md`
