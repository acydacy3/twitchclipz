---
type: system
title: Current-State
status: active
updated: 2026-08-25
tags: [system, state]
---

# Current-State — aktueller Stand

> Diese Note ist der **operative Schnappschuss**. Sie wird bei jeder Session
> aktualisiert (Stand-Zahlen kommen aus `analyse.py`, nicht aus dem Gedächtnis —
> gemessenes gewinnt gegen notiertes). Letztes Update: **2026-08-27**.

> **Selbstprüfung (Session-Start):** Liegt der Vault `YouTube-Knowledge/` und `analyse.py` im Checkout und sagt `CLAUDE.md` NICHT „git push 403"? Dann bist du aktuell. Falls nein → Recovery-Schritte oben in `CLAUDE.md` („⚠️ ZUERST"). Branch-Namen wechseln je Session; **`main` ist jetzt AKTUELL** (25.08. voll synchronisiert) — ebenso der jeweilige `claude/…`-Branch. Der richtige Checkout ist jeder, der **diesen Vault + `tools/`** enthält.

## Nordstern-Ziel (messbar)
- **YPP-Monetarisierung, Shorts-Pfad: 1.000 Abos + 10 Mio Shorts-Views in 90 Tagen** (vor der Feb-2027-Regel). Stand 25.08.: Abos **4,2 %**, Views **0,20 %** — Views-Soll ~111k/Tag vs. aktuell ~2k/Tag (Faktor ~55). **Fortschritt jede Session loggen** → [[Ziel-YPP-Monetarisierung]].

## Kanal
- *Katastrophenprotokoll* (`UC1KCzLNlgGiYsLNQ7Z0HA-g`, DE), gegründet 15.08.2026.
- **Gemessen 27.08. (nb_analytics_snapshot.py):** **45 Abos**, **30.751 Aufrufe** (+1.631 in 24 h!), **44 Videos**. Wachstum 2→9→37→41→45. *(Vor Produktion neu ziehen — analyse.py schlägt diese Notiz.)*
- Konto vidIQ: `kisha-ners@gmx.de`. Guthaben (19.08.): **30** (renewable 0/150,
  Add-on 30/80, refresh 15.09.2026). vidIQ nur auf Anfrage — Credits schonen.

## Videos (siehe Video-Gedächtnis)
- [[Video-01-Tham-Luang]] — veröffentlicht. 640 Aufrufe, 2 Abos. Langvideo 4,4 % Haltequote → Shorts tragen.
- [[Video-02-San-Jose]] — fertig + terminiert (11 Shorts + Langvideo, 18.–20.08.).
- [[Video-03-Koepcke]] — fertig, hochgeladen, terminiert 21.–24.08. (10 Shorts, 3/Tag). Titel-Score Short 1: 74/100.
- **Video 4 (Okene/Jascon-4) PRODUZIERT + terminiert (24.08.):** 10 Shorts gerendert, **9/10 geplant** (24.–27.08.); Short 10 via Trigger 25.08. Siehe [[Video-04-Okene]], [[Produktions-Runbook]].
- **Video 5 Lengede FERTIG + TERMINIERT (verifiziert 25.08. via `analyse.py`):** alle **10/10 Shorts terminiert (28.–31.08.)**. Okene-Shorts ebenfalls terminiert (25.–27.08.). Trigger lief durch. Siehe [[Video-05-Lengede]].
- **Video 6 Nutty Putty FERTIG + TERMINIERT (26.08.):** alle 10/10 Shorts hochgeladen, Schedule 31.08–03.09 (3/Tag bündig nach Lengede). Siehe [[Video-06-NuttyPutty]].
- **Video 7 Prosperi FERTIG + TERMINIERT (27.08.):** alle 10/10 Shorts hochgeladen, Schedule **04.09–07.09** (3/Tag bündig nach Nutty Putty). S01–S10 live. Branch: `claude/neubeginn-v7-prosperi-6mmj14`.
- **V8-Pipeline BEREIT (27.08.):** Aron Ralston (127 Stunden) als Primärkandidat definiert — Okene-Formel: Paradox-Hook + Anagnorisis + konkreter Zeitstempel. Hook-Pool fertig, Bilder-Strategie, Risiko-Analyse. Backup: Vesna Vulović. → [[Ideen-Pipeline]] **NÄCHSTER SCHRITT: Nutzer liefert V8-Skript.**
- **Voller Tagesstand: [[Audit-2026-08-25]] + [[Audit-2026-08-26]].**

