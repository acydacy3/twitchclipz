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

## Iterationen (Nutzer-Feedback)
- **v1 → „schwimmend":** Figur zu klein, gleitet linear.
- **v2:** zwei Figuren (Bruder orange) + senkrechte Endpose. Nutzer: „sieht aus wie 2 Leute, die durch die Luft schwimmen."
- **v3 (Fix, funktioniert):** **(a) enger Tunnel** — Körper als gefüllte Glow-Kapsel, die die Röhre *ausfüllt* (kein Schweben im Leeren mehr); **(b) Krabbel-Gang statt Gleiten** — Vortrieb in RUCKEN (Griff → vordere Hand plantet → Körper zieht sich heran → kurze Rast), Velocity-Profil je Zug. Das killt den Schwimm-Eindruck. Endpose senkrecht kopfüber.
- **Probe-Short gebaut** (`nuttyputty/build_probe.py` → `probe_short_teil1.mp4`): Animation-Opener + **echte CC-B-Roll aus Wikimedia Commons** (Ken-Burns) + Captions im Kanal-Stil, 9:16, 16,9 s. Zeigt den kompletten Zusammenbau (Animation + selbst gezogene Netz-Bilder). **ffmpeg-Falle notiert:** `zoompan d=N` mit `-loop 1 -t` multipliziert Frames → Standbild als `-loop 1 -i img … -frames:v N` (kein `-t`).

## Video-Recherche-Fähigkeit (25.08. getestet)
- **CC-Bilder/Videos aus Wikimedia Commons: JA** (curl, mit Attribution) — B-Roll-Quelle steht.
- **YouTube-Videos ansehen/ziehen: NEIN von dieser Server-IP.** yt-dlp + **bgutil PO-Token-Provider** (GitHub, Server läuft auf :4416) installiert — trotzdem blockt YouTube am *Player-API/Bot-Gate* („confirm you're not a bot"), das braucht **Login-Cookies** (PO-Token allein reicht nicht, greift erst nach dem Gate). → Um von Gewinner-Videos zu lernen: **vidiq-MCP** (`vidiq_video_watch`/`vidiq_video_transcript`/`vidiq_outliers`, kostet Credits) ODER Nutzer exportiert `cookies.txt`. Nicht erneut Zeit in yt-dlp-Client-Varianten stecken.

## Offen / nächste Iteration
- Zweite Figur (Bruder Josh, orange) wie in der Referenz; Figur größer/detaillierter; Krabbelzyklus deutlicher.
- Als echten Opener in einen Short schneiden und **AVP%/erste-3-s-Kurve** gegen einen Ken-Burns-Opener messen (der eigentliche Beleg).
- Remotion als Alternative testen (Plugin installiert) — SVG+Playwright ist aber schon leichtgewichtig und reicht.

## Messung
Erst belegt, wenn ein Short mit Animations-Opener vs. Bild-Opener verglichen ist (Tag 4–5, AVP%). Bis dahin: **vielversprechender Prototyp**, kein Beweis.

## Related
[[Learning-Hooks]] · [[Learning-Retention-und-Laenge]] · [[Learning-Editing-Video]] · [[Video-06-NuttyPutty]] · [[Experiment-Remotion-Motion-Graphics]]
