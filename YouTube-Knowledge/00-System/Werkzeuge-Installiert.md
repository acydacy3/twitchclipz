---
type: system
title: Werkzeuge-Installiert
status: active
date: 2026-08-25
tags: [system, werkzeuge, pipeline, setup]
---

# Zusatz-Werkzeuge — installiert & in der Pipeline verdrahtet (25.08.2026)

## Persistenz-Mechanik (0 Token pro Session)
- **`tools/setup-tools.sh`** installiert alles idempotent (Marker `~/.nb_tools_ready`).
- Eingehängt in **`setup.sh`** (Container-Build) UND in **`.claude/hooks/session-start.sh`** (Hintergrund, `nohup … >/dev/null`, marker-gesichert). → läuft je frischem Container **einmal**, schreibt nur ins Log, **kostet keinen Kontext/Token**.
- Scripts sind im Repo (getrackt); Binaries/Modelle (piper, torch) werden neu geladen (gitignored).

## Was neu ist & wie es genutzt wird
| Werkzeug | Status | Pipeline-Skript | Zweck |
|---|---|---|---|
| **YouTube-Suggest** | ✅ | `tools/nb_suggest.py "<q>"` | Keyword-Ideen für Titel/Tags (gratis) |
| **Google Trends** | ✅ (Laufzeit ggf. gedrosselt) | `tools/nb_trends.py "<kw>"…` | Interesse + verwandte Suchen, Themen-Gap |
| **Openverse** | ✅ | `tools/nb_openverse.py "<q>" <dir>` | breiterer CC-Bildpool (Ergänzung zu Commons) |
| **Piper TTS (de)** | ✅ | `tools/nb_tts.py "text" out.mp3` | deutsche VO — **legitim als finale Stimme** (Default gratis), nicht nur Scratch; ElevenLabs nur für Peak-Drama |
| **rembg** | ✅ | `tools/nb_upscale.py in out --cutout cut.png` | Figuren **freistellen** → in Querschnitt-Animation compositen |
| **Real-ESRGAN** | ⚠️ übersprungen (torch/basicsr-Konflikt) | (Fallback in `nb_upscale.py`) | Upscale → **Fallback Lanczos+Schärfen** greift automatisch |
| **Manim** | ✅ 0.21 | `manim -qh -r 1080,1920 tools/manim_scenes.py CrossSection` | Erklär-Animation (Querschnitt/Zeitleiste/Karte) → `{"clip":...}` in `short.py` |
| **90-Tage-Analytics** | ✅ Skript | `python3 tools/nb_views90.py` | rollierende 90-Tage-Views → YPP-Fortschritt loggen |
| **/video-Skill** | ✅ | `.claude/skills/video/SKILL.md` | ganze Pipeline in einem Befehl |

## Offen
- **Real-ESRGAN** braucht torch+basicsr (basicsr inkompatibel mit neuem torchvision). Bei Bedarf: gepinnte Versionen oder `realesrgan-ncnn`-Binary. Bis dahin Lanczos-Fallback (für 1600×2848 meist ausreichend).
- **Manim** in echten Produktions-Short integrieren (erst als Experiment testen).

## Related
[[Werkzeug-Backlog]] · [[Agent-Architecture]] · [[Ziel-YPP-Monetarisierung]] · [[Current-State]]
