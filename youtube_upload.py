"""YouTube-Upload mit Zeitplan-Terminierung.

Aufruf: python3 youtube_upload.py <mp4> <titel> <beschreibung_datei> <publishAtUTC>
     z.B. python3 youtube_upload.py short_01.mp4 "Titel" desc.txt 2026-08-21T09:30:00Z
"""
import os, sys, json, time
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

CATEGORY_ID = "22"  # People & Blogs
TAGS = [
    "juliane koepcke", "juliane diller", "lansa 508", "flugzeugabsturz",
    "amazonas", "dschungel", "1971", "peru", "wahre geschichte", "doku",
    "dokumentation", "katastrophe", "überlebende", "einzige überlebende",
    "regenwald", "überleben", "flugzeug", "unglück", "shorts",
    "katastrophenprotokoll", "wahre begebenheit", "history", "true story",
    "amazonasabsturz", "peru dschungel"
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

def upload(mp4, title, desc, publish_at):
    yt = build("youtube", "v3", credentials=creds())
    body = {
        "snippet": {
            "title": title,
            "description": desc,
            "tags": TAGS,
            "categoryId": CATEGORY_ID,
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
    req = yt.videos().insert(part="snippet,status", body=body, media_body=media)
    resp = None
    while resp is None:
        status, resp = req.next_chunk()
        if status:
            print(f"  upload {int(status.progress()*100)}%", flush=True)
    vid = resp["id"]
    print(f"video_id={vid}")
    return vid

if __name__ == "__main__":
    mp4 = sys.argv[1]
    title = sys.argv[2]
    desc = open(sys.argv[3], encoding="utf-8").read()
    publish_at = sys.argv[4]  # RFC3339 UTC z.B. 2026-08-21T09:30:00Z
    upload(mp4, title, desc, publish_at)
