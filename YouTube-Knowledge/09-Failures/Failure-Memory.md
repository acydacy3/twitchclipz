---
type: system
title: Failure-Memory
updated: 2026-08-24
tags: [system, failures, moc]
---

# Failure Memory — damit Fehler nur einmal bezahlt werden

Dauerhaftes Gedächtnis für gescheiterte Experimente, Fehlannahmen und
wiederkehrende Fehler — **quer durch den gesamten Lernkreislauf** ([[Agent-Architecture]]).
Zweck: verhindern, dass zukünftige Sessions bereits Widerlegtes erneut probieren.

## Status-Vokabular (nicht „funktioniert nie")
- `rejected` — bewusst verworfen
- `inconclusive` — Ergebnis nicht aussagekräftig
- `failed under conditions X` — scheiterte nur unter bestimmten Bedingungen
- `disproven` — widerlegt
- `superseded` — durch Besseres ersetzt

Jede Failure-Note dokumentiert: **Was getestet · Ergebnis · Warum gescheitert ·
Bedingungen · Learning · Wann es doch noch gültig sein könnte · „Do not repeat unless…"**.

## Failures (inhaltlich)
- [[Failure-Vertikale-Staffelung-Triptychon]] — Bild-Prompt (`disproven`)
- [[Failure-Verlorene-Videos-nicht-gesichert]] — Prozess (`failed under conditions`)
- [[Failure-OCR-Behauptung-TikTok]] — unbelegte Behauptung (`disproven`/`unknown`)
- [[Failure-Titelansage-und-Tempo]] — Dramaturgie/Takt (`disproven`)

## Failure Memory auf Agentenebene
Wenn ein Agent wiederholt denselben Fehler produziert:
```
Agent → Recurring Failure → Root Cause → Experiment → Fix → Validation → Agent Learning
```
Beispiel-Schema (noch kein realer Fall dokumentiert): Hook-Agent generiert
generische Hooks → Root Cause: Prompt priorisiert Neugier über Spezifität →
Constraint hinzufügen → Korrekturrate messen. **Nur mit echten Zahlen füllen,
nie erfinden** ([[Knowledge-Architecture]] §6).

## Related
[[Decision-Verworfene-Werkzeuge]] · [[Contrarian-Layer]] · [[Audit-System]]
