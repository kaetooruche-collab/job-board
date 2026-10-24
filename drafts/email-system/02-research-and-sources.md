# 02 · Research report, source register and recommendation-to-evidence matrix

Status: PROPOSED (Phase 2 deliverable). Research done 24 Oct 2026 with web search and page fetches. Labels used throughout: **Evidence** (a source says it), **Assumption** (we believe it, no source), **Hypothesis** (to test), **Recommendation** (our choice). Where a source was a summary by someone else, it says so. No benchmark in this document comes from memory.

## What the research can and cannot tell us (read this first)

1. **There is no study of paid CV services versus AI tools.** I found no randomised or even quasi-experimental study that compares a human-written CV service with AI-written CVs on interviews or hires. Everything below on "why pay $29" is adjacent evidence, and the positioning in 04 is a **hypothesis**, not a finding.
2. **There is no defensible universal email cadence.** The one peer-reviewed field experiment I found (subscription service, two emails two weeks apart helped, fatigue after the second) is from another industry. We use it only to justify a conservative cap, not to claim an ideal.
3. **Industry benchmark numbers (open rates, "4 vs 7 emails cut lifetime value 32%") were not verified and are not used.** Open rates are also unreliable (Phase 10).
4. **Legal sources are a mix of official pages and law-firm summaries.** The register marks which. None of this is legal advice; 08 lists what needs a lawyer.

## Findings

Each finding: claim, source, date, method and population, limitations, relevance, and whether it supports a decision or only a hypothesis.

### Why people might still pay a human when AI exists

**F1. Writing help raised hiring.** Wiles, Munyikwa and Horton, "Algorithmic Writing Assistance on Jobseekers' Resumes Increases Hires", NBER Working Paper 30886 (Jan 2023, revised Oct 2023); published in Management Science 2025, 71(12), 10144-10164. https://www.nber.org/papers/w30886
- Method: field experiment, about 500,000 jobseekers on an online labour marketplace; some got algorithmic writing assistance on their résumés.
- Result: about 8% more hires for the assisted group; no evidence employers were less satisfied.
- Limits: one marketplace (freelance work, not salaried jobs); the abstract does not say whether the tool edited or generated text; authors disclose consulting for the marketplace.
- Relevance: good writing matters, and AI-style help does help. So "we write better than you" is not our edge. **Supports a decision** (do not sell the writing itself) and **only hypothesises** that human judgement adds on top.

**F2. AI cover letters made applications look more alike and the signal weaker.** Cui, Dias and Ye, arXiv:2509.25054 (Sep 2025, revised Nov 2025). https://arxiv.org/abs/2509.25054
- Method: difference-in-differences around the launch of an AI cover-letter tool on a large hiring platform; observational.
- Result: callbacks rose, while the link between how well a letter fitted the job and the chance of a callback fell by about 51%; employers appeared to lean on other signals.
- Limits: observational; the abstract page gives no effect sizes beyond that; one platform.
- Relevance: generic AI text may lose value as more people use it, so specificity and checked facts are where a human can matter. **Hypothesis only.**

**F3. LLM screeners may prefer AI-written résumés.** University of Maryland Smith School working paper (preprint, simulated screening, self-preference 67-82%). **Weak**; not used in copy or decisions. A single-author SSRN synthetic study on a similar theme is weaker still.

**F4. How many people use paid help versus AI.** Novoresume 2026 survey: 3.7% of US workers had used a professional writer or coach; 42.6% had used AI; 55.8% of Gen Z. Source is a CV-software vendor; method and sample not verified here. Relevance: suggests a paid niche beside a large AI habit. **Hypothesis only; do not quote on the site.**

**F5. A competitor funnel.** TopResume offers a free CV review that leads to paid packages priced roughly $149 to $699+ (observed earlier in this project). Relevance: free review then paid is a normal pattern in this market; our price is much lower. Says nothing about outcomes. **Context only.**

### Free samples, frequency, referrals, urgency

