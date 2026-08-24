---
type: learning
status: active
confidence: high
domain: editing-ton
created: 2026-08-24
updated: 2026-08-24
evidence_count: 2
tags: [learning, ton, audio, ffmpeg, musik]
---

# Learning: Ton

## Current Learning
- **Ziel −14 LUFS, Spitze unter −1,5 dBTP.**
- `loudnorm` allein reicht nicht (bei dichter Stimme, LRA ~4, bremst die Spitzengrenze das Gain). Kette, die trifft: **zweistufiges `loudnorm` → `volume=1.6dB` → `alimiter=limit=0.84:level=false`**.
- **`level=false` beim `alimiter` ist Pflicht** — sonst zieht er auf Vollaussteuerung (gemessen +0,1 dBFS).

## Musik
- **Selbst erzeugen, nicht aus der YouTube-Bibliothek.** Bei Shorts teilt YouTube die Einnahmen je Musikstück (1 Track = 50 %, 2 = 33 %) + Content-ID-Sperren. `musik.py` erzeugt ein Moll-Bett (Drone, Pad, Herzschlag, Schimmer, Rauschen).
- **Sidechain-Ducking** unter die Stimme (nicht pauschal leise), in Sprechpausen kommt sie hoch.

## Scope
Alle Videos des Kanals.

## Counter Evidence
Keine. −14-LUFS-Ziel ohne explizites „Warum" dokumentiert (Broadcast-Standard, unkritisch).

## Operational Implication
Vor Export via `videocheck.py` prüfen.

## History
- 17.08. (Video 1 lag bei −15,7 LUFS → Kette entwickelt).

## Related
[[Learning-Editing-Video]] · [[Learning-Captions]]
