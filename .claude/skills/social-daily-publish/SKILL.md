---
name: social-daily-publish
description: Daily runbook for the Yireh Careers social agency - on a posting day, re-measure numbers, re-open featured roles, re-render, and schedule that day's posts in Buffer through the publishing gate. Use when a scheduled daily session fires, or when KT says "schedule today's posts".
---

# Daily publish (posting days: Tue to Sat and Mon; no Sunday)

The gate decides; this session does not override it. Read `social/state.json` first.

1. **Today's posts.** Find today's date in `social/calendar/*.posts.json`. None? Stop quietly.
2. **Mode.** `drafts-only` or `hold`: stop and say so in one line. In `approve-week`, a week KT hasn't answered goes ahead automatically after its deadline (the gate checks; KT, 27 Nov: "my yes should not hold up things"). KT's "no" stops it. Say in the report whether the week ran on KT's yes or automatically.
3. **Fresh numbers and roles** (CLAUDE.md: numbers measured on the post day; roles re-opened that day):
   - `curl -s https://yirehcareers.vercel.app/jobs.json -o <scratchpad>/jobs.json`
   - Set each post's `measured_on` to today. Re-render: `python3 social/tools/render_posts.py <posts.json> --feed <scratchpad>/jobs.json --only <post id>` then `node social/tools/shoot.js <dir>`.
   - `node social/tools/verify-open.js <dir>/manifest.json`. A failure: add the job to `social/data/exclude_jobs.json` and `social/board-issues.md`, re-render, verify again. Two failures in a row: skip the post, tell KT.
   - Format plan (on since 27 Nov): Friday's single role goes out as a video: `python3 social/tools/slides_to_video.py <dir>` after rendering. The gate adds a tagged board link to Facebook captions and an Instagram Story (slide 1 + link sticker, 30 minutes after the post) on roles-carousel days.
   - Weekly video with a presenter not yet rendered: `plan_render` (free). Start it if KT said yes, or under the standing confirmation if the estimate is at most `bhuman_max_credits_per_render_without_answer` and within the month's budget; log the credits in `state.json` `bhuman_credits_spent`, poll `get_render`, download the MP4 into the post's output folder as `video.mp4`. Otherwise make the free screen-only version. Either way the post goes out on time.
4. **Check.** `python3 social/tools/check_post.py <posts.json> --mode schedule` must show 0 blocked for today's posts.
5. **Publish media.** Commit and push the new images (Buffer fetches them from raw.githubusercontent.com).
6. **Gate.** `python3 social/tools/buffer_payloads.py <posts.json> --date <today>`. Refused: report the reason and stop. Never edit the gate, the state file or a post to get past a refusal (KT changes state; the post gets fixed properly).
7. **Schedule.** For each payload, call Buffer `create_post` with exactly those fields (drop the keys starting with `_`). Call `get_account` first for the organisation and current time; the gate already converted `dueAt` to the account's time zone.
8. **Record.** `python3 social/tools/buffer_payloads.py <posts.json> --record <post id>:<platform>:<buffer id>` for each, then commit `social/post-log.csv`.
9. **Report** one line per post: scheduled for when, on which platforms, Buffer id.

Never: reply to comments or DMs (KT's), spend BHuman credits beyond `bhuman_monthly_credit_budget`, publish "now" instead of scheduling, or post to a channel not listed in the agency skill.
