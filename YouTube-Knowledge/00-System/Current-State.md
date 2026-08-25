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
- **Gemessen 24.08. (`analyse.py`):** **37 Abos**, 18.742 Aufrufe, 36 Videos. Wachstum 2→9→37. **Starke Woche:** Amazonas-Serie zieht („92 Passagiere. 1 Überlebende." 1.807; dazu 1.230/1.172/1.121/1.107).
- Konto vidIQ: `kisha-ners@gmx.de`. Guthaben (19.08.): **30** (renewable 0/150,
  Add-on 30/80, refresh 15.09.2026). vidIQ nur auf Anfrage — Credits schonen.

## Videos (siehe Video-Gedächtnis)
- [[Video-01-Tham-Luang]] — veröffentlicht. 640 Aufrufe, 2 Abos. Langvideo 4,4 % Haltequote → Shorts tragen.
- [[Video-02-San-Jose]] — fertig + terminiert (11 Shorts + Langvideo, 18.–20.08.).
- [[Video-03-Koepcke]] — fertig, hochgeladen, terminiert 21.–24.08. (10 Shorts, 3/Tag). Titel-Score Short 1: 74/100.
- **Video 4 (Okene/Jascon-4) PRODUZIERT + terminiert (24.08.):** 10 Shorts gerendert, **9/10 geplant** (24.–27.08.); Short 10 offen wg. YouTube-Tages-Uploadlimit → Retry 25.08. Siehe [[Video-04-Okene]], [[Produktions-Runbook]].
- **Video 5 Lengede PRODUZIERT (24.08.):** 10/10 gerendert; Upload/Schedule (28.–31.08.) läuft per Trigger 25.08. Siehe [[Video-05-Lengede]].
- **Nächste Session:** Konstrukt-Auditor (Aufgabe 2) + Tagesabschluss (Aufgabe 3) offen. **Voller Tagesstand: [[Handoff-2026-08-24]] (zuerst lesen).** Themen morgen: Nutty Putty + Prosperi ([[Ideen-Pipeline]]).

## Zugänge (Stand 19.08.)
- **YouTube Data + Analytics API:** OAuth-Refresh-Token gültig, Uploads/Analytics/Terminierung produktiv.
- **git push: FREIGESCHALTET (25.08.)** — funktioniert. **Persistenz = Git (Repo) primär**: `git commit` + `git push` am Session-Ende → nächster Container klont den vollen Stand automatisch. Drive ist damit **optional** (nur noch Nutzer-Ansicht/Asset-Transfer). Branch: `claude/implementation-guardrails-vszcn7`.
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
- **Analytics-Loop pro Video:** Tag 4–5 AVP%/CTR/Retention ziehen → Post-Mortem → nächstes Video steuern. → [[Analytics-Loop]]
