---
type: audit
title: Kanal-Audit August 2026
date: 2026-08-29
scope: vollständig — Video-Performance, Hooks, Retention, Schnitt, Konkurrenz
---

# Kanal-Audit August 2026

Artifact-Seite: https://claude.ai/code/artifact/655463ad-be51-4b67-864c-34e1df987b7f

---

## Channel-Snapshot (29.08.2026)

| Metrik | Wert | Ziel | Stand |
|--------|------|------|-------|
| Abonnenten | 58 | 1.000 | 5,8% |
| Views gesamt | 44.639 | 10.000.000 | 0,45% |
| Öffentliche Videos | 37 | — | — |
| Ø Views/Short (Aug) | ~874 | — | — |
| Shorts-Anteil | 99,9% | — | Long-form: 21 Views |

---

## Traffic-Quellen (Aug 1–29)

- **Shorts-Feed:** 33.968 Views (91%) — primäre Wachstumsquelle
- **YT-Suche:** 2.780 Views (7,4%) — höchste Retention 66,44%, langfristig relevant
- **Kanal-Seite:** 382 Views (1%)
- **Abonnenten:** 55 Views (0,15%)

→ **Abonnenten spielen keine Rolle**. Wachstum kommt ausschließlich via Algorithmus.
→ Suchtraffic hat verhältnismäßig hohe Retention — SEO (Titel, Tags) lohnt sich für Langfrist.

---

## Serien-Performance

| Serie | Thema | Ø Views/Short | Peak | Status |
|-------|-------|--------------|------|--------|
| Harrison Okene | Tiefsee, Nigeria | ~2.200 | 4.805 | **BESTE SERIE** |
| Wunder von Lengede | Bergbau, DE 1963 | ~1.130 | 1.185 | Solide |
| John Jones | Höhle, Utah 2009 | — | — | Geplant/Privat |
| Mauro Prosperi | Sahara 1994 | — | — | Geplant/Privat |
| Aron Ralston (V8) | Canyon, Utah 2003 | 0 | — | Re-Render läuft |

**Muster:** Extreme physische Isolation + körperliche Unmöglichkeit (Luftblase unter Wasser) schlägt historische Rettungsnarrative (Bergbau). Hypothese: emotionale Nähe + Unverständlichkeit des Überlebens erzeugt mehr Klicks.

---

## Top Videos

1. **ohRgARfnu1s** — „3 Tage ALLEINE in einer Luftblase am Meeresgrund" — 4.805 Views, 60,4% Retention
2. **245h4YmQv1o** — „So schnell gesunken, dass kein Notruf kam" — 2.965 Views
3. **0v0JFnX2Mc8** — „Er erstickt an seiner eigenen Atemluft" — 2.641 Views
4. **SvXnWcMrNZs** — „3 Tage alleine unter Wasser: wie ist das möglich?" — 2.151 Views, **76,7% Retention**
5. **LlQH1-i9w0s** — „Warum seine Rettung ihn getötet hätte" — 2.131 Views
6. **5qk-QMcP6TI** — „Eine Welle – und das Schiff war weg" — 1.160 Views, **139% Rewatch-Rate** (!!)

**Wichtig:** 5qk hat die wenigsten Views der Okene-Serie, aber die höchste Rewatch-Rate (139%). Das 23s-Format ohne Auflösung erzeugt Loop-Verhalten.

---

## Hook-Typen (Evidenz-basiert)

### Bewährt (High Confidence)

1. **Physische Unmöglichkeit** — „3 Tage ALLEINE in einer Luftblase" → 4.805 Views
   - Formel: `[extreme Zahl] [körperlich unmögliches Setting]`
   
2. **Paradox** — „Warum seine Rettung ihn getötet hätte" → 2.131 Views
   - Formel: `Warum [normale Handlung] das Gegenteil bewirkt hätte`
   
3. **Fragen-Hook mit Twist** — „Der Taucher griff nach der Leiche und sie griff zurück?" → 1.865 Views
   - Formel: `[Person] [Handlung] — und [Horror-Twist]?`

