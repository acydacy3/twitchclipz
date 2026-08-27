---
type: system
title: Produktion-Pflichtliste
status: active
updated: 2026-08-26
tags: [system, pflicht, n+1, produktion]
---

# Vor jedem Produktionsschritt — Pflichtliste (n+1)

> **Diese Datei IMMER lesen, bevor ein Video produziert, geschnitten, getextet oder hochgeladen wird.**
> Kein Schritt wird übersprungen. Kein Werkzeug wird ausgelassen, weil der Nutzer es nicht erwähnte.
> Autonome Ausführung ist Pflicht, nicht Option.

---

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

Diese 14 Dateien werden gelesen, bevor das erste Bild, der erste Satz oder das erste Tag entsteht:

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

**Schritt 1 — Top-Videos zum Thema analysieren:**
```
python3 tools/nb_suggest.py "<thema>"   # Top-Keywords + Videos
```
→ Die Top-3-Videos aufrufen, **Thumbnails + erste 10 Sekunden** ansehen:
- Welche Bildsprache? (dunkel/hell, nah/weit, Person/Landschaft)
- Welche Stock-Kategorien offensichtlich genutzt?
- Was macht das Thumbnail sofort klickbar?

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

## 5. Manim/Remotion — Training-Pflicht (jede Reihe)

**So viele Animations-Clips pro Reihe wie sinnvoll und qualitativ gut wird — kein Limit nach oben, kein starres Minimum.** Jede Szene aktiv prüfen: Wäre hier eine Animation besser als ein Standbild?

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
