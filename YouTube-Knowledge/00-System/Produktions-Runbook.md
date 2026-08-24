---
type: process
status: active
confidence: high
created: 2026-08-24
updated: 2026-08-24
tags: [process, produktion, runbook, pipeline]
---

# Produktions-Runbook — ein Video von A bis Z (erprobt an V4 Okene)

> Damit die nächste Folge NICHT alle Fallen neu entdeckt. Reihenfolge + die konkreten Stolpersteine.

## 0. Assets vom Drive holen (der teure Teil)
- MCP-Download zieht base64 in den Chat → **viel zu teuer**. Stattdessen **`gdown --folder <url>`** (lädt direkt auf Platte).
- gdown scheitert bei **privaten** Dateien → Nutzer muss den Ordner **einmal auf „Jeder mit Link (Betrachter)"** stellen. `share_file` (MCP) kann das NICHT (nur E-Mail-Freigabe). Danach wieder privat.

## 1. Struktur (BASE = /home/user/twitchclipz/<video>/)
- `voiceover/short_01.mp3 … short_10.mp3` — **nullgepolstert!** (`build_configs`/`transcribe_all` leiten Index aus `short_NN` ab; sort-sicher).
- `bilder/short_NN/01.jpg, 02.jpg, …` — **jedes Bild exakt 1600×2848** (short.py rechnet Crops fix gegen 1600×2848; kleinere Bilder → kaputt). Umwandeln: `convert IN -resize 1600x2848^ -gravity center -extent 1600x2848 -q 92 OUT`. webp→jpg nötig.
- **Jeder Short = KI-Schlüsselbild (01) + echte Deko-Stills (02,03)** — nie nur 1 Bild (Nutzer-Regel). 1 Bild ⇒ nur 3 Crops, Sparvariante.

## 2. Skripte auf das Video zeigen
`transcribe_all.py`, `build_configs.py`, `upload_all.py`: `BASE` auf `<video>`; in `build_configs` die **HOOKS** (Banner-Text der Peak-Shorts) + Ausgabename anpassen; in `upload_all` die **TAGS** + `metadata.json`. **Besser (offen): BASE via ENV/argv parametrisieren**, statt jedes Mal sed.

## 3. Ablauf
`transcribe_all.py` (Whisper small de, lädt Modell 1×) → `build_configs.py` → **`short.py` je Config**. `short.py` macht Ton (−14 LUFS, loudnorm→volume→alimiter), Musik (`musik.py`, Ducking), Karaoke (`karaoke.py`), Ken-Burns, TEIL-Leiste, Hook-Banner, Untertitel.

## 4. Rendern — WICHTIG
- **Hintergrund-`nohup`-Loops sterben hier** (nach ~1 Short). **Vordergrund-Loop** nehmen; die Umgebung schiebt ihn nach 120 s in den Hintergrund und er läuft stabil weiter — aber **10-Min-Cap** pro Aufruf ⇒ ~6–7 Shorts/Aufruf, Rest im zweiten Aufruf.
- Nach jedem Batch **verifizieren** (`ffprobe` Dauer je mp4); „completed exit 0"-Notifs kommen manchmal voreilig.

## 5. Upload (nur YouTube)
- `upload_all.py` lädt privat + `publishAt` (geplant), liest `metadata.json`.
- **YouTube-Tages-Upload-Limit ~9–10 Videos/Tag** (`uploadLimitExceeded`). Bei V4 kam Short 10 nicht mehr durch → **Rest am Folgetag** (Kontingent-Reset ~00:00 PT ≈ 07:00 UTC). **Nie `upload_all.py` erneut ganz laufen lassen** (dupliziert 01-09) — nur die fehlenden einzeln.

## 6. Bilder generieren
- **Z-Image Turbo (HF)** gratis, aber **~8 Bilder/Tag** (ZeroGPU-Kontingent). Für den Rest higgsfield (Credits) oder Folgetag.

## Related
[[Analytics-Loop]] · [[Learning-Editing-Video]] · [[Learning-Bilder-Prompts]] · [[Video-04-Okene]] · [[Current-State]]
