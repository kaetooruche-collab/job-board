# Yireh Careers social strategy (27 Nov 2026)

Owner: the social agency (Claude), under KT's approval rules (`social/OPERATING-SYSTEM.md`). Status: **v1, proposed**; the numbers that judge it start with the first scheduled week.
Labels: **[Established]** read in data we hold or an official source · **[Reported]** vendor or press · **[Hypothesis]** ours, to test.

## 1. What we are, from the live site (audited 27 Nov 2026)
- **The board:** "See which remote jobs hire where you live." Every card links to the original posting on the company's hiring page, shows its real posting date and says where applicants can be based ("Worldwide", a named country or region, or "Location not specified"). It's free; nobody pays to apply or to see a link. Listings come from companies' public job feeds, are re-checked at least daily, are under 30 days old and read as remote; pay is shown only when stated (`/verify`).
- **What "verified" does not mean:** we don't audit employers, can't see inside hiring, and don't confirm that someone from a given country will be accepted (`/verify`). Social copy never says more than that.
- **Paid services, kept separate from the board:** free CV check (one per person, CV by email, deleted within 30 days if no order); Essential $29, Professional $49, Executive $149 (30 days), LinkedIn Growth $99 a month, add-ons (`/services`, `site-config.js`). Orders go through WhatsApp and email; card checkout is off.
- **Conversion paths that exist:** board visit → filter by where you live → apply on the employer's page (free); email signup (weekly jobs email); free CV check form (`/free-check`); services page → WhatsApp.

## 2. Positioning on social
**Promise:** find the remote jobs that actually take applicants from where you live, with the evidence on every card.
**Why it's believable:** a link to the original posting, the employer's own location wording, the posting date, no fee.
**What it is not:** the only board with a country filter (Himalayas is promoted for exactly that by a Nigerian creator, `research/2026-11-26-niche.md`) [Established]. So we never claim to be the only one; we show the evidence.
**Honest about scarcity:** on 27 Nov, 27 of 1,987 remote postings were confirmed open worldwide after checking the employers' own data (`tools/verify_source.py`) [Established for that day]. We say what's true for the viewer and point them to filter by where they live, rather than implying plenty for everyone.

## 3. Who it's for (people, not personas)
Everyone looking for remote work, at every level; we don't assume they're young, unemployed or desperate (`AUDIENCE_RESEARCH.md`):
1. **People outside the US who keep hitting "US only"** (core; Canada, UK and Europe, Latin America, South and South-East Asia, Africa: KT 26 Nov).
2. **Students, graduates and early-career applicants** looking for a first remote role ("entry-level and junior", never "for students").
3. **Experienced professionals** weighing whether remote is realistic from where they live (the hypothesised paying customer for CV and LinkedIn work; `drafts/decisions/2026-10-24-board-strategy-icp-inventory-seniority.md`).
4. **People unsure whether it's their CV or the market**, the bridge to the free CV check.
US viewers are welcome but not chased.

## 4. Objectives and how each is measured
| Objective | Measure | Source | Note |
|---|---|---|---|
| Awareness | reach, 2-second hold, views per post | TikTok Studio, Instagram Insights (KT pastes); Buffer impressions | Buffer has no watch time |
| Trust and usefulness | saves and sends per reach | platform insights; Buffer reactions | Instagram's head ranks sends and likes; saves signal reference value |
| Qualified traffic | board visits by `utm_source` / campaign | GoatCounter (`tools/social_metrics.py`) | baseline 20-27 Nov: Facebook 9, Instagram 2 |
| Conversion (later) | free-check requests and signups after a social visit | GoatCounter conversion events | judged monthly, not per post |
High views don't equal good traffic: a post is judged on its own goal metric (`funnel` and `goal_metric` on every post).

## 5. Content system
- **Pillars:** 15 topics in five families, each with a share of the week (`CONTENT_PILLARS.md`).
- **Mix per week (6 posts, no Sunday):**
  - 2 videos: one presenter-led, one screen demonstration or data story;
  - 2 carousels: roles open beyond one country, plus a tip or myth;
  - 1 static or question post;
  - 1 flexible slot (safety, service, community).
  - Plus 2 Instagram Stories with the link sticker on roles days.
- **Service share:** at most 1 post in 6 mentions a paid service, never inside a jobs post; the free CV check leads.
- **Formats per platform:** `PLATFORM_GUIDELINES.md` (the format plan KT approved on 27 Nov).
- **Voice:** `.claude/skills/social-media-humanizer`; tone chosen per piece and varied across the week.
- **Video:** `.claude/skills/bhuman-presenter-director`; the cast of three (`PRESENTER_PROFILES.md`).

## 6. Channels
| Channel | Status | Role |
|---|---|---|
| TikTok @yirehcareers | connected (Buffer) | reach; photo carousels and video |
| Instagram yireh.careers | connected (Buffer) | Reels, carousels, Stories with link sticker |
| Facebook Page | connected (Buffer) | Reels and carousels with a tagged board link; where most social visits came from so far |
| YouTube Shorts | **not connected** | would reuse the vertical videos; Buffer's free plan allows 3 channels (all used) |
| LinkedIn (company page) | **not connected** | best fit for experienced professionals and the CV/LinkedIn services; same channel limit |
Adding YouTube or LinkedIn means a paid Buffer plan or swapping a channel: KT's decision (cost).

## 7. Timing and testing
- Start at 15:00 UTC, no Sunday, weekly video on Tuesday (`research/2026-11-26-posting-times.md`). Move a time only with our own data.
- **One meaningful variable at a time**, recorded on the post (`variable` field). Queue: hook type (fact vs situation), presenter vs screen-led, video length (15 s vs 30 s), caption opening (question vs statement), CTA (board vs filter vs save).
- No winner called under about 1,000 views per variant [our working rule]; Instagram Trial Reels for hook tests once videos run.
- Review every Friday (`social-weekly-review`); one change a week.

## 8. Guardrails (always)
No invented jobs, numbers, testimonials or outcomes. No promise of hiring. No "all remote jobs are worldwide". Numbers measured that day and dated. No fake urgency or scarcity. No country named in posts (KT, 26 Nov). No hiring-system names. Platform AI labels on, no visible AI badge (KT, 27 Nov). Nothing published without KT's approval (or the approved-material backup).
