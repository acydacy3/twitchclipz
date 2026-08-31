---
name: video
description: Produziert ein komplettes Katastrophenprotokoll-Video (10 Shorts) aus einem Nutzer-Skript + Voiceover — Recherche, Bilder, Animation, Render, Terminierung. Nutzt die nb_-Pipeline und die Zusatz-Werkzeuge. Auslösen mit /video oder wenn der Nutzer ein neues Video produzieren will.
---

# /video — Video-Produktions-Pipeline (Katastrophenprotokoll)

**SCHRITT 0 — PFLICHT, NICHT ÜBERSPRINGEN:**
`YouTube-Knowledge/00-System/Produktion-Pflichtliste.md` **vollständig lesen und abarbeiten** bevor irgendetwas anderes passiert. Alle 15 Pflicht-Dateien lesen — 13 Learnings + Failure-Memory + Animation-Library (nicht aus dem Gedächtnis — physisch lesen), Werkzeug-Checklist abarbeiten, Konkurrenz-Referenz prüfen. Nicht ankündigen, einfach tun.

## Ablauf (BASE = ein neuer Ordner, z. B. `nuttyputty/`)
1. **Skript (Nutzer):** Original-Transkript → sinngemäß Deutsch, 10 Shorts segmentieren (Hook auf erste 3 s, keine Titelansage). **Jedes Segment als `<BASE>/skript/short_XX.txt` speichern (Titelzeile + Text)** — das ist die Caption-Wahrheitsquelle. Produktionsbrief schreiben.
2. **Recherche/SEO (gratis):** `python3 tools/nb_suggest.py "<thema>"` + `python3 tools/nb_trends.py "<kw1>" "<kw2>"` → Titel/Tags/Themen-Gap.
3. **VO:** Nutzer liefert `voiceover/short_01..10.mp3`. Zum Timen vorab Scratch-VO: `python3 tools/nb_tts.py "text" out.mp3` (Piper, deutsch).
4. **Captions — IMMER aus Skript, NIE aus ASR (F-V8-E):** ASR nur fürs Timing, dann `python3 align.py <BASE>/words_XX.json <BASE>/skript/short_XX.txt <BASE>/words_XX_fixed.json` → Wörter kommen aus dem Skript, Zeitstempel aus dem Audio. `nb_build.py captions()` macht das automatisch, wenn `skript/short_XX.txt` existiert. **Roh-ASR als Caption ist verboten** — sie verstümmelt Namen („Rallsturm" statt „Ralston", „jemes Franco"). Pflicht-Check im §0d-QC.
5. **Bilder autonom + PRÄZISE:**
   - Stock/Echt: `python3 <BASE>/nb_fetch_broll.py` (Commons-Kategorien) + `python3 tools/nb_openverse.py "<q>" <dir>` (breiterer CC-Pool).
   - **Schlüsselmomente IMMER generieren** (HF Z-Image gratis, Tagesquota voll nutzen): vorher echte Referenzen ziehen + ansehen (Standort-Look!), dann z_image-Formel. Optional schärfen/freistellen: `python3 tools/nb_upscale.py in.jpg out.jpg --cutout cut.png`.
   - **QC-Pflicht:** Kontaktabzug (`montage`) EINMAL ansehen, Ausreißer ersetzen. Dem Nutzer die Übersicht (S01-01…) zur Validierung zeigen.
6. **Animation (wo passend):** `nuttyputty/animation/` (SVG→Playwright→ffmpeg) oder Manim: `manim -qh -r 1080,1920 tools/manim_scenes.py CrossSection`. Als `{"clip":...}`-Shot in `nb_build.py`.
7. **Render:** aus **Repo-Root**: `python3 <BASE>/nb_build.py` → 10 Shorts. **Neuer Serien-Build MUSS die `captions()`-Funktion aus `ralston/nb_build.py` übernehmen** (Skript→align→Timing, ASR nur fürs Timing) — sonst kehren die ASR-Caption-Fehler zurück. **Musik db=-16 hörbar** (mit `ffmpeg volumedetect` prüfen).
8. **Terminieren bündig 3/Tag** ab letztem belegten Slot (analyse.py prüfen): `metadata.json` + `python3 <BASE>/nb_upload.py` (idempotent). YouTube-Tageslimit ~9–10 → Rest Folgetag.
9. **Persistenz:** Learnings sofort in Vault + `git commit/push` (Branch + main). Video-Note anlegen.
10. **Ziel loggen:** `python3 tools/nb_views90.py` → Zeile in `Ziel-YPP-Monetarisierung.md`.

## Reproduzierbarkeit
VO + Bilder + metadata + Skripte committen (Container ist ephemer). Reproduktion: `nb_build.py` → `nb_upload.py`.

## Nie
Titelansage; Musik db zu tief; fremdes News-/Filmmaterial; TikTok automatisch posten; KI-Porträt realer Toter (faceless).
