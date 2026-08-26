---
type: system
title: Memory-Workflow
updated: 2026-08-24
tags: [system, workflow]
---

# Memory-Workflow — der Kreis, der das Gedächtnis schließt

Verwandt: [[Knowledge-Architecture]], [[Agent-Architecture]], [[Audit-System]].

## Session-Start
```
Session-Start
 → Statusbericht des Hooks lesen (Pipeline/Werkzeuge/Zugänge/Netz + Pflichtliste-Reminder)
 → CLAUDE.md ist geladen (Einstieg + Rules, inkl. n+1-Constraint)
 → [[Current-State]] öffnen
 → Bei Produktion: [[Produktion-Pflichtliste]] VOLLSTÄNDIG lesen (alle 13 Learnings,
   Werkzeug-Checklist, Konkurrenz-Referenz, Animation-Library) — nicht aus Gedächtnis
```
Retrieval-Regel: Die **Pflichtliste ist das Retrieval-Protokoll für Produktion** — sie listet
exakt welche Dateien zu lesen sind. Nichts weglassen, nichts überspringen, auch wenn
es bekannt erscheint. Confidence + Scope + Counter-Evidence jeder Note beachten.

## Während der Arbeit
- Vor jeder wichtigen Entscheidung: [[Knowledge-Architecture]] §5 (Retrieval) +
  [[Guardrails]] #3. Bereits Getestetes nicht grundlos wiederholen.
- Neue Beobachtung? → als `Observation` festhalten, nicht sofort zum Learning erklären.

## Nach jedem relevanten Arbeitsschritt (Selbstprüfung)
> „Haben wir gerade etwas gelernt, das eine zukünftige Session wissen sollte?"
- **Nein** → keine künstliche Note erzeugen. Qualität vor Quantität.
- **Ja** → passende Learning-/Failure-/Experiment-Note anlegen **oder** eine
  bestehende fortschreiben (Historie erhalten, nicht überschreiben).

## Session-Ende (`/merken`)
```
neue Erkenntnis
 → richtige Note im Vault (mit Confidence + Scope + Evidence + History)
 → prüfen: wird daraus eine Rule? → nur dann [[Current-State]]/CLAUDE.md anpassen
 → `git add/commit/push` (freigeschaltet) — erreicht die nächste Session automatisch
 → optional: geänderte Note nach Drive (nur für Nutzer-Ansicht in Obsidian)
```

## Persistenz-Priorität (git push freigeschaltet, 25.08.)
1. **Git** (`commit` + `push`) — primärer, versionierter Persistenz-Träger; der nächste Container klont den vollen Stand.
2. **Google Drive** — optional (Nutzer-Ansicht in Obsidian, Asset-Transfer via gdown).
3. **SendUserFile an Nutzer** — für fertige Videos (z. B. TikTok).

Details/Historie: [[Decision-Git-vs-Drive-Persistenz]].

## Selbstkorrektur (wenn eine Note falsch/veraltet/zu pauschal ist)
1. Problem markieren. 2. Evidenz prüfen. 3. Note aktualisieren (History!).
4. Änderung dokumentieren. 5. abhängige Rules prüfen. 6. CLAUDE.md prüfen.
7. betroffene Skripte/Prompts prüfen. Siehe [[Guardrails]] #6.
