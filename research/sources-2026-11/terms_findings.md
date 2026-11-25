# Terms, robots and data checks per source (read 25 Nov 2026)

Standard (same as `drafts/decisions/2026-10-31-ats-terms-check.md`): (1) the vendor documents the read feed as public or it is the vendor's own public embed endpoint; (2) nothing in the vendor's terms forbids third parties reading or showing it; (3) robots.txt does not disallow it; plus the CLAUDE.md listing standard: (4) an original posting date exists; (5) the apply link opens the specific posting. Not legal advice.

| Source | 1 Public | 2 Terms | 3 Robots | 4 Original date | 5 Specific link | Verdict |
|---|---|---|---|---|---|---|
| Recruitee | Yes. Docs: the Careers Site API "does not require authorization and is available under your Careers Site address" | Terms: "This Careers Site is intended, among other things, to provide the public with a list of job opportunities, and therefore Subscriber's usage of the Careers Site is not intended to be private." | allowed | `published_at` | `careers_url` | **USE** |
| Personio | Yes. Help centre: "When you publish a job, you can find it in XML format at youraccount.jobs.personio.com/xml"; documented on developer.personio.de | not read (no clause found in docs) | allowed | `createdAt` | `/job/{id}` | **USE** (silent, like Greenhouse) |
| Workable | The widget endpoint used on customers' own sites | `workable.com/terms` read: no clause on scraping, third-party use or republishing found | allowed | `published_on` | `url` | **USE after a runner test**: every request from this environment got HTTP 429 |
| Breezy HR | Keyless JSON, "when the customer enables it" (third-party write-up; vendor docs not read) | not read | allowed | `published_date` | `url` | HOLD: read vendor docs first |
| JazzHR | Vendor help: XML feed "of all jobs in your account" for career-page integration | not read | allowed | none in feed (JobPosting on each page) | `url` | HOLD: one extra page fetch per job for the date |
| Rippling | Public board endpoint | not read | allowed (no robots.txt) | only in a per-job call | per-job | HOLD |
| BambooHR | Careers list endpoint | Terms prohibit use "with any robot, spider, other automated device, or manual process to monitor or copy any content from the Service" | allowed | not in list | yes | **NO** (terms) |
| Teamtailor | JSON feed | not read | **disallowed** | yes | yes | **NO** (robots) |
| SmartRecruiters | Posting API | not read | **disallowed** | yes | yes | **NO** (robots) |
| Pinpoint | | | **disallowed** | | | **NO** (robots) |
| Landing.jobs | API | | **disallowed** | | | **NO** (robots) |
| Workday | Internal JSON for each employer's own site | per-employer site terms, not read | allowed | `postedOn` is relative ("Posted 3 Days Ago") | yes | HOLD: no exact date, employer-specific hosts |
| Himalayas | Public API | API terms: "Show a visible link to the job on Himalayas"; "Do not pass them on to ... Google Jobs ... including through ... JobPosting structured data" | allowed | **No**: "pubDate: When the job was last updated" | `applicationLink` | **NO** (dates are not original; same reason as Jobicy) |
| Remote OK | Public API | In the API: "Please link back ... to the URL on Remote OK and mention Remote OK as a source" | allowed | cannot be checked: 0 of 100 latest jobs link to an employer's hiring page | Remote OK page | **NO for now** (dates unverifiable) |
| We Work Remotely | RSS | attribution allowed (Phase 0 note); full terms not read | allowed | `pubDate` (WWR's own date) | WWR page, apply needs a WWR account | HOLD (as before) |
| Arbeitnow | Public API | its page: jobs come "mostly from Applicant Tracking Systems (ATS) such as Greenhouse, SmartRecruiters, Join.com, Team Tailor, Recruitee, Comeet" | allowed | yes | yes | **NO**: re-serves systems whose robots.txt blocks us |
| The Muse | API | | | | | blocked (Cloudflare 403 for automated clients) |
| ReliefWeb (UN OCHA) | API v2 | needs an approved `appname` (request form) | | yes | yes | LATER: needs a request from KT's email |
| Remotive, Jobicy | | | | | | excluded earlier (terms; dates) |
| Paid vendors (TheirStack, Techmap, Coresignal, jobdataapi, JSearch) | | | | | | NO: cost, and resale of Google/LinkedIn/Indeed data |
| Board websites without a feed (NoDesk, Wellfound, Jobgether, Remote Rocketship, Arc, Dynamite, 4dayweek, WayUp, Internshala, newgrad-jobs, 80,000 Hours, Idealist, Tech Jobs for Good) | | competitors' compiled pages | | | | NO: HTML scraping of other boards (CLAUDE.md "Do not") |
| Public employment services (Sweden open, Germany 403, France/Norway/USAJobs need keys) | | | | | | NO for now: local-language, local, few remote roles |
| SimplifyJobs early-career lists | public JSON on GitHub | no licence file | | | | **USE ONLY AS A DISCOVERY SEED**: read which employer board each link points to, then fetch that employer's own feed; never republish the lists |
