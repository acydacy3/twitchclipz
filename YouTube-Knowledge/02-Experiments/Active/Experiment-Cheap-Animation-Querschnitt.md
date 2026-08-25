---
type: experiment
status: active
created: 2026-08-25
tags: [experiment, animation, retention, hooks, opener]
---

# Experiment: Billig-animierter Querschnitt als Opener

## Hypothese
Ein **bewegter Höhlen-Querschnitt mit leuchtender Figur** (Referenz-Stil des Nutzers: dunkler Fels,
Glow-Silhouetten, die sich durch den Spalt bewegen) schlägt in den **ersten 3 Sekunden** ein statisches
Ken-Burns-Bild als Pattern-Interrupt — genau der Hebel, den V1–V5 als entscheidend belegen
([[Learning-Hooks]], [[Learning-Retention-und-Laenge]]). „Wesentlich catchier als ein Podcast mit Bildern" (Nutzer).

## Umsetzung (funktioniert, 25.08.)
- **Rein Web-Stack, kostenlos, kein KI-Credit:** SVG (Fels via `feTurbulence`+`feDiffuseLighting`, Spalt als Pfad,
  Figur als Glow-Strichfigur mit Helmlichtkegel) + deterministische JS-Zeitachse `window.__seek(ms)`.
- **Render:** Chromium (`/opt/pw-browsers/chromium-1194`) via **Playwright** (`pip install playwright`, Browser schon da) →
  Frame-Capture (`__seek` je Frame + `screenshot`) → **ffmpeg** zu 1080×1920 mp4. Skript: `nuttyputty/animation/capture.py`.
- **Ergebnis:** `querschnitt_demo.mp4` (8 s), Figur kriecht durch den Gang und verkeilt sich kopfüber im Riss. Look = Referenz getroffen.
- **Als Artifact** läuft dieselbe HTML live (requestAnimationFrame-Loop, wenn `__CAPTURE` nicht gesetzt).

## Offen / nächste Iteration
- Zweite Figur (Bruder Josh, orange) wie in der Referenz; Figur größer/detaillierter; Krabbelzyklus deutlicher.
- Als echten Opener in einen Short schneiden und **AVP%/erste-3-s-Kurve** gegen einen Ken-Burns-Opener messen (der eigentliche Beleg).
- Remotion als Alternative testen (Plugin installiert) — SVG+Playwright ist aber schon leichtgewichtig und reicht.

## Messung
Erst belegt, wenn ein Short mit Animations-Opener vs. Bild-Opener verglichen ist (Tag 4–5, AVP%). Bis dahin: **vielversprechender Prototyp**, kein Beweis.

## Related
[[Learning-Hooks]] · [[Learning-Retention-und-Laenge]] · [[Learning-Editing-Video]] · [[Video-06-NuttyPutty]] · [[Experiment-Remotion-Motion-Graphics]]
