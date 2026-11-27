---
name: social-weekly-plan
description: Monday runbook for the Yireh Careers social agency - draft next week's posts (Tue to Mon) from the live board, finish anything marked needs_writing, render, check and hand the week to KT for approval. Use when a scheduled Monday session fires, or when KT says "plan next week".
---

# Weekly plan (Mondays)

Read first: `social/OPERATING-SYSTEM.md`, `social/state.json`, `.claude/skills/social-agency/SKILL.md` (rules), `social/brand-guide.md`.

1. **State.** If `mode` is `hold`, stop and tell KT nothing was planned. Otherwise continue (planning is allowed in every other mode).
2. **Draft.** `python3 social/tools/plan_week.py <next Tuesday>`. Refuses to overwrite: if the file exists, read it and finish it instead of replacing it (use `--force` only for a draft no human has touched).
3. **Finish needs_writing posts.**
   - Weekly video: write the script, on-screen lines and caption by the video recipe in the agency skill. Without a BHuman budget in `state.json`, make the free screen-only version: `record-board-footage.js` + `slides_to_video.py`, no presenter, no AI flags.
   - Exhausted hook bank: write two or three new hooks for that series, run them through `check_post.py`, add them to `social/data/hook_bank.json` (the test `test_autonomy.py` checks every bank line).
4. **Render.** `python3 social/tools/render_posts.py social/calendar/<week>.posts.json`, then `node social/tools/shoot.js <output dir>`. Look at every image (Read tool). Overflow or a stranded word means fix and re-render.
5. **Check.** `python3 social/tools/check_post.py social/calendar/<week>.posts.json` must show 0 blocked. Run the review passes in the agency skill and write findings in the week's calendar notes.
6. **Reviewer.** Spawn the `social-reviewer` agent on the week's posts file and images only if KT or a scheduled task asked for it; otherwise run its checklist yourself (`.claude/agents/social-reviewer.md`). Fix every BLOCK it raises.
7. **Calendar page.** `python3 social/tools/build_calendar.py social/calendar/<week>.posts.json`.
8. **Commit and push** to `claude/social-agency` (images must be public before Buffer can fetch them).
9. **Hand to KT** in five lines or fewer: the six hooks, anything new (a new hook style, a test), what needs their yes. In `approve-week` mode, ask for "yes week <date>"; record it in `state.json` `approvals` as `{"week": "<tuesday>", "by": "KT", "on": "<date>", "words": "<their words>"}`. Never record an approval KT did not give.
