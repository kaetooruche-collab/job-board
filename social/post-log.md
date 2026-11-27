# Post log: how to fill `post-log.csv`

One row per post per platform, written when the post goes out and updated at 24 h and 7 days.
- From **Buffer** (`get_post` with metrics, daily refresh, 31 days on the free plan): impressions or reach, reactions, comments; shares and saves where the network supplies them.
- From **TikTok Studio / Instagram Insights** (KT, about 2 minutes a week, or "n/a"): 2- or 3-second views, average watch time, completion, profile visits. Buffer's API does not return these (checked 27 Nov 2026).
- From **GoatCounter** (API connected): bio-link visits by `utm_source`, free-check page visits, WhatsApp clicks. The bio link is one per platform, so these attribute to a platform and day, not to one post; say so in reports.
- `metrics_source` names where each row's numbers came from; never leave a guessed number. Blank means not measured.
