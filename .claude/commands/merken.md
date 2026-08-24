---
description: Persistiert neue Erkenntnisse ins Obsidian-Vault + Git (Drive nur Fallback)
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
1. Lokal sichern: `git add -A` + `git commit -m "merken: <kurz was gelernt>"`.
2. `git push` **versuchen** — funktioniert er (kein 403), ist das Repo aktuell und du bist fertig.
3. **Solange Push 403 gibt (aktueller Stand):** das Vault als **Zip** bauen und mit `SendUserFile` an den Nutzer schicken, plus nach Google Drive
   (`Katastrophenprotokoll-Pipeline`, `1MFz5gNIBQfcXWBw8evnop_oUJ-9TnWtX`) sichern
   (search_files nach Namen → create_file → trash_file alte ID). **Einen** Satz in
   einfacher Sprache: ohne diese Datei gehen die Erkenntnisse verloren.

> **Sonderfall Drive-Vault:** Liegt das Obsidian-Vault des Nutzers in seinem
> Google-Drive-Ordner, schreib die geänderten Notes direkt dorthin — dann erscheinen
> sie automatisch in seinem Obsidian, ohne Datei-Handoff.

## Schritt 4 — Kurz melden
Zwei bis drei Sätze: was gelernt wurde, wo es jetzt steht (Vault-Note + Commit).
Keine Aufzählung deiner Arbeitsschritte.
