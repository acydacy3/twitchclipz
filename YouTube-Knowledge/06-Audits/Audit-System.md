---
type: system
title: Audit-System
updated: 2026-08-24
tags: [system, audit, moc]
---

# Audit-System — regelmäßige Selbstkritik

Zwei Ebenen: (A) **Kanal-Zahlen-Audit** (Retention/Aufrufe je Video) und
(B) **Konstrukt-Audit** (Widersprüche/Drift im Wissen selbst).

## A. Kanal-Zahlen → `audit-videos.csv` (nicht ins Vault/CLAUDE.md)
Pro Video mit Datum: Aufrufe, Aufrufe/Tag, AVP%, Ø-Dauer, Retention-Ratio,
Engagement%, Abos, Länge. Bei jedem Audit **alle Videos mit Tagesdatum anhängen**
→ Bindung jedes Videos über die Tage verfolgbar. Warum als CSV: tägliche Zahlen
wären im Vault Lärm; als CSV über Wochen vergleichbar + zu Kurven renderbar.
Hinweis: Analytics-API hinkt 2–3 Tage → frische Videos AVP=0.

## B. Konstrukt-Audit (Wissen prüfen)
An Meilensteinen (nicht jede Session — schont Limits): das Vault **kalt** lesen
und melden: Widersprüche, Doppelungen, verwaiste Learnings, fehlendes „Warum",
Veraltetes. Bevorzugt per Subagent/Zwei-Agenten-Methode ([[Contrarian-Layer]]).

## Zyklen
### Daily → `06-Audits/Daily/`
Was wurde heute gelernt? Was lief/lief nicht? Welche Annahmen verändert? Was muss
persistiert werden? Neue Widersprüche? Offene Fragen? Wiederholte Fehler?
Vorlage: [[_Daily-Audit-Template]].

### Weekly → `06-Audits/Weekly/`
Welche Learnings bestätigt/widerlegt? Offene Hypothesen? Fehlende/zu beendende
Experimente? Wiederkehrende Agenten-Fehler? Welche Rules updaten? Welche
Strategie neu bewerten? Neue Konkurrenzmuster? Vorlage: [[_Weekly-Audit-Template]].

### Monthly → `06-Audits/Monthly/`
Strategische Erkenntnisse? Welche alten Annahmen jetzt falsch? Welche Agenten
verbessert? Systematische Schwächen? Wiederholt erfolgreiche Methoden? Wo neue
Experimente/Chancen? Was im Wissen veraltet? Vorlage: [[_Monthly-Audit-Template]].

## Related
[[Strategy-Evolution]] · [[Contrarian-Layer]] · [[Failure-Memory]] · [[Memory-Workflow]]
