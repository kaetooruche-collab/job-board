# V3: "Three messages a real employer won't send you"
Status: **built 27 Nov, scheduled for Mon 7 Dec (w49-p6)** · Presenter: Daniel + three message cards · Length target: 30-35 s · Platforms: TikTok, Instagram Reel, Facebook (screen-only cut unless KT ticks "AI info")

1. **Objective:** awareness and trust → sends and saves. Goal metric: sends per reach (Instagram's main signal for reaching non-followers) and saves.
2. **Audience:** everyone job hunting online, especially people outside the US targeted by "remote job" scams.
3. **Audience insight:** "if someone wants to interview you through text on telegram or whatsapp, it's almost always fake" (r/globalwork); "Legitimate companies cover recruitment costs, not candidates" (r/buhaydigital); fear that the helper is the scammer (Nairaland) (`AUDIENCE_RESEARCH.md`).
4. **Concept:** different from V1 and V2: not about the board at all. Three recognisable messages, each read out then plainly explained. Useful even to someone who never visits us, which is what earns the send. The viewer remembers: *pay to start, a cheque to send back, a text-only interview: stop.*
5. **Emotion:** serious and assertive; calm authority. No jokes, no fear-mongering.
6. **Opening visual:** a phone-style message card, "There's a small fee to start your training.", with Daniel's voice already speaking.
7. **Opening spoken hook:** "Three messages a real employer won't send you."
8. **Spoken script** (88 words, about 33 s at 160 wpm):
   > Three messages a real employer won't send you.
   > One. "There's a small fee to start your training." If someone asks you to pay to get a job, it's a scam.
   > Two. "Here's a cheque. Deposit it, keep your pay, and send the rest back." The cheque bounces. The money you sent doesn't come back.
   > Three. "We'll do the whole interview by chat message." No call, no company email. People who've been scammed describe this one again and again.
   > If you get one of these, stop. Find the job on the company's own careers page.
   > And send this to someone who's job hunting.
9. **Presenter:** Daniel: practical, composed, credible on safety. Study setting (his default, first use).
10. **Voice:** Daniel's catalog voice **Joe** (`cdUhV8G3eltjOJdoi4lk`, neutral accent, steady); fixed for Daniel from this video on. `preset: deliberate`, `speed: 0.97`, `stability: 0.6`, `style: 0.15`. Feedback: "Calm, serious, like a sensible colleague warning a friend. Read each quoted message in a slightly flatter, 'reading it out' voice, then explain in your own natural voice. Firm, falling endings on 'it's a scam' and 'doesn't come back'. A short pause before each number. No drama, no raised voice. The last line is warmer and lighter."
11. **Direction sheet:**
| Line | Emotion | Energy | Pace | Stress | Pauses | Ending | Note |
|---|---|---|---|---|---|---|---|
| Three messages a real employer won't send you. | assertive | 3 | natural | *won't* | — | falling | direct to camera |
| One. "There's a small fee…" | neutral reading | 2 | natural | — | short after "One" | neutral | quoting |
| If someone asks you to pay to get a job, it's a scam. | serious | 3 | measured | *pay*, *scam* | — | falling, firm | — |
| Two. "Here's a cheque…" | neutral reading | 2 | natural | — | short after "Two" | neutral | quoting |
| The cheque bounces. The money you sent doesn't come back. | serious | 3 | slower | *bounces*, *doesn't* | short between | falling | let it land |
| Three. "We'll do the whole interview by chat message." | neutral reading | 2 | natural | *whole* | short after "Three" | neutral | quoting |
| No call, no company email. People who've been scammed describe this one again and again. | concerned | 3 | natural | *again and again* | short after "email" | falling | — |
| If you get one of these, stop. Find the job on the company's own careers page. | reassuring, firm | 3 | measured | *stop*, *own* | long after "stop" | falling | the takeaway |
| And send this to someone who's job hunting. | warm | 2 | natural | — | — | falling | lighter |
12. **Scenes:**
| Time | Picture | On screen | Sound |
|---|---|---|---|
| 0-3 s | Message card 1 (amber accent), "Example" label | — | voice |
| 3-9 s | Daniel | captions | voice |
| 9-12 s | Message card 2 | — | voice |
| 12-17 s | Daniel | captions | voice |
| 17-20 s | Message card 3 | — | voice |
| 20-33 s | Daniel | captions; closing frame "We never charge you to apply." + URL | voice |
13. **On-screen text:** three message cards ("Example message" kicker); closing line "We never charge you to apply." (the one free claim, on screen only).
14. **B-roll:** three 1080x1920 cards rendered by `render_posts.py` (safety theme: amber accent on light), turned into clips with `slides_to_video.py`.
15. **Music:** none.
16. **Subtitles:** emphasis: pay, scam, bounces, stop.
17. **Ending/CTA:** "send this to someone who's job hunting" (sends). No board link in the spoken script; the caption carries the bio-link line.
18. **Captions:**
   - TikTok: "If a job message looks like one of these, stop. #jobscams #remotejobs #jobsearch #careertips"
   - Instagram: "Three messages a real employer won't send you.\n\n1. A fee to start training or get the job.\n2. A cheque to deposit and send part back.\n3. An interview done entirely by chat message.\n\nIf you get one, stop and find the job on the company's own careers page. Save this, or send it to a friend who's job hunting.\n\n#jobscams #remotejobs #jobsearch #careertips"
   - Facebook: as Instagram; add "Our board lists jobs from companies' own hiring pages, and we never charge you to apply:" with the tagged link (the free claim moves into the caption there, so remove it from the closing frame for the Facebook cut).
19. **Hashtags:** the scam and safety set.
20. **QC:** humanizer passed (serious tone kept; no fear-mongering; one CTA). `check_post`: one free claim per platform; no country; WhatsApp and Telegram are not named (said as "chat message"). voice_qc on the final video (27 Nov): 102 words in 39.2 s = 156 wpm, -14.3 LUFS, one 1.4 s pause after 'back.' (the reveal before message 3, kept). Frames: watermark cropped, hook from frame 0, three message cards, end card. Captions use the script's words. KT listened: not yet. Credits: logged in state.json.
**Evidence and claims:** messages 1 and 2: FTC Consumer Advice, "Job Scams" (consumer.ftc.gov/articles/job-scams, updated 13 Aug 2026, read 27 Nov): "If someone asks you to pay to get a job, that's a scam." and "No honest potential employer will ever send you a check to deposit and then tell you to send on part of the money… The check will bounce." Message 3: job seekers' reports (Reddit r/globalwork, r/recruitinghell; `AUDIENCE_RESEARCH.md`), so the script says "people who've been scammed describe this", not "always a scam". The message texts are illustrative examples, labelled "Example message" on screen.
