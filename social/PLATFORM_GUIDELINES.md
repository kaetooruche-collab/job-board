# Platform guidelines (27 Nov 2026)

Specs and safe zones come from `research/2026-11-26-platform-specs.md`; ranking signals and the format plan from `research/2026-11-27-formats-and-colour.md` (KT approved the format plan on 27 Nov). Re-check official guidance before relying on a number older than three months.
Labels: [Established] official or API; [Reported] vendor or press quoting the platform; [Hypothesis] ours.

## Rules for every platform
- **Video:** 9:16, 1080x1920, H.264, AAC, about -14 LUFS. The first frame shows the subject, with no logo sting. Burned-in captions (most people watch muted [Reported]). Text inside the safe zone: top 270 px and bottom 420 px clear, right 150 px clear of the buttons.
- **Images:** carousels 1080x1350 (4:5); Stories 1080x1920.
- **Adapt each post to its platform; don't paste the same thing everywhere.** The hook line, caption, CTA, hashtags and cover change per platform. The media can stay the same.
- **AI disclosure:**
  - Each platform's own label is switched on for presenter or AI-voice videos: TikTok and Instagram via Buffer `isAiGenerated`; Facebook "AI info" ticked by KT, or the screen-only cut goes there instead.
  - There is no visible AI badge in the video, caption or design (KT, 27 Nov).
  - TikTok and Meta both require labelling realistic AI content [Established, platform rules]. Never switch the label off.
- **Music:** only from the platform's commercial library, added in the app (business accounts can't use the general music catalogue [Reported]). Never baked into our MP4 unless royalty-free with terms checked. Music must never fight the voice.

## TikTok
- **What it rewards** [Reported, TikTok's own advice: the point in the first 3 seconds]: watching to the end and rewatching. A small test audience first, then wider.
- **Formats:** video (15-45 s for us to start) and photo carousels with sound. No Stories through Buffer.
- **Caption:** a short first line that adds to the video (TikTok search reads captions and on-screen text, so use the words people type: "remote jobs open worldwide", "work from anywhere jobs"). 3-5 tags.
- **Cover:** the frame with the headline, six words or fewer.
- **CTA:** the link in bio (TikTok links need a business link in bio).
- **Tags:** #remotejobs #jobsearch #remotework plus a topic tag (#cvtips, #jobscams, #careertok).

## Instagram
- **What it rewards** [Reported, Mosseri, Jan 2025 and Oct 2026]: watch time, likes and sends; sends reach non-followers. Carousels beat single photos.
- **Formats:** Reels, carousels, and Stories with a link sticker (`metadata.instagram.link`). No single-image posts (format plan).
- **Caption:** first line under ~125 characters. Up to 5 hashtags, the hard limit since Dec 2025; Instagram says generic tags don't help [Reported].
- **Trial Reels:** for hook tests; shown to non-followers first.
- **CTA:** the link in bio, or the Story link sticker on roles days.

## Facebook (Page)
- **What it rewards** [Reported]: organic Page reach is low; Reels reach non-followers; carousels lead on saves.
- **The one place a post can carry a clickable link:** the gate puts a tagged board link in the caption (`utm_source=facebook&utm_campaign=<post id>`). So far, most social visits to the board came from Facebook (9 of 11, 20-27 Nov).
- **Caption:** can be a little longer and more explanatory. 0-3 tags.
- **AI label:** Buffer can't set it; KT ticks "AI info", or the screen-only version goes to Facebook.

## YouTube Shorts (not connected; ready when it is)
- **Same vertical files.**
- **Title:** under 60 characters, written for search.
- **Description:** two lines plus the board link (YouTube descriptions are clickable).
- **Altered or synthetic content:** YouTube asks creators to disclose realistic altered or synthetic content in YouTube Studio [Reported; re-check the current help page before the first upload].
- **Testing:** YouTube judges its own thumbnail tests on watch time, not clicks [Reported].

## LinkedIn (not connected; ready when it is)
- **Audience:** experienced professionals; the services' best audience [Hypothesis].
- **Formats:** document (PDF) carousels and native video; vendor studies report documents get the most dwell time and external links lower reach [Reported, Hootsuite/vendor 2026].
- **Link:** put it in the first comment rather than the post (vendor-reported reach effect; test it).
- **Tone:** professional, still human; first-person team voice ("we"), no founder name (KT's rule: the name and photo appear only on the services page).

## Posting times
- Start at 15:00 UTC, no Sunday; Tuesday is the weekly video.
- Facebook is the first platform to test a different time.
- Decisions come from our own data after week 3 (`research/2026-11-26-posting-times.md`).
