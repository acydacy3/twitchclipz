#!/usr/bin/env python3
"""Kanalstand des Katastrophenprotokolls — gemessen, nicht geschaetzt.

Aufruf:
    python3 analyse.py                  Kanalstand ausgeben
    python3 analyse.py --sprache-setzen Standardsprache auf Deutsch setzen

Zugangsdaten werden in dieser Reihenfolge gesucht:
    1. Umgebungsvariablen  YOUTUBE_CLIENT_ID / _SECRET / _REFRESH_TOKEN
    2. ZUGANGSDATEN.txt    im Projektordner, daneben oder im Home
    3. YOUTUBE_API_KEY     nur Lesezugriff, reicht fuer den Bericht

Was das Skript NICHT tut: schreiben, ausser wenn --sprache-setzen
ausdruecklich verlangt wird. Lesen kostet ~5 von 10.000 Kontingent-
einheiten pro Tag, ist also praktisch umsonst.
"""

import os
import re
import sys
from pathlib import Path

KANAL_ID = "UC1KCzLNlgGiYsLNQ7Z0HA-g"   # Katastrophenprotokoll

SUCHORTE = [
    Path(__file__).resolve().parent,
    Path(__file__).resolve().parent.parent,
    Path.home(),
    Path("/workspace"),
]


# --------------------------------------------------------------- Zugang

def lies_zugangsdatei():
    """Sucht ZUGANGSDATEN.txt und liest SCHLUESSEL=Wert-Zeilen."""
    werte = {}
    for ordner in SUCHORTE:
        pfad = ordner / "ZUGANGSDATEN.txt"
        if not pfad.is_file():
            continue
        for zeile in pfad.read_text(encoding="utf-8", errors="replace").splitlines():
            zeile = zeile.strip()
            if not zeile or zeile.startswith("#") or "=" not in zeile:
                continue
            schluessel, _, wert = zeile.partition("=")
            wert = wert.strip().strip('"').strip("'")
            if wert:
                werte[schluessel.strip()] = wert
        if werte:
            print(f"Zugangsdaten aus {pfad}")
            break
    return werte


def hole(name, datei):
    return os.environ.get(name) or datei.get(name) or ""


def dienst():
    """Baut den API-Zugang. Gibt (dienst, schreibrecht) zurueck."""
    try:
        from googleapiclient.discovery import build
    except ImportError:
        fehler("Die Google-Bibliothek fehlt.",
               "Nachinstallieren mit:  pip install google-api-python-client "
               "google-auth-oauthlib")

    datei = lies_zugangsdatei()
    cid = hole("YOUTUBE_CLIENT_ID", datei)
    secret = hole("YOUTUBE_CLIENT_SECRET", datei)
    refresh = hole("YOUTUBE_REFRESH_TOKEN", datei)
    api_key = hole("YOUTUBE_API_KEY", datei)

    if cid and secret and refresh:
        from google.oauth2.credentials import Credentials
        zugang = Credentials(
            token=None,
            refresh_token=refresh,
            client_id=cid,
            client_secret=secret,
            token_uri="https://oauth2.googleapis.com/token",
            scopes=["https://www.googleapis.com/auth/youtube"],
        )
        return build("youtube", "v3", credentials=zugang,
                     cache_discovery=False), True

    if api_key:
        print("Nur API-Key gefunden — Lesezugriff. Kein Sprache-Setzen, "
              "kein Hochladen.\n")
        return build("youtube", "v3", developerKey=api_key,
                     cache_discovery=False), False

    fehler(
        "Keine Zugangsdaten gefunden.",
        "",
        "Trage in claude.ai/code unter Environment variables ein:",
        "    YOUTUBE_CLIENT_ID=...",
        "    YOUTUBE_CLIENT_SECRET=...",
        "    YOUTUBE_REFRESH_TOKEN=...",
        "",
        "Danach eine NEUE Sitzung starten — eine laufende liest sie nicht.",
        "Alternativ eine ZUGANGSDATEN.txt in den Projektordner legen.",
    )


