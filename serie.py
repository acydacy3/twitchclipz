"""
Der komplette Serienplan fuer Video 2 (San José) - 11 Shorts.

    python3 serie.py            # alle bauen
    python3 serie.py 3 7        # nur Short 3 und 7

Grundsaetze, die hier drinstecken:
  - Alle Schnittgrenzen liegen auf echten Sprechpausen (>= 0,42 s).
    Kein Satz wird zerschnitten.
  - Jeder Short hat einen eigenen Bogen und endet auf Aufloesung oder
    Cliffhanger - nicht dort, wo das Bildmaterial ausgeht.
  - Einstellung 1 ist immer ein DETAIL, nie eine Totale, und dauert
    rund 2-3 s. Erster harter Schnitt spaetestens bei Sekunde 3.
  - Der Aufhaenger-Text sagt etwas ANDERES als die Stimme. Doppelte
    Information verschenkt einen Kanal.
  - Die Tonart wechselt, damit nicht elf Shorts gleich klingen.

Die Zeit 3.06 ist der Schnittpunkt: davor steht auf der Tonspur
"Das Wunder von San José. Kurzfassung." - genau die Titelansage, die
bei Video 1 die Haltequote zerstoert hat.
"""
import json
import os
import subprocess
import sys

FONT = "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Black.ttf"
B = "bilder/bild{:02d}.jpg"


def s(img, bis, cx, cy, z0, z1=None, px=0.0, py=0.0, drift=14, note=""):
    """Eine Einstellung. 'bis' ist die absolute Zeit im Voiceover."""
    return {"img": B.format(img), "bis": bis, "cx": cx, "cy": cy,
            "z0": z0, "z1": z1 if z1 is not None else z0 * 1.10,
            "px": px, "py": py, "drift": drift, "_": note}


