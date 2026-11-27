# BHuman production workflow (step by step, 27 Nov 2026)

The rules and reasons are in `.claude/skills/bhuman-presenter-director/SKILL.md`. This is the order of operations with the actual MCP tools. **Free** steps can run any time; **spend** steps need an approved week, KT's yes on the estimate, and budget (`state.json`).

| # | Step | Tool / command | Cost |
|---|---|---|---|
| 1 | Brief, script, on-screen text, caption, direction sheet | `social/video-briefs/<id>.md` (template: `video-briefs/TEMPLATE.md`) | free |
| 2 | Humanizer final check + `check_post.py` | skills + checker | free |
| 3 | Pick presenter and setting | `PRESENTER_PROFILES.md`, `cast.json` | free |
| 4 | Re-dress the presenter for the setting (optional) | `edit_presenter` (image_url, changes, save) | not stated; check balance |
| 5 | Create the project | `create_project` name `<id> <title>` | free |
| 6 | Voice: saved voice, or catalog preview files | `list_voices`; catalog `preview_url` downloads | free |
| 7 | B-roll: board screen recordings | `node social/tools/record-board-footage.js --out <dir> --seconds N`, then ffmpeg to MP4 | free |
| 8 | Ask KT (one message per batch): narration seconds + render credits | — | — |
| 9 | Narration with the direction settings | `create_narration` (project_id, script, voice, delivery {preset, speed, stability, style, feedback}, presenter_image_url) | **1 credit per second** |
| 10 | Voice QC | `python3 social/tools/voice_qc.py <narration.mp3> --script <script.txt>` | free |
| 11 | Re-take if QC fails (adjust feedback, speed) | `create_narration` again | spend |
| 12 | Plan the render (9:16, standard, duration) | `plan_render` | free |
| 13 | Render (after KT's yes on this estimate) | `start_render` (plan_id, confirm_credit_charge true, unique idempotency_key) | **video credits** |
| 14 | Wait and download | `get_render` until `video_url`; `curl -L -o presenter.mp4 <url>` | free |
| 15 | Composite: captions, b-roll, loudness | `python3 social/tools/compose_video.py --presenter presenter.mp4 --out social/output/<date>/<id>/video.mp4 --broll S:E:board.mp4 --emph … --hook "…"` | free |
| 16 | Final inspection | frames at 0, 1, 3 s and each cut; `voice_qc.py` on the final MP4; check watermark | free |
| 17 | Log credits and QC in the brief and `state.json` | — | — |
| 18 | Schedule through the gate (AI label on TikTok and Instagram; Facebook needs KT's "AI info" tick or the screen-only cut) | `social-daily-publish` | — |

## Known behaviour (observed)
- `generate_presenter` can take over 60 s and time out on our side while still completing: run `list_presenters` before retrying (one duplicate was created this way).
- `find_voice_candidates` with `source: "catalog"` returned designed voices once (charged). Check `source` in the result.
- Renders still carry a small "BHuman" mark at 91-92% of the frame height on the Ultimate plan (V1, 27 Nov). KT's rule (27 Nov): crop out all watermarks. `compose_video.py` crops the bottom 11% of the presenter frame by default; check a frame after every composite.
- Free catalog previews read the voice's own sample sentence, so they show the voice's quality but not our script.
