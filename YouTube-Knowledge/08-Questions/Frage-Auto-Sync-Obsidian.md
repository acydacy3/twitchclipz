---
type: question
status: open
created: 2026-08-24
updated: 2026-08-24
tags: [question, obsidian, drive, sync]
---

# Frage: Auto-Sync zwischen Claude und Obsidian herstellen?

## Problem
Der Nutzer hat das Vault aus der **Zip** in einen **lokalen** Ordner (`zippo`)
entpackt und in Obsidian geöffnet. Ich schreibe/pflege das Vault aber in **Google
Drive**. Da der Nutzer Drive **nur im Browser** nutzt (kein „Drive für Desktop"),
sind lokale Kopie und Drive-Kopie **getrennt** → Drift-Gefahr.

## Lösungsoptionen
1. **„Google Drive für Desktop" installieren** (empfohlen): Vault in den Drive-Ordner
   legen → beidseitig automatisch. Einmaliger Setup, danach echtes Auto-Sync.
2. **Claude lokal ausführen:** greift direkt auf `Desktop/zippo` zu (braucht Terminal).
3. **Manuell:** Claude gibt Dateien via `SendUserFile`, Nutzer legt sie ins Vault. Kein Drift-Schutz.

## Status
**Offen — Nutzer-Entscheidung.** Bis dahin: manueller Weg (Option 3).

## Related
[[Decision-Umgebung-und-Obsidian-Bruecke]] · [[Memory-Workflow]]
