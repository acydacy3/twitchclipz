"""
Captions mit Wort-Hervorhebung (Karaoke-Stil) aus words.json.

Erzeugt eine ASS-Datei: das gerade gesprochene Wort wird farbig und
groesser dargestellt, der Rest der Phrase bleibt weiss.

    python3 karaoke.py words.json out.ass [start] [ende]

Groessen gelten fuer 1080x1920 (Shorts). Fuer 16:9 mit --wide.
"""
import json
import sys

# --- Stil -------------------------------------------------------------
# vidIQ-Befund zu Video 1: Untertitel zu klein und zu unauffaellig.
# Referenz sind die grossen Shorts-Kanaele: Zeile fuellt 80-90 % der
# Breite, Schrift traegt sich auf einem Handy in der Hand.
FONT = "Roboto Black"
SIZE = 104             # war 78 -> +33 %
COL_IDLE = "&H00FFFFFF"   # weiss
COL_HOT = "&H0047D4FF"    # gold/gelb  (ASS ist BGR!)
OUTLINE = 9            # war 6; traegt ueber hellem Sand und Flutlicht
SHADOW = 5             # weicher Schlagschatten dahinter
MARGIN_V = 500         # Abstand vom unteren Rand (ueber der Shorts-Leiste)
MARGIN_H = 40          # schmalerer Rand -> Zeile darf breiter werden
HOT_SCALE = 118        # aktives Wort auf 118 % skalieren

# Zeilenumbruch: nicht stur nach Wortzahl, sondern nach Breite.
# So fuellt jede Zeile den Rahmen, statt mal 3 kurze Woerter zu zeigen.
MAX_CHARS = 15         # Zeichen pro Zeile (ohne Leerzeichen gerechnet)
MAX_WORDS = 3          # Notbremse fuer sehr kurze Woerter
MAX_LINES = 2          # eine Phrase belegt hoechstens 2 Zeilen
MAX_GAP = 0.55         # groessere Pause -> neue Phrase


def ts(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def header(w=1080, h=1920):
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {w}
PlayResY: {h}
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{FONT},{SIZE},{COL_IDLE},&H00000000,&HA0000000,-1,0,1,{OUTLINE},{SHADOW},2,{MARGIN_H},{MARGIN_H},{MARGIN_V},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""


def phrases(words, t0, t1):
    """Woerter im Zeitfenster zu Phrasen gruppieren.

    Ein Bruch entsteht bei: langer Pause, Satzende, oder wenn die Phrase
    voll ist (MAX_LINES Zeilen a MAX_CHARS).
    """
    sel = [w for w in words if w["end"] > t0 and w["start"] < t1]
    cap = MAX_CHARS * MAX_LINES
    out, cur, chars = [], [], 0
    for w in sel:
        n = len(w["word"])
        full = (chars + n > cap) or len(cur) >= MAX_WORDS * MAX_LINES
        brk = cur and (w["start"] - cur[-1]["end"] > MAX_GAP
                       or cur[-1].get("eos") or full)
        if brk:
            out.append(cur)
            cur, chars = [], 0
        cur.append(w)
        chars += n
    if cur:
        out.append(cur)
    return out


def wrap(words):
    """Phrase in Zeilen brechen (Indizes je Zeile)."""
    lines, cur, chars = [], [], 0
    for i, w in enumerate(words):
        n = len(w["word"])
        if cur and (chars + n > MAX_CHARS or len(cur) >= MAX_WORDS):
            lines.append(cur)
            cur, chars = [], 0
        cur.append(i)
        chars += n
    if cur:
        lines.append(cur)
    return lines


HOLD = 0.20      # wie lange die Phrase nach dem letzten Wort stehen bleibt
GAP = 0.02       # Mindestluecke zwischen zwei Ereignissen


def build(words, path, t0=0.0, t1=1e9, w=1080, h=1920):
    # 1. Ereignisse sammeln (noch ohne Ruecksicht auf Nachbarn)
    ev = []
    for ph in phrases(words, t0, t1):
        rows = wrap(ph)
        for i, wd in enumerate(ph):
            start = wd["start"] - t0
            end = (ph[i + 1]["start"] if i + 1 < len(ph) else wd["end"] + HOLD) - t0
            out_rows = []
            for row in rows:
                parts = []
                for j in row:
                    x = ph[j]["word"]
                    if j == i:
                        parts.append(
                            f"{{\\c{COL_HOT}\\fscx{HOT_SCALE}\\fscy{HOT_SCALE}}}"
                            f"{x}{{\\c{COL_IDLE}\\fscx100\\fscy100}}"
                        )
                    else:
                        parts.append(x)
                out_rows.append(" ".join(parts))
            ev.append([max(0.0, start), end, "\\N".join(out_rows)])

    # 2. Ueberlappungen kappen. Zwei gleichzeitig sichtbare Ereignisse
    #    stapelt libass uebereinander - genau der Ruckel-Effekt.
    ev.sort(key=lambda e: e[0])
    for i in range(len(ev) - 1):
        if ev[i][1] > ev[i + 1][0] - GAP:
            ev[i][1] = ev[i + 1][0] - GAP

    lines = [header(w, h)]
    dropped = 0
    for start, end, text in ev:
        if end - start < 0.04:      # zu kurz zum Lesen -> weglassen
            dropped += 1
            continue
        lines.append(f"Dialogue: 0,{ts(start)},{ts(end)},Cap,,0,0,0,,{text}")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"{path}: {len(lines)-1} Ereignisse"
          + (f", {dropped} zu kurze verworfen" if dropped else ""))


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--wide" in sys.argv:            # 16:9-Langvideo
        # Breiter Rahmen: laengere Zeilen, kleinere Schrift, tiefer sitzend.
        # MAX_WORDS muss mit hoch, sonst bricht die Zeile schon nach drei
        # Woertern und die Breite bleibt ungenutzt.
        # 60 Punkt auf 1920 entsprechen 34 auf 1080 - die Shorts haben 104.
        # Das ist derselbe Fehler wie bei Video 1, nur im anderen Format.
        # 76/1920 entspricht 43/1080; im Breitbild darf die Schrift kleiner
        # sein als im Hochformat, aber nicht dreimal kleiner.
        SIZE, MARGIN_V, OUTLINE, SHADOW = 76, 105, 7, 5
        MAX_CHARS, MAX_WORDS, MAX_LINES, MARGIN_H = 28, 5, 2, 140
    words = json.load(open(args[0], encoding="utf-8"))
    out = args[1]
    a = float(args[2]) if len(args) > 2 else 0.0
    b = float(args[3]) if len(args) > 3 else 1e9
    if "--wide" in sys.argv:
        build(words, out, a, b, 1920, 1080)
    else:
        build(words, out, a, b)
