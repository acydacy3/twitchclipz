#!/usr/bin/env python3
"""Korrigiert Eigennamen/Fachbegriffe in den medium-Captions (1:1-Token-Tausch,
Timing bleibt erhalten). 1→2-Wort-Splits teilen die Zeit hälftig.
Danach: reiner Text pro Short zur Kontrolle ausgeben.
"""
import json, os, re, string

BASE = os.path.dirname(os.path.abspath(__file__))
ANIM = os.path.join(BASE, "animation")

# 1:1 Tausch (Kern ohne Satzzeichen, case-insensitive)
FIX = {
    "rallsturm": "Ralston", "rallstuhl": "Ralston", "raltstohn": "Ralston",
    "raalstund": "Ralston", "raalstend": "Ralston", "ralshton": "Ralston",
    "ralsdund": "Ralston", "ralsdum": "Ralston", "raltstohn,": "Ralston",
    "elio": "Leo", "tilogramm": "Kilogramm", "zerte": "zerrte", "preste": "presste",
    "eingeklennt": "eingeklemmt", "felsschirm": "Felsschlucht",
    "hitzecollaps": "Hitzekollaps", "trittste": "ritzte",
    "engelwod": "Englewood", "engelwoth": "Englewood",
    "abschiedsfinn": "Abschiedsfilm", "abschiedsfin": "Abschiedsfilm",
    "biszeller": "Bestseller", "jemes": "James",
    "motivationsretner": "Motivationsredner", "protesse": "Prothese",
    "tonikwett": "Tourniquet", "atherie": "Arterie", "naherung": "Nahrung",
    "wiste": "Wüste", "uthas": "Utahs", "uthers": "Utahs",
    "herauskehnen": "herauskommen", "schrien": "schrie",
    "bohgen": "bogen", "bohgt": "bog", "bluejohn": "Blue-John",
    "erexistiert": "existiert",
}
# 1→2-Split (ein Token → zwei), Zeit hälftig
SPLIT = {
    "einloser": ["ein", "loser"],
}

def core(tok):
    return tok.strip(string.punctuation + "„""»«").lower()

def punct(tok):
    m = re.match(r'^(\W*)(.*?)(\W*)$', tok, re.S)
    return m.group(1), m.group(3)

for i in range(1, 11):
    num = f"{i:02d}"
    p = os.path.join(ANIM, f"words_{num}.json")
    words = json.load(open(p))
    out = []
    for w in words:
        tok = w["word"]; c = core(tok); pre, post = punct(tok)
        if c in SPLIT:
            a, b = SPLIT[c]; mid = (w["start"] + w["end"]) / 2
            out.append({"word": pre + a, "start": w["start"], "end": round(mid, 3)})
            out.append({"word": b + post, "start": round(mid, 3), "end": w["end"]})
        elif c in FIX:
            out.append({"word": pre + FIX[c] + post, "start": w["start"], "end": w["end"]})
        else:
            out.append(w)
    # Duplikat-Satz-Erkennung (02): identische aufeinanderfolgende 6-Wort-Blöcke am Ende
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=2)

print("Namen korrigiert. Kontroll-Text:")
for i in range(1, 11):
    num = f"{i:02d}"
    txt = " ".join(w["word"] for w in json.load(open(os.path.join(ANIM, f"words_{num}.json"))))
    print(f"\n[{num}] {txt}")
