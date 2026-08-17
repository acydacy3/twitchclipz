import json
import sys
import wave
from vosk import Model, KaldiRecognizer

MODEL_PATH = "vosk-model-small-de-0.15"
WAV_PATH = "voiceover_16k.wav"
SRT_PATH = "captions.srt"

MAX_CHARS = 42
MAX_WORDS = 9
MAX_GAP = 0.6

def fmt_ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

model = Model(MODEL_PATH)
wf = wave.open(WAV_PATH, "rb")
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

words = []
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())
        words.extend(res.get("result", []))
final = json.loads(rec.FinalResult())
words.extend(final.get("result", []))

if not words:
    print("Keine Wörter erkannt!", file=sys.stderr)
    sys.exit(1)

with open("words.json", "w", encoding="utf-8") as f:
    json.dump(words, f, ensure_ascii=False, indent=1)

chunks = []
cur = []
cur_len = 0
for w in words:
    if cur and (w["start"] - cur[-1]["end"] > MAX_GAP or len(cur) >= MAX_WORDS or cur_len + len(w["word"]) + 1 > MAX_CHARS):
        chunks.append(cur)
        cur = []
        cur_len = 0
    cur.append(w)
    cur_len += len(w["word"]) + 1
if cur:
    chunks.append(cur)

with open(SRT_PATH, "w", encoding="utf-8") as f:
    for i, chunk in enumerate(chunks, start=1):
        start = chunk[0]["start"]
        end = chunk[-1]["end"]
        text = " ".join(w["word"] for w in chunk)
        f.write(f"{i}\n{fmt_ts(start)} --> {fmt_ts(end)}\n{text}\n\n")

print(f"{len(chunks)} Caption-Blöcke, letzte Endzeit: {words[-1]['end']:.2f}s")
