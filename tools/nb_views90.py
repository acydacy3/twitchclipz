#!/usr/bin/env python3
"""Rollierende 90-Tage-Views + YPP-Fortschritt (YouTube Analytics API, gratis).
Nutzung: python3 tools/nb_views90.py  (nutzt YOUTUBE_* aus der Umgebung)"""
import os, datetime
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
def creds(scopes):
    return Credentials(None, refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        client_id=os.environ["YOUTUBE_CLIENT_ID"], client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
        token_uri="https://oauth2.googleapis.com/token", scopes=scopes)
end=datetime.date.today(); start=end-datetime.timedelta(days=90)
try:
    ya=build("youtubeAnalytics","v2",credentials=creds(["https://www.googleapis.com/auth/yt-analytics.readonly"]))
    r=ya.reports().query(ids="channel==MINE", startDate=str(start), endDate=str(end),
                         metrics="views,subscribersGained").execute()
    v=r["rows"][0][0] if r.get("rows") else 0
    print(f"90-Tage-Views ({start}–{end}): {v:,}".replace(",","."))
    print(f"  YPP-Views-Fortschritt: {v/10_000_000*100:.2f} % von 10.000.000")
    print(f"  Ø Views/Tag: {v/90:,.0f}  (Soll 111.000)".replace(",","."))
except Exception as e:
    print("Analytics-Query fehlgeschlagen (evtl. yt-analytics-Scope fehlt im Token):", str(e)[:120])
    print("-> Fallback: analyse.py (Gesamt-Views); solange Kanal <90 Tage ~ gleich.")
