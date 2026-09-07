#!/usr/bin/env python3
"""kp_ersetzen.py — terminierte Shorts durch neue Fassungen austauschen.

YouTube kann eine hochgeladene Videodatei nicht ersetzen. Ein neu gerenderter
Short muss deshalb neu hochgeladen und der alte geloescht werden.

Reihenfolge ist bewusst so und nicht anders:
    1. kp_gate.py --nachher   das FERTIGE Video pruefen
    2. hochladen              mit denselben Metadaten + Terminierung
    3. pruefen                laesst sich das neue Video abrufen?
    4. erst dann loeschen     das alte
So bleibt bei einem Abbruch immer eine Fassung stehen. Erst loeschen und dann
hochladen wuerde bei jedem Netzfehler eine Luecke im Sendeplan hinterlassen.

    python3 tools/kp_ersetzen.py <serie> --shorts 01,03,06 [--wirklich]

Ohne --wirklich passiert nichts: es wird nur angezeigt, was geschehen wuerde.
Veroeffentlichte (oeffentliche) Videos werden NIE angefasst -- nur private
und terminierte.
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


def lade_meta(serie):
    m = json.load(open(os.path.join(serie, "metadata.json"), encoding="utf-8"))
    return {s["id"]: s for s in m["shorts"]}


def lade_log(serie):
    p = os.path.join(serie, "upload_log.json")
    return (json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}), p


def hochladen(yt, mp4, meta):
    from googleapiclient.http import MediaFileUpload
    body = {
        "snippet": {"title": meta["title"], "description": meta["description"],
                    "tags": meta["tags"], "categoryId": "22",
                    "defaultLanguage": "de", "defaultAudioLanguage": "de"},
        "status": {"privacyStatus": "private", "publishAt": meta["publish_at"],
                   "selfDeclaredMadeForKids": False},
    }
    req = yt.videos().insert(
        part="snippet,status", body=body,
        media_body=MediaFileUpload(mp4, chunksize=-1, resumable=True,
                                   mimetype="video/mp4"))
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"    {int(status.progress()*100)} %", flush=True)
    return resp["id"]


def main():
    ap = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("serie")
    ap.add_argument("--shorts", required=True, help="z. B. 01,03,06")
    ap.add_argument("--wirklich", action="store_true",
                    help="ohne dieses Flag wird nur angezeigt")
    a = ap.parse_args()

    serie = a.serie.rstrip("/")
    nums = [n.strip().zfill(2) for n in a.shorts.split(",") if n.strip()]

    # ── 1. Riegel: das fertige Video pruefen ──────────────────────────────
    print("KP-GATE (nachher) — das fertige Material pruefen")
    for n in nums:
        p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "kp_gate.py"),
                            serie, "--nachher", "--short", n],
                           cwd=ROOT, capture_output=True, text=True)
        if p.returncode != 0:
            print(p.stdout)
            raise SystemExit(
                f"\nABBRUCH: Short {n} besteht die Nachher-Pruefung nicht.\n"
                f"Es wird nichts hochgeladen und nichts geloescht.")
        print(f"  Short {n}: grün")

    meta = lade_meta(serie)
    log, log_pfad = lade_log(serie)

    plan = []
    for n in nums:
        if n not in meta:
            raise SystemExit(f"Short {n} fehlt in {serie}/metadata.json")
        mp4 = os.path.join(serie, meta[n].get("file", f"render/short_{n}.mp4"))
        if not os.path.exists(mp4):
            raise SystemExit(f"Datei fehlt: {mp4}")
        plan.append((n, mp4, log.get(n, {}).get("video_id")))

    print(f"\nGeplanter Austausch in '{serie}':")
    for n, mp4, alt in plan:
        groesse = os.path.getsize(mp4) / 1e6
        print(f"  Short {n}  {groesse:5.1f} MB  →  neu hochladen, "
              f"Termin {meta[n]['publish_at']}")
        print(f"            alt: {alt or '(keines im Log)'}  →  danach loeschen")

    if not a.wirklich:
        print("\nProbelauf. Mit --wirklich wird es ausgefuehrt.")
        return 0

    yt = dienst()

    # ── Sicherung: oeffentliche Videos werden nicht angefasst ─────────────
    alte = [alt for _, _, alt in plan if alt]
    if alte:
        r = yt.videos().list(part="status,snippet", id=",".join(alte)).execute()
        for v in r.get("items", []):
            if v["status"]["privacyStatus"] == "public":
                raise SystemExit(
                    f"ABBRUCH: {v['id']} ist bereits OEFFENTLICH "
                    f"(\"{v['snippet']['title'][:50]}\").\n"
                    f"Veroeffentlichte Videos werden hier nicht ersetzt.")

    neu_ids = {}
    for n, mp4, _ in plan:
        print(f"\nShort {n} — hochladen …")
        neu_ids[n] = hochladen(yt, mp4, meta[n])
        print(f"  neu: {neu_ids[n]}")

    # ── 3. pruefen, bevor irgendetwas geloescht wird ──────────────────────
    r = yt.videos().list(part="status", id=",".join(neu_ids.values())).execute()
    da = {v["id"] for v in r.get("items", [])}
    fehlt = [i for i in neu_ids.values() if i not in da]
    if fehlt:
        raise SystemExit(
            f"ABBRUCH vor dem Loeschen: neue Videos nicht abrufbar: {fehlt}\n"
            f"Die alten Videos bleiben unangetastet.")
    print(f"\nAlle {len(neu_ids)} neuen Videos bestaetigt.")

    # ── 4. jetzt erst die alten entfernen ─────────────────────────────────
    for n, _, alt in plan:
        if not alt:
            continue
        try:
            yt.videos().delete(id=alt).execute()
            print(f"  Short {n}: altes Video {alt} geloescht")
        except Exception as e:
            print(f"  Short {n}: Loeschen von {alt} fehlgeschlagen — {e}")

    for n, neu in neu_ids.items():
        log[n] = {"uploaded": True, "video_id": neu, "ersetzt_am": "2026-09-07",
                  "vorher": log.get(n, {}).get("video_id")}
    json.dump(log, open(log_pfad, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"\n{log_pfad} aktualisiert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
