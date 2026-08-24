---
type: learning
status: active
confidence: high
domain: bilder
created: 2026-08-24
updated: 2026-08-24
evidence_count: 4
tags: [learning, bilder, prompts, engines]
---

# Learning: Bild-Prompts (Engine-Wahl siehe Decision)

## Current Learning
Bild-Prompts werden **von Bild zu Bild detailreicher**. Kernregeln:
- Ganze Sätze, kein Stichwortsalat. **Hauptmotiv zuerst** (frühe Wörter wiegen schwerer). 80–90 Wörter.
- **Lichtrichtung und -härte immer nennen.**
- **Nationalität explizit** („Chilean", „Latin American") — sonst europäische Gesichter.
- **Keine Anführungszeichen im Prompt** — Text in Anführungszeichen wird als echter Text ins Bild gemalt. Für leere Schilder „blank".
- Querschnitte: **„single continuous image, no panel borders"** — sonst Comic-Panels.
- Gegen flaue Bilder: „most of the frame in deep black shadow", „clear crisp air, no atmospheric haze", ein Gesicht nah an der Kamera.
- **Bei neuem Sujet erst ein Bild, prüfen, dann den Rest.**

## Figur-Prompts (18.08. an Koepcke gelernt)
- **Alter hart einklemmen:** „17-year-old teenage girl, clearly a teenager, NOT a young child and NOT an adult woman" + Extreme in den Negativ-Prompt.
- **Medium Shot (Hüfte–Kopf)** statt Extreme-Close-up (quetscht Hände/Gesicht → Gurtschnalle landete am Gesicht). Körperzonen ausdrücklich trennen.
- **Kamera-/Licht-Kürzel schlagen Adjektive:** „40mm f/2, focus on the buckle, 3:1 contrast, Kodak Ektachrome 1971 fine grain/halation".
- **Figuren-Konstanz + Look-Suffix** über alle Bilder einer Reihe → wirkt im Schnitt wie ein Film.
- **Emotion nachschärfen:** „quiet dread" rendert oft benommen → „jaw tense, brow furrowed, eyes wide with fear".
- **Negativ-Prompt-Pflichtblock:** `triptych, panels, collage, split screen, borders` + `child, adult woman` + `hands near face, holding object to face, deformed hands, extra fingers`.

## Creative-Director-Modus: Real vs. Generieren (pro Szene, 24.08.)
Bei jeder Szene **entscheiden, nicht beschreiben** — Claude liefert die Szenenliste als
Creative Director in einem Rutsch (pro Szene: Sek-Bereich + eins von zwei):
- **🎬 GENERIEREN** für Schlüsselmomente ohne Stock-Äquivalent (die Überlebende im Wrack,
  der Zettel aus 700 m Tiefe, ein Gesicht im Regen) → voller, tiefer Prompt nach den Regeln oben.
- **📹 ECHT** für Establishing-/Umgebungs-Shots (Dschungel, Höhle, Stollen, Meer) →
  generisches Stock-/Archiv-B-Roll. Billiger, glaubwürdiger, schneller.
- **Harte Grenze:** „Echt" = **generische Umgebung** aus Stock. Das **konkrete Ereignis /
  echte Personen** wird generiert oder nachgestellt — **nie** fremdes Nachrichtenmaterial
  (rechtlich sauber + Marke).

## Counter Evidence / widerlegte Annahme
Siehe [[Failure-Vertikale-Staffelung-Triptychon]]: „vertikale Staffelung
(oben/Mitte/unten) beschreiben" erzeugt echtes 3-Panel-Triptychon. **Stattdessen**
eine Kameraeinstellung, Tiefe über „foreground/midground/background", drei
Ausschnitte per Crop (→ [[Learning-Editing-Video]] Mehrfach-Ausschnitt).

## Scope
Alle Bilder des Kanals. Engine-Wahl (Nano Banana Pro/Seedance/Z-Image): [[Decision-Bild-Engine-Wahl]].

## History
- 17.08.: Grundregeln (Nationalität, Anführungszeichen, Panels).
- 18.08.: Triptychon-Bug widerlegt; Figur-Prompt-Lehren (Alter, Medium-Shot, Kamera-Kürzel).
- 24.08.: Creative-Director-Modus — Real-vs-Generieren-Entscheidung pro Szene (Nutzer-Anweisung).
- 24.08. (Korrektur): **„Faceless" bezieht sich auf den ERSTELLER** (kein Gesicht vor der Kamera), **nicht auf den Content.** Bilder DÜRFEN/SOLLEN echte Gesichter mit Emotion zeigen — stärker als Silhouetten. Silhouette nur bewusst als Stilmittel.
- 24.08.: **Z-Image Turbo via HuggingFace-Space = kostenlos, ABER tägliches ZeroGPU-Kontingent** (~8 Bilder/Tag auf Free, dann „ZeroGPU quota exceeded" bis Reset; HF-PRO = 25 Min/Tag). Default für Szenen-/Umgebungsbilder; higgsfield-Credits für schwierige Figuren aufsparen. **Bewährt (n=8):** rendert Gesichter UND Hände sauber; Prompt-Formel bestätigt — ganze Sätze, Kameraobjektiv (z. B. „35mm f/2.8"), Lichtrichtung, Nationalität explizit, Suffix „single continuous image, no panel borders, no text, no watermark". 9:16 = `864x1536`.

## Related
[[Decision-Bild-Engine-Wahl]] · [[Failure-Vertikale-Staffelung-Triptychon]] · [[Learning-Editing-Video]] · [[Video-03-Koepcke]]
