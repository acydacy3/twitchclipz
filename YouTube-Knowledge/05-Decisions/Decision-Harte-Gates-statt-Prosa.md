---
type: decision
title: Decision-Harte-Gates-statt-Prosa
status: active
confidence: high
scope: gesamte Produktion (alle Serien, alle Pipelines)
created: 2026-09-07
tags: [decision, enforcement, gates, hooks, n+1, qualitaet]
---

# Entscheidung: Regeln werden erzwungen, nicht aufgeschrieben

## Der Anlass

Die Generalüberholung am 07.09.2026 suchte die Ursache dafür, dass das
selbstlernende n+1 nicht greift. Sie ist nicht Vergesslichkeit und nicht
fehlendes Wissen. **Das Wissen war vollständig da und richtig.** Es fehlte an
jeder Stelle, an der eine Regel hätte greifen müssen, ein Mechanismus, der sie
erzwingt.

Belege (Stand vor der Überholung):

| Regel | Wo sie stand | Was sie durchsetzte |
|---|---|---|
| Captions IMMER aus Skript | Pflichtliste §0d, CLAUDE.md, `/video` §4, Failure-Memory | nichts |
| Bewegtbild-Pflicht | Pflichtliste §5, Current-State, Blueprint | nichts |
| Contrarian vor Render/Upload | Pflichtliste §0 | nichts — `nb_contrarian.py` gibt Exit 0 und wird von keinem Skript aufgerufen |
| §0d Selbst-QC vor Upload | Pflichtliste §0d | nichts — eine Checkliste zum Abhaken |
| Analytics-Loop Tag 4–5 | Pflichtliste §1, Analytics-Loop | nichts — letzter Snapshot 29.08. |

**Null von fünf Regeln hatten einen Prüfpunkt im Code.** Alle fünf wurden
gebrochen, während sie galten.

## Die Entscheidung

Ab sofort gilt für jede Produktionsregel:

> **Eine Regel ohne ausführbaren Prüfpunkt ist keine Regel, sondern eine
> Absichtserklärung. Sie darf im Vault stehen, aber nicht als „erzwungen",
> „pipeline-weit" oder „blockierend" bezeichnet werden.**

Konkret:

1. **Vorher-Gate** — `tools/kp_gate.py <serie>` prüft vor jedem Render:
   Skript-Herkunft (sha256 gegen `QUELLE.json`), Caption-Wörter gegen das
   Skript, echte Bewegung im Short, Musikpegel. Exit 1 bei Verstoß.
2. **Nachher-Gate** — `tools/kp_gate.py <serie> --nachher` prüft das
   **fertige Video**: Länge gegen Voiceover, Untertitel-Abdeckung, und ob im
   Untertitel-Band überhaupt Schrift im Bild ist (Helligkeitsmessung,
   validiert: 159 ohne / 235 mit Untertitel, Schwelle 200).
3. **Riegel** — `.claude/hooks/pre-tool-use.py` läuft als `PreToolUse`-Hook
   vor jedem Bash-Aufruf. Erkennt er einen Render- oder Upload-Befehl, ruft er
   das Gate. Rot → Exit 2 → der Befehl läuft **nicht**.
4. **Herkunft** — `tools/kp_skript.py` nimmt das Nutzer-Skript auf und legt
   `QUELLE.json` mit Prüfsumme an. Ohne Nachweis blockiert das Gate.
5. **Austausch** — `tools/kp_ersetzen.py` tauscht terminierte Shorts aus.
   Reihenfolge fest: Nachher-Gate → hochladen → bestätigen → **erst dann**
   löschen. Öffentliche Videos werden nie angefasst.
6. **Regressionstest** — `tools/tests/test_pre_tool_use.py` prüft, dass der
   Riegel sperrt **und** durchlässt.

## Warum ein Hook und nicht Disziplin

Externe Forschung 2026 zum selben Problem (siehe unten) kommt zum selben
Schluss: *„The model should not be responsible for enforcing its own
constraints. That responsibility belongs to the surrounding system."* Ein
`PreToolUse`-Hook mit Exit-Code 2 verhindert den Werkzeugaufruf, bevor die
Rechte-Prüfung überhaupt greift — er ist nicht überredbar.

Dasselbe gilt für die Bewertung: ein LLM, das seine eigene Arbeit benotet, ist
kein Maßstab. Der Autonomie-Score stieg von 48 auf 88, während der gesehene
Anteil je Short von 76 % auf 54 % fiel. Deshalb ersetzt `tools/kp_metrik.py`
den Selbst-Score durch AVP% aus der YouTube-Analytics-API.

## Was NICHT entschieden wurde

- `nb_contrarian.py` wird **nicht gelöscht**. Sein wissenschaftlicher Teil
  (Hypothesen-Peer-Review, Confidence gegen Stichprobengröße) ist gut und
  einzigartig. Nur sein Produktions-Teil ist wirkungslos und wird durch
  `kp_gate.py` ersetzt. Vorschlag zur Trennung liegt vor, Entscheidung beim
  Nutzer (Guardrail #9).
- Die Serien-Ordner behalten ihre eigenen `nb_build.py`. Eine Vereinheitlichung
  wäre richtig, ist aber ein Eingriff in laufendes Material (Guardrail #1) und
  braucht eine eigene Entscheidung.

## Evidenz

- Commit `1587675` („pipeline-weit erzwungen") ändert nur zwei Markdown-Dateien.
- Commit `02da686` (der echte Fix) ändert nur `ralston/nb_build.py`.
- `tools/nb_contrarian.py` Zeile 96: `_check_words` = `cfg.get("words")`.
- `tools/nb_contrarian.py`: einziges `sys.exit(1)` liegt im JSON-Lesefehler.
- `prosperi/nb_transcribe.py`: schreibt ASR nach `skripte/short_XX.txt`.
- Gate-Nachweis am 07.09.: `prosperi` 29 Verstöße in 10 Shorts, `ralston`
  5 Standbild-Shorts — beide vorher unbemerkt.

## Externe Quellen (07.09.2026 geprüft)

- Wahi, V. (2026): *LLM-as-a-Judge Is Not an Oracle: Why Self-Improving Agents
  Need Deterministic Guardrails*, arXiv:2609.02246 — elf Wege, wie das
  Bewertungssignal versagt; Vorschlag PROCTOR mit deterministischen Riegeln,
  die der Bewerter nicht überstimmen kann.
- Claude Code Hooks Reference (code.claude.com/docs/en/hooks) — `PreToolUse`
  mit Exit-Code 2 verhindert den Werkzeugaufruf; wirkt auch unter
  `bypassPermissions`.
- Forschung zu Memory-Poisoning 2026 (arXiv:2606.04329 u. a.): Verteidigung
  an vier Punkten, darunter **write-time admission** und **provenance
  binding** — genau das leistet `QUELLE.json`.

## History

- **Version 1 (07.09.2026)** — angelegt nach der Generalüberholung.
  Auslöser: alle 10 Prosperi-Shorts mit falschen Captions live, 5 von 10
  terminierten Ralston-Shorts reine Standbild-Diashows, beides trotz
  geltender Regeln unbemerkt. Confidence: High (Belege sind Code und Commits,
  nicht Interpretation).

## Related
[[Failure-Memory]] · [[Guardrails]] · [[Produktion-Pflichtliste]] ·
[[Knowledge-Architecture]] · [[Autonomie-Log]] · [[Current-State]]
