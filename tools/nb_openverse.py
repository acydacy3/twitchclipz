#!/usr/bin/env python3
"""Openverse CC-Bildsuche + Download. Nutzung: python3 nb_openverse.py "cave rescue rope" out_dir [n]

BEFUND 08.09.2026 (F-V9-R): Dieses Werkzeug hat monatelang NICHTS geliefert und
das nicht gesagt. Es legte die Datei als `ov_1.raw` ab; ImageMagick liest die
Endung `.raw` als Kamera-RAW (DNG) und bricht ab. Der Fehler wurde verschluckt,
die Zeile "Openverse: 0 Bilder" ging als Ergebnis durch, Exit-Code 0.
Zwei Lehren stecken hier drin, beide sind jetzt Code:
  1. Die Endung entscheidet, wie ImageMagick liest -> Endung aus der URL nehmen.
  2. Ein Werkzeug, das nichts liefert, meldet das mit Exit-Code != 0.
"""
import sys, json, subprocess, urllib.parse, pathlib, os

def search(q, n=5):
    u = ("https://api.openverse.org/v1/images/?format=json&license_type=commercial,modification"
         f"&page_size={n}&q={urllib.parse.quote(q)}")
    r = subprocess.run(["curl", "-s", "--max-time", "30",
                        "-A", "KatastrophenprotokollBot/1.0", u],
                       capture_output=True, text=True)
    try:
        return json.loads(r.stdout).get("results", [])
    except Exception:
        return []

def endung(url):
    e = os.path.splitext(urllib.parse.urlparse(url).path)[1].lower()
    return e if e in (".jpg", ".jpeg", ".png", ".webp", ".gif", ".tif", ".tiff") else ".jpg"

def hole(q, out, n=5, groesse="1600x2848"):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    got = 0
    quellen = []
    for r in search(q, n * 3):
        if got >= n:
            break
        url = r.get("url")
        if not url:
            continue
        raw = out / f"_lade{endung(url)}"
        subprocess.run(["curl", "-sL", "--max-time", "40", "-o", str(raw), url])
        if not raw.exists() or raw.stat().st_size < 5000:
            raw.unlink(missing_ok=True)
            continue
        o = out / f"ov_{got+1:02d}.jpg"
        rr = subprocess.run(["convert", str(raw), "-resize", f"{groesse}^",
                             "-gravity", "center", "-extent", groesse,
                             "-quality", "92", str(o)], capture_output=True, text=True)
        raw.unlink(missing_ok=True)
        if rr.returncode == 0 and o.exists():
            got += 1
            quellen.append({"datei": o.name, "titel": r.get("title", ""),
                            "lizenz": f"{r.get('license','')} {r.get('license_version','')}".strip(),
                            "urheber": r.get("creator", ""), "quelle": r.get("foreign_landing_url", ""),
                            "suchbegriff": q})
            print(f"{o.name} <- {r.get('title','')[:44]} [{quellen[-1]['lizenz']}] {r.get('creator','')}")
        else:
            print(f"  uebersprungen ({url.rsplit('/',1)[-1]}): {rr.stderr.strip().splitlines()[-1] if rr.stderr else 'Download leer'}")
    if quellen:
        hp = out / "HERKUNFT.json"
        alt = json.load(open(hp, encoding="utf-8")) if hp.exists() else []
        json.dump(alt + quellen, open(hp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return got

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    q = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "."
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 5
    groesse = sys.argv[4] if len(sys.argv) > 4 else "1600x2848"
    got = hole(q, out, n, groesse)
    print(f"Openverse: {got} Bilder")
    if got == 0:
        raise SystemExit(f"KEIN Bild fuer '{q}' geladen. Das ist ein Fehler, kein Ergebnis.")
