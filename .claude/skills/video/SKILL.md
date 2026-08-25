---
name: video
description: Produziert ein komplettes Katastrophenprotokoll-Video (10 Shorts) aus einem Nutzer-Skript + Voiceover — Recherche, Bilder, Animation, Render, Terminierung. Nutzt die nb_-Pipeline und die Zusatz-Werkzeuge. Auslösen mit /video oder wenn der Nutzer ein neues Video produzieren will.
---

# /video — Video-Produktions-Pipeline (Katastrophenprotokoll)

**IMMER zuerst (n+1):** komplettes Learning-Paket ziehen — `YouTube-Knowledge/00-System/Current-State.md` + alle `01-Learnings/*` (Hooks, Retention, Captions, Titel, SEO, Bilder, Editing) + `Ziel-YPP-Monetarisierung.md`. Autonom, nicht ankündigen.

## Ablauf (BASE = ein neuer Ordner, z. B. `nuttyputty/`)
1. **Skript (Nutzer):** Original-Transkript → sinngemäß Deutsch, 10 Shorts segmentieren (Hook auf erste 3 s, keine Titelansage). Produktionsbrief schreiben.
2. **Recherche/SEO (gratis):** `python3 tools/nb_suggest.py "<thema>"` + `python3 tools/nb_trends.py "<kw1>" "<kw2>"` → Titel/Tags/Themen-Gap.
3. **VO:** Nutzer liefert `voiceover/short_01..10.mp3`. Zum Timen vorab Scratch-VO: `python3 tools/nb_tts.py "text" out.mp3` (Piper, deutsch).
4. **Transkript:** `python3 <BASE>/nb_transcribe.py` → `words_XX.json` (Karaoke).
5. **Bilder autonom + PRÄZISE:**
   - Stock/Echt: `python3 <BASE>/nb_fetch_broll.py` (Commons-Kategorien) + `python3 tools/nb_openverse.py "<q>" <dir>` (breiterer CC-Pool).
   - **Schlüsselmomente IMMER generieren** (HF Z-Image gratis, Tagesquota voll nutzen): vorher echte Referenzen ziehen + ansehen (Standort-Look!), dann z_image-Formel. Optional schärfen/freistellen: `python3 tools/nb_upscale.py in.jpg out.jpg --cutout cut.png`.
   - **QC-Pflicht:** Kontaktabzug (`montage`) EINMAL ansehen, Ausreißer ersetzen. Dem Nutzer die Übersicht (S01-01…) zur Validierung zeigen.
6. **Animation (wo passend):** `nuttyputty/animation/` (SVG→Playwright→ffmpeg) oder Manim: `manim -qh -r 1080,1920 tools/manim_scenes.py CrossSection`. Als `{"clip":...}`-Shot in `nb_build.py`.
7. **Render:** aus **Repo-Root**: `python3 <BASE>/nb_build.py` → 10 Shorts. **Musik db=-16 hörbar** (mit `ffmpeg volumedetect` prüfen).
8. **Terminieren bündig 3/Tag** ab letztem belegten Slot (analyse.py prüfen): `metadata.json` + `python3 <BASE>/nb_upload.py` (idempotent). YouTube-Tageslimit ~9–10 → Rest Folgetag.
9. **Persistenz:** Learnings sofort in Vault + `git commit/push` (Branch + main). Video-Note anlegen.
10. **Ziel loggen:** `python3 tools/nb_views90.py` → Zeile in `Ziel-YPP-Monetarisierung.md`.

## Reproduzierbarkeit
VO + Bilder + metadata + Skripte committen (Container ist ephemer). Reproduktion: `nb_build.py` → `nb_upload.py`.

## Nie
Titelansage; Musik db zu tief; fremdes News-/Filmmaterial; TikTok automatisch posten; KI-Porträt realer Toter (faceless).
