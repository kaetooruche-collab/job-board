# Decision: a small server function for the website forms (api/subscribe.js)

Status: **APPROVED by KT, 24 Oct 2026** ("do the recommendation"). Supersedes the blueprint choice "Option A: Brevo-hosted forms, no server code" in `drafts/email-system/07-data-consent-event-model.md`.

## Context
- The site is static; a browser cannot call Brevo without exposing the API key, so the blueprint used Brevo-hosted forms.
- Brevo's API cannot create forms, so KT would have built three by hand (about an hour), with weaker consent evidence (a form cannot reliably store the wording version or date), and test T5 showed the live form re-subscribes blocklisted addresses.
- KT asked "why am I building forms in Brevo?" and approved the alternative.

## Decision
Add `api/subscribe.js` (a Vercel serverless function, no dependencies). The site's forms (home signup, `/free-check`, private `/order`) post JSON to it; it talks to Brevo with a key held only in Vercel (`BREVO_API_KEY`, sensitive, production only).

What it guarantees (each covered by `tests/node/subscribe.test.js`, 16 tests, and by live runs against the real Brevo account with KT's plus-addresses):
1. **Never writes to a blocklisted contact** (fixes T5). A signup from a blocked address is told plainly and nothing changes; a free-check or order from one still reaches KT.
2. **Consent evidence is exact and permanent**: `CONSENT_JOBS_AT/SRC` and `CONSENT_TIPS_AT/SRC` (date and wording version `signup-v1`, `check-v1`, `order-v1`) are set once and never overwritten.
3. Tips consent is a separate, unticked box that adds the contact to **Career tips** only when ticked.
4. Free-check and order forms **email KT a notice** (through Brevo's transactional email, delivered to yirehcareers@gmail.com, verified in Brevo's event log) so no request is missed; the free check adds no marketing list.
5. Abuse controls: same-origin only, 4 KB body limit, honeypot (quiet fake success), 8 submissions per IP per hour (best effort per server instance), strict validation, no personal data in logs.
6. Parallel submissions of one address produce one contact (create-conflict retry).

## Consequences and risks (accepted)
| Risk | Mitigation |
|---|---|
| The Brevo key (full account access) now lives in Vercel | Stored as a *sensitive* variable (not readable after saving), production only, never in the repo or client code. Revoke the key in Brevo and delete the variable to switch the forms off |
| Brevo "Block unknown IP addresses" must stay OFF (Vercel addresses change) | Documented in `12-dashboard-build-guide.md`; the site monitor fails if the endpoint breaks |
| Public endpoint can be hammered | Limits above; Brevo's own limits; monitor checks it refuses strangers every 3 hours |
| More code to maintain | About 200 lines, tested; no database, no dependencies |
| Single opt-in means typos and bots can add addresses | Honeypot and validation; the welcome email (AU-1) acts as a de-facto check; DOI remains an option if bounce rate exceeds 2% |

## Rollback
Delete `BREVO_API_KEY` in Vercel (the function then answers 500 and the forms show a plain error), or revert the PR; the old Brevo form still exists in Brevo.

## What does not change
Automations are still built by KT in the Brevo dashboard (no API). Service emails stay in Gmail. No domain for now (decision L-13).
