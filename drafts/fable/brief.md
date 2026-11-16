# Brief for Claude Fable 5.2: a full review and revamp plan for Yireh Careers

You are working for KT, the owner of Yireh Careers. KT is a marketing professional, not a developer. This brief is self-contained. Everything you need is in this file, in the files it names, and on the live web. You may use web research and run local read-only analysis. You may not change the live site (section 8).

Your job is to find the highest-value changes to this business and give KT a plan he can trust and act on. You are the senior strategist here. Use your judgment. This brief gives you the goal, the constraints and the evidence rules; it does not give you steps, because you will find better steps than any list written in advance.

## 1. The business

Yireh Careers is a free job board of remote jobs. Its single promise: each job shows where applicants can be based, in the employer's words, or says when that is unclear. Revenue is meant to come from paid CV, cover letter and LinkedIn services sold on WhatsApp: Essential $29, Professional $49, Executive $149 (30-day service), add-ons ($10 to $29), and LinkedIn Growth at $99 a month. The free CV check is the entry offer. The site launched on 24 Oct 2026 at https://yirehcareers.vercel.app.

How it works today: a Python job on GitHub Actions runs every 6 hours. It reads the public job feeds of Greenhouse, Lever and Ashby for about 285 configured company boards, classifies each posting (is it really remote, who can apply, what level), checks the link, and publishes about 1,000 listings from about 160 companies. The site is static pages on Vercel with one small serverless function for forms. Email is Brevo's free plan. Analytics is GoatCounter. A card-checkout (Whop) is built but switched off.

## 2. What is true today (measured, 16 Nov 2026)

Treat these as facts unless you find them wrong. Verify anything you build a recommendation on.

- **Traffic is tiny.** 410 page views all time, 101 in the last 7 days; about 30 home-page views in the last week. Facebook is the only visible referrer. 17 apply clicks all time.
- **The funnel produces nothing yet.** Zero email sign-ups, zero free-check form submissions, zero order forms, all time. 7 WhatsApp clicks about a CV. No paid order is recorded anywhere (KT to confirm).
- **Email.** One digest has been sent since the rebrand (30 Oct): 3 delivered, 2 opens, 0 clicks. The list has 3 subscribers, all KT's own contacts. The Tuesday routine that sends the digest failed on 10 Nov with an access error and no digest went out on 3 or 10 Nov.
- **The listings are concentrated.** All three sources are hiring-software feeds. Of 1,006 listings, 12 are open worldwide, 13 regional, 724 name specific countries (mostly the US), 249 are unclear, 8 timezone-based. Top 10 employers are 15% of listings. Software is the biggest category (207), then sales (160), healthcare (102). Early-career roles are about 85 of 1,006.
- **Link checking is fragile.** About 4% to 22% of apply links come back blocked (HTTP 403) to the GitHub runner on any run, all on Greenhouse hosts, which looks like throttling. A grace system keeps listings visible, but this is a warning about scaling sources.
- **Decisions already made (do not reopen without new evidence, and say so if you do):** the board stays free with no paywall on listings; one brand "Yireh Careers"; navy compact hero with an outcome-first headline; "Get Job-Ready" is the header button; no platforms/other-boards list; Jobicy and the Remotive API are excluded; card checkout stays off until KT approves; Executive wording makes no promise to continue; no country or city named in site copy; KT's name and photo appear on the services page only.

## 3. The goal this work serves

See `drafts/fable/kt-inputs.md`. It holds KT's goal, time and money limits, and risk appetite. Where an answer is marked DEFAULT, KT has not confirmed it: use it, and say in your memo that it was a default.

## 4. The questions to answer

Answer all of these. Where a question's answer depends on facts we do not have, say what you assumed and what would change your mind.

**A. Who and what.** Who is the person most likely to pay, and what is the sharpest true promise to that person? The existing hypothesis is experienced, non-executive professionals applying to remote roles, plus people outside the US who are filtered out by location. Test it against the evidence in the files, not against what sounds good.

