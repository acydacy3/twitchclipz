#!/usr/bin/env python3
"""kp_metrik.py — Kanalzahlen, die nicht gefaellig sind.

Ersetzt den selbstvergebenen Autonomie-Score. Der Score kam aus
Autonomie-Log.md, wo Claude ihn selbst eintrug -- und er stieg von 48 auf 88,
waehrend die Videos immer weniger Zuschauer hielten. Eine Zahl, die man sich
selbst gibt, misst nichts.

Hier wird ausschliesslich gemessen, was YouTube liefert:

  AVP%          Welcher Anteil eines Shorts wird tatsaechlich gesehen?
                Die einzige Qualitaetszahl, die NICHT mit dem Alter waechst --
                deshalb ist sie der ehrliche Serien-Vergleich. Ein 3 Tage
                alter und ein 3 Wochen alter Short sind hier vergleichbar,
                bei Aufrufen sind sie es nicht.
                (Diese Zahl war ueber die Analytics-API immer verfuegbar. Der
                Vault notierte seit dem 24.08. "AVP% steht aus".)

  Aufrufe@N     Aufrufe bei gleichem Video-Alter, aus den Snapshots.
                Ohne Altersabgleich ist jeder Serienvergleich wertlos:
                aeltere Videos gewinnen automatisch.

Aufruf
    python3 tools/kp_metrik.py              Serienbilanz
    python3 tools/kp_metrik.py --snapshot   zusaetzlich Tages-Snapshot sichern
    python3 tools/kp_metrik.py --json

Ohne Netz/Zugang bricht das Skript ab, statt Platzhalter zu erfinden.
"""

import argparse
import datetime as dt
import glob
import json
import os
import statistics
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
SNAPS = os.path.join(ROOT, "YouTube-Knowledge", "07-Analytics", "snapshots")

# Serien-Grenzen = Veroeffentlichungsfenster. Beim Anlegen einer neuen Serie
# hier eine Zeile ergaenzen -- sonst faellt sie aus der Bilanz.
SERIEN = [
    ("V1 Tham Luang",  "2026-08-15", "2026-08-17"),
    ("V2 San Jose",    "2026-08-18", "2026-08-20"),
    ("V3 Koepcke",     "2026-08-21", "2026-08-24"),
    ("V4 Okene",       "2026-08-25", "2026-08-27"),
    ("V5 Lengede",     "2026-08-28", "2026-08-30"),
    ("V6 Nutty Putty", "2026-08-31", "2026-09-03"),
    ("V7 Prosperi",    "2026-09-04", "2026-09-07"),
    ("V8 Ralston",     "2026-09-08", "2026-09-11"),
]

# Aus der Shorts-Forschung 2026: unter ~50 % gesehener Anteil verliert ein
# Short die Verteilung im Feed. 70 %+ gilt als starker Bereich.
AVP_KRITISCH = 50.0
AVP_STARK = 70.0


def zugang():
    import analyse
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    d = analyse.lies_zugangsdatei()
    cid = analyse.hole("YOUTUBE_CLIENT_ID", d)
    sec = analyse.hole("YOUTUBE_CLIENT_SECRET", d)
    ref = analyse.hole("YOUTUBE_REFRESH_TOKEN", d)
    if not (cid and sec and ref):
        raise SystemExit(
            "Keine OAuth-Zugangsdaten (YOUTUBE_CLIENT_ID/_SECRET/_REFRESH_TOKEN).\n"
            "Ohne sie gibt es keine AVP%-Zahlen -- und geraten wird hier nicht.")
    cr = Credentials(
        token=None, refresh_token=ref, client_id=cid, client_secret=sec,
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/yt-analytics.readonly",
                "https://www.googleapis.com/auth/youtube"])
    return (build("youtube", "v3", credentials=cr, cache_discovery=False),
            build("youtubeAnalytics", "v2", credentials=cr, cache_discovery=False),
            analyse.KANAL_ID)


def hole_videos(yt, kanal_id):
    up = yt.channels().list(part="contentDetails", id=kanal_id).execute(
        )["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, tok = [], None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=up,
                                    maxResults=50, pageToken=tok).execute()
        ids += [i["contentDetails"]["videoId"] for i in r["items"]]
        tok = r.get("nextPageToken")
        if not tok:
            break
    out = []
    for i in range(0, len(ids), 50):
        r = yt.videos().list(part="snippet,statistics,status,contentDetails",
                             id=",".join(ids[i:i + 50])).execute()
        for v in r["items"]:
            out.append({
                "id": v["id"],
                "pub": v["snippet"]["publishedAt"][:10],
                "titel": v["snippet"]["title"],
                "views": int(v["statistics"].get("viewCount", 0)),
                "dauer": v["contentDetails"]["duration"],
                "sichtbar": v["status"]["privacyStatus"],
            })
    return sorted(out, key=lambda r: r["pub"])


def hole_avp(ya, von, bis):
    r = ya.reports().query(
        ids="channel==MINE", startDate=von, endDate=bis,
        metrics="views,averageViewPercentage,averageViewDuration",
        dimensions="video", sort="-views", maxResults=200).execute()
    return {z[0]: {"views": z[1], "avp": z[2], "avd": z[3]}
            for z in r.get("rows", [])}


def alter(pub, stichtag):
    return (dt.date.fromisoformat(stichtag) - dt.date.fromisoformat(pub)).days


