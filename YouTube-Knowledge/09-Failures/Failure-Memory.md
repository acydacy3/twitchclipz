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

## Generalüberholung 07.09.2026 — warum die Regeln nicht griffen

> Diese fünf Einträge sind **nicht** inhaltliche Fehler, sondern **strukturelle**.
> Jeder von ihnen erklärt, wie eine Regel gelten und gleichzeitig gebrochen
> werden konnte, ohne dass es auffiel. Belege: Commit/Datei/Zeile.

### F-V9-A: Der Skript-Ordner enthielt ASR statt Skript (`root cause` → Rule)
**Was**: `prosperi/nb_transcribe.py` schrieb die Spracherkennung nach
`prosperi/skripte/short_XX.txt` — also genau dorthin, wo die Regel „Captions
IMMER aus Skript" ihre Wahrheitsquelle vermutet. Das echte Nutzer-Skript lag
daneben in `prosperi/skripte.json`.
**Ergebnis**: Alle **10** veröffentlichten Prosperi-Shorts tragen falsche
Captions — „Marathon des **Apples**" statt „Sables", „**Hartrigt** Bauer" statt
„Patrick", „**Kincea**"/„**Kindsjahr**" statt „Cinzia", „**Jeb**" statt „Jeep",
„**Neiden**" statt „Leiden". Short 10 enthält einen eingebrannten Stotter-Satz.
Übereinstimmung mit dem Skript: 81–97 %, nötig wären ~100 %.
**Root Cause**: Die Regel prüfte einen **Dateinamen**, nicht die **Herkunft**.
Ein Ordner beweist nichts.
**Fix**: `tools/kp_skript.py` schreibt `<serie>/skript/QUELLE.json` mit sha256
je Short. `tools/kp_gate.py` blockiert ohne diesen Nachweis. Zusätzlich
vergleicht das Gate die gerenderten Caption-Wörter Wort für Wort gegen das
Skript. `hoeren.py` schreibt jetzt `<pfad>.gehoert.txt` statt `short_XX.txt`,
damit ASR nie wieder wie ein Skript aussehen kann.
**Rule**: **Kein Text ist ein Skript, solange seine Herkunft nicht belegt ist.**
Werkzeuge, die ASR erzeugen, dürfen NIE in einen `skript/`-Ordner schreiben.

### F-V9-B: „pipeline-weit erzwungen" waren vier Zeilen Prosa (`disproven`)
**Was**: Commit `1587675` heißt „rule: Caption-aus-Skript **pipeline-weit**
erzwungen (F-V8-E **zukunftssicher**)". Er änderte ausschließlich
`.claude/skills/video/SKILL.md` und `Produktion-Pflichtliste.md` — **null
Code**. Der eigentliche Fix (`02da686`) traf nur `ralston/nb_build.py`.
**Ergebnis**: 1 von 3 Build-Skripten hatte den Fix. `/video` Schritt 7 schrieb
sogar fest, neue Serien sollten die Funktion aus `ralston/nb_build.py`
**kopieren** — Kopieren als Architektur.
**Rule**: Eine Regel ohne ausführbaren Prüfpunkt ist keine Regel. Ein Commit
darf „erzwungen" nur heißen, wenn ein Programm sie erzwingt.

### F-V9-C: Der Contrarian meldete „blockierend" und ließ durch (`disproven`)
**Was**: Die Pflichtliste §0 sagt „Kein Video wird gerendert oder hochgeladen,
bevor der Contrarian grün ist." Tatsächlich: `tools/nb_contrarian.py` gibt
**Exit-Code 0**, auch wenn es „FEHLER (blockierend)" druckt; es wird von
**keinem** Skript aufgerufen (nur in Markdown erwähnt); und sein Caption-Test
ist `cfg.get("words")` — er prüft, ob ein Schlüssel existiert, nie den Inhalt.
An `prosperi/configs/short_03.json` meldet er **„✓ Captions: words ✓"** — an
genau der Konfiguration, deren Wortliste „Apples" enthält.
**Rule**: Ein Prüfer, der niemanden aufhält, ist eine Meinung. Prüfer geben
Exit-Codes zurück und werden von einem Hook aufgerufen.

### F-V9-D: Der Erfolg meldete sich, das Ergebnis fehlte (`failed` → Rule)
**Was**: Beim Neu-Render der Ralston-Shorts am 07.09. schnitt `captions()` in
`ralston/nb_build.py` blind die erste Zeile des Skripts ab (dort stand früher
„short_01"). Nach der Umstellung auf saubere Skriptdateien war diese erste
Zeile der **gesamte Text**. Folge: leerer Abgleich → leere Wortliste → der
Untertitel-Filter wurde übersprungen → **fünf Videos ohne einen einzigen
Untertitel** — und der Build meldete „✓ Captions aus Skript".
**Root Cause**: Ein Gate **vor** dem Render kann nicht sehen, was **nach** dem
Render im Bild steht.
**Fix**: `kp_gate.py --nachher` misst im fertigen Video die Spitzenhelligkeit
im Untertitel-Band (validiert: 159 ohne, 235 mit Untertitel; Schwelle 200).
`captions()` bricht jetzt bei leerem Abgleich ab statt Erfolg zu melden.
**Rule**: **Jede Erfolgsmeldung braucht eine Messung am Ergebnis, nicht an der
Absicht.** Vorher-Gate UND Nachher-Gate.

### F-V9-E: Alle Manim-Animationen liefen in einer 3× zu großen Bühne (`fixed`)
**Was**: Manim leitet die Bühnenhöhe aus dem Seitenverhältnis ab. Bei
`-r 1080,1920` ergab das ~25 Einheiten Höhe; alle Szenen in
`tools/manim_scenes.py` sind aber für ~16 geschrieben (Titel bei `y=8.2`,
Achsen bei `x=±5`). **Jede** bisher produzierte Animation saß dadurch winzig
in der Bildmitte, umgeben von Leere.
**Zusammenhang**: Das erklärt das Nutzer-Urteil „furchbar" zu CrossSection
(F-V8-D) besser als der Inhalt der Szene.
**Fix**: `tools/manim_scenes.py` setzt im Hochformat `frame_height = 16`,
`frame_width = 9`.
**Rule**: Vor dem Einsetzen einer Animation ein Kontaktabzug ansehen
(`videoblick.py` oder ffmpeg-`tile`) — nicht nur prüfen, ob eine Datei entstand.

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
