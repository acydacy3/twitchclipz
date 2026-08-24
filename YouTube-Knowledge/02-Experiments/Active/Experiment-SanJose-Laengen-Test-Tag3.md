---
type: experiment
status: active
hypothesis: "Innerhalb 19–39 s erklärt Länge nicht die Performance; der Hook tut es."
domain: retention
variables: "Short-Länge (kurz 19–29 s vs. lang 33–39 s)"
control: "gleicher Kanal, gleiches Thema (San José), gleiche Tageszeiten-Slots"
test: "18./19.08. kurze Shorts, 20.08. drei lange Shorts"
start_date: 2026-08-18
end_date:
sample_size: 11
result: ""
confidence: low
decision: ""
created: 2026-08-24
updated: 2026-08-24
tags: [experiment, retention, laenge]
---

# Experiment: San-José-Längen-Test (Tag 3)

## Hypothese
→ [[Hypothese-Hook-schlaegt-Laenge]]. Bricht der dritte Tag (die drei langen
Shorts) ein, trägt die Längenthese; bricht er nicht ein, war es der Hook.

## Design
- **Unabhängige Variable:** Länge (kurz vs. lang), quasi-zufällig durch die Upload-Reihenfolge entstanden.
- **Abhängige Variable:** AVP% + 3-s-Retention (nicht Aufrufe — Verteilungslotterie).
- **Confounder:** verschiedene Hooks je Short → Länge/Hook nicht sauber getrennt (bekannte Schwäche, deshalb Confidence low).

## Result
**Offen** — Daten frühestens Tag 4–5 (Analytics-API hinkt 2–3 Tage). **Nicht mit
Schätzungen füllen.** Bei Auswertung: AVP% je Short aus `analyse.py`.

## Decision
Nach Auswertung: Learning in [[Learning-Retention-und-Laenge]] fortschreiben,
Confidence dort neu bewerten.

## Related
[[Video-02-San-Jose]] · [[Learning-Retention-und-Laenge]] · [[Experiment-Manager]]
