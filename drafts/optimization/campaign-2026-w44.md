# Campaign package — weekly job email, week of 28 Oct 2026

Prepared per the master prompt §6 (DRAFT). **No send has been made.** This is the first send ever,
so it stays behind initial authorisation: KT approves sender, list, consent process, content
standards and schedule, then presses send. After that approval, routine Tuesdays do not need
re-asking.

## Objective

Bring subscribers back to the board with genuinely useful, verified roles — and let the board do
the selling. Primary CTA: open the board. **No service pitch in this email**: consent class is
"job alerts", and the first send should establish that the email is worth opening, not that it is
an advert.

## Segment

**List: "Job alerts" (Brevo list 11)** — consent: job alerts, single opt-in. Three contacts, two
with recorded `legacy` consent from the old signup form and one `owner` test address. No
segmentation is applied (too few contacts to segment), no contact is added, no other list is
touched. Brevo suppresses blocklisted addresses automatically.

## Subject line options (pick one)

1. `299 new remote jobs this week` — **[recommended]** names the thing, 27 characters, no hype.
2. `299 new remote jobs, every one a direct link` — emphasises the differentiator.
3. `New this week: 299 remote roles` — plainer, lower pressure.

**Preheader:** `From starting out to senior. Each one links to the employer's own posting.`
(Already generated; it says what the subject does not, as the voice guide requires.)

## Email body

Ready-made HTML: **`data/weekly_digest.html`** — generated today with `make_digest.py --rename-note`,
so it carries the one-off line *"A quick note: RemoteNC is now Yireh Careers. It's the same weekly
job email, with the same one-tap unsubscribe."* Drop that line from the next generation (run
without the flag) once this first send is out.

The body is 6 verified roles grouped by level (starting out / mid / senior and leadership), each
linking straight to the employer's own posting, plus the board link and privacy link. Design and
copy come from `scripts/email_render.py` + `scripts/email_data.py` (template JA-D), which tests
guard (`tests/test_email_library.py`). Plain-text mirror for pasting: `data/weekly_digest.txt`.

### CTAs

- **Primary:** "See all 299" → `https://yirehcareers.vercel.app/?utm_source=brevo&utm_medium=email&utm_campaign=ja-d&utm_content=digest`
- **Secondary (justified):** none. One job per message — the footer privacy link and the
  unsubscribe are functional, not competing CTAs.

### Link verification (checked 28 Oct, HTTP status)

| Target | Status |
|---|---|
| Monzo job (Greenhouse) | 200 |
| Sword Health job (Greenhouse) | 200 |
| Headway job (Ashby) | 200 |
| Supabase job (Ashby) | 200 |
| Zapier job (Ashby) | 200 |
| GoHighLevel job (Lever) | 200 |
| Board link (UTM-tagged) | 200 |
| Privacy page | 200 |
| Unsubscribe | `{{ unsubscribe }}` — Brevo substitutes at send time (cannot be pre-checked without a send; see checklist) |

## Factual / compliance checklist

- [x] Every job and every link generated from the live `jobs.json` (968 listings, refreshed today 05:37 UTC) — none invented.
- [x] Subject states a count we can defend: 299 *new this week*, from the pipeline, not "299 jobs total".
- [x] No pay claim, no eligibility claim, no outcome promise in subject or preheader.
- [x] No promo inside a consent-class-S email (voice guide + CLAUDE.md rule).
- [x] Rename note present exactly once, for this first send only.
- [x] Unsubscribe present (`{{ unsubscribe }}`) — **must be clicked through in the Brevo preview before sending.**
- [x] Sender: "Yireh Careers" (sender id 4, yirehcareers@gmail.com) — the only verified sender.
- [x] UTM parameters on our own link (`utm_source=brevo&utm_medium=email&utm_campaign=ja-d&utm_content=digest`); employer links stay clean (they are outbound, and tagging them would be noise).
- [ ] **Duplicate-send protection:** confirm this campaign is the only one scheduled for the list (Brevo → Campaigns).
- [ ] **Test send:** send to kaetooruche@gmail.com first, open on a phone, check the logo renders and unsubscribe works.

## Send steps (KT, ~10 minutes)

1. Brevo → Campaigns → Create campaign (email), name `Weekly jobs 2026-10-28`.
2. From: **Yireh Careers** (yirehcareers@gmail.com). To: list **Job alerts**.
3. Subject: option 1 above; paste the preheader; paste `data/weekly_digest.html` into the body.
4. Send **a test** to yourself → open on your phone → tap the board link and the unsubscribe link.
5. Check Campaigns for anything already scheduled on that list (duplicate protection).
6. Schedule Tuesday 09:30 (your usual slot) or send now.
7. Tell me it's gone — I pull the numbers the next day (`utm_campaign=ja-d`) and record the result
   in the backlog: this is the first real data point in the whole funnel.

**Stop conditions (per the master prompt):** if consent looks wrong, links break, the unsubscribe
fails in preview, or deliverability warnings appear — do not send; report instead.

## Learning plan

Read after 7 days: delivered, bounces, unique clicks on the board link vs job links, sessions from
`utm_campaign=ja-d`, any `conversion-signup`, unsubscribes. Treat opens as unreliable (Apple/Mail
privacy distortion). Record counts, not trends — with 3 contacts, one click is a person, not a rate.