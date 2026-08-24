---
type: decision
status: active
confidence: high
created: 2026-08-24
updated: 2026-08-24
tags: [decision, persistenz, git, drive, memory]
---

# Decision: Git-Vault als primäre Persistenz (Drive als Fallback)

## Kontext / Widerspruch
Die Ur-CLAUDE.md und die Commands `/merken` + `/neubeginn` bauen darauf, dass
**`git push` gesperrt (403)** ist — deshalb wurde das lebende Gedächtnis nach
**Google Drive** gesichert und der Nutzer musste die Datei manuell ins Repo laden.

**Neue Evidenz (24.08.2026):** In der aktuellen Umgebung ist `git push`
**freigeschaltet** (Branch-Workflow der Aufgabe). Damit ist die Grundannahme
des Drive-Umwegs überholt.

## Entscheidung
1. **Primär:** dieses Vault + CLAUDE.md werden per `git commit` + `git push`
   persistiert (versioniert, mit Historie → passt zu [[Knowledge-Architecture]] §3).
2. **Fallback:** Wenn Push scheitert (403/Netz), weiter nach Drive sichern
   (`/merken`) und Datei an den Nutzer schicken.
3. **Fallback 2:** `SendUserFile`.

## Warum
- Guardrail #2 (Memory Must Be Persistent) ist mit Git **sauberer** erfüllt als mit manuellem Drive-Upload.
- Git bewahrt Historie automatisch (Guardrail #6/#17) — Drive überschreibt.
- Weniger Handarbeit für den Nutzer (er muss nichts mehr hochladen).

## Offen / zu prüfen bei nächster Session
- Gilt die Push-Freigabe **nur in dieser (Web-/Branch-)Umgebung** oder generell?
  Falls eine reguläre Session wieder 403 sieht → Fallback greift automatisch.
- `/merken` + `/neubeginn` wurden entsprechend aktualisiert (git zuerst, Drive Fallback).

## Related
[[Memory-Workflow]] · [[Guardrails]] · [[Knowledge-Architecture]]