**F6. Free trials of services can reduce perceived risk, but for services whose quality is hard to judge buyers need other quality signals, and trials can backfire.** Journal of Services Marketing (2018), survey experiment, n=396. Limits: self-reported intentions, general services, not careers. Relevance: supports the free CV check as a sample, and says the sample must itself show quality (three specific fixes), not just exist. **Supports a decision with low confidence.**

**F7. Email frequency.** Manufacturing & Service Operations Management (2022), field experiment with a car-wash subscription: two emails two weeks apart improved retention; fatigue appeared after the second. Limits: one company, subscription retention, not job seekers. Relevance: justifies a conservative cap (at most 2 promotional emails per rolling 14 days per person) as an assumption we then measure. **Hypothesis.** The "optimal number of emails" claims in vendor blogs were not found in peer-reviewed work; unverified claims are excluded.

**F8. Referred customers can be worth more.** Schmitt, Skiera and Van den Bulte, Journal of Marketing 75(1), 2011, 46-59; one German bank, roughly 10,000 customers; referred customers had lower churn and higher lifetime value per secondary summaries (figures not independently confirmed). A 2015 replication (Armelini, Barrot, Becker) found mixed results. Relevance: referrals are plausible but not guaranteed to be valuable for us. **Hypothesis.** We promise no incentive.

**F9. False urgency is treated as misleading.** UK Competition and Markets Authority, action over countdown-style pressure selling (Wowcher, 2024). Relevance: no countdowns, no "only 3 spots left" unless true and counted; the free-check "limited number each week" line needs a real number (08, RK-11). **Supports a decision.**

### Sending rules (official pages)

**F10. Google email sender guidelines**, https://support.google.com/a/answer/81126 (no date shown; footer 2026; requirements effective 1 Feb 2024).
- All senders: SPF or DKIM; valid forward and reverse DNS; TLS; spam rate in Postmaster Tools kept below 0.3% (the page also says aim for below 0.10%); do not impersonate Gmail From headers; From header should carry one address.
- Bulk senders (5,000+ messages a day to Gmail): SPF and DKIM and DMARC, aligned From domain, and one-click unsubscribe (List-Unsubscribe and List-Unsubscribe-Post headers) plus a visible link.
- Relevance: we are far below 5,000 a day, so the bulk rules do not apply today, but the all-sender rules do, and a From address at gmail.com that Brevo cannot sign for is the weak point. **Supports the domain recommendation.** Whether Gmail routes such mail to spam in practice is an inference, not something this page states.

**F11. Yahoo sender best practices**, https://senders.yahooinc.com/best-practices/ (undated). All senders: SPF or DKIM, spam rate below 0.3%. Bulk senders: SPF and DKIM, DMARC at least p=none and passing, aligned From domain, one-click unsubscribe, honour unsubscribes within 2 days. The page does not define "bulk". **Supports a decision:** we adopt the 2-day unsubscribe standard for ourselves.

**F12. ICO guidance on email marketing (PECR)**, https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/electronic-mail-marketing/ (undated; says it is under review because of the Data (Use and Access) Act).
- Individuals (including sole traders): specific consent, or the soft opt-in for your own previous customers who bought or negotiated for something similar, if they could opt out when you collected their details and can in every message.
- The soft opt-in does not cover prospective customers or bought lists.
- Every message needs a simple opt-out; keep a suppression list; do not disguise identity.
- The page does not address service messages.
- Relevance: UK recipients. **Supports** separate consent for tips and offers.

**F13. Asking for consent by email can itself be marketing.** ICO enforcement in 2017 (two businesses fined £70,000 and £13,000 for emails asking about marketing preferences), as summarised by law firms and enforcement blogs (White & Case, Bird & Bird and others). Primary ICO decision notices not retrieved; the sources predate current UK data law changes. Relevance: we must not send "please opt in to our tips" emails to existing contacts. **Supports a decision** (consent is collected at forms only), **with the caveat** that I have not read the primary notices.

