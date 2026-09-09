#!/usr/bin/env python3
"""kp.py — der Ablauf. Sagt, was als Naechstes dran ist, und fuehrt es aus.

WARUM ES DAS GIBT
-----------------
Bis zum 07.09.2026 stand der Produktionsablauf als Checkliste in einer
Markdown-Datei. Eine Checkliste kann uebersprungen werden, und sie wurde
uebersprungen — sieben Tage lang entstand kein Video, waehrend der
Sitzungsbericht „System laeuft" meldete. Der Nutzer musste jeden Schritt
selbst ansprechen.

Dieses Skript liest den TATSAECHLICHEN Zustand auf der Platte und in der
YouTube-API und leitet daraus ab, welcher Schritt offen ist. Es glaubt keiner
Notiz. Damit steht der naechste Schritt bei jedem Sitzungsstart von selbst da,
in einem frischen Container genauso wie in einer laufenden Sitzung.

DIE REIHENFOLGE (nicht verhandelbar, jeder Schritt prueft seinen Vorgaenger)
---------------------------------------------------------------------------
    1 MESSEN     Tages-Snapshot + AVP%   -> Entscheidungen auf frischen Zahlen
    2 SKRIPT     Nutzer-Skript aufnehmen -> Herkunft per Pruefsumme belegt
    3 VORHER     Gate gegen Skript/Konfig-> Bewegung, Captions, Titel, Ton
    4 RENDERN    Shorts bauen
    5 ANIMATION  Szenen messen           -> Rand, Fuellgrad
    6 NACHHER    Gate am fertigen Video  -> Untertitel wirklich im Bild
    7 AUSLIEFERN hochladen / austauschen
    8 LONGFORM   Langvideo je Serie

    python3 tools/kp.py status            Gesamtstand + naechster Schritt
    python3 tools/kp.py status <serie>    nur diese Serie
    python3 tools/kp.py schritte          die Reihenfolge mit Befehlen
"""

import argparse
import datetime as dt
import glob
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kp_regeln as R

ROOT = R.ROOT

# Ordner, die keine Produktionsserien sind
KEIN_SERIENORDNER = {"tools", "media", ".git", ".claude", "YouTube-Knowledge",
                     "__pycache__", "qc_frames"}


def serien():
    out = []
    for name in sorted(os.listdir(ROOT)):
        p = os.path.join(ROOT, name)
        if not os.path.isdir(p) or name.startswith(".") or name in KEIN_SERIENORDNER:
            continue
        # Eine Serie erkennt man an Voiceover oder Skript
        if os.path.isdir(os.path.join(p, "voiceover")) or \
           os.path.isdir(os.path.join(p, "skript")) or \
           os.path.isdir(os.path.join(p, "skripte")):
            out.append(name)
    return out


def gate(serie, nachher=False, system=False):
    cmd = [sys.executable, os.path.join(ROOT, "tools", "kp_gate.py")]
    cmd += ["--system"] if system else [serie]
    if nachher:
        cmd.append("--nachher")
    cmd.append("--json")
    r = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    try:
        return json.loads(r.stdout), r.returncode
    except Exception:
        return None, r.returncode


