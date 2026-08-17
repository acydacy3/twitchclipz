"""
Korrigierten Skripttext auf die Vosk-Wortzeitstempel abbilden.

Vosk liefert die Zeiten, aber falsch geschriebenen Text (klein, Eigennamen
verstuemmelt). Das Skript liefert korrekten Text, aber keine Zeiten.
Hier werden beide per Sequenzabgleich zusammengefuehrt.

    python3 align.py words.json ../video2_skript.txt words_fixed.json
"""
import json
import re
import sys
from difflib import SequenceMatcher


# Unicode-fest: deckt auch á é í ó ú ñ ab (Urzúa, José)
TOKEN_RE = r"[^\W_]+(?:[-'][^\W_]+)*"


def norm(s):
    return re.sub(r"[\W_]", "", s.lower())


def align(vosk, tokens, ends=None):
    a = [norm(w["word"]) for w in vosk]
    b = [norm(t) for t in tokens]
    out = []
    sm = SequenceMatcher(a=a, b=b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            for k in range(i2 - i1):
                out.append({**vosk[i1 + k], "word": tokens[j1 + k],
                            "eos": bool(ends and ends[j1 + k])})
        elif tag == "replace":
            # n Vosk-Woerter <-> m Skript-Woerter: Zeitspanne aufteilen
            n, m = i2 - i1, j2 - j1
            t0 = vosk[i1]["start"]
            t1 = vosk[i2 - 1]["end"]
            span = max(t1 - t0, 0.01)
            for k in range(m):
                out.append({
                    "word": tokens[j1 + k],
                    "start": t0 + span * k / m,
                    "end": t0 + span * (k + 1) / m,
                    "eos": bool(ends and ends[j1 + k]),
                })
        elif tag == "insert":
            # Skript hat Woerter, die Vosk nicht hoerte: an Nachbarzeit haengen
            anchor = vosk[i1]["start"] if i1 < len(vosk) else vosk[-1]["end"]
            for k in range(j2 - j1):
                out.append({
                    "word": tokens[j1 + k],
                    "start": anchor,
                    "end": anchor + 0.12,
                    "eos": bool(ends and ends[j1 + k]),
                })
        # tag == "delete": Vosk hoerte etwas, das nicht im Skript steht
        # (z. B. die herausgeschnittene Titelzeile) -> verwerfen

    out.sort(key=lambda w: w["start"])
    # Ueberlappungen glaetten
    for i in range(len(out) - 1):
        if out[i]["end"] > out[i + 1]["start"]:
            out[i]["end"] = out[i + 1]["start"]
    return out


if __name__ == "__main__":
    vosk = json.load(open(sys.argv[1], encoding="utf-8"))
    text = open(sys.argv[2], encoding="utf-8").read()
    if "\n" in text:                      # Titelzeile entfernen
        text = text.split("\n", 1)[1]
    # Tokens + Merker, ob danach ein Satzzeichen folgt
    tokens, ends = [], []
    for m in re.finditer(TOKEN_RE, text):
        tokens.append(m.group())
        rest = text[m.end():m.end()+3]
        ends.append(bool(re.match(r"\s*[.!?:]", rest)))

    fixed = align(vosk, tokens, ends)
    json.dump(fixed, open(sys.argv[3], "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    same = sum(1 for a, b in zip(vosk, fixed) if a["word"] != b["word"])
    print(f"Vosk {len(vosk)} -> abgeglichen {len(fixed)} Woerter")
    print("\nStichprobe:")
    for w in fixed[:10]:
        print(f"  {w['start']:6.2f}  {w['word']}")
