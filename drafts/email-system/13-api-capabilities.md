# 13 · What the Brevo API key can and cannot do (tested 24 Oct 2026)

Method: with the key KT created, every call below was made from the cloud session against `https://api.brevo.com/v3`. Account confirmed first (KAYZ Global Ltd, kaetooruche@gmail.com, Free plan). Nothing was sent, no contact was created or changed. No secret is stored in the repo.

## Why the first attempt failed
The key Brevo shows in its dashboard is a **base64 text** (it starts `eyJ...`) that wraps the real key (`xkeysib-...`). The environment variable held that wrapped form, so Brevo answered 401 "Key not found". **Put the plain `xkeysib-...` key in `BREVO_API_KEY`**, not the `eyJ...` text. (Decoding it, which was done in memory only, worked at once.) A new key only reaches a *new* session.

## Scope of this key: effectively full account access
Tested with real calls. "Read" means a GET worked; "write" means a create, change or delete was done in the build.

| Area | Result | Notes |
|---|---|---|
| Account details | read 200 | Plan Free, marketing automation enabled |
| Lists and folders | read, **write**, delete | Created 3 lists, renamed list 11, deleted 6 empty lists |
| Contact attributes | read, **write** | Created 8 attributes |
| Contacts | read 200 | Not written (rule: no contact changes before go-ahead). Contacts have no "source" field, so provenance of the two older subscribers cannot be read |
| Segments | **list only** (returns none); create gives 404 | Segments must be built in the dashboard |
| Email templates | read, **write**, delete | Created 8; deleted 11. A template must be set inactive before it can be deleted |
| Email campaigns | read, delete | Deleted two drafts. Not sent |
| Senders | read 200 (id 4 only) | Create and update exist in the API; not needed |
| Domains | read 200 (none yet) | `POST /senders/domains` and `/authenticate` exist: **usable once a domain is bought** |
| Webhooks | read ("none exist") | Create and delete exist; not needed in the chosen design |
| Custom events | read 200 | `POST /events` exists; could trigger an automation whose trigger is "Custom event" (Stage 2 option) |
| Blocklist | read 200 | Can see blocked contacts and domains |
| Users | read 200 | Only KT, owner |
| Sales CRM, companies, loyalty | read 200 | Not used |
| Consent groups | **403 CONSENT_GROUP_NOT_ENABLED** | Feature not on this account; we use lists and attributes instead |
| Account activity log | **400 "Upgrade to Enterprise plan"** | Cannot see who changed what |
| WhatsApp | **403 plan not eligible** | |
| Corporate and sub-accounts | **403 not a corporate account** | |
| **Automations (workflows)** | **404 on every route tried; none in Brevo's API reference** | **Cannot create, edit, activate, pause, list or read automations** |
| **Forms** | **404; none in the reference** | **Cannot create or read forms** |
| Dedicated IPs | read 200 (none) | |

Technical note for scripts: Brevo's `/senders` and `/senders/domains` sit behind a firewall rule that rejects the default Python user agent (Cloudflare error 1010). Send a normal `User-Agent` header (for example `curl/8.5.0`) and they work.

## What was built with it
| Object | Result |
|---|---|
| List 11 | Renamed to **Job alerts** (3 contacts kept) |
| New lists | **18 Career tips**, **19 Check result sent**, **20 Order completed** |
| New attributes | `CONSENT_JOBS_AT`, `CONSENT_JOBS_SRC`, `CONSENT_TIPS_AT`, `CONSENT_TIPS_SRC`, `LEVEL_INTEREST`, `STAGE`, `LAST_PACKAGE`, `COMPLETED_ON` |
| New templates (sender Yireh Careers, reply-to yirehcareers@gmail.com) | 74 JA-1, 75 CT-1, 76 CT-2, 77 CT-3, 78 JA-R, 79 CT-M1, 80 CT-M2, 81 CT-M3, 82 FC-1, 83 CU-1-ES, 84 CU-1-PRO, 85 CU-2 (all 12 Brevo emails except the digest, which is a weekly campaign) |
| Deleted | Lists 12-17 (empty), draft campaigns 19 and 53, templates 63-73 |
| Left alone | Sent campaigns 17, 18; templates 1, 2, 5-16; lists 6-10; templates 54-61 (belong to automations KT built) |
| Verified by reading back | Lists, campaigns, templates and attributes match the plan |

## What the key cannot do, so KT does it (see `12-dashboard-build-guide.md`)
1. **Pause or delete automations #3, #9, #10**, then delete their step templates 54-61.
2. **Build the three forms** (signup, free check, order intake).
3. **Build the automations** AU-1 to AU-4.
4. **Create segments** (Tips eligible, Dormant, Needs consent audit).
5. **Check the two older contacts' signup records** in each contact's timeline.
6. **Run the tests that need real inboxes** (T6 headers, T7 per-list unsubscribe, T5 blocklist and form).
7. **Buy the domain** (Vercel) and click **Authenticate** in Brevo. Claude can create the Brevo domain record and the DNS records with this key and the Vercel connection, if the key is still active then.

## Recommendation on the key
- **Keep it until the domain is authenticated and the first real send is done**, because that is the last step that benefits from the API (domain creation and checks, template updates when copy changes).
- **Then revoke it** in Brevo (SMTP and API, API keys), remove `BREVO_API_KEY` from the cloud environment, and turn Brevo's "Block unknown IP addresses" back on. The key was pasted into a chat once; treat that chat as containing a secret and do not leave the key active longer than needed.
- Use the plain `xkeysib-...` form only, and never put it in the repo.