**F14. Republic of Cyprus.** Law 112(I)/2004 as amended: prior consent for email marketing to natural persons, with a narrow existing-customer exception for similar products where the person could opt out at collection and each use. The Commissioner for Personal Data Protection's notice of April 2024, as summarised by Harris Kyriakides, says consent must be affirmative, informed, freely given and unambiguous, comes from the recipient, can be withdrawn at any time, and that an SMS or email that itself asks for consent is against the law. Chambers' guide reports fines up to EUR 20 million or 4% of turnover. Primary texts not retrieved; all via secondary summaries. **Applicability to us is uncertain:** Brevo shows the business address as "Kyrenia - North Cyprus", and whether Republic of Cyprus law reaches a business located there is a legal question (08, RK-14). Relevance: even if it does not apply, it matches the ICO position, so the design is the same either way.

**F15. FTC CAN-SPAM guide for business**, https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business (page edited Jan 2024). Eight requirements: accurate headers; non-deceptive subject lines; identify the message as an ad; a valid physical postal address; a clear opt-out; honour opt-out within 10 business days and keep the mechanism working at least 30 days; you cannot contract away responsibility to a vendor. Transactional or relationship messages must be mainly that content; a promotional subject line or promotional content at the start makes it commercial. Penalties up to $53,088 per email. Relevance: US recipients. **Supports** the rule "no promotion inside service messages" and a postal address in every marketing email.

**F16. EDPB Guidelines 05/2020 on consent** (adopted 4 May 2020): consent must be freely given, specific, informed and unambiguous, by a clear affirmative act; bundling purposes weakens it. Relevance: two purposes, two choices. **Supports a decision.** (Cited from earlier research; primary page not re-fetched in this pass.)

**F17. UK Data (Use and Access) Act 2025.** Secondary summaries: higher PECR fines (up to £17.5m or 4% of turnover) and changes to soft opt-in for charities; commencement timing partial or unclear. Relevance: UK rules are moving; check before launch. **Uncertain.**

### Brevo (official documentation unless noted)

**F18. Free plan limits.** Brevo help centre "What are the limits of the Free plan?" https://help.brevo.com/hc/en-us/articles/208580669-FAQs-What-are-the-limits-of-the-Free-plan: 300 sends a day, unused sends do not roll over; a campaign to more than 300 contacts delivers 300 on the scheduled day and the rest must be requeued; transactional mail over the cap waits in a retry queue of up to 1,000, beyond which it is dropped; no expiry. Test sends count.

**F19. Automation contact limit.** Several third-party reviews say the Free plan lets 2,000 contacts into automations; Brevo's own pages were not retrievable in readable form and the counting window (lifetime or monthly) is disputed. **Unverified.** Live account read (F24) shows marketing automation is enabled on the plan.

**F20. Webhooks.** https://developers.brevo.com/docs/marketing-webhooks and /docs/transactional-webhooks list the events (marketing: spam, opened, click, hard_bounce, soft_bounce, delivered, unsubscribe, contact_deleted, contact_updated, list_addition, proxy_open; transactional adds blocked, invalid_email, deferred, request). The pages say **nothing about authenticating the sender of a webhook** and give no general retry schedule (coupon events are documented as at-least-once, deduplicate by event_id). Relevance: any webhook endpoint we ever add must be treated as unauthenticated (secret path token, idempotent). Not needed under the recommended architecture.

**F21. IP security.** https://developers.brevo.com/docs/ip-security: when "Block unknown IP addresses" is on, requests from unauthorised IPs are blocked even with a valid key; CIDR ranges allowed; the page says nothing about serverless or dynamic IPs. Relevance: this is why the API failed from cloud sessions; it would also fight Vercel functions. **Supports** avoiding a Vercel-to-Brevo server path unless needed.

**F22. Contact, double opt-in and events API.** Create contact (attributes must already exist; `updateEnabled` defaults to false; `forceMerge`), double opt-in confirmation endpoint (email, `includeListIds`, `redirectionUrl`, template with `{{ params.DOIurl }}`), and custom events (`POST /v3/events`, event name letters, digits, dash, underscore, up to 255 characters; properties up to 50 KB; returns 204). No documented endpoint creates an automation; Brevo's builder is the dashboard.

