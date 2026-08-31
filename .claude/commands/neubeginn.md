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
`CLAUDE.md` ist geladen (Einstieg). Das Detailwissen liegt im **Vault**
`YouTube-Knowledge/`. Öffne gezielt:
- `YouTube-Knowledge/HOME.md` (Karte) und `00-System/Current-State.md` (Stand).
- Für die anstehende Aufgabe **gezielt retrieven** (nicht das ganze Vault): passende
  `01-Learnings/…`, `09-Failures/Failure-Memory.md`, `05-Decisions/…`. Confidence + Scope + Counter-Evidence beachten.
Besonders: Originalskript kommt **immer** vom Nutzer; er nutzt **keine** Kommandozeile und öffnet **keine** `.md` (er liest sie in seinem Markdown-Viewer).

## Schritt 3 — Echten Kanalstand holen
`python3 analyse.py` ausführen (Abos, Aufrufe, Videos, Termine, Sprache).
- Scheitert es an Zugangsdaten: in zwei Sätzen sagen, was einzutragen ist, weiter mit Schritt 4.
- Läuft es: **gemessene Zahlen gewinnen** gegen alles Notierte → `Current-State.md` aktualisieren.

## Schritt 4 — Repo-Stand prüfen (main ist die Wahrheit)
Neue Container klonen `main`. Prüfe den Stand:
```bash
git fetch origin main
git log --oneline main..HEAD   # Commits die noch NICHT auf main sind
```
- Commits auf main fehlen lokal → `git pull origin main` (frischer Container).
- Commits NUR auf Feature-Branch → Vault veraltet gegenüber deiner Arbeit → am Session-Ende ZWINGEND auf main mergen (`/merken` Schritt 2).
Drive ist optional (Nutzer-Ansicht). Bei Widerspruch gilt Vault/CLAUDE.md.

## Schritt 5 — Melden
Höchstens 15 Zeilen, einfache Sprache: **Kanalstand · was zuletzt lief · was ansteht ·
was blockiert** (nur wenn wirklich). Keine Häkchen-Tabelle, keine Arbeitsschritte.
Mehr als drei Dinge → Artifact-Seite, im Chat nur die drei wichtigsten Sätze.
