---
type: process
status: active
confidence: high
created: 2026-08-24
updated: 2026-08-24
tags: [audit, analytics, loop, prozess, retention]
---

# Analytics-Loop — von Video zu Video besser werden

> Verbindlicher datengetriebener Kreis: **jedes Video liefert Evidenz, die das nächste
> steuert.** Gemessenes schlägt Notiertes (Guardrail: Zahlen vor Vermutung).

## Wann
- **Pro Short:** Tag **4–5** nach Upload (YT-Analytics-Lag 2–3 Tage → vorher nicht bewerten).
- **Pro Video-Serie:** beim **Weekly-Audit** ([[Audit-System]]) gesammelt.

## Was ziehen (`analyse.py` + YT Analytics API)
Je Short: Aufrufe, Aufrufe/Tag, **AVP% (durchschn. angesehener Prozentsatz)**, frühe/3-s-Retention,
Impressionen-**CTR** (1. Frame = Thumbnail), Likes/Engagement, **Abos aus Video**.
Kanal: Abos, Gesamt-Aufrufe, Traffic-Quellen (For-You vs. Suche vs. Kanal).

## Der Entscheider
- **AVP% + CTR entscheiden, nicht Aufrufe** (Aufrufe = Verteilungslotterie).
- Schwellen (aus [[Learning-Retention-und-Laenge]]): **AVP < 60 % = Anfang trägt nicht; ≥ 75 % = gut.**

## Was daraus folgt (Post-Mortem je Video)
1. **Video-Note** (`03-Videos/`) mit den Messwerten aktualisieren (Hook, Länge, Thema, Performance, Überraschungen).
2. **Learnings fortschreiben** — Confidence neu bewerten, Widersprüche via `History` bewahren (nicht überschreiben).
3. **Konkrete Anweisung fürs nächste Video** ableiten: welche **Hook-Bauform**, welche **Länge**, welches **Thema-Muster** (Gewinner wiederholen, Verlierer meiden).
4. Bei Bedarf `Current-State` Kern-Rules anpassen; `/merken` autonom.

## Aktueller Stand (24.08., n=36)
- Gewinner-Hook = **Zahlen-/Kontrast-Kalt-Einstieg** („92 Passagiere. 1 Überlebende." 1.807).
- **Länge kein Faktor** (19–39 s, Faktor 0,9) → Kraft in Hook + tote Sekunden killen.
- **Offen:** AVP% für V3 (Amazonas) noch nachziehen → dann Hook-These auch über Bindung belegt.
- **Flops als Warnung:** vage/eklige Hooks („50 Maden im Arm" 11 Aufrufe), Langform tot (5:39 → 10, 4:29 → 0).

## Related
[[Audit-System]] · [[Memory-Workflow]] · [[Learning-Retention-und-Laenge]] · [[Learning-Hooks]] · [[Current-State]]
