#!/usr/bin/env python3
"""kp_gate.py — deterministisches Produktions-Gate (blockiert wirklich).

Der Unterschied zu nb_contrarian.py: dieses Skript liest den INHALT des
Materials, nicht nur die Schluessel einer Konfig, und es beendet sich mit
Exit-Code 1, wenn eine Regel verletzt ist. Ein Aufrufer (Hook, Makefile,
Mensch) kann daran verzweigen.

    python3 tools/kp_gate.py <serie>              alle Shorts pruefen
    python3 tools/kp_gate.py <serie> --short 03   einen Short pruefen
    python3 tools/kp_gate.py <serie> --json       maschinenlesbar

Exit-Code
    0   alle Pruefungen bestanden  -> rendern/hochladen erlaubt
    1   mindestens eine Regel verletzt -> BLOCKIERT
    2   Serie/Material nicht gefunden

Geprueft werden genau die Regeln, die in der Vergangenheit gebrochen wurden,
obwohl sie im Vault standen:

  HERKUNFT   Ist belegt, dass das "Skript" wirklich vom Nutzer kommt?
             (F-V8-E-Falle: prosperi/nb_transcribe.py schrieb die ASR-Ausgabe
             nach prosperi/skripte/short_XX.txt -- also genau dorthin, wo die
             Regel "Captions aus Skript" ihre Wahrheitsquelle vermutet.)
  CAPTIONS   Stimmen die gerenderten Caption-Woerter mit dem Skript ueberein?
             (faengt "Marathon des Apples" statt "Sables")
  BEWEGUNG   Hat der Short echte Bewegung, oder ist er eine Ken-Burns-Diashow?
  TON        Musikbett laut genug, um hoerbar zu sein?

Jede Pruefung nennt bei Verstoss die konkrete Stelle, nicht nur ein Urteil.
"""

import argparse
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Wortgrenzen wie in align.py -- Unicode-fest (Urzua, Koepcke, Prosperi)
TOKEN_RE = r"[^\W_]+(?:[-'][^\W_]+)*"

# Ab welcher Wort-Uebereinstimmung gilt eine Caption als "aus dem Skript"?
# 0.98 laesst Interpunktion/Zahlwort-Varianten durch, faengt aber jedes
# verstuemmelte Eigenwort. Bei prosperi/03 liegt der Wert bei ~0.87.
CAPTION_SCHWELLE = 0.98

# Musikbett: unter -18 dB war es in V1-V5 unhoerbar (Nutzer-Befund 25.08.)
MUSIK_MIN_DB = -18


# ─────────────────────────────────────────────────────── Hilfen

def tokens(text):
    return re.findall(TOKEN_RE, text)


def norm(s):
    return re.sub(r"[\W_]", "", s.lower())


def erste_datei(*kandidaten):
    """Gibt den ersten existierenden Pfad zurueck, sonst None."""
    for k in kandidaten:
        if k and os.path.exists(k):
            return k
    return None


class Befund:
    """Ein Pruefergebnis. 'hart' = blockiert den Render/Upload."""

    def __init__(self, regel, ok, text, hart=True, stelle=None):
        self.regel, self.ok, self.text = regel, ok, text
        self.hart, self.stelle = hart, stelle

    def __str__(self):
        zeichen = "OK  " if self.ok else ("FEHL" if self.hart else "warn")
        s = f"  [{zeichen}] {self.regel:<10} {self.text}"
        if self.stelle:
            s += f"\n              -> {self.stelle}"
        return s


# ─────────────────────────────────────────── Material auffinden

