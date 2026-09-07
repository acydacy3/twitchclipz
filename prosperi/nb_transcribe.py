"""ACHTUNG — DIESES SKRIPT HAT V7 PROSPERI ZERSTOERT (F-V9-A).

Es schrieb die Spracherkennung nach <serie>/skripte/short_XX.txt, also genau
dorthin, wo die Regel "Captions IMMER aus Skript" ihre Wahrheitsquelle
vermutet. Ergebnis: alle 10 veroeffentlichten Prosperi-Shorts tragen
ASR-Fehler im Bild -- "Marathon des Apples" statt "Sables", "Hartrigt Bauer"
statt "Patrick", "Kincea"/"Kindsjahr" statt "Cinzia".

Seit 07.09.2026 schreibt es nach <serie>/gehoert/ -- ein Ordner, den keine
Regel je fuer ein Skript halten kann. Das Nutzer-Skript kommt ausschliesslich
ueber tools/kp_skript.py in <serie>/skript/ und traegt dort eine Pruefsumme.

Whisper transkribiert prosperi/voiceover/short_XX.mp3 -> words_XX.json."""
import json
from pathlib import Path
from faster_whisper import WhisperModel
BASE = Path("/home/user/twitchclipz/prosperi")
VOICES = sorted((BASE/"voiceover").glob("short_*.mp3"))
print("Lade Whisper (small, DE) ...", flush=True)
model = WhisperModel("small", device="cpu", compute_type="int8")
(BASE/"gehoert").mkdir(exist_ok=True)
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
    (BASE/"gehoert"/f"short_{idx}.gehoert.txt").write_text(" ".join(parts))
    end = words[-1]['end'] if words else 0
    print(f"{vo.name}: {len(words)} Woerter, {end:.2f}s", flush=True)
print("TRANSKRIPTION FERTIG", flush=True)
