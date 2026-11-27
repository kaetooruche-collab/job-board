#!/usr/bin/env python3
"""Turn a post's rendered slides (1080x1350 JPEGs) into a 1080x1920 vertical video for Reels and TikTok. Free (ffmpeg).

    python3 social/tools/slides_to_video.py social/output/2026-12-04/w49-p4 --seconds 4
    python3 social/tools/slides_to_video.py <dir> --footage social/output/footage/board.mp4   # board clip after the slides

Slides sit in the vertical safe zone on the hero navy, with a short crossfade. A silent audio track is added because
some apps treat videos without audio as broken; KT or the platform adds music by hand if wanted (business accounts
are limited to the commercial music library). Writes <dir>/video.mp4 and prints its duration.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

NAVY = "0x131c35"
FADE = 0.4


def build(d: Path, seconds: float, footage: Path | None, out: Path) -> float:
    slides = sorted(d.glob("[0-9][0-9].jpg"))
    if not slides:
        raise SystemExit(f"no slides (NN.jpg) in {d}")
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for s in slides:
        cmd += ["-loop", "1", "-t", str(seconds), "-i", str(s)]
    if footage:
        cmd += ["-i", str(footage)]
    cmd += ["-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=44100"]
    n = len(slides) + (1 if footage else 0)
    parts = []
    for i in range(len(slides)):
        # 1080x1350 slide centred on a 1080x1920 navy canvas (y 285-1635; text stays well inside the safe zone)
        parts.append(f"[{i}:v]scale=1080:1350,pad=1080:1920:0:285:color={NAVY},setsar=1,fps=30,format=yuv420p[v{i}]")
    if footage:
        parts.append(f"[{len(slides)}:v]scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color={NAVY},setsar=1,fps=30,format=yuv420p[v{len(slides)}]")
    durs = [seconds] * len(slides)
    if footage:
        durs.append(float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(footage)]).strip()))
    last, t = "v0", durs[0]
    for i in range(1, n):
        parts.append(f"[{last}][v{i}]xfade=transition=fade:duration={FADE}:offset={t - FADE:.2f}[x{i}]")
        last, t = f"x{i}", t + durs[i] - FADE
    cmd += ["-filter_complex", ";".join(parts), "-map", f"[{last}]", "-map", f"{n}:a", "-shortest",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k",
            "-movflags", "+faststart", "-t", f"{t:.2f}", str(out)]
    subprocess.run(cmd, check=True)
    return t


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("dir")
    ap.add_argument("--seconds", type=float, default=4.0)
    ap.add_argument("--footage")
    a = ap.parse_args(argv)
    d = Path(a.dir)
    out = d / "video.mp4"
    t = build(d, a.seconds, Path(a.footage) if a.footage else None, out)
    m = d / "manifest.json"
    if m.exists():
        man = json.loads(m.read_text(encoding="utf-8"))
        man["video"] = {"file": out.name, "seconds": round(t, 2), "size": "1080x1920"}
        m.write_text(json.dumps(man, indent=2, ensure_ascii=False), encoding="utf-8")
    print(out, f"{t:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
