---
name: bhuman-presenter-director
description: Governs every Yireh Careers video made with BHuman (Speakeasy) - choosing the presenter and voice, writing the spoken script for the ear, the delivery direction sheet, voice tuning, render planning, credit rules, objective voice QC with voice_qc.py, compositing with board footage and captions, and final inspection. Use whenever a presenter video is planned, voiced, rendered, checked or re-made.
---

> **Connection (27 Nov 2026):** BHuman is a claude.ai connector named `bhuman_ai` (tools `mcp__bhuman_ai__*`), so every new session has it. Older notes say `mcp__bhuman-speakeasy__*`: same tools, use whichever prefix ToolSearch returns.

# BHuman presenter director (Yireh Careers)

BHuman is not a text-to-video button. A convincing presenter comes from deliberate choices about face, voice, pace, emotion, pauses, setting and framing, and from checking the result instead of trusting that a render finished. Copy rules come from `social-media-humanizer` and `CLAUDE.md`; this skill covers the production.

## 1. What the connected tools can and cannot do (checked 27 Nov 2026)
Read the docs before relying on anything (bhuman.ai/docs: speakeasy, projects-and-presenters, script-and-voice, rendering-and-sharing, subtitles). Facts from the docs and `get_capabilities`:
| Need | Tool | Cost | Notes |
|---|---|---|---|
| Project | `create_project` | free | Name it `<post id> <short title>` |
| Presenter | `list_presenters`, `generate_presenter` (from a description), `edit_presenter` (natural-language change to an image) | not stated by the tool; check the balance | Docs: one clear face, no extreme angles, believable environment; describe age, look, clothes, expression, environment. Generation can exceed the 60 s client timeout but still complete: check `list_presenters` before retrying (it created duplicates once). |
| Voice | `list_voices` (saved), `find_voice_candidates` (up to 3 auditions) | catalog playback free; **voice design 1 credit per second** | **Check the result's `source` field.** On 27 Nov a call with `source: "catalog"` came back `"design"` and was charged. If you only want free auditions, use the catalog voices' `preview_url` files and saved voices. |
| Narration | `create_narration` (script ≥ 100 characters; delivery preset natural / warmer / energetic / deliberate; speed 0.7-1.2; stability; similarity_boost; style; speaker_boost; natural-language `feedback`) | **1 credit per second, charged immediately, no confirmation** | So a narration is a spend: only inside an approved week and budget. |
| Script help | `write_script` (`improve_delivery` keeps wording) | free | Never let it change approved wording. |
| Plan | `plan_render` (quality standard 480p / hd, aspect 9:16, duration, B-roll %) | free | Gives the credit estimate KT must see. |
| Render | `start_render` | video credits (a 30 s standard render was estimated at 30 Speakeasy seconds = 7.5 shared credits; 1 Speakeasy minute = 15 credits, bhuman.ai/pricing) | **Only after KT explicitly confirms the plan's estimate** (BHuman's rule and ours). Unique `idempotency_key`. Poll `get_render`. |
| Layouts | `list_visual_presets` (16), `select_visual_preset`, `plan_visuals`, `generate_visual_scene`, `prepare_visual_upload` | planning free | Presets put captions and titles in BHuman's own colours (pink, yellow); cutout presets need a local matte helper. **Our default is to render the plain presenter and composite ourselves** (section 7), so captions and footage match the brand. |
| Subtitles | BHuman subtitles are an AI Studio campaign feature from the template transcript | — | Not used for Speakeasy videos; we burn our own captions from word timings. |
| Download | the finished `video_url` is a plain MP4 | — | Renders on the Ultimate plan still carry a small "BHuman" mark at 91-92% of the frame height (`output_watermarked.mp4`, checked 27 Nov). **KT, 27 Nov: crop out all watermarks**: `compose_video.py` does it by default (`--crop-bottom 0.11`). Always check a frame after compositing. |
| Publishing | BHuman's own social sharing exists in the app | — | Not used: publishing goes through Buffer and the gate only. |

## 2. The cast (`social/data/cast.json`, `social/PRESENTER_PROFILES.md`)
A small recurring cast. Each presenter always uses **their own** voice: a face and voice that match keep trust. The setting, outfit and framing change between videos; no presenter-setting pair repeats within 8 weeks (`plan_week.py` picks). KT decided on 27 Nov to keep the current cast; presenter look is not changed by default (evidence in `cast.json` decisions).
Pick the presenter by the job the video does, not by rotation alone:
- **Amara** (warm, a little wry): relatable frustration, reassurance, "we've all been there".
- **Daniel** (practical, direct): demonstrations, how-to, safety and scams.
- **Zee** (bright, curious): surprising numbers, discoveries, light humour.
Change the presenter only when it improves the piece. New presenters: describe face, age, clothes, expression and a believable home or work setting; look at the image (download and Read it) before saving it to the cast.

## 3. Write for the ear (after the humanizer has done its work)
- Sentences you can say in one breath. 8-16 words is typical; vary it.
- Numbers as words, the way they should be said ("twenty-seven", "nearly two thousand"). No symbols (%, /, &, $) in the narration script.
- The brand is written **"Yai-ray Careers"** in narration so it's said YYE-ray; "Yireh" on screen.
- Punctuation shapes delivery but does not guarantee it: an ellipsis or a full stop gives a pause; a question mark lifts the ending; a dash gives a short break. Preview and measure; don't assume.
- **Stage directions never go in the spoken script.** BHuman's narration takes no separate direction field per line; direction goes into `delivery.feedback` (one natural-language note for the whole take) and the tuning values.
- Length: 15-35 s for most social videos (about 40-90 words at 150-165 wpm). Say what's needed and stop.

