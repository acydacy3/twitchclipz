#!/usr/bin/env python3
"""nb_commons.py — Bilder aus Wikimedia-Commons-KATEGORIEN holen.

WARUM ES DIESES WERKZEUG GIBT
-----------------------------
CLAUDE.md Kernregel 8 verlangt seit Wochen "Broll autonom sourcing:
Commons-Kategorien + Openverse". Fuer Openverse gab es ein Werkzeug (kaputt,
s. F-V9-R), fuer Commons-Kategorien gar keins. Eine Regel ohne Werkzeug ist
dasselbe wie eine Regel ohne Pruefpunkt: sie wird nicht befolgt. Ergebnis waren
themenfremde Bilder in fertigen Videos (Schrein, Soldaten, Zeltlager im
Nutty-Putty-Langvideo).

Freitextsuche auf Commons liefert vor allem eingescannte Buecher. KATEGORIEN
liefern Fotos. Deshalb geht dieses Werkzeug ueber Kategorien.

    python3 tools/nb_commons.py "Cave rescue" out_dir [n] [breite x hoehe]
    python3 tools/nb_commons.py --suche-kategorie "cave rescue"

Jedes geladene Bild wird in out_dir/HERKUNFT.json mit Lizenz, Urheber und
Commons-Seite eingetragen — ohne diesen Eintrag ist ein Bild nicht belegt.
"""
import json
import os
import pathlib
import subprocess
import sys
import time
import urllib.parse

API = "https://commons.wikimedia.org/w/api.php"
UA = "KatastrophenprotokollBot/1.0 (acydacy3@gmail.com)"
BILD = (".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp")


def api(**p):
    """Commons-API mit Wartezeit und Wiederholung.

    Commons drosselt (HTTP-Text statt JSON: "You are making too many requests").
    Die alte Fassung verschluckte das mit `except: return {}` und meldete
    stattdessen "0 Bilder" — derselbe Fehler wie F-V9-R: ein Werkzeug, das
    schweigend nichts liefert. Deshalb: warten, wiederholen, und wenn es
    endgueltig nicht geht, den Grund sagen.
    """
    p.setdefault("format", "json")
    p.setdefault("action", "query")
    url = API + "?" + urllib.parse.urlencode(p)
    letzte = ""
    for versuch in range(4):
        if versuch:
            time.sleep(2 ** versuch)          # 2 s, 4 s, 8 s
        r = subprocess.run(["curl", "-s", "--max-time", "40",
                            "-H", f"User-Agent: {UA}", url],
                           capture_output=True, text=True)
        try:
            return json.loads(r.stdout)
        except Exception:
            letzte = (r.stdout or r.stderr or "leere Antwort").strip().splitlines()[0][:120]
    print(f"  Commons antwortet nicht als JSON: {letzte}", file=sys.stderr)
    return {}


def kategorien(begriff, n=12):
    d = api(list="search", srnamespace=14, srsearch=begriff, srlimit=n)
    return [x["title"][9:] for x in d.get("query", {}).get("search", [])]


def dateien(kategorie, n=20, tiefe=1):
    """Dateien der Kategorie, bei Bedarf eine Unterkategorie-Ebene tiefer."""
    raus, gesehen = [], set()

    def sammeln(kat, limit):
        d = api(generator="categorymembers", gcmtitle=f"Category:{kat}",
                gcmtype="file", gcmlimit=limit, prop="imageinfo",
                iiprop="url|extmetadata", iiurlwidth=2000)
        for p in (d.get("query", {}) or {}).get("pages", {}).values():
            ii = (p.get("imageinfo") or [{}])[0]
            u = ii.get("thumburl") or ii.get("url")
            if not u or os.path.splitext(urllib.parse.urlparse(ii.get("url", "")).path)[1].lower() not in BILD:
                continue
            if p["title"] in gesehen:
                continue
            gesehen.add(p["title"])
            m = ii.get("extmetadata", {})
            raus.append({
                "titel": p["title"][5:],
                "url": u,
                "lizenz": (m.get("LicenseShortName") or {}).get("value", ""),
                "urheber": (m.get("Artist") or {}).get("value", "")[:120],
                "seite": f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(p['title'])}",
                "kategorie": kat,
            })

    sammeln(kategorie, n)
    if len(raus) < n and tiefe > 0:
        d = api(list="categorymembers", cmtitle=f"Category:{kategorie}",
                cmtype="subcat", cmlimit=8)
        for s in d.get("query", {}).get("categorymembers", []):
            if len(raus) >= n:
                break
            sammeln(s["title"][9:], n - len(raus))
    return raus[:n]


def hole(kategorie, out, n=6, groesse="1600x2848"):
    out = pathlib.Path(out)
    out.mkdir(parents=True, exist_ok=True)
    vorhanden = len(list(out.glob("cm_*.jpg")))
    got, quellen = 0, []
    for r in dateien(kategorie, n * 2):
        if got >= n:
            break
        endung = os.path.splitext(urllib.parse.urlparse(r["url"]).path)[1].lower()
        roh = out / ("_lade" + (endung if endung in BILD else ".jpg"))
        subprocess.run(["curl", "-sL", "--max-time", "60", "-H", f"User-Agent: {UA}",
                        "-o", str(roh), r["url"]])
        if not roh.exists() or roh.stat().st_size < 8000:
            roh.unlink(missing_ok=True)
            continue
        ziel = out / f"cm_{vorhanden + got + 1:02d}.jpg"
        rr = subprocess.run(["convert", str(roh), "-resize", f"{groesse}^",
                             "-gravity", "center", "-extent", groesse,
                             "-quality", "92", str(ziel)], capture_output=True, text=True)
        roh.unlink(missing_ok=True)
        if rr.returncode == 0 and ziel.exists():
            got += 1
            r["datei"] = ziel.name
            quellen.append(r)
            print(f"{ziel.name} <- {r['titel'][:52]}  [{r['lizenz']}]")
        else:
            print(f"  uebersprungen: {r['titel'][:52]}")
    if quellen:
        hp = out / "HERKUNFT.json"
        alt = json.load(open(hp, encoding="utf-8")) if hp.exists() else []
        json.dump(alt + quellen, open(hp, "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)
    return got


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    if sys.argv[1] == "--suche-kategorie":
        for k in kategorien(sys.argv[2]):
            print(" ", k)
        raise SystemExit(0)
    kat = sys.argv[1]
    out = sys.argv[2] if len(sys.argv) > 2 else "."
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    groesse = sys.argv[4] if len(sys.argv) > 4 else "1600x2848"
    got = hole(kat, out, n, groesse)
    print(f"Commons '{kat}': {got} Bilder")
    if got == 0:
        raise SystemExit(f"KEIN Bild aus Kategorie '{kat}'. Das ist ein Fehler, kein Ergebnis.")
