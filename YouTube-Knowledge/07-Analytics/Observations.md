---
type: analytics
title: Observations
updated: 2026-08-26
tags: [analytics, observations, auto, kausal]
---

# Observations — Automatisch generiert

*Befüllt von `tools/nb_observe.py --vault` nach jeder Session.*
*Muster über mehrere Einträge → Hypothese → Experiment → Learning.*

---

## Wie Observations zu Entscheidungen werden

```
Observation (gemessen) → Muster erkannt → Hypothese formuliert
→ Experiment aufsetzen (02-Experiments/) → Result abwarten
→ Learning ableiten (01-Learnings/) → Rule / Strategy
```

**Confidence-Stufen:**
- `[beobachtet]` — einmalig gesehen, noch kein Muster
- `[Muster]` — mehrfach gesehen, Hypothese sinnvoll
- `[bestätigt]` — Experiment hat es bewiesen (Learning-Status)
- `[widerlegt]` — Counter-Evidence, alte Annahme korrigieren

---

## 2026-08-26

- [2026-08-26] COUNTER-EVIDENCE Längenthese: Lange Videos (≥22 s, n=38) zeigen Ø 847 Views vs. kurze (n=6) Ø 582 Views — Faktor 1.5× zugunsten Langer. Widerspricht bisheriger Annahme. `[beobachtet]` Kausalproblem: lange Videos existieren länger → mehr Zeit zum Wachsen. Erst belegt wenn gleich alte kurze vs. lange verglichen werden.
- [2026-08-26] OUTLIER: 'San José (Luftblasen-Doku)' — 4205 Views (5× Kanal-Schnitt = 811). Hypothese: Titel-Formel "X Tage alleine" + Überlebensaspekt schlägt Katastrophen-Chronik. Für V8 prüfen: Menschlichen Überlebens-Bogen stärker herausarbeiten.
- [2026-08-26] Top-3: San-José-Luftblase (4205) · San-José-Erklärer (2104) · Koepcke (1823). Pattern: Überlebensgeschichten mit konkreter Zeitangabe im Titel dominieren.
- [2026-08-26] Underperformer: Tham-Luang-Serie (V1, 11–31 Views). Erklärung: erste Videos, keine Kanal-Autorität, schwache Tags, kein Thumbnail-System.
- [2026-08-26] SEO: Alle 44 öffentlichen Videos haben Tags (100%). Kein A/B-Vergleich möglich. Korrelation mit Views nicht messbar.
- [2026-08-26] System-Note: Observation-Engine gestartet. Erste Snapshots gesammelt. Kausal-Analyse ab 2. Snapshot möglich.

---

## Kausal-Timeline (was wurde wann geändert → was passierte)

| Datum | Änderung | Beobachteter Effekt | Confidence |
|---|---|---|---|
| 2026-08-15 | Kanalstart (V1 Tham Luang) | 11–31 Views (V1-Serie schwach) | [beobachtet] |
| 2026-08-18 | V2 San José: Überlebens-Titel-Formel | 2104–4205 Views (Sprung) | [Muster] |
| 2026-08-25 | Manim CrossSection (V6 Nutty Putty) eingeführt | AVP% noch nicht gemessen | [beobachtet] |
| 2026-08-26 | ProsperiMap Manim (V7) produziert | Noch nicht veröffentlicht | [beobachtet] |

*Diese Tabelle wächst mit jeder Session. Nach 5+ Einträgen: Muster suchen → Hypothese.*

---

## Related
[[Autonomie-Log]] · [[Experiment-Manager]] · [[Hypotheses-Übersicht]] · [[Learning-Retention-und-Laenge]]
