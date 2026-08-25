---
type: system
title: Agent-Architecture
updated: 2026-08-24
tags: [system, architecture, pipeline]
---

# Agent-Architecture

Verwandt: [[Mission]], [[Guardrails]], [[Memory-Workflow]].

## Grundhaltung (Guardrail #8)
**Wenige starke Komponenten + klare Skills + starkes Memory** — nicht viele
kleine, überlappende Agenten. Vor jedem neuen Agent/Skill/Service: erst prüfen,
ob eine bestehende Funktion das kann.

## Produktions-Pipeline (Skripte im Repo-Root)
| Schritt | Datei | Aufgabe |
|---|---|---|
| 1 | `transcribe_vosk.py` / `transcribe_all.py` | Voiceover → Wortzeiten (Whisper Standard, Vosk Fallback) |
| 2 | `align.py` | korrigierten Skripttext auf Zeiten mappen |
| 3 | `pauses.py` | Sprechpausen → Schnittgrenzen (≥ 0,42 s) |
| 4 | `bildcheck.py` | Bilder prüfen, **bevor** produziert wird |
| 5 | `karaoke.py` | ASS-Untertitel mit Wort-Hervorhebung (flache Wort-Liste!) |
| 6 | `musik.py` | Musikbett (synthetisch, lizenzfrei) |
| 7 | `short.py` | einen Short bauen (9:16) |
| 8 | `serie.py` | alle Shorts als Stapel |
| 9 | `lang.py` | Langvideo (16:9) |
| 10 | `videocheck.py` | Ton/Bild/Untertitel prüfen **vor** Upload |
| + | `build_configs.py`, `youtube_upload.py`, `upload_all.py`, `analyse.py` | Metadaten, Upload/Terminierung, Kanalstand |

**Regel:** Wiederverwendbare Skripte bleiben im Repo, werden nie neu geschrieben,
sondern benutzt/verbessert. Details: [[Decision-Persistente-Werkzeuge-im-Repo]].

## Bewährte Arbeitsmethode: Zwei-Agenten-Verfahren
Zweimal erfolgreich: **zwei Agenten unabhängig dieselbe Aufgabe** — einer mit
Playbook, einer ausdrücklich ohne — dann eine Runde Gegenrede, dann zusammenführen.
Beide räumten in Runde zwei eigene Fehler ein, die im ersten Durchlauf niemand sah.
**Lehre:** Agenten liefern Struktur + Argumente, **Zahlen liefern die Entscheidung.**
Dies ist zugleich die native Umsetzung des [[Contrarian-Layer]].

## Wo die fünf Lernsysteme sitzen (aktuell kein eigener Agent nötig)
Ein eigener Agent ist **erlaubt**, sobald der [[Guardrails]]-#8-Test ihn
rechtfertigt (nötig? nicht schon vorhanden? echter Lern-/Produktionsgewinn?
vertretbare Wartung?). Bislang klärt keines der fünf Systeme diese Hürde —
deshalb Workflows + Struktur, nicht fünf kleine Agenten.

| System | Umsetzung | Ort |
|---|---|---|
| Experiment Manager | Workflow + Vorlage + Ordner | [[Experiment-Manager]], `02-Experiments/` |
| Evidence & Confidence | Frontmatter-Feld + Regeln, gilt für jede Note | [[Evidence-Confidence]], [[Knowledge-Architecture]] |
| Failure Memory | Note-Sammlung mit „Do not repeat unless…" | [[Failure-Memory]], `09-Failures/` |
| Contrarian / Red-Team | Zwei-Agenten-Methode + Audit-Checkliste | [[Contrarian-Layer]] |
| Strategy Evolution & Audit | Versions-Log der Strategie + Audit-Zyklen | [[Strategy-Evolution]], [[Audit-System]] |

## Integrierter Lernkreislauf
```
        OBSERVATION → EXPERIMENT → DATA → ANALYSIS
                                    ↙        ↘
                              EVIDENCE     CONTRARIAN
                                    ↘        ↙
                                    LEARNING → CONFIDENCE → DECISION
                                    → STRATEGY UPDATE → PIPELINE UPDATE → NEXT EXPERIMENT
```
[[Failure-Memory]] läuft quer durch den gesamten Kreislauf.

## Claude-Werkzeuge zum Arbeiten mit dem Vault
- **Lesen/Suchen:** Read, Grep, Glob über `YouTube-Knowledge/`.
- **Schreiben:** Write/Edit für neue/aktualisierte Notes.
- **Persistieren:** `git commit` + `git push` (freigeschaltet) — Repo trägt alles; Drive optional. Ablauf: [[Memory-Workflow]].
