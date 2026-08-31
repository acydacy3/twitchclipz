---
type: analytics
title: CTR-Benchmark & Monitoring
date: 2026-08-31
source: YouTube Studio "Aufrufe nach Videos", letzte 28 Tage (Nutzer-Screenshot)
confidence: High (echte Studio-Daten) für Benchmark; Medium für Kausalität der Muster
tags: [analytics, ctr, thumbnail, titel, monitoring]
---

# CTR-Benchmark & Monitoring (Stand 31.08.2026)

> **CTR + Impressionen sind NICHT über die YouTube-Analytics-API abrufbar** (getestet 31.08.: HTTP 400 für `impressions`/`impressionsClickThroughRate`). → Kommen je Analytics-Zyklus als **Studio-Screenshot** vom Nutzer, Claude extrahiert + loggt hier.

## Kanal-Benchmark (28 Tage)
- **57.216 Aufrufe · 142,6 Std Watch · 63 Abos · 69.944 Thumbnail-Impressionen · ⌀ CTR 1,5 %.**
- CTR-Kontext: Für Shorts stammt „Impressionen/CTR" v. a. aus Browse/Suche/Vorschläge (nicht Swipe-Feed). 1,5 % ist niedrig — Titel/erstes Bild lassen den Longtail liegen.

## Muster (belegt)
**🟢 Hohe CTR (>4 %) = Open-Loop-Titel + klarer Schock:**
- „Ein Damm bricht. **Dann passiert das**" — 8,4 % (262 Imp)
- „Ruhe Notfall Idee…" — 5,6 % (161 Imp)
- „Eine Welle – und das Schiff war weg" — 4,6 % (967 Imp)
- „Er erstickt an seiner eigenen Atemluft" — 4,5 % (4.710 Imp) **+5 Abos**
→ CTR-Beleg für Titel-Open-Loop ([[Learning-Titel]]).

**🔴 Reichweite verbrannt (CTR <0,5 % bei >1.500 Impressionen) — größte fixbare Verluste:**
- „Sie hörten… blind in den Sieg?" — 0,3 % @ 2.959 Imp
- „In 700m Tiefe… kein Ausg" — 0,4 % @ 3.763 Imp
- „Der Schäffchen retter… 50 Bergleute allein?" — 0,4 % @ 2.563 Imp
- „17 Jahre alt… Amazonas" — 0,2 % @ 2.039 Imp
→ YouTube zeigt sie, keiner klickt. Ursache: wirre/verstümmelte Titel + schwaches erstes Bild. Direkter Views-Beleg für F-V8-E (saubere Titel/Captions).

**Abo-Konzentration (körperliche Unmöglichkeit/Isolation):** „63 Mann, 700m tief" +6 · „erstickt" +5 · „Biber→Taucher" +4 · „3 Tage unter Wasser" +3. Viele Videos: 0 Abos.

**Watch-Time-Anker:** Okene-Luftblase-Longform ~90 von 142 Std (≈63 %). → Longform + Re-Run des Flaggschiff-Story-Typs ist Hebel.

## SCHWELLEN (permanent, ins Monitoring)
| Signal | Bedeutung | Aktion |
|---|---|---|
| CTR <0,5 % bei ≥1.500 Impressionen | Titel/Thumbnail-Leck (Reichweite verbrannt) | Titel überarbeiten (Open-Loop, sauber), Cover/erstes Bild prüfen — [[Learning-Thumbnails-Cover]], [[Learning-Titel]] |
| CTR >3 % | Gewinner-Muster | Titel-/Cover-Pattern replizieren, in [[Learning-Titel]] festhalten |
| Video mit +Abos ≥3 | Sub-Konverter | Story-Typ doppeln (Re-Run/nächste Reihe) |
| ⌀ CTR < 2 % (Kanal) | Longtail wird liegengelassen | Titel-Open-Loop + Cover-Qualität priorisieren |

## Monitoring-Mechanik (je Analytics-Zyklus, Tag 4–5)
1. Nutzer liefert Studio-Screenshot „Aufrufe nach Videos" (28 Tage).
2. Claude extrahiert je Video: Views · Watch · Abos · Impressionen · CTR → hängt eine datierte Zeile in dieses Log.
3. Flaggt gegen die Schwellen oben, leitet konkrete Titel-/Cover-Fixes ab.

## Related
[[Analytics-Loop]] · [[Learning-Titel]] · [[Learning-Thumbnails-Cover]] · [[Ziel-YPP-Monetarisierung]] · [[Observations]]
