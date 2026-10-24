# Verified remote job board: brief for Claude Code (version 4)

Save this file as `CLAUDE.md` in the project folder so it is read at the start of every session. It replaces the earlier brief completely. If anything here conflicts with an older note, this file wins.

**Version 4 changes (KT, 2026-10-24), which override anything below that says otherwise:**
- **One brand: "Yireh Careers"** for the job board AND the career services (replaces the placeholder "TrueRemote"/`PROJECT_NAME` and "Kaeto Career Services"). The public address is `https://yirehcareers.vercel.app` until KT buys a domain; the old `northcyprusremotejobboard.vercel.app` redirects to it (temporary 307 in `vercel.json`). The name is applied by hand across `index.html`, `services.html`, `verify.html`, `privacy.html`, `thanks.html`, `kit.html`, `site-config.js`, `scripts/make_outputs.py`, `scripts/site_monitor.py`, `og-image.png` and the drafts; `tests/test_brand.py` fails if a retired name returns. Decision evidence: `drafts/decisions/2026-10-24-brand-name-and-founder-visibility.md`; naming checklist: `drafts/brand-name-checklist.md`. Trademark, language and handle checks for "Yireh" are NOT done; KT chose to launch first.
- **No personal name, face or photo on the brand or the public pages** (KT's rule). The "Who's behind this?" block was replaced by "How we work". Do not re-add a founder section, photo, first name or role line. WhatsApp and email replies are signed as the team.
- **KAYZ Global Ltd is not a registered company** (KT, 2026-10-24). Do not call it a company, "Ltd", or the operator on any page or email. The privacy page says Yireh Careers is run by an individual business owner in Kyrenia and is not a registered company (KT may change it after registering a company). The Brevo account label "KAYZ Global Ltd" in the Brevo rule below is only a label. Whop opens as an individual until a company exists.
- **Jobicy is excluded** (`USE_JOBICY = False` in `scripts/fetch_jobs.py`, BLOCK rule `source-date-not-original` in `scripts/qa_checks.py`): its dates are not the employer's original posting dates (evidence: `tests/fixtures/jobicy_dates.json`, LaunchDarkly 23 Oct vs 8 Oct on the employer's board). Only turn it back on if a source of truth for the date is found.
- **Card checkout is built but OFF** (`SITE.checkout.mode = 'off'` in `site-config.js`); the site orders by WhatsApp. It goes live only with real `https://whop.com/checkout/ch_...` URLs and mode `live`, after `drafts/whop-go-live-checklist.md`. KT has no bank account linked yet; do not block launch on it.
- **Post kit:** `/kit` (unlisted, noindex, no analytics) builds ready-to-copy posts for WhatsApp, Facebook, TikTok and Snapchat from the live feed, with `utm_source`-tagged links. KT posts by hand.

