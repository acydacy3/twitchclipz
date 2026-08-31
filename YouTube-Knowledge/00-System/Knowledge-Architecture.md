---
type: system
title: Knowledge-Architecture
updated: 2026-08-24
tags: [system, epistemik, confidence]
---

# Knowledge-Architecture — das epistemische Modell

Dieses Dokument definiert, **wie** Wissen in diesem Vault behandelt wird. Es ist
die Grundlage für jede Learning-, Experiment- und Decision-Note. Verwandt:
[[Guardrails]], [[Memory-Workflow]], [[Evidence-Confidence]].

## 1. Die sieben Wissensebenen
Keine Ebene darf automatisch mit einer anderen gleichgesetzt werden.

```
Observation → Interpretation → Hypothesis → Experiment → Result → Learning → Rule
```

- **Observation** — was ist tatsächlich passiert? (z. B. „Short 26s → 1.286 Aufrufe")
- **Interpretation** — was könnte das bedeuten?
- **Hypothesis** — was wollen wir testen? (nach `07-Hypotheses/`)
- **Experiment** — was wurde konkret verändert? (nach `02-Experiments/`)
- **Result** — was ist tatsächlich herausgekommen?
- **Learning** — was leiten wir mit angemessener Sicherheit ab? (nach `01-Learnings/`)
- **Rule** — wann ist daraus eine operative Regel gerechtfertigt? (kommt in [[Current-State]] / CLAUDE.md)

**Ein einzelnes erfolgreiches Video ist kein Beweis für eine Regel.**

## 2. Confidence-System
Jedes substanzielle Learning trägt im Frontmatter `confidence:`.

| Stufe | Bedeutung |
|---|---|
| **Low** | Einzelbeobachtung oder schwache Evidenz. |
| **Medium** | Mehrere Beobachtungen ODER ein aussagekräftiges Experiment. |
| **High** | Wiederholt bestätigt, ausreichende Datenbasis. |
| **Very High** | Stark repliziert, über mehrere Situationen bestätigt, bisher nicht sinnvoll widerlegt. |

Confidence hängt an **tatsächlicher** Evidenz: Anzahl Beobachtungen, Sample Size,
Reproduzierbarkeit, Konsistenz, verschiedene Content-Typen, mögliche Confounder,
Gegenbeispiele, Zeitverlauf. **Nie künstlich erhöhen.**

## 3. Umgang mit Widersprüchen (Preserve Contradictions)
Wenn neue Evidenz einem bestehenden Learning widerspricht:
```
Old belief → New evidence → Contradiction → Re-evaluation → Updated belief
```
1. Bestehendes Learning **finden**, nicht neu anlegen.
2. Neue Evidenz im Abschnitt `## Counter Evidence` ergänzen.
3. `## Scope` präzisieren (unter welchen Bedingungen gilt es noch?).
4. `confidence` neu bewerten.
5. ggf. Rule ändern.
6. `## History` fortschreiben (Version 1 → neue Evidenz → Version 2 → Reason for change).

**Nie löschen, nie überschreiben, nie verschleiern.** Der Irrweg ist Teil des
Wissens. (Deckt sich mit der alten `~~durchgestrichen~~`-Regel der Ur-CLAUDE.md.)

## 4. Memory-Promotion — was wohin gehört
```
Raw Observation → Experiment/Evidence → Learning → Validated Learning → Operational Rule → CLAUDE.md
```
- **Vault** = Wissen, Gründe, Evidenz, Entscheidungen, Historie (dieses Verzeichnis).
- **CLAUDE.md** = nur ausreichend belastbares, für die unmittelbare Arbeit nötiges Wissen + Verweis hierher. Klein halten.
- **Git** = was tatsächlich technisch geändert wurde (Commits). Beschreibt **nicht** das Warum — das steht hier.

Nur Wissen mit ausreichender Confidence wird nach CLAUDE.md „promoted".

## 5. Retrieval before Reinvention
Vor jeder wichtigen Entscheidung **zuerst hier suchen**:
- Gibt es dazu ein Learning? Ein abgeschlossenes Experiment? Ein [[Failure-Memory]]-Eintrag?
- Welche [[Decisions-Übersicht|Entscheidung]] wurde früher getroffen — und warum?
- Hat sich die Evidenz seither verändert?

Nicht der ganze Vault muss je Session gelesen werden — **gezielt** retrieven statt
Context-Bloat. Der Ablauf steht in [[Memory-Workflow]].

## 6. Keine Halluzinationen im Memory
Niemals Daten/Ergebnisse/Experimente erfinden, Konkurrenzverhalten ohne Evidenz als
Fakt darstellen, Vermutungen als Learnings speichern oder Confidence künstlich heben.
Kennzeichne den echten Status: `Unknown` / `Hypothesis` / `Observation` / `Learning`.
