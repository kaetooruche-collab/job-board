#!/usr/bin/env python3
"""Objective checks on a voice track (narration, audition or rendered video). Claude cannot hear audio; this measures
what can be measured, and the presenter-director skill says what still needs a human ear.

    python3 social/tools/voice_qc.py narration.mp3 --script script.txt [--json out.json]
    python3 social/tools/voice_qc.py video.mp4                       # transcript, pace, pauses, loudness only

Reports: the transcript as heard (local speech-to-text, faster-whisper base.en), words that differ from the script
(mispronounced, dropped or added words show up here, e.g. "Yireh" heard as "Year"), speaking pace in words per minute,
every pause of 0.25 s or more with its position in the script, long gaps, and integrated loudness (LUFS).
Thresholds come from the presenter-director skill: 140-175 wpm for social talking-head delivery (conversational
English is commonly 150-160; our working range, not a cited standard), loudness normalised to about -14 LUFS at export.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from difflib import SequenceMatcher
from pathlib import Path

WORD = re.compile(r"[a-z0-9']+")
# Brand words the recogniser spells differently; the narration spelling "Yai-ray" is how Yireh is said aloud.
# "yari": how the recogniser writes Zee's "Yi-ray", which KT judged correct by ear (27 Nov, brand-tests/test3).
SAME = {"yari": "yireh", "yi-ray": "yireh", "yiray": "yireh", "yairay": "yireh", "yai": "yireh", "yaire": "yireh", "yireh": "yireh", "yai-ray": "yireh"}


_ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def _spell(n: int) -> str:
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("" if n % 10 == 0 else " " + _ONES[n % 10])
    if n < 1000:
        return _ONES[n // 100] + " hundred" + ("" if n % 100 == 0 else " " + _spell(n % 100))
    if n < 1_000_000:
        return _spell(n // 1000) + " thousand" + ("" if n % 1000 == 0 else " " + _spell(n % 1000))
    return str(n)


def words(text: str) -> list[str]:
    """Normalised words; digits are spelled out so '2,000' and 'two thousand' compare equal."""
    num2words = _spell
    t = re.sub(r"(\d)\s?[ ,]\s?(\d{3})\b", r"\1\2", text.lower().replace("yai-ray", "yairay").replace("yi-ray", "yiray"))
    if num2words:
        t = re.sub(r"\d+", lambda m: num2words(int(m[0])), t)
    out = []
    for w in WORD.findall(t.replace("-", " ")):
        out.append(SAME.get(w, w))
    return [w for w in out if w != "and"]   # "two thousand and seven" vs "two thousand seven"


def transcribe(path: Path) -> list[dict]:
    import numpy as np
    from faster_whisper import WhisperModel
    with tempfile.NamedTemporaryFile(suffix=".raw") as raw:
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(path), "-ar", "16000", "-ac", "1", "-f", "f32le",
                        raw.name], check=True)
        audio = np.fromfile(raw.name, dtype=np.float32)
    model = WhisperModel("base.en", device="cpu", compute_type="int8")
    segs, _ = model.transcribe(audio, word_timestamps=True)
    return [{"word": w.word.strip(), "start": round(w.start, 2), "end": round(w.end, 2)} for s in segs for w in s.words]


def loudness(path: Path) -> float | None:
    out = subprocess.run(["ffmpeg", "-i", str(path), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?\d+(?:\.\d+)?) LUFS", out)
    return float(m[-1]) if m else None


def analyse(path: Path, script: str | None) -> dict:
    ws = transcribe(path)
    heard = " ".join(w["word"] for w in ws)
    pauses = []
    for a, b in zip(ws, ws[1:]):
        gap = round(b["start"] - a["end"], 2)
        if gap >= 0.25:
            pauses.append({"after": a["word"], "before": b["word"], "at": a["end"], "seconds": gap})
    talk = (ws[-1]["end"] - ws[0]["start"]) if ws else 0
    res = {"file": str(path), "transcript": heard, "words": len(ws), "speech_seconds": round(talk, 2),
           "wpm": round(len(ws) / talk * 60) if talk else None, "pauses": pauses, "lufs": loudness(path), "timed_words": ws}
    if script:
        a, b = words(script), words(heard)
        sm = SequenceMatcher(None, a, b, autojunk=False)
        diffs = [{"script": " ".join(a[i1:i2]), "heard": " ".join(b[j1:j2]), "kind": tag}
                 for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]
        res["match"] = round(sm.ratio(), 3)
        res["differences"] = diffs
    flags = []
    if res["wpm"] and not 140 <= res["wpm"] <= 175:
        flags.append(f"pace {res['wpm']} wpm is outside 140-175")
    long = [p for p in pauses if p["seconds"] > 1.2]
    if long:
        flags.append("pause over 1.2 s after " + ", ".join(f"'{p['after']}' ({p['seconds']}s)" for p in long)
                     + ": fine only if the direction sheet asks for a reveal pause there")
    if script and res.get("match", 1) < 0.95:
        flags.append(f"transcript matches the script at {res['match']:.0%}: check the differences (pronunciation or dropped words)")
    # The brand (KT, 27 Nov 2026): "Yi" is "hi" with a Y (yai, no W sound), "reh" is "ray". A W sound ("why ray",
    # "worry", "wiric") or one merged syllable is wrong. Any brand difference is a hard flag, never waved through.
    for d in res.get("differences", []):
        if "yireh" in d["script"].split():
            flags.append(f"BRAND said wrong: heard '{d['heard']}' (say Yai-ray: 'hi' with a Y, then 'ray'; no W sound)")
    res["flags"] = flags
    return res


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--script")
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    script = Path(a.script).read_text(encoding="utf-8") if a.script and Path(a.script).exists() else a.script
    r = analyse(Path(a.audio), script)
    if a.json:
        Path(a.json).write_text(json.dumps(r, indent=2), encoding="utf-8")
    print(f"{Path(a.audio).name}: {r['words']} words in {r['speech_seconds']}s = {r['wpm']} wpm; loudness {r['lufs']} LUFS")
    print("heard:", r["transcript"])
    for p in r["pauses"]:
        print(f"  pause {p['seconds']}s after '{p['after']}' (at {p['at']}s)")
    for d in r.get("differences", []):
        print(f"  DIFF {d['kind']}: script '{d['script']}' / heard '{d['heard']}'")
    for f in r["flags"]:
        print("  FLAG", f)
    return 1 if r["flags"] else 0


if __name__ == "__main__":
    sys.exit(main())
