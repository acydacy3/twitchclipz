"""Whisper transkribiert nuttyputty/voiceover/short_XX.mp3 -> words_XX.json (flache Liste)."""
import json
from pathlib import Path
from faster_whisper import WhisperModel
BASE = Path("/home/user/twitchclipz/nuttyputty")
VOICES = sorted((BASE/"voiceover").glob("short_*.mp3"))
print("Lade Whisper (small, DE) ...", flush=True)
model = WhisperModel("small", device="cpu", compute_type="int8")
(BASE/"skripte").mkdir(exist_ok=True)
for vo in VOICES:
    idx = vo.stem.split("_")[1]
    segs,_ = model.transcribe(str(vo), language="de", word_timestamps=True, vad_filter=True)
    words=[]; parts=[]
    for seg in segs:
        for w in seg.words or []:
            t=w.word.strip()
            if not t: continue
            words.append({"word":t,"start":round(w.start,3),"end":round(w.end,3),"conf":1.0}); parts.append(t)
    (BASE/f"words_{idx}.json").write_text(json.dumps(words,ensure_ascii=False,indent=2))
    (BASE/"skripte"/f"short_{idx}.txt").write_text(" ".join(parts))
    print(f"{vo.name}: {len(words)} Woerter, {words[-1]['end']:.2f}s", flush=True)
print("TRANSKRIPTION FERTIG", flush=True)
