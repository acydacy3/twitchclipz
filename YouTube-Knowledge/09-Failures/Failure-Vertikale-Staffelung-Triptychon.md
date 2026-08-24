---
type: failure
status: disproven
confidence: high
created: 2026-08-24
updated: 2026-08-24
tags: [failure, bilder, prompts]
---

# Failure: „Vertikale Staffelung (oben/Mitte/unten) beschreiben"

- **Hypothese (v1):** Drei verschiedene Motive in „bottom/middle/top third" beschreiben → ein Bild gibt drei Einstellungen her.
- **Was getestet:** Bild A (Koepcke-Pilot), Seedream 5.0.
- **Ergebnis:** echtes **Drei-Panel-Triptychon** mit harten schwarzen Trennfugen. „single continuous image, no panel borders" überstimmt das **nicht**.
- **Warum gescheitert:** das Modell liest „three thirds" als drei Panels.
- **Learning / Fix:** **eine** Kameraeinstellung, Tiefe im *selben* Raum über „foreground/midground/background"; drei Ausschnitte per **Crop** ([[Learning-Editing-Video]] Mehrfach-Ausschnitt). Negativ-Prompt: `triptych, panels, collage, split screen, borders`.
- **Do not repeat unless:** eine Engine getestet ist, die räumliche Zonen nachweislich als eine Szene rendert.

## Related
[[Learning-Bilder-Prompts]] · [[Learning-Editing-Video]]