PLAN = [
  # ---------------------------------------------------------------- 1
  dict(nr=1, titel="Der Auftakt", von=3.06, bis=28.71, tonart="D",
       hook="KEINER SOLLTE ÜBERLEBEN",
       shots=[
         s(1,  7.74, 0.36, 0.79, 2.50, 2.62, drift=9,
           note="Detail: die Kumpel laufen in den Stollen"),
         s(1, 13.50, 0.50, 0.50, 1.02, 1.18, py=0.30, drift=17,
           note="Totale: Mine in der Atacama"),
         s(1, 21.57, 0.70, 0.33, 1.85, 2.00, drift=13,
           note="Foerdergebaeude und Muldenkipper am Hang"),
         s(1, 28.71, 0.36, 0.70, 1.55, 1.72, drift=12,
           note="Das Stollenmaul - hier faehrt Urzúa ein"),
       ]),
  # ---------------------------------------------------------------- 2
  dict(nr=2, titel="Der Einsturz", von=35.13, bis=61.83, tonart="A",
       hook="EINE NORMALE SCHICHT",
       shots=[
         s(1, 39.27, 0.36, 0.79, 2.40, 2.52, drift=9,
           note="Detail: Helme und Warnwesten"),
         s(2, 47.00, 0.30, 0.62, 2.10, 2.28, drift=15,
           note="Das Gesicht: der Berg erzittert"),
         s(2, 52.68, 0.48, 0.28, 1.30, 1.55, drift=18,
           note="Die Platte loest sich"),
         s(2, 57.93, 0.50, 0.42, 1.05, 1.30, py=-0.25, drift=16,
           note="Sturz und Staubwolke, Fahrt nach oben"),
         s(2, 61.83, 0.68, 0.77, 2.05, 2.20, drift=13,
           note="Helmlampen im Staub - der Ausgang ist zu"),
       ]),
  # ---------------------------------------------------------------- 3
  dict(nr=3, titel="Eingeschlossen", von=62.31, bis=90.30, tonart="E",
       hook="KEIN AUSGANG",
       shots=[
         s(2, 66.00, 0.30, 0.63, 2.20, 2.34, drift=9,
           note="Detail: das aufgerissene Gesicht"),
         s(2, 74.00, 0.65, 0.75, 1.75, 1.92, drift=15,
           note="Lampen suchen einen Fluchtweg"),
         s(3, 82.00, 0.50, 0.42, 1.55, 1.72, drift=14,
           note="Die Gruppe im Schutzraum"),
         s(3, 90.30, 0.62, 0.70, 2.30, 2.15, drift=11,
           note="Zwei Gesichter nah, Rueckzug"),
       ]),
  # ---------------------------------------------------------------- 4
  dict(nr=4, titel="Der Anführer", von=90.78, bis=110.73, tonart="D",
       hook="EINER MUSSTE FÜHREN",
       shots=[
         s(3, 94.20, 0.30, 0.73, 2.60, 2.72, drift=9,
           note="Detail: Urzúas Gesicht"),
         s(3, 102.00, 0.50, 0.45, 1.50, 1.68, drift=15,
           note="Er spricht zu den anderen"),
         s(3, 110.73, 0.42, 0.13, 2.00, 1.85, drift=12,
           note="Die einzelne Lampe an der Decke"),
       ]),
  # ---------------------------------------------------------------- 5
  dict(nr=5, titel="Die Rationierung", von=111.36, bis=133.41, tonart="G",
       hook="VORRAT FÜR ZWEI TAGE",
       pfeil=dict(w=220, x=690, y=520),
       shots=[
         s(4, 114.80, 0.52, 0.47, 2.45, 2.58, drift=9,
           note="Detail: die Reihe Loeffel"),
         s(4, 125.31, 0.50, 0.14, 1.70, 1.88, drift=14,
           note="Die Lampe und die zusehenden Gesichter"),
         s(4, 133.41, 0.55, 0.34, 2.05, 2.22, drift=12,
           note="Die Hand teilt den Fisch aus der Dose"),
       ]),
  # ---------------------------------------------------------------- 6
  dict(nr=6, titel="17 Tage", von=133.86, bis=162.69, tonart="C",
       hook="KEIN TRINKWASSER",
       shots=[
         s(4, 137.50, 0.75, 0.62, 2.55, 2.68, drift=9,
           note="Detail: halber Keks und Glas Milch"),
         s(4, 146.00, 0.29, 0.75, 1.95, 2.12, drift=13,
           note="Das Gesicht und die offenen Haende"),
         s(5, 154.53, 0.50, 0.60, 1.35, 1.55, drift=16,
           note="Der Schutzraum wird still"),
         s(5, 162.69, 0.72, 0.55, 2.20, 2.05, drift=11,
           note="Die Hand auf der Schulter"),
       ]),
  # ---------------------------------------------------------------- 7
  dict(nr=7, titel="Blind bohren", von=163.17, bis=186.09, tonart="A",
       hook="NIEMAND WUSSTE WO",
       shots=[
         s(5, 166.60, 0.26, 0.82, 2.50, 2.62, drift=9,
           note="Detail: die zusammengesunkene Gestalt"),
         s(6, 174.00, 0.55, 0.22, 1.35, 1.55, py=-0.30, drift=17,
           note="Der Bohrturm gegen den Sternenhimmel"),
         s(6, 180.87, 0.55, 0.63, 1.85, 2.02, drift=14,
           note="Ingenieure am Bohrkopf im Flutlicht"),
         s(6, 186.09, 0.18, 0.74, 2.40, 2.25, drift=11,
           note="Das Gesicht - niemand weiss, ob sie leben"),
       ]),
  # ---------------------------------------------------------------- 8
  dict(nr=8, titel="Sie gingen nicht nach Hause", von=186.69, bis=205.08,
       tonart="D", hook="SIE GINGEN NICHT HEIM",
       pfeil=dict(w=200, x=170, y=1030),
       shots=[
         s(7, 190.20, 0.62, 0.86, 2.45, 2.58, drift=9,
           note="Detail: das Maedchen mit der Kerze"),
         s(7, 196.14, 0.50, 0.36, 1.55, 1.75, drift=15,
           note="Das Zeltlager und die Feuer"),
         s(7, 200.46, 0.50, 0.11, 1.90, 2.05, drift=13,
           note="Presseautos und Satellitenschuesseln"),
         s(7, 205.08, 0.31, 0.71, 2.15, 2.30, drift=12,
           note="Haende am Maschendrahtzaun"),
       ]),
  # ---------------------------------------------------------------- 9
  dict(nr=9, titel="Der Zettel", von=200.66, bis=233.61, tonart="D",
       hook="SIE GALTEN ALS TOT",
       pfeil=dict(w=230, x=690, y=540),
       shots=[
         s(8, 202.86, 0.50, 0.79, 2.60, 2.72, drift=10,
           note="Detail: der Zettel in den Haenden"),
         s(8, 210.99, 0.50, 0.30, 1.02, 1.20, py=0.35, drift=16,
           note="Der Durchbruch"),
         s(8, 219.69, 0.42, 0.76, 1.70, 1.88, drift=14,
           note="Der Mann bindet den Zettel ans Rohr"),
         s(8, 226.41, 0.28, 0.64, 2.55, 2.38, drift=12,
           note="Gesicht nah - der Zettel wird vorgelesen"),
         s(8, 233.61, 0.46, 0.46, 2.15, 2.34, drift=15,
           note="Die jubelnden Kumpel: sie leben"),
       ]),
  # --------------------------------------------------------------- 10
  dict(nr=10, titel="Die Welt schaut zu", von=233.94, bis=267.84,
       tonart="F", hook="DAS GAB ES NOCH NIE",
       shots=[
         s(9, 237.00, 0.50, 0.47, 2.40, 2.52, drift=9,
           note="Detail: die Kapsel im Bohrloch"),
         s(9, 247.50, 0.50, 0.13, 1.75, 1.92, drift=14,
           note="Maschinen und Flutlicht an der Oberflaeche"),
         s(9, 256.00, 0.50, 0.86, 1.80, 1.98, drift=13,
           note="Die wartenden Bergleute in der Kaverne"),
         s(7, 262.00, 0.50, 0.11, 1.85, 2.02, drift=14,
           note="Die Weltpresse vor der Mine"),
         s(7, 267.84, 0.50, 0.36, 1.45, 1.62, drift=15,
           note="Das Camp - Pfarrer, Musik, ein Clown"),
       ]),
  # --------------------------------------------------------------- 11
  dict(nr=11, titel="Die Rettung", von=268.47, bis=306.81, tonart="D",
       hook="70 ZENTIMETER",
       pfeil=dict(w=220, x=660, y=560),
       shots=[
         s(6, 271.50, 0.55, 0.63, 2.35, 2.48, drift=10,
           note="Detail: der Bohrkopf im Flutlicht"),
         s(6, 284.73, 0.55, 0.22, 1.30, 1.52, py=-0.28, drift=17,
           note="Der Turm gegen den Sternenhimmel"),
         s(10, 291.63, 0.50, 0.12, 1.60, 1.78, drift=14,
           note="Der Windenturm bei Nacht"),
         s(10, 299.00, 0.45, 0.45, 1.90, 2.08, drift=12,
           note="Die Kapsel - der Mann steigt aus"),
         s(10, 306.81, 0.55, 0.85, 1.75, 1.92, drift=13,
           note="Die Menge und die 33 Fahnen"),
       ]),
]


