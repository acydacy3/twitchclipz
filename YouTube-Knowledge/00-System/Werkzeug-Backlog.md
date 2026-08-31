---
type: system
title: Werkzeug-Backlog
status: active
date: 2026-08-25
updated: 2026-08-31
tags: [system, werkzeuge, backlog, kostenlos, github, n+1]
---

# Werkzeug-Backlog — kostenlose Fähigkeiten nach ROI fürs 10-Mio-Ziel

> **Lebende Liste für das Capability-Integration-Gate** ([[Produktion-Pflichtliste]] §0c). Jede Reihe zieht hier ≥1 offenen Punkt und integriert ihn. Erledigtes wird abgehakt, nicht gelöscht (Historie). Alles gratis oder GitHub. Reihenfolge: **kostenlos zuerst.**

## ✅ Erledigt (integriert — nicht erneut vorschlagen)
1. ✅ **Manim** (gratis) — 9 Klassen live: CrossSection, Timeline, ProsperiMap, StatCounter, SurvivalDays, SearchRadius, DepthDive, RockTrap, CountdownTimer. → `tools/manim_scenes.py`
2. ✅ **pytrends + YouTube-Suggest** (gratis) — `tools/nb_trends.py`, `tools/nb_suggest.py`. Spart vidIQ-Credits.
3. ✅ **Openverse-API** (gratis) — `tools/nb_openverse.py`, breiterer CC-Pool.
4. ✅ **Real-ESRGAN + rembg** (gratis) — `tools/nb_upscale.py` (`--cutout` freistellen).
5. ✅ **Piper TTS** (gratis) — `tools/nb_tts.py`, deutsche Scratch-VO fürs Timing.
6. ✅ **`/video`-Projektskill** — Pipeline gekapselt.
7. ✅ **Selbst-Wahrnehmung** — `hoeren.py` (faster-whisper) + `videoblick.py` (Frames→Read). Seit 31.08. Pflicht-QC vor Upload ([[Produktion-Pflichtliste]] §0d).

## 🔴 Offen — hoher ROI (nächste Reihen ziehen hier)
1. **Remotion real einsetzen** (Node, installiert, 0 Nutzung) — getemplatete Motion-Graphics-Shorts (WordReveal, Lower-Thirds, Stat-Karten). Größte ungenutzte Fähigkeit. → [[Animation-Library]]
2. **`analyse.py` → rollierende 90-Tage-Shorts-Views** (YouTube-Analytics-Query, gratis) — nötig ab ~Mitte Nov. für sauberes YPP-Messen. → [[Ziel-YPP-Monetarisierung]]
3. **Canva-Free für Banner + Thumbnails** (Konto vorhanden) — Kanal-Banner + Cover statt nackter Render. Banner war Audit-Schwachstelle. → [[Learning-Thumbnails-Cover]]
4. **Wan2.1-I2V über HF** (gratis) — Standbild → kurze Bewegtszene für Schock-Momente (statt statischem Ken-Burns). Im Audit für V9 Loveparade markiert. → [[Learning-Bilder-Prompts]]

## 🟡 Offen — mittlerer ROI
5. **searchfit-seo Plugin** (gratis) — Keyword-Cluster + AI-Visibility, ergänzt `nb_suggest`/`nb_trends` bei Titel/Beschreibung.
6. **vidiq Thumbnail-/Titel-Score** (Credits, gezielt) — nur Gegencheck der besten 1–2 Kandidaten vor Publish, nicht flächig.
7. **ElevenLabs Peak-Drama-VO** (Free-Tier) — einzelne Hook-Zeilen mit Emotion/Pausen, wo Piper flach klingt. Sparsam, nur der Hook.

## Konnektoren
- Keine kritische Lücke (Drive, Buffer/TikTok, ElevenLabs, Higgsfield, HuggingFace, vidiq, Canva, ssemble, github, claude-remote vorhanden).
- **Obsidian bewusst NICHT** → [[Decision-Obsidian-nicht-noetig]].

## Regel
Ein Punkt gilt erst als ✅, wenn er in einer echten Produktion eingesetzt UND das Ergebnis per §0d-QC bestätigt wurde. Vorschlagen ohne Integrieren zählt nicht.

## Related
[[Produktion-Pflichtliste]] · [[Werkzeug-Register]] · [[Ziel-YPP-Monetarisierung]] · [[Current-State]] · [[Agent-Architecture]]
