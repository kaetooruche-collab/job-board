# Optional country at signup, and country editions of the weekly email (31 Oct 2026)

Status: built, signup live after merge; no country edition sent. KT said "yes" to "the country field and the personalised weekly email".

## Why (evidence label in brackets)
- Most listings are restricted to one country or region: of 1,038 listings, 15 are worldwide, 738 name countries, 261 are unclear (established, `jobs.json`, 31 Oct). A general digest therefore shows each reader many roles they cannot take (established); the board already lets a visitor pick a country (established).
- That a country-matched email is clicked more than the general one is a HYPOTHESIS. No data yet; the first country editions are the test.

## What was built
- Optional country dropdown on the full signup form; the inline card sends the country the visitor already chose in the filter and says so on screen. Stored in Brevo attribute `WORK_COUNTRY` (created 31 Oct after checking the account is KAYZ Global Ltd).
- Consent wording version `signup-v2` (record in `drafts/email-system/consent-wording-versions.md`); privacy page row updated. Purpose stated to the visitor: it only decides which roles come first.
- `api/subscribe.js` validates the value against a name pattern, never stores it for the check/order forms, never writes to a blocklisted contact.
- `scripts/make_digest.py --country X` builds an edition of only roles whose posting names X, X's region, or is worldwide. Stricter than the site filter (unclear, timezone and unknown-region roles do not count). The email says so in one sentence and repeats "check each employer's rules".
- `scripts/make_digest.py --coverage` counts this week's roles open to each country. 31 Oct: 363 recent remote roles; every one of the 189 countries had 10 or more; US 181, Canada 57, UK 46, Nigeria 13, Kenya 13, Philippines 10 (established, from the data).

## Limits and risks
- Eligibility still comes from the employer's wording as the classifier read it. Example: "EMEA, Germany" is expanded to all EMEA countries, so a Nigeria edition can include it. Hence the "check each employer" sentence; not a guarantee.
- Sending: Brevo segments cannot be created by the API (KT builds them). Whether a general campaign can exclude a segment is NOT verified; until it is, the routine keeps sending one general digest to list 11 and no edition is sent.
- Small lists: an edition needs at least 3 qualifying roles (`MIN_SHOWN`); suggested minimum 10 subscribers per country before it is worth a separate send.
