---
type: system
title: Experiment-Manager
updated: 2026-08-24
tags: [system, experiments, workflow]
---

# Experiment Manager

Umgesetzt als Workflow + Vorlage + Ordner `02-Experiments/` — **kein eigener Agent
nötig, Stand jetzt** (ein Agent wäre erlaubt, sobald der [[Guardrails]]-#8-Test ihn
rechtfertigt). Zweck: aktiv bestimmen **„Was sollten wir als Nächstes testen,
um unser Wissen zu verbessern?"** — nicht nur feststellen, ob ein Video lief.

## Ziel
**Nicht möglichst viele Experimente, sondern möglichst viel Wissen pro Experiment.**
Der Manager erkennt aktiv, wenn eine Hypothese **bereits ausreichend getestet** ist
(→ dann kein neues Experiment, sondern Learning/Rule).

## Ablauf
```
Hypothese (07-Hypotheses/) → Experiment planen (Vorlage) → durchführen
→ Result → Interpretation → Learning (01-Learnings/) → Confidence → Operational Decision
```

## Regeln
- **Genau eine unabhängige Variable** pro Experiment, wo möglich. Zu viele gleichzeitig → keine Schlussfolgerung.
- Klar trennen: Hypothese · unabhängige Variable · abhängige Variable · Kontrolle · Ergebnis · Interpretation · Entscheidung.
- Vor dem Planen: [[Failure-Memory]] + bestehende Experimente prüfen (nicht Widerlegtes neu testen).
- Status im Frontmatter: `planned | active | completed | rejected`.

## Vorlage
Nutze [[_Experiment-Template]] für jedes neue Experiment.

## Aktuelle Experimente
- [[Experiment-SanJose-Laengen-Test-Tag3]] (active) — Länge vs. Hook
- [[Experiment-Hook-Banner-abweichender-Text]] (planned) — Banner ≠ Stimme
- [[Experiment-TikTok-Lange-Schnitte]] (planned) — 90–150 s statt 25 s

## Related
[[Knowledge-Architecture]] · [[Evidence-Confidence]] · [[Hypotheses-Übersicht]]
