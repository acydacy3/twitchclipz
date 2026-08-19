"""Whisper transcribiert alle 10 Voiceover mit Wort-Zeiten -> words_XX.json (Vosk-Format)."""
import json
import sys
from pathlib import Path
from faster_whisper import WhisperModel

BASE = Path("/home/user/twitchclipz/koepcke")
VOICES = sorted((BASE / "voiceover").glob("*.mp3"))

print(f"Lade Whisper (small, DE) ...", flush=True)
model = WhisperModel("small", device="cpu", compute_type="int8")

for vo in VOICES:
    idx = vo.stem.split("_")[1]
    print(f"[{vo.name}] transkribiere ...", flush=True)
    segments, info = model.transcribe(str(vo), language="de", word_timestamps=True, vad_filter=True)
    words = []
    text_parts = []
    for seg in segments:
        for w in seg.words or []:
            wrd = w.word.strip()
            if not wrd:
                continue
            words.append({"word": wrd, "start": round(w.start, 3), "end": round(w.end, 3), "conf": 1.0})
            text_parts.append(wrd)
    out_json = BASE / f"words_{idx}.json"
    out_txt = BASE / "skripte" / f"short_{idx}.txt"
    out_json.write_text(json.dumps(words, ensure_ascii=False, indent=2))
    out_txt.parent.mkdir(exist_ok=True)
    out_txt.write_text(" ".join(text_parts))
    print(f"  -> {len(words)} Wörter, {words[-1]['end']:.2f}s")
