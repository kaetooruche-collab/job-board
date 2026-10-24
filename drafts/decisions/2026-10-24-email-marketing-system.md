# Decision review: the Yireh Careers email system (Brevo)

Status: PROPOSED, built as far as the tools allow (templates and draft campaign are in Brevo; lists and automations need KT's hands, see `drafts/brevo-setup-guide.md`). Written 24 Oct 2026.
Evidence labels: **[Established]** from a named source or measured by us; **[Hypothesis]** reasoned, to test; **[Assumption]** needs validation.

## 0. What KT asked for, and a correction
KT wants Brevo to become the email system for the whole business: subscribers get a welcome series; each buyer group (Essential, Professional, Executive, LinkedIn Growth) lands on its own list and receives its own follow-ups; campaigns go to chosen lists with a "do not send" exclusion; copy is punchy, brief, emotional and well-calibrated. 

Correction to my earlier answer ("nothing in Brevo triggers the order emails"): that was too absolute. Brevo's automation editor has a **Contact added to list** trigger (KT's screenshots), plus Custom event, Contact added manually and Contact matches custom filters. So a list-based design works: *KT adds a person to a list, the automation fires.* What I said still holds for the **operational** emails (order received, documents delivered, branding plan, privacy request): they need attachments, come from the Gmail mailbox, and happen one at a time, so they stay in Gmail. Everything that is **marketing or relationship-building** belongs in Brevo, and that is what this design covers.

## 1. Research summary (what shapes the design)
| Finding | Source | Confidence |
|---|---|---|
| Welcome series: 3-6 emails over 1-2 weeks, first one immediately, spaced 2-3 days; welcome emails get roughly 2-4x the opens/clicks of regular newsletters (figures vary widely by vendor) | Inbox Army, Klaviyo, Scalero, Stripo, GetResponse via web search | Directional (vendor blogs) |
| Post-purchase: confirm at once, check in early, ask for a review 7-14 days after delivery, upsell 14-21 days after delivery and by behaviour rather than calendar, keep sequences to 2-4 emails, stop when the person replies or opts out | QuickEmailVerification, Flowium, Bloomreach, Hustler Marketing | Directional (ecommerce-heavy) |
| Lead-magnet nurture: about 5 emails over 7-12 days, never more than one a day; soft offer mid-sequence, direct ask at the end | MailerLite, Tomba, Sequenzy | Directional |
| Job-alert digests: weekly is the common default; keep promotions out of the digest; skip empty sends; cap listings per email; let people change preferences | Cavuno, Articuler, Acedit | Directional (practitioners) |
| Open rates are inflated by Apple Mail Privacy Protection, so judge by clicks and click-to-open | ActiveCampaign, Omnisend, Pushwoosh | Established (widely reported) |
| Subject lines: studies disagree on length (about 25-50 characters is the common range); personalisation helped click rate in an old study; **no reliable evidence** found on emotional triggers or on single-CTA vs multi-CTA | Belkins, GetResponse, Attentive, Experian | Weak |
| Testimonial ask: soon after completion for simple services, weeks later for outcome-based ones; keep it under 30 seconds to read; resolve problems first | Elegant Themes, Wyzowl, Reply.io | Directional |
| Sunset policy: flag at about 30 days, win-back at 60-90, suppress about two weeks later; suppress rather than delete; weekly senders use shorter windows | Mailpro, Omnisend, Mailmodo | Directional |
| UK PECR: marketing email needs consent, or the **soft opt-in** for existing customers (bought or negotiated to buy; similar products; a simple opt-out at collection and in every message). It does **not** cover prospective customers or new contacts | ICO | **Established** |
| UK CMA treats false urgency (fake countdowns, "hurry") as misleading; Wowcher gave refunds in 2024 | CMA via law-firm summaries | Established for UK |
| Brevo free plan: 300 emails a day; up to 2,000 unique contacts can enter active automations; campaigns to more than 300 recipients deliver only 300 per day; **campaign tags are not allowed** (we hit this) | Brevo help (via search), Brevo API error | Established |
| Brevo cannot authenticate Gmail addresses, so mail from a Gmail sender goes out under Brevo's own sending identity | Brevo help | Established |

What the research could not tell us: the best send day, the best subject-line style for our readers, whether emotional copy lifts conversion, and how often our audience will tolerate. Those become tests (section 7).