def finde_skript(serie, num):
    """Der vom Nutzer gelieferte Text dieses Shorts.

    Reihenfolge ist Absicht: zuerst die Orte mit Herkunftsnachweis, dann die
    historischen. Ein Ordner allein beweist nichts -- pruefe_herkunft() sagt,
    ob dem Fund zu trauen ist.
    """
    # a) kanonisch: <serie>/skript/short_XX.txt
    p = erste_datei(os.path.join(serie, "skript", f"short_{num}.txt"))
    if p:
        text = open(p, encoding="utf-8").read()
        # Erste Zeile ist bei ralston eine Titelzeile ("short_01"), kein Inhalt
        zeilen = text.split("\n", 1)
        if len(zeilen) > 1 and re.fullmatch(r"short_\d+\s*", zeilen[0]):
            text = zeilen[1]
        return p, text
    # b) Sammel-Datei: <serie>/skripte.json  {"01": "...", ...}
    p = erste_datei(os.path.join(serie, "skripte.json"))
    if p:
        d = json.load(open(p, encoding="utf-8"))
        if num in d:
            return f"{p}[{num}]", d[num]
    # c) historisch/unsicher: <serie>/skripte/short_XX.txt
    p = erste_datei(os.path.join(serie, "skripte", f"short_{num}.txt"))
    if p:
        return p, open(p, encoding="utf-8").read()
    return None, None


def finde_words(serie, num):
    """Die Wortliste, aus der die Captions gebrannt werden."""
    p = erste_datei(
        os.path.join(serie, "animation", f"words_{num}.json"),
        os.path.join(serie, f"words_{num}.json"),
        os.path.join(serie, "words", f"words_{num}.json"),
    )
    if not p:
        return None, None
    return p, json.load(open(p, encoding="utf-8"))


def _shots_aus_nb_build(serie, num):
    """Shot-Konfig aus dem SHORTS-Dict in <serie>/nb_build.py lesen.

    Manche Serien (ralston) halten ihre Shot-Liste nicht in configs/*.json,
    sondern als Literal im Build-Skript. Ohne diesen Pfad geht das Gate dort
    gruen, weil es nichts zu pruefen findet -- die Bewegtbild-Regel waere
    genau bei der juengsten Serie unwirksam.

    Gelesen wird per ast.literal_eval, nicht per import: das Build-Skript
    darf beim Pruefen nichts ausfuehren.
    """
    import ast
    p = os.path.join(serie, "nb_build.py")
    if not os.path.exists(p):
        return None, None
    try:
        baum = ast.parse(open(p, encoding="utf-8").read())
    except SyntaxError:
        return None, None
    for knoten in baum.body:
        if not isinstance(knoten, ast.Assign):
            continue
        namen = [z.id for z in knoten.targets if isinstance(z, ast.Name)]
        if "SHORTS" not in namen:
            continue
        try:
            shorts = ast.literal_eval(knoten.value)
        except (ValueError, SyntaxError):
            return None, None
        eintrag = shorts.get(num) or shorts.get(int(num.lstrip("0") or "0"))
        if eintrag is None:
            return None, None
        # imgs = Standbilder (Ken-Burns), manim/clip = echte Bewegung
        shots = [{"img": b} for b in eintrag.get("imgs", [])]
        cfg = {"shots": shots}
        if eintrag.get("manim"):
            cfg["manim"] = eintrag["manim"]
        if eintrag.get("clip"):
            cfg["shots"].insert(0, {"clip": eintrag["clip"]})
        return f"{p}:SHORTS[{num}]", cfg
    return None, None


def finde_config(serie, num):
    p = erste_datei(os.path.join(serie, "configs", f"short_{num}.json"))
    if p:
        return p, json.load(open(p, encoding="utf-8"))
    return _shots_aus_nb_build(serie, num)


def shorts_einer_serie(serie):
    nums = set()
    for muster, gruppe in (
        (r"short_(\d+)\.txt", 1), (r"words_(\d+)\.json", 1),
        (r"short_(\d+)\.json", 1),
    ):
        for unter in ("", "skript", "skripte", "configs", "animation"):
            d = os.path.join(serie, unter)
            if not os.path.isdir(d):
                continue
            for name in os.listdir(d):
                m = re.fullmatch(muster, name)
                if m:
                    nums.add(m.group(gruppe))
    sj = os.path.join(serie, "skripte.json")
    if os.path.exists(sj):
        nums.update(json.load(open(sj, encoding="utf-8")).keys())
    return sorted(nums)


# ─────────────────────────────────────────────────── Pruefungen

