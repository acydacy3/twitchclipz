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
 → Bei Produktion: [[Produktion-Pflichtliste]] VOLLSTÄNDIG lesen (alle in §2 gelisteten Pflicht-Dateien:
   Learnings + Failure-Memory + Animation-Library, Werkzeug-Checklist, Konkurrenz-Referenz) — nicht aus Gedächtnis
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
 → [[Autonomie-Log]] updaten: A/B/C/D-Score + Strafen + User-Prompts dieser Session
 → git add/commit → IMMER auf Feature-Branch UND auf main mergen + pushen (siehe unten)
 → optional: geänderte Note nach Drive (nur für Nutzer-Ansicht)
```

## ⚠️ PFLICHT: Vault-Änderungen IMMER auf main pushen

**Neue Container klonen `main`.** Vault-Änderungen nur auf einem Feature-Branch sind für
den nächsten Container unsichtbar — sie gehen verloren.

**Ablauf am Session-Ende (Reihenfolge einhalten):**
```bash
# 1. Auf Feature-Branch committen (wie bisher)
git add -A && git commit -m "..."
git push origin <feature-branch>

# 2. IMMER auf main mergen und pushen
git checkout main
git pull origin main          # Stand holen
git merge --no-ff <feature-branch> -m "merge: Vault + [Serie] → main"
git push origin main

# 3. Zurück auf Feature-Branch
git checkout <feature-branch>
```

**Was NICHT auf main gehört:**
- `*/render/*.mp4` — in .gitignore, via nb_build.py reproduzierbar
- Temporäre Zwischenstände die noch kaputt sind

**Kontrolle:** `git log --oneline main | head -3` → neuester Commit auf main soll
dem aktuellen Vault-Stand entsprechen.

## Persistenz-Priorität (git push freigeschaltet, 25.08.)
1. **Git `main`** — primärer, versionierter Persistenz-Träger; neuer Container klont main → voller Stand.
2. **Git Feature-Branch** — für laufende Arbeit, MUSS am Session-Ende in main einfließen.
3. **Google Drive** — optional (Nutzer-Ansicht, Asset-Transfer via gdown).
4. **SendUserFile an Nutzer** — für fertige Videos (z. B. TikTok).

Details/Historie: [[Decision-Git-vs-Drive-Persistenz]].

## Selbstkorrektur (wenn eine Note falsch/veraltet/zu pauschal ist)
1. Problem markieren. 2. Evidenz prüfen. 3. Note aktualisieren (History!).
4. Änderung dokumentieren. 5. abhängige Rules prüfen. 6. CLAUDE.md prüfen.
7. betroffene Skripte/Prompts prüfen. Siehe [[Guardrails]] #6.