def fehler(*zeilen):
    print()
    for z in zeilen:
        print(z)
    print()
    sys.exit(1)


# ---------------------------------------------------------------- Hilfen

def sekunden(iso):
    """PT4M13S -> 253. Gibt 0 zurueck, wenn nichts zu holen ist."""
    t = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not t:
        return 0
    h, m, s = (int(x) if x else 0 for x in t.groups())
    return h * 3600 + m * 60 + s


def mmss(sek):
    return f"{sek // 60}:{sek % 60:02d}" if sek >= 60 else f"{sek}s"


def zahl(n):
    """1234567 -> 1.234.567"""
    return f"{int(n):,}".replace(",", ".")


# ---------------------------------------------------------------- Abrufe

def kanal(yt, schreibrecht):
    teile = "snippet,statistics,contentDetails,brandingSettings"
    if schreibrecht:
        antwort = yt.channels().list(part=teile, mine=True).execute()
    else:
        antwort = yt.channels().list(part=teile, id=KANAL_ID).execute()
    posten = antwort.get("items", [])
    if not posten:
        fehler("Kein Kanal gefunden.",
               "Bei OAuth: gehoert der Refresh-Token zu acydacy3@gmail.com?")
    return posten[0]


def alle_videos(yt, upload_liste):
    """Holt jedes Video der Uploads-Playlist mit Zahlen und Status."""
    ids, token = [], None
    while True:
        antwort = yt.playlistItems().list(
            part="contentDetails", playlistId=upload_liste,
            maxResults=50, pageToken=token,
        ).execute()
        ids += [p["contentDetails"]["videoId"] for p in antwort.get("items", [])]
        token = antwort.get("nextPageToken")
        if not token:
            break

    videos = []
    for i in range(0, len(ids), 50):
        antwort = yt.videos().list(
            part="snippet,statistics,contentDetails,status",
            id=",".join(ids[i:i + 50]),
        ).execute()
        videos += antwort.get("items", [])
    return videos


# --------------------------------------------------------------- Bericht

def bericht(k, videos):
    st = k.get("statistics", {})
    sn = k.get("snippet", {})
    br = k.get("brandingSettings", {}).get("channel", {})

    print("=" * 64)
    print(f"  {sn.get('title', 'Kanal')}")
    print("=" * 64)
    print(f"  Abonnenten     {zahl(st.get('subscriberCount', 0))}")
    print(f"  Aufrufe gesamt {zahl(st.get('viewCount', 0))}")
    print(f"  Videos         {zahl(st.get('videoCount', 0))}")

    sprache = br.get("defaultLanguage") or sn.get("defaultLanguage")
    if sprache:
        print(f"  Standardsprache {sprache}")
    else:
        print("  Standardsprache NICHT GESETZT  <- mit --sprache-setzen beheben")
    print()

    oeffentlich = [v for v in videos
                   if v.get("status", {}).get("privacyStatus") == "public"]
    geplant = [v for v in videos if v.get("status", {}).get("publishAt")]

    # ---- terminierte Uploads
    if geplant:
        print(f"  TERMINIERT ({len(geplant)})")
        for v in sorted(geplant, key=lambda x: x["status"]["publishAt"]):
            wann = v["status"]["publishAt"].replace("T", " ")[:16]
            laenge = sekunden(v["contentDetails"].get("duration"))
            print(f"    {wann} UTC  {mmss(laenge):>6}  "
                  f"{v['snippet']['title'][:44]}")
        print()

    # ---- veroeffentlichte Videos
    if oeffentlich:
        print(f"  VEROEFFENTLICHT ({len(oeffentlich)}), neueste zuerst")
        print(f"    {'Datum':<11}{'Laenge':>7}{'Aufrufe':>9}{'Likes':>7}  Titel")
        for v in oeffentlich:
            vst = v.get("statistics", {})
            laenge = sekunden(v["contentDetails"].get("duration"))
            print(f"    {v['snippet']['publishedAt'][:10]:<11}"
                  f"{mmss(laenge):>7}"
                  f"{zahl(vst.get('viewCount', 0)):>9}"
                  f"{zahl(vst.get('likeCount', 0)):>7}  "
                  f"{v['snippet']['title'][:40]}")
        print()

        # ---- die Laengenthese aus CLAUDE.md 4b nachrechnen
        kurz = [v for v in oeffentlich
                if sekunden(v["contentDetails"].get("duration")) <= 22]
        lang = [v for v in oeffentlich
                if sekunden(v["contentDetails"].get("duration")) > 22]

        def schnitt(gruppe):
            if not gruppe:
                return 0
            return sum(int(v.get("statistics", {}).get("viewCount", 0))
                       for v in gruppe) // len(gruppe)

        if kurz and lang:
            sk, sl = schnitt(kurz), schnitt(lang)
            print("  LAENGENTHESE (CLAUDE.md 4b)")
            print(f"    bis 22 s   n={len(kurz):<3} Schnitt {zahl(sk)} Aufrufe")
            print(f"    ueber 22 s n={len(lang):<3} Schnitt {zahl(sl)} Aufrufe")
            if sl:
                print(f"    Faktor {sk / sl:.1f}")
            print()

    ohne_tags = [v for v in oeffentlich if not v["snippet"].get("tags")]
    if ohne_tags:
        print(f"  ACHTUNG {len(ohne_tags)} veroeffentlichte Videos ohne Tags")
        print()

    print("=" * 64)