## Zugänge (Stand 19.08.)
- **YouTube Data + Analytics API:** OAuth-Refresh-Token gültig, Uploads/Analytics/Terminierung produktiv.
- **git push: FREIGESCHALTET (25.08.)** — funktioniert. **Persistenz = Git (Repo) primär**: `git commit` + `git push` am Session-Ende → nächster Container klont den vollen Stand automatisch. Drive ist damit **optional** (nur noch Nutzer-Ansicht/Asset-Transfer). **Alle MCP-/Zugriffe freigegeben (25.08.).** Branch-Namen wechseln je Session (`claude/…`); **`main` wird jede Session mitgepusht und ist aktuell** → neue Sessions starten garantiert korrekt, egal ob sie `main` oder den Feature-Branch ziehen.
- **Netzsperre:** aufgehoben (17.08.). elevenlabs/higgsfield/youtube erreichbar.
- **TikTok über Buffer:** @mausigermax verbunden (`acydacy3@gmail.com`).

## Werkzeuge
- **Whisper** (`faster-whisper small-de int8`) = Standard-Transkription; Vosk nur Offline-Fallback. Siehe [[Decision-Whisper-statt-Vosk]].
- **Bild-Engines:** Nano Banana Pro + Seedance (Figur/Hero), Z-Image (Landschaft, 0,15 Cr.). Siehe [[Decision-Bild-Engine-Wahl]].
- **claude-youtube** Skill (als claude.ai-Skill), yt-dlp (via deno), gdown.

## Aktuell wichtigste offene Punkte
- Längen-These **aufgelöst (24.08., n=35):** Faktor 0,9 statt 7,9 → Hook schlägt Länge (auf Aufruf-Basis; **AVP%/3-s-Retention für V3 steht aus**, ~2 Tage Analytics-Lag). → [[Learning-Retention-und-Laenge]]
- Hook-Banner mit abweichendem Text: nie belegt besser → [[Experiment-Hook-Banner-abweichender-Text]].
- TikTok-Hashtag-Wahl stützt sich auf YouTube-Volumen (schwächster Punkt) → [[Frage-TikTok-Hashtag-Volumen]].

## Neue Rules aus Competitor-Analyse (promoted 27.08.2026)
- **„| Doku" aus Titeln streichen** — „Doku" in Description + Tags, NICHT im Titel. Kein Top-Performer der Konkurrenz nutzt Genre-Labels.
- **Personennamen im Titel** wenn Person google-bar ist (Juliane Koepcke, Otto Warmbier…). Sofort: V03 Description + Tags mit „Juliane Koepcke" anreichern.
- **Short-Länge: Zone 19–39s bleibt operative Grundlage (n=44, intern bewiesen).** Competitor-Beobachtung 44–60s = Hypothese/Experiment-Vorschlag, KEIN Override. Ab V8: 2 Shorts mit 45–55s als A/B-Test.
- **Cinematische Schlüsselszene pro Short** — mindestens 1–2 Shots, die als Standbild funktionieren (Manim gratis). Diese Szenen = Thumbnail-Quelle: bereits produziertes Bild + Banner-Overlay hochladen, ODER Screenshot aus dem Video. Nie extra generieren für Shorts-Thumbnail.
- **Longform Custom-Thumbnail: unmögliches Bild** — 3D-Visualisierung (Manim) + einmalig KI-Portrait pro Produktionszyklus (Quota: max. 1 Higgsfield/HF-Call).
- **Rollenmodell: Scary Interesting** (0,99%/Monat Wachstum, ⌀ 1,21 Mio Views/Video — nicht HtSS, das stagniert bei 0,47%).
- **HtSS als Themen-Radar** — wenn Breakout > 5 auf Englisch, 4–8 Wochen Fenster für deutschen Suchverkehr. V03 Koepcke: HtSS aktuell 477 VPH.
- **Loveparade Duisburg → V9** (einzige deutsche Geschichte ohne deutschen Kanal, HtSS EN vorhanden).
- **Re-Run-Strategie**: Okene-Short → Re-Run Feb 2027 (neuer Titel, gleiche Geschichte).