def zustand_serie(name):
    """Welcher Schritt ist offen? Aus Dateien und API, nicht aus Notizen."""
    p = os.path.join(ROOT, name)
    z = {"serie": name}

    nums = sorted({os.path.basename(f).split("_")[1].split(".")[0]
                   for f in glob.glob(os.path.join(p, "voiceover", "short_*.mp3"))})
    z["shorts"] = len(nums)

    # 2 SKRIPT
    man = os.path.join(p, "skript", "QUELLE.json")
    if os.path.exists(man):
        eintraege = json.load(open(man, encoding="utf-8")).get("shorts", {})
        z["skript"] = len(eintraege) >= len(nums) and len(nums) > 0
        z["skript_n"] = len(eintraege)
    else:
        z["skript"], z["skript_n"] = False, 0

    # 3 VORHER
    _, rc = gate(name)
    z["vorher"] = rc == 0

    # 4 RENDERN
    gerendert = glob.glob(os.path.join(p, "render", "short_*.mp4"))
    z["gerendert"] = len(gerendert)

    # 6 NACHHER — nur sinnvoll, wenn ueberhaupt gerendert wurde
    if gerendert:
        _, rc2 = gate(name, nachher=True)
        z["nachher"] = rc2 == 0
    else:
        z["nachher"] = None

    # 7 AUSLIEFERN
    log = os.path.join(p, "upload_log.json")
    alt = os.path.join(p, "uploaded.json")
    hoch = 0
    for f in (log, alt):
        if os.path.exists(f):
            d = json.load(open(f, encoding="utf-8"))
            hoch = max(hoch, sum(1 for v in d.values()
                                 if (v.get("uploaded") if isinstance(v, dict) else bool(v))))
    z["hochgeladen"] = hoch

    # 7b OFFENER AUSTAUSCH — ein neu gerendertes Video, das noch nicht drueben ist
    # Ohne diesen Zustand haenge der Rest an einer Erinnerung. Genau so gehen
    # Dinge verloren: das YouTube-Tageslimit brach am 07.09. einen Austausch
    # nach dem fuenften Short ab, und nichts im System wusste davon.
    z["austausch_offen"] = []
    for f in (log, alt):
        if os.path.exists(f):
            d = json.load(open(f, encoding="utf-8"))
            z["austausch_offen"] = sorted(
                k for k, v in d.items()
                if isinstance(v, dict) and v.get("austausch_offen"))
            if z["austausch_offen"]:
                break

    # 8 LONGFORM — gebaut und hochgeladen sind zwei verschiedene Dinge.
    # Bis 08.09. galt eine Serie als fertig, sobald long.mp4 auf Platte lag;
    # das Video konnte terminlos herumliegen und niemand erfuhr davon.
    meta = os.path.join(p, "metadata.json")
    z["longform_meta"] = False
    z["longform"] = False          # gebaut
    z["longform_hoch"] = False     # hochgeladen
    if os.path.exists(meta):
        m = json.load(open(meta, encoding="utf-8"))
        z["longform_meta"] = bool(m.get("longform"))
        z["longform"] = z["longform_meta"] and \
            os.path.exists(os.path.join(p, "render", "long.mp4"))
    log = os.path.join(p, "upload_log.json")
    if os.path.exists(log):
        try:
            lf = json.load(open(log, encoding="utf-8")).get("longform")
            z["longform_hoch"] = bool(isinstance(lf, dict) and lf.get("video_id"))
        except Exception:
            pass
    # Ohne belegtes Skript ist der Shorts-Weg zu, der Longform-Weg aber offen:
    # nb_lang.py --ohne-captions brennt keinen Text ein, R30 misst das nach.
    z["ohne_captions"] = z["skript_n"] == 0 and z["shorts"] > 0
    return z


def naechster_schritt(z):
    """Genau EINE Handlung — die erste offene in der Reihenfolge."""
    n = z["serie"]
    if z["shorts"] == 0:
        return None, "keine Voiceover-Dateien — wartet auf Material"
    if not z["skript"]:
        # Kein einziges belegtes Skript: die Shorts warten auf Material vom
        # Nutzer, das Langvideo nicht. Es kommt ohne eingebrannte Untertitel
        # aus -- und R30 misst am fertigen Video nach, dass wirklich keiner
        # drin ist. Vorher schickte diese Zeile die naechste Sitzung auf die
        # Suche nach einem Skript, das es nicht gibt, und das Langvideo blieb
        # ungebaut liegen.
        if z.get("ohne_captions") and not z["longform"] and z.get("longform_meta"):
            return ("8 LONGFORM",
                    f"kein belegtes Skript ({z['skript_n']}/{z['shorts']}) — "
                    f"Langvideo geht trotzdem, ohne Untertitel: "
                    f"python3 nb_lang.py {n} --ohne-captions")
        if z.get("ohne_captions") and z["longform"] and not z["longform_hoch"]:
            return ("8 LONGFORM",
                    f"Langvideo gebaut, noch nicht hochgeladen: "
                    f"python3 tools/kp_longform.py {n} --wirklich")
        return ("2 SKRIPT",
                f"Skript-Herkunft belegen: python3 tools/kp_skript.py {n} "
                f"--aus <datei-vom-nutzer>   ({z['skript_n']}/{z['shorts']} belegt)")
    if not z["vorher"]:
        return ("3 VORHER",
                f"Gate ist rot: python3 tools/kp_gate.py {n}   "
                f"(Verstoesse beheben, dann weiter)")
    if z["gerendert"] < z["shorts"]:
        return ("4 RENDERN",
                f"{z['gerendert']}/{z['shorts']} gerendert: python3 {n}/nb_build.py")
    if z["nachher"] is False:
        return ("6 NACHHER",
                f"Fertiges Material faellt durch: python3 tools/kp_gate.py {n} --nachher")
    if z["hochgeladen"] < z["shorts"]:
        return ("7 AUSLIEFERN",
                f"{z['hochgeladen']}/{z['shorts']} hochgeladen: python3 {n}/nb_upload.py")
    if z.get("austausch_offen"):
        offen = ",".join(z["austausch_offen"])
        return ("7 AUSTAUSCH",
                f"{len(z['austausch_offen'])} Short(s) neu gerendert, aber noch nicht "
                f"drueben ({offen}): python3 tools/kp_ersetzen.py {n} "
                f"--shorts {offen} --wirklich")
    if not z["longform"]:
        return ("8 LONGFORM",
                f"kein Langvideo: python3 nb_lang.py {n}   "
                f"(6 von 8 Serien haben bis heute keines)")
    if not z["longform_hoch"]:
        return ("8 LONGFORM",
                f"Langvideo gebaut, noch nicht hochgeladen: "
                f"python3 tools/kp_longform.py {n} --wirklich")
    return None, "fertig"


