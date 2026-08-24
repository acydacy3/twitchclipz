# Katastrophenprotokoll — Operating Context

Diese Datei lädt automatisch zu Sitzungsbeginn. Sie ist der **Einstieg**, kein
Archiv. Das eigentliche Langzeitgedächtnis liegt im **Obsidian-Vault**
`YouTube-Knowledge/` — dort steht das Detailwissen mit Evidenz, Confidence und
Historie. **Öffne `YouTube-Knowledge/` als Vault in Obsidian**, um Links/Graph zu nutzen.

> Migration 24.08.2026: Das frühere große `CLAUDE.md` (1292 Zeilen) wurde nach
> `YouTube-Knowledge/` überführt und liegt **verbatim** unter
> `YouTube-Knowledge/00-System/_archive/`. Nichts ging verloren.

---

## Sofort wissen (die 6 wichtigsten Constraints)
1. **Das Originalskript kommt IMMER vom Nutzer.** Kürzen/formen aus vorhandenem Material: ja. Erfinden: nein.
2. **Der Nutzer arbeitet nicht mit der Kommandozeile** und kann **keine `.md`-Dateien öffnen** → längere Ergebnisse als **Artifact-Seite** ausliefern. (Ausnahme: das Vault liest er in Obsidian.)
3. **Zahlen schlagen Vermutungen, immer.** `analyse.py` gewinnt gegen Notiertes.
4. **Retrieval before Reinvention:** vor wichtigen Entscheidungen zuerst im Vault suchen (bereits Getestetes nicht wiederholen).
5. **Ein Learning ist nicht automatisch eine Rule.** Unsicherheit sichtbar lassen (Confidence Low/Medium/High/Very High).
6. **Erkenntnisse persistieren:** `git push` ist weiterhin **403-gesperrt** → lokal committen, dann **nach Google Drive sichern + Vault als Datei an den Nutzer** (`/merken`). Push nutzen, sobald freigeschaltet. Details: `YouTube-Knowledge/05-Decisions/Decision-Git-vs-Drive-Persistenz.md`.

## So arbeitet dieses System (Kurzfassung)
- **Ziel ist bessere Entscheidungsqualität je Produktionszyklus**, nicht mehr Output → `YouTube-Knowledge/00-System/Mission.md`.
- **Epistemik:** Observation → Hypothesis → Experiment → Result → Learning → Rule; Widersprüche werden bewahrt, nicht überschrieben → `.../Knowledge-Architecture.md`.
- **Leitplanken (Vorrang):** `.../Guardrails.md` — u. a. #1 Bestehendes schützen, #8 minimale Komplexität (neue Agenten nur, wenn der #8-Test sie rechtfertigt), #9 bei irreversiblen Änderungen erst analysieren + vorschlagen.

## Einstiegspunkte im Vault
- **Start / Karte:** `YouTube-Knowledge/HOME.md`
- **Aktueller Stand:** `YouTube-Knowledge/00-System/Current-State.md`
- **Was tun bei Session-Start / -Ende:** `YouTube-Knowledge/00-System/Memory-Workflow.md`
- **Vor jedem Schnitt:** `YouTube-Knowledge/00-System/Schnitt-Protokoll.md`
- **Learnings** (Hooks, Retention/Länge, Captions, Titel, SEO, Bilder, TikTok …): `YouTube-Knowledge/01-Learnings/`
- **Gescheiterte Ansätze** (nicht wiederholen): `YouTube-Knowledge/09-Failures/Failure-Memory.md`

## Kanal in einem Satz
Deutscher Faceless-Kanal *Katastrophenprotokoll* (`UC1KCzLNlgGiYsLNQ7Z0HA-g`),
Nische Katastrophen nüchtern erklärt, Vorbild *Fascinating Horror*. Takt: alle 48 h
ein Langvideo (~5 min) + täglich 2–5 Shorts; **die Shorts tragen**.

## Pipeline (Skripte im Repo-Root)
`transcribe_all.py`/`transcribe_vosk.py` → `align.py` → `pauses.py` → `bildcheck.py`
→ `karaoke.py` → `musik.py` → `short.py` → `serie.py` → `lang.py` → `videocheck.py`;
dazu `build_configs.py`, `youtube_upload.py`, `upload_all.py`, `analyse.py`.
Details + Werkzeug-Regel: `YouTube-Knowledge/00-System/Agent-Architecture.md`.

## Am Ende jeder Sitzung
Neue Erkenntnisse in die passende Vault-Note (mit Confidence + Scope + Historie),
dann `git add/commit/push`. Ablauf: `YouTube-Knowledge/00-System/Memory-Workflow.md`
(bzw. `/merken`). Prüfen, ob daraus eine Rule wird → dann `Current-State.md`/diese Datei anpassen.