**F23. Blocklist behaviour.** Brevo help articles and developer reference: blocklisted contacts are kept so you do not re-import them by mistake; the update endpoint can clear the blocklist flag; imports default to updating existing contacts. Community posts describe awkward bulk resubscription. **Official statement on what a form or API upsert does to a blocklisted contact not found.** Relevance: we must test it (06, T5) and never write to blocklisted contacts.

**F24. Live account state** (read through the Brevo connector, 24 Oct 2026): see A10 and A11 in 01. Evidence for what exists today.

**F25. Brevo's own blog states that list-unsubscribe headers are enabled by default** (https://www.brevo.com/blog/how-to-add-unsubscribe-link-to-email). Vendor claim; verify by inspecting a test email's headers (06, T6).

### Copy and tone

**F26. Tone, clarity, plain language.** Nielsen Norman Group's four tone dimensions (small effect: about half a point to one point on a five-point scale, 50 US respondents); Mailchimp's "clear is more important than entertaining"; Monzo's read-aloud and "clarity and kindness"; Australian Style Manual on plain language; ICO on layered privacy notices. Details and URLs in `drafts/voice-and-copy-guide.md`. Directional, practitioner-grade. **Supports** short, plain copy; does not prove it lifts conversions.

## Source register

| ID | Source | Type | Date | Method / population | Main limitation | Used for |
|---|---|---|---|---|---|---|
| F1 | NBER w30886 / Management Science 2025 | Peer-reviewed, field experiment | 2023, 2025 | ~500k jobseekers, one marketplace | Not salaried jobs; tool scope unclear; author conflict | Decision (don't sell writing) |
| F2 | arXiv 2509.25054 | Preprint, observational | 2025 | One platform, DiD | No effect sizes seen; unreviewed | Hypothesis |
| F3 | UMD Smith working paper; SSRN | Preprint | 2025 | Simulated screening | Simulated, unreviewed | Not used |
| F4 | Novoresume survey | Vendor survey | 2026 | US workers, method unverified | Vendor, unverified | Context only |
| F5 | TopResume pricing and funnel | Competitor observation | 2026 | Public site | No outcomes | Context only |
| F6 | J Services Marketing | Peer-reviewed, survey experiment | 2018 | n=396 | Intentions, not behaviour | Low-confidence decision |
| F7 | MSOM car-wash experiment | Peer-reviewed, field experiment | 2022 | One subscription business | Other industry | Hypothesis (cap) |
| F8 | Schmitt et al., J Marketing | Peer-reviewed | 2011 | One bank | Replication mixed | Hypothesis |
| F9 | UK CMA, Wowcher | Regulator action | 2024 | Enforcement | Summary not read in full | Decision (no false urgency) |
| F10 | Google sender guidelines | Official | undated, eff. Feb 2024 | Provider rules | Inference on gmail.com From | Decision (domain) |
| F11 | Yahoo sender best practices | Official | undated | Provider rules | No bulk definition | Decision (2-day unsubscribe) |
| F12 | ICO PECR email marketing | Official regulator | undated, under review | Guidance | Silent on service messages; UK only | Decision (consent) |
| F13 | ICO enforcement via law firms | Secondary | 2017-2018 | Fines for consent-seeking emails | Secondary, dated | Decision with caveat |
| F14 | Cyprus Law 112(I)/2004 and Commissioner notice via law firms | Secondary | 2024 | Summaries | Secondary; applicability uncertain | Decision with caveat |
| F15 | FTC CAN-SPAM guide | Official regulator | Jan 2024 edit | Guidance | US only | Decision |
| F16 | EDPB Guidelines 05/2020 | Official | 4 May 2020 | Guidelines | Not re-fetched in this pass | Decision |
| F17 | DUAA 2025 summaries | Secondary | 2025 | Summaries | Commencement unclear | Uncertainty flag |
| F18 | Brevo Free plan help | Official | current | Documentation | Test sends count | Decision (caps) |
| F19 | 2,000-contact automation limit | Third-party | 2026 | Reviews | Unverified, window disputed | Open item |
| F20 | Brevo webhook docs | Official | current | Documentation | Silent on authentication | Decision (avoid) |
| F21 | Brevo IP security | Official | current | Documentation | Silent on serverless | Decision |
| F22 | Brevo API reference pages | Official | current | Documentation | No automation-create | Decision |
| F23 | Brevo blocklist help and community | Official + community | varies | Docs and posts | No official statement on upserts | Test required |
| F24 | Live account read | Direct observation | 24 Oct 2026 | Connector reads | Snapshot | Fact |
| F25 | Brevo blog on unsubscribe header | Vendor | current | Blog | Vendor claim | Test required |
| F26 | NN/g, Mailchimp, Monzo, Style Manual, ICO | Practitioner and guidance | various | See voice guide | Small samples | Copy rules |

## Recommendation-to-evidence matrix

Confidence: **High** = official rule or direct observation; **Medium** = one decent study or consistent regulator position; **Low** = adjacent or secondary evidence; **Assumption** = judgement, no source.

| # | Recommendation | Evidence | Confidence | What would change our mind |
|---|---|---|---|---|
| R1 | Do not sell "better writing"; sell judgement, checked facts and a finished, delivered package | F1, F2 | Low (adjacent) | Customer interviews saying writing quality is the reason they pay |
| R2 | Free CV check stays as the main sample, with three specific fixes | F6, F5 | Low | Free-check to order rate after 30 checks |
| R3 | Two separate consents: job alerts, and CV tips and offers | F12, F14, F16 | High (regulators agree) | Legal advice that one wording suffices |
| R4 | No consent-request emails to existing contacts; consent only at forms | F13, F14 | Medium (secondary sources) | Reading ICO and Commissioner primary texts |
| R5 | Customers join promotions only by an unticked box at order intake | F12, F14, F16 | High | Lawyer approves relying on soft opt-in |
| R6 | Service emails carry no promotion | F15, F12 | High | none |
| R7 | Get a sending domain before any send to more than a handful of outsiders | F10, F11 | Medium (inference on Gmail routing) | A sent test showing inbox placement from the Gmail identity (does not prove it for others) |
| R8 | Honour unsubscribes within 2 days (target same day) | F11, F15 | High | none |
| R9 | Cap promotional emails at 2 per 14 days per person | F7 | Low | Our own unsubscribe and complaint data |
| R10 | No countdown timers, no unstated scarcity | F9 | High | none |
| R11 | Use Brevo as marketing store only; keep service emails in Gmail | F18, F20, F21 and project facts | Medium | Order volume above the Stage 2 trigger (07) |
| R12 | Measure clicks, enquiries and orders; ignore opens | Phase 10 rationale; F18 limits | Medium | none |
| R13 | Referrals: invite, never reward | F8 (mixed) | Low | Consumer-law advice on incentives |
| R14 | Single opt-in stays for job alerts; revisit double opt-in once a domain exists | KT decision 24 Oct; F16 (does not require double opt-in) | Medium | Bounce rate above 2% or bot sign-ups |
| R15 | Short, plain, warm copy; one next step | F26 | Low (directional) | Our reply and enquiry data |

## Gaps I could not close

1. Primary texts: ICO enforcement notices, the Cyprus Commissioner's notice, Law 112(I)/2004 itself, EDPB guideline text (re-fetch).
2. Brevo plan page (readable), automation caps, DPA availability and its sub-processors list.
3. Evidence on double opt-in effects on deliverability and conversion (not researched to evidence standard; do not claim either way).
4. Other markets' rules (US state laws, Canada CASL, Turkey KVKK, Nigeria NDPA and others) and which audiences you actually reach. Your analytics will tell you where visitors come from; the answer changes which rules matter most.
5. WhatsApp Business policy on business-initiated messages outside the customer-service window and opt-in. I know the general shape; I did not verify the current policy here, so no design depends on messaging people first on WhatsApp.
