---
type: system
title: Werkzeug-Register
status: active
updated: 2026-09-01
tags: [system, werkzeuge, register, mcp, skills, connectors, produktion]
---

# Werkzeug-Register — das VOLLE Repertoire (bei Produktion immer konsultieren)

> **Regel:** Bei jeder Produktion das **gesamte** Repertoire berücksichtigen und **je Bedarf** wählen — nicht nur die zuletzt genutzten. Reihenfolge: **kostenlos zuerst** (HF/Piper/Manim/Commons), Credits nur für Peak-Qualität. Stand 25.08.2026.
>
> **Register ist Katalog, nicht Kür:** Das [[Produktion-Pflichtliste]]-**Capability-Gate §0c** erzwingt, dass jede Reihe hieraus ≥1 **neue kostenlose** Fähigkeit real integriert (offene Punkte: [[Werkzeug-Backlog]]). Und **§0d** erzwingt Selbst-QC (ansehen + hören) vor Upload. Beides ist der Riegel gegen V8 (hatte Werkzeug, nutzte es nicht).

## 0) ZUERST — Wissens-Retrieval (n+1, IMMER vor Produktion)
Vor dem ersten Schnitt autonom das **komplette geprüfte Wissen** ziehen und anwenden — nicht nur Tools, auch die **Psychologie/Tricks**:
- **Retention/Hooks/erste 3 s:** [[Learning-Retention-und-Laenge]] · [[Learning-Hooks]]
- **Psychologisch catchende Schnitte / Dramaturgie / Pattern-Interrupt:** [[Learning-Storytelling-Shorts]] · [[Learning-Editing-Video]]
- **Captions / Titel / SEO:** [[Learning-Captions]] · [[Learning-Titel]] · [[Learning-SEO]]
- **Bilder (referenz-getrieben) / Themen / Viral:** [[Learning-Bilder-Prompts]] · [[Learning-Topics-Themenwahl]] · [[Ideen-Pipeline]]
- **Ton/Musik · Cross-Platform · Fehler:** [[Learning-Editing-Ton]] · [[Learning-Cross-Platform-TikTok]] · [[Failure-Memory]]
- **Leitplanken + Ziel:** [[Guardrails]] · [[Ziel-YPP-Monetarisierung]] · [[Analytics-Loop]]
Jedes Video baut auf allen vorherigen auf; nichts vergessen, jeder Schritt täglich besser.

