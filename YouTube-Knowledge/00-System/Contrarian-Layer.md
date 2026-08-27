---
type: system
title: Contrarian-Layer
updated: 2026-08-27
tags: [system, contrarian, red-team, produktion]
---

# Contrarian / Red-Team Layer

**Zweck:** Nicht optimieren — beweisen, dass die aktuelle Strategie falsch oder unvollständig ist.
Und: **garantieren, dass bewiesene Learnings tatsächlich angewendet werden**, nicht nur dokumentiert.

## Zwei Modi

### Modus 1 — Produktions-Gate (vor JEDEM Render/Upload)
```bash
python3 tools/nb_contrarian.py short07.json   # prüft Konfig automatisch
python3 tools/nb_contrarian.py --kurz          # nur HIGH+VERY_HIGH Regeln
```
Prüft automatisch: Musik-db · Hook · Hook-Until · Titel-Länge · Emoji · Shots · Audio · Words · Font.
Gibt außerdem die manuelle Checkliste aus: Bilder-Sourcing · SEO-Tools · Retention · Karaoke · Upload-Reihenfolge.

### Modus 2 — Strategie-Audit (wöchentlich / vor V-Planung)
```bash
python3 tools/nb_contrarian.py                 # voller Vault-Learning-Report
```
Zeigt alle Learnings mit Confidence-Level und aktuellem Stand.
Identifiziert Gegenbeweise und noch ungelöste Widersprüche.

## Cross-Cutting-Layer (alle Domänen)

Der Contrarian prüft NICHT nur SEO. Er ist der letzte Checkpoint in jeder Produktionskette:

| Domäne | Kernregel | Confidence |
|---|---|---|
| **Ton** | Musik db ≥ -18 (Ziel -16) + volumedetect nach Render | Very High |
| **Hook** | Jeder Short hat Hook · Hook ≠ gesprochenem Satz · ≤ 4 s | Very High |
| **Captions** | Untertitel = Stimme 1:1 | Very High |
| **Titel** | Aussage bei Zeichen 35 · kein Emoji | Very High |
| **SEO** | Min. 1 starkes Keyword · nb_suggest + nb_trends vorher | High |
| **Bilder** | Schlüsselmoment generieren · Kontaktabzug QC | High |
| **Retention** | Zone 19-39 s · tote Sekunden raus | High |
| **Upload** | analyse.py vorher · TikTok NIE automatisch | Very High |
| **Persistenz** | git commit + push nach Session | Very High |

## Epistemik-Checks (manuell, wöchentlich)

```
Belief: "X funktioniert besser"
→ Welche Videos widersprechen diesem Glauben?
→ Stichprobengröße? (n < 10 = Low Confidence)
→ Confounder? (Thema, Länge, Slot, Wochentag)
→ Funktioniert X nur in Kombination mit Y?
→ Ist das Learning > 14 Tage alt ohne neue Evidenz? → neu testen
```

## Aktuelle offene Widersprüche

| Belief | Gegenbeweise | Status |
|---|---|---|
| „Hook schlägt Länge" | Sample klein; Hook/Länge nicht getrennt | Hypothese → [[Hypothese-Hook-schlaegt-Laenge]] |
| „Kürze gewinnt (Faktor 7,9)" | Confounder Hook-Qualität · 27.08: Faktor 0,69 (lang>kurz) | WIDERLEGT → [[Learning-Retention-und-Laenge]] |
| „San-José-Titel-Formel" | Kausalitätsproblem: älteres Video = mehr Zeit für Views | Medium → [[Hypothese-Ueberlebens-Titel-Formel]] |

## Wichtig

- **Nicht aus Prinzip widersprechen.** Ist die Evidenz stark → ausdrücklich anerkennen.
- Ziel: Überzeugungen durch **Evidenz** behalten, nicht durch Selbstbestätigung.
- Strafen im Autonomie-Log, wenn der Nutzer Dinge ansprechen muss, die hier hätten aufgefangen werden sollen.

## Related

[[Evidence-Confidence]] · [[Audit-System]] · [[Failure-Memory]] · [[Produktion-Pflichtliste]]