def pruefe_herkunft(serie, num, skript_pfad, skript_text):
    """HERKUNFT -- ist belegt, dass dieser Text vom Nutzer stammt?

    Belegt heisst: <serie>/skript/QUELLE.json enthaelt fuer diesen Short einen
    sha256 des Textes, den der Nutzer geliefert hat, und der Text auf der
    Platte hat noch denselben Hash.

    Ohne diesen Nachweis ist "das Skript" nur ein Dateiname. Genau daran
    scheiterte V7: prosperi/nb_transcribe.py schrieb die Spracherkennung nach
    prosperi/skripte/short_XX.txt und machte die ASR-Ausgabe damit zur
    vermeintlichen Wahrheitsquelle.
    """
    regel = "HERKUNFT"
    if skript_text is None:
        return Befund(regel, False, f"Short {num}: kein Skript gefunden",
                      stelle=f"erwartet: {serie}/skript/short_{num}.txt")

    manifest_pfad = os.path.join(serie, "skript", "QUELLE.json")
    if not os.path.exists(manifest_pfad):
        return Befund(
            regel, False,
            f"Short {num}: kein Herkunftsnachweis fuer '{skript_pfad}'",
            stelle=(f"{serie}/skript/QUELLE.json fehlt -- anlegen mit: "
                    f"python3 tools/kp_skript.py {serie} --aus <nutzer-datei>"))

    man = json.load(open(manifest_pfad, encoding="utf-8"))
    eintrag = man.get("shorts", {}).get(num)
    if not eintrag:
        return Befund(regel, False,
                      f"Short {num}: nicht in QUELLE.json eingetragen",
                      stelle=manifest_pfad)

    ist = hashlib.sha256(skript_text.strip().encode("utf-8")).hexdigest()
    if ist != eintrag.get("sha256"):
        return Befund(
            regel, False,
            f"Short {num}: Skript wurde nach der Nutzer-Lieferung veraendert",
            stelle=(f"{skript_pfad}\n                 sha256 jetzt {ist[:16]}, "
                    f"laut QUELLE.json {eintrag.get('sha256','?')[:16]}"))

    stufe = eintrag.get("vertrauen", "unbekannt")
    herkunft = {
        "nutzer": "vom Nutzer geliefert",
        "repo-historisch": "aus dem Repo uebernommen (nicht neu vom Nutzer)",
    }.get(stufe, f"Vertrauensstufe '{stufe}' unbekannt")
    return Befund(regel, True,
                  f"Short {num}: {herkunft}, unveraendert "
                  f"({eintrag.get('geliefert_am','?')})")


def pruefe_captions(num, skript_text, words_pfad, words):
    """CAPTIONS -- stehen im Video wirklich die Woerter des Skripts?

    Das ist die Pruefung, die "Marathon des Apples" faengt. Sie vergleicht
    nicht Dateinamen und nicht Konfig-Schluessel, sondern Wort fuer Wort.
    """
    regel = "CAPTIONS"
    if words is None:
        # Vor dem ersten Render gibt es noch keine Wortliste. Das ist kein
        # Regelverstoss, sondern ein Zustand -- sonst koennte nie gerendert
        # werden, weil der Render die Wortliste erst erzeugt. Verbindlich
        # geprueft wird nach dem Render (--nachher).
        return Befund(regel, True,
                      f"Short {num}: noch keine words_{num}.json "
                      f"(wird beim Render erzeugt) -- Pruefung erfolgt in --nachher",
                      hart=False)
    if skript_text is None:
        return Befund(regel, False, f"Short {num}: kein Skript zum Vergleich")

    cap = [norm(w["word"]) for w in words if norm(w["word"])]
    skr = [norm(t) for t in tokens(skript_text) if norm(t)]
    if not cap or not skr:
        return Befund(regel, False, f"Short {num}: leere Wortliste oder leeres Skript")

    sm = difflib.SequenceMatcher(a=cap, b=skr, autojunk=False)
    quote = sm.ratio()

    # Konkrete Abweichungen benennen -- ein Urteil ohne Fundstelle hilft nicht.
    abweichungen = []
    roh_cap = [w["word"] for w in words if norm(w["word"])]
    roh_skr = [t for t in tokens(skript_text) if norm(t)]
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        im_video = " ".join(roh_cap[i1:i2]) or "(fehlt)"
        im_skript = " ".join(roh_skr[j1:j2]) or "(fehlt)"
        abweichungen.append((im_video, im_skript))

    if quote >= CAPTION_SCHWELLE:
        return Befund(regel, True,
                      f"Short {num}: Captions = Skript ({quote:.0%})")

    zeilen = [f"{words_pfad}  (Uebereinstimmung {quote:.0%}, "
              f"noetig {CAPTION_SCHWELLE:.0%})"]
    for im_video, im_skript in abweichungen[:8]:
        zeilen.append(f'                 im Video "{im_video}"  '
                      f'-- im Skript "{im_skript}"')
    if len(abweichungen) > 8:
        zeilen.append(f"                 ... und {len(abweichungen)-8} weitere")
    return Befund(regel, False,
                  f"Short {num}: Captions weichen vom Skript ab "
                  f"({len(abweichungen)} Stellen)",
                  stelle="\n".join(zeilen))