## Operative Kern-Rules (aus Learnings promoted, Stand jetzt)
Diese gelten aktuell in der Produktion (Belege in den verlinkten Learnings):
- **Hook entscheidet, nicht Sekundenzahl.** Sichere Zone 19–39 s, tote Sekunden killen. → [[Learning-Retention-und-Laenge]]
- **Untertitel = Stimme** (Ton-aus-Publikum). Hook-Banner optional/abweichend nur als Test. → [[Learning-Captions]], [[Learning-Storytelling-Shorts]]
- **Jeder Titel trägt ein starkes Keyword; Aussage bis Zeichen 35 fertig.** → [[Learning-Titel]]
- **Fertige Videos vor Upload nach Drive/Repo sichern.** → [[Learning-Editing-Video]]
- **Szenen: Real vs. Generieren pro Szene** (Establishing = echt/Stock, Schlüsselmoment = generieren). → [[Learning-Bilder-Prompts]]
- **`/merken` läuft autonom + SOFORT**, sobald ein echtes Learning/Update entsteht: Note ändern + `git commit`/`push` direkt — **nicht** aufs Session-/Tagesende warten (Nutzer-Anweisung 25.08.).
- **Feinschliff (Tags, letzte Details) macht i. d. R. der Nutzer per Hand** — Claude produziert + terminiert, Nutzer poliert.
- **TikTok NIE automatisch posten.** Beleg: Auto-Schedule = 1 View/Video, manuell hochgeladen = Tausende. Claude gibt die fertigen Shorts an den Nutzer (SendUserFile/Drive) → **Nutzer lädt TikTok selbst hoch.** YouTube bleibt autonom. Gilt für ALLE künftigen Videos.
- **Bild-Sourcing autonom + präzise (Nutzer 25.08.).** Claude sucht ALLE Stock/Echt-Bilder selbst via Commons-**Kategorien** + Kontaktabzug-QC. Nutzer sucht keine Bilder mehr. → [[Learning-Bilder-Prompts]]
- **Musik MUSS hörbar sein (Nutzer 25.08.).** War V1–V5 unhörbar (db=-25 + falsches CWD). Fix: db≈-16, Render aus Repo-Root, mit volumedetect verifizieren. → [[Learning-Editing-Ton]]
- **HF Z-Image gratis ZUERST (~8/Tag), dann Higgsfield z_image (0,15 Cr).** Reihenfolge Pflicht.
- **Animation als Video-Clip in der Pipeline:** `short.py` nimmt jetzt `{"clip":...}`-Shots (Animation-Opener + Karaoke). Banner ok für Retention.
- **analyse.py + Retrieval macht Claude autonom/kostenlos mit allen Zugriffen; n+1 ist IMMER die Regel** — jedes Video/jeder Schritt wird täglich besser, nichts wird vergessen.
- **Vor JEDER Produktion:** `YouTube-Knowledge/00-System/Produktion-Pflichtliste.md` vollständig lesen — alle 13 Learnings (inkl. Animation-Library), Werkzeug-Checklist, Konkurrenz-Referenz. Kein Schritt vorher.
- **Obsidian: NICHT einführen (25.08. getestet).** Kein Connector vorhanden; brächte Claude nichts (Direktzugriff via Dateisystem/Grep ist besser). Vault bleibt reines Markdown. → [[Decision-Obsidian-nicht-noetig]]
- **Bild-Übersicht pro Short zur Validierung (Nutzer 25.08.):** ab jedem Projekt vorab Kontaktabzug (S01-01…) zeigen, bis der Nutzer blind vertraut.
- **Werkzeuge AUTONOM einsetzen (nicht nur installiert, Nutzer 25.08.):** `tools/nb_suggest|trends|openverse|tts|upscale|views90.py` + **Manim** (`tools/manim_scenes.py`) als Standard-Weg für Erklär-Animation (Querschnitt/Zeitleiste/Karte). Ganze Pipeline: `/video`. **Volles Repertoire (MCP+Skills+Tools+Engines) → [[Werkzeug-Register]] bei jeder Produktion konsultieren.** → [[Werkzeuge-Installiert]]
- **Analytics-Loop pro Video:** Tag 4–5 AVP%/CTR/Retention ziehen → Post-Mortem → nächstes Video steuern. → [[Analytics-Loop]]
- **Schedule bündig 3 Shorts/Tag, durchlaufend (Nutzer-Regel 25.08.).** Slots 10:30/14:30/18:00 UTC. Endet eine Short-Reihe mitten am Tag, wird der Rest mit den ersten Shorts der nächsten Geschichte aufgefüllt — kein 2er-Tag, keine künstliche Frisch-Start-Ausrichtung. → [[Produktions-Runbook]] Abschnitt 5
- **Retrieval IMMER autonom, n+1 (Nutzer 25.08.).** Vor jedem Schnitt still alle Learnings der Vorvideos ziehen (jedes Video baut auf allen vorherigen auf) — nicht ankündigen, einfach tun.
- **Szenen pro Short 2–6; nur Schlüsselszene(n) KI, Rest aus dem Netz (Nutzer 25.08.).** Web-Download (Wikimedia Commons/CC) läuft autonom + getestet. → [[Learning-Bilder-Prompts]]
- **Claude kann UND soll animieren (Nutzer 25.08.) — strategische Richtung.** Nicht „billig", sondern **wachsende Qualität** (SVG+JS → Chromium/Playwright → ffmpeg; Remotion als Ausbaustufe). Animation kann Opener sein, muss aber nicht — **wo sie passt**. **Langfristiges Ziel: weg von Standbild+Voiceover, hin zu echter Animation.** → [[Experiment-Cheap-Animation-Querschnitt]]
