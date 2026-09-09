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

### F-V9-F: Universelle Klassen mit fremden Vorgabewerten (`root cause` → Rule)

**Was**: Die Manim-Klassen `StatCounter` und `SurvivalDays` sind universell
gebaut und tragen Beispielwerte aus V7 Prosperi. Ralston Short 04 und 05
benutzten sie, ohne die Werte anzupassen. Im Bild stand:
„**0 TAGE allein in der Sahara**" und „**10 Tage — Mauro Prosperi**" —
in einem Video über Aron Ralston in einer Schlucht in Utah.
**Ergebnis**: Zwei terminierte Shorts trugen die Geschichte eines anderen
Menschen. Sie wären am 09. und 10.09. so erschienen.
**Root Cause**: Eine universelle Klasse ohne reihen-spezifische Ausprägung ist
eine Falle: sie rendert fehlerfrei und zeigt trotzdem das Falsche. Kein Gate
kann Inhalt gegen Geschichte prüfen — nur der Blick ins Bild fängt das.
**Fix**: Reihen-spezifische Unterklassen `RalstonMeissel` (15 Stunden
gemeißelt) und `RalstonInschrift` (Name, Geburts- und Todesdatum im Fels).
`Ralston65Minuten` ersetzt `RockTrap` für Short 08.
**Rule**: **Jede Reihe legt eigene Unterklassen an.** Eine universelle Klasse
wird nie direkt in einem Short verwendet — ihre Vorgabewerte gehören einer
anderen Geschichte. Vor dem Einsetzen einen Kontaktabzug ansehen.

### F-V9-G: Der ganze Kanal lief 8 dB zu leise (`fixed`, 07.09.2026)

**Was**: Alle gerenderten Shorts lagen bei **−22 LUFS**. YouTube normalisiert
auf etwa −14 und dreht dabei **nur herunter, nie herauf**. Der Kanal war damit
über alle bisherigen Videos hinweg deutlich leiser als jedes Konkurrenzvideo
im selben Feed.
**Root Cause**: Zwei Fehler in der Tonkette von `nb_build.py`:
1. `amix=inputs=2` teilt die Pegel standardmäßig durch die Anzahl der
   Eingänge — die Stimme verlor dadurch rund 6 dB.
2. Danach wurde nirgends auf einen Zielpegel normalisiert.
**Wie gefunden**: Nicht durch Hinhören, sondern durch die neu eingebaute
Regel R18, die die Lautheit am fertigen Video misst. Sie schlug beim ersten
Lauf bei allen zehn Shorts an.
**Fix**: `amix=…:normalize=0` + `loudnorm=I=-14:TP=-1.5:LRA=11`.
Ergebnis: −15,0 bis −15,7 LUFS über alle zehn Shorts.
**Rule**: **Lautheit wird gemessen, nicht geschätzt.** Zielband −20 bis −11
LUFS (R18). Gilt für jede Reihe und jedes Longform.
**Offen**: Alle bereits veröffentlichten Videos (V1–V7) sind zu leise. Nicht
korrigierbar ohne Neu-Upload — Entscheidung beim Nutzer.

### F-V9-H: Die Messung selbst war falsch kalibriert (`fixed`, 07.09.2026)

**Was**: Die Animations-QC meldete `RockTrap` als „nutzt nur 14 % der
Bildbreite". Die Szene war in Ordnung — die Schwelle war falsch. Gemessen
wurde ab Helligkeit 150; die orangen Felswände liegen bei etwa 133 und fielen
komplett durch das Raster, sodass nur noch die Schrift gemessen wurde.
**Gegenprobe**: Bei Schwelle 130 nutzt RockTrap 67 % der Breite. Der dunkelste
Szenen-Hintergrund erreicht 48 — 130 trennt also sicher.
**Zweiter Fall am selben Tag**: Die Untertitel-Messung lief zunächst mit
`ffmpeg -v error`, was genau die `metadata`-Ausgabe unterdrückt, die gemessen
werden sollte. Sie meldete deshalb immer 0 — also „keine Untertitel", egal was
im Bild stand.
**Rule**: **Jede neue Messung wird gegen einen bekannten guten UND einen
bekannten schlechten Fall geprüft, bevor man ihr glaubt.** Die Kalibrierung
gehört als Kommentar neben den Schwellwert, nicht in eine Notiz. Eine Messung,
die immer dasselbe sagt, misst nichts.

### F-V9-I: Der Riegel blockierte das Schreiben von Dokumentation (`fixed`)

