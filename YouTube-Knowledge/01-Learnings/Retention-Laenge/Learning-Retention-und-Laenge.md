---
type: learning
status: active
confidence: high
domain: retention
created: 2026-08-24
updated: 2026-08-24
evidence_count: 4
tags: [learning, retention, laenge, hooks, shorts]
---

# Learning: Der Hook entscheidet, nicht die Sekundenzahl

## Current Learning
Innerhalb der erprobten Zone **19–39 s** erklärt die Länge **nicht** die Streuung
der Aufrufe/Bindung — **der Hook tut es.** Nicht „unter 30 s" ist die Regel,
sondern **„keine toten Sekunden": jede Sekunde muss ihren Platz verdienen.**

## Observation / Evidence
- **Vosk n=12 (Tham Luang):** bis 22 s → Ø 354 Aufrufe · über 22 s → Ø 45 („Faktor 7,9"). ABER mit Hook-Qualität vermischt (Confounder).
- **vidIQ-Audit:** bester Short war **34 s** (Hook „Katastrophe abgewehrt, Opfer gerettet!") → 666, schlug alle kürzeren; 18 s → 885; 19 s → 469.
- **Kanal-Bestwert:** Fakten-Kalt-Einstieg **„33 Mann fahren ein. 700 Meter tief." (26 s → 1.286)**.
- **Bindung (AVP%):** 19 s lieferte 113 % UND 79 %; 22 s nur 56,8 % → Länge trennt die Fälle nicht, der Anfang schon.

## Interpretation
„Faktor 7,9" ist real, aber teils, **weil** kurze Videos schneller zum Punkt
kommen — nicht weil Kürze an sich gewinnt.

## Scope
- Gilt für **YouTube-Shorts** dieses Kanals, Zone 19–39 s.
- **Ultra-kurz (4–19 s)** kann explodieren, WENN der Hook ein vollständiger
  Neugier-Bogen ist (Koepcke 4 s → 872k, fremder Kanal) — riskant, kein Erzählbogen.
- **Langform ist für diesen Kanal Gift:** Humantary 26 min → 3.222; eigenes Langvideo → 5 Aufrufe. Langvideo ≤ 5 min als Zweitschiene.

## Counter Evidence / Contradiction
- **NEU 24.08. (n=35, stärkster Beleg bisher):** Über alle 3 Serien gemessen (`analyse.py`): bis 22 s → Ø 523 Aufrufe · über 22 s → Ø **591** · **Faktor 0,9**. Die alte „Faktor 7,9 / Kürze gewinnt"-These (Vosk n=12) ist damit **klar überholt** — Länge ist innerhalb 19–39 s **kein** eigenständiger Vorteil. Die San-José-Längenprobe (33–39 s am 20.08.) brach **nicht** ein (33s→917, 34s→915, 39s→531) → bestätigt: **Hook > Länge**. Siehe [[Experiment-SanJose-Laengen-Test-Tag3]] (abgeschlossen).
- **TikTok kehrt es um** (siehe [[Learning-Cross-Platform-TikTok]]): Gewinner-Median ~100 s, kein einziger unter 60 s. **YouTube-Längenregel NICHT nach TikTok mitnehmen.**
- Vorsicht Prozent-Retention: sie hängt mechanisch an der Länge (31 % von 18 s = 5,6 s). Prozent-Anstieg bei kürzeren Videos ist teils Arithmetik.
- **Weiterhin offen:** Diese Zahlen sind **Aufrufe**, nicht AVP%/3-s-Retention. Länge vs. Hook ist damit *plausibel* getrennt (Länge fällt als Faktor weg), aber der positive Hook-Beleg braucht noch AVP-Daten (V3-Analytics lag 2–3 Tage).

## Messgröße, die es wirklich entscheidet
Nicht Aufrufe (= Verteilungslotterie), sondern **durchschnittlich angesehener
Prozentsatz + Kurve der ersten 3 s**. **< 60 % = Anfang trägt nicht, ≥ 75 % = gut.**
Short frühestens **Tag 4–5** bewerten (YT) / in den ersten 10 Tagen (TikTok).

## Operational Implication
Beim Schnitt: Länge nicht nach Sekunden optimieren, sondern tote Sekunden killen.
Kraft in die ersten 3 s legen. → [[Learning-Hooks]], [[Learning-Storytelling-Shorts]].

## Competitor-Evidenz: Erfolgszone 44–60s (27.08.2026)
Externe Bestätigung durch Analyse von Top-Shorts bei HtSS + Scary Interesting (n=5, 1,27–28,3 Mio Views):
- Scary Interesting #1: 56s (5,73 Mio), #2: 60s (1,70 Mio), #3: 57s (1,27 Mio).
- HtSS #1: 47s (28,3 Mio), #5: 52s (5,34 Mio).
- **Unser Kanal-Durchschnitt: ~25s — 20 Sekunden unter der belegten Erfolgszone.**

Interpretation: Die Zone 19–39s war unser internes Erfahrungswert — Competitor-Daten zeigen, dass die Erfolgszone höher liegt. Nicht Länge an sich, sondern **ausreichend Raum für vollständige Narrative** (zweiter Spannungsbogen, Anagnorisis, Auflösung). Neue operative Zone: **40–55s als Ziel**, tote Sekunden weiterhin killen.

Confidence: High (externe Daten, 5 Datenpunkte, direkter View-Bezug).

## History
- **v1 (17.08.):** „unter 22 s: Faktor 7,9" (Vosk n=12).
- **v2 (18.–19.08.):** vidIQ + Kanal-Audit zeigen: Hook schlägt Länge; 34 s-Short gewinnt. Synthese „keine toten Sekunden, Zone 19–39 s".
- **v3 (24.08., n=35):** Faktor auf **0,9** gefallen — Längenvorteil verschwunden. San-José-Längenprobe hielt (917/915). „Hook > Länge" damit deutlich gestützt (Confidence high, aber auf Aufruf-Basis; AVP steht aus).
- **v4 (26.08., n=44, nb_observe.py):** Faktor **0.69** — lange Videos (≥22 s, n=38) Ø 847 Views vs. kurze (n=6) Ø 582 Views. Counter-Evidence zu v1, aber: kurze Videos (n=6) kaum repräsentativ; Kausalproblem — lange Videos existieren i.d.R. länger. Kein Entscheidungsbedarf. Bestätigt: Länge ist nicht der Hebel.
- **v5 (27.08.):** Competitor-Daten (n=5 Top-Shorts, 1,27–28,3 Mio) → Erfolgszone **44–60s**. Eigenes Ziel auf **40–55s** angehoben. Zone 19–39s war zu konservativ.
- **offen:** positiver Hook-Beleg über **AVP%** statt Aufrufe → [[Hypothese-Hook-schlaegt-Laenge]].

## Related
[[Learning-Hooks]] · [[Learning-Cross-Platform-TikTok]] · [[Video-02-San-Jose]] · [[Experiment-SanJose-Laengen-Test-Tag3]]
