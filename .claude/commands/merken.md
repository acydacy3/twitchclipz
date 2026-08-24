---
description: Persistiert neue Erkenntnisse → Drive-Vault (primär, da Push 403) + Git-Commit lokal
---

# Merken

Der Nutzer hat „merken" geschrieben, **oder** eine Arbeitssitzung geht zu Ende,
**oder** ein Meilenstein ist erreicht. Dann läuft dieser Ablauf — auch ungefragt.

Zweck des Projekts (Nutzer-Worte): *„Learning gemerkt, Fehler gemerkt, verbessert,
immer aktueller Stand ohne Befehl."* Dieser Befehl ist die Hälfte davon, die nicht
von allein läuft.

> **Stand 24.08.2026 (geprüft):** `git push` ist **weiter 403-gesperrt**. Lokal
> `commit` geht, aber die Sicherung läuft über **Google Drive + Datei-Handoff**
> (Zip des Vaults an den Nutzer). Siehe
> `YouTube-Knowledge/05-Decisions/Decision-Git-vs-Drive-Persistenz.md`.

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

## Schritt 2 — Persistieren
1. **Drive zuerst (der Weg, der die nächste Session erreicht):** die **geänderten**
   Notes direkt in den Drive-Vault schreiben — **ein** Vault unter
   `Katastrophenprotokoll-Pipeline/YouTube-Knowledge`
   (search_files nach Dateiname → bei Treffer `update_file`-Inhalt bzw. alte trashen +
   `create_file` neu; nur die geänderten, nicht alles). Das ist mein Gehirn für n+1.
2. Lokal sichern: `git add -A` + `git commit -m "merken: <kurz was gelernt>"` (Versionshistorie).
3. `git push` **versuchen** — klappt er (kein 403), ist das Repo wieder primär, fertig.
   **Solange 403:** kein Zip-Zwang; Drive (Schritt 1) trägt. Nur wenn der Nutzer es
   ausdrücklich will, zusätzlich `SendUserFile`.

> **Obsidian ist optional:** Liegt das Vault des Nutzers in seinem Drive-Ordner,
> erscheinen die Drive-Schreibvorgänge automatisch dort. Falls nicht, ist das kein
> Blocker — Drive bleibt trotzdem der Persistenz-Träger für die nächste Session.

## Schritt 4 — Kurz melden
Zwei bis drei Sätze: was gelernt wurde, wo es jetzt steht (Vault-Note + Commit).
Keine Aufzählung deiner Arbeitsschritte.
