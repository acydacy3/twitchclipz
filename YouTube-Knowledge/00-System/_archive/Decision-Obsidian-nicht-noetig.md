---
type: decision
status: active
date: 2026-08-25
tags: [decision, obsidian, werkzeuge, konstrukt]
---

# Entscheidung: Obsidian-Anbindung bringt Claude nichts — nicht einführen

## Test (25.08.2026)
- **Kein Obsidian-Connector/MCP vorhanden:** `ToolSearch` (obsidian/vault/notes) + `ListConnectors` (obsidian, notes, vault, markdown) → **leer**. Die vermutete „Obsidian-Anbindung" existiert als Tool nicht.
- Der Vault ist ein **Obsidian-*kompatibler* Markdown-Ordner** im Repo — aber es gibt keine Live-Obsidian-Schnittstelle.

## Abwägung (aus Claude-Nutzungssicht)
- Was ein Obsidian-MCP böte (Notiz suchen, lesen, Backlinks, Graph) **mache ich bereits besser direkt über das Dateisystem:** `Read/Write/Edit` (präzises Bearbeiten), `Grep/Glob` (Volltext/Namen), und ein Mini-Skript für `[[Link]]`/Backlink-Traversierung (Link-Integritäts-Audit lief so: 71 Notizen, 0 tote Links).
- Direktzugriff ist **schneller, ohne API-Limits, git-integriert, offline** und erlaubt exaktes Editieren. Ein MCP wäre nur Indirektion/Latenz.
- Obsidians eigentlicher Mehrwert ist die **visuelle Graph-/UI-Ansicht** — die der **Nutzer ausdrücklich nicht braucht**.

## Ergebnis
- **Obsidian NICHT einführen.** Vault als reines Markdown belassen (bleibt für den Nutzer jederzeit in Obsidian öffnbar, ist aber keine Abhängigkeit).
- Retrieval/Persistenz/n+1 laufen vollständig auf den Rohdateien — kein Bedarf, das Thema erneut zu prüfen.

## Related
[[Current-State]] · [[Memory-Workflow]] · [[Knowledge-Architecture]]