**Was**: Der PreToolUse-Riegel prüft den Befehlstext auf Render-/Upload-Aufrufe.
Er blockierte dadurch einen Aufruf, der lediglich eine Tabelle **schrieb**, in
der ein Render-Befehl als Beispiel vorkam — und anschließend sogar seine eigene
Reparatur, weil auch die den Beispieltext enthielt.
**Doppelter Befund**: Das war zugleich der Beweis, dass der Riegel nicht
umgangen werden kann, und ein echter Fehlalarm.
**Fix**: Der Rumpf jedes Here-Dokuments wird vor der Prüfung entfernt.
Regressionsfall in `tools/tests/test_pre_tool_use.py`.
**Rule**: **Ein Riegel mit Fehlalarmen wird abgeschaltet und schützt danach gar
nichts mehr.** Jede Verschärfung braucht einen Testfall, der beweist, dass
normales Arbeiten weiter durchläuft.

### F-V9-J: Alle hochladen, dann alle löschen — Dubletten nach Abbruch (`fixed`)

**Was**: `kp_ersetzen.py` lud erst alle zehn Shorts hoch und löschte danach
alle alten. Nach dem fünften Upload griff YouTubes Tageslimit
(`uploadLimitExceeded`). Weil noch nichts gelöscht war, standen anschließend
**fünf Dubletten im Sendeplan** — zwei Videos auf demselben Termin.
**Was gut lief**: Nichts ging verloren. Die Reihenfolge „erst hochladen,
bestätigen, dann löschen" hat gehalten — hätte das Werkzeug zuerst gelöscht,
wären fünf Sendeplätze leer geblieben.
**Root Cause**: Der Zustand „neu gerendert, aber noch nicht drüben" existierte
nirgends. Das System wusste nach dem Abbruch nicht, dass etwas offen war.
**Fix**: Austausch läuft je Short vollständig durch (hochladen → bestätigen →
löschen → protokollieren) und schreibt `upload_log.json` nach **jedem** Short.
Offene Austausche tragen dort `austausch_offen: true`; `tools/kp.py status`
meldet sie als Schritt 7b und nennt den Befehl.
**Rule**: **Ein mehrteiliger Vorgang wird je Teil abgeschlossen, nicht je
Phase.** Und: jeder Zwischenzustand, der eine Handlung erfordert, muss auf der
Platte stehen — nicht im Gedächtnis der Sitzung.

### F-V9-K: Die Regel galt für die Shorts und lief am Langvideo vorbei (`fixed`)