## A) MCP-Konnektoren (verbunden + aktiv)
| Konnektor | Wofür in der Produktion | Kosten |
|---|---|---|
| **huggingface** | **Z-Image Turbo** (Schlüsselbilder, `gr1_z_image_turbo_generate`), Hub/Recherche | **gratis** (~8/Tag) → ZUERST |
| **higgsfield** | Bild/**Video**-Gen (z_image, image2video), Upscale, Motion, Virality-Predictor, TikTok-Publish | Credits → nur wenn HF nicht reicht |
| **ElevenLabs** | Voiceover für **Peak-Drama** (Emotion/Pausen), Transkription, SFX | Credits → sparsam |
| **Google Drive** | VO/Assets holen (`gdown`/read), Ablage für Nutzer | gratis |
| **Buffer** | **TikTok** planen/posten — ABER: nie automatisch (Regel), Nutzer lädt selbst | gratis |
| **vidiq** | Outlier/Keyword/Titel-Score, Competitor, Trending — Gegencheck vor Schnitt | Credits (schonen) |
| **Canva** | Thumbnails/Cover/Grafik-Vorlagen (Alternative zu eigenem Render) | Konto |
| **ssemble** | Shorts/Meme-Hooks/Musik/Templates-Generator (schneller Draft) | Konto |
| **github** | Repos/PRs/Issues/CI (Code-Ops) | gratis |
| **claude-code-remote** | Sessions/Trigger/Zeitpläne (z. B. Upload-Trigger) | gratis |

## B) Claude-Skills (produktionsrelevant)
- **`/video`** — ganze Produktions-Pipeline (Kern). · **`/merken`** — Persistenz. · **`/neubeginn`** — Stand laden.
- **NEU (01.09.) Video-Engine-Skills → siehe §H:** **`video-shotcraft`** (Remotion-Motion-Design, 152 Shot-Rezepte), **`video-use`** (Schnitt/Grade/Overlay/Sub per Gespräch, gratis-Transkript), **`watch`** (Video ansehen+hören für QC/Konkurrenz).
- **`youtube`** — Audit/SEO/Hooks/Retention/Calendar/Analytics-Skill. · **`dataviz`** — Charts (Analytics/Statistik-Grafik).
- **`canvas-design`** / **`design`** / **`theme-factory`** — Cover/Poster/Design-Artboards. · **`prompt-master`** — Bild/Video-Prompts optimieren.
- **`artifact-design`/`artifact-diagramming`** — wenn dem Nutzer eine HTML-Seite geliefert wird. · **`pdf`/`docx`/`pptx`/`xlsx`** — Dokumente. · **`skill-creator`** — neue Skills. · **`code-review`/`simplify`** — Pipeline-Code.

## C) Lokale Pipeline (Repo-Root) + `tools/`
- **Kern:** `transcribe_all`/`nb_transcribe` → `align` → `pauses` → `bildcheck` → `karaoke` → `musik` → `build_configs`/`nb_build` → `short` → `serie`/`lang` → `videocheck`; Upload: `youtube_upload`/`nb_upload`; Analyse: `analyse.py`.
- **Bild autonom:** `nuttyputty/nb_fetch_broll.py` (Commons-Kategorien) · `tools/nb_openverse.py` (CC-Pool) · `tools/nb_upscale.py` (schärfen/`--cutout` freistellen, rembg).
- **SEO:** `tools/nb_suggest.py` (YT-Keywords) · `tools/nb_trends.py` (Google Trends).
- **Animation:** `tools/manim_scenes.py`/`manim_demo.py` (Manim) · `nuttyputty/animation/` (SVG+Playwright→ffmpeg) · **Remotion** (Node) — **jetzt real über `video-shotcraft`-Template getestet, §H**.
- **VO:** `tools/nb_tts.py` (**Piper de = gratis Default**). · **Ziel:** `tools/nb_views90.py`.

## D) Auswahl-Heuristik je Bedarf
- **Themen/SEO:** `nb_suggest`+`nb_trends` (gratis) → vidiq nur zum Gegencheck.
- **Bild je Beat:** Foto-möglich → **Commons/Openverse** (gratis); Schock-Moment ohne Foto → **HF Z-Image** (gratis, referenz-getrieben) → higgsfield nur wenn nötig; Erklären (Ort/Geometrie/Zeit/Zahlen) → **Manim**.
- **VO:** Default **Piper** (gratis); ElevenLabs nur Peak-Drama.
- **Musik:** `musik.py` (db −16, hörbar).
- **Video-Gen (bewegte Realszene):** higgsfield image2video (Credits) nur wenn Animation/Stock nicht reicht.
- **Cross-Platform:** YouTube autonom (`nb_upload`), **TikTok manuell** (Buffer nur Vorbereitung).
- **Thumbnail/Cover:** eigener Render/`canvas-design`/Canva.
- **Analyse/Ziel:** `analyse.py` + `nb_views90.py` → [[Ziel-YPP-Monetarisierung]] loggen.

## E) Claude-Plugins (aktiv)
- **`searchfit-seo`** — gratis AI-SEO-Toolkit: Keyword-Cluster, Content-Strategie, Schema, AI-Visibility. → für Titel/Beschreibung/Themen (ergänzt `nb_suggest`/`nb_trends`/vidiq).
- **`postiz`** — Social-Automation-CLI, 28+ Plattformen (YouTube, TikTok, Instagram, X, Reddit…). Für Cross-Platform-Planung. **TikTok bleibt manuell** (Regel) — postiz nur zur Vorbereitung/andere Plattformen.

## F) Alle Claude-Skills (Katalog, je Bedarf)
- **Produktion:** `/video`, `youtube`, `/merken`, `/neubeginn`, `dataviz`, `prompt-master`.
- **Design/Deliverables:** `canvas-design`, `design`, `theme-factory`, `artifact-design`, `artifact-diagramming`, `artifact-capabilities`, `web-artifacts-builder`, `algorithmic-art`.
- **Dokumente:** `pdf`, `docx`, `pptx`, `xlsx`.
- **Code/System:** `code-review`, `simplify`, `skill-creator`, `mcp-builder`, `update-config`, `session-start-hook`, `fewer-permission-prompts`, `keybindings-help`, `run`, `init`, `security-review`, `loop`, `claude-api`, `learn`, `import-memory`, `morning`.
- (Vollzähligkeit variiert je Konto — bei Bedarf via Skill-Liste prüfen.)

## H) Vendorte Video-Engines (installiert 01.09. — weg von Standbild, hin zu Animation/Schnitt)
> Code + Rezepte + Templates liegen im Repo (auf `main`). **Schwere deps (node_modules/.venv) sind NICHT im Repo** → im frischen Container einmalig `bash tools/nb_install_video_engines.sh <ziel>` (idempotent, gratis-first: keine Cloud/GPU-Pakete). Ziele: `core|video-use|shotcraft|openmontage|watch|all`.

| Engine | Ort | Wofür | Gratis? | Einbindung |
|---|---|---|---|---|
| **video-shotcraft** (Skill) | `.claude/skills/video-shotcraft/` | Remotion-Motion-Graphics: 152 Shot-Rezeptkarten (`references/shots`), 2.5D-Kamerafahrten, Beat-Cut, Sound-Design (36 MB SFX in `assets/audio`), Kinetic-Typografie. **Getestet:** echter 1920×1080-Render aus `template/` mit Bewegung+Ton. | **ja**, lokal | `bash tools/nb_install_video_engines.sh shotcraft` → `cd template && npx remotion render src/index.ts <Comp> out.mp4 --concurrency=1` (**ohne** `--browser-executable`; Remotion bringt eigene headless-shell). Für unsere Shorts Composition auf **1080×1920** setzen. |
| **video-use** (Skill) | `.claude/skills/video-use/` | Schnitt per Gespräch: Füllwörter/Stille raus, Color-Grade (ASC-CDL), Overlay-Animationen (HyperFrames/Remotion/Manim/PIL), Sub-Burn — mit harten Korrektheitsregeln (Sub zuletzt, 30 ms Fades, PTS-Shift). **Genau „retention-catching Schnittstile".** | **ja** (Transkript via **`helpers/transcribe_local.py`** = faster-whisper, kein ElevenLabs-Key) | `bash tools/nb_install_video_engines.sh video-use` → Skill nutzen; Transkribieren immer mit `transcribe_local.py`. |
| **watch** (Skill) | `.claude/skills/watch/` | Video ansehen (Frames) + hören (Captions/Whisper) → **§0d-Selbst-QC + visuelle Konkurrenz-Analysepflicht** poliert. | **ja** (yt-dlp+ffmpeg+Whisper) | `bash tools/nb_install_video_engines.sh watch`. Ergänzt `videoblick.py`/`hoeren.py`. |
| **OpenMontage** (Tool) | `tools/vendor/OpenMontage/` | Agentisches Full-Video-System: Remotion + **HyperFrames (HTML/CSS/GSAP)** + FFmpeg + Piper. Pipeline-Defs/Schemas für Explainer/Doku/Trailer. Reservoir für größere Motion-Bausteine. | Kern **ja** (Piper/Commons/lokal); Cloud-Modelle optional (kostenpflichtig, nur auf Anfrage) | `bash tools/nb_install_video_engines.sh openmontage`. `AGENT_GUIDE.md` lesen. HyperFrames als neue Bewegtbild-Fähigkeit fürs Capability-Gate §0c. |

**Regel-Einbindung:** Diese Engines erfüllen die **Bewegtbild-Pflicht** (Bewegung in Sek. 1, ≥1 bewegter Schlüssel-Shot) und die **§0c-Capability-Gate**-Vorgabe (je Reihe ≥1 neue kostenlose Fähigkeit). Nicht als Standbild-Diashow produzieren, solange eine dieser Engines den Shot bewegen kann. `open-design` (Electron-Desktop-App) wurde bewusst **nicht** vendored (GUI, kein headless-Pipeline-Nutzen, überschneidet `/design`).

## G) Repos
- **`acydacy3/twitchclipz`** (push-Recht) — dieses Projekt. Kein weiteres Repo im Zugriff.

## Related
[[Werkzeuge-Installiert]] · [[Werkzeug-Backlog]] · [[Agent-Architecture]] · [[Learning-Bilder-Prompts]] · [[Learning-Editing-Video]] · [[Current-State]]
