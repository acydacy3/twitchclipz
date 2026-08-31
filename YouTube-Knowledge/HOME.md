---
type: moc
title: YouTube-Knowledge — Startseite
updated: 2026-08-24
tags: [moc, home]
---

# 🏠 YouTube-Knowledge — Langzeitgedächtnis des Kanals

> **⏱️ NEU HIER? 60-Sekunden-Einstieg:**
> 1. [[Current-State]] — aktueller Kanalstand, was zuletzt lief, was ansteht.
> 2. [[Produktion-Pflichtliste]] — **DER kanonische Produktionsprozess** (Gates §0a–§0d + Ablauf §1–§7).
> 3. Für die Aufgabe gezielt retrieven: `01-Learnings/` · [[Failure-Memory]] · `05-Decisions/`.
> Persistenz: alles am Session-Ende auf `main` mergen ([[Memory-Workflow]]).

> Dies ist das **persistente Gedächtnis** des Kanals *Katastrophenprotokoll*.
> Es überlebt jede Claude-Session. Vor jeder wichtigen Entscheidung wird hier **zuerst gesucht** (Retrieval before Reinvention).
> Reiner Markdown-Ordner — navigiert über `[[Wikilinks]]` und `Grep`/`Read`.

## Wie dieses Gedächtnis funktioniert (in 4 Sätzen)
1. **Nicht jede Erfahrung ist ein Learning.** Wir trennen Observation → Hypothese → Experiment → Result → Learning → Rule. Siehe [[Knowledge-Architecture]].
2. **Jedes Learning trägt eine Confidence** (Low/Medium/High/Very High) und einen **Scope** (wofür es gilt).
3. **Widersprüche werden bewahrt, nicht überschrieben** — die Historie zeigt, warum wir heute anders denken als früher.
4. **CLAUDE.md ist nur der Einstieg**, das Detailwissen lebt hier im Vault.

---

## 🗺️ Karte des Wissens

### 00 · System (fang hier an)
- [[Mission]] — warum es diesen Kanal und dieses Gedächtnis gibt
- [[Knowledge-Architecture]] — das epistemische Modell (Confidence, Widersprüche, Retrieval, Memory-Promotion)
- [[Current-State]] — aktueller Kanal- und Produktionsstand
- [[Agent-Architecture]] — Pipeline, Zwei-Agenten-Methode, wo die 5 Lernsysteme sitzen
- [[Guardrails]] — die verbindlichen Implementierungs-Leitplanken
- [[Memory-Workflow]] — Session-Start → arbeiten → Learning → zurückschreiben

### 01 · Learnings (was wir gelernt haben — mit Confidence)
- [[Learning-Hooks]] · [[Learning-Retention-und-Laenge]] · [[Learning-Storytelling-Shorts]]
- [[Learning-Editing-Video]] · [[Learning-Editing-Ton]] · [[Learning-Captions]]
- [[Learning-Titel]] · [[Learning-Thumbnails-Cover]] · [[Learning-Bilder-Prompts]]
- [[Learning-Topics-Themenwahl]] · [[Learning-SEO]] · [[Learning-Cross-Platform-TikTok]]

### 02 · Experimente
- [[_Experiment-Template]] — Vorlage
- [[Experiment-Manager]] — wie wir entscheiden, was als Nächstes zu testen ist
- Aktiv: `02-Experiments/Active/` · Abgeschlossen: `02-Experiments/Completed/`

### 03 · Video-Gedächtnis
- [[Video-01-Tham-Luang]] · [[Video-02-San-Jose]] · [[Video-03-Koepcke]]

### 04–09 · Wissen im weiteren Sinn
- [[Competitors-Übersicht]] (04) — Konkurrenzbeobachtung
- [[Decisions-Übersicht]] (05) — Entscheidungen **mit Begründung**
- [[Audit-System]] (06) — Daily/Weekly/Monthly-Selbstprüfung
- [[Hypotheses-Übersicht]] (07) — offene Hypothesen
- [[Questions-Übersicht]] (08) — offene Fragen
- [[Failure-Memory]] (09) — gescheiterte Ansätze, damit sie sich nicht wiederholen

---

## 🧭 Die fünf Lernsysteme (Advanced Layer)
Umgesetzt als Workflows + Struktur in diesem Vault — **kein eigener Agent nötig,
Stand jetzt.** Ein Agent ist erlaubt, sobald der [[Guardrails]]-#8-Test ihn
rechtfertigt (bislang tut das keiner). Siehe [[Agent-Architecture]]:

| System | Wo es lebt |
|---|---|
| Experiment Manager | [[Experiment-Manager]] + `02-Experiments/` |
| Evidence & Confidence | [[Knowledge-Architecture]] — gilt für **jede** Learning-Note |
| Failure Memory | [[Failure-Memory]] (09) |
| Contrarian / Red-Team | [[Contrarian-Layer]] + Abschnitt in [[Audit-System]] |
| Strategy Evolution & Audit | [[Strategy-Evolution]] + [[Audit-System]] |

---

## ⚠️ Nie vergessen (Kern-Constraints des Nutzers)
- **Das Originalskript kommt IMMER vom Nutzer.** Kürzen/formen: ja. Erfinden: nein.
- **Der Nutzer arbeitet nicht mit der Kommandozeile** und kann **keine `.md`-Dateien öffnen** → längere Ergebnisse als **Artifact-Seite**, nicht als Textdatei.
- **Zahlen schlagen Vermutungen, immer.**
