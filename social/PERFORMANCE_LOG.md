# Performance log (how we learn)

The raw data is `social/post-log.csv`: one row per post per platform. The Friday review fills it (`social-weekly-review`) from Buffer (impressions, reactions, comments), the platform apps (watch time, saves and sends, which KT pastes in), and GoatCounter (board visits by `utm_source` and campaign, `tools/social_metrics.py`). Weekly write-ups go in `social/reviews/<date>.md`; this page keeps the running lessons.

## How to read results
- Judge each post on **its own goal metric** (the `funnel` and `goal_metric` fields), not on views alone. High views with no saves, sends or visits is reach, not interest.
- **One variable per test** (the `variable` field). No winner under about 1,000 views per variant (our working rule).
- Label every lesson **established** (seen in our data, repeated), **hypothesis** (seen once) or **assumption** (not yet tested).
- Traffic is not conversion. Board visits are judged weekly; free-check requests and signups monthly.

## Baseline (before scheduled posting)
| Date | What | Number | Source |
|---|---|---|---|
| 26 Nov 2026 | Video 1 (Amara, "halfway through an application…") on TikTok | 84 views (26 Nov); 425 views, avg watch 1.3 s of 26 s (27 Nov) | KT; Buffer metrics |
| 26 Nov 2026 | Video 1 on Instagram / Facebook | reach 8, avg watch 6.3 s / reach 0 | Buffer metrics |
| 20-27 Nov 2026 | Board visits from social | Facebook 9, Instagram 2, TikTok 0 | GoatCounter, 27 Nov |
| 27 Nov 2026 | Video 1 delivery | 195 wpm (too fast), watermark present | `voice_qc.py`, frame check |

## Running lessons
| Date | Lesson | Status | Evidence |
|---|---|---|---|
| 27 Nov | Voice pace needs directing: the default delivery ran at 195 wpm | hypothesis (one video) | voice_qc on Video 1 |
| 27 Nov | Facebook visits (9) came from somewhere other than the Page posts (reach 0-1, 0 clicks): likely group shares | hypothesis | Buffer + GoatCounter 20-27 Nov |
| 27 Nov | Video 1 lost most TikTok viewers in the first 1-2 s (avg 1.3 s): the opening must show the point in frame 0 | hypothesis (one video) | Buffer avg watch time; review 2026-11-27 |

## Tests queue (one at a time)
1. Hook type: a specific fact vs a recognisable situation (Instagram Trial Reels).
2. Presenter-led vs screen-led video, same message.
3. Length: about 15 s vs about 30 s.
4. Caption opening: a question vs a statement.
5. CTA: see the board vs filter by where you live vs save this.