**Version 4.1 changes (KT, 2026-10-24), which override anything below that says otherwise:**
- **Board and kit:** the home page has an Experience row (All levels / Early career / Mid-level / Senior & leadership; `?level=early|mid|senior_plus`). The post kit defaults to "Entry-level and junior" (7-day window) with a group-country filter, and early posts link to `/?level=early`. Post wording must stay "entry-level and junior", never "for students/graduates" (copy rule: do not claim a role suits a background). Senior roles stay on the board; there is no global seniority default.
- **Strategic review (read before any inventory, sourcing, seniority or pricing decision):** `drafts/decisions/2026-10-24-board-strategy-icp-inventory-seniority.md`. Its status is PROPOSED. Main points: no scraping and no shrinking until the validation plan (who is in KT's channels, free-CV-check stage and country log, spot-check of 50 listings) has data; primary paying customer is a HYPOTHESIS (experienced non-executive professionals applying to remote roles), students and graduates are audience-building, executives inbound-only; the real supply gap is roles open to non-US readers (only 17 of 1,026 are worldwide), which more US-based Greenhouse/Ashby/Lever boards will not fix. Label every claim established, hypothesis or assumption. GoatCounter needs KT's login, so Claude has no traffic data.
- **Known data issues to fix with regression fixtures (CLAUDE.md quality rule):** about 26 of 96 early-career labels are doubtful (licensed roles, engineers and account executives asking 2 years at high pay, "Senior Program Manager" labelled entry); "junior" is mechanically 1-2 years asked; 8 employer sites (31 listings) did not visibly show the posting when opened; 6 Carvana links are bot-blocked and unverified; 103 rows are location variants of the same role (793 distinct roles).

**Copy and voice (KT, 2026-10-24): read `drafts/voice-and-copy-guide.md` before writing any email, WhatsApp message, post or page copy.** KT's feedback: the first emails were too long and abrasive ("you are talking to human beings, not machines"; legal compliance must not produce terrible copy). Rule: short, warm, plain, one next step per message; say each legal point once, where it matters, in one friendly sentence; contractions; no stacked disclaimers; emails 60-110 words. Brevo templates 34-40 (Yireh set, sender id 4) hold the rewritten emails; the WhatsApp library and `drafts/whatsapp-business-setup.md` (generated by `drafts/build_whatsapp_setup.py`) hold the rewritten messages. The website copy has NOT been reviewed against this guide yet. **How customer emails are sent (KT asked 24 Oct):** nothing in Brevo triggers the order emails, by design. Orders happen on WhatsApp; Brevo cannot attach documents, cannot authenticate a Gmail sender and should not hold customer details. Customer emails (order received, onboarding complete, delivered, branding plan, order complete, privacy request) are sent from the yirehcareers@gmail.com mailbox using Gmail templates built from `drafts/gmail-customer-emails.md` (generated by `drafts/emails/build_emails.py`). Brevo is for the newsletter only: the sign-up form adds people to list #11 and an automation sends template 40; the weekly jobs email is a manual campaign. Brevo templates 34-39 are a fallback for when a domain and an order trigger (for example Whop webhooks) exist.

**Version 3 changes (KT, 2026-10-15), which override anything below that says otherwise:** the audience is every job seeker (students, graduates, mid-career, specialists, career changers, freelancers), not only entry-level people; listings span all fields (administration, customer service, sales and marketing, finance and accounting, technology, healthcare, education, legal, HR, and more), not mainly tech; senior and leadership roles are allowed and filterable by level; "remote" is decided by reading the whole posting (see Work-arrangement classification below); remote roles restricted to a country or region are published with the restriction shown, and unconfirmed-but-marketed-as-remote roles are published with a plain "not confirmed" label. Build for the person searching, not for the scraper.

## Working principles (KT, 2026-10-15): apply to every project and every new session
- Evaluate KT's ideas independently. Neither agree nor disagree without adequate reasoning.
- Research consequential technical, legal, regulatory, privacy, security and financial questions using current, authoritative sources.
- Identify assumptions, counterevidence, alternatives, uncertainty, risks and long-term costs.
- Consider GDPR where applicable, cookies, data protection, intellectual property, licensing, security, dependencies, maintenance and financial viability.
- Require a documented decision review (`drafts/decisions/`) before substantial or high-risk implementation.
- Require KT's explicit approval before consequential or irreversible actions (for example: creating things in Brevo that cannot be edited or deleted afterwards, merging to main, spending money, publishing terms).
- Verify changes with appropriate tests and checks. Never claim verification that was not performed.
- Use proportionate reviews for minor tasks.
- Before ANY action in Brevo (create, change, send), first call `accounts_get_account` and check that `companyName` is "KAYZ Global Ltd" (account email kaetooruche@gmail.com). If it is not, do not create or change anything and tell KT. (Rule from KT, 2026-10-17.)
- KT may override any rule by saying OVERRIDE.

## Quality system for the job feed (KT asked for this on 2026-10-17: "we keep finding something new")
Never tell KT the job board is "good to go" from the classifier alone. The layers are:
1. `tests/` : unit tests, plus `tests/fixtures/regressions.json` (real postings that once broke the classifier).
2. `scripts/qa_checks.py` runs inside every refresh and does not reuse the classifier's reasoning. BLOCK rules hold a listing back (logged in `data/removed.log` and `data/review_queue.json`); WARN rules and drift are in `data/qa_report.md` and `data/qa_history.json`. A sudden drop in listings stops the run and keeps the previous data.
3. `scripts/site_monitor.py` (`.github/workflows/site-monitor.yml`, every 3 hours) checks the LIVE site: pages load, data is fresh, tracking present, forbidden wording absent, prices/email/WhatsApp are the approved ones, sample of apply links open.
4. `scripts/spot_check.py` + `drafts/weekly-audit-prompt.md`: random listings opened and compared with their real postings. This is the only layer that tests truth. Report the real numbers (for example "14 of 15 correct"), never "looks fine".
Rule: every bug found gets (a) the real text added to `tests/fixtures/regressions.json`, (b) the fix, (c) if it is a class of bug, a rule in `qa_checks.py` with tests, (d) an old-versus-new comparison on real postings before it ships. Before saying the board is ready, read `data/qa_report.md` and report the numbers.

## KT's to-do list
The single master list of what KT must do or decide is `drafts/kt-todo.md`. When KT asks "what do I need to get done?" (or similar), read that file and show the open items, most urgent first, in plain language. Update it whenever something is done, added or decided, and commit the change. `drafts/launch-checklist.md` is history only.

## Scope of this chat and repository work
This project covers the public job board and the career services page (and their pipeline, emails, pricing and monitoring). KT's personal pharmacy job search is a separate project that lives in `jobsearch/` and is handled in its own chat (`jobsearch/CLAUDE.md`, `jobsearch/HANDOFF.md`). Do not work on it from the job-board chat unless KT asks; do not mix its items into `drafts/kt-todo.md`.

## Who you are working with
KT is a marketing professional, not a developer. Explain every step in plain language, one step at a time. Do the typing and running yourself. Ask KT only for things nobody else can do: logins, approvals, decisions. After each phase, summarise in plain language what now works and what KT must do next.

## The product
A free job board of verified remote jobs at every experience level and in every field, for job seekers anywhere. It is NOT tied to any country or city, and nothing in the code identifiers, site copy or URLs should name one. Country and region names appear only as data taken from listings (and in `data/geo_lexicon.json`), for example the eligibility label on a card.

Revenue comes from KT's paid CV and LinkedIn services, sold by WhatsApp (+90 533 822 5854) and email. The board earns trust and traffic. Later revenue lines (a seeker plan, employer listings, partners) wait for gates; do not build them.

**Name.** Yireh Careers (decided by KT on 2026-10-24; see Version 4 changes). The contact email is **yirehcareers@gmail.com** (KT created it on 2026-10-24; the single mailbox for the website, clients and the Brevo sender "Yireh Careers", sender id 4); keep it in `site-config.js`. Newsletter signup is **single opt-in** (KT decided 2026-10-24). Brevo cannot authenticate Gmail addresses, so a domain is needed before sending to more than a handful of people.

Already in place and to be kept:
- Static site on Vercel (project `north_cyprus_remote_job_board`, public address yirehcareers.vercel.app). A copy of the previous site is in the folder KT downloaded (`remotenc-oct5`); ask KT for its location. Keep the visual style: navy hero, job cards, category filters, search. Remove the country-specific hero copy.
- Email signup posts to a Brevo embedded-form URL. Reuse the exact `action` URL and hidden fields from the old `index.html`. Never put an API key in client code.
- GoatCounter analytics for `kayzglobal.goatcounter.com`.
- A holding page is live on the old project while this is built.

## Why the old board was taken down
The old `jobs.json` was written by hand. Most links went to company homepages or search pages. Pay and descriptions were summaries, not taken from postings. "New this week" meant new to our board. One claim (health-science graduates earning premium pay on a Mercor role) was unsupported. KT's standard is trust: the readers are stressed job seekers.

## Listing standard: a listing is published only if ALL hold
1. The URL opens the specific posting, never a homepage, search page or category page.
2. The posted date and time come from the source, using the original posting date rather than the last edit where the source gives both.
3. The posting reads as remote: fully remote, remote with stated location restrictions, or marketed as remote but unconfirmed (labelled as such). Hybrid, on-site and self-contradicting listings are not published. Where applicants may live is shown as the employer states it ("Worldwide", a country or region, or "Eligibility unclear"); nothing is assumed to be worldwide.
4. Pay is shown only if the posting states it; otherwise show "Not stated". Never invent or estimate figures.
5. The source is credited and linked.
6. The link passed a check at the last run, and the page shows no closed-role wording ("no longer accepting", "expired", "position filled", "closed").
7. It is not commission-only and charges no applicant fee. Experience level is recorded and filterable; senior titles are NOT excluded. Show KT a sample of what was removed and why (`data/removed.log`, `data/review_queue.json`).

A page that still loads does not prove a role is open, so age matters. Drop anything posted more than 30 days ago, and anything past an apply-before date when the source gives one (the ATS feeds almost never do).

Copy rules for the whole site, emails and messages: never write "no work permit needed", "guaranteed", "the only job board", or claim a role suits a degree or background unless the posting says so. Tell users to check each employer's eligibility.

## Work-arrangement classification (the heart of the pipeline)
`scripts/classify.py` reads the title, location, structured hints and the FULL description of every listing and returns: work arrangement (fully remote / remote with geographic restrictions / remote unclear / hybrid / on-site), office attendance, geographic eligibility (with the employer's own wording kept), experience level (from the experience the posting asks for, not just the title), multi-label category, employment type, quality flags, evidence quotes, confidence and unresolved questions. Rules: no single keyword decides; negations and company-level wording ("some roles may be remote") do not count as proof; contradictions go to `data/review_queue.json` instead of being silently resolved; hybrid and on-site are excluded from the main feed; remote-unclear is published only with a visible "not confirmed" label. Tests live in `tests/test_classify.py` and must pass before a change to the classifier ships. The Claude Code skill `.claude/skills/classify-job-listing/SKILL.md` describes how to review borderline listings.

## Trust rules to publish on the site ("How we verify" page) and in the channel
1. We never charge a job seeker to apply or to see a listing's apply link.
2. We never post a listing that asks applicants to pay.
3. Commission-only roles are excluded.
4. Every listing shows its source, posting date and when we last checked it.
5. Every claim we publish links to the posting that supports it.
6. A wrong listing is corrected in public within one day.

## Sources, in build order
1. **Employer applicant-tracking-system public endpoints** (Greenhouse, Lever, Ashby; other systems only after checking). They give the employer's own posting URL, location and timestamps. Reported fields: Greenhouse `absolute_url`, `first_published`, `updated_at`; Lever `hostedUrl` and `createdAt` in epoch milliseconds; Ashby `jobs` list. Verify each against live data; do not trust this summary. Needs a curated company list: propose 40 or more companies that hire worldwide in entry-level roles (customer support, operations, data, moderation, writing), with the evidence for each, and let KT approve it. Vendor terms for aggregation are NOT read yet: read them in Phase 0. Build a removal process for any company that asks.
2. **We Work Remotely RSS feeds.** Allowed for anyone if links are attributed back to We Work Remotely. Per-category feeds exist. On the one listing KT showed, "Apply now" sent applicants to create a WWR account first, so the card must say so. Full WWR Terms of Service NOT read yet: read them in Phase 0.
3. **Listings KT verifies by hand**, only if they meet the standard.
4. **Employer-submitted form**: Phase 3, do not start without KT's go-ahead.

**Excluded:** the Remotive API. Its terms say showing its jobs to collect signups or email addresses is a breach, and this site has an email signup. Candidates for later, ONLY after reading their terms: Remote OK API, Himalayas, Working Nomads.

## Phase 0: discovery (before writing site code)
1. Fetch live data from the ATS endpoints for a sample of at least 15 companies from the proposed list, and from the WWR feeds. Print the fields that exist and what each link points to.
2. Read the terms for Greenhouse, Lever, Ashby and We Work Remotely. Report plainly whether aggregation, email capture, or showing listings beside paid services is restricted.
3. Count listings after each filter: total, worldwide, within 30 days, not commission-only, not senior, link check passed. Show KT the counts and 10 sample listings with direct URLs, opening each to confirm the page matches.
4. Stop and report. **Gate 1:** at least 10 suitable listings a week survive. If fewer, do not build on these sources alone; propose options (more companies, more sources, hand-verified listings, or the employer form).

## Phase 1: pipeline and site
- GitHub repository (KT creates a free account and approves access). Connect it to a new Vercel project so every commit redeploys. (Connecting Git stops drag-and-drop updates on that project.)
- A script (Node or Python; keep it simple) runs on GitHub Actions every 6 hours plus a manual trigger: fetch, normalise, filter, check links, write the data file and `data/removed.log` (dropped listings with the reason), commit only when something changed. Poll gently: Greenhouse publishes no hard limits but advises every few hours.
- Record fields: id, title, company, category, jobType, regionAsStated, salaryText (null if not stated), postedAt, applyBefore (null if none), sourceName, sourceUrl, firstSeenAt, lastVerifiedAt, flags.
- Pages: home (filters by category, job type and posted-within; search; a "last updated" stamp); one page per job (title, company, source link, posted date and time shown relative, e.g. "2 days ago", AND absolute, in the visitor's own time zone, plus last-checked time and an Apply button to the posting); "How we verify"; "Report a listing" (email or WhatsApp link); services page; subscribe form.
- Services page (updated 18 Oct 2026, KT approved `drafts/decisions/2026-10-18-pricing-and-offer-structure.md`): three packages, Essential $29, Professional $49 (labelled "Recommended"), Executive $149 (Professional + personal branding strategy + 12 posts over 30 days + targeted connection building each week of the 30-day service, aiming towards 500+ total connections or 100 new relevant ones if already above 500; NO open-ended continuation; the 30 days start when onboarding is complete). At day 30 the client can continue with LinkedIn Growth, $99 a month, month to month, paid by arrangement on WhatsApp, nothing automatic. Add-ons: cover letter $15 and LinkedIn setup $25 (Essential orders), extra revision $10, second CV $15, 48-hour priority $15, interview preparation sheet $29. Free quick CV check (one per person, CV emailed not sent on WhatsApp, deleted within 30 days if no order) and a "Get a CV for this role" button on each job card, both opening WhatsApp. Do not change prices, package names, revision limits (2, 3 and 3), the 12-post commitment, the 30-day period or the connection aim without KT's explicit approval, and do not publish refund, approval or other service terms KT has not decided. Keep the Executive wording free of any promise to continue until a number is reached (`scripts/site_monitor.py` fails on it).
- Search: JobPosting structured data on each job page, with `datePosted` = the original posting date, expired jobs removed, markup matching the visible page. Because we do not own these listings, check Google's CURRENT job-posting rules before adding markup, and tell KT what you find.
- Measurement: GoatCounter events on every apply click, with source and listing id (check GoatCounter's current event documentation), and tagged links for channel posts.
- Two sections, clearly labelled: "Open listings" (from the pipeline) and "Platforms you can sign up to" (a hand-kept `platforms.json`). Each platform entry is verified by opening its signup page, shows no pay claim unless that page states it, and shows no posted date.
- Empty state if there are no listings: say so plainly and point to the email signup.
- Responsive to a 360px phone width, readable in dark mode, visible keyboard focus.
- Email consent: Brevo labels double confirmation as recommended for GDPR, and the current form sends none. Ask KT to decide; do not change it silently.
- At relaunch: the old Vercel link is in WhatsApp posts and groups. Replace the old project's holding page with a redirect to the new site, or tell KT the old link will stop working.

## Phase 2: channel and email output
Each run also writes (a) a ready-to-post WhatsApp message of three to five new listings with direct links and posting times, and (b) weekly, a ready-to-paste Brevo email (HTML) in the style of the existing weekly email, with campaign name, subject line and preview text. KT posts and sends by hand. Subject lines must not overstate pay or eligibility.

## Phase 3: employer "post a job" form
Do not start without KT's go-ahead.

## Not part of this build
Payments: KT decided on 2026-10-15 that there is no payment processor on the website (reason: KT had no Whop account at the time). On 2026-10-23 KT chose to add Whop hosted checkout, sandbox first. Current rules: (1) only Essential and Professional get a "Pay by card" button, linking to a Whop-hosted checkout link (no payment form, API key or webhook on this site; client code holds only public checkout URLs in `site-config.js`); (2) the buttons show only when `SITE.checkout.mode` is `live` with `https://whop.com/checkout/...` URLs; `sandbox` mode shows them only on a page opened with `?pay=test` and with a TEST banner, and must never be live (tests and `scripts/site_monitor.py` fail on it); (3) Executive, add-ons, LinkedIn Growth, bank transfer and crypto stay on WhatsApp (KT sends the details in the chat); (4) documents are sent only by email; (5) `thanks.html` is information only, noindex, and never claims a payment was verified; (6) do not add any other payment processor, a paywall on listings or a seeker subscription; (7) going live (production URLs, mode `live`, merge to main) needs KT's explicit approval after the checklist in `drafts/whop-go-live-checklist.md`. WhatsApp message wording lives in `drafts/whatsapp-messages.md`; decision reviews: `drafts/decisions/2026-10-15-payments.md`, `2026-10-19-whop-payments.md`, `2026-10-23-whop-checkout-integration-plan.md`.

## Acceptance tests (show KT the evidence for each)
- 100% of published listings pass the link check at deploy time, and each links to the employer's or source's specific posting.
- Every listing has a postedAt value and displays it relative and absolute in the visitor's time zone.
- No published listing is older than 30 days or past its apply-before date.
- Ten random published listings opened by you and confirmed to match their card; show URLs.
- A deliberately broken URL, a deliberately commission-only test listing and a deliberately senior-title test listing are all dropped.
- No country or city name appears in the site copy, code identifiers or page titles.
- The scheduled GitHub Action runs successfully twice in a row.
- GoatCounter shows the click events.
- The signup form still reaches Brevo list #11 (test with KT's email).
- Mobile and dark-mode check.
- The "How we verify" page matches the six trust rules.

## Do not
- Scrape HTML pages of sites whose terms forbid it.
- Use the Remotive API.
- Put API keys or secrets in client code or commit them to the repo.
- Publish any listing, pay figure or claim you could not verify.
- Add anything that names a country or city. (One exception approved by KT on 2026-10-17: the legal notice on the privacy page states where the operator is based.)

## Open unknowns: resolve by checking, do not assume
- Which fields each ATS endpoint and the WWR feed carry for original posting time and for region.
- Vendor terms for Greenhouse, Lever, Ashby and WWR; terms for Remote OK, Himalayas and Working Nomads.
- How many suitable entry-level worldwide listings exist (Gate 1).
- Whether Google accepts job markup for listings we do not own.
- Whether listed employers can contract or pay people in every country. This cannot be verified from feeds, so the site must tell users to check each employer's eligibility.