def pruefe_bewegung(num, cfg_pfad, cfg):
    """BEWEGUNG -- echte Bewegung, oder Ken-Burns-Diashow?

    Stehende Regel seit 31.08./06.09.: Ken-Burns-Zoom ueber ein Standbild
    zaehlt ausdruecklich NICHT als Bewegung. Gezaehlt wird nur ein echter
    Bewegtshot: ein Video-Clip ({"clip": ...}) oder eine Manim-Szene.
    """
    regel = "BEWEGUNG"
    if cfg is None:
        return Befund(regel, False, f"Short {num}: keine Konfig gefunden",
                      hart=False,
                      stelle=f"erwartet {cfg_pfad or 'configs/short_XX.json'}")

    shots = cfg.get("shots", [])
    bewegt = [s for s in shots if s.get("clip") or s.get("manim") or s.get("video")]
    # Ein Manim-Clip auf oberster Ebene laeuft am Anfang des Shorts (so baut
    # ralston/nb_build.py) -- er zaehlt als Bewegung UND als bewegter Hook.
    manim_vorne = bool(cfg.get("manim"))
    if manim_vorne:
        bewegt.append({"manim": cfg["manim"]})

    if not bewegt:
        return Befund(
            regel, False,
            f"Short {num}: {len(shots)} Shots, davon 0 bewegt -- Standbild-Diashow",
            stelle=(f"{cfg_pfad}\n                 Ken-Burns zaehlt nicht. "
                    f"Noetig: >=1 Shot mit \"clip\" (Remotion/Wan2.1-I2V) "
                    f"oder \"manim\"."))

    # Sekunde 1 muss bewegt sein -- der Hook entscheidet ueber die Retention.
    erster = shots[0] if shots else {}
    hook_bewegt = manim_vorne or bool(
        erster.get("clip") or erster.get("manim") or erster.get("video"))
    if not hook_bewegt:
        return Befund(
            regel, False,
            f"Short {num}: {len(bewegt)}/{len(shots)} Shots bewegt, "
            f"aber Sekunde 1 ist ein Standbild",
            stelle=(f"{cfg_pfad}\n                 Der Hook-Shot (shots[0]) muss "
                    f"bewegt sein -- ruhiges Establishing kostet die Retention."))

    return Befund(regel, True,
                  f"Short {num}: {len(bewegt)}/{len(shots)} Shots bewegt, Hook bewegt")


def pruefe_ton(num, cfg_pfad, cfg):
    """TON -- ist das Musikbett laut genug, um gehoert zu werden?"""
    regel = "TON"
    if cfg is None:
        return Befund(regel, True, f"Short {num}: keine Konfig -- Ton nicht pruefbar",
                      hart=False)
    mus = cfg.get("musik")
    if not mus:
        return Befund(regel, True, f"Short {num}: kein Musikbett konfiguriert",
                      hart=False)
    db = mus.get("db")
    if db is None:
        return Befund(regel, False, f"Short {num}: musik ohne db-Wert",
                      stelle=cfg_pfad)
    if db < MUSIK_MIN_DB:
        return Befund(regel, False,
                      f"Short {num}: musik.db={db} -- unter {MUSIK_MIN_DB} unhoerbar "
                      f"(Fehler V1-V5)", stelle=cfg_pfad)
    return Befund(regel, True, f"Short {num}: musik.db={db}")


# ──────────────────────────────────── Nach dem Render: ins Bild sehen

