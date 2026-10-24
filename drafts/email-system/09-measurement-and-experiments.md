# 09 · Measurement and experimentation plan

Status: PROPOSED (Phase 10 deliverable). **There are no baselines.** Brevo has 3 contacts, two campaigns with 0 clicks, and no order register. Every number below is a *metric to start counting*, not a target. Thresholds named "alert" are our own tripwires, not industry benchmarks.

## Principles

1. **Clicks, enquiries, orders, revenue.** Opens are unreliable (privacy protections such as Apple Mail Privacy Protection and automated scanners inflate or hide them); Brevo's `proxy_open` webhook event exists for exactly this reason (F20). Opens are not used for any decision, including the dormant rule.
2. **Count what a person did.** A click on the free-check button, a submitted form, a WhatsApp message with a source code, a payment confirmed by KT.
3. **Be honest about sample size.** See "What small numbers can and cannot tell us" below.
4. **Never run conversion tests on consent wording.** The wording is chosen for clarity (EDPB, F16), not for opt-in rate.

## Metrics

| Metric | Definition | Source | Reliable today? | Notes |
|---|---|---|---|---|
| New eligible subscribers by source | New contacts on a list with consent recorded, by `LEAD_SOURCE` | Brevo | Yes once forms set source | Excludes the 2 unverified contacts until resolved |
| Tips opt-in rate | Tips box ticked ÷ form submissions, per form | Brevo | Yes once forms exist | |
| Consent withdrawal | Unsubscribes ÷ sends, per purpose | Brevo | Yes | Needs T7 |
| Hard bounce rate | Hard bounces ÷ delivered | Brevo | Yes | Alert at 2% |
| Spam complaint rate | Complaints ÷ delivered | Brevo | Yes (Brevo events) | Alert at 0.10% (Google's own monitoring target, F10) |
| Link clicks per send | Unique clickers ÷ delivered | Brevo | Mostly (scanners can click links; treat early-second clicks as suspect) | |
| Qualified enquiry rate | WhatsApp or form enquiries carrying a source code ÷ unique clickers of a CV-service CTA | Register / enquiry log | **Manual** | Codes in the prefilled WhatsApp text |
| Free-check requests per week | Count of submissions | Form + register | Yes once the form exists | Also the quota counter |
| Enquiry-to-purchase | Orders ÷ enquiries | Register | Manual | |
| Revenue by package and source | Sum of confirmed payments | Register | Manual | Revenue is KT-confirmed only |
| Add-on attachment rate | Orders with add-ons ÷ orders | Register | Manual | |
| Repeat purchase | Customers with a second order | Register | Manual | |
| Referral activity | WhatsApp or form enquiries naming a referrer | Register | Manual (asked in intake) | No incentives, so self-reported |
| Delivery completion | Orders delivered on the promised date | Register | Manual | Operational quality |
| Deliverability by provider | Gmail, Outlook, Yahoo delivery and complaint rates | Brevo reports; Google Postmaster Tools once a domain exists | Partly | Postmaster needs a domain |
| Automation failures, duplicate sends | Weekly audit (06) | Audit script | After Phase 12 | Target zero |

## Source tracking

- Email links carry `utm_source=brevo&utm_medium=email&utm_campaign=<email id>&utm_content=<cta>` (the existing site convention, `kit.html`). **Verify** that GoatCounter reads `utm_*` as referrer data (not confirmed in this pass); fallback `?ref=<email id>`.
- WhatsApp links carry a short code in the prefilled text (for example `from:ct2`) so KT can write the source in the register without any tool.
- The free-check form stores its own source in `LEAD_SOURCE`.

## What small numbers can and cannot tell us

A quick calculation, with its assumptions stated: to detect a difference between two email versions in a rate with a baseline of 5% (for example link clicks), at 5% significance and 80% power, using a simple normal approximation:

| Recipients per version | Smallest difference detectable (approx.) |
|---|---|
| 100 | about 8.6 percentage points |
| 500 | about 3.9 points |
| 1,000 | about 2.7 points |

So with a list in the low hundreds, **almost any A/B test is noise**. Rule: below roughly 1,000 recipients per version we do not A/B test; we look at the numbers, read replies, talk to people, and change one thing at a time.

## Proposed experiments (all conditional on sample size)

| ID | Hypothesis | Audience | Primary metric | Guardrails | Sample note | Duration | Decision rule |
|---|---|---|---|---|---|---|---|
| E-1 | A short follow-up after the free-check result (FC-1) leads to more orders than none | Free-check requesters with tips consent; alternate weeks send / hold out | Orders within 30 days of the result | Unsubscribe and complaint rate for FC-1 | Likely under 20 people per arm: **cannot prove causality** | 12 weeks or 40 eligible people, whichever is later | Keep FC-1 unless unsubscribes or complaints exceed alert levels; do not claim it "works" from the result |
| E-2 | Digest on Tuesday gets more clicks than Thursday | Job-alert list | Unique clickers per delivered | Unsubscribes | Weak power | 8 weeks, alternating | Switch day only if Thursday wins in at least 6 of 8 pairs |
| E-3 | An honest "when AI is enough" line in CT-2 does not reduce free-check requests | Tips list | Clicks on the free-check button | Unsubscribes | Weak power | First 100 recipients | Keep unless clicks are clearly lower than CT-1 and CT-3; qualitative reading of replies decides |
| E-4 | 2 promotional emails per 14 days is a safe cap | Tips list | Unsubscribe rate per promotional email | Complaints | Observational only | Ongoing | Lower the cap if unsubscribes per email exceed 1% or complaints exceed 0.10% (our alerts, not benchmarks) |
| E-5 | The "Get a CV for this role" button on job cards produces enquiries | Board visitors | WhatsApp enquiries with source code `from:jobcard` | None | Needs a code on that button | 8 weeks | Keep; outcome is a count, not an experiment |

Holdouts: used where it is cheap and harmless (E-1). Never withhold a service message.

## Reporting rhythm (what KT looks at and when)

| When | What | How long |
|---|---|---|
| Weekly, 10 minutes | Register updated; overdue deletions; "Needs consent audit" segment empty; digest sent; any "stop" replies applied; free-check count against the cap | 10 min |
| Monthly | Clicks, qualified enquiries, orders by source, unsubscribes, bounces, complaints; one decision about what to change | 30 min |
| Quarterly | Dormant sweep; privacy page and consent wording check; re-read ICO and Commissioner pages | 1 hour |

## Tripwires (when to change the design)

| Signal | Action |
|---|---|
| Digest list over about 200 recipients | The 300-a-day cap starts to matter with tests and automations; consider staggering or a paid plan |
| Orders over about 15 a month | Re-open option B (07) |
| Bounce over 2% or odd signups | Add double opt-in (07, F22) |
| Complaints at or above 0.10% | Pause promotional sends and review |
| Free-check requests over the weekly cap for 3 weeks | Raise the cap or change the promise on the site |