def aufrufe_bei_alter(videos_der_serie, tage=(2, 3)):
    """Aufrufe bei gleichem Video-Alter -- aus den gespeicherten Snapshots.

    Gibt (median, n, snapshot-datum) zurueck oder None, wenn zum passenden
    Zeitpunkt kein Snapshot gezogen wurde. Dieses None ist wichtig: es sagt
    ehrlich "diese Serie wurde nie altersgleich gemessen" statt eine
    unvergleichbare Zahl zu zeigen. V5 und V6 stehen genau so da -- die
    Snapshots endeten am 29.08.
    """
    heute = dt.date.today().isoformat()
    quellen = []
    for p in sorted(glob.glob(os.path.join(SNAPS, "*.json"))):
        d = json.load(open(p, encoding="utf-8"))
        quellen.append((d["snapshot_date"], {v["id"]: v["views"]
                                             for v in d["videos"]}))
    quellen.append((heute, {v["id"]: v["views"] for v in videos_der_serie}))

    for datum, tabelle in quellen:
        treffer = [tabelle[v["id"]] for v in videos_der_serie
                   if v["id"] in tabelle
                   and tage[0] <= alter(v["pub"], datum) <= tage[1]]
        if len(treffer) >= 3:
            return statistics.median(treffer), len(treffer), datum
    return None


def snapshot_schreiben(videos, abos, gesamt):
    os.makedirs(SNAPS, exist_ok=True)
    heute = dt.date.today().isoformat()
    p = os.path.join(SNAPS, f"{heute}.json")
    json.dump({"snapshot_date": heute, "subscribers": abos,
               "total_views": gesamt, "video_count": len(videos),
               "videos": [{"id": v["id"], "title": v["titel"],
                           "published": v["pub"] + "T00:00:00Z",
                           "status": v["sichtbar"], "duration_iso": v["dauer"],
                           "views": v["views"]} for v in videos]},
              open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return p


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--snapshot", action="store_true",
                    help="Tages-Snapshot sichern (Grundlage des Altersabgleichs)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    yt, ya, kanal = zugang()
    videos = hole_videos(yt, kanal)
    ch = yt.channels().list(part="statistics", id=kanal).execute()["items"][0]
    abos = int(ch["statistics"].get("subscriberCount", 0))
    gesamt = int(ch["statistics"].get("viewCount", 0))
    avp = hole_avp(ya, "2026-08-15", dt.date.today().isoformat())

    if a.snapshot:
        p = snapshot_schreiben(videos, abos, gesamt)
        print(f"Snapshot gesichert: {os.path.relpath(p, ROOT)}\n")

    bilanz = []
    for name, von, bis in SERIEN:
        s = [v for v in videos if von <= v["pub"] <= bis and v["sichtbar"] == "public"]
        if not s:
            bilanz.append({"serie": name, "n": 0})
            continue
        werte = [avp[v["id"]]["avp"] for v in s if v["id"] in avp]
        agl = aufrufe_bei_alter(s)
        bilanz.append({
            "serie": name, "n": len(s),
            "avp_median": round(statistics.median(werte), 1) if werte else None,
            "avp_n": len(werte),
            "views_median": round(statistics.median([v["views"] for v in s])),
            "views_altersgleich": None if not agl else round(agl[0]),
            "altersgleich_n": None if not agl else agl[1],
            "altersgleich_am": None if not agl else agl[2],
        })

    if a.json:
        print(json.dumps({"abos": abos, "aufrufe": gesamt,
                          "videos": len(videos), "serien": bilanz},
                         ensure_ascii=False, indent=1))
        return 0

    print("=" * 78)
    print(f"  KP-METRIK  —  gemessen am {dt.date.today().isoformat()}")
    print(f"  {abos} Abos · {gesamt:,} Aufrufe · {len(videos)} Videos"
          .replace(",", "."))
    print("=" * 78)
    print(f"{'Serie':<16}{'n':>3}{'AVP% (gesehen)':>16}{'Aufrufe@2-3T':>14}"
          f"{'Aufrufe roh':>13}")
    print("-" * 78)
    for b in bilanz:
        if not b["n"]:
            print(f"{b['serie']:<16}  —  noch nichts veroeffentlicht")
            continue
        if b["avp_median"] is None:
            avps = "keine Daten"
        else:
            marke = ("schwach" if b["avp_median"] < AVP_KRITISCH
                     else "stark" if b["avp_median"] >= AVP_STARK else "")
            avps = f"{b['avp_median']:.1f} {marke}".strip()
            if b["avp_n"] < b["n"]:
                avps += f" ({b['avp_n']}/{b['n']})"
        agl = ("nie gemessen" if b["views_altersgleich"] is None
               else f"{b['views_altersgleich']}")
        print(f"{b['serie']:<16}{b['n']:>3}{avps:>16}{agl:>14}"
              f"{b['views_median']:>13}")

    print("-" * 78)
    print("  AVP% = Anteil des Shorts, der tatsaechlich gesehen wird.")
    print(f"  Waechst NICHT mit dem Alter -> der einzige faire Serienvergleich.")
    print(f"  Unter {AVP_KRITISCH:.0f} % verliert ein Short die Verteilung im Feed.")
    print("  'nie gemessen' = zum passenden Video-Alter wurde kein Snapshot")
    print("  gezogen. Diese Serie ist dauerhaft unvergleichbar. Deshalb:")
    print("  taeglich 'python3 tools/kp_metrik.py --snapshot' laufen lassen.")

    echte = [b for b in bilanz if b.get("avp_median") is not None]
    if len(echte) >= 2:
        print()
        erste, letzte = echte[0], echte[-1]
        d = letzte["avp_median"] - erste["avp_median"]
        richtung = "gestiegen" if d > 0 else "gefallen"
        print(f"  Trend {erste['serie']} -> {letzte['serie']}: "
              f"AVP {erste['avp_median']:.1f} -> {letzte['avp_median']:.1f} "
              f"({richtung}, {d:+.1f} Punkte)")
    print("=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
