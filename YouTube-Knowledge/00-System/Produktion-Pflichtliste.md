---
type: system
title: Produktion-Pflichtliste
status: active
updated: 2026-08-31
tags: [system, pflicht, n+1, produktion]
---

# Vor jedem Produktionsschritt — Pflichtliste (n+1)

> **⭐ DIES IST DER KANONISCHE PRODUKTIONSPROZESS.** Immer lesen, bevor ein Video produziert, geschnitten, getextet oder hochgeladen wird. Kein Schritt übersprungen, kein Werkzeug ausgelassen. Autonome Ausführung ist Pflicht, nicht Option.
> **Zwei Detail-Ebenen darunter** (keine konkurrierenden Prozesse): [[Produktions-Runbook]] = konkrete Pipeline-Mechanik (gdown, Render-Cap, Upload-Limit, Schedule) · [[Schnitt-Protokoll]] = Schnitt-/Caption-Detailspecs. Der Ablauf/Prozess selbst steht HIER.

---

## 0a. Story-Score (bei jeder NEUEN Geschichte, vor Skript-Anforderung)
Bewerte die Geschichte intern nach:
- Unmögliche Prämisse (25%) · Menschliche ID (20%) · Visuell (15%) · Twist (15%) · DE-Nische (10%) · Suche (10%) · Longform (5%)
- **Schwelle: ≥ 70 Punkte** — darunter entweder besseren Angle suchen oder Geschichte zurückstellen.

## 0b. Angle-Extraktion (vor Schnitt-Beginn)
Für die aktuelle Geschichte: **10–20 mögliche Short-Hooks** aufschreiben.
- Jeder Hook muss alleine funktionieren — kein „Teil X".
- Die stärksten 8–10 produzieren. Nicht alle, die möglich wären.
- Frage per Hook: *Würde jemand, der diese Geschichte noch nie gesehen hat, genau hier stehen bleiben?*

## 0c. Capability-Integration-Gate (n+1 — PFLICHT je Reihe, autonom)
> **Warum:** V8 scheiterte nicht an fehlenden Werkzeugen, sondern daran, dass vorhandene nicht genutzt wurden. Dieses Gate erzwingt Fortschritt statt Stillstand. Das System schlägt selbstständig kostenlose Fähigkeiten vor und integriert sie — der Nutzer muss HF/Manim/Remotion/Canva/vidiq/SEO nie selbst ansprechen.
1. **Scannen** (30 s, kostenlos): [[Werkzeug-Register]] + Live-Repertoire (MCP-Konnektoren, Skills, Plugins, `tools/`). Startbericht listet den aktuellen Stand.
2. **Vorschlagen:** Welche **kostenlose** Fähigkeit, die im letzten Zyklus NICHT genutzt wurde, hebt dieses Video messbar (Retention, CTR, Watch-Time, Produktionsqualität)? Reihenfolge: **gratis zuerst** (HF Z-Image · Manim · Remotion · Openverse/Commons · Piper · searchfit-seo · Canva-Free), Credits nur für Peak.
3. **Integrieren:** Mindestens **eine** neue kostenlose Fähigkeit pro Reihe real einsetzen — nicht ankündigen, tun. Wenn wirklich keine passt: in einem Satz begründen (echte Ausnahme, kein Default).
4. **Persistieren:** Entscheidung + Ergebnis in [[Werkzeug-Backlog]] (erledigt/offen) und [[Autonomie-Log]] eintragen. Neue Fähigkeit erstmals genutzt → [[Werkzeuge-Installiert]] + [[Werkzeug-Register]] updaten.
> Verknüpft mit Anti-Stall §7: 3 Reihen ohne neue Fähigkeit = harter STOPP.