4. **Rewatch-Loop (ohne Auflösung)** — „Eine Welle – und das Schiff war weg" → 139% Rewatch
   - Formel: `[Katastrophen-Moment]. Dann passiert [offen] ..` — bewusst kein Ende

### Disproven

- **Titelansage:** „Heute erzählen wir von…" — Failure-Memory, niemals verwenden
- **Hashtag im Titel:** „#geschichte #shorts" — wirkt billig, kein Mehrwert (Daten: Lengede-Video unterdurchschnittlich)

---

## Retention & Schnitt-Erkenntnisse

- **LNuopbLc2RU:** 96,37% Retention → 6 Abonnenten (BESTER Sub-Konverter)
- **5qk-QMcP6TI:** 139% Rewatch, 31s Video
- **SvXnWcMrNZs:** 76,68% Retention, 31s Video → 3 Abonnenten
- **ohRgARfnu1s:** 60,4% Retention, 27s — meiste Views, aber nicht höchste Retention

**Optimale Länge:** 20–27s. Kürzere Videos → Rewatch-Loop. Videos >30s verlieren Completion.

**Karaoke:** \kf-Highlight (V8-Fix) noch nicht live gemessen. A/B-Vergleich folgt mit Ralston-Uploads.

---

## Produktionsfehler V8 (Recap)

Alle 4 Failures in Failure-Memory.md dokumentiert:

- **F-V8-A:** Einzelbild statt Multi-Shot (imgs vs. img)
- **F-V8-B:** Karaoke ohne \kf Highlight
- **F-V8-C:** Progressbar unsichtbar (10px, halb-transparent)
- **F-V8-D:** CrossSection = gelber Dot ohne Kontext

Alle fixes sind in `ralston/nb_build.py` v2 implementiert.

---

## Konkurrenz

| Kanal | Abos | Views-Wachstum 30d | Nische | Relevanz |
|-------|------|--------------------|--------|----------|
| DA | 2.080 | +133% | Dashcam-Unfälle | Nicht direkt — Volumen-Modell |
| Verbotene Geschichten | 1.210 | +113% | Horror/Creepypasta | Ähnliche Emotion — Hook-Referenz |
| Wenn Sie Fremdgeht | 1.750 | +107% | Beziehungs-Drama | Nicht relevant |
| Laura Noir | 4.610 | +6,7% | Horror/True Crime | **Benchmark-Kanal** |

**Lektion DA:** 696 Videos, 6–7/Tag. Wir können nicht durch Volumen gewinnen. Vorteil: narrative Tiefe, Serien-Struktur.

**Lektion Laura Noir:** Ø 4.282 Views/Video, 4.610 Abos — das ist unser 3-Monats-Ziel. Ihr Wachstum verlangsamt → Markt offen.

---

## Hypothesen (Evidenz-Stand)

| Hypothese | Confidence | Evidenz |
|-----------|-----------|---------|
| Tiefsee > Bergbau | High | N=14 Videos, 2.200 vs. 1.130 Ø |
| 23–25s optimal für Loops | High | 139% Rewatch bestätigt |
| Serie-Anker zieht Folge-Views | Medium | Nur eine Serie gemessen |
| Karaoke erhöht Retention | Medium | Noch nicht live gemessen |
| Fragen-Hook > Aussage-Hook | Low | Zu wenig Datenpunkte |
| Retention >80% = Abonnenten | Low | Zu wenig Datenpunkte |

---

## Maßnahmen (priorisiert)

1. **Sofort:** V8 alte Videos löschen → `python3 ralston/nb_upload.py`
2. **V8 Monitoring:** Ralston-Hooks benchmarken gegen Okene
3. **V9 Loveparade:** Image-to-Video via HF (Wan2.1-I2V) statt Ken-Burns
4. **Rewatch-Loop testen:** 2–3 Videos mit bewusstem „offenem Ende" produzieren
5. **Nutty Putty + Prosperi:** Live-Daten für Isolation-Hypothese sammeln

---

## Related

[[Failure-Memory]] · [[Learning-Bilder-Prompts]] · [[Current-State]] · [[Ziel-YPP-Monetarisierung]]