# ------------------------------------------------------- Sprache setzen

def sprache_setzen(yt, k, sprache="de"):
    """Setzt die Kanal-Standardsprache. Schickt brandingSettings vollstaendig
    zurueck — sonst leert die API die uebrigen Felder (CLAUDE.md 4d)."""
    branding = k.get("brandingSettings", {})
    branding.setdefault("channel", {})["defaultLanguage"] = sprache

    yt.channels().update(
        part="brandingSettings",
        body={"id": k["id"], "brandingSettings": branding},
    ).execute()

    pruef = yt.channels().list(part="brandingSettings",
                               id=k["id"]).execute()["items"][0]
    jetzt = pruef.get("brandingSettings", {}).get("channel", {}).get(
        "defaultLanguage")
    if jetzt == sprache:
        print(f"Standardsprache steht jetzt auf '{sprache}'. Bestaetigt.")
    else:
        print(f"Gesetzt, aber die Rueckfrage meldet '{jetzt}'. "
              "In YouTube Studio nachsehen.")


# ----------------------------------------------------------------- Start

def main():
    setzen = "--sprache-setzen" in sys.argv
    yt, schreibrecht = dienst()

    k = kanal(yt, schreibrecht)

    if setzen:
        if not schreibrecht:
            fehler("Sprache setzen braucht OAuth, ein API-Key reicht nicht.",
                   "YOUTUBE_CLIENT_ID, _SECRET und _REFRESH_TOKEN eintragen.")
        sprache_setzen(yt, k)
        print()
        k = kanal(yt, schreibrecht)

    videos = alle_videos(
        yt, k["contentDetails"]["relatedPlaylists"]["uploads"])
    bericht(k, videos)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as e:
        nachricht = str(e)
        if "invalid_grant" in nachricht:
            fehler("Der Refresh-Token wird abgelehnt.",
                   "Haeufigste Ursache: der OAuth-Zustimmungsbildschirm steht "
                   "noch auf 'Test'.",
                   "Dort verfaellt der Token nach 7 Tagen. Auf "
                   "'In Produktion' umstellen (CLAUDE.md 4d).")
        if "accessNotConfigured" in nachricht or "has not been used" in nachricht:
            fehler("Die YouTube Data API v3 ist im Google-Cloud-Projekt "
                   "nicht aktiviert.",
                   "Cloud Console -> APIs & Dienste -> Bibliothek -> "
                   "YouTube Data API v3 -> Aktivieren.")
        fehler(f"Abgebrochen: {nachricht}")
