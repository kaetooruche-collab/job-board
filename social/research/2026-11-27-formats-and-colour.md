# Formats per platform, and colour (27 Nov 2026)

KT's questions (27 Nov): every post is the same navy, so is that the best we can do? Have we decided which content types (static, carousel, Reel, Story) go on which platform and when, given the platforms rank differently? Or do we wait for data?
**Short answer:** No, the formats were not decided per platform. Phase 0 sent the same file to all three. Some things can't wait for data: how each platform ranks content is stated by the platforms or measured on millions of posts. Data decides the ratios, the times and the winners, not the basic fit.
**Labels:** [Established] = from the platform, its API, or a peer-reviewed study we read the summary of; [Reported] = vendor studies or press quoting platform staff (large samples, but their customers and their definitions); [Conflict] = sources disagree; [Hypothesis] = ours.

## 1. What each platform rewards
### Instagram
- **The three signals that matter most are watch time, likes and sends.** Likes count more with followers; sends count more for reaching non-followers. Mosseri, January 2025, repeated in 2026. [Reported, quoting Mosseri: Social Media Today; Buffer; ZoomSphere 30 Oct 2026]
- **"Carousels do better than single photos," and you can grow without Reels.** Mosseri, Stories Q&A, 23 Oct 2026. [Reported, quoted with a still of the video by ZoomSphere]
- **Reels reach further, carousels engage more.** Buffer, 4 million+ posts: Reels get 36% more reach than carousels; carousels 12% more engagement. [Reported]
  - Dash Social says carousels average 24% *more views* than Reels. [Conflict]
  - Socialinsider: carousels 0.55% engagement rate, ahead of Reels. [Reported]
- **Stories reach followers, not new people;** they deepen relationships. [Reported, Buffer's surface table]
- **A Story can carry a clickable link sticker.** That's the only clickable link on Instagram besides the bio, and Buffer can schedule it (`metadata.instagram.link`). [Established, Buffer API schema, 27 Nov]

### TikTok
- **Every video is shown to a small test audience first, then widened if people watch.** Completion and rewatch weigh most; follower count matters little. [Reported, vendor summaries; TikTok's own guidance is to put the point in the first 3 seconds, Established earlier]
- **Photo carousels exist:** photo mode, up to 35 images. [Reported] One source claims +81% engagement for carousels over single images. [Reported, weak]
- **No Stories through Buffer.** The TikTok fields in Buffer's API have no story type. [Established, 27 Nov]

### Facebook (Page)
- **Organic Page reach is low; Reels are the main way to reach non-followers.** [Reported, several vendor guides; quality varies]
- **Reels drive the most comments and shares; carousels lead on saves.** Socialinsider Facebook benchmarks 2026. [Reported]
- **Facebook posts can carry a clickable link** (Buffer `linkAttachment`). So Facebook is the one platform where we can tag each post's link separately and see clicks per post. [Established, Buffer API schema]

## 2. Colour
- **More colour variety inside an image draws more attention and engagement.** Kanuri, Hughes and Hodges, *International Journal of Research in Marketing* (2024), "Standing out from the crowd: When and why color complexity in social media images increases user engagement": eye-tracking plus field data. [Established that the study found this; peer-reviewed; one study]
  - The effect is stronger for larger images and posts later in the day.
  - It is weaker when the caption's tone is negative.
- **What that means for us:** [Hypothesis]
  - Our slides are flat single-colour backgrounds with text, which is low colour complexity. The study measures variety *within* an image.
  - A different background colour per post makes the grid and the feed less samey, but each slide stays simple.
  - The bigger lever is visual variety inside the slide: real screenshots of the board, the role card on a light background, and photos where they're honest.
- **Recognition still needs constant brand cues:** the YC mark, Inter, the card layout and the colours from the site.
  - Taking every series colour from the site's own palette keeps them recognisably ours. [Hypothesis; standard brand-asset reasoning, not tested here]

**Change made (27 Nov):** the renderer now has five themes from the site's own colours, one per series, with text contrast checked by eye and the mark ringed on blue and teal backgrounds.
- **Navy:** roles.
- **Light grey-blue:** tips.
- **Amber:** safety and scams.
- **Bright blue:** numbers and the weekly video's thumbnail.
- **Teal:** the CV service.

## 3. Proposed format plan (for KT's yes; replaces "same file everywhere")
| Slot | TikTok | Instagram | Facebook | Why |
|---|---|---|---|---|
| Tue weekly video | Video | Reel (AI label) | Reel (AI info ticked by KT, or the screen-only version) | Reach to non-followers on all three |
| Wed roles | Photo carousel with sound | Carousel | Carousel + link to the board in the post (per-post link tag) | Carousels engage; FB link gives per-post clicks |
| Thu tip | Photo carousel | Carousel | Carousel | Saves and sends |
| Fri one role | **10–15 s screen video** of the role on the board (free, recorder) | Reel | Reel + link | Replaces the single image: TikTok needs video; Mosseri says carousels beat single photos |
| Sat roles | Photo carousel | Carousel | Carousel + link | As Wednesday |
| Mon tip | Photo carousel | Carousel | Carousel | As Thursday |
| Stories (new, Wed and Sat) | – | Story: slide 1 + link sticker to the board (`utm_source=instagram_story`) | Story | Clickable link, followers only; cheap reuse |

Times: 15:00 UTC for all, as decided 26 Nov. Facebook is the first place to test a different time if its reach lags.

## 4. What waits for data, and what doesn't
| Decided now (platform mechanics) | Decided by our numbers (from week 3) |
|---|---|
| Video for reach, carousels for depth, Stories for followers with a link | The mix: how many videos vs carousels per platform |
| No single-image posts on Instagram | Best day and time per platform |
| Per-post link tags on Facebook and Stories | Which series colour and hook styles win |
| Sends per reach and saves per reach as the main numbers | Whether TikTok photo carousels earn their slot |
