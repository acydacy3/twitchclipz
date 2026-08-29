---
type: system
title: Ziel-YPP-Monetarisierung
status: active
updated: 2026-08-25
tags: [system, ziel, ypp, monetarisierung, metrik, nordstern]
---

# Nordstern-Ziel: YPP-Monetarisierung über den Shorts-Pfad

> **Das übergeordnete, messbare Ziel des Kanals.** Jede Session prüft den Fortschritt (kostenlos via `analyse.py`) und trägt eine Zeile in die Tabelle unten ein. Vor der neuen YPP-Regelung ab **Februar 2027** einsteigen.

## Zielkriterium (YouTube Partner Program, Shorts-Pfad)
- **1.000 Abonnenten** UND
- **10.000.000 gültige öffentliche Shorts-Views in 90 Tagen (rollierend).**

## Baseline (25.08.2026, `analyse.py`)
- **42 Abonnenten** → 4,2 % des Ziels (1.000).
- **20.321 Views gesamt.** Kanal gegründet 15.08.2026 (~10 Tage alt) → **90-Tage-Views ≈ Gesamt-Views** = 20.321 → **0,20 % des 10-Mio-Ziels.**
- 40 Videos, ~19 terminiert.

## Was das quantitativ bedeutet (realistisch, Stand 29.08.2026)

| Metrik | Ist | Soll | Faktor |
|--------|-----|------|--------|
| Views/Tag (7d-Schnitt) | ~1.500 | 111.000 | ×74 |
| Abonnenten | 58 | 1.000 | ×17 |

**Realistische Horizonte:**
- **Abonnenten-Ziel (1.000):** 3–5 Monate bei konsequenter Serien-Qualität (1 viral gehendes Video reicht).
- **10-Mio-Shorts-Views:** 9–12 Monate. Eine einzelne Serie, die viral geht (100K+ Views), kann das Tempo signifikant verschieben — aber das ist nicht planbar, nur wahrscheinlicher machbar durch Qualität + Volumen.
- **Vor Februar 2027 einsteigen** bleibt realistisch, wenn ab Sep. 2026 monatlich 150K+ Views erreicht werden (nächste Stufe: 1 viral Short pro Serie).

**Wachstums-Trigger (priorisiert):**
1. CTR erhöhen — Thumbnail-Qualität (prüfen via YouTube Studio, Spalte "Klickrate")
2. Sub-Conversion — CTA "Kanal folgen" (ab V8-Ralston eingebrannt, letzte 4s jedes Shorts)
3. Long-Form pro Serie — baut Watch Time + Suchtraffic, zieht Abos nach
4. Systematisches A/B-Testing von Hook-Typen — 2 Varianten je Serie, Titel-Unterschied

**Abo-Ziel (1.000) ist der realistisch erreichbare erste Meilenstein** (ca. Q1 2027).
Das 10-Mio-Views-Fenster öffnet sich, sobald 1–2 Shorts viral gehen (>50K Views).

## Hebel (aus den Learnings, priorisiert)
1. **Hook / erste 3 s** — der belegte Haupthebel für Reichweite. → [[Learning-Hooks]], [[Learning-Retention-und-Laenge]]
2. **Taktung 3 Shorts/Tag, durchlaufend** — mehr Lose in der Verteilungslotterie. → [[Produktions-Runbook]]
3. **Animation + dynamischer Schnitt** statt statischer Diashow. → [[Experiment-Cheap-Animation-Querschnitt]], [[Learning-Editing-Video]]
4. **Referenz-getriebene, authentische Schlüsselbilder** (Standort-Look). → [[Learning-Bilder-Prompts]]
5. **Themenwahl mit Suchlücke + Viral-Muster** (1-von-N-Überlebt, DE-ungesättigt). → [[Ideen-Pipeline]], [[Learning-Topics-Themenwahl]]
6. **Analytics-Loop** Tag 4–5 → Post-Mortem → nächstes Video steuern. → [[Analytics-Loop]]

## Messmechanik (wöchentlich, kostenlos)
- **Jede Session/Audit:** `analyse.py` ziehen, Zeile ergänzen. Solange Kanal < 90 Tage: 90-Tage-Views = Gesamt-Views.
- **Ab ~90 Tagen (Mitte Nov. 2026):** echte rollierende 90-Tage-Shorts-Views nötig → `analyse.py` um YouTube-Analytics-Query erweitern (`views`, letzte 90 Tage, Shorts). Kostenlos (Analytics-API).
- **Fortschritt %** = 90-Tage-Views / 10.000.000. **Tempo-Check** = Views/Tag (7-Tage-Schnitt) vs. Soll 111.000.

## Fortschritts-Log
| Datum | Abos | 90-Tage-Views | Views/Tag (7d) | Fortschritt Views | Fortschritt Abos | Notiz |
|-------|------|---------------|----------------|-------------------|------------------|-------|
| 2026-08-25 | 42 | 20.321 | ~2.000 | 0,20 % | 4,2 % | Baseline. V6 Nutty Putty terminiert (31.08–03.09). Faktor ~55 zum Views-Soll. |
| 2026-08-26 | 42 | 23.727 | ~3.406 | 0,24 % | 4,2 % | V6 Upload komplett (10/10). 25 terminiert. Views +3.406 in 1 Tag — bestes Tageswachstum. |

## Related
[[Current-State]] · [[Mission]] · [[Analytics-Loop]] · [[Learning-Hooks]] · [[Learning-Retention-und-Laenge]] · [[Ideen-Pipeline]]
