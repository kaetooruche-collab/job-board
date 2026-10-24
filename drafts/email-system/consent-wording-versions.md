# Consent wording versions (evidence)

Brevo's form submissions record when someone was added to a list, but not which wording they saw. This file is the record of the wording and the form behind each version. Add a row whenever a form or its wording changes. Never edit an old row.

| Version | Date live | Form (Brevo name) | Purpose | Exact wording shown |
|---|---|---|---|---|
| `legacy` | until 24 Oct 2026 | "RemoteNC Job Alerts Signup" (email only) | Job alerts | Site notice: "By subscribing you agree to receive our weekly job email. You can unsubscribe at any time." No tips box. |
| `signup-v1` | set on go-live | `Yireh Careers: job alerts signup` | Job alerts + optional tips | See `07-data-consent-event-model.md`, Wording v1 |
| `check-v1` | set on go-live | `Yireh Careers: free CV check` | Free check + optional tips | As above |
| `order-v1` | set on go-live | `Yireh Careers: order intake` | Order + optional tips | As above |

Contacts created before `signup-v1` are `legacy` and have no consent attributes. The two older non-KT contacts (created 14 and 18 Sept 2026) have no recorded source and receive nothing until KT confirms it.
