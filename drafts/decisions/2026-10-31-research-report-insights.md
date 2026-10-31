# Research report (31 Oct 2026): what we took, with the evidence behind each change

Source: `Yireh_Careers_Research_Report.docx` supplied by KT. The report states its limits: it could not open the live site or code, it has no analytics or conversion data, and its headlines and colour recommendations are design hypotheses. Competitor facts are cited public pages that were not re-verified here. Three of its claims were checked against our real data on 31 Oct and held.

## Data checks (our own `jobs.json`, 31 Oct)
- Level buttons did not add up: Early 99 + Mid 349 + Senior 454 = 902 against 1,041 listings; **139 listings have no level.**
- Eligibility mix: worldwide 15 (1.4%), **country-limited 738 (71%)**, unclear 261 (25%), regional 22, timezone 5.
- "ATS-optimised" appeared on the home page, the services page and the WhatsApp copy.
- No search events were being tracked.

## Changes made, and why
| # | Change | Evidence class | Why it holds |
|---|---|---|---|
| 1 | Optional "Where can you work from?" selector beside the search box (moved out of "More filters"; same control, same URL state) | Product data (71% country-limited) + usability guidance | The country filter keeps worldwide AND "unclear" listings (verified in code), so choosing a country never hides roles that might be open; those cards still read "Eligibility unclear". No geolocation. |
| 2 | "Level not stated" option; level buttons now sum to All levels | Our own data | Removes an unexplained 139-listing gap |
| 3 | Eligibility pill reads "Apply from: ..." for country and region limits | Usability guidance (applicant location, not company location) | Keeps "who can apply" distinct from where the employer is based |
| 4 | "ATS-optimised" replaced by "ATS-friendly structure / role-relevant keywords" | Truth-in-advertising risk | "Optimised" reads as a promise to pass screening; we do not test that |
| 5 | Events: `search-used` (length bucket only, never the words), `no-results`, `filters-cleared`, `verified-meaning-click` | Measurement gap | Needed to judge the search-first layout; no personal data sent |

## Not done, and why
- Headline test ("Find remote jobs. Know where you can apply." vs the current one): a design hypothesis; test only when traffic can support it.
- Timezone wording in the hero: only 5 of 1,041 listings carry a timezone requirement.
- Free CV check "who reviews it" and Executive "what connection building involves": need KT's facts.
- Founder photo: waiting on KT's answers (genuine photo, name or not, a few true sentences).
