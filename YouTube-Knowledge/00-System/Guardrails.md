---
type: system
title: Guardrails
status: active
confidence: very high
updated: 2026-08-24
tags: [system, rules, guardrails]
---

# Implementation Guardrails

Diese Leitplanken haben **Vorrang** bei jeder Implementierung an den Knowledge-,
Memory-, Experiment- und Audit-Systemen. Quelle: Nutzer-Auftrag 24.08.2026.

1. **Protect the Existing System.** Das Bestehende (Pipeline, Ur-CLAUDE.md,
   Skills) funktioniert teilweise. Nicht neu bauen, was schon läuft. Erst
   analysieren. Bestehendes nur bei nachgewiesenem Nutzen oder nötiger
   Integration ändern. Keine großflächigen Refactorings ohne Begründung.
2. **Memory Must Be Persistent.** Relevantes Wissen darf nie nur im
   Session-Kontext leben: `Session → Erkenntnis → Vault → zukünftige Sessions`.
   (Persistenz-Träger ist der **Git-Vault**: `commit` + `push` (seit 25.08. freigeschaltet); Drive optional.)
3. **Retrieval before Reinvention.** Vor wichtigen Entscheidungen zuerst
   bestehendes Wissen suchen (Learnings, Experimente, [[Failure-Memory]],
   Decisions, Konkurrenz, Agenten-Learnings, aktuelle Rules).
4. **Learning Is Not Automatically a Rule.** Rules brauchen ausreichend Evidenz
   und einen klaren Scope. Unsicherheit bleibt sichtbar.
5. **Never Hide Uncertainty.** Nicht „das funktioniert", sondern z. B. „Hinweise,
   dass X funktioniert. Confidence: Medium."
6. **Preserve Contradictions.** Widerspricht neue Evidenz einem Learning:
   nicht löschen/überschreiben, sondern Re-Evaluation dokumentieren
   (siehe [[Knowledge-Architecture]] §3).
7. **Separate Memory From Code.** Vault = Wissen/Gründe/Evidenz/Entscheidungen.
   Git = tatsächliche technische Änderungen. Nicht unnötig vermischen.
8. **Minimal Complexity.** Vor jedem neuen Agent/Skill/Service/MCP prüfen:
   nötig? existiert schon? kann ein bestehender Agent das? erhöht es Lern-/
   Produktionsqualität wirklich? erhöht es Wartung unverhältnismäßig? →
   Bevorzugt wenige, klar abgegrenzte Komponenten. **Ein neuer Agent ist
   erlaubt, wenn dieser Test ihn rechtfertigt** — aktuell tut das keines der 5
   Advanced-Systeme, deshalb sind sie Workflows im Vault statt eigener Agenten.
9. **Human Control Over Irreversible Changes.** Bei strategischen Änderungen mit
   großer Auswirkung erst analysieren + Vorschlag machen, bevor Produktionsregeln
   fundamental geändert werden. Betrifft: Agent-Architektur, Production Rules,
   Monetarisierung, große Prompt-/Skill-Änderungen, Entfernung von Funktionalität.
10. **The Ultimate Objective.** Nicht mehr produzieren, sondern die
    **Entscheidungsqualität** je Zyklus erhöhen (siehe [[Mission]]).

## Präzedenzfall — Guardrail-Verletzung 27.08.2026

**Was passiert ist:** Competitor-Analyse ergab, dass HtSS/Scary Interesting Top-Shorts 44–60s lang sind. Daraus wurde fälschlicherweise eine **promoted Rule** gemacht (Short-Länge Ziel 40–55s) und in Current-State.md + Learning-Retention-und-Laenge.md als operative Guideline eingetragen — obwohl unsere interne bewiesene Zone 19–39s (n=44) nie widerlegt wurde.

**Warum falsch:** Externer Survivorship-Bias (nur Gewinner sichtbar) + andere Kanal-DNA = kein Beweis für unseren Kanal. Guardrail #4 „Learning is not automatically a Rule" und #9 „Human Control Over Irreversible Changes" wurden verletzt.

**Korrektur:** Competitor-Längen-Beobachtung als Low-Confidence-Hypothese herabgestuft. Interner n=44-Befund bleibt operative Grundlage. Experiment ab V8 vorgeschlagen.

**Fixe Regel daraus (ab sofort):**
> **Externe Competitor-Daten dürfen niemals eine intern gemessene und bewiesene Rule überschreiben.** Sie können als Hypothese eingetragen werden, brauchen aber ein internes A/B-Experiment und eigene Daten bevor sie zu einer Rule werden. Competitor zeigt Möglichkeit, nicht Verpflichtung.

## Anwendung in diesem Vault
- Migration der Ur-CLAUDE.md: **verbatim archiviert** unter
  `00-System/_archive/`, keine Information gelöscht (→ #1, #6).
- Behauptungen ohne Evidenz aus der Ur-Datei sind als solche gekennzeichnet,
  nicht als Learning „geadelt" (→ #4, #5).
- CLAUDE.md wurde **nicht blind** gekürzt, sondern nach Analyse zum schlanken
  Einstieg umgebaut, der hierher verweist (→ #1, #9).
