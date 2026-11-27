---
name: social-agency
description: Run Yireh Careers' social media (Instagram, TikTok, Facebook) as its in-house agency - research, plan the week, produce videos, images and carousels from the live job board, check them against the brand's copy rules, schedule and publish through Buffer, and review results. Use in the "Yireh Social Agency" session or whenever social posts for Yireh Careers are planned, made, scheduled or reviewed.
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

## Who decides wording (KT, 27 Nov 2026)
Small wording (hooks, covers, captions, CTAs) is the agency's call, aimed at conversion, inside CLAUDE.md's copy rules and the humanizer skill; log it on the post as `copy_edits` (`state.json` copy_authority). Don't ask KT about it. Ask KT only about new claims, prices, service terms, spend and publishing approvals.

## Mandatory skills for every piece (27 Nov 2026)
- Any words the accounts will show or say: `.claude/skills/social-media-humanizer/SKILL.md` (tone, first impression, read-aloud test).
- Any presenter video: `.claude/skills/bhuman-presenter-director/SKILL.md` (cast, direction sheet, credits, voice_qc, compose_video).
- Strategy and references: `social/SOCIAL_STRATEGY.md`, `AUDIENCE_RESEARCH.md`, `CONTENT_PILLARS.md`, `PLATFORM_GUIDELINES.md`, `PRESENTER_PROFILES.md`, `BHUMAN_WORKFLOW.md`, `BRAND_GUIDELINES.md`, `CONTENT_CALENDAR.md`, `PERFORMANCE_LOG.md`; video briefs in `social/video-briefs/` (TEMPLATE.md).

## Operating system (27 Nov 2026)
The runbooks `social-weekly-plan` (Monday), `social-daily-publish` (posting days) and `social-weekly-review` (Friday), the `social-reviewer` agent, the switches in `social/state.json` and the publishing gate `social/tools/buffer_payloads.py` are mapped in `social/OPERATING-SYSTEM.md`. Read it before any scheduled run.

## Tools (Phase 0, 26 Nov 2026)
`social/tools/README.md`: `feed.py` (live numbers and roles open beyond one country), `render_posts.py` (1080x1350 images and carousels), `verify-open.js` (featured postings still open and matching), `record-board-footage.js` (board footage with no country on screen), `check_post.py` (this checklist, automated; tests in `social/tools/tests`), `build_calendar.py` (calendar page from `<week>.posts.json`). Brand guide: `social/BRAND_GUIDELINES.md`.

## Review passes (every post, after the checker passes; written in the week's calendar notes)
Adapted from safrin96/agentic-content-system's review protocol (MIT; idea only). One line each, then GO or NO-GO:
1. **Skeptic:** is there a specific, checkable fact (a real role, a dated number), or is it generic?
2. **Scroller:** does the first line or first second stop a thumb, read on a phone, in a second language?
3. **Competitor:** would the big remote-job accounts post this as is? If yes, what makes ours different (evidence on the card, who can apply)?
4. **Editor:** one next step; the funnel stage and goal metric fit the post; no stacked disclaimers.
The checker also blocks a hook repeated within 60 days (`series` posts are only flagged) and a post without `funnel` and `goal_metric`. Results go in `social/post-log.csv` (see `social/post-log.md`). Evidence for these choices: `social/research/2026-11-27-agency-repos-assessment.md`.

## Guardrail checklist (every post, before scheduling)
1. **No forbidden claim:** "guaranteed"; "the only"; any hiring-system name (Greenhouse, Lever, Ashby, Recruitee, Personio, Workable); "direct/straight to the employer"; "employer's own posting"; a role "suits" a background; "DM me" or "comment for the list".
2. **Numbers:** every number re-measured on today's live feed, and dated on screen if shown.
3. **Countries:** no country named in videos (KT, 26 Nov 2026).
4. **Spelling:** spell-check all on-screen text and captions.
5. **AI label:** set for an AI presenter or a cloned voice.
6. **Featured jobs:** a job shown or named is still open (open its posting) and its card matches the posting.
7. **Free claim:** "free / never charge you to apply" said once, not stacked with other disclaimers.

## Publishing (Buffer, connected 27 Nov 2026; replaces Postiz)
- Buffer organisation "My organization" (`6b092db6e98ed22e37731d71`), free plan: 3 channels, 10 scheduled posts per channel at a time (refills as posts go out), 30 days of analytics.
- Channels: Facebook Page "Yireh Careers" `6b0931cb8541f09ecbbe07af`; TikTok @yirehcareers `6b092ffc8541f09ecbbdfa1d`; Instagram yireh.careers (business) `6b092f368541f09ecbbdf3ab`.
- Media must be a public URL: commit the rendered files to `social/output/` on this public repo and use `https://raw.githubusercontent.com/kaetooruche-collab/job-board/claude/social-agency/social/output/...` (push first, check the URL returns 200).
- `schedulingType: automatic`; times from `get_account` (account time zone Europe/Istanbul); Instagram needs `metadata.instagram.type` (`post`, or `reel` for a video) with `shouldShareToFeed: true`; Facebook needs `metadata.facebook.type`.
- AI label: set `isAiGenerated: true` on TikTok and Instagram for presenter or AI-voice videos. Buffer has no AI flag for Facebook, so presenter videos go to Facebook only if KT ticks "AI info" by hand; otherwise post the screen-led version there.
- Results: `get_aggregated_post_metrics` (Buffer) plus GoatCounter visits by `utm_source`.
- BHuman: key in the environment's network secrets for `speakeasy.bhuman.ai` (MCP over HTTP). Never spend credits beyond KT's budget; never use the "leadr" email-campaign tools.

## What needs KT
Money above the agreed budget; a new platform or tool; replying to comments or DMs (unless KT hands it over); anything on the CV service's prices or terms; any rule exception. Report briefly, with one clear question.
