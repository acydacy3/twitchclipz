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
 → Statusbericht des Hooks lesen (Pipeline/Werkzeuge/Zugänge/Netz)
 → CLAUDE.md ist geladen (Einstieg + Rules)
 → [[Current-State]] öffnen
 → relevantes Wissen GEZIELT retrieven (nicht das ganze Vault)
```
Retrieval-Regel: erst überlegen, **welches** Wissen die Aufgabe braucht, dann
gezielt in `01-Learnings/`, `02-Experiments/`, `09-Failures/`, `05-Decisions/`
suchen. Confidence + Scope + Counter-Evidence jeder gefundenen Note beachten.

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
 → git add/commit/push  (Persistenz — seit Push frei)
 → Fallback: nach Google Drive sichern + Datei an Nutzer schicken
```

## Persistenz-Priorität (seit `git push` frei ist)
1. **Git** (Repo-Vault) — primärer, versionierter Persistenz-Träger. Historie inklusive.
2. **Google Drive** — Fallback, wenn Push scheitert (403 o. ä.).
3. **SendUserFile an Nutzer** — letzter Fallback (er lädt manuell hoch).

Warum diese Reihenfolge neu ist: Der Drive-Umweg entstand nur wegen der
früheren Push-Sperre. Details + Widerspruchsauflösung: [[Decision-Git-vs-Drive-Persistenz]].

## Selbstkorrektur (wenn eine Note falsch/veraltet/zu pauschal ist)
1. Problem markieren. 2. Evidenz prüfen. 3. Note aktualisieren (History!).
4. Änderung dokumentieren. 5. abhängige Rules prüfen. 6. CLAUDE.md prüfen.
7. betroffene Skripte/Prompts prüfen. Siehe [[Guardrails]] #6.
