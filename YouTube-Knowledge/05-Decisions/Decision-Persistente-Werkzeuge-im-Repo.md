---
type: decision
status: active
confidence: very high
created: 2026-08-24
updated: 2026-08-24
tags: [decision, werkzeuge, skripte]
---

# Decision: Wiederverwendbare Skripte bleiben im Repo — nie neu schreiben

## Entscheidung (19.08.2026)
Jedes wiederverwendbare Skript kommt sofort ins Repo und wird in Folge-Sessions
**benutzt oder verbessert**, nie neu geschrieben.

## Warum / Evidence
Der Container ist Wegwerfware. Am 19.08. mussten vier Skripte
(`transcribe_all.py`, `build_configs.py`, `youtube_upload.py`, `upload_all.py`)
neu gebaut werden, weil sie nur in ausgelaufenen Containern lagen → 15+ min
Blindflug, zu Recht verärgerter Nutzer. Gleicher Fehler wie beim San-José-Verlust
([[Failure-Verlorene-Videos-nicht-gesichert]]), nur für Code.

## Status (Tiefen-Audit 19.08.)
Die vier Skripte liegen im **Repo-ROOT**, nicht unter `werkzeuge/` (per curl gegen
raw.githubusercontent.com verifiziert; `werkzeuge/` existiert remote nicht).
**Regel für Folge-Sessions:** erst `ls`/`grep` im Repo-Root, dann ggf. bauen.
Da `git push` jetzt frei ist ([[Decision-Git-vs-Drive-Persistenz]]), kann eine
spätere Session sie sauberer nach `werkzeuge/` konsolidieren.

## Related
[[Agent-Architecture]] · [[Failure-Verlorene-Videos-nicht-gesichert]]
