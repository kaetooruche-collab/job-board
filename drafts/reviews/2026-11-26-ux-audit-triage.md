# UX audit (pasted by KT, 26 Nov 2026): checked against the live site

Method: every claim that could be checked was checked on the live site in a real browser (Playwright, 1280px and 360px), in the code on `main`, or in the live `jobs.json` (1,765 jobs, 26 Nov). Status: **SUPERSEDED** the same day by `2026-11-26-ux-audit-ledger.md` (all 102 points worked through; merged as PR #78 on KT's yes; KT kept the CV link on every card).

## 1. Where the audit is wrong or out of date
| Audit point | What is actually true |
|---|---|
| D "Paid checkout is in test mode" (rated critical) | False for visitors. `SITE.checkout.mode` is `off`; the TEST banner is in the page source but `hidden`, and no pay buttons show. Checked in a browser: banner not visible, text not on screen. The auditor likely read the raw HTML. |
| 3 "I want to search by company name" | Already works: search matches title first, then company, field and location (`search.js`). |
| 28, 29 Filters kept and shareable | Already: every filter is written to the address bar, so a filtered search can be bookmarked or shared. |
| 70, 72 CV message "interrupting" and "repeated" | It appears only after 40 listings have been shown, sits below the listings (never between them), and its × hides it for good on that device. The wording point (71, "Your CV is the next step" assumes too much) is fair. |
| 60 Say which hiring system the Apply button opens | KT decided on 25 Nov: no hiring-system names anywhere public. Not doing it. |

## 2. Where the audit is right (verified)
- 101 Consistent terms: /verify still said "Eligibility unclear" and "Remote: not confirmed"/"Why this label?", all retired on 25 Nov. **Fixed in PR #78** (waiting for KT's yes, because it is public copy).
- 48 Missing pay: /verify promised "Not stated", but cards showed nothing. **Fixed in PR #78**: cards say "Pay not stated".
- E Duplicates: 66 roles appear as 176 cards because the same role is listed once per country (Mozilla: one engineering role is 7 cards). One card per role, with "Also open in: …", would fix it.
- 18-19 Experience appears in four places (quick row, More filters, "Experience asked for", the guide). It could be one control.
- 5-7, 42 The country choice is the product's strongest point and is not the first thing a visitor sees; the country list is a plain long dropdown.
- 54 No way to save jobs.
- 56 Reporting a listing is only possible from the bottom of /verify, not from the card.

## 3. Requests our data cannot support honestly (not now)
Time-zone, language, employee-versus-contractor, visa, education and "existing work authorisation" filters (9, 10, 11, 12, 13, 14): the feed does not hold these reliably (for example, only 9 of 1,765 jobs state a time zone). A filter built on guessed data would break the trust promise. The classifier could learn some of them later, with the usual fixtures and spot checks.
Salary sort and comparison (17, 21, 22, 47): pay is stated on 61% of jobs, in several currencies and periods; a salary sort would push 39% to the bottom for a reason unrelated to the job.
Company logos (41): needs a third-party logo service (another dependency, trademark use). Low value against cost.
Descriptions on cards (37-40): we keep only the first 300 characters, and copying more of employers' text, or writing AI summaries of it, raises accuracy and copyright questions. Needs its own decision.
Application tracker, compare and job-detail pages (55, 58, 64): larger builds; job pages also bring a search-markup decision that is still open.

## 4. Context that decides priority
- KT's rule (31 Oct): traffic comes first; at about 50 home views a week, conversion is not the bottleneck.
- The 16 Nov review recommended freezing building during a 30-day demand test.
- So the proposal is one bounded batch, not the audit's 12-step roadmap.

## 5. Proposed batch (each small, each tested; build only on KT's yes)
1. Country first: "Where do you live?" with type-to-search becomes the first control, and the count line says how many jobs are open to you and how many don't say.
2. One card per role: same company and title merged, with "Also open in: …".
3. One experience control instead of four.
4. Save jobs on this device (no account), and "Report this listing" on each card.
5. For KT to decide (commercial, not technical): the "Get a CV for this role" button on every card (KT's own spec) and the wording of the CV message after 40 listings.