## 0d. Selbst-Wahrnehmungs-QC (PFLICHT vor Upload — der Anti-V8-Riegel)
> **Der eigentliche V8-Fehler:** unsichtbare Progressbar, Karaoke ohne Highlight, Einzelbild statt Multi-Shot, Dot-Animation ohne Kontext — alle **hochgeladen, weil das Ergebnis nie angesehen/gehört wurde.** Ein Werkzeug allein reicht nicht; das Rendern muss geprüft werden.
Vor JEDEM Upload, für **mindestens 2 Stichproben-Shorts** (immer #01 + der komplexeste):
```bash
python3 videoblick.py render/short_XX.mp4   # in Einzelbilder zerlegen → mit Read ANSEHEN
python3 hoeren.py render/short_XX.mp4        # Tonspur/VO HÖREN → gegen Skript abgleichen
```
Gegen die [[Failure-Memory]]-Checkliste prüfen (jede Zeile bewusst abhaken):
- [ ] **BEWEGUNG in Sekunde 1** (bewegter Schlüssel-Shot/Animation, kein ruhiges Standbild-Establishing)? → Anti-Diashow, Hook/Retention. [[Short-Konzept-Blueprint]]
- [ ] **≥1 bewegter Schlüssel-Shot** im Short (I2V/Remotion/Manim), nicht nur Ken-Burns?
- [ ] Progressbar sichtbar (≥18 px, gelb, kein Alpha)?
- [ ] Karaoke-Highlight `\kf` läuft wortweise mit?
- [ ] **Caption-Text = Nutzer-Skript, Eigennamen KORREKT** (keine ASR-Verstümmelung wie „Rallsturm"/„jemes Franco")? Captions kommen aus `skript/short_XX.txt` via `align.py`, nie aus roher ASR (F-V8-E). Stichprobe lesen.
- [ ] Multi-Shot (mehrere Bilder/Beat), kein statisches Einzelbild?
- [ ] Animationen tragen Label + ≥3 Elemente (kein nackter Dot)?
- [ ] CTA „Kanal folgen" in den letzten 4 s sichtbar?
- [ ] VO verständlich, −16 LUFS, Musik hörbar aber nicht drüber?
**Ein Fehler → nicht hochladen, neu rendern.** Kein Upload ohne diesen Blick.

## 0. Contrarian-Gate (IMMER VOR RENDER/UPLOAD — ~10 s)
```bash
python3 tools/nb_contrarian.py <short.json>   # automatische Konfig-Prüfung
python3 tools/nb_contrarian.py --kurz         # nur HIGH+VERY_HIGH ohne Konfig
```
Prüft **alle Domänen**: Ton · Hook · Captions · Titel · SEO · Bilder · Retention · Upload · Persistenz.
Kein Video wird gerendert oder hochgeladen, bevor der Contrarian grün ist.
Vollständiger Strategie-Audit (wöchentlich): `python3 tools/nb_contrarian.py` ohne Argumente.

---

## 1. Zahlen holen + Observations generieren (autonom, ~15 s)
```bash
python3 tools/nb_analytics_snapshot.py   # Snapshot speichern (1×/Tag)
python3 tools/nb_observe.py              # Delta, Outlier, Experimente bewerten
python3 analyse.py                       # Detailbericht (Uploads, Termine)
```
- Snapshot-Delta: Views/Abos-Wachstum seit letztem Snapshot → erkennt was wächst.
- Observation Engine: rankt Top/Under, prüft Längen- und SEO-These, meldet Experimente die Daten haben.
- Ergebnis in [[Current-State]] eintragen wenn abweichend. Gemessenes schlägt Notiertes.
- Neue Observation? → `python3 tools/nb_observe.py --vault` (schreibt in `07-Analytics/Observations.md`).

---

## 2. Learnings LESEN — alle, vollständig (nicht aus dem Gedächtnis)

**Diese Tabelle IST die vollständige Pflicht-Leseliste** (keine feste Zahl — wächst mit neuen Learnings). Alle werden gelesen, bevor das erste Bild, der erste Satz oder das erste Tag entsteht:

| Datei | Was drin steht |
|---|---|
| `01-Learnings/Hooks/Learning-Hooks.md` | Hook-Formeln, Timing, was konvertiert |
| `01-Learnings/Retention-Laenge/Learning-Retention-und-Laenge.md` | Länge, tote Sekunden, sichere Zone |
| `01-Learnings/Captions/Learning-Captions.md` | Untertitel-Stil, Zeilenbruch, Rhythmus |
| `01-Learnings/Titles/Learning-Titel.md` | Keyword-Platzierung, Zeichenlimit, Formeln |
| `01-Learnings/SEO/Learning-SEO.md` | Tags, Beschreibung, Trend-Keywords |
| `01-Learnings/Bilder/Learning-Bilder-Prompts.md` | Prompt-Formel, Schlüsselszenen-Regel, Größen |
| `01-Learnings/Editing-Ton/Learning-Editing-Ton.md` | LUFS-Ziel, Musik-db, Ducking |
| `01-Learnings/Editing-Video/Learning-Editing-Video.md` | Render-Reihenfolge, Bildquellen, Backup |
| `01-Learnings/Storytelling/Learning-Storytelling-Shorts.md` | Narrationsbogen, Tempo, Cliffhanger |
| `01-Learnings/Storytelling/Short-Konzept-Blueprint.md` | Kopierbares Bauprinzip viraler Hits: Beats, Bewegtbild, Hook |
| `01-Learnings/Thumbnails/Learning-Thumbnails-Cover.md` | Cover-Regeln, Schrift, Kontrast |
| `01-Learnings/Topics/Learning-Topics-Themenwahl.md` | Nischen-Check, Sättigungsgrad |
| `01-Learnings/Topics/Learning-Competitor-Strategie.md` | Scary Interesting als Rollenmodell, Längenzone 40–55s, Themen-Lücken, Re-Run-Strategie |
| `01-Learnings/Cross-Platform/Learning-Cross-Platform-TikTok.md` | TikTok manuell, Buffer-Logik |
| `09-Failures/Failure-Memory.md` | Was nicht funktioniert hat — nicht wiederholen |
| `04-Animation/Animation-Library.md` | Welche Animations-Klassen existieren, was kommt als nächstes |

**Lesedauer: ~3 Minuten. Ersparnis durch vermiedene Fehler: unbegrenzt.**

---

## 3. Werkzeuge — vollständiges Repertoire prüfen (vor jedem Schritt)

**Bilder (Reihenfolge einhalten — kostenlos zuerst):**
- [ ] **HF Z-Image** (`mcp__huggingface__gr1_z_image_turbo_generate`) — gratis, ~8/Tag → IMMER zuerst ausschöpfen
- [ ] **Openverse** (`tools/nb_openverse.py "<q>" <dir>`) — CC-Pool für Stock/Broll
- [ ] **Wikimedia Commons** (`tools/nb_fetch_broll*.py`) — spezifische Kategorien, globaler Dedup-Set
- [ ] **Higgsfield Z-Image** (0,15 Cr) — nur für echte Schlüsselszenen wenn HF-Quota erschöpft
- [ ] **Higgsfield Cinematic** (teuer) — nur auf expliziten Nutzer-Wunsch

**Animation (Pflicht-Überlegung bei jedem Video):**
- [ ] **Manim** (`manim -qh -r 1080,1920 tools/manim_scenes.py <Szene>`) — Karten, Zeitleisten, Querschnitte → Standard für Erklär-Animation
- [ ] **Remotion** — in Training, schrittweise einsetzen wo Manim nicht reicht
- [ ] SVG+Playwright+ffmpeg — für einfache Animationen ohne Manim

**SEO/Recherche:**
- [ ] `tools/nb_suggest.py "<thema>"` — YouTube-Keywords
- [ ] `tools/nb_trends.py "<kw1>" "<kw2>"` — Trendvergleich

**Audio:**
- [ ] `tools/nb_tts.py "text" out.mp3` — Scratch-VO für Timing vor finaler VO (Piper de)
- [ ] VO-Ziel: **−16 LUFS**, Musik: **db=−16**, kein Boost

**Messen:**
- [ ] `tools/nb_views90.py` — 90-Tage-Views → [[Ziel-YPP-Monetarisierung]] loggen

**Vollständiges Repertoire (MCP-Konnektoren + Plugins):** [[Werkzeug-Register]]

---

## 4. Konkurrenz-Referenz + Bild-Strategie (PFLICHT vor Bild-Produktion)

> **REGEL (Nutzer 31.08.): Jede Analyse/Recherche erfasst IMMER das VISUELLE — Bildsprache, Schnittstil, Hook, Beat-Struktur, Caption-Stil, Audio — nie nur Metadaten (Views/Titel/Tags).** Metadaten sagen WAS läuft, nicht WARUM. Werkzeuge: `vidiq_watch_shortform_content` (szenenweise Analyse eines Shorts, ~10 Cr) · `videoblick.py` (Frames ansehen) · `hoeren.py`. Ergebnis-Standard + kopierbares Bauprinzip: [[Short-Konzept-Blueprint]] — vor jeder Produktion lesen.

**Schritt 1 — Top-Videos UND Evergreens zum Thema analysieren:**
> **REGEL (Nutzer 01.09.): Themen-spezifische Konkurrenz + Evergreens sind PFLICHT — und zwar gekoppelt an den Moment, in dem du Assets/Stock-Bilder suchst.** Bevor/während du Bilder für einen Short sourc(e)st, sieh dir zum konkreten Thema (hier: Loveparade / Massenpanik / Menschenmengen-Katastrophe) an: (a) die aktuellen Top-Shorts UND (b) **Evergreens** — zeitlose Dauerläufer, die seit Jahren Views ziehen (oft die besten Bildsprache-/Schnitt-Vorlagen). Lass dich von **Schnitt, Bildsprache, Kamerabewegung, Reveal-Timing** inspirieren — nicht von Metadaten. Nutze `watch`/`videoblick.py`/`hoeren.py`, um echte Frames + Ton zu sehen. Ziel: unsere Shots sollen visuell mit den Besten mithalten, in nüchterner Marke.
```
python3 tools/nb_suggest.py "<thema>"    # YouTube-Suche/Suggest (gratis)
python3 tools/nb_trends.py "<a>" "<b>"   # Google-Trends-Momentum (gratis)
```
→ Die Top-Videos **und Evergreens visuell** analysieren (nicht nur Titel lesen):
- Hook: erste 2s — Bewegung oder Standbild? Welcher Schock-Satz? Caption-Einblendung?
- Schnitt: Szenenlänge, Kamerabewegung, Anteil Bewegtbild vs Standbild.
- Struktur: Beats bis Payoff, Cliffhanger-Pause, Realitäts-Beweis am Ende?
- Bildsprache, Caption-Stil/Farbe/Position, Audio (Score/SFX).
→ Abgleich mit [[Short-Konzept-Blueprint]]: Was übernehmen, was widerspricht der nüchternen Marke?

**Schritt 2 — Referenz-Kanäle (persistent, immer prüfen):**
- **Scary Interesting** (UCNXvmGafmrtJ7VPSqjRRbwg) — **Primäres Rollenmodell.** 0,99%/Monat, ⌀ 1,21 Mio Views/Video. Rein narrativ, anonym, cinematisch. Was machen ihre besten Shorts visuell?
- **How to Survive Show** (UCOch_vMp7AKaiGE7e6kSHfg) — **Themen-Radar.** Breakout > 5 → 4–8 Wochen DE-Fenster. Longform-Thumbnail-Formel: unmögliches Bild.
- **Fascinating Horror** — Stil-Referenz: nüchtern, präzise, kein Reißerisches
- **Bright Sun Films** — unterirdische Orte, atmosphärische Bilder
→ Was machen Views-starke Videos visuell anders als wir? Welche Shots als Standbild funktionieren?

**Schritt 3 — Stock-Photo-Reverse-Engineering:**
Wenn ein Konkurrenz-Video ein starkes Bild nutzt:
1. Was ist die Kategorie (Wikimedia, Getty, Unsplash-Stil)?
2. Welches Keyword würde dieses Bild finden?
3. In `nb_openverse.py` oder Commons-Suche testen.
4. Ergebnis → [[Learning-Bilder-Prompts]] ergänzen.

**Schritt 4 — KI-Prompt aus Referenz ableiten:**
Starkes Competitor-Bild als Ausgangspunkt:
- Motiv: was genau ist zu sehen (Figur, Landschaft, Licht)
- Stilwörter: cinematic / documentary / 35mm / golden hour / moody
- Nicht kopieren — abstrahieren und besser machen.
- Prompt → Z-Image → Ergebnis in [[Learning-Bilder-Prompts]] mit Bewertung.

---

## 5. Bewegtbild-PFLICHT — Hook & Retention (jede Reihe, autonom, ohne Nachfrage)

> **STEHENDE REGEL (Nutzer 31.08., gilt bis zum nächsten Learning):** Bewegung schlägt Standbild-Diashow für Hook + Anfangs-Retention (belegt: virale Hits fahren ~90 % Bewegtbild, öffnen mit Bewegung — [[Short-Konzept-Blueprint]]). Der Nutzer muss das **nie** ansprechen. Bei JEDER Produktion:
> 1. **Sekunde 1 = Bewegung.** Der Hook-Shot ist bewegt (I2V/Remotion/Manim), nie ruhiges Establishing-Standbild. Blockierend im §0d-QC.
> 2. **Volles Bewegtbild-Repertoire prüfen — kostenlos zuerst:** **Manim** (Querschnitt/Karte/Zahl/Zeit) · **Remotion** (getemplatete Motion-Graphics, WordReveal, Lower-Thirds — endlich einsetzen) · **Wan2.1-I2V über HF** (Standbild→Bewegtszene, gratis) · **Ken-Burns** nur als Minimum, nicht als Standard · SVG+Playwright+ffmpeg für Einfaches. Higgsfield-Video nur wenn gratis nicht reicht.
> 3. **≥1 bewegter Schlüssel-Shot pro Short** (der Fels kippt, die Welle bricht, der Arm löst sich, der Querschnitt zoomt). Rein statische Shorts sind ab jetzt ein QC-Fehler.
> 4. Neue Bewegtbild-Technik erstmals genutzt → §0c-Gate: in [[Werkzeug-Backlog]] abhaken.

**Animations-Clips pro Reihe: so viele wie sinnvoll und qualitativ gut — kein Limit nach oben.** Jede Szene aktiv prüfen: Bewegung besser als Standbild? (Standard-Antwort ab jetzt: ja, wo es die Szene trägt.)

Animation-Bibliothek lesen: `YouTube-Knowledge/04-Animation/Animation-Library.md`

**Entscheidungsbaum:**
- Gibt es eine Zahl/Statistik im Skript? → `StatCounter`
- Gibt es eine Route/Karte? → `ProsperiMap`-Vorlage anpassen
- Gibt es eine Tages-Abfolge? → `SurvivalDays`
- Gibt es eine Suchaktion? → `SearchRadius`
- Gibt es eine Tiefe (Grube/Höhle/Wasser)? → `DepthDive`
- Gibt es einen engen Spalt/Tunnel? → `CrossSection`
- Gibt es eine Zeitleiste (Stunden)? → `Timeline`

**Pflicht:** Jede neue Reihe committet ≥1 neue Manim-Klasse. Backlog: [[Animation-Library]].

Remotion: schrittweise einführen. Nächster Schritt: `tools/remotion/` Setup + erste `WordReveal`-Komponente.

---

## 6. Was nie ausgelassen werden darf (auch wenn der Nutzer es nicht erwähnt)
- HF Z-Image-Quota vollständig nutzen (gratis → verschenkter Wert wenn nicht genutzt)
- Broll-Dedup-Set: globaler Set pro Produktion, kein Bild in 2 Shorts
- Bilder auf 1600×2848 skalieren vor Render
- VO auf −16 LUFS normalisieren
- Musik prüfen: `ffmpeg -af volumedetect` nach Render
- git commit+push am Ende jeder Session (auch unfertige Zwischenstände)
- [[Ziel-YPP-Monetarisierung]] Fortschritt loggen
- **LONGFORM pro Serie** — `metadata.json` muss `"longform"` enthalten; nach Short-Upload: `python3 <serie>/nb_upload.py --longform`. Long-Form baut Watch Time + Suchtraffic und zieht Abos. **Nie vergessen — `nb_upload.py` ohne `--longform` ist unvollständig.**

---

---

## 7. Anti-Stall-Checkpoints — Sicherheitsfallen gegen Kreisdrehen

**Vor Produktionsstart — diese Fragen beantworten (intern, 30 Sekunden):**

| Frage | Warnsignal wenn… |
|---|---|
| Welches neue Werkzeug oder welche neue Technik wende ich heute an, das/die ich im letzten Video NICHT benutzt habe? | Antwort ist „keines" → aktiv suchen |
| Welches Learning aus `09-Failures/` ist direkt relevant? | Ich erinnere mich nicht → Datei lesen |
| Habe ich die HF Z-Image-Quota schon genutzt? | Nein → sofort einplanen |
| Gibt es eine Animation (Manim/Remotion) die diese Geschichte besser erklärt als ein Standbild? | Ich habe nicht darüber nachgedacht → nachdenken |
| Welcher Competitor hat ein ähnliches Thema gemacht? Was hat er anders gemacht? | Ich weiß es nicht → nb_suggest + ansehen |

**Nach Produktionsende — Persistenz-Check:**

| Check | Pflicht |
|---|---|
| Neue Erkenntnis entstanden? | → Vault-Note anlegen/updaten, Confidence angeben |
| Werkzeug erstmals genutzt? | → [[Werkzeuge-Installiert]] + [[Werkzeug-Register]] updaten |
| Fehler gemacht? | → [[Failure-Memory]] ergänzen |
| Experiment gestartet? | → `02-Experiments/` Note anlegen mit Hypothese |
| Wurde eine Rule gebrochen? | → Rule überdenken oder Ausnahme dokumentieren |
| git push? | → Pflicht. Kein Session-Ende ohne Push. |
| **Autonomie-Score eintragen?** | → `YouTube-Knowledge/00-System/Autonomie-Log.md` updaten: A/B/C/D + Strafen + User-Prompts. Pflicht — auch wenn Score schlecht. |

**Anti-Drift-Regel (gegen schleichendes Vergessen):**
Wenn 3 Videos hintereinander **keine neue Technik** eingesetzt haben → STOPP. Nächste Session beginnt mit Recherche: Was machen Top-Kanäle, was machen wir noch nicht? Ziel: Jedes Video ist messbar besser als das vorherige in mindestens einer Dimension.

---

## Related
[[Memory-Workflow]] · [[Werkzeug-Register]] · [[Current-State]] · [[Schnitt-Protokoll]]