**B. Getting visitors.** At about 30 home views a week, what actually gets the first thousand qualified visitors, ranked by expected visitors per hour of KT's time? Cover search and Google for Jobs (including whether we may use JobPosting markup for listings we do not own), programmatic pages such as "remote jobs open to applicants in [country]", communities and groups (the rules of Reddit and Facebook groups are in the files), the WhatsApp channel, partnerships, and anything we have not thought of. Be specific about what to do in the first 30 days.

**C. The product.** Audit every corner of the board, the services page, the free-check page, the emails and the WhatsApp flow: layout, information order, copy, mobile, speed, accessibility, trust signals, calls to action, the guided finder, filters and country selection. Say what to change, what to cut, and what to leave alone, with a reason for each. Include retention: what would make a visitor come back next week?

**D. Offer and pricing.** Are the services, prices, add-ons, guarantees and the free check the right offer for the people we can actually reach? Use competitor prices, willingness-to-pay evidence, and purchasing power across countries. Recommend changes as options with the evidence for each. Nothing you recommend is applied without KT's yes. Consider new products or revenue lines (for example employer listings, a seeker plan, country-specific application kits, partnerships), but flag which of these conflict with the decisions in section 2 and what gate each would need.

**E. Sourcing: the 100-sites question.** KT wants a system that scrapes jobs from over 100 job sites in every country, because most listings come from the same three places. Treat that as a hypothesis, not a requirement. Decide what serves the promise in section 1. Specifically:
  1. What would more sources add for our actual audience (people who need to know where they can apply)? Quantify where you can: for example, what share of listings on national boards are remote at all, and what share are open to applicants abroad.
  2. For each candidate source type (more hiring-software feeds such as Workable, Recruitee, Personio, Teamtailor, BambooHR, SmartRecruiters; aggregator APIs; remote-only boards; national boards; company career pages; structured-data providers such as Firecrawl's jobs providers), decide whether it is legal and permitted for us to use it (read the terms and robots rules; do not guess), how we would access it, how complete its original posting dates and location data are, and what it costs to maintain.
  3. Give a ranked roadmap of the sources worth adding, each tested on a real sample of at least 20 postings, and a clear recommendation on the 100-sites idea. The file `drafts/fable/inputs/country-job-boards-unverified.csv` is a list KT received from another AI. It has not been verified. Check it before you rely on any line of it. Note that it contains some countries and sites that need a sanctions or terms check before any use.
  4. Describe the architecture that would let us add and monitor sources safely at scale, including how we verify links when the checker is already throttled, how we keep dates honest, and how we keep wrong listings out. Keep it simple enough for a small team to maintain.

**F. Trust, law and claims.** Audit every public claim on the site, emails, WhatsApp and posts against the overall impression a reader gets (FTC net impression; EU Unfair Commercial Practices Directive articles 6 and 7), consent and privacy (GDPR), terms of use of every source, and accessibility. List anything that must change before we grow.

**G. Measurement and learning.** With this little traffic, how do we learn quickly? Name the few numbers that matter, the instruments we are missing, the experiments that can work at this scale (including qualitative ones), and the rules for deciding when to keep, change or stop something.

**H. Sequencing.** Put it together: what to do in the next 30, 60 and 90 days, what to stop doing, what each step needs from KT's time, what it depends on, and how we will know it worked.

## 5. Non-negotiables

- Never invent a listing, number, quote or source. Never publish or recommend publishing a claim we cannot verify.
- Do not recommend scraping any site whose terms or robots rules forbid it, or any approach that harms a site. If a source's terms are unclear, say so and treat it as not permitted until checked.
- Trust rules stay: we never charge a job seeker to apply or to see an apply link; we never post a listing that asks applicants to pay; commission-only roles are excluded; every listing shows source, posting date and last check.
- The brand voice is "we" and the team. Copy must be short, warm and plain. No "guaranteed", no "no work permit needed", no claim that a role suits a background.
- KT's money, time and risk limits in `kt-inputs.md` are real limits.
- Keep the project's own rules in `CLAUDE.md`, but treat its long history as context and not as a list of cautions to apply to your own work. Section 8 names exactly what you may do without asking.

## 6. Evidence rules

- Label every claim **Established** (you read it first-hand: a page, a file, a measurement; give the URL or file and the date), **Reported** (a source says so and you did not check it), **Inference** (your reasoning), or **Assumption**. Keep these labels visible in your deliverables.
- Prefer primary sources. For competitor and market claims, read the live page and quote it. One reported test is not proof; say how strong each piece of evidence is and how small our sample is.
- Use independent verification for the claims your top recommendations depend on. A fresh-context sub-agent that checks a claim against its source, without seeing your reasoning, is worth its cost; do not use sub-agents for ordinary reading.
- Argue against your own top five recommendations before you finalise them. Then say what would make each one wrong.
- If something you need is blocked or missing, say so, state the assumption you used, and carry on. A labelled assumption is better than a stall.

## 7. Using the project's files

Read these first, in this order: `CLAUDE.md`, `drafts/site-inventory.md`, `drafts/kt-todo.md`, `drafts/analytics/` (newest two files), `drafts/decisions/` (all), `research/job-sources-100.md`, `drafts/marketing/audience-research-and-icp.md`, `drafts/marketing/outreach-hooks-and-copy-by-platform.md`, `drafts/voice-and-copy-guide.md`, `drafts/fable/inputs/`. Inspect the live site (https://yirehcareers.vercel.app and its pages), `jobs.json`, `data/metrics.json`, `data/qa_report.md` and the code under `scripts/`, `api/`, and the page files. `python3 scripts/build_fable_context.py` assembles most of this into one file if that is easier.

## 8. What you may and may not do

You may, without asking: read any file in the repository; browse and search the web; use Firecrawl search and scrape; run local read-only scripts and analysis on files in the repository; create and edit files only under `drafts/fable/output/`.

You may not: change any other file; commit, push, merge or deploy; send any email or message; post anywhere; change Brevo, Vercel, GitHub settings or any account; contact anyone; spend money beyond Firecrawl credits for research. If a step would need any of these, write it as a recommendation for KT.

## 9. Deliverables

Write these files in `drafts/fable/output/`. Write for a low-context reader.

1. `00-memo.md`: the executive memo, two pages at most. The diagnosis in five sentences, the five bets you would make and why, what to stop, the 90-day plan on one screen, and the three decisions KT must make first.
2. `01-findings.md`: a table of every finding. Columns: id, area (A to H), finding, evidence label, source and date, impact (high/medium/low), effort, confidence.
3. `02-sourcing.md`: the answer to question E, including the tested sample for each recommended source and the architecture.
4. `03-product-and-ux.md`: the audit for question C, page by page, with specific changes written so a developer can build them without asking you.
5. `04-offer-and-pricing.md`: the analysis for question D, with options, evidence, and a test for each.
6. `05-visibility-plan.md`: the plan for question B, with the first 30 days in detail.
7. `06-trust-and-law.md`: the audit for question F.
8. `07-measurement.md`: the plan for question G.
9. `08-tickets.md`: at most 30 implementation tickets in priority order. Each: what and why, files or systems touched, acceptance tests, risk, and which model tier should do it (an everyday coding model should be able to build most of them).
10. `09-open-questions.md`: what you could not verify, what you assumed, and what you need from KT.

Put the key points first in every file. Use plain full sentences, one idea per sentence, and the same word for the same thing. Do not use a term you made up during the work. Write mostly prose and keep bullets for lists of separate items. Be as long as the content needs and no longer.

## 10. Finishing

Please avoid stopping while you still owe work this brief asks for. Be persistent. If you meet ordinary obstacles such as an error, a timeout, an empty result or a failing tool, diagnose them first, then work through them with the access you have. If something is clearly a hard blocker, such as access KT withheld or a rule in section 5, leave it alone, say plainly what you found, and look for another safe way to finish. Stopping before every deliverable exists is very rarely right. When you finish, give a short recap that stands on its own: what you found, what you wrote, and what KT should decide first.
