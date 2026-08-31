---
description: Persistiert neue Erkenntnisse → Git (commit + push, freigeschaltet); Drive optional
---

# Merken

Der Nutzer hat „merken" geschrieben, **oder** eine Arbeitssitzung geht zu Ende,
**oder** ein Meilenstein ist erreicht. Dann läuft dieser Ablauf — auch ungefragt.

Zweck des Projekts (Nutzer-Worte): *„Learning gemerkt, Fehler gemerkt, verbessert,
immer aktueller Stand ohne Befehl."* Dieser Befehl ist die Hälfte davon, die nicht
von allein läuft.

> **Stand 25.08.2026:** `git push` ist **freigeschaltet** — Persistenz läuft über
> **Git (`commit` + `push`)**; der nächste Container klont den vollen Stand. Drive optional.
> Siehe `YouTube-Knowledge/05-Decisions/Decision-Git-vs-Drive-Persistenz.md`.

---

## Schritt 1 — Ins Vault eintragen (das Gedächtnis)
Trag jede neue Erkenntnis in die **passende Note** unter `YouTube-Knowledge/` ein:
- Learning → `01-Learnings/<Domain>/` · Fehler → `09-Failures/` · Experiment → `02-Experiments/` · Entscheidung → `05-Decisions/`.
- **Ergänzen/fortschreiben, nie überschreiben.** Widerspricht neue Evidenz einem Learning: `## Counter Evidence` + `## History` + `confidence` neu (siehe `00-System/Knowledge-Architecture.md`).
- Jede substanzielle Note trägt **Confidence** (Low/Medium/High/Very High) und **Scope**.
- **Nichts erfinden.** Nur gemessene Zahlen/echte Ergebnisse. Unklares als `Unknown`/`Hypothesis` markieren.

**Prüfen:** Wird daraus eine **Rule**? Nur dann `00-System/Current-State.md` (und
ggf. `CLAUDE.md`) anpassen — sonst bleibt es im Vault (Memory-Promotion).

**Selbstprüfung:** Ist wirklich nichts Neues dazugekommen? Dann **keine künstliche
Note** erzeugen. Qualität vor Quantität.

## Schritt 2 — Persistieren (ZWINGEND auf `main`)
> **Neue Container klonen `main`.** Ein Push nur auf den Feature-Branch erreicht die nächste Session NICHT. Deshalb IMMER auf `main` mergen.
1. **Auf Feature-Branch committen:** `git add -A` + `git commit -m "merken: <kurz was gelernt>"` + `git push origin <feature-branch>`.
2. **Auf `main` mergen (der eigentliche Weg zur nächsten Session):**
   ```bash
   git checkout main && git pull origin main
   git merge --no-ff <feature-branch> -m "merge: Vault → main"
   git push origin main
   git checkout <feature-branch>
   ```
   Kontrolle: `git log --oneline main | head -3` → neuester Commit = aktueller Vault-Stand. Details: [[Memory-Workflow]].
3. **Optional Drive:** nur wenn der Nutzer die Notiz ansehen will — geänderte Notes in den Drive-Vault (`Katastrophenprotokoll-Pipeline/YouTube-Knowledge`).
4. **SendUserFile:** für fertige Videos (z. B. TikTok-Upload durch den Nutzer).

## Schritt 3 — Kurz melden
Zwei bis drei Sätze: was gelernt wurde, wo es jetzt steht (Vault-Note + Commit).
Keine Aufzählung deiner Arbeitsschritte.
