import json

with open("words.json", encoding="utf-8") as f:
    words = json.load(f)

# Alle Pausen ab 400ms auflisten - das sind die Kandidaten fuer Szenengrenzen
gaps = []
for i in range(len(words) - 1):
    gap = words[i + 1]["start"] - words[i]["end"]
    if gap >= 0.40:
        gaps.append({
            "at": round((words[i]["end"] + words[i + 1]["start"]) / 2, 2),
            "len_ms": int(gap * 1000),
            "before": " ".join(w["word"] for w in words[max(0, i - 4):i + 1]),
            "after": " ".join(w["word"] for w in words[i + 1:i + 6]),
        })

print(f"{len(gaps)} Pausen >= 400ms gefunden, Gesamtlaenge {words[-1]['end']:.1f}s\n")
for g in gaps:
    m, s = int(g["at"]) // 60, g["at"] % 60
    print(f"{m}:{s:05.2f}  {g['len_ms']:4d}ms  ...{g['before']}  ||  {g['after']}...")