## 4. The direction sheet (required for every spoken script)
Write it in the video brief (`social/video-briefs/<id>.md`) as a table, one row per line:
| Line | Emotion | Energy (1-5) | Pace | Stress these words | Pauses | Ending | Note |
- **Emotion** from the humanizer's 12 tones.
- **Pace:** slow / natural / brisk (and the target wpm range).
- **Stress:** the one or two words that carry the meaning ("*where* you could apply").
- **Pauses:** short (about 0.3 s) / long (about 0.8-1.2 s, only for a reveal).
- **Ending:** rising (a real question), falling (a statement, a fact), neutral.
- **Note:** amused, concerned, surprised, thoughtful, confident, reassuring; and what *not* to do ("don't shout", "don't overdramatise").
Then translate it into the take's settings:
- `delivery.preset` from the dominant tone (humanizer table);
- `speed` (0.92-1.05 normally);
- `stability` (0.45 for more expressive; 0.6 for composed, serious);
- `style` (0-0.4; higher = more character, more risk of odd emphasis);
- `feedback`: one plain paragraph summarising the sheet ("Conversational and warm, like telling a friend something you just noticed. Small pause before 'US residents only', said with mild disbelief…").

## 5. Credits and approval
- Narration and voice design charge immediately; renders charge after `start_render`. Every spend needs: the week (or the piece) approved by KT, KT's yes on the `plan_render` estimate, and the month within `state.json` `bhuman_monthly_credit_budget` (200 of the Ultimate plan's 500). Log every spend in `state.json` `bhuman_credits_spent` (date, what, credits).
- Free work, any time: scripts, direction sheets, presenter choice, catalog preview files, `plan_render`, B-roll recording, compositing tests.
- Ask KT once per batch, with the numbers: "Narration about N s (N credits) + render (N credits) for videos X, Y, Z: yes?"

## 6. Voice QC (Claude can't hear; measure what can be measured)
After every narration or render: `python3 social/tools/voice_qc.py <audio or mp4> --script <script> --json <brief dir>/qc.json`
| Check | Pass |
|---|---|
| Transcript vs script | ≥ 95% match; every difference explained (number formats are normalised; "Yai-ray" is heard as "Yairay") |
| Pace | 140-175 wpm (our working range for social talking-head delivery, not a cited standard) |
| Pauses | only where the direction sheet asks; nothing over 1.2 s except a planned reveal |
| Loudness | measured; the composite is normalised to about -14 LUFS (the level the main short-video apps play at; working target) |
| Lip-sync and face | look at frames at 0.5 s, the middle and the end (`ffmpeg -ss <t> -frames:v 1`): mouth moving with speech, eyes natural, expression not contradicting the line (smiling through bad news) |
What the measurement **cannot** judge: warmth, sincerity, odd emphasis, a smile in the voice, whether it sounds like a real person. Say so in the brief, and in the hand-off ask KT to listen to the first 5 seconds and the ending. If the measured checks fail, regenerate with adjusted feedback or settings, or change voice. **Never approve a video because the render completed.**

## 7. Composite (our default) with `social/tools/compose_video.py`
Render the presenter full-frame 9:16 at standard quality. Then composite locally (free):
1. **Captions** burned from the word timings (Inter ExtraBold, white on a navy box, one or two short lines, keywords in brand blue), placed inside the safe zone (y 1150-1450 of 1920, clear of the right-hand buttons and the bottom caption area; `social/PLATFORM_GUIDELINES.md`).
2. **B-roll and screen recordings** cut in full-screen where seeing matters more than the presenter (the board, a posting's location line), with the voice continuing over them. Record real screens only (`record-board-footage.js`; never show a country name: KT, 26 Nov).
3. **Opening frame:** the first frame must already show the subject (the presenter mid-thought, or the screen) **with a six-word-or-fewer hook on screen from frame 0** (`--hook`). No logo sting. Why: Video 1 opened without one and averaged 1.3 s of watch time on TikTok (review 27 Nov).
4. **Ending:** a short, natural close; the last frame can hold the board URL for one second.
5. **Audio:** loudness normalised (about -14 LUFS). Music only if it fits the emotion and stays under the voice; on business accounts only the platforms' commercial music libraries, added inside the app at posting, never baked in.
6. **No visible "AI presenter" badge, tool watermark or tag** in the video, caption or design (KT, 27 Nov: no AI badges; crop out all watermarks). Disclosure is done with each platform's own AI label: `isAiGenerated` on TikTok and Instagram (the gate sets it), and on Facebook KT ticks "AI info" or the screen-only version goes there. Never switch a required platform label off.

## 8. Final inspection before a video can be scheduled
- Frames at 0, 1, 3 s and every scene change: subject visible at once, text readable, nothing under the app buttons, no country shown, no hiring-system name.
- `voice_qc.py` passes (section 6); KT has heard it, or the brief says it's unheard.
- The humanizer's final check (section 11) passes for the script, on-screen text and caption.
- `check_post.py` passes; the gate does the rest.
Write the results in the brief's QC section. If anything important fails, re-make it. Better a free screen-only video than a presenter who sounds wrong.
