---
description: Persistiert neue Erkenntnisse ins Obsidian-Vault + Git (Drive nur Fallback)
---

# Merken

Der Nutzer hat „merken" geschrieben, **oder** eine Arbeitssitzung geht zu Ende,
**oder** ein Meilenstein ist erreicht. Dann läuft dieser Ablauf — auch ungefragt.

Zweck des Projekts (Nutzer-Worte): *„Learning gemerkt, Fehler gemerkt, verbessert,
immer aktueller Stand ohne Befehl."* Dieser Befehl ist die Hälfte davon, die nicht
von allein läuft.

> **Neu seit 24.08.2026:** `git push` ist in dieser Umgebung frei. Das Repo kann
> sich also **selbst** fortschreiben — der frühere Google-Drive-Umweg ist nur noch
> **Fallback**. Siehe `YouTube-Knowledge/05-Decisions/Decision-Git-vs-Drive-Persistenz.md`.

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

## Schritt 2 — Persistieren (Git zuerst)
```
git add -A
git commit -m "merken: <kurz was gelernt>"
git push -u origin <aktueller-branch>
```
Bei Netzfehler bis zu 4× mit Backoff (2s/4s/8s/16s) wiederholen.

## Schritt 3 — Fallback, falls Push scheitert (403 o. ä.)
Nur dann den alten Weg gehen: `CLAUDE.md` **und** die geänderten Vault-Dateien
nach Google Drive (`Katastrophenprotokoll-Pipeline`, `1MFz5gNIBQfcXWBw8evnop_oUJ-9TnWtX`)
sichern (search_files nach Namen → create_file → trash_file alte ID) und die
Dateien mit `SendUserFile` an den Nutzer schicken, mit **einem** Satz in einfacher
Sprache. Deutlich sagen: geht die Sicherung nur über ihn, gehen die Erkenntnisse
sonst verloren.

## Schritt 4 — Kurz melden
Zwei bis drei Sätze: was gelernt wurde, wo es jetzt steht (Vault-Note + Commit).
Keine Aufzählung deiner Arbeitsschritte.
