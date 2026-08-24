---
type: decision
status: active
confidence: high
created: 2026-08-24
updated: 2026-08-24
tags: [decision, transkription, whisper, vosk]
---

# Decision: Whisper ist Standard, Vosk nur Offline-Fallback

## Entscheidung (19.08.2026)
`faster-whisper small-de int8` ist Standard-Transkription; Vosk
(`vosk-model-small-de-0.15`) nur noch Offline-/Notfall-Fallback.

## Warum / Evidence
- An Video 3 (Koepcke): alle 10 Voiceover in ~2 min auf CPU mit Wort-Zeiten; deutsche Fremdwörter/Namen (Koepcke, LANSA, Yacumama) **korrekt** — Vosk hätte sie sehr wahrscheinlich verstümmelt.
- Bei Doku-Themen mit vielen Eigennamen ist Namensgenauigkeit die halbe Miete für Untertitel + SEO.
- Möglich wurde es erst, weil die **Netzsperre weg** ist (Whisper-Download); vorher Vosk-Zwang.
- Nutzer-Faustregel: „wenn Whisper besser ist, nimm es."

## Historie / aufgelöster Widerspruch
- Ur-CLAUDE.md hatte an einer Stelle noch „Whisper statt Vosk? offen" — das widersprach der bereits getroffenen Entscheidung und wurde als veraltet markiert. Hier ist der Stand eindeutig: **Whisper = Standard.**

## Operational Implication
`transcribe_all.py` nutzt Whisper; Ausgabe als **flache Wort-Liste** → [[Learning-Captions]].

## Related
[[Video-03-Koepcke]] · [[Agent-Architecture]]