SCHRITTE = [
    ("1 MESSEN", "python3 tools/kp_metrik.py --snapshot",
     "Tages-Snapshot + AVP%. Ein fehlender Tag ist dauerhaft verloren."),
    ("2 SKRIPT", "python3 tools/kp_skript.py <serie> --aus <datei>",
     "Herkunft per Pruefsumme belegen. Ein Ordnername beweist nichts."),
    ("3 VORHER", "python3 tools/kp_gate.py <serie>",
     "Bewegung, Captions gegen Skript, Titel, Ton, Fremdmaterial."),
    ("4 RENDERN", "python3 <serie>/nb_build.py",
     "Der Riegel laesst das nur durch, wenn Schritt 3 gruen ist."),
    ("5 ANIMATION", "python3 tools/kp_anim_qc.py",
     "Randabstand und Fuellgrad messen, nicht begutachten."),
    ("6 NACHHER", "python3 tools/kp_gate.py <serie> --nachher",
     "Am fertigen Video: stehen die Untertitel wirklich im Bild?"),
    ("7 AUSLIEFERN", "python3 <serie>/nb_upload.py  /  tools/kp_ersetzen.py",
     "Austausch: Gate -> hochladen -> bestaetigen -> erst dann loeschen."),
    ("8 LONGFORM", "python3 nb_lang.py <serie>",
     "Langvideo baut Watch Time und Suchtraffic."),
]


def status(nur=None, kurz=False):
    zeilen = []
    z = zeilen.append

    g, ges = R.deckung()
    sys_befunde = [regel["pruefung"](None) for regel in R.regeln_der_phase("dauerhaft")]
    sys_offen = [b for b in sys_befunde if not b.ok]

    z("=" * 74)
    z(f"  KP-ABLAUF  —  {dt.date.today().isoformat()}  ·  "
      f"{g}/{ges} Regeln erzwungen")
    z("=" * 74)

    for b in sys_befunde:
        marke = "OK  " if b.ok else "TUN "
        z(f"  [{marke}] {b.titel:<14} {b.text}")

    offene = []
    for name in (nur or serien()):
        zu = zustand_serie(name)
        schritt, text = naechster_schritt(zu)
        fertig = [
            f"Skript {zu['skript_n']}/{zu['shorts']}",
            f"Gate {'gruen' if zu['vorher'] else 'ROT'}",
            f"Render {zu['gerendert']}/{zu['shorts']}",
            f"Upload {zu['hochgeladen']}/{zu['shorts']}",
            "Longform " + ("hoch" if zu.get("longform_hoch")
                           else ("gebaut" if zu["longform"] else "nein")),
        ] + ([f"AUSTAUSCH OFFEN: {','.join(zu['austausch_offen'])}"]
             if zu.get("austausch_offen") else []) + [
        ]
        z("")
        z(f"  {name}")
        z(f"    {' · '.join(fertig)}")
        if schritt:
            z(f"    -> {schritt}: {text}")
            offene.append((name, schritt, text))
        else:
            z(f"    -> {text}")

    z("")
    z("-" * 74)
    if sys_offen:
        z(f"  ZUERST (Systemzustand): {sys_offen[0].titel} — {sys_offen[0].text}")
        if sys_offen[0].stelle:
            z(f"    {sys_offen[0].stelle.splitlines()[0]}")
    if offene:
        name, schritt, text = offene[0]
        z(f"  NAECHSTER SCHRITT: [{name}] {schritt}")
        z(f"    {text}")
    elif not sys_offen:
        z("  Nichts offen. Neue Geschichte: Nutzer liefert das Skript, dann Schritt 2.")
    z("=" * 74)
    return "\n".join(zeilen), bool(offene or sys_offen)


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("befehl", nargs="?", default="status",
                    choices=["status", "schritte"])
    ap.add_argument("serie", nargs="?")
    a = ap.parse_args()

    if a.befehl == "schritte":
        print("=" * 74)
        print("  DIE REIHENFOLGE — jeder Schritt prueft seinen Vorgaenger")
        print("=" * 74)
        for name, befehl, warum in SCHRITTE:
            print(f"\n  {name}")
            print(f"    {befehl}")
            print(f"    {warum}")
        print("\n" + "=" * 74)
        return 0

    text, offen = status([a.serie] if a.serie else None)
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
