# Social production tools (free; no accounts, no spend)

| Tool | What it does |
|---|---|
| `feed.py` | Reads the LIVE feed. `stats` = today's numbers; `wide` = roles open worldwide or across a region that includes Africa or Asia (newest first, at most 2 per company, skips `social/data/exclude_jobs.json`). |
| `render_posts.py` | Renders image and carousel posts (1080x1350) from a week's `.posts.json` in the site's look; roles are picked live; writes `social/output/<date>/<id>/NN.jpg` + `manifest.json`. Uses `shoot.js` (Playwright). |
| `verify-open.js` | Guardrail 6: opens every featured posting in a real browser; fails on a missing title, closed-role wording, or single-country wording on a Worldwide/region card. Writes the result into the manifest. |
| `record-board-footage.js` | Records 1080x1920 frames of the live board for videos: types "Worldwide roles only", hides cards until filtered, scans the last view for country names (exit 1 if any). |
| `check_post.py` | The guardrail checker (CLAUDE.md copy rules, no country, dated numbers, spelling, AI label, free-claim once, hashtags, no service in jobs posts). `--mode schedule` is strict. Tests: `python3 -m pytest social/tools/tests -q`. |
| `build_calendar.py` | Writes the readable `social/calendar/<week>.md` from `<week>.posts.json`, with each post's check result and the preview's roles. |

Day-of sequence (also at the end of each calendar file): `feed.py stats` → update numbers → `render_posts.py --only <id>` → `verify-open.js <manifest>` → copy checked roles into `featured_jobs` → `check_post.py --mode schedule` → look at every slide → schedule.

Video assembly (ffmpeg, free): `ffmpeg -framerate <fps from meta.json> -i <out>/frames/f%05d.jpg -vf "scale=1080:1920,format=yuv420p" -c:v libx264 board.mp4`, then cut presenter + board + presenter and burn captions with an `.ass` file as in `drafts/marketing/video/video1/README.md`.

## Autonomy (27 Nov 2026)
- `plan_week.py <tuesday>`: drafts a week from the feed, `data/hook_bank.json` and `data/tip_sets.json`.
- `buffer_payloads.py <posts.json> --date <day>`: the publishing gate; prints Buffer `create_post` calls or refuses with the reason. `--record id:platform:buffer_id` logs a scheduled post.
- `slides_to_video.py <dir>`: slides to a 1080x1920 MP4 (ffmpeg, silent track).
- `social_metrics.py --days 7`: board visits by platform (GoatCounter; needs its credential).
Map of the whole system: `social/OPERATING-SYSTEM.md`.
