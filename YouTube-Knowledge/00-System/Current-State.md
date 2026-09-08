---
type: system
title: Current-State
status: active
updated: 2026-09-07
tags: [system, state]
---

# Current-State — aktueller Stand

> Diese Note ist der **operative Schnappschuss**. Sie wird bei jeder Session
> aktualisiert (Stand-Zahlen kommen aus `analyse.py`, nicht aus dem Gedächtnis —
> gemessenes gewinnt gegen notiertes). Letztes Update: **2026-08-31 (Tagesabschluss)**.

> **Selbstprüfung (Session-Start):** Liegen `YouTube-Knowledge/` und `analyse.py` im Checkout? Dann bist du aktuell. Falls nein → `git pull origin main` (Recovery-Schritte in `CLAUDE.md`, „⚠️ ZUERST"). **`main` trägt immer den vollen Vault-Stand** — jede Session mergt am Ende auf `main` (`/merken` Schritt 2). Branch-Namen wechseln je Session; der richtige Checkout ist jeder, der **diesen Vault + `tools/`** enthält.

## ⚠️ GENERALÜBERHOLUNG 07.09.2026 — was sich geändert hat

**Befund:** Das n+1 scheiterte nicht an fehlendem Wissen. Das Wissen war
vollständig und richtig. Es fehlte an **jeder** Stelle ein Mechanismus, der
eine Regel erzwingt. Null von fünf Produktionsregeln hatten einen Prüfpunkt im
Code — alle fünf wurden gebrochen, während sie galten.
Vollständig: [[Decision-Harte-Gates-statt-Prosa]] · [[Failure-Memory]] F-V9-A…E.

**Gemessen am 07.09. (`tools/kp_metrik.py`):** 71 Abos · 59.453 Aufrufe · 86 Videos.
AVP% je Serie (Anteil des Shorts, der gesehen wird — wächst NICHT mit dem Alter):

| Serie | AVP% | Aufrufe@2–3 Tage |
|---|---|---|
| V1 Tham Luang | 76,4 | nie gemessen |
| V3 Koepcke | 71,9 | 1.212 |
| V4 Okene | 64,2 | 1.702 |
| V5 Lengede | 64,9 | **nie gemessen** |
| V6 Nutty Putty | **53,6** | **nie gemessen** |
| V7 Prosperi | 69,3 *(erst 3/10)* | 993 |

**Der gesehene Anteil fällt** (76 → 54), während der Autonomie-Score von 48 auf
88 stieg. V5 und V6 (20 Videos) sind **dauerhaft unbewertbar**, weil die
Snapshots am 29.08. aufhörten — nicht nachholbar.

**Was jetzt erzwungen wird (kein Abhaken mehr):**
- `tools/kp_gate.py <serie>` — Herkunft · Captions gegen Skript · Bewegung · Ton
- `tools/kp_gate.py <serie> --nachher` — prüft das **fertige Video** (Untertitel im Bild)
- `.claude/hooks/pre-tool-use.py` — hält Render/Upload physisch an (Exit 2)
- `tools/kp_skript.py` — Skript-Herkunft per sha256 (`QUELLE.json`)
- `tools/kp_metrik.py` — Zahlen aus der Analytics-API statt Selbst-Score
- `tools/kp_ersetzen.py` — terminierte Shorts sicher austauschen
- `tools/tests/test_pre_tool_use.py` — 12/12, der Riegel sperrt UND lässt durch

**Was am 07.09. behoben wurde:**
- V8 Ralston: 5 von 10 terminierten Shorts (01, 03, 06, 07, 10) waren reine
  Standbild-Diashows trotz Bewegtbild-Pflicht seit 31.08. → neu gerendert mit
  je einer Manim-Szene in Sekunde 1 + 4 Bildern, neu hochgeladen, alte gelöscht,
  Termine unverändert (08.–11.09.). Neue IDs in `ralston/upload_log.json`.
- Neue Manim-Klassen: `RalstonNiemandWeiss`, `RalstonTiefe`, `RalstonAbschied`,
  `RalstonFuenfteNacht` + **neu** `StundenBogen` (§0c erfüllt).
- **Alle** Manim-Szenen liefen bisher in einer ~3× zu großen Bühne (F-V9-E) →
  im Hochformat jetzt `frame_height=16`, `frame_width=9`.
- `hoeren.py` schreibt `*.gehoert.txt` statt `short_XX.txt` — ASR kann nie mehr
  wie ein Nutzer-Skript aussehen.

**Zweite Runde am 07.09. (nach dem ersten Durchgang):**
- **Regel-Register gebaut** (`tools/kp_regeln.py`): 22 von 24 Regeln haben
  einen Prüfpunkt. Erzeugt [[Regel-Register]]. Eine Regel ohne Prüffunktion
  erscheint überall als UNGEDECKT — Prosa zählt nicht mehr als Durchsetzung.
- **Ablauf-Dirigent** (`tools/kp.py`): leitet aus dem echten Zustand ab, was
  als Nächstes dran ist. Läuft automatisch beim Sitzungsstart.
- **Tages-Snapshot läuft automatisch** im Session-Hook — der Schaden aus
  Befund 4 kann sich nicht wiederholen.
- **Shorts 04 und 05 trugen Prosperis Geschichte** („allein in der Sahara",
  „10 Tage — Mauro Prosperi") — universelle Manim-Klassen mit fremden
  Vorgabewerten (F-V9-F). Ersetzt durch `RalstonMeissel`, `RalstonInschrift`,
  `Ralston65Minuten`.
- **Der ganze Kanal lief 8 dB zu leise** (−22 statt −14 LUFS, F-V9-G).
  Gefunden von der neu gebauten Regel R18, nicht durch Hinhören.
  Tonkette korrigiert, alle 10 Ralston-Shorts liegen jetzt bei −15 LUFS.
- **Alle 10 Ralston-Shorts neu gerendert und ausgetauscht.** 01–05 am
  07.09., 06–10 am 08.09. (Tageslimit abgewartet). Sendeplan sauber:
  7 terminiert, keine Dubletten, Termine unverändert. Die Marke
  `austausch_offen` hat den offenen Rest über den Container-Neustart
  getragen — der Nutzer musste nichts ansprechen.
- Zwei Messfehler in meinen eigenen Prüfwerkzeugen gefunden und behoben
  (F-V9-H): falsche Helligkeitsschwelle, unterdrückte ffmpeg-Ausgabe.

**Bildherkunft (08.09.):** `nb_openverse.py` war seit jeher wirkungslos und
meldete das nicht (F-V9-R) — repariert, meldet jetzt Fehler mit Exit-Code.
Neu: `tools/nb_commons.py` für Wikimedia-Commons-Kategorien; die Regel nannte
diese Quelle seit Wochen, das Werkzeug fehlte (F-V9-S). Beide schreiben
`HERKUNFT.json` mit Lizenz und Urheber neben die Bilder.

**Themenfremde Bilder (08.09.):** Acht Bilder im Nutty-Putty-Langvideo hatten
keinen Bezug zum Stoff, bei grünem Gate (F-V9-T). Neuer Mechanismus:
`<serie>/bilder/AUSSORTIERT.json` (Bild → Grund, nichts wird gelöscht),
ausgewertet von `bild_ausgeschlossen()` in `kp_regeln.py`, aufgerufen von
`nb_lang.py`. Die beiden Entscheidungsdateien sind ausdrücklich **nicht**
gitignoriert — sonst wäre die Entscheidung im nächsten Container weg.

**Langvideos (08.09.):** Der Kanal hatte **2 bei 86 Videos**. Neu gebaut und
hochgeladen: **Ralston** `m5YYT5FNrgk` (5:51, terminiert 12.09.) und
**Prosperi** `DgYMVuBmzCM` (3:42, terminiert 13.09.). Nutty Putty, Lengede und
Okene sind gebaut oder bereit (Metadaten angelegt, Termine 14.–16.09.);
Lengede und Okene **ohne Untertitel**, weil für sie kein belegtes Skript
existiert. San José: nur die fertigen Shorts vorhanden → nur Montage aufs
Querformat möglich, sichtbar schwächer.

Werkzeuge dafür: `tools/kp_longform.py` (ein Uploader für alle Serien),
`tools/kp_drive_holen.py` (Material aus Drive), `tools/kp_captions.py`
(Captions serienweit aus dem Skript), `nb_lang.py --ohne-captions`.

**⚠️ OFFEN — Nutzer-Entscheidung nötig:**
- **Alle 10 Prosperi-Shorts sind LIVE mit falschen Captions** („Marathon des
  Apples", „Hartrigt Bauer", „Kincea"/„Kindsjahr" statt „Cinzia", „Jeb" statt
  „Jeep"). Ersetzen bedeutet: Aufrufe und Alter gehen verloren. **Nicht
  angefasst** — deine Entscheidung.
- `nb_contrarian.py` Produktions-Teil ist wirkungslos (F-V9-C). Vorschlag:
  wissenschaftlichen Teil behalten, Produktions-Teil auf `kp_gate.py` verweisen
  lassen. **Nichts gelöscht** (Guardrail #1/#9).
- V8 Short 07 heißt „Vier Nächte allein im dunklen Canyon", das Skript sagt „in
  der fünften Nacht". Titel nicht geändert — Titel sind deine Domäne.

---

## Nordstern-Ziel (messbar)
- **YPP-Monetarisierung, Shorts-Pfad: 1.000 Abos + 10 Mio Shorts-Views in 90 Tagen** (vor der Feb-2027-Regel). Stand 31.08. (analyse.py): Abos **6,3 %** (63/1.000), Views **0,53 %** (53.229/10 Mio). Wachstum: +21 Abos, +32.900 Views seit 25.08. Realistischer Horizont: Abos 3–5 Monate, 10-Mio-Views 9–12 Monate. **Fortschritt jede Session loggen** → [[Ziel-YPP-Monetarisierung]].

## Kanal
- *Katastrophenprotokoll* (`UC1KCzLNlgGiYsLNQ7Z0HA-g`, DE), gegründet 15.08.2026.
- **Gemessen 01.09. (analyse.py):** **68 Abos**, **57.783 Aufrufe**, **60 Videos**, **26 terminiert**. Wachstum Abos: 42(25.08)→58(29.08)→63(31.08)→68(01.09). *(Vor Produktion neu ziehen — analyse.py schlägt diese Notiz.)*
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
- **Video 8 Ralston ABGESCHLOSSEN + HOCHGELADEN (31.08.):** Aron Ralston / 127 Stunden, 10 Shorts terminiert 08.–11.09. Diese Session neu gerendert mit **Caption-Fix (F-V8-E)**: Captions kamen aus ASR → „Aron Rallsturm", „jemes Franco", „Protesse"; jetzt aus dem Skript via `align.py`. **§0d-Selbst-QC (videoblick.py + hoeren.py) hat die Fehler VOR Upload gefangen** — erster Ernstfall des Riegels, bestanden. Alte 10 YT-Videos gelöscht, 10 neue hoch (IDs neu in `ralston/upload_log.json`). Multi-Shot/Karaoke/Progressbar/CTA verifiziert. **Offen: Longform `render/long.mp4` noch nicht gebaut** (`python3 lang.py ralston/` → `nb_upload.py --longform`).
- **Nächste Geschichte: V9 Loveparade Duisburg 2010.** Nächste kostenlose Technik (Capability-Gate §0c): Image-to-Video via HF (Wan2.1-I2V) ODER Remotion real einsetzen. Nutzer liefert Skript frisch.

## Aktuell wichtigste offene Punkte (Stand 31.08.)
1. **Ralston-Longform bauen + hochladen** — einziger offener Rest der V8-Reihe.
2. **V9 Loveparade** — auf Nutzer-Skript warten, dann §0a–§0d durchziehen (Capability-Gate: ≥1 neue Gratis-Technik).
3. **Analytics-Loop V8** — ab ~Tag 4 nach Publish (12.09.) CTR/Retention der Ralston-Shorts ziehen, gegen Okene-Benchmark (beste Serie) prüfen.
- **Voller Tagesstand: [[Audit-2026-08-25]] + [[Audit-2026-08-26]].**

## ⭐ Stehende Regeln seit 31.08. (für nächste Produktion — Loveparade)
Diese gelten ab jetzt automatisch, ohne Nutzer-Nachfrage:
- **Bewegtbild-Pflicht:** jeder Short öffnet mit **Bewegung in Sekunde 1**, ≥1 bewegter Schlüssel-Shot (Manim/Remotion/Wan2.1-I2V). Blockierend im §0d-QC. → [[Short-Konzept-Blueprint]]
- **Captions IMMER aus Skript** via `align.py`, nie roh-ASR (F-V8-E). `nb_build.py captions()` erledigt das; Skript als `<serie>/skript/short_XX.txt` ablegen.
- **Titel-Open-Loop** („…dann [Cliffhanger]"), Confidence HIGH (CTR-Beleg). → [[Learning-Titel]], [[CTR-Benchmark-2026-08]]
- **§0d Selbst-QC** (videoblick + hoeren) vor JEDEM Upload · **§0c** ≥1 neue Gratis-Fähigkeit je Reihe.
- **Konkurrenz-/Analyse-Pflicht:** immer visuell (Bild/Schnitt/Hook), nie nur Metadaten. **Gekoppelt ans Asset-Sourcing (Nutzer 01.09.):** beim Stock-/Bild-Suchen je Thema zusätzlich themen-spezifische Konkurrenten UND **Evergreens** ansehen (echte Frames+Ton via `watch`/`videoblick`/`hoeren`) und Schnitt/Bildsprache adaptieren. → Pflichtliste §4 Schritt 1.
- **Kanonischer Prozess:** [[Produktion-Pflichtliste]] (Detail: [[Produktions-Runbook]] · [[Schnitt-Protokoll]]).
- **Nächste 10 Videos:** [[Ideen-Pipeline]] §Schlachtplan (Loveparade + Anden = Breakout-Versuche).

## Zugänge (Stand 19.08.)
- **YouTube Data + Analytics API:** OAuth-Refresh-Token gültig, Uploads/Analytics/Terminierung produktiv.
- **git push: FREIGESCHALTET (25.08.)** — funktioniert. **Persistenz = Git (Repo) primär**: `git commit` + `git push` am Session-Ende → nächster Container klont den vollen Stand automatisch. Drive ist damit **optional** (nur noch Nutzer-Ansicht/Asset-Transfer). **Alle MCP-/Zugriffe freigegeben (25.08.).** Branch-Namen wechseln je Session (`claude/…`); **`main` wird jede Session mitgepusht und ist aktuell** → neue Sessions starten garantiert korrekt, egal ob sie `main` oder den Feature-Branch ziehen.
- **Netzsperre:** aufgehoben (17.08.). elevenlabs/higgsfield/youtube erreichbar.
- **TikTok über Buffer:** @mausigermax verbunden (`acydacy3@gmail.com`).

## Werkzeuge
- **Whisper** (`faster-whisper small-de int8`) = Standard-Transkription; Vosk nur Offline-Fallback. Siehe [[Decision-Whisper-statt-Vosk]].
- **Bild-Engines:** Nano Banana Pro + Seedance (Figur/Hero), Z-Image (Landschaft, 0,15 Cr.). Siehe [[Decision-Bild-Engine-Wahl]].
- **claude-youtube** Skill (als claude.ai-Skill), yt-dlp (via deno), gdown.
- **NEU (01.09.) Video-Engines vendored → weg von Standbild, hin zu Animation/Schnitt:** Skills **`video-shotcraft`** (Remotion-Motion-Design, echter Render getestet), **`video-use`** (Schnitt/Grade/Overlay per Gespräch, gratis-Transkript via faster-whisper), **`watch`** (ansehen+hören für QC/Konkurrenz) + Tool **OpenMontage** (Remotion/HyperFrames). Deps im frischen Container: `bash tools/nb_install_video_engines.sh <core|shotcraft|video-use|watch|openmontage|all>`. Voll dokumentiert: [[Werkzeug-Register]] §H. Diese Engines bedienen die Bewegtbild-Pflicht + §0c-Capability-Gate. `open-design` bewusst nicht vendored (GUI-App).

## Offene Experiment-/Analytics-Fragen
- Längen-These **aufgelöst (24.08., n=35):** Faktor 0,9 statt 7,9 → Hook schlägt Länge (auf Aufruf-Basis; **AVP%/3-s-Retention für V3 steht aus**, ~2 Tage Analytics-Lag). → [[Learning-Retention-und-Laenge]]
- Hook-Banner mit abweichendem Text: nie belegt besser → [[Experiment-Hook-Banner-abweichender-Text]].
- TikTok-Hashtag-Wahl stützt sich auf YouTube-Volumen (schwächster Punkt) → [[Frage-TikTok-Hashtag-Volumen]].

## 5 Inhalts-Säulen (operativ ab sofort)
1. **„Sie hätten sterben müssen"** — Person + unmögliche Situation + Zahl + Überleben
2. **„Die Rettung war eigentlich unmöglich"** — chancenlose Rettung als Kernversprechen
3. **„Ein Fehler löste alles aus"** — Single point of failure → Katastrophe
4. **„Katastrophe in Echtzeit"** — Timer-Erzählung (gut für Longform)
5. **„Der Moment, in dem alles vorbei schien"** — emotionaler Wendepunkt isoliert

**Kernidentität:** Nicht „Doku über Katastrophe X", sondern „Mensch in unmöglicher Situation".
**Angle-Extraktion:** Pro Story 20 mögliche Angles generieren → stärkste 8–10 produzieren. Jeder Short steht allein.
**Story-Score:** Unmögliche Prämisse (25%) + Menschliche ID (20%) + Visuell (15%) + Twist (15%) + DE-Nische (10%) + Suche (10%) + Longform (5%) → Schwelle ≥ 70.

## Neue Referenz-Kanäle (27.08.)
- **Spds**: 39 Videos, 43+ Mio Views — Proof: Qualität > Quantität
- **Der Soldat spricht**: 25 Mio Views, 319 Videos — DE-Publikum nimmt sachlich-dramatische Shorts an
- **Tap Thrill**: Schnell wachsender DE-Storytelling-Shorts-Kanal — beobachten

## Neue Rules aus Competitor-Analyse (promoted 27.08.2026)
- **„| Doku" aus Titeln streichen** — „Doku" in Description + Tags, NICHT im Titel. Kein Top-Performer der Konkurrenz nutzt Genre-Labels.
- **Personennamen gezielt im Titel** wenn Person google-bar ist (Otto Warmbier…) — nicht in jeden Short-Titel der Reihe, nur wo es natürlich passt (typisch 1–2 Shorts). Bestehende Videos: kein Titel-Edit (Performance-Risiko), nur Description nachbessern wenn Name fehlt. Ab V8: von Anfang an einplanen.
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
- **Vor JEDER Produktion:** `YouTube-Knowledge/00-System/Produktion-Pflichtliste.md` vollständig lesen — alle in §2 gelisteten Pflicht-Dateien (Learnings + Failure-Memory + Animation-Library), Werkzeug-Checklist, Konkurrenz-Referenz. Kein Schritt vorher.
- **Bild-Übersicht pro Short zur Validierung (Nutzer 25.08.):** ab jedem Projekt vorab Kontaktabzug (S01-01…) zeigen, bis der Nutzer blind vertraut.
- **Werkzeuge AUTONOM einsetzen (nicht nur installiert, Nutzer 25.08.):** `tools/nb_suggest|trends|openverse|tts|upscale|views90.py` + **Manim** (`tools/manim_scenes.py`) als Standard-Weg für Erklär-Animation (Querschnitt/Zeitleiste/Karte). Ganze Pipeline: `/video`. **Volles Repertoire (MCP+Skills+Tools+Engines) → [[Werkzeug-Register]] bei jeder Produktion konsultieren.** → [[Werkzeuge-Installiert]]
- **Analytics-Loop pro Video:** Tag 4–5 AVP%/CTR/Retention ziehen → Post-Mortem → nächstes Video steuern. → [[Analytics-Loop]]
- **Schedule bündig 3 Shorts/Tag, durchlaufend (Nutzer-Regel 25.08.).** Slots 10:30/14:30/18:00 UTC. Endet eine Short-Reihe mitten am Tag, wird der Rest mit den ersten Shorts der nächsten Geschichte aufgefüllt — kein 2er-Tag, keine künstliche Frisch-Start-Ausrichtung. → [[Produktions-Runbook]] Abschnitt 5
- **Retrieval IMMER autonom, n+1 (Nutzer 25.08.).** Vor jedem Schnitt still alle Learnings der Vorvideos ziehen (jedes Video baut auf allen vorherigen auf) — nicht ankündigen, einfach tun.
- **Szenen pro Short 2–6; nur Schlüsselszene(n) KI, Rest aus dem Netz (Nutzer 25.08.).** Web-Download (Wikimedia Commons/CC) läuft autonom + getestet. → [[Learning-Bilder-Prompts]]
- **Claude kann UND soll animieren (Nutzer 25.08.) — strategische Richtung.** Nicht „billig", sondern **wachsende Qualität** (SVG+JS → Chromium/Playwright → ffmpeg; Remotion als Ausbaustufe). Animation kann Opener sein, muss aber nicht — **wo sie passt**. **Langfristiges Ziel: weg von Standbild+Voiceover, hin zu echter Animation.** → [[Experiment-Cheap-Animation-Querschnitt]]

## Session-Ende-Log: 27./28.08.2026

### Erledigte Aufgaben (diese Session)

**Playlists erstellt (alle 5 fehlenden Reihen):**
- V3 Koepcke `PLNjurTl75o48` — 11/11 Videos
- V4 Okene `PLTK8wu63dmls` — 9/9 öffentliche Videos (1 private korrekt übersprungen)
- V5 Lengede `PLc1loqPA51r4` — 10/10 Videos
- V6 Nutty Putty `PLPOAfNkl0mRA` — 10/10 Videos
- V7 Prosperi `PLWNMREfuPoq0` — 10/10 Videos

**Titel aller scheduled/privaten Videos überarbeitet (30/30):**
- V5 Lengede (10 Shorts), V6 Nutty Putty (10 Shorts), V7 Prosperi (10 Shorts)
- Kein „| Doku" mehr. Paradox-Hooks, Staccato-Punkte, gezielt Personennamen eingesetzt.
- Umlaute korrekt (Männer, stürzen, verschüttet — kein ASCII-Workaround mehr).

**System-Upgrades operativ:**
- Story-Score (Produktion-Pflichtliste §0a) — 7-Faktor-Bewertung, Schwelle ≥70
- Angle-Extraction (§0b) — 10–20 Hooks → stärkste 8–10 produzieren
- 5 Inhalts-Säulen als Kern-Identität (→ Current-State.md + Competitor-Learning)
- Neue Referenzkanäle: Spds, Der Soldat spricht, Tap Thrill

**Learnings korrigiert und gepusht:**
- Learning-Competitor-Strategie.md vollständig neu geschrieben (Confidence-Fehler bei Short-Länge behoben)
- Learning-Retention-und-Laenge.md: 3-Gruppen-Test ab V8 präzisiert
- Learning-Titel.md: Personennamen-Regel präzisiert (selektiv, nicht retroaktiv)
- Learning-Thumbnails-Cover.md: Shorts-Thumbnail-Regel korrigiert (Upload möglich, aber kein neues Material)
- Guardrail permanent: „Externe Competitor-Daten dürfen niemals eine intern gemessene Rule überschreiben"

### Nächste Session — sofort beginnen mit
1. **V03 Koepcke SEO (Sofortmaßnahme):** Description + Tags ergänzen: „Juliane Koepcke", „juliane koepcke deutsch", „juliane koepcke doku" — NUR Description/Tags, KEIN Titel-Edit (Video live)
2. **V8 Aron Ralston:** Nutzer liefert Skript → sofort produzieren (Story-Score, Angle-Extraction, Hook-Pool vorbereitet)
3. **Längen-Experiment ab V8:** Gruppe A/B/C (20–30s / 30–45s / 45–60s) planmäßig integrieren
4. **„Ähnliche Videos" in YouTube Studio:** Manuell für wichtigste Videos eintragen (API nicht verfügbar — Playlists sind das API-Äquivalent, Done)
