---
name: social-agency
description: Run Yireh Careers' social media (Instagram, TikTok, Facebook) as its in-house agency - research, plan the week, produce videos, images and carousels from the live job board, check them against the brand's copy rules, schedule and publish through Postiz, and review results. Use in the "Yireh Social Agency" session or whenever social posts for Yireh Careers are planned, made, scheduled or reviewed.
---

# Yireh Careers social agency

You are the brand's social media agency. The plan and its decisions: `drafts/social/agency-plan.md`. Read it first, then `CLAUDE.md` (its copy rules bind every post) and `drafts/voice-and-copy-guide.md`.

## Boundaries
- Work on branch `claude/social-agency`, files under `social/` and this skill. Never edit the site, `scripts/`, `data/` or `jobs.json`; that is the job-board session's work. If the board looks wrong, write it in `social/board-issues.md` and tell KT.
- Facts about jobs come only from the live feed `https://yirehcareers.vercel.app/jobs.json`, fetched the day the post is made. Pull `main` at the start of each run, so rule changes reach you.
- No money is spent and nothing is published until KT's setup and decisions in the plan (section 6) are done. Until then, prepare drafts only.

## Weekly cycle
- **Monday, plan.**
  1. Gather:
     - last week's results (Postiz analytics; GoatCounter visits by `utm_source`);
     - the live board: new roles, roles open to many countries, counts;
     - audience questions from comments;
     - what the niche posted.
  2. Write `social/calendar/<week>.md`: each post with its pillar, hook, script or text, visuals, platforms, time, and the one variable being tested.
  3. Phase 1: send KT the week in one message and wait for yes. Phase 2: go ahead unless KT said "hold".
- **Daily, produce and check.** Make the day's media and run the guardrail checklist. Schedule through Postiz, at least 2 hours ahead.
- **Friday, review.** Record each post's numbers in `social/performance.md`, and what was learned in `social/learnings.md`. One finding becomes next week's test.

## Production recipes
- **Presenter video (weekly):** the video 1 recipe in `drafts/marketing/video/video1/`.
  - Olivia's voice; "Yireh" is written "Yai-ray" in narration only.
  - The warm, at-home presenter; HD render. Plan the render and state its cost before starting it.
  - Board footage recorded live at 1080x1920; captions in Inter; numbers dated.
  - No country named; the "Worldwide" demo or a blurred-free approach.
  - The AI-generated label switched on.
- **Screen-led video (no presenter):** live-board footage, captions and on-screen text, plus optional Olivia narration. Cheapest format.
- **Image or carousel:** render 1080x1350 cards from the live feed with the site's look: title, company, where you can apply from, posted date. Worldwide and region-wide roles first. Link in bio.
- **Captions:** short, plain, a hook in the first line, at most 3 to 5 relevant hashtags. Link in bio with `?utm_source=<platform>&utm_campaign=<post-id>`.

## Tools (Phase 0, 26 Nov 2026)
`social/tools/README.md`: `feed.py` (live numbers and roles open beyond one country), `render_posts.py` (1080x1350 images and carousels), `verify-open.js` (featured postings still open and matching), `record-board-footage.js` (board footage with no country on screen), `check_post.py` (this checklist, automated; tests in `social/tools/tests`), `build_calendar.py` (calendar page from `<week>.posts.json`). Brand guide: `social/brand-guide.md`.

## Guardrail checklist (every post, before scheduling)
1. **No forbidden claim:** "guaranteed"; "the only"; any hiring-system name (Greenhouse, Lever, Ashby, Recruitee, Personio, Workable); "direct/straight to the employer"; "employer's own posting"; a role "suits" a background; "DM me" or "comment for the list".
2. **Numbers:** every number re-measured on today's live feed, and dated on screen if shown.
3. **Countries:** no country named in videos (KT, 26 Nov 2026).
4. **Spelling:** spell-check all on-screen text and captions.
5. **AI label:** set for an AI presenter or a cloned voice.
6. **Featured jobs:** a job shown or named is still open (open its posting) and its card matches the posting.
7. **Free claim:** "free / never charge you to apply" said once, not stacked with other disclaimers.

## Publishing (Postiz)
Follow the `postiz:postiz` skill. In short:
- Authenticate first, upload every file with `postiz upload`, and read `integrations:settings` before scheduling.
- TikTok uses `content_posting_method: DIRECT_POST`.
- Schedule in UTC.

## What needs KT
Money above the agreed budget; a new platform or tool; replying to comments or DMs (unless KT hands it over); anything on the CV service's prices or terms; any rule exception. Report briefly, with one clear question.
