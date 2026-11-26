# Platform specs, safe zones, caption limits and AI-label rules (26 Nov 2026)

**Labels:** **[Established]** = from the platform itself; **[Reported]** = consistent secondary sources quoting the platform; **[Conflict]** = sources disagree; **[Unverified]** = not checked this pass.
Re-check every three months; platforms change these often.

## 1. Sizes and lengths
| | TikTok | Instagram | Facebook |
|---|---|---|---|
| Video | 1080x1920 (9:16) | Reels 1080x1920; up to 3 minutes [Reported] | Reels 1080x1920 [Reported] |
| Images | Photo mode: up to 35 images in one post [Reported, TikTok Content Posting API docs via several guides] | Feed and carousel: 1080x1350 (4:5), the safest choice; the profile grid became 3:4 in 2025 and also takes 1080x1440 [Reported] | 1080x1350 works in feed [Reported] |
| Carousel length | 35 | 20 slides [Reported] | – |
| Caption | 2,200 characters on a video [Reported, one guide]; photo posts via the API: title 90, description 4,000 [Reported] — **[Conflict]**: we keep every caption under 2,200 | 2,200 characters [Reported, long-standing] | very long; keep the first line under ~125 characters, feeds cut it [Reported] |
| Hashtags | no hard cap found; we use 3–5 | **5 per post or Reel** since 18 Dec 2025 (Instagram's @creators: "Starting today, Instagram will allow up to 5 hashtags in a reel or post"); generic tags like #reels or #explore "don't help" [Reported, five sources quoting the announcement] | we use 3–5 |

**Our defaults:** images and carousels 1080x1350; videos 1080x1920, 20–35 s; captions under 1,000 characters; 3–5 specific hashtags.

Sources: <https://creatorflow.so/blog/how-many-hashtags-instagram/>, <https://swapbiswas.com/blog/instagram-hashtag-limit/>, <https://www.krumzi.com/blog/instagram-carousel-size-guide>, <https://recurpost.com/instagram-scheduler/instagram-post-size-guide/>, <https://adaptlypost.com/blog/tiktok-photo-mode>, <https://www.mymarky.ai/social-media-image-and-video-sizes>.

## 2. Safe zones on a 1080x1920 video (keep text and faces inside)
| Keep clear | TikTok (from TikTok's safe-zone file, scaled from 720x1280) | Instagram/Facebook Reels (Meta's ad guidance) | Facebook's organic Reels tip |
|---|---|---|---|
| Top | 240 px | 269 px (14%) | 250 px |
| Bottom | 660 px | 672 px (35%) | 420 px |
| Sides | 120 px each; right side 300 px from 840 px down (the buttons) | 65 px (6%) | "margins" |

[Reported] <https://clear-cortex.com/insights/tiktok-safe-zones> (checked 2 Nov 2026), <https://taletok.io/blog/instagram-reels-dimensions>, <https://www.facebook.com/fb-answers/reels-text-safe-zone/>.
**Our rule (fits all three):** text between y = 270 and y = 1250, x = 120 to 780 when it sits low on the right; nothing important in the bottom 670 px. Video 1's captions sit at 720 px from the bottom (`MarginV` 720), which fits.
For 1080x1350 images: keep text 84 px in from every edge (the renderer does). The 3:4 profile grid shows a 4:5 image about 1012 px wide, trimming about 34 px from each side [Established, arithmetic], so the 84 px margin keeps text clear.

## 3. AI labels
| Platform | Rule | Strength |
|---|---|---|
| TikTok | Realistic AI-generated people, scenes or voices must carry the AI-generated label; voice clones count. | [Established] TikTok support page, read 25-26 Nov: <https://support.tiktok.com/en/using-tiktok/creating-videos/ai-generated-content> |
| Instagram, Facebook (Meta) | Label content with photorealistic video or realistic-sounding audio that was digitally made or altered, including with AI; Meta's own example includes a Reel narrated with a realistic AI voiceover. Shown as "AI info". You switch it on before sharing; Meta also adds it when it detects industry signals. | [Established] for the "AI info" label (Meta newsroom, updated 1 Jul 2024: <https://about.fb.com/news/2024/04/metas-approach-to-labeling-ai-generated-content-and-manipulated-media/>); [Reported] for the exact help-centre wording (<https://www.zolyp.com/blog/ai-content-labels-on-social-media>) |

**Our rule:** any post with the AI presenter or the AI voice gets the label on every platform, plus "AI-generated presenter" on screen (as in Video 1). Screen recordings, text slides and role cards are not AI-generated and carry no label. `check_post.py` blocks a post with `ai_presenter` or `ai_voice` and no `ai_label`.

## 4. Not checked this pass
- TikTok and Facebook maximum video lengths [Unverified]; irrelevant at 20–35 s.
- The follower thresholds for TikTok Studio and Instagram Insights audience data [Unverified].
- Postiz: how it sets the AI label per platform (check in `integrations:settings` when connected; if it cannot, KT ticks it in the app after posting, which defeats autopilot for presenter videos).