## 2. Design
### Lists (KT creates in Brevo; I have no list-creation tool)
| List | Who is on it | How people get on | Used for |
|---|---|---|---|
| Job alert subscribers (existing #11) | Everyone who signs up on the site | The sign-up form | Welcome series, weekly digest, monthly tip, sunset |
| Free CV check requested | People who ask for the free check | KT adds them when sending the result | 2-email follow-up |
| Customers: Essential / Professional / Executive | Buyers whose order is **complete** and who said yes to occasional emails | KT adds them (see consent, section 3) | Post-order sequence by package |
| LinkedIn Growth: active | Monthly clients | KT adds when the month starts | Service emails only (renewals stay on WhatsApp for now) |
| **Do not send** | Anyone who asked to stop, bounced badly, complained, or went through the sunset | Automation or KT | **Excluded from every campaign** under Advanced options |

No custom attributes are needed: every email uses only the first name (a contact's FIRSTNAME, with "there" as the fallback).

### Flows (automations; KT builds, exact steps in the setup guide)
| Flow | Trigger | Emails | Exit |
|---|---|---|---|
| Welcome | Added to Job alert subscribers | W1 now, W2 day 3 (value), W3 day 7 (free CV check; skipped for customers) | End; or added to Do not send |
| Free-check follow-up | Added to Free CV check requested | F1 day 3, F2 day 8 (skipped if they ordered) | End |
| After an order (3 versions) | Added to Customers: X | P1 day 1 (check-in), P2 day 10 (feedback ask), P3 day 21 (upsell: Essential add-ons, Professional LinkedIn Growth; Executive at day 30), P4 day 60 (how's the search, forward to a friend) | End |
| Sunset | No click on any email in about 60 days (build in week 8) | S1, then Do not send if no click in 14 days | Suppressed, not deleted |

### Campaigns (manual, scheduled, to a chosen list, **exclude: Do not send**)
- **Weekly jobs digest.** Generated by `scripts/make_digest.py` from the live feed (6 roles, one per company, spread across levels, clear eligibility first, worldwide or region-wide roles preferred, no promotion inside, skip the send if fewer than 3 fresh roles). Tell Claude "weekly email" and a draft is created in Brevo with a test sent to you; you schedule it.
- **Monthly tip** (T1 is the first): one idea, one soft offer.
- **Re-engagement** is the sunset flow.

### Cadence rules
One email a day at most per person; at most the digest plus one lifecycle email in a week; no new automation sends to the same person within 24 hours of another. Welcome and post-order flows pause naturally because they are short.

### Copy rules (see `drafts/voice-and-copy-guide.md`, plus these for marketing)
Punchy and brief (40-70 words); warm and emotionally honest (name the real feeling: the silence after applying, the wasted evening on a role you can't take); one call to action; **no false urgency, no fake scarcity, no outcome promises, no claims that a role or package suits a background**; one legal fact where it matters (the 30-day deletion of a free-check CV). Subject lines 25-45 characters, plain and specific.

## 3. Consent and privacy: decisions KT needs to make
1. **Two lawful routes, and our data fits them unevenly.** [Established, ICO] Subscribers consented to *job alerts*. Sending them promotional emails about CV services goes beyond that, and the soft opt-in does not cover people who are not yet customers. **Recommendation:** make the promise at sign-up explicit: "Weekly remote jobs, plus the occasional note about our CV and LinkedIn services. Unsubscribe any time." That is a change to the Brevo form and the line under it on the home page (site change, needs your yes to merge). Until then keep promotion in the lifecycle emails to a single soft line (W3, T1) and out of the weekly digest.
2. **Customers vs our "we delete your details in 90 days" promise.** The order-complete email says we delete documents and details within 90 days. Keeping buyers in Brevo for follow-ups conflicts with that. **Recommendation:** at completion, ask on WhatsApp: "Want occasional tips and offers by email? Reply yes." Only those who say yes go into the Customers lists; everyone else is simply deleted on schedule. Service emails (the Gmail ones) are unaffected.
3. **Privacy page.** It should name Brevo as the email provider and say what is kept and for how long. I will draft the wording; merging it to the live site is your call.
4. **The domain.** [Established] Brevo cannot authenticate a Gmail sender. At 3 subscribers this does not matter. Before the list passes roughly 100-250 (and certainly before sending to strangers), a domain with proper email authentication is the single biggest deliverability fix.

## 4. Limits we are working inside
- Free plan: 300 emails a day (test sends count toward it: about 22 used today), 2,000 unique contacts into automations, no campaign tags. A weekly digest to more than 300 people needs a paid plan or a staggered send.
- No Brevo key is visible to this session (no environment variable, the API returns "not authorised"). I work through the Brevo connector, which can create and edit **templates and campaigns, read lists and contacts, and send tests**. It cannot create lists, contacts, attributes, segments or automations, and cannot delete anything. KT added a network secret to the environment. Tried on 24 Oct: neither this session nor a fresh one could see a Brevo key (no environment variable; Brevo's API answered 401 to keyless calls on /v3). A second session reported that the proxy may inject the key only for `/api/v1/` paths, which I could not verify and which would not cover Brevo's `/v3` API. Likely fix: add the key as a plain environment variable (for example `BREVO_API_KEY`) in the cloud environment settings and start a new session. Until then the lists are created by hand (5 minutes). Automations remain UI-only either way.

## 5. What is built
| Item | Where |
|---|---|
| 13 lifecycle emails W1-T1 | Brevo templates 40-52 (W1 reuses 40); sources `drafts/emails/build_marketing.py`; review sheet `drafts/email-copy-review.md` |
| Weekly digest generator | `scripts/make_digest.py` (tested in `tests/test_digest.py`) |
| Sample digest campaign (draft, no recipients, not scheduled) | Brevo campaign 53 |
| Customer-service emails | Gmail pack `drafts/gmail-customer-emails.md` (templates 34-39 remain as fallback) |
| Lists and automations | **KT**, following `drafts/brevo-setup-guide.md` |

## 6. Template map
W1 = 40, W2 = 41, W3 = 42, F1 = 43, F2 = 44, P1 = 45, P2 = 46, P3 Essential = 47, P3 Professional = 48, P3 Executive = 49, P4 = 50, S1 = 51, T1 = 52. Old sets 20-33 can be deleted by KT; 34-39 are the fallback transactional versions.

## 7. How we will know it works
Judge by **clicks, replies and enquiries**, not opens. Track weekly:
| Metric | What it tells us | Starting expectation |
|---|---|---|
| Click-to-open rate on the digest | Is the content relevant | Compare week to week; no benchmark we trust |
| Unsubscribes and spam complaints per send | Are we too frequent or too promotional | Investigate above about 0.5% unsubscribes or any complaint |
| Free CV check requests per 100 welcome-series recipients (W3 and T1 clicks) | Does the soft offer work | Unknown; this is the number to learn |
| Orders per 100 free checks | Does the follow-up convert | Unknown |
| Replies to P1/P2 | Service quality and testimonials gathered | Count them |
| Sunset: share of subscribers suppressed | List health | Review at day 90 |
Tests, one at a time and only once the list is large enough to read (a few hundred): digest send day (Tuesday vs Thursday), subject style (plain vs a feeling), digest with and without pay shown.

## 8. Rollout
1. This week: KT creates the lists and the Welcome automation (30 minutes), sends the tests to self, decides section 3.
2. Week 2: Free-check follow-up and the After-order automations; first weekly digest campaign (Claude creates the draft, KT schedules).
3. Week 4: first monthly tip. Week 8: sunset flow.
4. When the list passes about 100: buy the domain and authenticate it, then move the sender off Gmail.

## 9. Risks
- Over-emailing a small list teaches people to ignore us: the cadence rules cap it.
- Consent drift: promotions to people who signed up for jobs. Mitigated by the sign-up wording change and a soft touch until then.
- Copy that is too clever: every email is plain; judge by replies.
- Template editing: templates cannot be edited by "dragging" in Brevo because they were created from HTML (they open in the code editor). Fine for our use.

## Sources
ICO electronic mail marketing: https://ico.org.uk/for-organisations/direct-marketing-and-privacy-and-electronic-communications/guide-to-pecr/electronic-and-telephone-marketing/electronic-mail-marketing/ ; Brevo custom events and the automation trigger list: Brevo's help article and KT's screenshots of the automation editor (24 Oct 2026); Brevo free plan limits and domain authentication: Brevo help centre (via search); CMA / Wowcher: https://www.rpclegal.com/snapshots/consumer/autumn-2024/cma-secures-undertakings-from-wowcher-and-4-million-customer-refunds/ ; welcome series, post-purchase, lead-magnet, job-alert and sunset guidance: vendor and practitioner blogs surfaced by web search on 24 Oct 2026 (treat as directional).
