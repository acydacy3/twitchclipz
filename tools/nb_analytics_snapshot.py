#!/usr/bin/env python3
"""Speichert einen Analytics-Snapshot des Kanals als JSON.

Aufruf:
    python3 tools/nb_analytics_snapshot.py          Snapshot speichern
    python3 tools/nb_analytics_snapshot.py --show   Letzten Snapshot ausgeben

Snapshot-Pfad: YouTube-Knowledge/07-Analytics/snapshots/YYYY-MM-DD.json
Ein Snapshot pro Tag (Überschreiben am selben Tag ist OK).
"""

import json
import os
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP_DIR = ROOT / "YouTube-Knowledge" / "07-Analytics" / "snapshots"
SNAP_DIR.mkdir(parents=True, exist_ok=True)

SUCHORTE = [ROOT, ROOT.parent, Path.home(), Path("/workspace")]


def lies_zugangsdatei():
    werte = {}
    for ordner in SUCHORTE:
        pfad = ordner / "ZUGANGSDATEN.txt"
        if not pfad.is_file():
            continue
        for zeile in pfad.read_text(encoding="utf-8", errors="replace").splitlines():
            zeile = zeile.strip()
            if not zeile or zeile.startswith("#") or "=" not in zeile:
                continue
            k, _, v = zeile.partition("=")
            v = v.strip().strip('"').strip("'")
            if v:
                werte[k.strip()] = v
        if werte:
            break
    return werte


def hole(name, datei):
    return os.environ.get(name) or datei.get(name) or ""


def hole_kanal_daten():
    try:
        from googleapiclient.discovery import build
        from google.oauth2.credentials import Credentials
    except ImportError:
        print("google-api-python-client fehlt. pip install google-api-python-client google-auth-oauthlib")
        return None

    datei = lies_zugangsdatei()
    cid = hole("YOUTUBE_CLIENT_ID", datei)
    secret = hole("YOUTUBE_CLIENT_SECRET", datei)
    refresh = hole("YOUTUBE_REFRESH_TOKEN", datei)
    api_key = hole("YOUTUBE_API_KEY", datei)

    if not ((cid and secret and refresh) or api_key):
        print("Keine YouTube-Zugangsdaten. Snapshot ohne Kanaldaten.")
        return None

    if cid and secret and refresh:
        zugang = Credentials(
            token=None, refresh_token=refresh,
            client_id=cid, client_secret=secret,
            token_uri="https://oauth2.googleapis.com/token",
            scopes=["https://www.googleapis.com/auth/youtube"],
        )
        yt = build("youtube", "v3", credentials=zugang, cache_discovery=False)
        schreibrecht = True
    else:
        yt = build("youtube", "v3", developerKey=api_key, cache_discovery=False)
        schreibrecht = False

    kanal_id = "UC1KCzLNlgGiYsLNQ7Z0HA-g"
    if schreibrecht:
        resp = yt.channels().list(
            part="snippet,statistics,contentDetails", mine=True
        ).execute()
    else:
        resp = yt.channels().list(
            part="snippet,statistics,contentDetails", id=kanal_id
        ).execute()

    items = resp.get("items", [])
    if not items:
        print("Kanal nicht gefunden.")
        return None

    k = items[0]
    st = k.get("statistics", {})
    upload_list = k["contentDetails"]["relatedPlaylists"]["uploads"]

    # Alle Videos holen
    ids, token = [], None
    while True:
        ans = yt.playlistItems().list(
            part="contentDetails", playlistId=upload_list,
            maxResults=50, pageToken=token,
        ).execute()
        ids += [p["contentDetails"]["videoId"] for p in ans.get("items", [])]
        token = ans.get("nextPageToken")
        if not token:
            break

    videos = []
    for i in range(0, len(ids), 50):
        ans = yt.videos().list(
            part="snippet,statistics,contentDetails,status",
            id=",".join(ids[i:i + 50]),
        ).execute()
        videos += ans.get("items", [])

    video_daten = []
    for v in videos:
        sn = v.get("snippet", {})
        sv = v.get("statistics", {})
        ct = v.get("contentDetails", {})
        st_v = v.get("status", {})
        video_daten.append({
            "id": v["id"],
            "title": sn.get("title", ""),
            "published": sn.get("publishedAt", ""),
            "status": st_v.get("privacyStatus", ""),
            "duration_iso": ct.get("duration", ""),
            "views": int(sv.get("viewCount", 0)),
            "likes": int(sv.get("likeCount", 0)),
            "comments": int(sv.get("commentCount", 0)),
            "tags": sn.get("tags", []),
        })

    return {
        "subscribers": int(st.get("subscriberCount", 0)),
        "total_views": int(st.get("viewCount", 0)),
        "video_count": int(st.get("videoCount", 0)),
        "videos": video_daten,
    }


def speichere_snapshot():
    heute = date.today().isoformat()
    pfad = SNAP_DIR / f"{heute}.json"

    daten = hole_kanal_daten()
    if daten is None:
        daten = {}

    daten["snapshot_date"] = heute
    daten.setdefault("subscribers", 0)
    daten.setdefault("total_views", 0)
    daten.setdefault("video_count", 0)
    daten.setdefault("videos", [])

    pfad.write_text(json.dumps(daten, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Snapshot gespeichert: {pfad}")
    print(f"  Abonnenten: {daten['subscribers']}")
    print(f"  Aufrufe:    {daten['total_views']}")
    print(f"  Videos:     {daten['video_count']}")
    return pfad


def zeige_letzten():
    snaps = sorted(SNAP_DIR.glob("*.json"))
    if not snaps:
        print("Kein Snapshot vorhanden.")
        return
    daten = json.loads(snaps[-1].read_text(encoding="utf-8"))
    print(json.dumps(daten, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if "--show" in sys.argv:
        zeige_letzten()
    else:
        speichere_snapshot()
