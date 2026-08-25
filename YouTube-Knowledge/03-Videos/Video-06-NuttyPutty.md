---
type: video
status: in-production
created: 2026-08-25
updated: 2026-08-25
tags: [video, nuttyputty, john-jones, hoehle, shorts, animation]
---

# Video 06 — Nutty Putty (John Jones, 2009)

## Thema
Nutty-Putty-Höhle, Utah, 24.11.2009. Medizinstudent John Jones (26), 1,88 m/90 kg, verkeilt sich
**kopfüber** in einem 18×10-cm-Spalt in unerforschtem Fels. 27 Stunden invertiert (3× länger als
für möglich gehalten), 24 h Rettungseinsatz, Seil reißt → Wendepunkt. Stirbt 25.11. Körper nicht
bergbar → Höhle **mit Beton versiegelt**, Plakette. Quelle: Nutzer-Originalskript (engl. Transkript
`o-TaF2DbaWw`), sinngemäß Deutsch. Starker DE-Suchlücke, trendet 2025/26.

## Produktion (Stand 25.08.)
- **Produktionsbrief fertig:** `nuttyputty/PRODUKTIONSBRIEF.md` — 10 Shorts, je Hook/VO(DE)/Schlüsselbild-Prompt,
  Erzählbogen, **auf die ersten 3 s gebaute Hooks** (Retention-Playbook V1–V5 geladen).
- **Animations-Experiment fertig (Prototyp):** `nuttyputty/animation/querschnitt.html` (+ `capture.py`, `querschnitt_demo.mp4`).
  Höhlen-Querschnitt mit leuchtender Figur, die kriecht und sich kopfüber verkeilt — Referenz-Stil des Nutzers.
  Deterministisch (`window.__seek(ms)`) → Chromium/Playwright Frame-Capture → ffmpeg. **Als bewegter Opener** für die ersten Sekunden (Story-Peaks TEIL 1/4/5/8/9). Siehe [[Experiment-Cheap-Animation-Querschnitt]].
- **Bilder-Regel angewandt:** pro Short **2–6 Szenen; nur Schlüsselszene(n) KI**, Rest aus dem Netz (CC/Commons).
- **Richtung: VOLL auf Animation** (Nutzer 25.08.) — Schlüsselszenen animiert (Querschnitt-Stil), Umgebung als echte B-Roll aus dem Netz; wenig/keine KI-Stills.
- **Workflow-Regel (Effizienz):** Animierte Szenen **erst final rendern, wenn die VO da ist** — das Timing (Szenenlänge/Schnitte) kommt aus der Narration; vorher nur wiederverwendbares System/Assets/B-Roll vorbereiten, sonst doppelte Rechenzeit. Nutzer schickt VO → dann Szenen timen + rendern → terminieren (bündig 3/Tag an Lengede anschließen).
- **Bereit:** Animations-Engine (`animation/querschnitt.html`, `capture.py`) als Vorlage für weitere Szenen; Web-Download für B-Roll steht.
- **Copyright:** kein „Last Descent"-Film, keine Familienfotos, kein echtes Rettungsmaterial; John faceless/Silhouette.

## Related
[[Produktions-Runbook]] · [[Learning-Bilder-Prompts]] · [[Learning-Hooks]] · [[Learning-Retention-und-Laenge]] · [[Ideen-Pipeline]] · [[Current-State]]
