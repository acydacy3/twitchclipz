"""Lädt alle 10 Prosperi-Shorts zu YouTube hoch (idempotent).
Prüft vorher ob bereits hochgeladen (uploaded.json). Terminiert nach metadata.json."""
import json, os, sys, time
from pathlib import Path

BASE = Path("/home/user/twitchclipz/prosperi")
META = json.loads((BASE/"metadata.json").read_text())
UPLOADED = BASE/"uploaded.json"
OUTPUT   = BASE/"output"

TAGS = [
    "mauro prosperi", "marathon des sables", "sahara", "überleben",
    "wüste", "sahara überleben", "wahre geschichte", "doku",
    "katastrophenprotokoll", "shorts", "desert survival", "marathon",
    "dokumentation", "true story", "1994", "marokko", "algerien",
    "sandsturm", "sahara doku", "faceless",
]
CATEGORY_ID = "22"

def creds():
    from google.oauth2.credentials import Credentials
    return Credentials(
        None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/youtube"],
    )

def upload_one(yt, mp4: Path, n: str) -> str:
    from googleapiclient.http import MediaFileUpload
    m = META[n]
    body = {
        "snippet": {
            "title": m["title"],
            "description": m["desc"],
            "tags": TAGS,
            "categoryId": CATEGORY_ID,
            "defaultLanguage": "de",
            "defaultAudioLanguage": "de",
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": m["publish_utc"],
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(str(mp4), chunksize=-1, resumable=True, mimetype="video/mp4")
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"  {int(status.progress()*100)}%", end=" ", flush=True)
    print()
    return resp["id"]

def main():
    done: dict[str, str] = {}
    if UPLOADED.exists():
        done = json.loads(UPLOADED.read_text())

    only = sys.argv[1:] or [f"{i:02d}" for i in range(1, 11)]

    from googleapiclient.discovery import build
    yt = build("youtube", "v3", credentials=creds())

    for n in only:
        mp4 = OUTPUT/f"prosperi_{n}.mp4"
        if not mp4.exists():
            print(f"[{n}] SKIP — {mp4.name} nicht gefunden")
            continue
        if n in done:
            print(f"[{n}] bereits hochgeladen: {done[n]}")
            continue
        print(f"[{n}] upload → {META[n]['title'][:50]}...", flush=True)
        try:
            vid = upload_one(yt, mp4, n)
            done[n] = vid
            UPLOADED.write_text(json.dumps(done, indent=2, ensure_ascii=False))
            print(f"[{n}] OK: https://youtu.be/{vid}  scheduled={META[n]['publish_utc']}")
            time.sleep(3)
        except Exception as e:
            print(f"[{n}] FEHLER: {e}")
            time.sleep(10)

    print("\nALLE HOCHGELADEN")
    for n, vid in done.items():
        print(f"  S{n}: https://youtu.be/{vid}  → {META[n]['publish_utc']}")

if __name__ == "__main__":
    main()
