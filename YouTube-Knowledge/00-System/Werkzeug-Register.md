---
type: system
title: Werkzeug-Register
status: active
updated: 2026-08-25
tags: [system, werkzeuge, register, mcp, skills, connectors, produktion]
---

# Werkzeug-Register — das VOLLE Repertoire (bei Produktion immer konsultieren)

> **Regel:** Bei jeder Produktion das **gesamte** Repertoire berücksichtigen und **je Bedarf** wählen — nicht nur die zuletzt genutzten. Reihenfolge: **kostenlos zuerst** (HF/Piper/Manim/Commons), Credits nur für Peak-Qualität. Stand 25.08.2026.

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
- **`youtube`** — Audit/SEO/Hooks/Retention/Calendar/Analytics-Skill. · **`dataviz`** — Charts (Analytics/Statistik-Grafik).
- **`canvas-design`** / **`design`** / **`theme-factory`** — Cover/Poster/Design-Artboards. · **`prompt-master`** — Bild/Video-Prompts optimieren.
- **`artifact-design`/`artifact-diagramming`** — wenn dem Nutzer eine HTML-Seite geliefert wird. · **`pdf`/`docx`/`pptx`/`xlsx`** — Dokumente. · **`skill-creator`** — neue Skills. · **`code-review`/`simplify`** — Pipeline-Code.

## C) Lokale Pipeline (Repo-Root) + `tools/`
- **Kern:** `transcribe_all`/`nb_transcribe` → `align` → `pauses` → `bildcheck` → `karaoke` → `musik` → `build_configs`/`nb_build` → `short` → `serie`/`lang` → `videocheck`; Upload: `youtube_upload`/`nb_upload`; Analyse: `analyse.py`.
- **Bild autonom:** `nuttyputty/nb_fetch_broll.py` (Commons-Kategorien) · `tools/nb_openverse.py` (CC-Pool) · `tools/nb_upscale.py` (schärfen/`--cutout` freistellen, rembg).
- **SEO:** `tools/nb_suggest.py` (YT-Keywords) · `tools/nb_trends.py` (Google Trends).
- **Animation:** `tools/manim_scenes.py`/`manim_demo.py` (Manim) · `nuttyputty/animation/` (SVG+Playwright→ffmpeg) · **Remotion** (Node, installiert).
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

## Related
[[Werkzeuge-Installiert]] · [[Werkzeug-Backlog]] · [[Agent-Architecture]] · [[Learning-Bilder-Prompts]] · [[Learning-Editing-Video]] · [[Current-State]]
