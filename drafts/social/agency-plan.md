# Yireh Careers social agency: plan (26 Nov 2026)

Status: **PROPOSED**. The session and Phase 0 start now; publishing waits for KT's setup and decisions (section 6).
KT, 26 Nov 2026: "I want you to handle automatically the creation of the videos, the posting of the videos, pictures,
posts, scheduling, everything for all platforms by yourself ... another session that is dedicated to just being
essentially the social media agency for this particular brand, but that is still connected to the job board."

## 1. How it is set up
| Piece | What it is |
|---|---|
| Agency session | A separate Claude cloud session, "Yireh Social Agency", on this same repository but its own branch `claude/social-agency`. It never edits the site, the pipeline or `jobs.json`; the job-board session never edits `social/`. |
| Sync with the board | Every plan and every post reads the **live** feed (`https://yirehcareers.vercel.app/jobs.json`) and pulls `main` for rule changes (CLAUDE.md, copy rules, decisions). Numbers in posts are measured the same day. |
| Operating manual | Skill `.claude/skills/social-agency/SKILL.md`: the weekly cycle, recipes, guardrails, what needs KT. |
| Working files | `social/`: brand guide, content calendar, scripts, post log, performance log, research. |
| Publishing | **Postiz** (one API for Instagram, TikTok and Facebook: schedule, publish, analytics). TikTok posts use `DIRECT_POST`. |
| Production | BHuman (presenter and voice, the video 1 recipe), live-board screen recordings and ffmpeg assembly (free), image and carousel posts rendered from the live feed (free). |
| Rhythm | Scheduled tasks into the agency session: Monday plan, daily produce-and-check, Friday performance review. |
| Measurement | Postiz analytics (views, watch time, follows, per post) plus GoatCounter visits from `utm_source=tiktok|instagram|facebook` links, then apply clicks and CV enquiries. |

## 2. What it posts (starting point; changed by results, not taste)
1. **The weekly jobs video** (Tuesdays, all three platforms): video 1's format, presenter for the hook and the ending, the live board in the middle, a different opening each week (testing one variable).
2. **Real roles, posted as images or carousels** (3 a week): roles open to many countries first (worldwide and region-wide), each with "where you can apply from", the posted date, and the link in bio. No country named (KT, 26 Nov).
3. **Short "check this before you apply" tips** (2 a week): eligibility wording, scam signs (no fees, no Telegram interviews), reading a posting. Screen-led, no presenter needed.
4. **The CV service**: at most 1 in 6 posts, never inside a jobs post (copy rule).

## 3. Guardrails, checked automatically before anything is scheduled
- **CLAUDE.md copy rules:** no "guaranteed", no "the only", no hiring-system names, no "direct to the employer", no claim that a role suits a background; "free, and we never charge you to apply" said once.
- **Numbers:** every number is measured on the live board that day and dated on screen.
- **Countries:** no country named in videos (KT, 26 Nov 2026).
- **AI label:** any post with the AI presenter or a cloned voice gets the platform's AI-generated label switched on.
- **Calls to action:** never "DM me" or "comment for the list" (the scam pattern our audience fears). The CTA is the link in bio.
- **Spelling:** on-screen text and captions are spell-checked. (The 26 Nov Instagram thumbnail said "DOSEN'T".)
- **Language:** KT's voice and copy guide: short, warm, plain, one next step.

## 4. The process for every week (KT's: think, gather, catalogue, checklist, execute)
1. **Monday, gather:** last week's numbers, the live board (what's new, what's open widely), comments and DMs (questions in the audience's own words), and what the niche is posting.
2. **Catalogue and decide:** pick the week's posts and the one thing being tested.
3. **Checklist:** each post gets its acceptance tests (the guardrails above, plus its numbers).
4. **Execute:** produce, check, schedule.
5. **Friday:** review, then write what was learned into `social/learnings.md`.

## 5. Phases
- **Phase 0 (starts now, no spending, no posting):** research, brand guide, the first two weeks' calendar and scripts, and the production scripts (footage recorder, image and carousel renderer, caption checker).
- **Phase 1 (after KT's setup):** two weeks of "approve the week". On Monday KT gets the week's posts in one message and replies yes or with changes. Then everything is scheduled.
- **Phase 2:** autopilot. Posts go out unless KT says "hold". KT only hears about results and anything that needs a decision.

## 6. What only KT can do (one-off setup)
1. **Postiz:** create an account (7-day trial, then about $29 a month, Standard, 5 accounts; check the current price on postiz.com). Then connect TikTok, Instagram and the Facebook Page inside Postiz.
2. **Facebook:** create the Yireh Careers Facebook Page, and link the Instagram account to it (needed for Reels audio through Postiz).
3. **Keys:** give the agency session the Postiz API key, and a BHuman key, through the secure form it shows (never in chat).
4. **Decisions:**
   - (a) Approve "approve the week" for 2 weeks, then autopilot. This is a standing approval for public posts under the guardrails above, as an exception to the CLAUDE.md copy-change rule.
   - (b) A monthly BHuman credit budget for videos (video 1 used about 96 credits).
   - (c) Whether replies to comments and DMs stay with KT (recommended at first).
