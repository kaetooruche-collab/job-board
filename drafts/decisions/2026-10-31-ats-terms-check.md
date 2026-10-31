# Greenhouse, Lever and Ashby: what their own pages say about showing their listings (31 Oct 2026)

Status: CHECKED. This closes the Phase 0 gap noted in `drafts/reviews/2026-10-31-published-elements-review.md` (item 7). It is a reading of public pages, not legal advice. KT decides any response.

Why it matters, in proportion: all 1,038 listings come from these three feeds (Greenhouse 549, Ashby 352, Lever 137; 160 companies). Losing them would empty the board. But the board is not the bottleneck for the goal; visitors are, so this was a bounded check.

## What the vendors say (each point read on the vendor's own page on 31 Oct 2026)

| Point | Greenhouse | Lever | Ashby |
|---|---|---|---|
| Is the read feed public? | **Established.** [Job Board API docs](https://docs.greenhouse.io/job-board.html): "Job Board data is publicly available, so authentication is not required for any GET endpoints." | **Established.** [Postings API README](https://github.com/lever/postings-api): published jobs are publicly viewable; no key for GET. | **Established.** [Public job posting API](https://developers.ashbyhq.com/docs/public-job-posting-api): no credentials in any example. |
| Does the vendor say anything about third parties showing the data? | Nothing either way. Docs describe the API as for building careers pages. | **Yes, explicitly tolerant:** "all job postings in the `published` state are publicly viewable. These jobs may be scraped by third parties." Also "designed to help you create a job site". | Nothing either way. Described as for populating your own careers page. |
| Rate limits | None published for GET. (Our pipeline: every 6 hours, 0.6 to 1 second between calls.) | Only a limit on application POSTs (2 a second), which we never use. "May also be changed without warning." | None published. |
| Terms that bind outsiders | The [Master Subscription Agreement](https://www.greenhouse.com/master-subscription-agreement) binds paying customers and says "There are no third-party beneficiaries". It does not mention public job data. The [My Greenhouse User Agreement](https://my.greenhouse.io/users/agreement) bars bots and "monetize the Services or related data", but it binds account holders of the candidate service and says nothing about public job boards. | [Terms of Service](https://www.lever.co/terms-of-service/) are written for customers; no mention of postings or scraping. | [Customer Terms](https://www.ashbyhq.com/resources/terms) bind customers; no mention of scraping or public postings. |

## What this means
- **Established:** no vendor page prohibits reading these public feeds or showing the postings, and Lever says outright that third parties may scrape published postings. What we do (read the public endpoint, link to the employer's own posting, credit the source, no account, no login) is the intended public use.
- **Not established / unclear:** (a) Greenhouse and Ashby are silent rather than permissive, so "no objection found" is not "permission". (b) Greenhouse's My Greenhouse "no bots" clause is written for candidate accounts; whether its authors would read it onto public boards is unknown, but our pipeline uses no account. (c) We found no separate API terms for any of the three. (d) Our link check opens employers' public posting pages automatically; none of the pages read says that is forbidden, and it is low volume.
- **The real remaining risk is per company, not per vendor:** an employer can ask to be removed. The board already has the process (`/verify` trust rules; "Report a listing" by email or WhatsApp; `data/boards.json` lets one company be dropped).

## Recommended actions (none changes the site; KT approves)
1. Leave everything as is. No change needed.
2. Optional, low effort: put a contact address in the fetch User-Agent (currently "JobBoard/1.0 (remote job board; contact via site)") so a vendor can reach us before blocking. Not done: it could change how employers' sites treat our link check, so it needs an old-versus-new check on the link-check results first.
3. Keep this as an assumption on the register: "vendors do not object to public-feed use", revisit if any vendor or employer writes to us, or if a vendor adds API terms.
4. Do not read this as cover for scraping employers' HTML pages or other boards; the CLAUDE.md "Do not" list still applies.

## Not done
- Greenhouse's general website terms: the obvious addresses returned 404 and search did not find a separate visitor-terms page; only the three documents above were read.
- Workday, Personio, Teamtailor and other systems (see `research/job-sources-100.md`): not in use on the live board.
