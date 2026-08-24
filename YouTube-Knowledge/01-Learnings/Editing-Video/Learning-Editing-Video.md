---
type: learning
status: active
confidence: very high
domain: editing-video
created: 2026-08-24
updated: 2026-08-24
evidence_count: 5
tags: [learning, editing, ffmpeg, video]
---

# Learning: Video / ffmpeg — harte technische Lehren

## Current Learning (jede Zeile war ein realer Fehler)
- **`-pix_fmt yuv420p` immer explizit setzen.** `xfade` wählt sonst yuv444p → viele Player verweigern die Wiedergabe (Video 1: kompletter Neu-Export).
- **`zoompan` erzeugt `d` Frames pro *Eingangs*frame.** Bild nur als **ein** Frame hineingeben (`-i bild.jpg`), nie `-loop 1 -t` → sonst wiederholen sich Einstellungen, Zeitachse kaputt.
- **Grundzoom minimal > 1 (`1.05`).** Bei 1.0 ist der Schwenkbereich null.
- **Gegen „statisch": drei Dinge zusammen** — kurze Einstellungen (Schnitt alle 6–11 s), weich beschleunigter Zoom (smoothstep `3t²−2t³`), Handkamera-Drift aus zwei Schwingungen. Dazu Filmkorn + Vignette.
- **Mehrfach-Ausschnitt ist der eigentliche Hebel.** Ein Bild = 3–5 Einstellungen, nicht eine. Halbiert Bildbedarf, verdoppelt Tempo. 1600×2848 → 16:9-Ausschnitt 1600×900 (31 % der Höhe → drei klar verschiedene Einstellungen übereinander). Langvideo in 1080p.

## Bild-Größen-Normalisierung (Pflicht vor `short.py`)
Higgsfield/Seedance/Nano Banana Pro liefern **nicht** verlässlich 1600×2848
(gemessen: 768×1344, 896×1200, 960×1696, 1024×1024, 1152×2048 bunt gemischt).
`short.py` hat `SRC_W=1600, SRC_H=2848` **hardcoded**. Fix am Pipeline-Eingang:
```
convert IMG -resize 1600x2848^ -gravity center -extent 1600x2848 IMG
```
Warum vor `short.py`: der Fix ist bild-, nicht szenenbezogen → macht alle
Downstream-Skripte ausfallsicher.

## Fertige Videos IMMER vor Upload nach Drive/Repo sichern
Die YouTube Data API hat **keinen Download-Befehl** — hochgeladene Videos sind
nicht als Datei zurückholbar (nur Handarbeit im Studio-Browser). Am 17./18.08.
gingen 11 San-José-Shorts verloren, weil sie nur im Container lagen. Regel:
jedes fertige Video/Cover nach `Katastrophenprotokoll-Pipeline` (Drive), benannt
nach Teilnummer (`teil01.mp4`), **bevor** irgendetwas hochgeladen wird.

## Scope
Gesamte Video-Produktion dieses Kanals (Shorts + Langvideo).

## Operational Implication
Teil des [[Schnitt-Protokoll]]. Vor jedem Schnitt Reihenfolge einhalten.

## History
- 17.08.: pix_fmt-, zoompan-, Mehrfach-Ausschnitt-Lehren (Video 1/2).
- 19.08.: Bild-Normalisierung als Pflicht (Video 3, gemischte Größen).

## Related
[[Learning-Editing-Ton]] · [[Learning-Captions]] · [[Learning-Bilder-Prompts]] · [[Failure-Verlorene-Videos-nicht-gesichert]]
