# Facts that are not in the repository, collected 16 Nov 2026

Labels: Established = read first-hand on the date shown. Reported = a source says so.

## 1. Email (Brevo account KAYZ Global Ltd, checked 16 Nov)
- Established: list "Job alerts" (id 11) has 3 contacts, all KT's own. Lists "Career tips", "Check result sent", "Order completed" have 0.
- Established: the only digest sent since the rebrand was campaign 105, "Weekly jobs 2026-10-30": 3 delivered, 2 opens (1 is an Apple Mail privacy pre-load), 0 clicks, 0 unsubscribes. Earlier campaigns (5 Oct, 21 Sept) went to the same 3 contacts.
- Established: the scheduled routine "Tuesday weekly job email" last fired on 10 Nov and failed in 5 seconds with `ROUTINE_RUN_FAILURE_REASON_ACCESS_DENIED`. No digest appears as sent for 3 or 10 Nov. It is due again on Tue 17 Nov at 08:20 Istanbul. Likely cause: its Brevo and Gmail connector permissions need re-authorising. Only KT can do that.

## 2. Traffic (GoatCounter, snapshots in `drafts/analytics/`, newest `GC-2026-11-10.md`)
- Established: all-time 410 page views, 174 events; last 7 days 101 views. Home page 211 views all time, services 17, verify 3, free-check 2.
- Referrers last 7 days: direct 54, Facebook (several spellings) about 24, the site itself 11, "Greenhouse" 6 and "Ashby" 3 (visits whose referrer is a hiring-system page; Inference: people returning from an apply page).
- Events all time: apply-click 17, filter-country 18 (the most recent value sent was "worldwide only"; the breakdown by country is not recorded), filter-level 15, cv-click 7, search-used 5, no-results 3. Conversion events (signup, free-check, order form): 0.

## 3. Link checking (from `data/metrics.json` history and `data/link_state.json`)
Failure rate by refresh, newest first (share of apply links that could not be checked, all HTTP 403 on Greenhouse hosts): 22.1%, 4.0%, 10.4%, 11.1%, 15.2%, 4.6%, 16.5%, 18.8%, 21.8%, 11.3%, 6.7%, 10.4%, 17.2%, 9.0%. Published listings stayed between 976 and 1,022 because unchecked links are kept for up to three refreshes. 15 listings reached the third consecutive miss on the newest run. Inference: the GitHub runner is being throttled by Greenhouse; the checker's own baseline has drifted upward and now treats 10% to 20% as normal, so the circuit breaker is less sensitive than designed.

## 4. Independent studies on location restrictions (read in full on 1 Nov, still current)
- Job Badger, "Remote Jobs Report", 16 Sept 2026: 993 remote listings from four public boards; 92% name a country, region, city or time zone; 38% US-only; 6% set no location rule; a US resident could apply to 53%, India 12%, Nigeria 11%. Job Badger's own product is AI cover letters plus a posting checker, so it is an adjacent competitor.
- WorkinVirtual, "Remote Job Eligibility Index 2026", 13 Aug 2026: 112 listings; 11.6% worldwide; 61.6% US-restricted; 99.1% sent applicants to an external site.
- Our own board: 12 of 1,006 worldwide (1.2%), 724 country-named. Our share is lower than both studies. Do not present our numbers as "the market".
- Reported only: "only 3,015 of 119,649 indexed Himalayas remote listings are open to applicants from any country" (RoamJobs, October 2026). Not verified.

## 5. What leading remote boards say above the fold (Firecrawl, read 1 Nov, verbatim)
FlexJobs: "The #1 Job Site to Find Work From Home Jobs. No Ads, Scams, or Junk"; "We spend 200+ hours per day hand-screening each job". Himalayas: "Get matched with your next remote job. Then land it with AI."; "Join 250,000+ job seekers"; "No credit card required". Working Nomads: "Get Hired for the Best Fully Remote Jobs". Remote OK: "#1 Remote Job Platform", "1,137,608+ remote jobs", "#OpenSalaries". Job Badger: "Your application, prepared by AI". Wellfound: "Find work that matters." None leads with where you can apply from.

## 6. Structured job-data providers available through Firecrawl (catalogue read 16 Nov, free to browse, billed per call)
Employer career-site providers: Ashby, Greenhouse, Lever, Workable (also its public board jobs.workable.com), SmartRecruiters (including search across all employers), iCIMS, Workday (myworkdayjobs), SAP SuccessFactors (respects robots.txt), JOIN (join.com), Wayfair careers. Board and aggregator providers: Indeed (US plus 26 country sites), Glassdoor US, ZipRecruiter US, JobLeads (40 country sites), Built In, Y Combinator jobs. Company and jobs data vendors: TheirStack, BlitzAPI, Crustdata, Sumble. Not checked: coverage, completeness of original posting dates, location fields, per-record price, or whether each provider's terms allow republication. Fable should read the provider contracts (`/library/jobs/` through the Firecrawl library tools) before relying on any of them.

## 7. Where the earlier sourcing research is
`research/job-sources-100.md` (15 Oct 2026) is an earlier study of 100 sources and strategies with tags USE, TEST, LINK-OUT, PLATFORM, STRATEGY and a "not on the list, and why" section (Himalayas, We Work Remotely, Remote OK, Remotive, Jobicy, Jobgether, FlexJobs and others). Its findings predate the current site and some are stale; its legal reasoning is still the project's position. The terms check for Greenhouse, Lever and Ashby is `drafts/decisions/2026-10-31-ats-terms-check.md`.
