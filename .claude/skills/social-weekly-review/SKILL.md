---
name: social-weekly-review
description: Friday runbook for the Yireh Careers social agency - collect the week's numbers (Buffer, GoatCounter by utm_source, platform figures KT pastes), log them, judge each post against its goal metric, and propose next week's one change. Use when a scheduled Friday session fires, or when KT asks "how did the posts do?".
---

# Weekly review (Fridays)

1. **Buffer.** `get_account`, then for each post in `social/post-log.csv` from the last 14 days with a `buffer_post_id`: `get_post` for its status and metrics. Also `get_aggregated_post_metrics` per channel for the last 7 days. Buffer gives reactions, comments and impressions only; watch time and 3-second views are not in its API.
2. **Board visits.** `python3 social/tools/social_metrics.py --days 7`. Exit 1 means GoatCounter is not connected: say "board visits unknown" (never estimate).
3. **Platform figures.** If KT pasted TikTok Studio or Instagram Insights numbers, add them with `metrics_source` = where they came from.
4. **Log.** Fill the metric columns of `social/post-log.csv` (one row per post per platform; `metrics_source` is required). Commit.
5. **Judge against the goal metric of each post** (its `funnel` and `goal_metric`), never on likes alone. Under about 1,000 views per variant, call nothing a winner; write "too early" and keep the test running. Label each statement established, hypothesis or assumption.
6. **One change.** Propose at most one change for next week (a hook style, a time, a format), with the evidence and its tier (`social/research/2026-11-27-question-bank-and-sources.md`). Write it in `social/reviews/<date>.md`; the Monday plan reads the latest review.
7. **Report to KT** in plain words: what went out, the numbers that matter, the one change, and anything that needs them.
