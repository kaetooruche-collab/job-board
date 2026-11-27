# Presenter profiles (from the actual BHuman library, 27 Nov 2026)

Machine-readable version: `social/data/cast.json` (the planner reads it). Images: BHuman saved presenters. Each presenter keeps **one voice** for good. KT decided on 27 Nov to keep this cast (evidence in `cast.json` → decisions).

## Amara: the friend who's been there
- **BHuman presenter:** "Yireh presenter - warm home" (`53bb213d-afdc-4aab-b7bb-a73a2104deb6`). Woman, early 30s, dark wavy hair, navy knit jumper, tidy home office, window light, plant behind. Small natural smile, relaxed, direct to camera. Used in Video 1.
- **Voice:** saved project voice (`03fdb21e-f95b-472b-bf8d-28fb973eb5b6`; ElevenLabs `pPoztmvzd5p26S3MsNrV`), conversational, upbeat, crisp. Says "Yai-ray" correctly (heard as "Yairay" by speech-to-text in Video 1, as intended).
- **Measured:** Video 1 narration ran at **195 wpm**, too fast for second-language viewers. Direct her at speed 0.9-0.93 and a "slower, unhurried" note; target 150-165 wpm.
- **Best for:** relatable frustrations ("remote… but not for you"), reassurance, empathetic CV topics.
- **Tones:** frustrated (mild), empathetic, reassuring, happy. Avoid: assertive lectures, data dumps.
- **Settings to vary:** home office (used 26 Nov, Video 1), kitchen table in the evening, sofa with laptop, balcony daylight. Re-dress via `edit_presenter` ("change the jumper to a cream shirt, evening lamp light") rather than a new face.

## Daniel: the practical colleague
- **BHuman presenter:** "Yireh cast - Daniel (practical)" (`78b7e5ad-aff1-48fc-896a-6e113c4ffcd6`). Man, mid 30s, short dark hair, trimmed beard, charcoal sweater over a white T-shirt, study with bookshelf and lamp. Composed, attentive, slight knowing half-smile. Image inspected 27 Nov: realistic, not stock-like.
- **Voice (to fix on first narration):** catalog **Joe** "Warm, Conversational and Steady" (`cdUhV8G3eltjOJdoi4lk`; neutral accent; free preview measured 162 wpm). Backup: **Chris** "Calm, Friendly, Wise" (`t3w9KdcqUZPgHazmeinf`, slower). Not Craig (strong regional accent) for an international audience.
- **Best for:** demonstrations, step-by-step how-tos, scams and safety, "here's the one thing to check".
- **Tones:** professional, reassuring, serious, assertive. Avoid: jolly.
- **Settings to vary:** study (default), desk with second screen, kitchen counter, co-working corner.

## Zee: the curious one
- **BHuman presenter:** "Yireh cast - Zee (curious)" (`e86c752d-95f9-42b0-ad79-4f9e347b4362`). Woman, mid 20s, curly hair, mustard cardigan, kitchen table, laptop and mug, afternoon light. Raised eyebrows, amused, "you won't guess this" energy, without the clickbait.
- **Voice:** designed audition "Voice option 1" (`vTY0k99cZ1kYJcuV50Xq`, 27 Nov): measured 173 wpm, full test script heard correctly, natural 1.6 s pause before the reveal. Save it on first narration (designed auditions expire after 30 minutes in the session; if expired, re-audition from the saved description, which costs about 10 credits).
- **Best for:** surprising numbers from our own board, discoveries, light myth-busting, relatable humour.
- **Tones:** curious, surprised, jolly, excited. Avoid: scams, rejection, anything sad.
- **Settings to vary:** kitchen (default), café corner, bedroom desk with fairy lights, park bench with phone (vertical, daylight).

## Not used
- "Yireh cast - Zee (curious) v2" (`6edc0aa2-…`): created by a call KT stopped; never used (KT, 27 Nov).
- "Yireh presenter - clean brand" and "Yireh Careers presenter": studio light-blue backdrops; they look like adverts, and real-person settings fit social better [Hypothesis]. Kept for a possible test only.

## Choosing who presents
1. What job does the video do? (frustration → Amara; how-to or safety → Daniel; numbers and discoveries → Zee)
2. Is the emotion in that presenter's range?
3. Has this presenter-setting pair run in the last 8 weeks? (`plan_week.py` checks)
4. Would no presenter be better? A pure screen demo is often clearer (and free).
