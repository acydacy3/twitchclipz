"""Lädt alle 10 Koepcke-Shorts zu YouTube hoch mit Zeitplan."""
import json, os, sys, time
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

BASE = Path("/home/user/twitchclipz/lengede")
CATEGORY_ID = "22"
TAGS = [
    "wunder von lengede", "lengede", "grubenunglück", "dahlbuschbombe", "1963",
    "bergleute", "verschüttet", "bergwerk", "rettung", "wahre geschichte", "doku",
    "dokumentation", "katastrophe", "überleben", "unglück", "shorts",
    "katastrophenprotokoll", "bergbau", "niedersachsen", "eisenerz", "alter mann",
    "gerettet", "deutschland", "true story"
]

def creds():
    return Credentials(
        None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token",
        scopes=["https://www.googleapis.com/auth/youtube"],
    )

def upload_one(yt, n, meta):
    mp4 = BASE / "output" / f"okene_{n}.mp4"
    body = {
        "snippet": {
            "title": meta["title"],
            "description": meta["desc"],
            "tags": TAGS,
            "categoryId": CATEGORY_ID,
            "defaultLanguage": "de",
            "defaultAudioLanguage": "de",
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": meta["publish_utc"],
            "selfDeclaredMadeForKids": False,
        },
    }
    media = MediaFileUpload(str(mp4), chunksize=8*1024*1024, resumable=True, mimetype="video/mp4")
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    tries = 0
    while resp is None:
        try:
            _, resp = req.next_chunk()
        except HttpError as e:
            tries += 1
            if tries > 3:
                raise
            time.sleep(2 ** tries)
    return resp["id"]

def main():
    yt = build("youtube", "v3", credentials=creds())
    metas = json.load(open(BASE / "metadata.json"))
    results = {}
    for n in [f"{i:02d}" for i in range(1, 11)]:
        try:
            vid = upload_one(yt, n, metas[n])
            print(f"Short {n}: video_id={vid} publishAt={metas[n]['publish_utc']}", flush=True)
            results[n] = vid
        except Exception as e:
            print(f"Short {n}: FAILED - {e}", flush=True)
            results[n] = None
    (BASE / "upload_results.json").write_text(json.dumps(results, indent=2))

if __name__ == "__main__":
    main()
