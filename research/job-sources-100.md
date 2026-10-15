# 100 job sources and strategies for PROJECT_NAME (TrueRemote)

Compiled 2026-10-15 from three research passes. Nothing here is copied from the sample "deep research" report KT attached; that report was treated as a sample only.

**How to read the tags**
- **USE** = verified working and fits the listing standard, build or keep it.
- **TEST** = looks promising, needs a live test or written permission first.
- **LINK-OUT** = we only link people to this site (no reuse of its listings). Allowed only if it is free with no signup wall before the apply link.
- **PLATFORM** = a sign-up platform, goes in `platforms.json`, no posted date, no pay claim unless its own page states it.
- **STRATEGY** = a method, not a feed.
- **V** = we opened or called it ourselves on 2026-10-15. **U** = unverified (documentation or third-party text only).

## Read this first: what the research means for Gate 1

1. **Dates are solid, "worldwide" is the weak spot.** Greenhouse `first_published`, Lever `createdAt` and Ashby `publishedAt` all work (V). But almost all "remote" roles are "Remote - <one country>", which does not meet listing standard #3 (posting says open worldwide). Structured "Global / Anywhere" labels were found on only a handful of postings (V), and most were engineering or senior roles, or Talent Community sign-ups rather than real roles.
2. **Expect a thin board from feeds alone.** Entry-level plus worldwide plus under 30 days is a small set. Hand-verified listings (strategy 77), link-outs and the platforms section carry real weight.
3. **Apply-before dates almost never exist.** Greenhouse `application_deadline` was null on 2,977 of 2,977 jobs (V). We rely on the 30-day age cut plus the link check.
4. **Our pipeline was broken in two ways.** Fixed: the Ashby code read the wrong date field name, so every Ashby job was silently dropped. Not yet fixed: most company slugs in the lists are dead (see strategy 93).
5. **No vendor gives an explicit licence to aggregate.** Lever's README says public postings "may be scraped by third parties" (strongest). Greenhouse docs say GET needs no authentication. Ashby and others are silent. Keep the removal process for any company that asks (strategy 99).

## A. Applicant-tracking-system (ATS) endpoints (1-11)

