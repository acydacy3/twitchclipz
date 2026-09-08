---
type: analytics
title: Observations
updated: 2026-09-08
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

## 2026-09-08 (Bildherkunft)

- [2026-09-08] **Das autonome Bildwerkzeug hat noch nie ein Bild geliefert.**
  `nb_openverse.py` gab bei jedem Aufruf „Openverse: 0 Bilder" zurück, mit
  Exit-Code 0. Ursache war die Dateiendung `.raw` beim Zwischenspeichern.
  `[bestätigt]` → F-V9-R. **Konsequenz für die Deutung älterer Sessions:**
  Wo im Log steht, Bilder seien „per Openverse beschafft" worden, ist das
  falsch — sie kamen anderswoher.

- [2026-09-08] **Acht von dreißig Bildern im Nutty-Putty-Langvideo hatten
  keinen Bezug zum Stoff** (Zeltlager mit lachenden Menschen, historische
  Soldatenfotos, ein Straßen-Schrein), und alle vier Longform-Regeln waren
  grün. `[bestätigt]` → F-V9-T.
  **Methodische Lehre, zum zweiten Mal an einem Tag** (nach F-V9-O): Ein Gate
  misst, was eine Datei *ist*, nie, was sie *zeigt*. Der Kontaktabzug vor dem
  Upload ist deshalb kein Zusatzschritt, sondern der einzige Prüfpunkt für
  Bildinhalt, den es gibt.

---

## 2026-09-08 (Langvideos)

- [2026-09-08] **Der Kanal hatte 2 Langvideos bei 86 Videos.** Tham Luang
  (5:39, 13 Aufrufe) und Koepcke (4:29, 64 Aufrufe) — beide aus dem August.
  Sechs Serien hatten keines. Heute kamen Ralston (5:51, terminiert 12.09.) und
  Prosperi (3:42, terminiert 13.09.) dazu. `[beobachtet]`
  **Erwartung ausdrücklich offen:** Ob Langvideos auf diesem Kanal tragen, ist
  unbelegt. Die zwei vorhandenen haben 13 und 64 Aufrufe — das ist wenig, aber
  bei n=2 und ohne AVP-Daten keine Aussage. Frühestens ab Tag 4–5 nach dem
  12.09. bewertbar, dann gegen die Shorts derselben Serie.

- [2026-09-08] **Der Longform-Bauer lieferte Videos aus einem einzigen Bild.**
  5:55 Laufzeit, 62 geplante Einstellungen, **0 Bildwechsel**. Die drei
  Longform-Regeln (Länge, Format, Lautheit) gingen alle grün durch.
  `[bestätigt]` → F-V9-O, neue Regel R29 zählt jetzt die Schnitte.
  **Methodische Lehre:** Regeln, die Dateieigenschaften messen, sagen nichts
  darüber, ob ein Video etwas zeigt. Für jede Eigenschaft, die ein Zuschauer
  sofort sieht, braucht es eine eigene Messung — oder einen Blick.

- [2026-09-08] **Alle zehn Prosperi-Short-Titel tragen „| Doku".** Die Regel
  dagegen gilt seit dem 27.08. (Competitor-Analyse: kein Top-Performer nutzt
  Genre-Labels) und wurde bei V7 nie angewandt. Aufgefallen erst, als das Gate
  die Titel prüfte. `[beobachtet]` — Titel sind Nutzer-Domäne, nicht geändert.

---

## 2026-09-08

- [2026-09-08] **V7 Prosperi korrigiert sich nach unten: AVP 69,3 % → 61,7 %.**
  Gestern waren erst 3 von 10 Videos in den Analytics, heute 9 von 10. Damit
  ist Prosperi die **zweitschwächste** Serie nach V6 Nutty Putty (53,5 %).
  Reihenfolge nach gesehenem Anteil: V1 76,4 · V3 71,4 · V5 64,9 · V4 64,3 ·
  V2 61,7 · V7 61,7 · V6 53,5. `[Muster]`
  **Lehre zur Methode:** Ein AVP-Wert mit weniger als etwa 7 von 10 gemessenen
  Videos ist noch keine Aussage — der Analytics-Verzug verschiebt ihn um bis zu
  8 Punkte. Der Serienvergleich braucht Tag 4–5, nicht Tag 1.

- [2026-09-08] **Der automatische Messpunkt hat zum ersten Mal von selbst
  gegriffen.** `snapshots/2026-09-08.json` entstand ohne Zutun im
  Sitzungsstart-Hook. Das ist die Gegenprobe zu Befund 4: die Snapshot-Pflicht
  stand seit dem 26.08. in der Pflichtliste und lief dreimal. Als Automatik
  läuft sie. `[bestätigt]`
  **Kleiner Schönheitsfehler:** Der Statusbericht liest die Snapshot-Liste,
  bevor der Hintergrund-Snapshot fertig ist, und meldet deshalb beim Start noch
  den Vortag. Kein Fehlverhalten — die Regel R19 erlaubt bis zu einem Tag
  Rückstand. Nur beim Lesen wissen.

