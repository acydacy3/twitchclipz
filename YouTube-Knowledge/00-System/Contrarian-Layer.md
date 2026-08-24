---
type: system
title: Contrarian-Layer
updated: 2026-08-24
tags: [system, contrarian, red-team]
---

# Contrarian / Red-Team Layer

Aufgabe: **nicht optimieren, sondern beweisen, dass die aktuelle Strategie falsch
oder unvollständig ist.** Native Umsetzung ist die **Zwei-Agenten-Methode**
([[Agent-Architecture]]) — ein dedizierter Agent hierfür ist erlaubt, wenn der
[[Guardrails]]-#8-Test ihn rechtfertigt; bisher reicht die Methode + diese Checkliste.

## Regelmäßig prüfen
- Gegenbeispiele · widersprüchliche Daten · alternative Erklärungen
- Survivorship Bias · Confirmation Bias · kleine Sample Sizes · Confounder
- Konkurrenzstrategien · Marktveränderungen · Veränderungen auf YouTube/TikTok · veraltete Learnings

## Vorgehen an einem Belief
```
Current belief: "Hook X funktioniert besser."
→ Welche Videos widersprechen?
→ Wie groß ist die Stichprobe?
→ Themen-Effekt? Audience-Effekt? Length-Effekt?
→ Funktioniert X nur in Kombination mit Y?
```

## Wichtig
- **Nicht aus Prinzip widersprechen.** Ist die Evidenz stark, das ausdrücklich anerkennen.
- Ziel: Überzeugungen durch **Evidenz** behalten, nicht durch Selbstbestätigung.

## Aktuelle Contrarian-Ziele
- „Hook schlägt Länge" — Sample klein, Hook/Länge nicht getrennt → [[Hypothese-Hook-schlaegt-Laenge]].
- „Faktor 7,9 (Kürze gewinnt)" — Confounder Hook-Qualität → [[Learning-Retention-und-Laenge]].
- TikTok-Längen-Sample auf Gewinner gefiltert → [[Learning-Cross-Platform-TikTok]].
- Der OCR-Fall zeigt, warum: [[Failure-OCR-Behauptung-TikTok]].

## Related
[[Evidence-Confidence]] · [[Audit-System]] · [[Failure-Memory]]
