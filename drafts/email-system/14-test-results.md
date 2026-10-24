# 14 · Test results (run by Claude, 24 Oct 2026)

Method: tests ran against the live Brevo account and the live signup form, using plus-addresses of KT's own Gmail (`kaetooruche+yct1@gmail.com` and similar, which deliver to KT's inbox) and a one-recipient campaign to a list that held only a test address. Responses were read back through the Brevo API and the Gmail connection. All test contacts were deleted afterwards (contacts are back to 3). Nothing went to anyone but KT's own mailbox.

| Test | Result | What was observed |
|---|---|---|
| **T1** form → list | **Pass, with a gap** | The live signup form puts a new contact on list 11 (Job alerts) and the form answers `{"success":true,"message":"Your subscription has been successful."}`. **No consent attribute is set** (the form is email-only and has no tips box, consent text or hidden fields), so `CONSENT_JOBS_AT` stays empty. The new form must set it (T2) or the date is added later |
| **T2** hidden field / consent attribute | **Not testable by Claude** | Needs the new form to exist (KT builds it). The current form has no hidden consent field. The form is still called "RemoteNC Job Alerts Signup" inside Brevo (old name) |
| **T3** add to list starts an automation | **Not testable yet** | No automation exists. The form did **not** send any welcome email to the test addresses, confirming that nothing currently triggers on a list add. Rerun after AU-1 is built |
| **T4** condition step in automations | **Not testable by Claude** | Only visible in the dashboard editor; KT answers it while building AU-3 and AU-4 |
| **T5** blocklisted contact submits the form again | **FAIL: important** | After blocklisting a test contact, submitting the live form again **set `emailBlacklisted` back to false**. So anyone, including a bot or someone typing another person's address, can reverse an unsubscribe or complaint through the signup form. This breaks rule C-8 and is now risk RK-27. Recommended fix: turn on **double opt-in** on the signup form (see 12, Part B). That needs KT's decision (D-11 reopened) |
| **T6** headers and authentication | **Pass** | The received Brevo email has `List-Unsubscribe` and `List-Unsubscribe-Post: List-Unsubscribe=One-Click` (one-click unsubscribe), DKIM pass, SPF pass, DMARC pass. All three are for Brevo's sending domain (`brevosend.com`), not for gmail.com, as expected: the visible From address is `yirehcareers@10516007.brevosend.com` with replies going to yirehcareers@gmail.com. **Defect found and fixed:** the From name read "Hibarr" because the templates carried no sender name. All 12 templates now carry the name "Yireh Careers" (verified by reading back and by Gmail's `from:"Yireh Careers"` matching both a template test and a real campaign email) |
| **T7** unsubscribe from tips only | **FAIL: design change needed** | A real campaign email to the Career tips list was unsubscribed through its link. Brevo's default unsubscribe page offers a single "Unsubscribe" button for "marketing emails from us". Result: the contact became **blocklisted globally** (and stays on both lists, but nothing is sent). So tips and job alerts cannot be unsubscribed separately with this page. Unsubscribe links in *template test* emails do nothing (the contact stayed subscribed), so only real sends test this |
| **T8** real inbox rendering | **Partly done** | Tested emails reached Gmail's inbox: the welcome in **Updates**, tips in **Promotions** (normal for promotional mail, not spam). The first-name merge works and falls back to "Hi there,". Outlook, Apple Mail and phones not tested by Claude |
| **T9** duplicate submit | **Pass** | Two simultaneous submissions of one address produced one contact and two identical success replies |

## What changed because of the tests
1. **Signup message** now reads the form's real answer (the form allows our site's origin and returns JSON): "Thanks, you're on the list. Your weekly job email will arrive in your inbox." on success; a plain error otherwise. It no longer promises a welcome email, because none is triggered yet. Tested in a browser with four mocked answers (success, failure, non-JSON, network error).
2. **All 12 templates** got the From name "Yireh Careers".
3. **Footers:** every Brevo email now says "Unsubscribe from all our emails", and promotional emails add: "Only want the weekly job email? Reply 'jobs only' and we'll stop the tips." (KT then removes that contact from the Career tips list; it is manual and rare.) This replaces the design assumption that one click could stop only one purpose.
4. **Risk register and rules** updated (RK-27, RK-28; C-8 and C-9 restated).

## Re-tests after the server function (24 Oct, live Brevo, KT's plus-addresses, all deleted afterwards)
| Test | Result |
|---|---|
| **T5** blocklisted address submits the signup | **Pass:** contact stays blocklisted, nothing written, the visitor is told plainly |
| **T1** consent evidence | **Pass:** `CONSENT_JOBS_AT`/`SRC`, `CONSENT_TIPS_AT`/`SRC`, level, stage and lead source set; repeat signup does not overwrite the original consent |
| **T2** wording version stored | **Pass:** `signup-v1`, `check-v1`, `order-v1` set by the function |
| **T9** three parallel submissions | **Pass** after a retry fix: one contact, three successes |
| Free check and order | **Pass:** no marketing list for the check; the order sets `LAST_PACKAGE`; a notice email to yirehcareers@gmail.com showed as *delivered* in Brevo's event log |
| Origin check | **Pass:** another origin gets 403 |

## T3 and T4 (24 Oct, after KT built the four automations)
| Check | Result |
|---|---|
| AU-1 starts on **form signup** (jobs only, and jobs + tips) | **Pass.** Welcome (copy 87) arrived within seconds, first name merged ("Hi Aa") |
| AU-1 starts on **API add** to Job alerts | **Pass.** Same email, same speed |
| AU-1 does NOT fire for the **free-check form** (no Job alerts list) | **Pass** (no email) |
| AU-2 does not send CT-1 immediately (one-day wait) | **Consistent so far:** nothing arrived for tips contacts added by form (t3b, t3c) or by API (t3d). The positive proof (CT-1 arriving after a day) is scheduled for ~15:20 UTC on 25 Oct |
| AU-3 and AU-4 start from the marker lists | **Pass (KT, 24 Oct):** the test contacts show correctly in both automations. Their waits are 4 and 21 days, so the final emails will only prove themselves on those dates (the scheduled test contacts are deleted after the AU-2 check) |
| T4 condition step exists | **Yes**, KT built conditions in AU-3 and AU-4 (confirmed by KT's message that the automations are built as specified; ask KT if any condition was missing) |

## Leftovers
- Campaign **86** ("TEST T7 delete me", sent to the test address) cannot be deleted through the API once sent. KT may delete it in the dashboard (Campaigns); it holds no personal data beyond the deleted test address.
- Test addresses deleted: yct1, yct5, yct7, yct9. Verified: 3 contacts, list 18 empty.