- [2026-09-08] **V8 Ralston, erste drei Shorts live** (die korrigierten
  Fassungen mit Bewegung, Untertiteln aus dem Skript und −15 LUFS).
  Stand wenige Stunden nach Veröffentlichung: Short 01 = 745 Aufrufe,
  Short 03 = 21, Short 02 = 6. `[beobachtet]`
  **Ausdrücklich noch keine Aussage.** Bei wenigen Stunden Alter sagt die
  Streuung nichts. Belastbar wird das an Tag 4–5 (12./13.09.) — dann gegen
  V4 Okene (bestes AVP der jüngeren Serien, 64,3 %) prüfen.

---

## 2026-09-07

- [2026-09-07] **AVP% erstmals gezogen — die Zahl war die ganze Zeit verfügbar.**
  Die YouTube-Analytics-API liefert `averageViewPercentage` je Video über
  `reports().query(dimensions="video")`. Der Vault notiert seit dem 24.08.
  „AVP%/3-s-Retention steht aus" — es war ein einziger API-Aufruf.
  Werte (Median je Serie): V1 76,4 · V2 61,7 · V3 71,9 · V4 64,2 · V5 64,9 ·
  V6 **53,6** · V7 69,3 (erst 3/10 wegen Analytics-Lag). `[Muster]`
  **Bedeutung:** AVP% wächst nicht mit dem Alter — anders als Aufrufe. Damit ist
  es die erste Zahl, mit der sich Serien überhaupt fair vergleichen lassen.
  V6 Nutty Putty liegt bei 53,6 % und damit nahe an dem Bereich, ab dem ein
  Short laut Shorts-Benchmarks 2026 die Verteilung im Feed verliert (~50 %).

- [2026-09-07] **Der Selbst-Score ist gegenläufig zur Qualität.** Autonomie-Score
  V4→SYS5: 48 → 55 → 62 → 68 → 81 → 88 → 91 → 82 → 88. AVP% im selben Zeitraum:
  64 → 65 → 54. Die fünf höchsten Scores stammen aus Sitzungen ohne ein
  einziges produziertes Video. `[bestätigt]` → [[Autonomie-Log]] stillgelegt.

- [2026-09-07] **Zwei Serien sind dauerhaft unbewertbar.** Altersbereinigte
  Aufrufe (Video-Alter 2–3 Tage) existieren nur für V3 (1.212), V4 (1.702) und
  V7 (993) — für V5 und V6 wurde zum passenden Zeitpunkt kein Snapshot gezogen
  (letzter Snapshot: 29.08.). 20 Videos ohne Ergebnis, nicht nachholbar.
  `[beobachtet]` **Konsequenz:** täglicher Snapshot ist Pflicht, nicht Kür —
  `python3 tools/kp_metrik.py --snapshot`.

- [2026-09-07] **Prosperi-Einbruch ist NICHT sauber auf die Captions
  zurückzuführen.** Die Aufrufe der Serie streuen extrem (5 bis 1.205), aber
  die niedrigen Werte betreffen überwiegend die jüngsten Videos (1 Tag alt).
  Eine Ausnahme bleibt erklärungsbedürftig: Short 02 (26 Aufrufe) gegen zwei
  Geschwister vom selben Tag (998 und 1.205). Recency erklärt das nicht.
  `[beobachtet]` — **keine Kausalaussage.** Für einen Beleg fehlt der
  altersgleiche Vergleich, den die fehlenden Snapshots unmöglich machen.

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
| 2026-08-31 | Bewegtbild-Pflicht als Regel eingeführt (15:17 Uhr) | 0 Videos bis 06.09.; Ralston (10:17 gerendert) blieb zu 50 % Standbild | [bestätigt] |
| 2026-09-07 | Harte Gates + PreToolUse-Riegel eingeführt | Fing sofort 29 Verstöße in Prosperi + 5 Standbild-Shorts in Ralston | [beobachtet] |
| 2026-09-07 | Manim-Bühne im Hochformat korrigiert (F-V9-E) | Alle Animationen füllen erstmals das Bild | [beobachtet] |
| 2026-09-08 | V8 Ralston vollständig ausgetauscht (Bewegung + Untertitel + −15 LUFS) | Ergebnis ab Tag 4–5 (12.09.) messbar | [offen] |

*Diese Tabelle wächst mit jeder Session. Nach 5+ Einträgen: Muster suchen → Hypothese.*

---

## Related
[[Autonomie-Log]] · [[Experiment-Manager]] · [[Hypotheses-Übersicht]] · [[Learning-Retention-und-Laenge]]