| # | Source | Endpoint / access | Dates and apply link (V unless noted) | Tag |
|---|---|---|---|---|
| 1 | Greenhouse | `boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true` | `absolute_url`, `first_published` is the original date, `updated_at` is not (use only `first_published`). Docs: no auth for GET. | USE |
| 2 | Lever | `api.lever.co/v0/postings/{slug}?mode=json` | `hostedUrl`, `applyUrl`, `createdAt` (epoch ms), `workplaceType`. README: postings "may be scraped by third parties". | USE |
| 3 | Ashby | `api.ashbyhq.com/posting-api/job-board/{slug}` | `jobUrl`, `publishedAt` (documented as "last published"; one cross-check matched the page's `datePosted`). Skip `isListed: false`. | USE (bug fixed) |
| 4 | Workable | `apply.workable.com/api/v1/widget/accounts/{slug}` | `url`, `published_on`, `created_at` (can differ). Blocked from this sandbox by Cloudflare; worked via Firecrawl. Unofficial endpoint. | TEST |
| 5 | Recruitee | `{slug}.recruitee.com/api/offers/` | `careers_url`, `published_at`, `close_at` (apply-before field, null on 21 of 21 tested). EU-heavy. | TEST |
| 6 | SmartRecruiters | `api.smartrecruiters.com/v1/companies/{id}/postings` | Works keyless but docs say key or OAuth, so outside the documented contract. Apply URL needs a second call. Higher legal risk. | TEST |
| 7 | Personio | `{slug}.jobs.personio.de/xml` | `createdAt` present; no apply URL or remote flag in the feed. German-market. Terms not read. | TEST |
| 8 | Teamtailor | `{slug}.teamtailor.com/jobs.rss` | `link`, `pubDate`, `remoteStatus`. Terms not read. | TEST |
| 9 | BambooHR | `{slug}.bamboohr.com/careers/list` then `/careers/{id}/detail` | `datePosted` (date only) in detail call; list has no date. | TEST |
| 10 | Breezy HR | `{slug}.breezy.hr/json` | `published_date`, `is_remote`. Only a demo account verified. | TEST |
| 11 | Rippling ATS | `ats.rippling.com/api/v2/board/{slug}/jobs` | Date only in the per-job detail (`createdOn`). | TEST |

## B. Named employers with live endpoints (12-35)

Counts are open postings on 2026-10-15. "Country-specific" means the role says "Remote - <country>", so the card must show the country and the listing cannot claim worldwide.

| # | Employer | ATS / slug | Open | Evidence | Tag |
|---|---|---|---|---|---|
| 12 | Supabase | Ashby / supabase | 53 | "Remote, Global" on about 29 (mostly engineering) | USE |
| 13 | Turing | Greenhouse / turing | 28 | Investigations Analyst, "Global - Remote", 2026-09-18 | USE |
| 14 | Toptal | Lever / toptal | 28 | All remote; one "Anywhere" role (senior). One role dates from 2023, so the age cut matters. | USE |
| 15 | Oyster HR | Ashby / oyster | 24 | Only "Any Location" entry is a Talent Community sign-up, not a job (drop those) | USE |
| 16 | GitLab | Greenhouse / gitlab | 217 | 192 "Remote, <country>"; about 6 to 35 entry-ish titles | USE |
| 17 | Invisible Technologies | Greenhouse (EU host) / invisibletech | 22 | 4 remote, all country-specific | USE |
| 18 | Appen | Lever / appen | 61 | Voice Recording Specialist roles, remote, per language/country | USE |
| 19 | Twilio | Greenhouse / twilio | 141 | Billing Operations Analyst, "Remote - Mexico" | USE |
| 20 | ClickUp | Ashby / clickup | 50 | CX Operations Analyst, Philippines, remote | USE |
| 21 | GoHighLevel | Lever / gohighlevel | 93 | BDR Support Apprentice, India. Check for commission-only. | USE |
| 22 | Preply | Ashby / preply | 135 | Customer Support Agent, Ukraine-based, April 2026 (old) | USE |
| 23 | Mozilla | Greenhouse / mozilla | 89 | All "Remote US/Canada" | USE (filters) |
| 24 | Wikimedia Foundation | Greenhouse / wikimedia | 12 | All "Remote", senior-leaning | USE (filters) |
| 25 | PostHog | Ashby / posthog | 11 | "Remote" and "Remote (EMEA)", mostly senior | USE |
| 26 | Handshake | Ashby / handshake | 87 | Support Specialist, contract, "Remote (USA)" | USE |
| 27 | Zapier | Ashby / zapier | 11 | Remote, regional, mostly mid/senior | USE |
| 28 | Grafana Labs | Greenhouse / grafanalabs | 112 | "<country> (Remote)" pattern | USE |
| 29 | Automattic | Greenhouse / automatticcareers | 12 | Remote company; check each role's wording | USE |
| 30 | Dropbox | Greenhouse / dropbox | 29 | "Remote - Japan" style country roles | TEST |
| 31 | Hugging Face | Workable / huggingface | 6 | "EMEA/US Remote", senior | TEST |
| 32 | Canva | SmartRecruiters / Canva | 122 | Trust & Safety role was hybrid, not remote | TEST |
| 33 | Ubisoft | SmartRecruiters / Ubisoft2 | 327 | 8 entry-level, 21 internships, few remote | TEST |
| 34 | Toloka | Greenhouse / toloka | 16 | AI data company; roles not read in detail | TEST |
| 35 | Prolific | Greenhouse / prolific | 29 | Research platform staff roles; not read in detail | TEST |

## C. Link-out boards (36-46): we send people there, we do not reuse their listings

Rule from KT: linking out is fine as long as there is no paywall or signup wall before the apply link. Three are confirmed free; the rest must be tested by opening a real listing before they appear on the site.

| # | Site | Free with no signup wall? | Tag |
|---|---|---|---|
| 36 | NoDesk (nodesk.co/remote-jobs) | V: page says "No account or sign-up required"; dates shown | LINK-OUT |
| 37 | Skip The Drive | V: "no registration and no charge to search" | LINK-OUT |
| 38 | Remote Rocketship | Front page showed no wall; apply step not checked | TEST |
| 39 | Adzuna | Front page showed no wall; apply goes through Adzuna; apply step not checked | TEST |
| 40 | Idealist | Free signup offered; whether apply links need an account was not shown | TEST |
| 41 | Working Nomads | Terms-site says no account to browse (U); redirect goes to employer | TEST |
| 42 | Jobspresso | Not checked; terms page not found | TEST |
| 43 | JustRemote | Not checked | TEST |
| 44 | Dynamite Jobs | Not checked | TEST |
| 45 | Impactpool | Listings visible without login (V), but link to Impactpool pages, not employer | TEST |
| 46 | ReliefWeb (site, not API) | Site is free (U); few remote entry-level roles | TEST |

## D. Platforms to sign up to (47-59): `platforms.json` only

Never in "Open listings". No posted dates. No pay claim unless the platform's own signup page states it (DataAnnotation's page does state figures; we still should not repeat them as our claim).

