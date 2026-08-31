#!/usr/bin/env python3
"""Re-Transkription aller 10 Ralston-VOs mit faster-whisper 'small'.
Ersetzt die schwachen Vosk-Captions durch saubere Wort-Zeitstempel.
Ausgabe: ralston/animation/words_XX.json  [{"word","start","end"}]
"""
import json, os, sys
from faster_whisper import WhisperModel

BASE = os.path.dirname(os.path.abspath(__file__))
VO   = os.path.join(BASE, "voiceover")
ANIM = os.path.join(BASE, "animation")

print("Lade Modell medium…", flush=True)
model = WhisperModel("medium", device="cpu", compute_type="int8")

for i in range(1, 11):
    num = f"{i:02d}"
    mp3 = os.path.join(VO, f"short_{num}.mp3")
    if not os.path.exists(mp3):
        print(f"  ⚠ {mp3} fehlt", flush=True); continue
    print(f"  ✍ short_{num}…", flush=True)
    segs, _ = model.transcribe(mp3, word_timestamps=True, language="de", beam_size=5)
    words = []
    for seg in segs:
        for w in (seg.words or []):
            words.append({"word": w.word.strip(), "start": round(w.start, 3), "end": round(w.end, 3)})
    with open(os.path.join(ANIM, f"words_{num}.json"), "w") as f:
        json.dump(words, f, ensure_ascii=False, indent=2)
    print(f"    → {len(words)} Wörter", flush=True)

print("FERTIG", flush=True)
