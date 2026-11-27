# How the social agency runs itself (27 Nov 2026)

KT asked (27 Nov): "you need systems, skills, agents that will run this agency autonomously." This is the map.

## The idea in one paragraph
Buffer can only be reached by Claude inside a session, so "autonomous" means: **scheduled Claude sessions** follow **written runbooks**, which call **scripts** that do the work and **gates** that refuse anything unsafe. KT sets the switches in `social/state.json` and is asked only for approvals, budgets and things nobody else can do (comments and DMs, app-only settings).

## The weekly loop
| When (Istanbul time) | Runbook (skill) | What happens | Needs KT? |
|---|---|---|---|
| Monday 10:00 | `social-weekly-plan` | Draft next week from the live board, finish scripts, render, check, review, commit; ask KT for "yes week <date>" | Yes, in `approve-week` mode |
| Tue-Sat and Mon, 11:00 (4 h before posting) | `social-daily-publish` | Re-measure numbers, re-open featured roles, re-render, check in schedule mode, gate, schedule in Buffer, log | No, once the week is approved |
| Friday 16:00 | `social-weekly-review` | Buffer numbers, board visits by platform, log, judge against each post's goal, one change for next week | Only to paste platform numbers Buffer can't read |
The times are a proposal; the scheduled tasks are created only after KT's yes.

## The switches (`social/state.json`, only KT changes them)
- `mode`: `drafts-only` (now: plan and render, never schedule) → `approve-week` (schedule a week after KT's recorded yes) → `autopilot` (schedule unless `hold`) · `hold` stops everything new.
- `bhuman_monthly_credit_budget`: 0 now, so videos are the free screen-only kind.
- `formats_plan_approved`: false now, so every post goes to all three platforms as one file.

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
| `buffer_payloads.py` | **The publishing gate**: refuses unless mode, approval, checker, same-day numbers, same-day role checks and public image links all pass; prints the exact Buffer calls |
| `social_metrics.py` | Board visits by platform from GoatCounter (needs its credential) |
| `build_calendar.py` | The readable calendar page for KT |

## The reviewer
`.claude/agents/social-reviewer.md`: a fresh-eyes critic that reads the posts and images and returns BLOCK/WARN. It cannot edit, schedule or publish.

## What stays with KT
Comments and DMs, the AI label on Facebook (Buffer can't set it), any spend, changing `state.json`, new countries or languages, the CV-service posts' wording, and anything in CLAUDE.md that says "KT's approval".

## Tests
`python3 -m pytest -q social/tools/tests`: the checker, every hook-bank line, and the gate's refusals.
