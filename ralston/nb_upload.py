#!/usr/bin/env python3
"""V8 Ralston — Upload aller 10 Shorts + Longform (idempotent via upload_log.json).

Aufruf (aus Repo-Root):
    python3 ralston/nb_upload.py                 # alle Shorts + Longform
    python3 ralston/nb_upload.py --short 01      # einzelner Short
    python3 ralston/nb_upload.py --longform       # nur Longform
    python3 ralston/nb_upload.py --dry-run        # nur anzeigen
"""
import argparse
import json
import os
import sys
import time

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
META = os.path.join(BASE, "metadata.json")
LOG  = os.path.join(BASE, "upload_log.json")

def _creds():
    from google.oauth2.credentials import Credentials
    return Credentials(
        None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/youtube"],
    )

def _upload_to_yt(mp4, title, desc, tags, publish_at):
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    yt = build("youtube", "v3", credentials=_creds())
    body = {
        "snippet": {
            "title": title,
            "description": desc,
            "tags": tags,
            "categoryId": "22",
            "defaultLanguage": "de",
            "defaultAudioLanguage": "de",
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_at,
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(mp4, chunksize=-1, resumable=True, mimetype="video/mp4")
    req  = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"  upload {int(status.progress()*100)}%", flush=True)
    return resp["id"]


def load_log():
    if os.path.exists(LOG):
        with open(LOG) as f:
            return json.load(f)
    return {}


def save_log(log):
    with open(LOG, "w") as f:
        json.dump(log, f, indent=2)


def upload_one(entry, dry_run=False):
    num        = entry["id"]
    title      = entry["title"]
    mp4        = os.path.join(BASE, entry["file"])
    publish_at = entry["publish_at"]
    desc       = entry["description"]


    print(f"\n{'─'*55}")
    print(f"  S{num} | {title[:50]}")
    print(f"  Geplant: {publish_at}")
    print(f"  Datei: {mp4}")

    if not os.path.exists(mp4):
        print(f"  ✗ Datei nicht gefunden!")
        return False

    if dry_run:
        print("  [DRY-RUN] Würde hochladen.")
        return True

    print("  ▶ Uploading…")
    try:
        vid_id = _upload_to_yt(mp4, title, desc, entry["tags"], publish_at)
        print(f"  ✓ Hochgeladen: {vid_id}")
        return vid_id
    except Exception as e:
        print(f"  ✗ FEHLER: {e}")
        return False


def upload_longform(entry, dry_run=False):
    title      = entry["title"]
    mp4        = os.path.join(BASE, entry["file"])
    publish_at = entry["publish_at"]
    desc       = entry["description"]

    print(f"\n{'─'*55}")
    print(f"  LONGFORM | {title[:50]}")
    print(f"  Geplant: {publish_at}")
    print(f"  Datei: {mp4}")

    if not os.path.exists(mp4):
        print(f"  ✗ Datei nicht gefunden! → Zuerst: python3 lang.py ralston/")
        return False

    if dry_run:
        print("  [DRY-RUN] Würde hochladen.")
        return True

    print("  ▶ Uploading Longform…")
    try:
        vid_id = _upload_to_yt(mp4, title, desc, entry["tags"], publish_at)
        print(f"  ✓ Hochgeladen: {vid_id}")
        return vid_id
    except Exception as e:
        print(f"  ✗ FEHLER: {e}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--short", help="Nur dieses Short (z.B. 01)")
    parser.add_argument("--longform", action="store_true", help="Nur Longform hochladen")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    with open(META) as f:
        meta = json.load(f)

    log = load_log()

    # ── Longform ─────────────────────────────────────────────────────────
    if args.longform or (not args.short):
        lf = meta.get("longform")
        if lf:
            if log.get("longform", {}).get("uploaded"):
                print("  Longform bereits hochgeladen — überspringe")
            else:
                result = upload_longform(lf, dry_run=args.dry_run)
                if result and not args.dry_run:
                    log["longform"] = {"uploaded": True, "video_id": str(result), "ts": time.time()}
                    save_log(log)
                    time.sleep(3)
        else:
            print("  Kein 'longform'-Eintrag in metadata.json")

    if args.longform:
        return  # nur Longform gewünscht

    # ── Shorts ───────────────────────────────────────────────────────────
    shorts = meta["shorts"]

    if args.short:
        shorts = [s for s in shorts if s["id"] == args.short]
        if not shorts:
            print(f"Short {args.short} nicht in metadata.json")
            return

    ok = err = skip = 0
    for entry in shorts:
        num = entry["id"]
        if num in log and log[num].get("uploaded"):
            print(f"  S{num} bereits hochgeladen — überspringe")
            skip += 1
            continue

        result = upload_one(entry, dry_run=args.dry_run)

        if result and not args.dry_run:
            log[num] = {"uploaded": True, "video_id": str(result), "ts": time.time()}
            save_log(log)
            ok += 1
            time.sleep(3)   # Rate-Limit Puffer
        else:
            err += 1

    print(f"\n{'='*55}")
    print(f"  Fertig: {ok} hochgeladen | {skip} übersprungen | {err} Fehler")
    print(f"  Log: {LOG}")


if __name__ == "__main__":
    main()