def _dauer(pfad):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", pfad],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def _ass_zeiten(ass_pfad):
    """(Anzahl Dialogzeilen, letzte Endzeit in Sekunden)."""
    zeilen = 0
    letzte = 0.0
    for z in open(ass_pfad, encoding="utf-8", errors="ignore"):
        if not z.startswith("Dialogue:"):
            continue
        zeilen += 1
        teile = z.split(",")
        if len(teile) > 2:
            try:
                h, m, s = teile[2].strip().split(":")
                letzte = max(letzte, int(h) * 3600 + int(m) * 60 + float(s))
            except ValueError:
                pass
    return zeilen, letzte


def _caption_sichtbar(video, sekunde):
    """Sind im Untertitel-Band ueberhaupt helle Schriftpixel?

    Das ist die Pruefung, die kein Dateiname und kein Konfig-Schluessel
    ersetzen kann: sie sieht in das fertige Bild. Genau hier ging es schief --
    nb_build.py meldete "Captions aus Skript" und rendert trotzdem ein Video
    ohne einen einzigen Untertitel, weil die Wortliste leer war.

    Gemessen wird im unteren Viertel (ueber der Fortschrittsleiste) die
    Helligkeit der hellsten Stelle. Untertitel sind gelb/weiss auf dunklem
    Grund mit Kontur -- sie heben die Spitzenhelligkeit deutlich an.
    """
    # -v info ist Pflicht: unter -v error unterdrueckt ffmpeg genau die
    # metadata-Ausgabe, die hier gemessen wird -- die Pruefung meldete dann
    # immer 0 und damit "keine Untertitel", egal was im Bild stand. Eine
    # Messung, die immer dasselbe sagt, misst nichts.
    r = subprocess.run(
        ["ffmpeg", "-v", "info", "-ss", f"{sekunde:.2f}", "-i", video,
         "-frames:v", "1", "-vf",
         "crop=iw:ih/5:0:ih*0.72,signalstats,metadata=print:key=lavfi.signalstats.YMAX",
         "-f", "null", "-"],
        capture_output=True, text=True)
    werte = [int(x) for x in re.findall(r"YMAX=(\d+)", r.stderr + r.stdout)]
    return max(werte) if werte else -1


def pruefe_render(serie, num):
    """Prueft das FERTIGE Video, nicht die Absicht."""
    befunde = []
    video = erste_datei(os.path.join(serie, "render", f"short_{num}.mp4"),
                        os.path.join(serie, "output", f"short_{num}.mp4"))
    if not video:
        return [Befund("RENDER", False, f"Short {num}: kein gerendertes Video",
                       stelle=f"erwartet {serie}/render/short_{num}.mp4")]

    dauer = _dauer(video)
    vo = erste_datei(os.path.join(serie, "voiceover", f"short_{num}.mp3"))
    if vo:
        vd = _dauer(vo)
        if abs(dauer - vd) > 1.5:
            befunde.append(Befund(
                "RENDER", False,
                f"Short {num}: Video {dauer:.1f}s, Voiceover {vd:.1f}s "
                f"({abs(dauer-vd):.1f}s Abweichung)", stelle=video))
        else:
            befunde.append(Befund("RENDER", True,
                                  f"Short {num}: {dauer:.1f}s, deckt das Voiceover"))
    else:
        befunde.append(Befund("RENDER", True, f"Short {num}: {dauer:.1f}s"))

    # ── Untertitel: erst die Datei, dann das Bild ─────────────────────────
    ass = erste_datei(os.path.join(serie, "animation", f"sub_{num}.ass"),
                      os.path.join(serie, f"sub_{num}.ass"))
    if not ass:
        befunde.append(Befund("UNTERTITEL", False,
                              f"Short {num}: keine ASS-Datei gefunden"))
        return befunde

    zeilen, letzte = _ass_zeiten(ass)
    if zeilen == 0:
        befunde.append(Befund("UNTERTITEL", False,
                              f"Short {num}: ASS ohne eine einzige Dialogzeile",
                              stelle=ass))
        return befunde
    abdeckung = letzte / dauer if dauer else 0
    if abdeckung < 0.6:
        befunde.append(Befund(
            "UNTERTITEL", False,
            f"Short {num}: Untertitel enden bei {letzte:.1f}s von {dauer:.1f}s "
            f"({abdeckung:.0%} Abdeckung)", stelle=ass))

    # Ins Bild sehen: an drei Stellen, an denen laut ASS Text stehen muss.
    proben = [letzte * f for f in (0.25, 0.5, 0.8)]
    helligkeiten = [_caption_sichtbar(video, t) for t in proben]
    hell = max(helligkeiten)
    if hell < 0:
        befunde.append(Befund("UNTERTITEL", False,
                              f"Short {num}: Helligkeit nicht messbar "
                              f"(ffmpeg lieferte keinen Wert)", stelle=video))
    elif hell < 200:
        befunde.append(Befund(
            "UNTERTITEL", False,
            f"Short {num}: im Untertitel-Band keine Schrift erkennbar "
            f"(Spitzenhelligkeit {hell}, erwartet >=200)",
            stelle=(f"{video}\n                 {zeilen} ASS-Zeilen vorhanden, "
                    f"aber nicht ins Bild gebrannt.\n"
                    f"                 Geprueft bei "
                    f"{', '.join(f'{t:.1f}s' for t in proben)}")))
    else:
        befunde.append(Befund(
            "UNTERTITEL", True,
            f"Short {num}: Untertitel im Bild sichtbar "
            f"({zeilen} Zeilen, {abdeckung:.0%} Abdeckung, Helligkeit {hell})"))
    return befunde


