---
name: social-weekly-plan
description: Monday runbook for the Yireh Careers social agency - draft next week's posts (Tue to Mon) from the live board, finish anything marked needs_writing, render, check and hand the week to KT for approval. Use when a scheduled Monday session fires, or when KT says "plan next week".
---

# Weekly plan (Mondays)

Read first: `social/OPERATING-SYSTEM.md`, `social/state.json`, `.claude/skills/social-agency/SKILL.md` (rules), `social/brand-guide.md`.

1. **State.** If `mode` is `hold`, stop and tell KT nothing was planned. Otherwise continue (planning is allowed in every other mode).
2. **Draft.** `python3 social/tools/plan_week.py <the Tuesday 8 days ahead>` (a full week for KT to approve). If that week's file already exists, finish it. Refuses to overwrite: if the file exists, read it and finish it instead of replacing it (use `--force` only for a draft no human has touched).
3. **Finish needs_writing posts.**
   - Weekly video: write the script, on-screen lines and caption for the post's `cast` (presenter persona, look, voice and setting from `social/data/cast.json`): the setting goes into the BHuman presenter/scene prompt, the persona shapes the wording. A `new_presenter`: generate the look (generate_presenter), audition voices (find_voice_candidates), pick one that fits the persona, then set the presenter's status to active with its ids in `cast.json` (that voice is fixed for that presenter from then on).
   - Then `plan_render` (free) and put its credit estimate in the hand-off. Never `start_render` before KT's yes for that week, and never beyond `bhuman_monthly_credit_budget` minus this month's `bhuman_credits_spent` (log each render there). No budget or no yes by Monday 23:00: make the free screen-only version (`record-board-footage.js` + `slides_to_video.py`, no presenter, no AI flags).
   - Exhausted hook bank: write two or three new hooks for that series, run them through `check_post.py`, add them to `social/data/hook_bank.json` (the test `test_autonomy.py` checks every bank line).
4. **Render.** `python3 social/tools/render_posts.py social/calendar/<week>.posts.json`, then `node social/tools/shoot.js <output dir>`. Look at every image (Read tool). Overflow or a stranded word means fix and re-render.
5. **Check.** `python3 social/tools/check_post.py social/calendar/<week>.posts.json` must show 0 blocked. Run the review passes in the agency skill and write findings in the week's calendar notes.
6. **Reviewer.** Spawn the `social-reviewer` agent on the week's posts file and images only if KT or a scheduled task asked for it; otherwise run its checklist yourself (`.claude/agents/social-reviewer.md`). Fix every BLOCK it raises.
7. **Calendar page.** `python3 social/tools/build_calendar.py social/calendar/<week>.posts.json`.
8. **Commit and push** to `claude/social-agency` (images must be public before Buffer can fetch them).
9. **Hand to KT** in five lines or fewer: the six hooks, the video's presenter and setting, the BHuman credit estimate, anything new, what needs their yes. In `approve-week` mode, ask for "yes week <date>"; record it in `state.json` `approvals` as `{"week": "<tuesday>", "by": "KT", "on": "<date>", "words": "<their words>"}`. Never record an approval KT did not give.
