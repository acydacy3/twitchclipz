#!/usr/bin/env python3
"""videoblick.py — damit Claude ein Video ANSEHEN kann.

Das ist der Ersatz fuer "Video-Use" aus der Werkzeugliste. Selbst gebaut,
weil es unter dem Namen kein eindeutiges Paket gibt, sondern ein halbes
Dutzend fremder Repos mit gleichem Namen — und blind installieren ist der
Weg, auf dem man sich Schadcode einfaengt.

Was es tut: zerlegt ein Video in Einzelbilder, die Claude dann mit dem
Read-Werkzeug wirklich anschauen kann. Zwei Betriebsarten:

  gleichmaessig  alle N Sekunden ein Bild      (Standard, N=3)
  szenen         nur bei Szenenwechseln        (findet die Schnitte)

BENUTZUNG (Claude fuehrt das aus, nicht der Nutzer):

  python3 werkzeuge/videoblick.py video.mp4
  python3 werkzeuge/videoblick.py video.mp4 --jede 5
  python3 werkzeuge/videoblick.py video.mp4 --szenen
  python3 werkzeuge/videoblick.py video.mp4 --von 30 --bis 60

Die Bilder landen in einem Unterordner und werden am Ende aufgelistet.
"""
import argparse, subprocess, sys, json, os, shutil

def dauer(pfad):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "json", pfad], capture_output=True, text=True)
    try:
        return float(json.loads(r.stdout)["format"]["duration"])
    except Exception:
        return 0.0

def main():
    p = argparse.ArgumentParser(description="Video in ansehbare Einzelbilder zerlegen")
    p.add_argument("video")
    p.add_argument("--jede", type=float, default=3.0, help="alle N Sekunden ein Bild (Standard 3)")
    p.add_argument("--szenen", action="store_true", help="statt gleichmaessig: nur Szenenwechsel")
    p.add_argument("--schwelle", type=float, default=0.30, help="Empfindlichkeit der Szenenerkennung 0..1")
    p.add_argument("--von", type=float, default=None, help="Startsekunde")
    p.add_argument("--bis", type=float, default=None, help="Endsekunde")
    p.add_argument("--breite", type=int, default=768, help="Bildbreite (kleiner = weniger Kontext)")
    p.add_argument("--max", type=int, default=40, help="Hoechstzahl Bilder")
    p.add_argument("--ordner", default=None)
    a = p.parse_args()

    if not os.path.exists(a.video):
        sys.exit(f"Video nicht gefunden: {a.video}")
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg fehlt.")

    ziel = a.ordner or os.path.splitext(os.path.basename(a.video))[0] + "_blick"
    if os.path.isdir(ziel):
        shutil.rmtree(ziel)
    os.makedirs(ziel)

    laenge = dauer(a.video)
    cmd = ["ffmpeg", "-v", "error", "-y"]
    if a.von is not None:
        cmd += ["-ss", str(a.von)]
    cmd += ["-i", a.video]
    if a.bis is not None:
        cmd += ["-to", str(a.bis - (a.von or 0))]

    if a.szenen:
        filt = f"select='gt(scene,{a.schwelle})',scale={a.breite}:-2"
        cmd += ["-vf", filt, "-vsync", "vfr"]
    else:
        filt = f"fps=1/{a.jede},scale={a.breite}:-2"
        cmd += ["-vf", filt]

    cmd += ["-frames:v", str(a.max), "-q:v", "3", os.path.join(ziel, "bild_%03d.jpg")]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("ffmpeg-Fehler:\n" + r.stderr[:800])

    bilder = sorted(os.listdir(ziel))
    if not bilder:
        sys.exit("Keine Bilder erzeugt. Bei --szenen die --schwelle senken (z.B. 0.15).")

    print(f"Video:  {a.video}")
    print(f"Laenge: {laenge:.1f} s")
    print(f"Modus:  {'Szenenwechsel' if a.szenen else f'alle {a.jede} s'}")
    print(f"Bilder: {len(bilder)} in {ziel}/\n")
    for i, b in enumerate(bilder):
        if a.szenen:
            print(f"  {ziel}/{b}")
        else:
            t = (a.von or 0) + i * a.jede
            print(f"  {t:7.1f} s  {ziel}/{b}")
    print("\nJetzt diese Bilder mit dem Read-Werkzeug oeffnen, um das Video zu sehen.")

if __name__ == "__main__":
    main()
