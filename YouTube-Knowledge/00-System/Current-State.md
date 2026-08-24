---
type: system
title: Current-State
status: active
updated: 2026-08-24
tags: [system, state]
---

# Current-State — aktueller Stand

> Diese Note ist der **operative Schnappschuss**. Sie wird bei jeder Session
> aktualisiert (Stand-Zahlen kommen aus `analyse.py`, nicht aus dem Gedächtnis —
> gemessenes gewinnt gegen notiertes). Letztes Update: **2026-08-24**.

## Kanal
- *Katastrophenprotokoll* (`UC1KCzLNlgGiYsLNQ7Z0HA-g`, DE), gegründet 15.08.2026.
- Konto vidIQ: `kisha-ners@gmx.de`. Guthaben (19.08.): **30** (renewable 0/150,
  Add-on 30/80, refresh 15.09.2026). vidIQ nur auf Anfrage — Credits schonen.

## Videos (siehe Video-Gedächtnis)
- [[Video-01-Tham-Luang]] — veröffentlicht. 640 Aufrufe, 2 Abos. Langvideo 4,4 % Haltequote → Shorts tragen.
- [[Video-02-San-Jose]] — fertig + terminiert (11 Shorts + Langvideo, 18.–20.08.).
- [[Video-03-Koepcke]] — fertig, hochgeladen, terminiert 21.–24.08. (10 Shorts, 3/Tag). Titel-Score Short 1: 74/100.
- **Video 4 Kandidat:** Lengede (deutscher Erinnerungsanker, verbindet mit V2/V3). Siehe [[Decision-Themenwahl-Koepcke-vor-Lengede]].

## Zugänge (Stand 19.08.)
- **YouTube Data + Analytics API:** OAuth-Refresh-Token gültig, Uploads/Analytics/Terminierung produktiv.
- **git push:** in dieser Umgebung **frei** (Branch-Workflow). ⚠️ Das ist neu — der frühere
  403-Zustand (Drive-Umweg) ist damit überholt; siehe [[Decision-Git-vs-Drive-Persistenz]].
- **Netzsperre:** aufgehoben (17.08.). elevenlabs/higgsfield/youtube erreichbar.
- **TikTok über Buffer:** @mausigermax verbunden (`acydacy3@gmail.com`).

## Werkzeuge
- **Whisper** (`faster-whisper small-de int8`) = Standard-Transkription; Vosk nur Offline-Fallback. Siehe [[Decision-Whisper-statt-Vosk]].
- **Bild-Engines:** Nano Banana Pro + Seedance (Figur/Hero), Z-Image (Landschaft, 0,15 Cr.). Siehe [[Decision-Bild-Engine-Wahl]].
- **claude-youtube** Skill (als claude.ai-Skill), yt-dlp (via deno), gdown.

## Aktuell wichtigste offene Punkte
- Längen-These vs. Hook-These noch nicht sauber getrennt (n zu klein) → [[Hypothese-Hook-schlaegt-Laenge]].
- Hook-Banner mit abweichendem Text: nie belegt besser → [[Experiment-Hook-Banner-abweichender-Text]].
- TikTok-Hashtag-Wahl stützt sich auf YouTube-Volumen (schwächster Punkt) → [[Frage-TikTok-Hashtag-Volumen]].

## Operative Kern-Rules (aus Learnings promoted, Stand jetzt)
Diese gelten aktuell in der Produktion (Belege in den verlinkten Learnings):
- **Hook entscheidet, nicht Sekundenzahl.** Sichere Zone 19–39 s, tote Sekunden killen. → [[Learning-Retention-und-Laenge]]
- **Untertitel = Stimme** (Ton-aus-Publikum). Hook-Banner optional/abweichend nur als Test. → [[Learning-Captions]], [[Learning-Storytelling-Shorts]]
- **Jeder Titel trägt ein starkes Keyword; Aussage bis Zeichen 35 fertig.** → [[Learning-Titel]]
- **Fertige Videos vor Upload nach Drive/Repo sichern.** → [[Learning-Editing-Video]]
