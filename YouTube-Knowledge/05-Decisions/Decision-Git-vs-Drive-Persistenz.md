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

**Prüfung 24.08.2026:** `git commit` geht lokal, aber `git push` scheitert weiter
mit **403** (`Claude doesn't have GitHub access … / Resource not accessible`).
**UPDATE 25.08.: `git push` ist FREIGESCHALTET** — die 403-Sperre ist aufgehoben; **Git ist wieder primärer Persistenz-Weg**, Drive optional. Der folgende Text dokumentiert die frühere (aufgehobene) Sperre.

~~Die Push-Sperre besteht also **fort** — die frühere Annahme „Push frei" war falsch~~
und ist hiermit korrigiert. Persistenz läuft daher weiter über Drive + Datei-Handoff.

## Entscheidung (Stand 24.08., korrigiert)
1. **Primär (sobald Push freigeschaltet ist):** Vault + CLAUDE.md per
   `git commit` + `git push` (versioniert, Historie → [[Knowledge-Architecture]] §3).
   **Seit 25.08. verfügbar — Git ist der Weg.**
2. **Aktuell aktiv:** `commit` lokal + **nach Google Drive sichern** (`/merken`) +
   **`SendUserFile`** an den Nutzer (Zip des Vaults). So wie schon die Ur-CLAUDE.md
   es beschrieb — die Push-Sperre ist real.
3. **Voraussetzung für den Wunsch „Claude nutzt Obsidian selbst":** ein gemeinsam
   erreichbarer Ort — entweder das Vault im Google-Drive-Ordner (dieser Server
   schreibt hinein) **oder** Claude läuft lokal auf dem PC (Desktop/zippo direkt).

## Warum
- Guardrail #2 (Memory Must Be Persistent) ist mit Git **sauberer** erfüllt als mit manuellem Drive-Upload.
- Git bewahrt Historie automatisch (Guardrail #6/#17) — Drive überschreibt.
- Weniger Handarbeit für den Nutzer (er muss nichts mehr hochladen).

## Offen / zu prüfen bei nächster Session
- Gilt die Push-Freigabe **nur in dieser (Web-/Branch-)Umgebung** oder generell?
  (Historisch — nur falls je wieder 403: Drive-Fallback. Stand 25.08.: Push frei.)
- `/merken` + `/neubeginn` wurden entsprechend aktualisiert (git zuerst, Drive Fallback).

## Related
[[Memory-Workflow]] · [[Guardrails]] · [[Knowledge-Architecture]]