**Was**: Regel R24 („kein Fremdmaterial im Schnitt") prüft die Shot-Konfiguration
der Shorts. `nb_lang.py` sucht sich seine Bilder aber selbst — über einen
Dateinamen-Treffer `_01.` bis `_04.` — und zog dabei
`ralston/bilder/broll/ref_01.jpg` bis `ref_04.jpg` heran: **echte Pressefotos
von Aron Ralston**, die nur Vorlage für die Bildgenerierung waren.
**Root Cause**: Die Regel existierte an einer Stelle, die Umgehung an der
nächsten. Genau das Muster, das dem Befund vom 07.09. zugrunde liegt — nur
eine Ebene höher.
**Fix**: `ist_fremdmaterial()` in `tools/kp_regeln.py` ist jetzt die **einzige**
Stelle, an der das entschieden wird. Sowohl R24 als auch `nb_lang.py` und
`kp_drive_holen.py` rufen sie auf.
**Rule**: **Eine Regel gehört in genau eine Funktion, und jeder Erzeuger ruft
sie auf.** Zwei Orte mit derselben Absicht laufen früher oder später
auseinander — und man merkt es erst im fertigen Video.

### F-V9-L: Auch V6 Nutty Putty trägt ASR-Fehler in den Captions (`root cause`)

**Was**: Beim Aufnehmen der Skripte für die Langvideos stellte sich heraus:
nicht nur V7 Prosperi, auch **V6 Nutty Putty** hat verstümmelte Caption-Wörter
(„zwenkt" statt „zwängt"). 9 von 10 Shorts wichen vom Skript ab.
**Woher das Skript kam**: Aus `nuttyputty/PRODUKTIONSBRIEF.md`, wo das vom
Nutzer gelieferte Skript je Short unter „**VO:**" steht. Es war die ganze Zeit
da — nur nutzte es niemand als Wahrheitsquelle.
**Fix**: Neues Werkzeug `tools/kp_captions.py` setzt die Caption-Wörter
serienunabhängig aus dem Skript neu (Timing bleibt aus der ASR, Text kommt aus
dem Skript, `align.py` führt beides zusammen). Die alten Listen bleiben als
`*.asr.json` daneben stehen. Beide Serien stimmen jetzt zu 100 % mit ihrem
Skript überein.
**Das ist das Werkzeug, das Commit `1587675` am 31.08. versprochen hat**
(„Caption-aus-Skript pipeline-weit erzwungen") und das nie existierte: jener
Commit änderte nur zwei Markdown-Dateien.
**Offen**: Die bereits veröffentlichten Shorts von V6 und V7 tragen die Fehler
eingebrannt. Nur durch Neu-Render und Austausch behebbar — kostet Aufrufe und
Alter der Videos. Nutzer-Entscheidung.

### F-V9-M: Eigene YouTube-Videos sind aus dem Container nicht ladbar (`failed under conditions`)

**Was**: Für Serien ohne lokales Material war der naheliegende Weg, die
veröffentlichten Shorts zu laden und zu einem Querformat-Langvideo zu montieren.
`yt-dlp` antwortet: *„Sign in to confirm you're not a bot."*
**Bedingung**: Betrifft Downloads aus dem Rechenzentrum, auch für **eigene**
Videos. Mit Browser-Cookies ginge es; die gibt es hier nicht.
**Ausweg, der funktioniert**: Das Material lag im Google Drive des Nutzers.
`gdown` kommt an die Dateien heran. Neues Werkzeug `tools/kp_drive_holen.py`
holt Voiceover und Bilder in die Ordnerstruktur, die `nb_lang.py` erwartet —
und überspringt dabei Fremdmaterial nach derselben R24-Definition.
**Rule**: **Der Container ist eine Wegwerfumgebung, Drive ist das Materiallager.**
Fehlt lokales Material, zuerst dort suchen — nicht bei YouTube.
**Nebenbefund**: Im Okene-Ordner lagen ein Getty- und ein AP-Pressefoto. Beide
wurden von R24 zurückgehalten. Ohne die Regel wären sie im Langvideo gelandet.

### F-V9-N: ffmpeg-Fehler waren nicht lesbar (`fixed`)

**Was**: `nb_lang.py` rief ffmpeg mit `-loglevel error` und `check=True` auf,
ohne stderr einzufangen. Bei einem Abbruch bekam man den kompletten Befehl als
Python-Traceback zu sehen — mehrere tausend Zeichen — aber **nicht die eine
ffmpeg-Zeile, die sagt warum**. Debuggen war Raten.
**Fix**: `sh()` fängt stderr ein und gibt im Fehlerfall die letzten zwölf
Zeilen aus.
**Rule**: Ein Werkzeug, das abbricht, muss den Grund zeigen, nicht den Befehl.

### F-V9-O: Ein Langvideo aus EINEM Bild — und alle Regeln gingen grün durch (`fixed`)

**Was**: `nb_lang.py` lieferte für Ralston ein 5:55 langes Video, das über die
volle Länge **ein einziges Motiv** zeigte — sanft geschwenkt, aber nie
gewechselt. Geplant waren 62 Einstellungen aus 8 verschiedenen Bildern; der
Schnittplan war nachweislich korrekt.

**Root Cause**: Die Eingaben wurden als `-loop 1 -t <dauer> -i bild` gebaut,
während `zoompan` zusätzlich `d=<frames>` bekam. `zoompan` erzeugt aus **einem**
Eingangsbild bereits genau `d` Ausgabeframes. Mit `-loop` liefert der Eingang
unendlich viele Frames, und jeder davon wird nochmals zu `d` Frames aufgeblasen.
Die erste Einstellung füllt damit das ganze Video, `-shortest` schneidet am Ton
ab — heraus kommt ein Film aus dem ersten Bild.

**Woher der Fehler kam**: `lang.py`, das Original, macht es richtig (`-i bild`,
kein `-loop`). Der Fehler entstand am 06.09. bei der Verallgemeinerung zu
`nb_lang.py` (Commit `e153bdd`, „generischer Longform-Builder") und wurde nie
geprüft — bis heute hatte die Serie, für die er gebaut wurde, gar kein
Langvideo, an dem es aufgefallen wäre.
*(Die 4,4 % Haltequote des V1-Langvideos hat damit NICHTS zu tun — V1 wurde
mit `lang.py` gebaut. Erst geprüft, dann behauptet.)*

**Warum keine Regel es fing**: R26 Länge (5:55 ✓), R27 Format (1920×1080 ✓),
R28 Ton (−14,1 LUFS ✓) — **alle drei grün**. Kein Messwert sagte etwas darüber,
ob sich das Bild jemals ändert. Ein Ein-Bild-Video besteht jede Prüfung, die
Datei-Eigenschaften misst statt Inhalt.

**Fix**: `-loop 1 -t` entfernt. Neue Regel **R29 Bildwechsel**: ffmpeg-
Szenenerkennung zählt die harten Schnitte, gefordert ist mindestens einer je
30 Sekunden. Gegen das kaputte Video gemessen: 0 Bildwechsel, nötig ≥ 11 —
sofort blockiert.

**Rule**: **Für jede Eigenschaft, die ein Zuschauer sofort sieht, muss es eine
Messung geben.** Länge, Format und Pegel sind Datei-Eigenschaften; ob ein Video
etwas zeigt, ist keine. Nach jeder neuen Erzeugungsart gehört ein Kontaktabzug
angesehen — die Regeln fangen das Messbare, der Blick fängt den Rest.

### F-V9-P: Das Gate blockierte den falschen Bau — Regeln brauchen Geltungsbereich (`fixed`)

**Was**: Der Riegel hielt den Bau eines **Langvideos** an, weil die **Shorts**
derselben Serie die Bewegtbild- und Titel-Regeln verletzen. Diese Shorts sind
seit dem 04.09. veröffentlicht und wurden gar nicht angefasst — der
Longform-Bauer nutzt nur Voiceover und Bilder, nicht die Shot-Konfiguration.
**Warum das gefährlich ist**: Ein Fehlalarm ist nicht bloß lästig. Er ist der
Weg, auf dem ein Riegel abgeschaltet wird — und danach schützt er nichts mehr.
Dasselbe Muster wie F-V9-I (Blockade beim Schreiben von Dokumentation).
**Fix**: Regeln tragen ein Feld `bauart`. Ohne Angabe gelten sie für alles
(R01 Herkunft, R02 Captions, R24 Fremdmaterial). Nur wer ausdrücklich
`"shorts"` trägt, wird beim Longform-Bau übersprungen (R03/R04 Bewegtbild,
R05–R09, R11). `kp_gate.py --fuer shorts|longform` wählt den Satz; der Riegel
setzt ihn bei `nb_lang.py` automatisch.
**Gegenprobe**: prosperi als Shorts geprüft = rot, als Longform = grün.
**Rule**: **Eine Regel ohne Geltungsbereich ist entweder zu eng oder zu weit.**
Präzisieren, wo sie gilt — nicht abschwächen, wo sie stört.

### F-V9-Q: Zum vierten Mal — ein Werkzeug je Serie kopiert (`superseded`)

**Was**: `ralston/nb_upload.py` kann Langvideos hochladen, `prosperi/nb_upload.py`
nicht, `nuttyputty/nb_upload.py` wieder anders. Für das Prosperi-Langvideo hätte
man ein viertes Skript kopieren müssen.
**Zusammenhang**: Das ist derselbe Befund wie F-V9-B (Caption-Fix nur in einer
von drei Kopien) und F-V9-K (Fremdmaterial-Regel nur an einer von zwei Stellen).
Innerhalb von zwei Tagen viermal dieselbe Ursache.
**Fix**: `tools/kp_longform.py` — **ein** Werkzeug für alle Serien. Es liest die
Metadaten aus `<serie>/metadata.json` unter `longform`, lässt immer erst das
Langform-Gate laufen und lädt nur bei grünem Ergebnis hoch.
**Rule**: **Ein neues Werkzeug gehört nach `tools/`, nie in einen Serien-Ordner.**
Serien-Ordner enthalten Material und Konfiguration, keine Logik. Was in einem
Serien-Ordner liegt, wandert nicht — und ein Fix, der nicht wandert, ist keiner.

### F-V9-R: Das Bildwerkzeug lieferte seit Monaten nichts — und nannte das ein Ergebnis (`fixed`)

**Was**: `tools/nb_openverse.py` ist seit Wochen in CLAUDE.md als autonome
Bildquelle geführt („Broll autonom sourcing, Nutzer sucht nie selbst"). Es hat
**nie ein einziges Bild geliefert**. Jeder Aufruf endete mit `Openverse: 0 Bilder`
und **Exit-Code 0**.
**Root Cause**: Das Werkzeug lud die Datei als `ov_1.raw` und rief dann
`convert` auf. ImageMagick entscheidet nach der Endung: `.raw` heißt
Kamera-RAW, also DNG. Der Decoder brach ab, `rr.returncode != 0` wurde still
übersprungen, die Zählung blieb bei 0.
**Warum es niemandem auffiel**: Weil „0 Bilder" wie ein Suchergebnis aussieht
und nicht wie ein Absturz. Das ist dieselbe Bauart wie F-V9-D — ein Schritt
meldet Erfolg, während er nichts produziert.
**Fix**: Endung aus der URL ableiten. Und: **ein Werkzeug, das nichts liefert,
beendet sich mit Exit-Code ≠ 0.** Zusätzlich schreibt es jetzt `HERKUNFT.json`
mit Lizenz, Urheber und Quellseite je Bild.
**Rule**: **Ein Werkzeug, das leer zurückkommt, muss das als Fehler melden.**
Ein leeres Ergebnis und ein kaputtes Werkzeug sehen von außen gleich aus —
also muss das Werkzeug den Unterschied sagen.

### F-V9-S: Eine Regel nannte eine Quelle, für die es kein Werkzeug gab (`fixed`)

**Was**: CLAUDE.md Kernregel 8 verlangt Bildbeschaffung über
„Commons-Kategorien + Openverse". Für Openverse gab es ein (kaputtes)
Werkzeug, für Commons-Kategorien **gar keins**. Die halbe Regel war seit ihrer
Niederschrift unausführbar.
**Folge**: Das Bildmaterial kam faktisch aus unbelegten Beständen — mit dem
Ergebnis in F-V9-T.
**Fix**: `tools/nb_commons.py` — Kategoriesuche, Dateiliste inkl. einer Ebene
Unterkategorien, Download mit Lizenz-Eintrag in `HERKUNFT.json`. Die
Drosselung der Wikimedia-API wird abgewartet und, wenn sie bleibt, **genannt**
statt als „0 Bilder" verkauft (Lehre aus F-V9-R).
**Rule**: **Eine Regel, die eine Quelle nennt, braucht ein Werkzeug für diese
Quelle.** Sonst ist sie Prosa — derselbe Befund wie beim Gate, nur eine Ebene
früher: nicht „Regel ohne Prüfpunkt", sondern „Regel ohne Ausführungspunkt".

### F-V9-T: Acht themenfremde Bilder liefen durch jede Prüfung (`fixed`)

**Was**: Im fertigen Nutty-Putty-Langvideo liefen mit:
- ein Höhlen-**Zeltlager** mit lachenden Menschen in rosa Schlafsäcken und
  Einkaufstüten — unter dem Satz, dass die Reibung im Fels jeden Zug auffraß
  (`short_06/03,04`, `short_07/02,03`),
- drei **historische Schwarzweißfotos** von Soldaten mit Tragen auf
  Feldbahngleisen — das Unglück ist von 2009 in Utah (`short_08/01–03`),
- ein **Straßen-Schrein** mit Figur hinter Gitter — unter dem Satz, dass die
  Höhle mit Beton versiegelt wurde (`short_10/02`).
**Alle Regeln waren grün.** R26 Länge, R27 Format, R28 Ton, R29 Bildwechsel —
das Video erfüllte jede messbare Eigenschaft und war trotzdem falsch.
**Root Cause**: Die Regeln messen **Dateieigenschaften**. Kein Prüfpunkt kann
sagen, wovon ein Bild handelt. Das ist keine Lücke, die man mit einer weiteren
Schwelle schließt — es ist die Grenze der Bauart. Gefunden wurde es durch
Hinsehen (Kontaktabzug), nicht durch Messen. Vgl. F-V9-O, gleiche Lehre.
**Fix (drei Teile, weil ein Teil nicht reicht)**:
1. `<serie>/bilder/AUSSORTIERT.json` — Bild → **Grund**. Nichts wird gelöscht
   (Guardrail #1); ein Bild wird ausgetragen und seine Begründung liegt daneben.
2. `bild_ausgeschlossen(serie, pfad)` in `tools/kp_regeln.py` — **eine**
   Funktion, die Fremdmaterial UND Aussortiertes entscheidet. `nb_lang.py` ruft
   nur noch sie auf und **druckt jedes ausgeschlossene Bild mit Grund**.
3. `.gitignore` der Serie: `bilder/` ist weiterhin ignoriert, aber
   `AUSSORTIERT.json` und `HERKUNFT.json` sind **ausgenommen**. Sonst wäre die
   Entscheidung mit dem Container weg und die Bilder beim nächsten Bau zurück.
**Ersatz**: 2 Bilder aus Wikimedia Commons (Kategorie *Caving*, CC BY / CC BY-SA)
und 3 selbst erzeugte (Hugging Face Z-Image, gratis) — Seilabstieg im Spalt,
Flaschenzug im Fels, betonversiegelter Eingang mit Gedenktafel. Prompts und
Seeds stehen in `nuttyputty/bilder/HERKUNFT.json`.
**Rule**: **Was ein Riegel nicht messen kann, muss angesehen und die
Entscheidung neben das Material geschrieben werden.** Ein Blick, der nicht
festgehalten wird, muss beim nächsten Container noch einmal geworfen werden —
und wird es nicht.

### F-V9-U: Die richtige Regel am falschen Gegenstand — und wie eine Ausnahme trotzdem kein Freibrief wird (`fixed`)

**Was**: R01 (Skript-Herkunft) hielt den Bau des **Lengede**-Langvideos an.
Für Lengede und Okene gibt es kein belegtes Nutzer-Skript — nur
Voiceover-Dateien aus dem Drive. Der Bau läuft deshalb mit
`nb_lang.py --ohne-captions`: **es kommt kein Text ins Bild.**
**Warum das eine echte Frage war**: R01 hatte recht — rohe Spracherkennung
einzubrennen hat V6 und V7 ruiniert, das ist F-V9-A. Sie zielte nur am
Gegenstand vorbei: R01 schützt nicht das Skript, sondern **den Text im Bild**.
Wo keiner ins Bild kommt, kann keiner falsch sein.
**Die Versuchung, der nicht nachgegeben wurde**: `--ohne-captions` einfach als
Ausnahme durchzuwinken. Damit wäre das Flag eine Hintertür — einmal angehängt,
und R01 schweigt für immer, auch dort, wo sie gebraucht wird. Genau so werden
Riegel wertlos (vgl. F-V9-P: Fehlalarme führen zum Abschalten, Freibriefe zum
Aushöhlen — beide Wege enden am selben Punkt).
**Fix**: Die Ausnahme wird zu einer **Behauptung mit Preis**.
1. R01/R02 tragen `betrifft="text"`. `--ohne-captions` überspringt genau diese
   zwei — keine anderen.
2. `nb_lang.py --ohne-captions` legt `<serie>/render/long.ohne-captions.json`
   ab, mit Grund und dem Hinweis, wer das nachmisst. Ein späterer Bau **mit**
   Untertiteln löscht die Marke wieder.
3. **Neue Regel R30**: Liegt die Marke, misst sie am fertigen Langvideo die
   Helligkeit im Untertitel-Band — dieselbe Messung wie R15, mit umgekehrtem
   Vorzeichen. Steht dort Schrift, ist das Gate rot.
4. Der Riegel reicht `--ohne-captions` an das Gate durch.
**Gegenprobe**: `kp_gate.py lengede --fuer longform` = rot (10 Verstöße),
mit `--ohne-captions` = grün; ralston (mit Untertiteln gebaut) meldet R30 als
„nicht zutreffend"; ein untertitelloses Video mit Schrift im Band wäre rot.
**Rule**: **Eine Ausnahme von einer Regel muss selbst eine prüfbare Behauptung
sein.** Wer sich auf sie beruft, muss am Ergebnis belegen, dass die Bedingung
wirklich vorlag. Sonst ist die Ausnahme nur ein Schalter, mit dem man die Regel
abstellt.

### F-V9-V: Der Dirigent schickte die nächste Sitzung auf eine Sackgasse (`fixed`)

**Was**: `kp.py status` nannte für **Lengede** und **Okene** als nächsten
Schritt „2 SKRIPT — Skript-Herkunft belegen: `kp_skript.py <serie> --aus
<datei-vom-nutzer>`". Für beide Serien existiert kein Nutzer-Skript und wird
keins existieren; es gibt nur Voiceover-Dateien aus dem Drive. Der Schritt war
also nicht bloß der falsche — er war unerfüllbar, und der **mögliche** Schritt
(das Langvideo ohne Untertitel) kam gar nicht vor.
**Zweiter Befund am selben Ort**: Eine Serie galt als fertig, sobald
`render/long.mp4` auf Platte lag. Ob das Video jemals hochgeladen wurde, hat
niemand geprüft. Ein gebautes, nie hochgeladenes Langvideo war unsichtbar.
**Warum das zählt**: `kp.py status` läuft bei **jedem** Sitzungsstart und ist
für die nächste Sitzung die einzige Ansage, was zu tun ist. Ein Dirigent, der
in eine Sackgasse zeigt, kostet eine ganze Sitzung — und der Nutzer müsste es
ansprechen, genau das soll er nicht müssen.
**Fix**:
- `longform` zerfällt in **gebaut** und **hochgeladen** (aus
  `upload_log.json`). Die Zeile zeigt jetzt `nein` / `gebaut` / `hoch`, und
  „gebaut, noch nicht hochgeladen" ist ein eigener nächster Schritt
  (`kp_longform.py <serie> --wirklich`).
- Sind **0** Skripte belegt, ist der Shorts-Weg zu, der Longform-Weg offen:
  der nächste Schritt ist `nb_lang.py <serie> --ohne-captions`. Das ist keine
  Umgehung von R01 — R30 misst am fertigen Video nach (F-V9-U).
**Gegenprobe**: Okene → „Langvideo geht trotzdem, ohne Untertitel"; Lengede →
„gebaut, noch nicht hochgeladen"; Ralston (hochgeladen) → „fertig".
**Rule**: **Der nächste Schritt muss ausführbar sein.** Ein Schritt, der auf
etwas wartet, das es nicht gibt, ist keine Anweisung, sondern eine Blockade —
und blockiert die Schritte, die möglich wären, gleich mit.

### F-V9-W: Meine eigene neue Regel war nach 20 Minuten falsch (`fixed`)

**Was**: R30 sollte belegen, dass ein als untertitellos ausgewiesenes Langvideo
wirklich keinen Text trägt. Erste Fassung: Spitzenhelligkeit im
Untertitel-Band messen, unter der Schwelle bleiben. Der erste Einsatz
blockierte das Lengede-Langvideo mit „als untertitellos ausgewiesen, aber im
Band steht Schrift (Helligkeit 237)".
**Im Band stand keine Schrift.** Dort waren Grubenlampen und Gesichter aus
dem Spielfilmmaterial. Nachgesehen an drei Einzelbildern (68 s, 137 s, 220 s):
kein einziger Buchstabe im ganzen Video.
**Der Denkfehler**: R15 misst richtig herum — *Untertitel vorhanden* macht das
Band hell. Die Umkehrung gilt nicht: *Band hell* heißt nicht *Untertitel*. Eine
Spitzenhelligkeit kann weiße Schrift nicht von einem hellen Bild
unterscheiden. **Die Messung maß nicht, was sie behauptete** — derselbe Fehler,
den ich am selben Tag an der anim-QC-Schwelle und an der `-v error`-Messung
korrigiert habe, nur diesmal in einer Regel, die ich gerade erst geschrieben
hatte.
**Warum es trotzdem gut ausging**: Der Fehlalarm kam am ersten Video, an dem
die Regel lief, und wurde nachgesehen statt weggeschaltet. Wäre er beim
zwanzigsten aufgetreten, wäre die naheliegende Reaktion gewesen, R30
abzuschalten — und danach hätte sie nichts mehr geschützt (F-V9-P).
**Fix**: R30 prüft jetzt den **Beleg statt des Pixels**. Die Marke enthält die
**Filterkette, die wirklich an ffmpeg ging**; enthält sie einen Textfilter
(`subtitles=`, `ass=`, `drawtext=`), ist die Behauptung falsch. Deterministisch,
ohne Fehlalarm. Die Helligkeit bleibt als **R31 — Hinweis, keine Regel**
(`hart=False`), mit ihrer Grenze im Regeltext und im Code daneben.
**Preis**: Das fertige Lengede-Video musste neu gebaut werden, weil seine Marke
noch keine Filterkette trug. Die Alternative wäre gewesen, das Feld von Hand
nachzutragen — also die Behauptung aufzuschreiben, statt sie zu belegen. Genau
das soll die Regel verhindern.
**Rule**: **Vor jeder neuen Messung: Gilt sie auch in der Gegenrichtung?**
Wenn A ⇒ B gemessen wird, aber B ⇒ A gebraucht wird, ist die Messung falsch.
Und: **Wo ein Beleg über den Bauvorgang möglich ist, schlägt er die Messung am
Ergebnis** — der Bauvorgang weiß, was er getan hat; das Pixel muss es raten.

### F-V9-X: Weichzeichnen löscht Schrift nicht — es macht sie groß (`fixed`)

**Was**: Das San-José-Langvideo entsteht als Montage der fertigen 9:16-Shorts
auf einen 16:9-Rahmen; daneben stand bisher ein weichgezeichneter, gezoomter
Ausschnitt desselben Bildes. Die Shorts tragen **eingebrannte Untertitel** —
der Zoom vergrößerte sie mit und legte sie als lesbare Geisterschrift an
beide Bildränder. Im Kontaktabzug standen dort „Die", „aufgeteilt", „zuerst",
„verst…" in halber Bildhöhe.
**Warum der Reflex falsch war**: Weichzeichnen wirkt wie Unkenntlichmachen. Es
ist aber nur ein Tiefpass — und ein um den Faktor 1,8 vergrößerter Buchstabe
bleibt nach `sigma=28` gut lesbar. Was die Schrift unlesbar macht, ist nicht
der Weichzeichner, sondern der Verzicht darauf, sie überhaupt zu vergrößern.
**Fix**: `nb_concat_shorts.py --hintergrund dunkel|blur`.
- `dunkel` legt eine ruhige, fast schwarze Fläche neben das Bild. Für Shorts
  mit eingebrannten Untertiteln ist das die richtige Wahl — und es passt zur
  nüchternen Anmutung des Kanals besser als ein Farbmatsch.
- `blur` bleibt für Material ohne eingebrannten Text, jetzt mit `sigma=48`
  und abgedunkelt, damit derselbe Effekt dort schwächer ausfällt.
**Nebenbefund, im selben Zug behoben**: `kp_gate.py --langform` brach mit
„Keine Shorts gefunden" ab, weil es zuerst Voiceover-Dateien suchte. San José
hat keine mehr — nur die fertigen Shorts aus dem Drive. Ausgerechnet die
Serie, die den einzig möglichen Weg geht, hätte ihr Gate nie durchlaufen und
nie hochgeladen werden können. Die Langform-Regeln gelten je Serie; die
Short-Suche entfällt jetzt bei `--langform`.
**Zweiter Anlauf, zweiter Fehler**: Die erste Umsetzung des dunklen
Hintergrunds erzeugte **je Short einen eigenen `color`-Generator** und legte
das Bild per `overlay` darauf. Bei zehn Shorts sind das zehn Dekoder plus
zehn Generatoren — der Kernel schoss ffmpeg mit SIGKILL ab, und übrig blieb
eine abgeschnittene Datei ohne `moov`-Atom. **Das Gate fing genau das**:
„R26 nur 0:00 — unter 3 Minuten", „R27 Bildmaße nicht lesbar". Ein
halbgeschriebenes Video wäre sonst hochgeladen worden.
Richtig ist `pad=1920:1080:(ow-iw)/2:0:color=…` — ein Filter, kein zweiter
Eingang, kein Puffer.

**Rule**: **Was ein Effekt verspricht, ist nicht, was er tut.** Vor dem
Einsatz eines Filters als Schutzmaßnahme: das Ergebnis ansehen, nicht die
Absicht bewerten. Und: **ein Riegel, der den einzigen möglichen Weg versperrt,
wird abgeschaltet** — dann schützt er nichts mehr (dritte Ausprägung nach
F-V9-I und F-V9-P).

### F-V9-Y: R29 zählte 1 statt 23 — ein schwarzer Rand zerstört die Szenenerkennung (`fixed`)

**Was**: Das San-José-Langvideo besteht aus zehn aneinandergesetzten Shorts —
unstreitig voller Schnitte. R29 zählte **einen** Bildwechsel in 4:32 und
blockierte den Upload.
**Root Cause**: Die ffmpeg-Szenenerkennung vergleicht **ganze Bilder**. Bei
einer Montage von 9:16-Material auf einen 16:9-Rahmen sind links und rechts
zwei Drittel der Fläche unveränderlich schwarz. Bei jedem Schnitt bleibt der
größte Teil des Bildes identisch, der Unterschied fällt unter die Schwelle.
**Die Regel maß nicht das Video, sondern meinen eigenen Rand.**
**Kalibrierung** (09.09., dieselben Dateien, voller Rahmen → mittlere Hälfte
`crop=iw/2:ih:iw/4:0`):

| Serie | voller Rahmen | Bildmitte |
|---|---|---|
| sanjose | **1** | **23** |
| ralston | 46 | 52 |
| nuttyputty | 44 | 45 |
| lengede | 37 | 42 |
| okene | 28 | 29 |

Bei vollformatigem Material ändert der Ausschnitt praktisch nichts; bei
gerahmtem rettet er die Messung.
**Fix**: R29 misst auf der Bildmitte. Die Tabelle steht als Kommentar neben
der Messung. **Die Schwelle bleibt unverändert** — „mindestens ein Schnitt je
30 Sekunden". Präzisiert wurde die Messung, nicht die Anforderung.
**Rule**: **Eine Messung, die ganze Bilder vergleicht, misst auch den Rahmen
mit.** Vor der Übernahme einer Schwelle aus einer Materialform in eine andere:
an beiden Formen nachrechnen. Das ist innerhalb von zwei Tagen der dritte
Fall derselben Art — anim-QC-Schwelle (150 statt 130), R30 (Bandhelligkeit),
jetzt R29. Alle drei maßen etwas Benachbartes statt der Sache selbst.

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
