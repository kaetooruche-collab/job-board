# How the social agency runs itself (27 Nov 2026)

KT asked (27 Nov): "you need systems, skills, agents that will run this agency autonomously." This is the map.

## The idea in one paragraph
Buffer can only be reached by Claude inside a session, so "autonomous" means: **scheduled Claude sessions** follow **written runbooks**, which call **scripts** that do the work and **gates** that refuse anything unsafe. KT sets the switches in `social/state.json` and is asked only for approvals, budgets and things nobody else can do (comments and DMs, app-only settings).

## The weekly loop
| When (Istanbul time) | Runbook (skill) | What happens | Needs KT? |
|---|---|---|---|
| Monday 09:43 | `social-weekly-plan` | Draft next week from the live board, finish scripts, render, check, review, commit; ask KT for "yes week <date>" | Yes, in `approve-week` mode |
| Mon-Sat 10:41 (posts go out at 18:00) | `social-daily-publish` | Re-measure numbers, re-open featured roles, re-render, check in schedule mode, gate, schedule in Buffer, log | No, once the week is approved |
| Friday 15:41 | `social-weekly-review` | Buffer numbers, board visits by platform, log, judge against each post's goal, one change for next week | Only to paste platform numbers Buffer can't read |
Scheduled tasks created 27 Nov with KT's yes; they fire into the social agency session (ids: plan trig_01DZVLMvHmVw5EstL27eSceH, publish trig_01PkKVZeEQ9JruuPT6VkQvy3, review trig_01GscxB42RQqnz9tbADCHYJj). KT's Google Calendar holds approve/check/review reminders for the first two weeks (30 Nov to 11 Dec).

## The switches (`social/state.json`, only KT changes them)
- `mode`: now `approve-week` (week of 1 Dec approved). **KT's yes is required** (KT, 27 Nov). Backup if KT can't check: escalating reminders, then after 23:00 Istanbul on the Monday before the week only KT-approved material goes out (`social/tools/backup.py`); new wording, scripts, presenters and service posts wait. KT's "no" or `hold` stops everything. `drafts-only` means plan and render, never schedule → `approve-week` (schedule a week after KT's recorded yes) → `autopilot` (schedule unless `hold`) · `hold` stops everything new.
- `bhuman_monthly_credit_budget`: 200 of the Ultimate plan's 500 a month; every render needs KT's yes on its estimate.
- `formats_plan_approved`: true since 27 Nov (Facebook tagged links, Instagram Stories on roles days, single role as a video).
- Presenter cast: `data/cast.json` (rotating presenter, each with a fixed voice, and a new setting each video).

## The scripts (`social/tools/`)
| Script | Job |
|---|---|
| `plan_week.py` | Drafts a week: slots, series, goal metric, a hook from `data/hook_bank.json` not used in 60 days, tip sets from `data/tip_sets.json`; marks what a human or Claude must write |
| `feed.py` | Live board numbers and the roles open beyond one country |
| `render_posts.py` + `shoot.js` | 1080x1350 slides and carousels |
| `slides_to_video.py` | Slides (and optional board footage) to a 1080x1920 video; free |
| `record-board-footage.js` | Board screen recording with no country shown |
| `verify-open.js` | Re-opens every featured posting on the day |
| `check_post.py` | The copy rules, automated (draft and schedule modes) |
| `backup.py` | When KT can't check: swaps unapproved posts for approved ones, or holds them |
| `buffer_payloads.py` | **The publishing gate**: refuses unless mode, approval, checker, same-day numbers, same-day role checks and public image links all pass; prints the exact Buffer calls |
| `social_metrics.py` | Board visits by platform from GoatCounter (needs its credential) |
| `build_calendar.py` | The readable calendar page for KT |

## The creative system (27 Nov 2026)
Skills: `social-media-humanizer` (all copy), `bhuman-presenter-director` (all presenter video). Documents: `SOCIAL_STRATEGY.md`, `AUDIENCE_RESEARCH.md`, `CONTENT_PILLARS.md`, `PLATFORM_GUIDELINES.md`, `PRESENTER_PROFILES.md`, `BHUMAN_WORKFLOW.md`, `BRAND_GUIDELINES.md`, `CONTENT_CALENDAR.md`, `PERFORMANCE_LOG.md`. Tools added: `voice_qc.py` (transcript, pace, pauses, loudness), `compose_video.py` (brand captions, b-roll, -14 LUFS), `verify_source.py` (cards match the employer's data).

## The team (27 Nov 2026, KT: "different agents or skills so the best possible output is produced")
Each role is a separate agent in `.claude/agents/`, so it works in a fresh context with only its own instructions and tools. The main session is the **producer**: it runs the pipeline, talks to KT, and is the only one that spends BHuman credits or schedules.
| Step | Agent | Produces |
|---|---|---|
| 1 Research | `social-researcher` | `social/research/<date>-<topic>.md`: pain points in their words, stats with sources and tiers, angles to use, things not to claim |
| 2 Plan | `social-planner` | the week's `posts.json`, balanced by pillar, tone, format and test; assignments; credit estimate |
| 3 Copy | `social-copywriter` | hooks (5 options, 1 chosen), per-platform captions, slide and on-screen text, scripts for the ear (`TONE_OF_VOICE.md`, humanizer) |
| 4a Design | `social-designer` | slides, covers, Story frames, rendered and inspected, plus `preview.jpg` |
| 4b Video | `social-video-editor` | composited videos (captions, b-roll, -14 LUFS, watermark cropped) with QC in the brief; BHuman renders are done by the producer after KT's yes |
| 5 QA | `social-qa` | PASS / BLOCK / WARN per post: truth, rules, tone, conversion score, video frames |
| 6 Catalogue | `python3 social/tools/catalog.py` | `social/CATALOG.md` and `.csv`: every piece, its status, assets, approvals, Buffer ids and results |
| 7 Publish | producer + `social-daily-publish` + the gate | scheduled posts and the log |
| 8 Review | producer + `social-weekly-review` | the week's numbers and one change, which feeds back into step 1 |

## The reviewer (now QA)
`.claude/agents/social-qa.md`: the QA agent, a fresh-eyes critic that reads the posts and images and returns BLOCK/WARN. It cannot edit, schedule or publish.

## What stays with KT
Comments and DMs, the AI label on Facebook (Buffer can't set it), any spend, changing `state.json`, new countries or languages, the CV-service posts' wording, and anything in CLAUDE.md that says "KT's approval".

## Tests
`python3 -m pytest -q social/tools/tests`: the checker, every hook-bank line, and the gate's refusals.