# ───────────────────────────────────────────────────────── Lauf

def pruefe_short(serie, num):
    skript_pfad, skript_text = finde_skript(serie, num)
    words_pfad, words = finde_words(serie, num)
    cfg_pfad, cfg = finde_config(serie, num)
    return [
        pruefe_herkunft(serie, num, skript_pfad, skript_text),
        pruefe_captions(num, skript_text, words_pfad, words),
        pruefe_bewegung(num, cfg_pfad, cfg),
        pruefe_ton(num, cfg_pfad, cfg),
    ]


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("serie", help="Serien-Ordner, z. B. prosperi")
    ap.add_argument("--short", help="nur diesen Short, z. B. 03")
    ap.add_argument("--json", action="store_true", help="maschinenlesbar")
    ap.add_argument("--nachher", action="store_true",
                    help="das FERTIGE Video pruefen statt der Absicht "
                         "(Untertitel im Bild, Laenge, Abdeckung)")
    a = ap.parse_args()

    serie = a.serie.rstrip("/")
    if not os.path.isdir(serie):
        serie2 = os.path.join(ROOT, serie)
        if not os.path.isdir(serie2):
            print(f"Serie '{a.serie}' nicht gefunden.", file=sys.stderr)
            return 2
        serie = serie2

    nums = [a.short] if a.short else shorts_einer_serie(serie)
    if not nums:
        print(f"Keine Shorts in '{serie}' gefunden.", file=sys.stderr)
        return 2

    pruefer = pruefe_render if a.nachher else pruefe_short
    alle = {n: pruefer(serie, n) for n in nums}
    verstoesse = [(n, b) for n, bs in alle.items() for b in bs
                  if not b.ok and b.hart]

    if a.json:
        print(json.dumps({
            "serie": serie, "blockiert": bool(verstoesse),
            "shorts": {n: [{"regel": b.regel, "ok": b.ok, "hart": b.hart,
                            "text": b.text, "stelle": b.stelle} for b in bs]
                       for n, bs in alle.items()},
        }, ensure_ascii=False, indent=1))
        return 1 if verstoesse else 0

    print("=" * 70)
    print(f"  KP-GATE {'NACHHER' if a.nachher else 'VORHER '} —  {serie}  ({len(nums)} Shorts)")
    print("=" * 70)
    for n in nums:
        print(f"\nShort {n}")
        for b in alle[n]:
            print(b)

    print("\n" + "=" * 70)
    if verstoesse:
        print(f"  BLOCKIERT — {len(verstoesse)} Regelverletzung(en) in "
              f"{len({n for n, _ in verstoesse})} Short(s).")
        print("  Kein Render, kein Upload, bis diese behoben sind.")
        print("=" * 70)
        return 1
    print("  GRUEN — alle Pruefungen bestanden.")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