| # | Platform | Notes | Tag |
|---|---|---|---|
| 47 | DataAnnotation | Signup and qualification test; no fee mentioned (V) | PLATFORM |
| 48 | Outlier | Account, ID check, onboarding (V) | PLATFORM |
| 49 | Prolific (participants) | Waitlist and ID check (V); studies, not a job | PLATFORM |
| 50 | Clickworker | Registration required; "136 countries" (V) | PLATFORM |
| 51 | Toloka (workers) | "100+ countries" (V) | PLATFORM |
| 52 | Remotasks | Confirm it is still operating before listing | PLATFORM |
| 53 | Appen (crowd) | Crowd signup page returned 404; find the current one first | PLATFORM |
| 54 | TELUS Digital AI Community | Roles page at jobs.telusdigital.com; ATS unknown | PLATFORM |
| 55 | Rev | Transcription; signup page not yet opened | PLATFORM (not yet researched) |
| 56 | TranscribeMe | Not yet opened | PLATFORM (not yet researched) |
| 57 | Gengo | Not yet opened | PLATFORM (not yet researched) |
| 58 | Unbabel | Not yet opened | PLATFORM (not yet researched) |
| 59 | ProZ | Not yet opened | PLATFORM (not yet researched) |

## E. Already in use (60)

| # | Source | Notes | Tag |
|---|---|---|---|
| 60 | Jobicy API | In the pipeline now; direct employer links; worldwide filter. Terms not re-read this session. | USE |

## F. Strategies (61-100)

| # | Strategy | What to do | Tag |
|---|---|---|---|
| 61 | Search-operator discovery | Claude runs a few searches such as `site:jobs.lever.co "worldwide"` and logs candidate employers for KT to approve. Manual and low volume. | STRATEGY |
| 62 | JobPosting JSON-LD cross-check | Read `datePosted` and `validThrough` from an employer's own posting page to confirm ATS dates. Fetch known posting URLs only. | STRATEGY |
| 63 | Career-page sitemap watching | Watch `sitemap.xml` of employers with no ATS API for new job URLs. Obey robots.txt. | STRATEGY (later) |
| 64 | Common Crawl slug harvest | Use the crawl only to collect ATS company slugs, never job content. Its licence is limited, so KT should decide knowingly. | STRATEGY (maybe) |
| 65 | Monthly Google Jobs sanity check | Compare a manual search with what the board has missed. Never automate it. | STRATEGY |
| 66 | HN "Who is hiring" pilot | Free Algolia API, thread exists (V). Mostly engineering, no formal posting date; one report says pilot, another says avoid. Low priority. | STRATEGY (test) |
| 67 | remoteintech company list | The `remoteintech/remote-jobs` repo (ISC licence) lists 884+ companies, 404 tagged Worldwide (V). Use as a seed list only. | STRATEGY |
| 68 | Pre-screen the Worldwide companies | For each seed company, find its careers page and ATS, record the evidence (quote plus URL) of worldwide hiring. | STRATEGY |
| 69 | Newsletter link swaps | Email 5 to 10 remote-work newsletters with the "How we verify" page. Distribution, not listings. | STRATEGY |
| 70 | Telegram channels (with permission) | Ask channel owners; never scrape. | STRATEGY |
| 71 | Discord and Slack communities | Join as KT for leads and distribution only; never bulk copy. | STRATEGY |
| 72 | Fediverse hashtag feeds | `#hiring` tag feeds; employers post apply links directly. Low yield. | STRATEGY (low) |
| 73 | "Where we hire" pages | Store each employer's country-eligibility page as eligibility evidence next to its listings. | STRATEGY |
| 74 | EOR country-coverage pages | Deel, Remote and Oyster publish country lists. Evidence only; each employer decides. | STRATEGY |
| 75 | BPO and trust-and-safety vendors | Pilot 5 vendors; most roles are location-bound. Check for training fees or bonds. No Greenhouse board found for TaskUs, Concentrix or Teleperformance (V). | STRATEGY (pilot) |
| 76 | VC portfolio boards | Boards on Getro: ask the platform or VC for a partner feed; do not scrape. | STRATEGY (ask) |
| 77 | KT hand-verification checklist | A sheet with the seven listing-standard tests. Claude pre-fills from a pasted URL (quotes the worldwide line and date); KT confirms. Target 5 to 10 a week. | STRATEGY |
| 78 | "Suggest a listing" form | Feeds a private queue; nothing publishes without the seven-point check. | STRATEGY |
| 79 | Employer self-submit form | Phase 3. Do not start without KT's go-ahead. | STRATEGY (wait) |
| 80 | Seeker tip line | The "Report a listing" page and WhatsApp also take "I saw this job" tips. | STRATEGY |
| 81 | Claim-and-confirm outreach | Email employers whose roles appear: reply to correct or remove. Also serves as the required removal process. | STRATEGY |
| 82 | University, bootcamp and NGO partners | Ask career offices to share the board. No student data collected. | STRATEGY (later) |
| 83 | GitHub Actions heartbeat | Schedule at an off-peak minute. GitHub disables scheduled workflows after 60 days of no repo activity, so add a monthly heartbeat commit. | STRATEGY |
| 84 | n8n workflow | Optional visual flow from feeds to a WhatsApp draft. Adds a second system. | STRATEGY (optional) |
| 85 | Google Alerts | Surface new employers saying "hiring worldwide". Noisy. | STRATEGY (optional) |
| 86 | Page-change monitoring | Watch the 40 careers and "where we hire" pages for policy changes. | STRATEGY |
| 87 | Closed-role detection | Greenhouse, Lever and Ashby list only active jobs, so absence on the next poll means closed. Also check closed-role wording. | STRATEGY |
| 88 | Cross-source dedupe | Key on canonical URL, then a hash of company, title and location. Keep the earliest `postedAt`. | STRATEGY |
| 89 | Verification badges | "Direct from employer's ATS" or "Hand-checked by KT on [date]", plus last-checked time. | STRATEGY |
| 90 | Eligibility evidence field | Show the exact worldwide quote and the employer's eligibility page beside the Apply button. | STRATEGY |
| 91 | Public corrections log | A page listing every fix, honouring the one-day rule. | STRATEGY |
| 92 | JobPosting markup decision | Google says `datePosted` must be the employer's original date and bans posting jobs on behalf of a company without authorization. Default to no markup unless an employer agrees. KT decides. | STRATEGY (decision) |
| 93 | Rebuild the company slug lists | Live check found 78 of 121 Greenhouse, 66 of 72 Lever and 6 of 22 Ashby slugs return 404 (dead examples: remotecom, buffer, zapier on Greenhouse; anthropic, openai on Lever). Live: 43, 5 and 16. Replace with verified slugs and re-check weekly. | STRATEGY (to do) |
| 94 | Use `first_published` only | Greenhouse `updated_at` is often over 30 days after `first_published` (1,660 of 2,977 jobs). Never use it as the posting date. | STRATEGY |
| 95 | Filter pseudo-postings | Drop "Talent Community" and "Any Location" sign-up entries that are not real roles (Oyster, Udemy examples). | STRATEGY |
| 96 | Canonical Greenhouse URLs | Some `absolute_url` values are custom-domain search-style links (Stripe, Pinterest). Prefer `job-boards.greenhouse.io/{board}/jobs/{id}` so the link check does not wrongly reject them. | STRATEGY |
| 97 | Ashby partner feed | Ashby offers hourly partner feeds by agreement (integrations@ashbyhq.com). Ask once the board has traffic. | STRATEGY (ask) |
| 98 | Written permission outreach | Email Working Nomads and Jobspresso for written permission and a terms page before reusing any data. | STRATEGY (ask) |
| 99 | Aggregation clarification | Ask Greenhouse, Lever and Ashby support whether public-board aggregation is fine. Keep the company removal process regardless. | STRATEGY (ask) |
| 100 | Eligibility text classifier | Search posting text for "worldwide", "anywhere", "any country" and exclude "US only", "must reside in". Structured location fields rarely say worldwide, so this decides standard #3. | STRATEGY |

