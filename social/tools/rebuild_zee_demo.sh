#!/usr/bin/env bash
# Rebuild Zee's board-demo video (V2 presenter cut) with board footage filmed TODAY, so the cards on screen are live,
# open and say the right "Posted ..." age. Free: no BHuman credits (Zee's render and voice are reused).
#
#   bash social/tools/rebuild_zee_demo.sh <output dir>      e.g. social/output/2026-12-17/w51-p3
#
# Refuses (exit 1) if any card filmed fails the employer-data check or the open check: then the post is skipped.
set -euo pipefail
OUT="${1:?output dir}"
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; cd "$ROOT"
A=social/video-briefs/assets/v2-zee
T="$(mktemp -d)"
mkdir -p "$OUT"
# 13 s: top, typing, filter, first card, then about 3.5 s of slow scroll (only the cards in that window are filmed)
node social/tools/record-board-footage.js --out "$T/foot" --seconds 13 --scroll
FPS=$(python3 -c "import json;print(json.load(open('$T/foot/meta.json'))['fps'])")
ffmpeg -loglevel error -y -framerate "$FPS" -i "$T/foot/frames/f%05d.jpg" -vf "scale=1080:1920,format=yuv420p" -c:v libx264 "$T/board.mp4"
python3 - "$T" "$OUT" <<'EOF'
import json, sys, urllib.request
t, out = sys.argv[1], sys.argv[2]
feed = json.load(urllib.request.urlopen("https://yirehcareers.vercel.app/jobs.json"))
jobs = feed["jobs"] if isinstance(feed, dict) else feed
by = {j["sourceUrl"]: j for j in jobs}
m = json.load(open(f"{t}/foot/meta.json"))
shown = [c for c in m.get("cards_shown", []) if c.get("link")]
missing = [c["link"] for c in shown if c["link"] not in by]
if missing or m.get("countries_visible_at_end"):
    sys.exit(f"REFUSED: filmed cards not in today's feed {missing} or a country on screen")
json.dump({"jobs": [by[c["link"]] for c in shown], "footage": "rebuild_zee_demo.sh"}, open(f"{out}/manifest.json", "w"), indent=2)
print(len(shown), "cards filmed")
EOF
python3 social/tools/verify_source.py "$OUT/manifest.json"
node social/tools/verify-open.js "$OUT/manifest.json"
D=$(python3 -c "import json;print(json.load(open('$T/foot/meta.json'))['marks']['D_card']/1000)")
ffmpeg -loglevel error -y -t 11.3 -i "$T/board.mp4" -an -vf "fps=30,format=yuv420p" -c:v libx264 "$T/board1.mp4"
ffmpeg -loglevel error -y -ss "$D" -i "$T/board.mp4" -frames:v 1 "$T/hold.png"
ffmpeg -loglevel error -y -loop 1 -t 2.4 -i "$T/hold.png" -vf "scale=1080:1920,fps=30,format=yuv420p" -c:v libx264 "$T/hold.mp4"
ffmpeg -loglevel error -y -ss "$D" -t 3.7 -i "$T/board.mp4" -an -vf "setpts=2.35*PTS,fps=30,format=yuv420p" -c:v libx264 "$T/scroll.mp4"
ffmpeg -loglevel error -y -i "$T/hold.mp4" -i "$T/scroll.mp4" -filter_complex "[0][1]concat=n=2:v=1[v]" -map "[v]" -c:v libx264 -pix_fmt yuv420p "$T/board2.mp4"
python3 social/tools/compose_video.py --presenter $A/presenter.mp4 --script $A/script.txt --out "$OUT/video.mp4" \
  --broll "5.2:16.6:$T/board1.mp4" --broll "17.2:28.3:$T/board2.mp4" \
  --emph "actually,live,open,original" --hook "Do this before you apply" --endcard
rm -f "$OUT/video.captions.ass"
python3 social/tools/voice_qc.py "$OUT/video.mp4" --script $A/script.txt
echo "Rebuilt $OUT/video.mp4 with today's board. Inspect frames before scheduling."
