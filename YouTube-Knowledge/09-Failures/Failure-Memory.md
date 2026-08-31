---
type: system
title: Failure-Memory
updated: 2026-08-24
tags: [system, failures, moc]
---

# Failure Memory — damit Fehler nur einmal bezahlt werden

Dauerhaftes Gedächtnis für gescheiterte Experimente, Fehlannahmen und
wiederkehrende Fehler — **quer durch den gesamten Lernkreislauf** ([[Agent-Architecture]]).
Zweck: verhindern, dass zukünftige Sessions bereits Widerlegtes erneut probieren.

## Status-Vokabular (nicht „funktioniert nie")
- `rejected` — bewusst verworfen
- `inconclusive` — Ergebnis nicht aussagekräftig
- `failed under conditions X` — scheiterte nur unter bestimmten Bedingungen
- `disproven` — widerlegt
- `superseded` — durch Besseres ersetzt

Jede Failure-Note dokumentiert: **Was getestet · Ergebnis · Warum gescheitert ·
Bedingungen · Learning · Wann es doch noch gültig sein könnte · „Do not repeat unless…"**.

## Failures (inhaltlich)
- [[Failure-Vertikale-Staffelung-Triptychon]] — Bild-Prompt (`disproven`)
- [[Failure-Verlorene-Videos-nicht-gesichert]] — Prozess (`failed under conditions`)
- [[Failure-OCR-Behauptung-TikTok]] — unbelegte Behauptung (`disproven`/`unknown`)
- [[Failure-Titelansage-und-Tempo]] — Dramaturgie/Takt (`disproven`)

## Failure Memory auf Agentenebene (V8-Recap — 3 Failures in einer Produktion)

### F-V8-A: Ein-Bild-Problem (`failed under conditions` → Rule)
**Was**: nb_build.py v1 hatte nur 1 Bild pro Short (SHORTS-Config mit `"img"` statt `"imgs"`) — alle 10 Shorts bestanden aus EINEM einzigen Ken-Burns-Clip.
**Ergebnis**: Alle 10 bereits hochgeladenen Shorts mussten neu gerendert und re-uploaded werden. Nutzer-Feedback: „unfassbare Enttäuschung".
**Root Cause**: Contrarian-Regel „2-6 Shots je Short" aus `Learning-Bilder-Prompts` wurde nicht angewendet. Schritt 4 (Bilder QC) der Produktion-Pflichtliste nicht durchgeführt.
**Fix**: SHORTS-Config auf `"imgs": [list]`, ffmpeg-Filtergraph mit N-fach concat, 4 KB-Presets wechselnd.
**Rule (Never again)**: Multi-Shot ist **IMMER** Pflicht. SHORTS-Config hat IMMER `"imgs"` (Liste), nie `"img"` (Singular). Vor Render: Kontaktabzug mit Einzel-Frame je Bild ansehen.

### F-V8-B: Karaoke-Subtitles ohne Highlight (`failed` → Rule)
**Was**: ASS-Dateien wurden ohne `\kf`-Tags generiert — plain text, kein Karaoke-Highlight. Wörter leuchteten beim Sprechen nicht auf.
**Root Cause**: `words_to_ass()` schrieb ganzen Chunk als Klartext statt `{\kf<cs>}Wort {\kf<cs>}Wort`.
**Fix**: `words_to_ass()` generiert jetzt `\kf<centiseconds>` pro Wort. Style: PrimaryColour=Gelb (`&H0000FFFF`), SecondaryColour=Weiß.
**Rule**: ASS-Karaoke **immer** mit `\kf` je Wort. Testen vor Upload via `ffplay`.

### F-V8-C: Unsichtbare Progressbar (`failed` → Rule)
**Was**: Progress-Bar war nur 10px hoch, halbdurchsichtig (`@0.85`). Auf Mobilgerät nicht sichtbar.
**Fix**: h=20px, `color=yellow` (voll opak), `t=fill`.
**Rule**: Progressbar immer h≥18px, kein alpha, color=yellow oder white.

### F-V8-D: CrossSection-Animation (gelber Punkt) (`superseded`)
**Was**: CrossSection (V6, V8 S02) = gelber Dot der durch einen Spalt gleitet. User: „furchbar, wieso arbeitest du nicht selbstständig mit Referenz".
**Fix**: Vollständig neu als cinematischer Slot-Canyon-Querschnitt — Felswände, Sandsteinschichten, Arm-Silhouette, Boulder-Drop mit Impact-Flash, Labels.
**Rule**: Animations-Klassen immer mit Beschriftung (Zahlen, Ortsname, Datum) und mindestens 3 erklärendem Grafik-Element. Keine anonymen Dots/Blobs.

### F-V8-E: Captions aus ASR statt aus dem Skript (`fixed`, 31.08.2026)
**Was**: Die Karaoke-Captions wurden aus der Spracherkennung der Tonspur (Vosk/Whisper) erzeugt — nicht aus dem Nutzer-Skript. Ergebnis: eingebrannte Fehler in fast jedem Short — „Aron Ralston" → „Rallsturm/Ralsdum/Raalstund", „Prothese" → „Protesse", „James Franco" → „jemes Franco", „Tourniquet" → „Tonikwett", „Bestseller" → „biszeller". Wäre ungeprüft hochgegangen; **§0d-Selbst-QC (videoblick.py) hat es vor dem Upload gefangen**.
**Root Cause**: Pipeline nutzte ASR für die WÖRTER. ASR rät und verstümmelt Namen/Fachbegriffe. Der korrekte Text existiert längst — im Skript (Constraint #1). Das vorhandene `align.py` (Text vom Skript, Timing vom Audio) war da, wurde aber übergangen — dasselbe V8-Muster wie A–D (Werkzeug vorhanden, nicht genutzt).
**Fix**: `nb_build.py` → neue `captions()`-Funktion: Wenn `skript/short_XX.txt` existiert, kommen die Wörter aus dem Skript, `align.py` mappt sie auf die Audio-Zeitstempel. ASR liefert nur noch Timing. Ohne Skript: lauter Warn-Fallback. 10 Shorts neu gerendert + §0d-verifiziert + neu hochgeladen (alte gelöscht).
**Rule**: **Caption-Text kommt IMMER aus dem vom Nutzer gelieferten Skript, nie aus ASR.** ASR nur fürs Timing (align.py). Gilt für jede Reihe, jede Pipeline. Skript wird je Video frisch vom Nutzer geliefert (nicht im Repo persistiert).

## Failure Memory auf Agentenebene
Wenn ein Agent wiederholt denselben Fehler produziert:
```
Agent → Recurring Failure → Root Cause → Experiment → Fix → Validation → Agent Learning
```
Beispiel-Schema (noch kein realer Fall dokumentiert): Hook-Agent generiert
generische Hooks → Root Cause: Prompt priorisiert Neugier über Spezifität →
Constraint hinzufügen → Korrekturrate messen. **Nur mit echten Zahlen füllen,
nie erfinden** ([[Knowledge-Architecture]] §6).

## Related
[[Decision-Verworfene-Werkzeuge]] · [[Contrarian-Layer]] · [[Audit-System]]
