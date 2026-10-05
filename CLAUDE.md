# Verified remote job board: brief for Claude Code (version 2)

Save this file as `CLAUDE.md` in the project folder so it is read at the start of every session. It replaces the earlier brief completely. If anything here conflicts with an older note, this file wins.

## Who you are working with
KT is a marketing professional, not a developer. Explain every step in plain language, one step at a time. Do the typing and running yourself. Ask KT only for things nobody else can do: logins, approvals, decisions. After each phase, summarise in plain language what now works and what KT must do next.

## The product
A free job board of verified, worldwide-eligible, entry-level remote jobs, for job seekers anywhere. It is NOT tied to any country or city, and nothing in the code, copy or URLs should name one.

Revenue comes from KT's paid CV and LinkedIn services, sold by WhatsApp (+90 533 822 5854) and email. The board earns trust and traffic. Later revenue lines (a seeker plan, employer listings, partners) wait for gates; do not build them.

**Name.** The final name is not chosen yet. Use the placeholder `PROJECT_NAME` in code and copy, kept in ONE config file so a rename is a one-line change. The current contact email (remotenc.jobs@gmail.com) and the old site name will change at the rename; keep them in the same config.

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
3. The posting text states it is open to applicants worldwide.
4. Pay is shown only if the posting states it; otherwise show "Not stated". Never invent or estimate figures.
5. The source is credited and linked.
6. The link passed a check at the last run, and the page shows no closed-role wording ("no longer accepting", "expired", "position filled", "closed").
7. It is not commission-only, charges no applicant fee, and has no senior title (head of, director, VP, chief, principal, staff, senior). Propose the exact word lists, and show KT a sample of what was removed and why.

A page that still loads does not prove a role is open, so age and apply-before dates matter. Drop anything posted more than 30 days ago or past its apply-before date.

Copy rules for the whole site, emails and messages: never write "no work permit needed", "guaranteed", "the only job board", or claim a role suits a degree or background unless the posting says so. Tell users to check each employer's eligibility.

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
- Services page: describe the CV and LinkedIn services and link to WhatsApp. Prices are placeholders: do NOT publish prices until KT confirms them.
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
Payments. Services are paid for by hand (bank transfer or the client's local method), so do not add Stripe, PayPal or any checkout. No paywall on listings. No seeker subscription yet.

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
