#!/usr/bin/env python3
"""Composite a rendered presenter video into a finished social video (free, local, ffmpeg).

    python3 social/tools/compose_video.py --presenter presenter.mp4 --out video.mp4 \
        [--broll 6.2:10.5:board.mp4] [--emph remote,anywhere] [--hook "Remote… but not for you?" --hook-seconds 2.2]

- 1080x1920. The presenter fills the frame (scaled and centre-cropped).
- Captions burned in from the words actually spoken (voice_qc.transcribe): Inter ExtraBold, white on a navy box,
  short chunks (up to 4 words, split at punctuation), placed in the safe zone; words in --emph turn brand blue.
- --broll START:END:FILE cuts to that footage full-screen between START and END (seconds) while the voice continues;
  repeat for several. Footage shorter than the gap is held on its last frame.
- --hook: optional on-screen headline for the first seconds (six words or fewer; the humanizer's rule).
- Audio normalised to about -14 LUFS (two-pass loudnorm). No AI badge or watermark is added (KT, 27 Nov): disclosure
  is the platform's own AI label. The BHuman watermark is cropped off the bottom of the presenter frame (--crop-bottom,
  default 0.11; KT, 27 Nov 2026); board footage and slides are not cropped.
Writes the video and <out>.captions.ass; prints the duration.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import voice_qc  # noqa: E402

W, H = 1080, 1920
NAVY, BLUE, WHITE = "&H004D2A0F&", "&H00EB6325&", "&H00FFFFFF&"   # ASS colours are &HAABBGGRR


def ts(t: float) -> str:
    h, r = divmod(max(t, 0), 3600)
    m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"


def chunks(words: list[dict], max_words: int = 4, max_len: float = 1.8) -> list[list[dict]]:
    out, cur = [], []
    for w in words:
        cur.append(w)
        end_punct = bool(re.search(r"[.,!?;:…]$", w["word"]))
        if len(cur) >= max_words or end_punct or (cur[-1]["end"] - cur[0]["start"]) >= max_len:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    return out


def ass(words: list[dict], emph: set[str], hook: str | None, hook_s: float) -> str:
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter ExtraBold,74,{WHITE},{WHITE},{NAVY},{NAVY},1,0,0,0,100,100,0,0,3,18,0,2,90,150,560,1
Style: Hook,Inter ExtraBold,86,{WHITE},{WHITE},{NAVY},{NAVY},1,0,0,0,100,100,-1,0,3,26,0,8,90,150,330,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    lines = []
    if hook:
        lines.append(f"Dialogue: 1,{ts(0)},{ts(hook_s)},Hook,,0,0,0,,{hook}")
    cs = chunks(words)
    for i, c in enumerate(cs):
        start = c[0]["start"]
        end = cs[i + 1][0]["start"] if i + 1 < len(cs) and cs[i + 1][0]["start"] - c[-1]["end"] < 0.5 else c[-1]["end"] + 0.15
        txt = []
        for w in c:
            word = w["word"].replace("Yairay", "Yireh").replace("Yai-ray", "Yireh")
            key = re.sub(r"[^a-z0-9']", "", word.lower())
            txt.append("{\\c" + BLUE + "}" + word + "{\\c" + WHITE + "}" if key in emph else word)
        lines.append(f"Dialogue: 0,{ts(start)},{ts(end)},Cap,,0,0,0,,{' '.join(txt)}")
    return head + "\n".join(lines) + "\n"


def loudnorm_filter(path: Path) -> str:
    out = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(path), "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    m = json.loads(out[out.rindex("{"):out.rindex("}") + 1])
    return (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--presenter", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--broll", action="append", default=[])
    ap.add_argument("--emph", default="")
    ap.add_argument("--hook")
    ap.add_argument("--hook-seconds", type=float, default=2.2)
    ap.add_argument("--crop-bottom", type=float, default=0.11,
                    help="fraction of the presenter frame cut from the bottom before scaling; removes the BHuman watermark "
                         "(at 91-92%% of the height; KT, 27 Nov: crop out all watermarks). 0 to keep the full frame")
    a = ap.parse_args(argv)
    src, out = Path(a.presenter), Path(a.out)
    words = voice_qc.transcribe(src)
    emph = {w.strip().lower() for w in a.emph.split(",") if w.strip()}
    sub = out.with_suffix(".captions.ass")
    sub.write_text(ass(words, emph, a.hook, a.hook_seconds), encoding="utf-8")
    inputs = ["-i", str(src)]
    keep = 1 - max(0.0, min(a.crop_bottom, 0.3))
    chain = [f"[0:v]crop=iw:trunc(ih*{keep:.3f}/2)*2:0:0,scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps=30[base]"]
    last = "base"
    for k, spec in enumerate(a.broll, 1):
        start, end, f = spec.split(":", 2)
        inputs += ["-i", f]
        chain.append(f"[{k}:v]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,fps=30,"
                     f"tpad=stop_mode=clone:stop_duration=30,setpts=PTS-STARTPTS+{float(start)}/TB[b{k}]")
        chain.append(f"[{last}][b{k}]overlay=enable='between(t,{float(start)},{float(end)})':eof_action=pass[o{k}]")
        last = f"o{k}"
    subpath = str(sub).replace(":", r"\:")
    chain.append(f"[{last}]subtitles='{subpath}':fontsdir=/usr/share/fonts,format=yuv420p[v]")
    chain.append(f"[0:a]{loudnorm_filter(src)},aresample=48000[a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(chain), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-c:a", "aac", "-b:a", "160k", "-shortest",
                    "-movflags", "+faststart", str(out)], check=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(out)]))
    print(out, f"{dur:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
