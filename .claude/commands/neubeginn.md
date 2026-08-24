---
description: Bringt die Sitzung ohne Rückfragen auf den vollständigen Projektstand
---

# Neubeginn

Der Nutzer hat „neubeginn" geschrieben: **eine neue Sitzung hat begonnen, bring
dich selbst auf den aktuellsten Stand — ohne dass er etwas erklären muss.**
Arbeite die Schritte der Reihe nach ab, frag nichts zwischendurch, melde dich erst am Ende.

## Schritt 1 — Fundament prüfen
Der Sitzungsstart-Hook hat einen Statusbericht ausgegeben. Lies ihn.
- **Pipeline unvollständig?** Repo nicht richtig angehängt → sag das in einem Satz, hör auf.
- **Werkzeuge fehlen?** Selbst nachinstallieren (ffmpeg, imagemagick, vosk, pillow, numpy, google-api-python-client). Nur bei Scheitern erwähnen.
- **Kein Statusbericht?** `bash .claude/hooks/session-start.sh` von Hand ausführen.

## Schritt 2 — Das Gedächtnis lesen (Vault)
`CLAUDE.md` ist geladen (Einstieg). Das Detailwissen liegt im **Obsidian-Vault**
`YouTube-Knowledge/`. Öffne gezielt:
- `YouTube-Knowledge/HOME.md` (Karte) und `00-System/Current-State.md` (Stand).
- Für die anstehende Aufgabe **gezielt retrieven** (nicht das ganze Vault): passende
  `01-Learnings/…`, `09-Failures/Failure-Memory.md`, `05-Decisions/…`. Confidence + Scope + Counter-Evidence beachten.
Besonders: Originalskript kommt **immer** vom Nutzer; er nutzt **keine** Kommandozeile und öffnet **keine** `.md` (Ausnahme Obsidian).

## Schritt 3 — Echten Kanalstand holen
`python3 analyse.py` ausführen (Abos, Aufrufe, Videos, Termine, Sprache).
- Scheitert es an Zugangsdaten: in zwei Sätzen sagen, was einzutragen ist, weiter mit Schritt 4.
- Läuft es: **gemessene Zahlen gewinnen** gegen alles Notierte → `Current-State.md` aktualisieren.

## Schritt 4 — Nachziehen (Drive/Datei, da git push 403)
`git push` ist aktuell gesperrt → die lebende Fassung kommt per **Drive/Datei-Handoff**
der Vorsitzung, nicht zwingend über das Repo. `git pull` auf den aktuellen Branch
holt, was gepusht wurde (falls Push zwischenzeitlich freigeschaltet ist). Im Drive-Ordner
`Katastrophenprotokoll-Pipeline` nach neueren `CLAUDE.md`/Vault-Dateien sehen
(über Namen suchen). Neuer/größer → übernehmen und dem Nutzer in einem Satz sagen.
Ältere Drive-Dateien (`REGELN.md`, `START-HIER.md`, `LEARNINGS-*.md` vom 15./16.08.)
sind **Altlast** — bei Widerspruch gilt Vault/CLAUDE.md.

## Schritt 5 — Melden
Höchstens 15 Zeilen, einfache Sprache: **Kanalstand · was zuletzt lief · was ansteht ·
was blockiert** (nur wenn wirklich). Keine Häkchen-Tabelle, keine Arbeitsschritte.
Mehr als drei Dinge → Artifact-Seite, im Chat nur die drei wichtigsten Sätze.