def cfg_bauen(p):
    von, bis = p["von"], p["bis"]
    shots = []
    t = von
    for sh in p["shots"]:
        shots.append({k: v for k, v in sh.items() if k != "bis"} |
                     {"start": t - von, "end": sh["bis"] - von})
        t = sh["bis"]
    return {
        "out": f"shorts/short{p['nr']:02d}_{p['titel'].split()[0].lower()}.mp4",
        "audio": "voiceover.mp3",
        "words": "words_fixed.json",
        "start": von, "end": bis,
        "teil": f"TEIL {p['nr']}",
        "font_black": FONT,
        "hook": {"text": p["hook"], "y": 250},
        "hook_until": 3.0,
        "musik": {"tonart": p["tonart"], "intensitaet": 1.0, "db": -21},
        **({"arrow": {"img": "arrow.png", **p["pfeil"]}} if p.get("pfeil") else {}),
        "shots": shots,
        "tmp": f"_tmp/s{p['nr']:02d}",
    }


if __name__ == "__main__":
    os.makedirs("shorts", exist_ok=True)
    os.makedirs("konfig", exist_ok=True)
    nur = {int(a) for a in sys.argv[1:]} if len(sys.argv) > 1 else None
    for p in PLAN:
        if nur and p["nr"] not in nur:
            continue
        c = cfg_bauen(p)
        kp = f"konfig/short{p['nr']:02d}.json"
        json.dump(c, open(kp, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=2)
        laenge = p["bis"] - p["von"]
        print(f"\n=== Short {p['nr']:2d}  {p['titel']:<30} "
              f"{laenge:5.1f}s  {len(p['shots'])} Einstellungen ===")
        subprocess.run([sys.executable, "short.py", kp], check=True)
