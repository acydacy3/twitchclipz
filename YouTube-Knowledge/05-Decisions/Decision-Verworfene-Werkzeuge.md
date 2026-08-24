---
type: decision
status: active
confidence: high
created: 2026-08-24
updated: 2026-08-24
tags: [decision, werkzeuge, verworfen]
---

# Decision: Bewusst NICHT eingesetzte Werkzeuge

Damit sie nicht in drei Wochen erneut evaluiert werden. Siehe auch [[Failure-Memory]].

- **`ruvnet/ruflo`** (Agent-Meta-Harness) — verworfen 19.08.: `npx ruflo init` überschreibt unsere CLAUDE.md + 27 Hooks + 12 Auto-Worker (verbrennt Limits); Kernnutzen (Vektor-Gedächtnis) braucht persistenten Workspace, den wir mit Vault + Git schon lösen; Enterprise-Schwarm = Overkill für 1-Personen-Pipeline. Falls je testen: nur in leerem Wegwerf-Ordner.
- **omniroute** (LLM-Router) — getestet 17.08., kein Gewinn: drei Bugs umgangen (SQLite fehlt → `omniroute repair`; Fehlalarm 129 Migrationen → `OMNIROUTE_MAX_PENDING_MIGRATIONS=0`; Katalog nennt `google`, Code will `gemini`), aber direkter API-Aufruf war in jedem Fall einfacher. Installationszeile aus Setup entfernt.
- **`thedotmack/claude-mem`** — Sitzungsgedächtnis-Plugin; müsste jede Session neu installiert werden. Vault + Git leisten dasselbe zu Kosten null.
- **`AgriciDaniel/claude-seo`** — reines Website-SEO, für einen Kanal ohne Website nutzlos (nur die YouTube-Data-API-Referenz war brauchbar).
- **Gemini-Bildgenerierung (Gratis-Key)** — festes Kontingent **0**, kein Cooldown; braucht Cloud-Projekt mit Abrechnung. → Higgsfield bleibt.
- **Instagram/TikTok-Direkt-Uploader** (Browser-Automatisierung) — brechen bei Layout-Änderung, gefährden Konto. TikTok über Buffer stattdessen.

## Related
[[Failure-Memory]] · [[Decision-Git-vs-Drive-Persistenz]]