## Not on the list of 100, and why

- **Remotive API:** excluded by the brief (terms forbid use beside email capture).
- **We Work Remotely, Remote OK:** removed (paywall; Remote OK terms never vetted).
- **Himalayas:** its Apply button goes to a Himalayas signup page, and its docs ask that jobs not be submitted to third-party sites.
- **Reddit:** commercial-use terms are a problem (reported by secondary sources; Reddit's own terms were not fetched).
- **YC Work at a Startup:** terms prohibit scraping.
- **Mercor:** 111 of 112 ATS postings are on-site; its contractor work is not in the ATS.
- **Arbeitnow, Jooble, Careerjet, Findwork, The Muse, USAJOBS, Authentic Jobs, Remote100K:** not worldwide, dev-only, tracking redirects, unread terms or senior-only.
- **Pinpoint:** no posting date. **Workday:** list shows only "Posted 30+ days ago". **Comeet, JazzHR:** need a key. **Homerun, iCIMS, Jobvite:** no keyless endpoint found.
- **FlexJobs, Virtual Vocations, Jobgether, Devex, Upwork:** paywall or signup wall.
- **Jobgether on Lever (3,714 postings):** re-posts for other employers, so links are not the employer's own posting.

## What could not be verified

Terms for Personio, Teamtailor, BambooHR, Breezy, Rippling and Workday; Greenhouse's public-site terms; whether Greenhouse, Lever or Ashby rate-limit a GitHub Actions address; whether Ashby `publishedAt` ever differs from the original date for reposted roles (one cross-check only); worldwide wording in the full descriptions of the Appen, ClickUp, GoHighLevel and Preply roles; apply steps on Remote Rocketship, Adzuna and Idealist; every platform in section D beyond what their signup pages showed.
