# Verified remote job board: brief for Claude Code (version 3)

Save this file as `CLAUDE.md` in the project folder so it is read at the start of every session. It replaces the earlier brief completely. If anything here conflicts with an older note, this file wins.

**Version 3 changes (KT, 2026-10-15), which override anything below that says otherwise:** the audience is every job seeker (students, graduates, mid-career, specialists, career changers, freelancers), not only entry-level people; listings span all fields (administration, customer service, sales and marketing, finance and accounting, technology, healthcare, education, legal, HR, and more), not mainly tech; senior and leadership roles are allowed and filterable by level; "remote" is decided by reading the whole posting (see Work-arrangement classification below); remote roles restricted to a country or region are published with the restriction shown, and unconfirmed-but-marketed-as-remote roles are published with a plain "not confirmed" label. Build for the person searching, not for the scraper.

## Who you are working with
KT is a marketing professional, not a developer. Explain every step in plain language, one step at a time. Do the typing and running yourself. Ask KT only for things nobody else can do: logins, approvals, decisions. After each phase, summarise in plain language what now works and what KT must do next.

## The product
A free job board of verified remote jobs at every experience level and in every field, for job seekers anywhere. It is NOT tied to any country or city, and nothing in the code identifiers, site copy or URLs should name one. Country and region names appear only as data taken from listings (and in `data/geo_lexicon.json`), for example the eligibility label on a card.

Revenue comes from KT's paid CV and LinkedIn services, sold by WhatsApp (+90 533 822 5854) and email. The board earns trust and traffic. Later revenue lines (a seeker plan, employer listings, partners) wait for gates; do not build them.

**Name.** The final name is not chosen yet. Use the placeholder `PROJECT_NAME` in code and copy, kept in ONE config file so a rename is a one-line change. The current contact email (trueremote@gmail.com) and the site name will change at the rename; keep them in the same config.

Already in place and to be kept:
- Static site on Vercel. A copy of the previous site is in the folder KT downloaded (`remotenc-oct5`); ask KT for its location. Keep the visual style: navy hero, job cards, category filters, search. Remove the country-specific hero copy.
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
- Services page: describe the CV and LinkedIn services and link to WhatsApp. KT confirmed three packages: Essential $29, Professional $49, Executive $99 (Executive = Professional + personal branding + 30-day LinkedIn growth service; 12 posts over 30 days; target of 500+ connections, timing depends on the client's starting point; the 30 days start when onboarding is complete). Do not change prices, package names, revision limits (2, 3 and 3), the 12-post commitment, the 30-day period or the 500+ target without KT's explicit approval, and do not publish refund, approval or other service terms KT has not decided. See `drafts/services-audit.md`.
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
Payments are handled by KT's Payhip hosted checkout (decided by KT after this brief was written): the site only links to Payhip product pages via keys in `site-config.js` and never handles card data; until a product key is filled in, the button opens a WhatsApp message instead. Do not add any other payment processor or checkout. No paywall on listings. No seeker subscription yet.

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
- Add anything that names a country or city.

## Open unknowns: resolve by checking, do not assume
- Which fields each ATS endpoint and the WWR feed carry for original posting time and for region.
- Vendor terms for Greenhouse, Lever, Ashby and WWR; terms for Remote OK, Himalayas and Working Nomads.
- How many suitable entry-level worldwide listings exist (Gate 1).
- Whether Google accepts job markup for listings we do not own.
- Whether listed employers can contract or pay people in every country. This cannot be verified from feeds, so the site must tell users to check each employer's eligibility.
