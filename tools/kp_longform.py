#!/usr/bin/env python3
"""kp_longform.py — Langvideo einer Serie pruefen und hochladen. Fuer JEDE Serie.

WARUM GENERISCH
---------------
Jede Serie hatte bisher ihr eigenes nb_upload.py. ralston/nb_upload.py kann
Langvideos, prosperi/nb_upload.py nicht — und nuttyputty wieder anders. Genau
dieses Kopieren je Serie ist die Ursache des Befundes vom 07.09.: ein Fix
wandert nur so weit, wie jemand ihn von Hand traegt (F-V9-B). Deshalb hier
EIN Werkzeug fuer alle Serien.

    python3 tools/kp_longform.py <serie>                nur anzeigen
    python3 tools/kp_longform.py <serie> --wirklich     hochladen

Metadaten kommen aus <serie>/metadata.json unter dem Schluessel "longform":
    {"longform": {"title": …, "description": …, "tags": [...],
                  "publish_at": "2026-09-12T10:00:00Z", "file": "render/long.mp4"}}

Vor dem Upload laeuft IMMER das Langform-Gate (R26 Laenge, R27 Querformat,
R28 Lautheit, R29 Bildwechsel). Ohne gruenes Gate passiert nichts — das ist
kein Vorschlag, sondern der Ablauf.
"""

import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def dienst():
    from googleapiclient.discovery import build
    from google.oauth2.credentials import Credentials
    fehlend = [v for v in ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET",
                           "YOUTUBE_REFRESH_TOKEN") if not os.environ.get(v)]
    if fehlend:
        raise SystemExit(f"Zugangsdaten fehlen: {', '.join(fehlend)}")
    cr = Credentials(
        None, refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/youtube"])
    return build("youtube", "v3", credentials=cr, cache_discovery=False)


def gate(serie):
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "kp_gate.py"),
                        serie, "--langform"], cwd=ROOT,
                       capture_output=True, text=True)
    return p.returncode, p.stdout


def hochladen(yt, mp4, meta):
    from googleapiclient.http import MediaFileUpload
    status = {"privacyStatus": "private", "selfDeclaredMadeForKids": False}
    if meta.get("publish_at"):
        status["publishAt"] = meta["publish_at"]
    body = {
        "snippet": {"title": meta["title"], "description": meta["description"],
                    "tags": meta.get("tags", []), "categoryId": "22",
                    "defaultLanguage": "de", "defaultAudioLanguage": "de"},
        "status": status,
    }
    req = yt.videos().insert(
        part="snippet,status", body=body,
        media_body=MediaFileUpload(mp4, chunksize=-1, resumable=True,
                                   mimetype="video/mp4"))
    resp = None
    while resp is None:
        st, resp = req.next_chunk()
        if st:
            print(f"    {int(st.progress()*100)} %", flush=True)
    return resp["id"]


def main():
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("serie")
    ap.add_argument("--wirklich", action="store_true")
    a = ap.parse_args()

    serie = a.serie.rstrip("/")
    pfad = serie if os.path.isdir(serie) else os.path.join(ROOT, serie)
    if not os.path.isdir(pfad):
        raise SystemExit(f"Serie '{a.serie}' nicht gefunden.")

    mp = os.path.join(pfad, "metadata.json")
    if not os.path.exists(mp):
        raise SystemExit(f"{mp} fehlt.")
    m = json.load(open(mp, encoding="utf-8"))
    meta = m.get("longform")
    if not meta:
        raise SystemExit(
            f"Kein \"longform\"-Eintrag in {mp}.\n"
            f"Noetig: title, description, tags, publish_at, file.\n"
            f"Regel R12 meldet das auch im Gate.")

    mp4 = os.path.join(pfad, meta.get("file", "render/long.mp4"))
    if not os.path.exists(mp4):
        raise SystemExit(f"Datei fehlt: {mp4}  (bauen: python3 nb_lang.py {a.serie})")

    log_pfad = os.path.join(pfad, "upload_log.json")
    log = json.load(open(log_pfad, encoding="utf-8")) if os.path.exists(log_pfad) else {}
    if isinstance(log.get("longform"), dict) and log["longform"].get("video_id"):
        print(f"Bereits hochgeladen: {log['longform']['video_id']}  "
              f"(Eintrag in {log_pfad} loeschen, um neu hochzuladen)")
        return 0

    print("=" * 74)
    print(f"  LANGVIDEO {a.serie}")
    print("=" * 74)
    print(f"  Titel:   {meta['title']}")
    print(f"  Termin:  {meta.get('publish_at', '(sofort privat)')}")
    print(f"  Datei:   {os.path.relpath(mp4, ROOT)}  "
          f"({os.path.getsize(mp4)/1e6:.1f} MB)")

    rc, ausgabe = gate(serie)
    if rc != 0:
        print("\n" + ausgabe)
        raise SystemExit("ABBRUCH: Langform-Gate ist rot. Nichts hochgeladen.")
    print("  Gate:    grün (R26 Länge · R27 Querformat · R28 Ton · R29 Bildwechsel)")

    if not a.wirklich:
        print("\nProbelauf. Mit --wirklich wird hochgeladen.")
        return 0

    yt = dienst()
    print("\n  hochladen …")
    vid = hochladen(yt, mp4, meta)
    print(f"  ✓ {vid}")

    log["longform"] = {"uploaded": True, "video_id": vid,
                       "publish_at": meta.get("publish_at")}
    json.dump(log, open(log_pfad, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"  {os.path.relpath(log_pfad, ROOT)} aktualisiert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
