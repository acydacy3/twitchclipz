---
type: library
title: Animation-Library
updated: 2026-08-26
tags: [animation, manim, remotion, library, training]
---

# Animation-Library — Katastrophenprotokoll

> **Strategische Richtung:** Weg von Standbild+VO (Pan/Zoom-Einstellungen) hin zu echter Animation.
> Jede neue Videoreihe committet ≥1 neue Manim-Klasse. Mehrere Animations-Clips pro Reihe anstreben.
> Longterm-Ziel: Animations-Clips als Haupt-Bildsprache, nicht als Ausnahme.

---

## Manim-Bibliothek (`tools/manim_scenes.py`)

| Klasse | Beschreibung | Eingeführt | Genutzt in |
|---|---|---|---|
| `CrossSection` | Felsspalte + Figur gleitet hinab | V6 (Nutty Putty) | V6 S01 Opener |
| `Timeline` | Generische Stunden-Zeitleiste | V6 | noch nicht produktiv |
| `ProsperiMap` | Routenkarte Marokko→Algerien | V7 (Prosperi) | V7 S09 Opener |
| `StatCounter` | Große animierte Zahl zählt hoch | V8+ | — |
| `SurvivalDays` | Tag-für-Tag-Strip mit Events | V8+ | — |
| `SearchRadius` | Expanding Suchkreis auf Karte | V8+ | — |
| `DepthDive` | Kamera taucht in Tiefe | V8+ | — |

### Render-Befehl
```bash
manim -qh -r 1080,1920 tools/manim_scenes.py <ClassName>
# Output: media/videos/manim_scenes/<ClassName>/1080p60/<ClassName>.mp4
```

### Einbinden in short.py
```python
{"clip": "pfad/zum/animation.mp4", "clip_start": 0.0, "start": 0, "end": 5.0}
```

---

## Remotion (`tools/remotion/`)

**Status:** Noch nicht eingerichtet. Schrittweise aufbauen.

**Wann Remotion statt Manim:**
- Komplexe Text-Animationen (Wort für Wort einblenden mit Timing)
- Intro/Outro-Elemente mit Branding
- Composite: Animation + Bild gleichzeitig
- Reaktive Elemente (Balken die wachsen, Counter mit Echtzeit-Timing)

**Nächster Schritt Remotion:**
```bash
# Setup (einmalig):
npx create-video@latest tools/remotion
cd tools/remotion && npm install
# Render: npx remotion render src/index.tsx MyComp out.mp4
```

---

## Was als nächstes bauen (Backlog)

| Idee | Anwendung | Komplexität |
|---|---|---|
| `WaterRising` | Flut/Tsunami-Szenen, Wasser steigt | Manim, mittel |
| `PeopleCounter` | Figuren-Piktogramme die aufleuchten | Manim, einfach |
| `TemperatureGauge` | Thermometer steigt im Wüstensand | Manim, einfach |
| `MineshaftCross` | Grubenquerschnitt mit Etagen | Manim, mittel |
| `WordReveal` | Schlagwort baut sich Buchstabe für Buchstabe auf | Remotion, einfach |
| `SplitScreen` | Vorher/Nachher nebeneinander | Remotion, mittel |
| `CountdownTimer` | Verbleibende Zeit zählt runter | Manim, einfach |

---

## Anti-Stall-Regel
**Jede neue Videoreihe:** mindestens 1 neue Klasse committen.
**Mindestens 2 Animations-Clips pro 10-Short-Reihe** (nicht nur 1 Opener).
Wenn keine neue Klasse entsteht → ins Backlog schauen und etwas umsetzen.

## Related
[[Produktion-Pflichtliste]] · [[Experiment-Cheap-Animation-Querschnitt]] · [[Werkzeuge-Installiert]]
