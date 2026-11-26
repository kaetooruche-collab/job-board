# UX audit, item by item (26 Nov 2026)

All 102 points and findings A to F from KT's pasted audit, each checked against the site and given an outcome. Fixes are on branch `claude/verify-location-wording` (PR #78), not live until merged.
Evidence: a browser walk-through of the changed page served from disk with the live `jobs.json` of 26 Nov (1,765 postings), at 1280 px and 360 px, with no page errors. The test suite (251 tests) passes, and a new test (`tests/test_page_ids.py`) fails on the live code and passes on the branch.

Outcomes:
- **FIXED**: changed on the branch.
- **ALREADY**: already worked; checked in the browser.
- **PARTLY**: part done, and the rest is stated.
- **NOT DOING**: not done, with the reason.
- **KT**: a commercial or copy decision that is KT's to make.
- **WRONG**: the audit's claim is not true.

| # | Point (short) | Outcome | What was done or found |
|---|---|---|---|
| 1 | Don't know where to start | PARTLY | "Where do you live?" is now the first box, then the keyword box. The hero is unchanged; changing it is a copy decision for KT. |
| 2 | Search not prominent | FIXED | It sits second at the top, with the placeholder "Job title, company or keyword". |
| 3 | Search by company | ALREADY | Typing "Mozilla" returns 6 roles (15 postings). |
| 4 | Related titles | ALREADY | "customer support" returns 122 roles, including Customer Success titles (matched through the field). |
| 5 | Eligibility more prominent | FIXED | The country box comes first. The list shows how many jobs are open to each country. |
| 6 | Country dropdown tedious | FIXED | Type-to-search box. An exact name applies at once; an unknown name gets a hint. |
| 7 | Unclear eligibility excluded? | FIXED | With a country chosen, a legend explains the three labels, and "Show N more that don't say" was already there (252 for Cyprus). |
| 8 | Worldwide vs regional | FIXED | A "Worldwide roles only" choice (19 jobs) and separate pills. A region pill now says "(includes Cyprus)". |
| 9 | Time-zone filter | NOT DOING | Only 9 of 1,765 jobs state a time zone (shown on their pill). A filter on guessed data would break the trust rule. |
| 10 | Language filter | NOT DOING | Not in the data yet. The classifier would have to learn it, with fixtures and spot checks. |
| 11 | Employee vs contractor | PARTLY | Job type shows Contract or Freelance (153 jobs). Employer-of-record status is not in the feeds. |
| 12 | Filter out jobs needing existing work authorisation | FIXED | Choosing your country removes jobs restricted elsewhere. Cards say "You'll need the right to work there already" when the posting says so. |
| 13 | Visa or relocation filter | NOT DOING | These are remote roles, and the feeds do not state it. |
| 14 | Education filter | FIXED | "Hide jobs that mention a degree (unless they accept equivalent experience)". The card shows "The posting asks for: … a degree or equivalent experience". |
| 15 | Years without overlapping categories | FIXED | One experience row, plus "Years of experience the posting asks for". |
| 16 | Exclude internships, temporary, unpaid | FIXED | "Hide internships and temporary roles". Commission-only roles were already excluded. "Unpaid" is not detectable. |
| 17 | More sort options | FIXED | Newest first (default), least experience asked first, pay stated first. A salary sort is not offered because 39% of jobs state no pay. |
| 18 | Experience duplicated | FIXED | The duplicate Experience select is removed. |
| 19 | Inconsistent categories | FIXED | One row of 5 groups. The fine levels remain only for old links. |
| 20 | Level vs years | FIXED | Labelled separately ("Experience" and "Years of experience the posting asks for"). |
| 21 | Salary filter complicated | PARTLY | A note explains it. The currency choice stays because pay is in several currencies. |
| 22 | Hourly vs annual | PARTLY | The filter counts hourly pay as 2,080 hours, and the note says so. Cards keep the employer's own words (listing rule 4). |
| 23 | Does a minimum hide jobs without pay? | FIXED | The note says it does. |
| 24 | More filters hierarchy | PARTLY | Duplicate removed, sort row added. No full regrouping. |
| 25 | Active filters visible | ALREADY | Removable chips above the list. |
| 26 | Count before committing | PARTLY | Counts on levels, fields and every country. Not on every combination. |
| 27 | Clear one vs clear all | FIXED | The chip × clears one; "Clear all filters" clears all. **Bug found and fixed:** "Clear filters" crashed on the live site (it pointed at a removed checkbox), and a test now catches this class of bug. |
| 28 | Filters kept | ALREADY | Kept in the address bar and remembered on the device. |
| 29 | Share or bookmark a search | ALREADY | The address bar holds the filters. |
| 30 | No-results help | ALREADY | Suggests fewer filters or "Any location". |
| 31 | Guide repeats filters | PARTLY | Kept, as the audit itself recommends. A note says it sets the same filters. |
| 32 | Guide's advantage unclear | FIXED | Note: "Optional…". |
| 33 | Guide country list long | NOT DOING | It is a native picker on phones (type-ahead works). Low value. |
| 34 | Replaces or adds? | FIXED | Note: "sets the field, experience and country filters; your other filters stay". |
| 35 | Edit answers | FIXED | Answers persist; the note says "open it again to change an answer". |
| 36 | Guide competing | FIXED | Now a small text link, shown on phones only. |
| 37 | Cards say too little | PARTLY | Added the "asks for" line (years, degree, licence) and "still in the employer's feed". |
| 38 | Short description on card | NOT DOING | The stored text is the company's "About us" in 5 of 5 sampled jobs, not the role. Real summaries need the full posting, which raises accuracy and copyright questions; separate decision. |
| 39 | Key requirements | FIXED | "The posting asks for: 3+ years of experience · a degree or equivalent experience · a licence or certification", when stated. |
| 40 | Responsibilities | NOT DOING | Same reason as 38. |
| 41 | Company logos | NOT DOING | Needs a third-party logo service, another dependency, and trademark use. |
| 42 | Eligibility prominence | FIXED | Pill plus "(includes <your country>)" and the legend. |
| 43 | Remote / not specified / Apply from | FIXED | The legend explains all three. |
| 44 | Why this label | ALREADY | "Where this comes from" gives the employer's location text and quotes. |
| 45 | Worldwide vs unspecified | FIXED | Separate pills plus the legend. |
| 46 | Employment arrangement | PARTLY | See 11. |
| 47 | Standardised salary | NOT DOING | We show the employer's words (listing rule 4). The minimum filter converts. |
| 48 | "Not disclosed" label | FIXED | "Pay not stated" on 39% of cards. |
| 49 | Time zone visible | ALREADY | Shown on the pill for the 9 jobs that state one. |
| 50 | Occasional office visits | ALREADY | "May need occasional office visits" on the card. |
| 51 | Posted vs last seen | FIXED | "Posted …" and "Still in the employer's job feed …" are separate lines on the card. |
| 52 | Define "New" | FIXED | It now means posted by the employer in the last 2 days (it used to mean first seen by us), with a tooltip. |
| 53 | Reposted? | NOT DOING | A repost with a new ID looks like a new job in the feed. Not detectable reliably. |
| 54 | Save jobs | FIXED | Save / Saved on each card, and "Saved jobs (n)". Stored on the device only. |
| 55 | Compare shortlisted | PARTLY | The saved list shows them together. No side-by-side table. |
| 56 | Report from card | FIXED | "Report" opens an email with the job filled in. |
| 57 | Share a job | FIXED | "Share" copies `/?job=<id>` (or opens the phone's share sheet). The link opens that role on the board. |
| 58 | Detail view without leaving | PARTLY | The shared link shows the single role on the board. Separate job pages wait on the search-markup decision. |
| 59 | Clearer application journey | PARTLY | The Apply button says where it goes ("the original posting on the company's hiring page… you apply there, not through us"). |
| 60 | Name the hiring platform | NOT DOING | KT's 25 Nov rule: no hiring-system names. |
| 61 | Still accepting? | FIXED | "Still in the employer's job feed <time>" on the card. |
| 62 | Account required? | NOT DOING | The feeds don't say. |
| 63 | Extra location restrictions | ALREADY | "Not open to applicants in: …" and right-to-work lines. |
| 64 | Track applications | PARTLY | "You opened this application on <date>" after a click. No status tracking. |
| 65 | Applied vs not explored | FIXED | Same marker. |
| 66 | Accepts my country, not just remote | PARTLY | The country filter plus "(includes …)". The employer still decides, and the legend says so. |
| 67 | CV button competes with Apply | FIXED (KT may reverse) | Now a quiet text link under the card. Apply is the only button. |
| 68 | CV on every card | KT | Still on every card (KT's own spec), but quiet. KT decides whether it stays. |
| 69 | Free vs paid unclear | FIXED | Label "(paid service)". The message names the free check and the paid service separately. |
| 70 | Promo interrupts | WRONG / FIXED | It appears after 40 listings, below them, never between them. Wording changed. |
| 71 | "Your CV is the next step" assumes | FIXED | Now "Found a role worth applying for? … Both are optional". Copy change, so KT reviews it in the PR. |
| 72 | Dismiss for good | ALREADY | × hides it for good on the device. |
| 73 | CV optional | FIXED | "Both are optional: you apply to the employer directly either way." |
| 74 | Uncertainty about who processes the application | FIXED | The tooltip says it is not part of the employer's application. |
| 75 | Signup far down | WRONG | An email card already appears after the 6th listing. |
| 76 | What the email contains | FIXED | "a hand-picked selection of roles posted that week, the most widely open first". This matches how the digest picks roles. |
| 77 | Jobs matching country and level | ALREADY | Country is passed on, and the full form asks for level. |
| 78 | Alerts vs marketing | ALREADY | "We'll send you the weekly job email only"; tips are a separate unticked box. |
| 79 | Manage preferences | NOT DOING | Needs a preference page in Brevo; any Brevo change is gated on KT. |
| 80 | Confirmation | ALREADY | On-page message and the /subscribed page. |
| 81 | New only or older too | FIXED | "roles posted that week". |
| 82 | Easy unsubscribe | ALREADY | One tap. |
| 83 | "Verified" on the listing | PARTLY | The hero link and the legend. No per-card explanation (it would be repeated 40 times). |
| 84 | When last checked | FIXED | On the card (see 61). |
| 85 | Company vs listing verified | FIXED | "We check each listing, not the employer behind it" in "How these listings work". |
| 86 | What happens when a job closes | ALREADY | /verify: it leaves at the next update (at least daily). |
| 87 | Really worldwide? | FIXED | See 8. |
| 88 | Evidence without digging | ALREADY | One click: "Where this comes from". |
| 89 | Obvious report option | FIXED | See 56. |
| 90 | Credibility earlier | PARTLY | Hero link, the legend and the new disclaimer line. No hero rewrite (KT's copy). |
| 91 | Too much competing | PARTLY | Legend and saved row show only when relevant; the guide is now a link. |
| 92 | Filters progressive | ALREADY | Fields and More filters are collapsed by default. |
| 93 | Card hierarchy | PARTLY | One primary button; the CV link is demoted. |
| 94 | Secondary info competing | PARTLY | Same. |
| 95 | Breathing room | ALREADY | Card gap unchanged; judged fine. |
| 96 | Active filters indicator | ALREADY | Chips. |
| 97 | Count visible while scrolling | NOT DOING | A sticky bar takes phone screen space. The count is at the top and "Show N more" sits at the bottom. |
| 98 | Better mobile | PARTLY | The first job now starts at the same height as before (958 vs 962 px at 360 px). Cards are about 80 px taller because they carry the new requirement and feed lines. |
| 99 | Key filters on mobile | ALREADY / FIXED | Country and search come first. |
| 100 | Apply reachable on mobile | ALREADY | On every card. |
| 101 | Consistent terms | FIXED | /verify no longer says "Eligibility unclear", "Remote: not confirmed" or "Why this label?". A test blocks their return. |
| 102 | Navigation focused on jobs | PARTLY | "Jobs" link added to the desktop nav. The "Get Job-Ready" button stays (KT's commercial choice). |
| A | Experience filters overlap | FIXED | See 18. |
| B | Unclear eligibility fatigue | FIXED | Hidden by default under a country, one click to show, and a legend. |
| C | Repeated paid promotions | PARTLY + KT | Demoted and reworded. Whether it stays on every card is KT's call. |
| D | Checkout in test mode | WRONG | Checkout is off; the banner is hidden. Checked in a browser. |
| E | Duplicate opportunities | FIXED | One card per role: 1,765 postings show as 1,648 roles; Mozilla's 7 become 1 with "Also listed for". |
| F | No descriptions | NOT DOING (partly offset) | See 38. The "asks for" line was added instead. |

Count (by the first outcome in each row, all 108 rows): 46 fixed, 22 partly done (the rest stated in the row), 22 already worked, 3 where the audit was wrong (D, 70, 75), 14 not done with the reason, 1 left to KT (68). Every row has been addressed; "partly" and "not doing" rows say exactly what is missing and why.
