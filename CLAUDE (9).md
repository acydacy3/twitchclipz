# Katastrophenprotokoll — Produktions-Konstrukt

Diese Datei wird zu Sitzungsbeginn automatisch geladen. Sie ist das
Gedächtnis des Projekts: alles, was wir durch Versuch und Irrtum gelernt
haben, steht hier, damit es nicht in jeder neuen Sitzung neu erarbeitet
werden muss.

**Regel für dieses Dokument:** Erkenntnisse werden ergänzt, nie
überschrieben. Wenn eine Regel sich als falsch erweist, wird sie
durchgestrichen und begründet — der Irrweg ist Teil des Wissens.

**Wozu das Ganze — in den Worten des Nutzers:** „Learning gemerkt,
Fehler gemerkt, verbessert, immer aktueller Stand ohne Befehl, quasi
selbst wissen was wir alles gelernt haben, wenn es von Video zu Video
geht über Tage und Wochen." Das ist kein Nebenziel, das ist der Zweck
des Projekts. Jede Sitzung soll auf dem Stand der letzten aufsetzen,
ohne dass er etwas dafür tun muss.

**Wo dieser Kreis heute offen ist:** Das Lesen läuft automatisch — diese
Datei wird zu Sitzungsbeginn geladen, ohne dass jemand etwas sagt.
Getestet am 17.08.2026: der Container hatte sich zurückgesetzt, die
Datei kam aus dem Repo zurück. Das **Zurückschreiben** läuft nicht
automatisch, weil `git push` mit 403 gesperrt ist. Solange das so ist,
gilt: am Ende jeder Sitzung die aktualisierte Datei zum Hochladen
schicken. **Sobald die Claude-GitHub-App Schreibrecht hat, entfällt
dieser Schritt und der Kreis ist vollständig geschlossen.**

---

## 0. Konstrukt-Landkarte & Wachstums-Checkliste (Selbstprüfung)

**Zweck:** Kompakte Übersicht über das ganze Konstrukt + laufendes Protokoll
jeder neuen Sache (Learning ODER Fehler). Damit prüft sich die Sitzung selbst,
ob die Datei **stetig wächst** und nichts übersehen wurde.

**Ressourcen-Prinzip (Nutzer, 19.08. — nicht falsch verstehen):** „Limits/
Credits nicht verschwenden" meint **WASTE vermeiden** — redundante Checks,
unnötige vidIQ-Abrufe, Arbeit, die nichts bringt. Es meint **NICHT** sparen, wo
Qualität zählt. **Wenn Auftrag, Modell und das nach unserem Wissen beste
erreichbare Ergebnis viel fordern, wird VOLL investiert** — Tiefe, mehrere
Durchläufe, Subagenten, so viel wie nötig. Geiz beim entscheidenden Schritt ist
der teurere Fehler. Sparsamkeit gilt für Überflüssiges, nie für Qualität.

**Selbstprüf-Regel (bei jedem Sitzungsende):** (1) Ist mindestens eine Zeile im
Wachstums-Log dazugekommen? Wenn nein → laut fragen „haben wir wirklich nichts
gelernt?". (2) Jede neue Erkenntnis/jeder Fehler bekommt hier EINE Zeile + steht
ausführlich in der passenden Sektion. (3) Bild-Prompts werden von Bild zu Bild
detailreicher — dieser Fortschritt gehört in Sektion 6. (4) **Jede Regel nennt
ihr WARUM**, nicht nur das Was.

**Absicherung gegen Festfahren (mehrschichtig, limit-schonend):** Kapazität ist
KEIN Problem — die Datei ist winzig gegen das Kontextfenster; das Risiko sind
Widersprüche, Aufmerksamkeit und Drift, nicht die Zeilenzahl. Deshalb: (a) jede
Sitzung die Selbstprüfung oben (gratis, Claude selbst); (b) an **Meilensteinen**
(alle ~+300 Zeilen ODER vor jedem großen Stapellauf) ein **Subagent-Konstrukt-
Audit** — liest die Datei KALT und meldet Widersprüche, Doppelungen, verwaiste
Learnings, fehlendes Warum, Veraltetes. Nicht jede Sitzung (spart Limits). Der
Audit-Prompt liegt im Projekt-Chat/Wissen. (c) Bläht eine Sektion auf →
konsolidieren statt endlos anhängen. Letzter Konstrukt-Audit: 19.08.2026 abends
(Tiefen-Audit, 15 Prüfpunkte, 4 Fixes — siehe Wachstums-Log oben).

**Audits (YouTube-Zahlen) → einzige Datei `audit-videos.csv`**, NICHT in der
CLAUDE.md (hält die Memory schlank). **PRO Video** mit Datum: Aufrufe,
Aufrufe/Tag, AVP%, Ø-Dauer, Retention-Ratio, Engagement%, Abos gewonnen, Länge.
Regel: bei jedem Audit **alle Videos mit dem Tagesdatum anhängen** → so verfolgt
man die Bindung JEDES Videos über die Tage. Warum diese eine Datei: der Nutzer
will die Experten-Ebene (Pro-Video), Kanal-Summen lassen sich daraus ableiten —
eine frühere Kanal-Summen-CSV (`audit-log.csv`) wurde am 19.08. als redundant
gelöscht. Warum getrennt von CLAUDE.md: tägliche Zahlen wären dort Lärm; als CSV
über Tage/Wochen vergleichbar + jederzeit zu Trend-Kurven renderbar. Gehört ins
Upload-Paket. **Hinweis:** Analytics-API hinkt 2–3 Tage → frische Videos haben
noch AVP=0, füllt sich mit dem Altern.

### Landkarte
| # | Sektion | Inhalt |
|---|---|---|
| 1 | Der Kanal | Nische, Takt, Arbeitsteilung, Umgang mit Nutzer |
| 2 | Die Pipeline | 10 Schritte (transcribe→videocheck), Spracherkennung |
| 3 | Harte Lehren | Video/ffmpeg, Ton, Untertitel, Hook, **Bilder**, Shorts-Dramaturgie, Analytik, SEO |
| 4 | Werkzeuge & Zugänge | APIs, vidIQ, Netzsperre (weg), yt-dlp, TikTok/Buffer, verworfene Tools |
| 4b–4f | Kanaldaten & Audits | gemessene Längen/Aufrufe, Titel/Cover, YouTube-API, Agenten-Widerspruch |
| 5 | Stand | Video 1 (Tham Luang), 2 (San José), 3-Idee |
| 6 | Sitzung 18.08. | Koepcke gewählt, Werkzeuge, **Bild-Engine-Vergleich**, Bild-Prompt-Lehren, Längen-Konsolidierung |
| 7 | Schnitt-Protokoll | verbindliche Reihenfolge vor jedem Schnitt |
| 8 | Persistente Werkzeuge | wiederverwendbare Skripte im Repo, Regel + Zweck |

**Hinweis zur Reihenfolge:** Sektionen 4b–4e sind vor Sektion 5 eingeschoben
(Detail-Unterabschnitte zu Sektion 4). **4f steht abweichend NACH Sektion 5**
(am 18.08. chronologisch als Audit-Nachtrag angehängt, statt physisch bei 4e
einzusortieren — Kalt-Leser stolpert hier; bewusst so belassen, weil eine
spätere Umsortierung Anker/Verweise brechen würde). Sektionen 7 und 8 stehen
in numerischer Reihenfolge (Fix 19.08. abends nach Nutzer-Hinweis — vorher stand
8 vor 7). **Meta-Regel für neue Sektionen:** an der numerisch richtigen Stelle
einfügen, nicht am Datei-Ende; nur wenn Umsortierung existierende Verweise
brechen würde, mit Datums-Kommentar am Datei-Ende anhängen.

### Wachstums-Log (neueste zuerst)
- **19.08. abends (Tiefen-Audit, 15 Prüfpunkte):** 4 echte Fixes, 11 sauber. (1) Werkzeug-Ordner: 4 Skripte liegen im Repo-**ROOT** (per curl gegen raw.githubusercontent.com verifiziert), NICHT unter `werkzeuge/` — Sektion 8 Statuswarnung + Tabellen-Pfade korrigiert. (2) Zeile 435 „Whisper statt Vosk?, offen" widersprach Sektion 2 („Whisper=Standard seit 19.08.") — durchgestrichen + Querverweis. (3) Bild-Engine-Tabelle Zeile 1134 nannte Z-Image „Standard-Engine", direkt darunter überstimmt Nutzer-Entscheidung für Nano Banana Pro/Seedance — Tabellen-Zelle präzisiert, „Standard-Engine" durchgestrichen. (4) Landkarten-Hinweis behauptete „4b–4f vor Sektion 5" — falsch, 4f steht physisch NACH Sektion 5; korrigiert + Begründung (Umsortierung würde Anker brechen). Sauber geprüft: Netzsperre-Referenzen (alle historisch als durchgestrichen markiert, außer omniroute-Notiz historisch-korrekt), YouTube-API-Notizen (schon abgehakt), Video-3-Status (Sektion 5+6-Nachtrag konsistent), vidIQ 30 (überall konsistent, 170 nur durchgestrichen), Retention 60/75% (jede Wiederholung im Kontext gerechtfertigt), Zahlen (alle Aufruf-/Video-/Short-Werte mit Datum+Kontext), Wachstums-Log (chronologisch, ohne interne Widersprüche), Nutzer-Zitate (unverändert), Warum-Pflicht (Stichprobe: die meisten Regeln nennen ein Warum, wenige Zielgrößen wie −14 LUFS ohne — nicht kritisch).
- **19.08. abends (Reihenfolge-Fix):** Sektion 8 hinter Sektion 7 verschoben (numerische Ordnung 6→7→8). Vorher stand 8 zwischen 6 und 7 (weil beim Anlegen nur an Landkarte gedacht, nicht an physische Position). **Meta-Regel:** neue Sektionen physisch an der numerisch richtigen Stelle einfügen, nicht am Datei-Ende. Nutzer-Hinweis: „bleib bitte ordentlich sodass neue sessions wissen was abgeht" — das ist Kern des Konstrukts.
- **19.08. abends (Konstrukt-Audit):** Toter Verweis `v2/` in Sektion 2 durchgestrichen (Skripte liegen im Repo-Root, per `ls` verifiziert). `werkzeuge/` existiert im Repo noch NICHT — Statuswarnung in Sektion 8 ergänzt. Landkarten-Reihenfolge-Hinweis (8 vor 7, 4b–4f vor 5). Sektion-6-Nachtrag: Video 3 mittlerweile fertig, verweist auf Sektion 5. Keine echten Widersprüche (Bild-Engine, YouTube-Zugang, vidIQ=30, Netzsperre weg, Whisper=Standard, Retention 60/75% — überall konsistent oder mit Querverweis).
- **19.08. abends:** Video 3 (Koepcke) komplett produziert — 10 Shorts (19–33s, Karaoke, Ken-Burns, Musik, TEIL-Leiste, Hook-Banner bei 1/3/6/7/9), alle zu YouTube hochgeladen und terminiert 21.–24.08. (IDs siehe Sektion 5). Titel-Score Short 1: 74/100 (vidIQ) — Kalibrierung für spätere Titel.
- **19.08. abends:** **KERN-REGEL: wiederverwendbare Skripte kommen ins Repo unter `werkzeuge/`, werden NIE neu geschrieben.** In dieser Sitzung mussten `transcribe_all.py`, `build_configs.py`, `youtube_upload.py`, `upload_all.py` neu gebaut werden, weil sie nur in ausgelaufenen Containern lagen — 15+ Minuten Blindflug. Nutzer zu Recht verärgert. Neue Sektion 8.
- **19.08. abends:** vidIQ-Balance korrigiert: **30** (renewable 0/150 + Add-on 30/80, refresh 15.09.), NICHT 170. Sektion 4-Tabelle nachgezogen.
- **19.08. abends:** Whisper > Vosk BESTÄTIGT (nicht mehr nur „offen"). `faster-whisper small-de int8` transkribierte alle 10 Voiceover in ~2 min mit Wort-Zeiten; „Koepcke", „LANSA", „Yacumama" korrekt. Neue Regel: Voiceover mit Fremdwörtern/Namen → Whisper. Vosk nur Offline-Fallback.
- **19.08. abends:** Bild-Größen-Normalisierung Pflicht vor `short.py` (Higgsfield/Seedance/NBP liefern 768×1344, 1024×1024, 1152×2048, …). `short.py` hat SRC 1600×2848 hardcoded — Fix per `convert -resize 1600x2848^ -gravity center -extent 1600x2848` (fill+crop). Ergänzt in Sektion 3/Bilder.
- **19.08. abends:** JSON-Escape-Falle bei deutschen Anführungszeichen („…") in YouTube-Beschreibungen — schließendes `"` als `\"` sonst `json.load`-Bruch. Ergänzt in Sektion 4d.
- **19.08. abends:** `karaoke.py` erwartet **flache Liste** `[{...}, ...]`, NICHT `{"words": [...]}`. Whisper-Ausgabe entsprechend speichern. Ergänzt in Sektion 2.
- **19.08. abends:** Google Drive über `gdown --folder URL -O outdir` funktioniert bei öffentlichen Ordnern, ohne Google-API-Setup. Ergänzt in Sektion 8.
- **19.08. abends:** Nutzer-Klarstellung zur Skript-Rolle: **aus Transkript kürzen ist erlaubt und erwartet** — die alte Regel „Skript kommt vom Nutzer, nicht erfinden" gilt weiter, aber Kürzen/Formen aus vorhandenem Material ist Kernaufgabe hier. Sektion 1 „Arbeitsteilung" spannt das schon ab (Kürzen: ja, Erfinden: nein) — Erinnerungs-Zeile fürs Log.
- **19.08.:** Ressourcen-Prinzip klargestellt (Sparen = WASTE vermeiden, NIE Qualität; fordert die Aufgabe viel → voll investieren).
- **19.08.:** ruvnet/ruflo geprüft, verworfen (würde CLAUDE.md überschreiben +
  Limits verbrennen; Wegwerf-Container hebelt Kernnutzen aus). audit-videos.csv
  als einzige Audit-Datei (audit-log.csv gelöscht).
- **19.08.:** Erster Subagent-Konstrukt-Audit → Drift gefixt: Engine (Z96/217),
  YouTube-Zugang (nur-API-Key veraltet), Video 3=Koepcke (Lengede→V4), 4f-Top-
  Short 885 überholt durch 1.286, claude-youtube-Tabelle nachgezogen.
- **19.08.:** Absicherung angelegt (Subagent-Audit an Meilensteinen, Warum-Pflicht).
- **19.08.:** Hook-Text-Regel präzisiert (Untertitel=Stimme; Banner optional).
- **19.08.:** Sektion 7 Schnitt-Protokoll angelegt (Nutzer-Regel).
- **19.08.:** defaultLanguage=de per API gesetzt; Tag-Regel präzisiert (Video vs Kanal).
- **19.08.:** Kostenloser YT-Audit (Hook>Länge am eigenen Kanal belegt, 1.286-Short).
- **19.08.:** Diese Landkarte + Selbstprüfung angelegt (Sektion 0).
- **18.08.:** Bild-Engine-Vergleich (6 Engines); Nutzer wählt Nano Banana Pro + Seedance.
- **18.08.:** Bild-Prompt-Lehren: Alter-Band, Medium-Shot statt Close-up, Kamera-Kürzel, Figur-Konstanz.
- **18.08.:** Triptychon-Bug (vertikale Staffelung widerlegt).
- **18.08.:** Video 3 = Koepcke; Skript-Entwurf + 10-Shorts-Plan.
- **18.08.:** yt-dlp läuft (deno); claude-youtube als claude.ai-Skill; Remotion installiert.
- **17.–18.08.:** Netzsperre aufgehoben; YouTube-Token gültig; GitHub-Push weiter 403 (Nur-Lese).

---

## 1. Der Kanal

Deutscher Faceless-YouTube-Kanal. Nische: Katastrophen und Unglücke,
nüchtern erklärt. Vorbild im Tonfall: *Fascinating Horror* — sachlich,
kein Drama in der Stimme, das Ereignis trägt sich selbst.

- **Takt:** alle 48 h ein Langvideo (~5 min), täglich 2–5 Shorts
- **Kern:** aus **einem** Voiceover und ~10 Bildern entstehen **ein
  Langvideo und 9–11 Shorts**. Die Bulk-Produktion ist der Kanal.
- **Priorität liegt auf den Shorts.** Bei Video 1 hat das Langvideo
  abgeschnitten (4,4 % Haltequote), die Shorts trugen.

### Arbeitsteilung
- **Das Originalskript kommt vom Nutzer.** Niemals eigenmächtig ein Skript
  schreiben und lospro­duzieren. Kürzen, korrigieren, Fremdwörter
  nachschlagen: ja. Erfinden: nein.
- Voiceover: ElevenLabs (Nutzer). Bilder: über Higgsfield (Nutzer) — **aktuelle
  Engine-Wahl siehe Sektion 6** (Nutzer bevorzugt Nano Banana Pro + Seedance,
  Z-Image für Landschaft; Seedream 5.0 Lite als Reserve). Schnitt, Ton,
  Untertitel, SEO: hier.
- **Vor jedem großen Stapellauf einen einzelnen Testdurchlauf zeigen
  und bestätigen lassen.**

### Wie mit dem Nutzer gearbeitet wird
- **Er arbeitet nicht mit der Kommandozeile.** Nie einen Terminalbefehl
  als blanke Anweisung hinwerfen. Entweder selbst erledigen, oder eine
  Datei zum **Doppelklicken** bauen (`.bat` unter Windows), oder in
  nummerierten Klick-Schritten erklären — mit den echten Knopfnamen.
- **Zu jedem Befehl gehört die Anleitung**, in einfacher Sprache, ohne
  Fachwörter. Er hat ausdrücklich darum gebeten.
- **`.md`-Dateien kann er nicht öffnen.** Längere Ergebnisse als
  Artifact-Seite ausliefern, nicht als Textdatei.
- **Diese Datei sammeln, nicht tröpfeln.** Erkenntnisse laufend
  eintragen, die Datei aber nur **einmal am Ende einer Arbeitssitzung**
  zum Hochladen schicken.
- Grosse Dateien: `split -b 25000000`, dazu eine `.bat`, die die Teile
  prueft, zusammenfuegt, die Groesse gegen den Sollwert vergleicht und
  die Teile danach selbst loescht. Das hat zweimal funktioniert.

---

## 2. Die Pipeline

Reihenfolge und Werkzeuge (~~alle im Projektordner `v2/`~~ **korrigiert 19.08.2026
abends: liegen im Repo-Root, nicht in `v2/`** — verifiziert per `ls`: kein
`v2/`-Ordner existiert; die Skripte unten liegen direkt neben dieser CLAUDE.md.
Wiederverwendbare Neubauten kommen nach `werkzeuge/`, siehe Sektion 8):

| Schritt | Datei | Was sie tut |
|---|---|---|
| 1 | `transcribe_vosk.py` | Voiceover → `captions.srt` + `words.json` (Wortzeiten) |
| 2 | `align.py` | korrigierten Skripttext auf die Vosk-Zeiten abbilden |
| 3 | `pauses.py` | alle Sprechpausen listen → Schnittgrenzen |
| 4 | `bildcheck.py` | Bilder prüfen, **bevor** produziert wird |
| 5 | `karaoke.py` | ASS-Untertitel mit Wort-Hervorhebung |
| 6 | `musik.py` | Musikbett erzeugen (synthetisch, lizenzfrei) |
| 7 | `short.py` | einen Short bauen (9:16) |
| 8 | `serie.py` | alle Shorts als Stapel |
| 9 | `lang.py` | das Langvideo bauen (16:9) |
| 10 | `videocheck.py` | Ton, Bild, Untertitel prüfen **vor** dem Hochladen |

**Spracherkennung:** ~~Vosk (`vosk-model-small-de-0.15`) ist der Standard~~
**geändert 19.08.2026 abends: Whisper ist jetzt Standard, Vosk nur noch
Offline-Fallback.** Belegt an Video 3 (Koepcke): `faster-whisper small-de int8`
auf CPU transkribierte alle 10 Voiceover in ~2 Minuten mit Wort-Zeiten und
erkannte deutsche Fremdwörter/Namen (Koepcke, LANSA, Yacumama) korrekt — Vosk
hätte diese sehr wahrscheinlich verstümmelt. Warum umgestellt: bei Doku-Themen
mit vielen Eigennamen ist Namensgenauigkeit die halbe Miete für Untertitel und
SEO. Nutzer-Faustregel: „wenn Whisper besser ist, nimm es". Vosk-Modelle über
`kercre123/vosk-models` bleiben installiert — für Notfälle ohne Netz.

**Ausgabeformat für karaoke.py (19.08.2026 gelernt):** `karaoke.py` liest die
Wort-Zeiten als **flache Liste** `[{"word": …, "start": …, "end": …}, …]`,
NICHT als `{"words": [...]}`. Whisper-Ausgabe deshalb ohne den `words`-Wrapper
speichern, sonst bricht der Karaoke-Renderer stumm. Warum: eine einheitliche
Liste, weil auch Vosk in diesem Format arbeitete.

---

## 3. Harte Lehren

### Video / ffmpeg

- **`-pix_fmt yuv420p` immer explizit setzen.** `xfade` wählt sonst
  yuv444p, und viele Player verweigern die Wiedergabe. Das hat bei
  Video 1 einen kompletten Neu-Export gekostet.
- **`zoompan` erzeugt `d` Frames pro *Eingangs*frame.** Das Bild darf
  deshalb nur als **ein** Frame hineingehen (`-i bild.jpg`), niemals mit
  `-loop 1 -t`. Sonst wiederholen sich Einstellungen und die Zeitachse
  ist Müll.
- **Grundzoom minimal über 1 (`1.05`).** Bei genau 1.0 ist der
  Schwenkbereich null und `zoompan` verschluckt die Handkamera-Bewegung.
- **Gegen den „statisch"-Eindruck wirken drei Dinge zusammen:** kurze
  Einstellungen (Schnitt alle 6–11 s), weich beschleunigter Zoom
  (smoothstep `3t²−2t³` statt linear), Handkamera-Drift aus zwei
  unterschiedlich schnellen Schwingungen. Dazu Filmkorn und Vignette.
- **Mehrfach-Ausschnitt ist der eigentliche Hebel.** Ein Bild liefert
  drei bis fünf Einstellungen, nicht eine. Der Ausschnitt macht den
  Schnitt, nicht das Bildmaterial. Halbiert den Bildbedarf und
  verdoppelt das Tempo.
- Bilder sind 1600×2848 (9:16). Ein 16:9-Ausschnitt daraus ist 1600×900
  — nur 31 % der Höhe, also drei klar verschiedene Einstellungen
  übereinander. **Langvideo in 1080p** (1,2× Hochrechnung, unkritisch).

### Ton

- **Ziel −14 LUFS, Spitze unter −1,5 dBTP.** Video 1 lag bei −15,7.
- `loudnorm` allein reicht nicht: bei dichter Sprecherstimme (LRA ~4)
  bremst die Spitzengrenze das Gain aus. Kette, die trifft:
  **zweistufiges `loudnorm` → `volume=1.6dB` → `alimiter=limit=0.84:level=false`**
- **`level=false` beim `alimiter` ist Pflicht** — sonst zieht er das
  Ergebnis selbsttätig auf Vollaussteuerung (gemessen: +0,1 dBFS).
- **Musik selbst erzeugen, nicht aus der YouTube-Bibliothek.** Bei Shorts
  teilt YouTube die Einnahmen mit jedem Musikstück: ein Track = 50 % des
  Anteils, zwei = 33 %. Dazu Content-ID-Sperren. `musik.py` erzeugt ein
  Moll-Bett aus Drone, Pad, Herzschlag, Schimmer und Rauschen.
- **Musik duckt per Sidechain unter die Stimme**, wird nicht pauschal
  leise gedreht. In Sprechpausen kommt sie hoch.

### Untertitel

- **Größe 104 bei 1080 Breite** (Shorts). 58 war bei Video 1 zu klein —
  von vidIQ ausdrücklich bemängelt. 78 war immer noch zu klein.
- Kontur 9, Schatten 5, aktives Wort gold (`&H0047D4FF`, ASS ist **BGR**)
  auf 118 % skaliert.
- **Umbruch nach Breite (15 Zeichen), nicht nach Wortzahl.** Sonst steht
  mal eine kurze Zeile über 55 % der Breite. Ziel: 85–90 %.
- **Überlappende Ereignisse stapelt libass übereinander** — das ist der
  Ruckel-Effekt („das alte steht noch unten drunter"). Endzeiten hart auf
  `nächster Start − 0,02 s` kappen.
- `PlayResX`/`PlayResY` müssen gesetzt sein, sonst verschwinden die
  Untertitel.
- Lesegrenze: **21 Zeichen/Sekunde, 45 Zeichen/Zeile.**
- **Breitbild (16:9) braucht 76 Punkt, nicht 60.** 60 auf 1920 entspricht
  34 auf 1080 — dreimal kleiner als in den Shorts. Derselbe Fehler wie
  bei Video 1, nur im anderen Format. Dazu `MAX_CHARS 28`, `MAX_WORDS 5`,
  `MARGIN_V 105`.

### Aufhaenger-Text (Hook)

- **Groesse automatisch rechnen, nie fest setzen.** Roboto Black belegt
  rund 0,49 px je Zeichen und Groessenpunkt; bei 1080 Breite bleiben nach
  Rand und Kastenrand 948 px. Formel: `min(78, 948 / (0.49 * Zeichen))`.
  Ohne das lief der Text bei Teil 3, 6 und 10 aus dem Bild.
- **Hoechstens ~22 Zeichen.** Laenger wird die Schrift so klein, dass der
  Aufhaenger seinen Zweck verliert. Kurz schlaegt vollstaendig.
- **Pfeil nur, wo es ein einzelnes Objekt zum Zeigen gibt.** Sonst wirkt
  er wie ein Tic. Bei Video 2 auf 4 von 11 Shorts.
- ImageMagick: `-rotate` **braucht `-background none`**, sonst verliert
  das PNG seine Transparenz und der Pfeil bekommt einen weissen Kasten.

### Bilder (über Higgsfield — Engine-Wahl siehe Sektion 6)

- Ganze Sätze, kein Stichwortsalat. **Hauptmotiv zuerst** — frühe Wörter
  wiegen schwerer. 80–90 Wörter.
- ~~**Vertikale Staffelung ausdrücklich beschreiben** (oben / Mitte /
  unten). Ohne sie gibt jedes Bild nur eine Einstellung her.~~
  **Falsch — am 18.08.2026 an Bild A (Koepcke-Pilot) belegt.** Wer drei
  *verschiedene* Motive in „bottom/middle/top third" beschreibt, bekommt
  bei Seedream 5.0 ein **echtes Drei-Panel-Triptychon** mit harten
  schwarzen Trennfugen — „single continuous image, no panel borders"
  überstimmt das NICHT. Stattdessen: **eine** Kameraeinstellung, Tiefe im
  *selben* Raum über „foreground / midground / background". Drei
  Ausschnitte holt man dann per Crop aus diesem einen zusammenhängenden
  Bild, nicht durch drei beschriebene Zonen. Zusätzlich in den
  Negativ-Prompt: `triptych, panels, collage, split screen, borders`.
- **Lichtrichtung und -härte immer nennen.**
- **Nationalität explizit** („Chilean", „Latin American") — sonst
  rendert das Modell europäische Gesichter.
- **Keine Anführungszeichen im Prompt** — was in Anführungszeichen steht,
  malt das Modell als echten Text ins Bild. Für leere Schilder/Zettel
  „blank" schreiben.
- Bei Querschnitten **„single continuous image, no panel borders"** —
  sonst kommen Comic-Panels mit schwarzen Balken (Bild 9, Video 2).
- Gegen flaue Bilder: „most of the frame in deep black shadow",
  „clear crisp air, no atmospheric haze", ein Gesicht nah an der Kamera.
- **Bei neuem Sujet erst ein Bild, prüfen, dann den Rest.**
- Intime Zwei-Personen-Szenen sträuben sich gegen Hochformat-Staffelung.
- **Bild-Größen vor `short.py` normalisieren — Pflicht (19.08.2026 gelernt).**
  Higgsfield/Seedance/Nano Banana Pro liefern NICHT verlässlich 1600×2848.
  An Video 3 gemessen: 768×1344, 896×1200, 960×1696, 1024×1024, 1152×2048 kamen
  bunt gemischt. `short.py` hat `SRC_W=1600, SRC_H=2848` HARDCODED — jeder
  Ausschnitt wird auf diese Größe berechnet, ein falsch dimensioniertes Bild
  gibt Bildrand oder Beschnitt. Fix vor Pipeline-Eintritt:
  `convert IMG -resize 1600x2848^ -gravity center -extent 1600x2848 IMG` (fill
  plus zentrierter Crop, so bleibt das Motiv mittig). Warum vor `short.py` und
  nicht in `short.py`: der Fix ist bild-, nicht szenenbezogen; eine Normalisierung
  am Pipeline-Eingang macht alle Downstream-Skripte ausfall­sicher.

### Shorts-Dramaturgie

- **Auf Erzählgrenzen schneiden, nie mechanisch.** Video 1 hatte
  13 Stücke „eine Szene = ein Short" — 15–33 s, die irgendwo anfingen.
  Jeder Short braucht Aufhänger → Spannung → Auflösung/Cliffhanger.
- **Alle Grenzen auf echte Sprechpausen (≥ 0,42 s).**
- **Einstellung 1 ist ein Detail, nie eine Totale**, ~2–3 s. Erster
  harter Schnitt spätestens bei Sekunde 3.
- ~~**Der Aufhänger-Text sagt etwas anderes als die Stimme.** Doppelte
  Information verschenkt einen Kanal.~~ **Präzisiert 19.08.2026 (Nutzer-Einwand,
  bestätigt):** Die alte Regel warf ZWEI Texte zusammen.
  **(a) Laufende Untertitel = IMMER die Stimme spiegeln** — die Mehrheit schaut
  anfangs stumm, die Caption ist der einzige Weg, dass der Hook bei Ton-aus
  ankommt; hält Blick + Verständnis. Alle bisherigen Shorts machen das richtig,
  der Bestwert (1.286) hatte Text=Stimme. Nicht dran rütteln.
  **(b) NUR ein zusätzlicher Hook-Banner** (große Zeile oben, erste 2–3s) DARF
  etwas anderes sagen (Neugier-Anker, den die Stimme noch nicht beantwortet, z.B.
  „Nur 1 von 92 überlebte"). Das ist **optionale Kür, kein Muss** — testen (2–3
  Shorts mit vs. ohne), Zahlen entscheiden. Kein Beleg, dass Abweichen je besser lief.
- **Keine Titelansage.** „Das Wunder von San José. Kurzfassung." am
  Anfang des Voiceovers ist die Doku-Variante von „Hey guys welcome
  back" — bei Video 1 nachweislich der Grund für 4,4 % Haltequote.
  Erste 3,06 s werden weggeschnitten.
- **„TEIL X" oben** als Leiste, damit Zuschauer im Raster sehen, wo es
  weitergeht.
- Tonart pro Short wechseln, damit nicht elf Stück gleich klingen.

### Analytik — Denkfehler, die wir schon gemacht haben

- **640 Aufrufe bei 58 Impressionen ist für Browse/Suche arithmetisch
  unmöglich.** Über 90 % der Reichweite kam aus dem Shorts-Feed. Der
  Shorts-Feed erzeugt keine Thumbnail-Impressionen.
- **Keine CTR-Schlüsse unter ~1000 Impressionen.** Der vidIQ-Audit lobte
  „exzellente 15,52 % CTR" — das waren 9 Klicks. Rauschen.
- Seit März 2025 zählt jeder Playback als 1 View, Loops zählen mit.
  **Engaged Views** nutzen, nicht Aufrufe.
- Einen Short **frühestens an Tag 4–5** bewerten.
- **Der Kanal wurde am 15.08.2026 gegründet.** Frühere Notizen mit
  „neun Tage alt" waren falsch. 628 Aufrufe am ersten vollen Tag sind
  ein normaler Start, kein Misserfolg.
- **Höchstens 3 Benachrichtigungen pro 24 Stunden.** Bei Video 1 kamen
  zehn Uploads in 48 Stunden; ab dem vierten lief keine mehr. Das
  Ergebnis war 440, 274, dann 14, 9, 6, 4. Nicht die Teile waren das
  Problem, das Tempo war es. **Zwei Shorts pro Tag, Langvideo zuerst.**
- Der Nutzer teilt Langvideos **bewusst** in Teile auf und bleibt dabei,
  auch gegen den vidIQ-Rat. Seine Zahlen stützen ihn: „Teil 8" war mit
  274 Aufrufen sein zweitbestes Video. Der echte Befund des Audits war
  ein **Titel**problem („Teil 7 😮😦" enthält kein Suchwort) — deshalb
  steht die Teilnummer als **Leiste im Bild**, nie im Titel.

### SEO — was echte Zahlen ergeben haben

- **Das Suchvolumen sitzt im Genre, nicht im Ereignis.** Gemessen für DE:
  `grubenunglück` 0 (Wettbewerb 51), `bergleute` 0, `lengede` 0, `zeche`
  0, `unter tage` 0 — dagegen `doku` 230.831, `dokumentation deutsch`
  37.258, `wahre geschichte` 28.225, `katastrophe` 9.927, `bergbau`
  5.099, `bergwerk` 3.335.
- **Deutsche Titel reißen mitten im Kompositum ab** („Grubenunglüc…")
  und verlieren dabei den Sinn komplett; Englisch bleibt lesbar. Regel:
  **die vollständige Aussage muss bei Zeichen 35 fertig sein**, danach
  ist alles Zugabe.
- **„69 Tage" nie als Titelanfang.** Der Spielfilm mit Antonio Banderas
  heißt auf Deutsch „69 Tage Hoffnung". Als Faktanker im Mittelteil
  stark, als Anfang chancenlos.
- **Falsche Tags schaden aktiv.** Bei einem neuen Kanal ist Text das
  einzige Einordnungssignal. Ein Tag für Inhalte, die im Video nicht
  vorkommen (`tschernobyl` auf einem Bergwerksvideo), ist kein neutraler
  Tag, sondern ein falsches Signal im ungünstigsten Moment.
- Kanal-Grundset des Nutzers: ~25 Tags, davon 80 % dauerhaft, 1–2
  ereignisspezifisch pro Video. Höhlenbegriffe gehören zu Video 1.
- **Untertiteldatei (.srt) hochladen** — eingebrannte Untertitel sind für
  YouTube Pixel, kein Text. Bei einem Kanal ohne Verhaltenssignale mehr
  wert als Titel, Beschreibung und Tags zusammen.
- Kanal-Standardsprache und Themenkategorien waren **nicht gesetzt**. **ERLEDIGT 19.08.: defaultLanguage=de per API gesetzt** (brandingSettings, erst lesen dann voll zurückschreiben). **Präzisierung zur Tag-Regel:** „falscher Tag (tschernobyl)" gilt für **Video**-Tags, NICHT für **Kanal**-Keywords — dort sind Genre-Begriffe (flugzeugabsturz, mayday, tschernobyl) für einen allgemeinen Katastrophen-Kanal legitim und richtig.

### Wie mit Agenten gearbeitet wird

Bewährtes Verfahren, zweimal erfolgreich: **zwei Agenten unabhängig
dieselbe Aufgabe, einer mit Playbook, einer ausdrücklich ohne — dann
eine Runde Gegenrede, dann zusammenführen.** Beide haben in Runde zwei
eigene Fehler eingeräumt, die im ersten Durchlauf niemand gesehen hätte.

**Die Lehre daraus:** Agenten liefern Struktur und Argumente, **Zahlen
liefern die Entscheidung.** Beide lagen beim Haupt-Keyword falsch, und
das kam erst durch einen einzigen vidIQ-Abruf heraus. Nie umgekehrt.

---

## 4. Werkzeuge und Zugänge

| Werkzeug | Stand |
|---|---|
| **YouTube Data API v3** | `googleapis.com` **erreichbar**, 10.000 Einheiten/Tag. ~~nur API-Key, wichtigster offener Punkt~~ **ERLEDIGT: OAuth-Refresh-Token gültig** (Scopes youtube + yt-analytics), Uploads/Analytics/Terminierung produktiv — siehe 4d/Sektion 6. |
| vidIQ (MCP) | **richtiger Kanal verbunden** (`UC1KCzLNlgGiYsLNQ7Z0HA-g`, „Katastrophenprotokoll", DE). Konto `kisha-ners@gmx.de`. **Guthaben 30 (renewable 0/150, Add-on 30/80, refresh 15.09.2026)** — Stand 19.08.2026 abends, ~~170~~ war veraltet. Kostet Credits — sparsam, aber **ein gezielter Keyword-/Titel-Score-Abruf vor jeder Titelentscheidung lohnt sich immer**. |
| `YoutubeTags` (pip) | installiert; scrapt youtube.com. ~~**hier blockiert**~~ **19.08.2026: Netzsperre ist weg — vermutlich hier nutzbar, noch nicht neu geprüft.** Fallback bleibt: auf dem PC des Nutzers. Liefert Tags/Titel/Beschreibung fremder Videos. |
| `claude-youtube` Skill | **als claude.ai-Skill hochgeladen (lädt automatisch je Sitzung)**, 14 Sub-Skills, 9 Guides. Quelle AgriciDaniel/claude-youtube; setup.sh klont zusätzlich als Fallback. Siehe Sektion 6. |
| Google Drive | Ordner `Katastrophenprotokoll-Pipeline` (`1MFz5gNIBQfcXWBw8evnop_oUJ-9TnWtX`) |

### Die Netzsperre — aufgehoben am 17.08.2026

~~Die Umgebung heißt „Default — trusted network access"
(`env_01BD8vQ6WzwWTY1m1wUrAzj1`, angelegt 14.08.2026). Der Name führt in
die Irre: es ist eine Gästeliste, kein Türsteher — nur ausdrücklich
gelistete Hosts kommen durch, alles andere fällt automatisch raus.~~
**Der Nutzer hat die Netzwerkrichtlinie der Umgebung selbst umgestellt**
(claude.ai/code → Environments → Network access → auf eine offene Stufe).
Bestätigt getestet: `youtube.com`, `api.elevenlabs.io`, `higgsfield.ai`,
`trends.google.com`, `reddit.com` antworten jetzt alle normal (301/200),
vorher kam überall `gateway answered 403 to CONNECT (policy denial)`.

**Wichtig, falls die Umgebung je zurückgesetzt wird:** Diese Einstellung
ist Teil der Umgebungs-Konfiguration, nicht des Repos — sie überlebt
keinen Neuaufbau der Umgebung selbst (wohl aber normale Container-Resets
innerhalb derselben Umgebung). Falls Hosts wieder mit 403 blockiert
erscheinen, ist das der erste Verdacht: Environments → Network access
prüfen, nicht neu debuggen.

**Damit fällt eine ganze Reihe alter Notizen weg** (ElevenLabs/Higgsfield
nicht bezahlen wegen Sperre, Gemini als Bild-Notlösung wegen Sperre,
Whisper wegen Sperre auf Vosk ausgewichen) — die galten nur, solange die
Gästeliste stand. ~~Ob sich das jetzt lohnt, neu zu bewerten (z. B. Whisper
statt Vosk?), ist offen~~ **entschieden 19.08.2026 abends: Whisper ist
Standard, Vosk nur Offline-Fallback — siehe Sektion 2.**

### Weitere geprüfte und verworfene Werkzeuge
- **yt-dlp läuft (Stand 18.08.2026).** Die alte „YouTube blocks all major
  cloud IPs"-Notiz ist überholt — mit `deno` als JS-Runtime holt yt-dlp
  Untertitel, Metadaten und Cover problemlos. Nur die Video-*Streams* sind
  auf Datacenter-IPs bot-gesperrt („confirm you're not a bot") und
  bräuchten Login-Cookies; Untertitel/Thumbnails reichen für die Analyse.
- **`ZeroPointRepo/youtube-skills`** (521★) — läuft über
  `transcriptapi.com`. ~~gesperrt~~ **Netzsperre seit 17.08. weg** — technisch
  jetzt vermutlich nutzbar, aber nie neu geprüft; kein akuter Bedarf, weil wir
  Untertitel schon über yt-dlp/Whisper haben.
- **Instagram/TikTok-Uploader** (alle unter 2 Sternen) — meist
  Browser-Automatisierung, bricht bei jeder Layout-Änderung und
  gefährdet das Konto. Dazu: Instagram nimmt **keine Dateien** entgegen,
  nur eine **öffentliche URL**; TikTok verlangt ein Prüfverfahren, ohne
  das nur private Entwürfe möglich sind.
- ~~**Brauchbar, sobald die Sperre fällt:**~~ **Sperre ist seit 17.08. weg —
  Punkt gilt jetzt allgemein:** `pauling-ai/youtube-mcp-server` — 40 Werkzeuge
  inkl. **Analytics API**. Noch nicht installiert (unsere eigenen
  Werkzeuge in `werkzeuge/` reichen bisher), aber jederzeit greifbar.

### Bewusst NICHT installiert
- **`ruvnet/ruflo`** (Agent-Meta-Harness, 68k★, MIT) — geprüft 19.08.2026,
  **verworfen für unser Umfeld.** Drei Gründe: (1) `npx ruflo init` schreibt
  eine eigene `CLAUDE.md` + `.claude/` + 27 Hooks + 12 Auto-Hintergrund-Worker →
  würde unser handgebautes Konstrukt überschreiben UND verbrennt Claude-Limits
  (Gegenteil der Nutzer-Regel). (2) Sein Kernnutzen (selbst-lernendes Gedächtnis/
  Vektor-DB) braucht einen persistenten Workspace — bei Wegwerf-Container + Push-
  Sperre jede Sitzung weg; Cross-Session-Gedächtnis lösen wir schon per CLAUDE.md +
  audit-videos.csv + claude.ai-Skill. (3) Enterprise-Schwarm (100+ Agenten, Raft)
  = Overkill für 1-Personen-Pipeline; Agenten-Hilfe haben wir nativ (Subagenten +
  Zwei-Agenten-Methode). Falls je testen: NUR in leerem Wegwerf-Ordner, nie im Repo.
- **`AgriciDaniel/claude-seo`** — 25 Skills, aber reines *Website*-SEO
  (Sitemap, Schema.org, hreflang, Core Web Vitals). Für einen Kanal ohne
  Website nutzlos. Brauchbar war genau eine Datei: die YouTube-Data-API-
  Referenz. Zurückholen, falls je eine Website entsteht.
- **`rediumvex/ai-video-generator-claude`** — Prompts für Seedance 2.0
  (Video), wir nutzen Seedream (Standbilder).
- **`Panniantong/Agent-Reach`** — kann genau, was fehlt, läuft über
  `mcp.exa.ai`/`r.jina.ai`. ~~beide hier blockiert. Nur lokal sinnvoll.~~
  **19.08.: Netzsperre weg — technisch jetzt vermutlich hier nutzbar, nicht neu geprüft.**
- **`thedotmack/claude-mem`** — Sitzungsgedächtnis-Plugin. In einer
  Wegwerf-Umgebung wie dieser müsste es jede Sitzung neu installiert
  werden. Diese Datei im Repo leistet dasselbe zu Kosten null.

### omniroute — getestet und wieder verworfen, Stand 17.08.2026

**Ergebnis nach ausführlichem Test: kein Gewinn für diesen Kanal, Einsatz
beendet.** Wurde vom Setup-Skript der Umgebung automatisch global
installiert (npm, `/opt/node22`, bestätigt über den npm-Log-Zeitstempel —
7 Sekunden nach Container-Start). **Die Installationszeile ist am
17.08.2026 aus dem Setup-Skript entfernt worden** — omniroute wird ab
sofort nicht mehr automatisch installiert. Der zwischenzeitlich gebaute
`.claude/hooks/session-start.sh`-Automatik-Fix (siehe Git-Historie dieser
Datei für Details) wurde aus demselben Grund wieder **gelöscht** — er
hätte nur einem Werkzeug gedient, das wir nicht mehr benutzen.

**Zwei echte Programmfehler beim ersten Start (Version 3.8.49), damals per
Hook umgangen, jetzt nur noch als Erinnerung — falls omniroute je wieder
versucht wird:**
1. Die native SQLite-Programmdatei (`better-sqlite3`) fehlt nach der
   automatischen Installation. Behoben mit `omniroute repair`.
2. Der Start bricht mit „129 ausstehende Migrationen, Tracking-Tabelle
   vermutlich geleert" ab — auf einer **frischen** Datenbank ist das ein
   Fehlalarm. Umgangen mit `OMNIROUTE_MAX_PENDING_MIGRATIONS=0` in
   `~/.omniroute/.env`.
3. **Der wichtigste Fund:** Der Anbieter-Katalog (`omniroute providers
   available`, `omniroute keys add <id>`) zeigt Google als **`google`** an
   und lässt sich auch nur unter dieser ID anlegen. Der tatsächliche
   Routing-Code (`open-sse/config/providers/registry/gemini/index.ts`)
   kennt aber nur die ID **`gemini`** (eigener Auth-Header
   `x-goog-api-key`, nicht Bearer). Jeder Aufruf über `google/<modell>`
   scheitert deshalb — mal mit einer falschen Anbieter-Fehlermeldung
   („modal"), mal mit „no active credentials". Lösung: die Verbindung nicht
   über `omniroute keys add google ...` anlegen (wird zwar angenommen,
   funktioniert aber nie), sondern direkt per Management-API mit
   `"provider":"gemini"` — das ist ein Katalog-Bug, keine Fehlbedienung.

**Entscheidung, warum aufgegeben statt repariert:** Selbst nachdem alle
drei Bugs umgangen waren und Text-Chat nachweislich lief, blieb der
Kernnutzen aus — siehe „Einordnung" und „Bildgenerierung" unten. Ein
funktionierender direkter API-Aufruf ohne omniroute war in jedem
getesteten Fall einfacher als der Umweg über omniroute. Deshalb: Skript
und Hook raus, statt sie für ein Werkzeug zu pflegen, das keinen Vorteil
bringt.

**Funktionstest, Stand 17.08.:**
- Text-Chat über `gemini/gemini-3.5-flash` funktioniert — echte, korrekte
  Antwort erhalten.
- Bildgenerierung über `gemini/gemini-3.1-flash-image` ist technisch
  verdrahtet, lief aber beide Male in ein Rate-Limit
  („cooling down") — noch kein Bild tatsächlich erhalten.
- Die dedizierte Imagen-API (`imagen-4.0-*`) braucht laut omniroutes
  eigenem Code-Kommentar ein **kostenpflichtiges** Google-Cloud-Projekt;
  mit einem reinen Gratis-AI-Studio-Key ist von 403/Kontingent 0
  auszugehen.
- Einer der eingebauten „kostenlosen" Dritt-Anbieter-Wege
  (`tllm/gemini_2_0_flash`, läuft ohne eigenen Key über omniroutes
  Aggregatoren) scheiterte sofort mit 502 — passt zur bekannten
  Netzsperre. Nicht alle Dutzend durchgetestet, aber das Versprechen
  „dutzende kostenlose Tools" ist in dieser Umgebung mit Vorsicht zu
  genießen.

**Einordnung:** Der einzige tatsächlich funktionierende Pfad (eigener
Gemini-Key, Text-Chat) lief auch **direkt** gegen Googles API — ein simpler
`curl`/Python-Aufruf ohne omniroute, ohne Server, ohne Datenbank, ohne die
beiden oben genannten Bugs. Für den aktuellen Bedarf (ein Anbieter, ein
Schlüssel) ist omniroute Mehraufwand ohne klaren Gegenwert. Könnte sich
lohnen, sobald mehrere Anbieter gleichzeitig sinnvoll verwaltet werden
müssen — dafür bisher kein Bedarf.

**Bildgenerierung mit reinem Gratis-Key: fest bei Kontingent 0, kein
Zeitlimit.** Direkt bei Google getestet (`generativelanguage.googleapis.com`,
Modell `gemini-3.1-flash-image`), ganz ohne omniroute: `429, limit: 0,
model: gemini-3.1-flash-image`. Das ist kein Cooldown, der abläuft — der
Gratis-Tarif hat für Bildgenerierung ein **festes Kontingent von null**.
Warten hilft nicht. Nötig: ein Google-Cloud-Projekt mit **aktivierter
Abrechnung** auf demselben Schlüssel, dann steigt das Kontingent über 0.
Ohne Abrechnung bleibt nur Higgsfield (jetzt technisch wieder erreichbar,
seit die Netzsperre fällt, siehe oben) oder Gemini rein für Text.

### GitHub-Schreibzugriff — Sackgasse, Stand 17.08.2026

Ausführlich durchgesucht, kein selbst einstellbarer Schalter gefunden:
- `github.com/settings/installations` (**Installed GitHub Apps**): leer,
  bei `acydacy3` eingeloggt geprüft.
- `github.com/settings/applications` (**Authorized OAuth Apps**): „Claude"
  ist dort gelistet, aber Status **„never used"** — das ist nachweislich
  nicht der Weg, über den diese Sitzung liest (Lesen funktioniert ja).
- claude.ai-GitHub-Konnektor: zeigt nur allgemeinen Beschreibungstext,
  keine Repo-/Rechte-Detailansicht mit Umschalter.
- Repo-Ebene: selbst `list_repository_collaborators` (reiner Lesezugriff)
  scheitert mit **derselben** Meldung wie `git push`: „403 Resource not
  accessible by integration". Das deutet auf einen bewusst sehr eng
  gefassten Berechtigungssatz der GitHub-App hin, nicht auf eine
  Kleinigkeit, die sich in irgendeinem Menü umlegen lässt.

**Schluss daraus:** Das ist vermutlich serverseitig bei Anthropic
festgelegt, nicht etwas, das über GitHub- oder claude.ai-Einstellungen
selbst änderbar ist. Nächster Schritt wäre echter Support-Kontakt
(support.claude.com o. ä.), nicht weiteres Klicken durch Menüs. Bis
dahin bleibt: Ergebnisse am Ende der Sitzung als Datei zum Hochladen
schicken (siehe Kopf dieser Datei).

### TikTok über Buffer — eingerichtet 18.08.2026

**Kein eigener TikTok-App-Antrag nötig.** Die frühere Notiz, TikTok verlange
ein Prüfverfahren, gilt nur, wenn man **direkt** auf TikToks Content-Posting-API
aufbaut. Dienste wie Buffer haben die Prüfung selbst bestanden — man verbindet
dort nur sein TikTok-Konto per normalem Login.

| | |
|---|---|
| Konto | `acydacy3@gmail.com`, Organisation „My Organization" |
| TikTok-Kanal | **@mausigermax** |
| Zeitzone | Europe/Berlin (Buffer rechnet selbst um) |
| Gratis-Grenzen | **3 Kanäle, 10 geplante Beiträge je Kanal**, 1 API-Schlüssel, 3.000 Anfragen/30 Tage |

- Zugang läuft über **API-Schlüssel** (`publish.buffer.com/settings/api`), nicht
  über OAuth — der Schlüssel geht als `Authorization: Bearer …` an
  `https://mcp.buffer.com/mcp`. **Nie ins Repo**, das ist öffentlich.
- **Buffer holt Medien über eine öffentlich erreichbare Adresse.** Es nimmt
  über diese Schnittstelle keine Datei entgegen, nur einen Link. Drive-Dateien
  müssen deshalb auf „Jeder, der über den Link verfügt" stehen — sonst liefert
  Google **statt der Datei eine HTML-Anmeldeseite** aus, und Buffer bekommt
  Müll. Am 18.08. genau so gemessen: HTTP 200, aber 900 KB HTML statt Video.
- Die Zehner-Grenze ist der Grund, warum von elf Shorts einer wegfällt.

**Praxis, am 18.08.2026 mit zehn echten Beiträgen durchgeführt:**
- `create_post` braucht `channelId`, `schedulingType: "automatic"`,
  `mode: "customScheduled"` und `dueAt` als ISO-Zeit **mit Zeitzonen-Versatz**
  (`2026-08-18T11:30:00+02:00`). Buffer rechnet selbst nach UTC um.
- Das Video-Asset nimmt **ausschliesslich `url`** — dazu optional
  `metadata.thumbnailOffset` (Zeitpunkt fuers Cover) und `metadata.title`.
  **Ein Coverbild laesst sich gar nicht uebergeben.** Das bestaetigt
  unabhaengig, dass das TikTok-Cover aus dem Video kommt: unsere
  1280x720-Cover werden dort nicht gebraucht.
- Buffer holt das Video beim Anlegen **wirklich ab und analysiert es** —
  im angelegten Beitrag stehen danach `mimeType`, `durationMs` und ein
  selbst erzeugtes Vorschaubild. Ein leeres `durationMs` heisst: die URL
  war nicht erreichbar.
- **Vorsicht bei den Werkzeugnamen:** `get_post` erwartet `postId`,
  nicht `id`. Mit `id` kommt nur ein Validierungsfehler zurueck.
- **Drive-Freigabe ist Pflicht und `?usp=sharing` im Link beweist gar
  nichts** — das haengt Google beim Kopieren automatisch an. Entscheidend
  ist im Freigabe-Dialog der untere Block **„Allgemeiner Zugriff"**: von
  „Eingeschraenkt" auf „Jeder, der ueber den Link verfuegt" stellen.
  Solange das fehlt, liefert Drive bei jedem Abruf **HTTP 200 mit rund
  900 KB HTML** — Seitentitel „Google Drive: Sign-in". Der Statuscode
  taeuscht also; immer den Inhaltstyp pruefen.
- Abrufadresse fuer Buffer: `https://drive.google.com/uc?export=download&id=<ID>`
- **Nur den Unterordner freigeben, nie den Elternordner
  `Katastrophenprotokoll-Pipeline`** — dort liegt `ZUGANGSDATEN.txt` mit
  dem YouTube-Client-Secret.

**TikTok-Cover sind nicht die YouTube-Cover.** TikTok kennt kein Vorschaubild
im YouTube-Sinn: das Cover ist **hochkant (9:16) und wird aus dem Video selbst
gewählt**. Die 1280×720-Cover würden dort mit schwarzen Balken landen. Es gilt
also dieselbe Regel wie im Shorts-Feed — das stärkste Einzelbild des Clips ist
das Cover.

**`#shorts` auf TikTok ist wirkungslos** und verwässert nur die Einordnung.
Das Format erkennt TikTok an Seitenverhältnis und Länge.

### TikTok-SEO — Zwei-Agenten-Lauf vom 18.08.2026

Verfahren wie gehabt: zwei Agenten unabhängig, einer mit diesem Playbook,
einer ausdrücklich ohne, dann Gegenrede. Vier echte Widersprüche.

**Die Zahl, die alles einordnet.** Gemessen über 2,3 Mio. Beiträge aus
92.000+ Konten verteilen sich die Aufrufe so: **For-You-Feed 72,7 % ·
eigenes Profil 11 % · Hashtags 10 % · Suche 4 % · Following 2 %**.
Damit ist „TikTok-SEO" im Sinne von Suchoptimierung die **viertgrößte**
Quelle, hinter dem eigenen Profil. Die Bildunterschrift ist ein billiges
Nebengeschäft, keine Wachstumsstrategie — die ersten drei Sekunden im
Bild sind es. Nebenbei widerlegt: „Hashtags sind tot" ist falsch, sie
sind die einzige Quelle außer dem Feed, die gewachsen ist (+114 %).

**~~TikTok liest eingebrannten Text per OCR und indexiert ihn.~~**
Das wurde in dieser Sitzung zunächst als Tatsache behauptet — auch von
mir gegenüber dem Nutzer. **Es gibt keine Primärquelle dafür.** TikToks
einziges offizielles Dokument zum Empfehlungssystem ist vom 18.06.2020
und nennt nur Bildunterschriften, Sounds und Hashtags. Praktisch alle
Ratgeber behaupten es trotzdem. Die abgeleitete Taktik gilt aber in
beide Richtungen: **Die Bildunterschrift liefert, was im Voiceover nicht
vorkommt** (Genre, Ort, Jahr, Kategorie) — wird der Bildtext gelesen,
darf sie ihn nicht doppeln; wird er nicht gelesen, ist sie der einzige
Textkanal.

**`#chile` gehört NICHT unter deutschsprachige Clips.** Es ist auf
TikTok ein spanischsprachiger Pool. Chilenische Zuschauer im ersten
Testpublikum wischen bei deutschem Voiceover sofort weg, und Wegwischen
in der ersten Verteilungsrunde würgt die weitere Verteilung ab. Lösung
ohne Verlust: **„Chile" als normales Wort in die Bildunterschrift.**
TikTok indexiert Wörter, nicht nur Hashtags. Gleiches gilt für englische
Tags (`#mining`, `#survival`).

**Hashtag-Menge ist fast wirkungslos, Konstanz ist der Hebel.**
Normalisiert gegen den Median des jeweiligen Kontos: ohne Tags 0,975 ·
1–3 Tags 0,967 · 4–6 Tags 1,004 · 7+ Tags 1,069. Also rund **+4 % für
„überhaupt Hashtags"**. Der eigentliche Grund für feste Tags ist ein
anderer: **TikTok ordnet ein Konto anhand der ersten 5–10 Videos einem
Thema zu.** Deshalb vier feste Tags auf allen zehn Beiträgen
(`#doku #wahregeschichte #katastrophe #bergwerk`) plus einer, der
wechselt.

**Warnung zur Datenqualität:** Dieselben Rohdaten ohne Normalisierung
„zeigen", dass Hashtags 73-fach schaden — weil Mega-Creator ohne Tags
posten und Nischenkonten mit. Wer diese Rohzahl zitiert, misst
Kontogröße und nennt es Hashtag-Strategie. Solche Screenshots kursieren.

**`#fyp`:** Es gibt **keinen Primärbeleg**, dass TikTok sich je dazu
geäußert hätte — die überall zitierte „Bestätigung" existiert nicht.
Gemessen liegt `#fyp` sogar bei +16,7 %, aber das ist der Befund mit dem
größten Auswahlverdacht (Leute setzen ihn unter Videos, die sie ohnehin
für stark halten). Trotzdem weglassen: ein inhaltsleeres Tag verwässert
genau die Themenzuordnung, die ein neues Konto braucht.

**Eine Frage in der Bildunterschrift bringt +26,2 % Kommentare** — der
einzige Bildunterschrift-Effekt mit klarem zweistelligem Ausschlag in
großer Stichprobe. Aber nicht unter jedem Beitrag: bei einem nüchternen
Format wird es zur Masche, und unter Katastrophenbildern kippt es leicht
ins Pietätlose. **Zwei von zehn, nur auf technischen Rätsel-Momenten,
nie auf Leid.**

**Die Teilnummer gehört auf TikTok in die Bildunterschrift — ans ENDE.**
Das kehrt die YouTube-Regel um. Auf YouTube war „Teil 7 😮😦" ein Titel
*ohne Suchwort* — das war der Fehler, nicht die Zahl. Auf TikTok gibt es
kein Titelfeld, und bei null Followern ist der Profil-Tipp der einzige
Weg zu Teil 3. Ans Ende, damit niemand zuerst liest, dass er sechs Teile
verpasst hat.

**Weitere übertragene Grenzen:**
- Sichtbar sind vor dem „mehr" nur rund **70 Zeichen** (Quellen nennen
  80/100/125/140 — bei ≤70 ist man unter jeder Variante sicher).
  Die YouTube-Regel „vollständige Aussage bei Zeichen 35" gilt hier nicht.
- Caption-Grenze laut TikToks eigener API: **2.200 Zeichen**.
- Die YouTube-Benachrichtigungsdeckel-Regel (3/24 h) gilt auf TikTok
  **nicht** — TikTok hat keine solche Mechanik.
- Links in TikTok-Bildunterschriften sind nicht klickbar.

**Achtung, TikTok-Bedienoberfläche verdeckt unsere Untertitel.** Sie
liegt tiefer und weiter links als bei YouTube Shorts. Unsere
`MARGIN_V`-Werte sind für Shorts gebaut — für die TikTok-Fassung
anheben und die rechten ~15 % freihalten.

**Bewertungsfenster:** 96 % der Reichweite und fast 98 % der
Interaktionen fallen in die **ersten 10 Tage**. Nach 24 Stunden ist jede
Zahl Rauschen. Das schärft die bisherige Regel („frühestens Tag 4–5").

**Erwartungshaltung:** Marktweit sind die Aufrufe je Beitrag im
Jahresvergleich um **31 % gefallen**, bei 72 % mehr veröffentlichten
Videos. Wer mit 2024er-Werten rechnet, hält ein normales Ergebnis für
ein Scheitern.

**Zwei Maßnahmen außerhalb der Bildunterschrift, die mehr bringen:**
alle Clips einer Reihe in eine **TikTok-Playlist**, und die **Bio mit
Suchwörtern** füllen — das eigene Profil ist mit 11 % die zweitgrößte
Quelle, fast dreimal so groß wie die Suche.

**Offen und ungelöst:** Die Hashtag-Wahl stützt sich auf **YouTube-**
Volumen, nicht auf TikTok-Volumen — beide Agenten haben das unabhängig
als schwächsten Punkt markiert. TikTok Creative Center → Keyword
Insights (DE) wäre die Quelle, ist aber nur aus der App heraus abrufbar.

### Der Längenbefund, der unserer YouTube-Lehre widerspricht

Über vidIQ gezogen: zwölf deutschsprachige TikTok-Ausreißer im
Katastrophen-/Doku-Feld (Ausreißer-Faktor 18× bis 152× des
Kanalmedians). Laufzeiten 63–578 Sekunden, **Median rund 100 Sekunden,
kein einziger unter 60**. Unsere Shorts sind 19–39 Sekunden.

Das steht frontal gegen den YouTube-Befund „bis 22 s: Faktor 7,9"
(Abschnitt 4b). **Die YouTube-Längenlehre darf nicht nach TikTok
mitgenommen werden.**

Einschränkung, die beide Agenten selbst benannt haben: Die Stichprobe
ist auf Gewinner gefiltert (n=12, ≥10 K Aufrufe) und übergewichtet
systematisch, was ohnehin gewonnen hat. Sie beweist **nicht**, dass
kurze deutsche Doku-Clips scheitern.

**Billiger Test für Video 3:** das Langvideo für TikTok in zwei bis drei
Stücke à 90–150 Sekunden schneiden statt in zehn à 25 Sekunden.

**Risiko im Blick behalten:** TikToks Feed-Standards nennen
„Nachwirkungen einer Naturkatastrophe" ausdrücklich als eingeschränkt
verteilbare Kategorie. Unser Material ist erzeugtes Standbild ohne
Gewaltdarstellung, das Risiko ist gering — aber wenn ein Teil auffällig
wenig Reichweite bekommt, ist das der erste Verdacht, nicht der
Aufhänger.

---

## 4b. Gemessene Kanaldaten — Stand 17.08.2026

Erstmals über die YouTube-API gezogen, nicht geschätzt. 12 öffentliche
Videos, alle Tham Luang, alle vor der neuen Pipeline entstanden.

Länge → Aufrufe, chronologisch:
19s→442 · 28s→23 · 22s→175 · 28s→7 · 32s→14 · 339s→5 · 21s→196 ·
34s→170 · 19s→441 · 33s→9 · 18s→517 · 24s→49

| | n | Schnitt Aufrufe |
|---|---|---|
| **bis 22 s** | 5 | **354** |
| **über 22 s** | 6 | **45** |

**Faktor 7,9.** Jedes einzelne Video unter 22 s liegt über 175. Von den
sechs längeren liegen fünf unter 50 (Ausnahme: 34 s → 170).

**Was widerlegt wurde:**
- ~~Frühe Uploads bekommen den Schub, späte gehen leer aus.~~ Falsch.
  Das erste öffentliche Video holte 442, das drei Minuten später 23.
  Das **jüngste** Video ist mit 517 das beste. Auch die
  Benachrichtigungsgrenze (3/24 h) erklärt das Muster nicht.
- ~~Die neuen Tags haben den Sprung gebracht.~~ Nicht belegbar. Alle 12
  Videos haben Tags; die neueren haben 33–34 statt 27 und liegen im
  Schnitt **niedriger** (145 vs. 184).

**Offen:** Länge und Hook-Qualität lassen sich mit n=12 nicht trennen.
Die Analytics-API gibt Daten erst nach 2–3 Tagen frei — Studio zeigt
Echtzeitschätzungen, die API nur Abgeschlossenes. Der Wert, der es
entscheidet: **„Betrachtet vs. weggewischt"** pro Short. Unter 60 % =
Anfang trägt nicht, ab 75 % = gut.

**Achtung bei Prozent-Retention:** Sie hängt mechanisch an der Länge.
31 % von 18 s = 5,6 s; 14 % von 34 s = 4,8 s. Ein Anstieg der Prozentzahl
bei gleichzeitig kürzeren Videos ist teils Arithmetik, nicht besserer
Inhalt.

## 4c. Titel, Beschreibung, Thumbnails — Stand nach zwei Agentenläufen

### Titel-Bauform
**Kern (bis Zeichen 35, trägt die vollständige Aussage) + Trennstrich +
Genre-Anhang.** Der Anhang ist im Feed abgeschnitten, wird aber
indexiert. Beispiel:
`Ein Zettel aus 700 Metern Tiefe | Bergwerk Chile Doku`

- **`Grubenunglück` nie im Titel** — 0 Suchen bei Wettbewerb 51, und es
  bricht im Feed mitten im Kompositum ab.
- Starke Keywords für dieses Thema: **`Bergwerk`** (3.335),
  **`Bergbau`** (5.099), **`Doku`** (230.831), **`Katastrophe`** (9.927).
- Vorgabe des Nutzers: **jeder Titel trägt ein starkes Keyword.**
- Kein Emoji, keine Teilnummer im Titel (die steht als Leiste im Bild).

### Beschreibung
~300 Wörter sind vertretbar, aber **nur als Faktentext**. Aufbau:
Kopfzeile 115–125 Zeichen (das Einzige, was ein Mensch sieht) → zwei
Absätze Fließtext → Faktenblock mit Stichzeilen → Reihenhinweis →
Kanal-Boilerplate → 5 Hashtags (max. 60 Zeichen, die ersten drei
erscheinen über dem Titel).

- **Keyword-Häufung schadet.** 2–4× in 200–350 Wörtern ist die Decke.
  Länge durch wiederholte Suchbegriffe zu erzeugen ist der Fehlerfall.
- **Keine Kapitelmarken in Shorts** — dafür braucht es mindestens
  3 Kapitel à 10 s, bei 20 s unmöglich.
- **Kein Funnel-Block zum Langvideo.** Überlappung Shorts/Langform ~10 %,
  Related-Video-Konversion unter 1 %. Das Langvideo hat 5 Aufrufe.

### Thumbnails — die Zweiteilung
- **Format immer 1280×720 (16:9), auch bei Hochkantvideos.** Ein 9:16-
  Bild wird von YouTube in den Querformatrahmen gesetzt und erscheint als
  grauer Kasten. Dieser Fehler ist am 17.08. real passiert.
- **Im Shorts-Feed ist das Thumbnail unsichtbar** — Autoplay zeigt den
  ersten Videoframe. Sichtbar wird das Cover nur im **Kanal-Raster, in
  der Suche und in Abo-Kacheln**.
- Daraus: **Cover** trägt das volle Paket (Motiv, 2–3 Wörter riesig,
  **ein** rotes Element, Positionsziffer). Der **erste Videoframe**
  bleibt fast leer — jedes Overlay dort kostet die Sekunden, in denen der
  Hook landen muss.
- Der eigentliche Zweck der Cover: **die Reihe im Raster als Reihe
  lesbar machen.**
- **Ein rotes Element pro Bild.** Zwei heben sich gegenseitig auf.
- **Text nie im unteren Fünftel** — wird von der YouTube-Oberfläche
  verdeckt. Rechte ~12 % ebenfalls (Aktionsspalte).
- Text im Cover **nie aus dem Titel wiederholen** — verschenkt eine der
  zwei Flächen. Cover = Bild und Emotion, Titel = Keyword und Versprechen.
- **Warnung:** Es gibt eine KI-gestützte Prüfung auf irreführende
  Thumbnails, und Katastrophen-Inhalte sind genau das Feld. Ein Pfeil auf
  etwas, das im Video nicht vorkommt, ist ein Risiko, kein Trick.

## 4d. YouTube-API — was gemessen funktioniert

Erstmals produktiv genutzt am 17.08.2026. Alle Punkte unten sind
ausprobiert, nicht angenommen.

- **Terminieren funktioniert über die Schnittstelle.** `privacyStatus:
  private` **zusammen mit** `publishAt` (RFC3339, UTC) erzeugt denselben
  Zustand wie „Zeitplan" in Studio. Deutsche Zeit minus 2 Stunden = UTC
  (MESZ). Die Beschränkung für ungeprüfte Projekte hat **nicht**
  gegriffen — `publishAt` wurde bei allen 11 Uploads übernommen.
- **Resumable Upload** ist der zuverlässige Weg: erst POST mit den
  Metadaten und `X-Upload-Content-Length`, dann PUT der Bytes an die
  zurückgegebene `Location`.
- **`videos.update` ersetzt den kompletten Snippet.** Wer nur Tags
  setzen will, muss Titel, Beschreibung, `categoryId` und
  `defaultLanguage` **mitschicken**, sonst werden sie geleert. Erst
  `videos.list` lesen, dann vollständig zurückschreiben.
- **Thumbnails haben ein Tempolimit.** Nach etwa neun Uploads in Folge
  kommt `429 The user has uploaded too many thumbnails recently`.
  Kein Fehler — später erneut versuchen.
- **Analytics-API liefert nur abgeschlossene Daten**, Vorlauf 2–3 Tage.
  Studio zeigt Echtzeitschätzungen, die es über die Schnittstelle nicht
  gibt. Bei einem frischen Kanal kommen überall Nullen zurück, obwohl
  der Zugang funktioniert. Kein Konfigurationsfehler.
- **Data API und Analytics API sind getrennt freizuschalten**, auch im
  selben Google-Cloud-Projekt.
- Kontingent: 10.000 Einheiten/Tag, ein Upload kostet 1.600 → **rund
  6 Uploads pro Tag**.
- **Widersprüchliche Aufrufzahlen:** Summe der Videoaufrufe 2.048,
  Kanalstatistik meldet 966. Zwei verschiedene Zählungen. Prozentwerte,
  die darauf beruhen, sind mit Vorsicht zu behandeln.
- **JSON-Escape-Falle bei deutschen Anführungszeichen (19.08.2026 gelernt).**
  Beschreibungen mit typographischen Zitaten (öffnend `„`, schließend `"`) bringen
  `json.load` mit „Expecting ',' delimiter" zu Fall, wenn das schließende
  Zitatzeichen nicht als `\"` escaped wird — es ist derselbe Codepoint wie das
  JSON-String-Ende. Öffnendes `„` (U+201E) ist harmlos, nur das schließende
  `"` (U+201C, sieht wie ASCII `"` aus) muss geschützt werden. Warum das teuer
  war: der Bruch geschieht erst beim Einlesen der fertigen `configs/*.json`,
  also nach dem eigentlichen Fehler.

### Fertige Videos IMMER vor dem Hochladen nach Drive sichern

**Am 17./18.08.2026 teuer gelernt.** Die elf fertigen San-José-Shorts und ihre
Cover entstanden in einer Sitzung und wurden von dort direkt zu YouTube
hochgeladen — aber **nie nach Drive oder ins Repo gesichert**. Als sie einen
Tag später für TikTok gebraucht wurden, waren sie weg: der Container der
alten Sitzung war fort, und

- **die YouTube Data API hat keinen Download-Befehl.** Es gibt keinen
  API-Weg, ein hochgeladenes Video als Datei zurückzuholen — auch nicht
  als Kanalinhaber. Der einzige Weg ist der Herunterladen-Knopf in
  YouTube Studio, also Handarbeit im Browser.
- Auch die Artefakt-Seite („Upload-Protokoll San José") half nicht: sie
  enthält Titel, Beschreibung und Tags zum Kopieren, aber keine
  Dateipfade und keine Video-IDs.

**Regel ab sofort:** Jedes fertige Video und jedes Cover geht in den
Drive-Ordner `Katastrophenprotokoll-Pipeline`, **bevor** irgendetwas
hochgeladen wird. Benennung nach Teilnummer (`teil01.mp4`), damit die
Zuordnung später eindeutig ist. Der Container ist Wegwerfware — was nur
dort liegt, existiert morgen nicht mehr.

~~**Zweite Lehre, gleicher Tag:** `YOUTUBE_REFRESH_TOKEN` steht in den
Umgebungsvariablen auf dem unausgefüllten Platzhalter
`<refresh-token-aus-token.json>` — ein echter Token-Tausch gegen
`oauth2.googleapis.com` antwortet mit `invalid_grant`. Client-ID und
Secret sind gesetzt, das Token nicht.~~ **Überholt seit 18.08.2026:** Token ist
gesetzt und gültig (siehe Sektion 6, „Zugänge neu getestet"); Uploads/Analytics
funktionieren produktiv. Der Prüfpunkt bleibt trotzdem sinnvoll — wenn eine
Sitzung Kanalzugriff braucht und `invalid_grant` sieht, ist die Ursache
weiterhin: Platzhalter statt echtes Token in den Umgebungsvariablen.

### Zugang
OAuth-Client Typ **Desktop**, Weiterleitung `http://localhost:8765`.
Der OAuth-Zustimmungsbildschirm muss auf **„In Produktion"** stehen —
im Testbetrieb kommt `403 access_denied` für alle Konten, die nicht als
Testnutzer eingetragen sind, und der Dauerschlüssel verfällt nach
7 Tagen. Zugangsdaten liegen im Drive-Ordner, **nie im Repo** (öffentlich).

## 4e. Widerspruch der beiden Agenten — was sich durchgesetzt hat

Zweiter Durchlauf am 17.08. Wo sie sich uneinig waren, hat sich das hier
als richtig erwiesen oder ist zumindest besser begründet:

- **Der erste Videoframe IST das Thumbnail.** Bei rund 97 % Feed-Verkehr
  sieht kaum jemand das Cover. Die Empfehlung „ersten Frame leer lassen"
  ist falsch — er gehört zum stärksten Bild des Shorts gemacht. Was
  richtig gemeint war: keine statische Intro- oder Logokarte.
- **Kein Trennstrich-Anhang im Titel** (`… | Bergwerk Chile Doku`). Der
  Feed schneidet bei ~40 Zeichen ab, der Anhang fällt weg und kostet nur
  sichtbare Zeichen. Keyword in den natürlichen Satz.
- **Beschreibung 50–90 Wörter bei Shorts**, nicht 290. Die Begründung für
  lange Texte (KI-Zitationen) stützt sich auf Daten, bei denen **94 % der
  YouTube-Zitate an Langform gehen**, Shorts nur 5,7 %. Zitiert wird das
  Transkript, nicht die Beschreibung — ein 20-Sekunden-Short hat ~50
  Wörter Transkript. **Die lange Beschreibung gehört aufs Langvideo.**
- **Die Längenregel heißt nicht „unter 30 Sekunden", sondern „keine
  toten Sekunden".** Verdient ein 33-Sekünder alle 33 Sekunden, bleibt
  er. Hat er 6 Sekunden Leerlauf, fällt der Leerlauf — das ist kein
  verlorenes Erzählmaterial, das ist Polster.
- **Nicht nach Aufrufen bewerten, sondern nach Bindung.** Aufrufe sind
  das Ergebnis der Verteilungslotterie. Aussagekräftig ist der
  durchschnittlich angesehene Prozentsatz und die Kurve der ersten drei
  Sekunden.
- **Nicht wieder viele Videos in zwei Tagen.** Die ersten 12 sind schwer
  auszuwerten, weil alle 0–48 h alt sind. Gleichmäßiger Takt heißt
  vergleichbare Zeitfenster.
- **„0 Suchen" ist eine Meldeschwelle, keine Messung.** Deutsche
  Volumendaten sind dünner als englische. Kein Titel auf ein Wort mit
  0 bauen — aber ein gutes deutsches Wort auch nicht für tot erklären.

## 5. Stand

**Video 1** (Tham Luang, Höhlenunglück): veröffentlicht. 640 Aufrufe,
0,85 h Wiedergabezeit, 2 Abos. Langvideo 4,4 % Haltequote, Shorts
trugen. Diagnose: die ersten 5 Sekunden, in beiden Formaten.

**Video 2** (Grubenunglück San José, Chile): **fertig und geplant.**
11 Shorts (19–39 s) + Langvideo (5:04, 1080p). Alle 11 mit Titel,
Beschreibung, Cover, 33 Tags und Zeitstempel hochgeladen — 18.–20.08.,
je 11:30 / 14:30 / 18:30 / 21:30 deutscher Zeit.

Die Reihenfolge ergibt zufällig einen Test: 18. und 19.08. überwiegend
kurze Shorts (19–29 s), am 20.08. die drei langen (33, 34, 39 s).
Bricht der dritte Tag ein, trägt die Längenthese. Bricht er nicht ein,
war es der Hook — dann darf künftig länger erzählt werden.

Faktenlage geprüft: „aus Deutschland kommt Spezialtechnik" ist gedeckt —
Deutschland steuerte ein **Spezialseil** bei, das die Kapsel im Schacht
am Rotieren hinderte. Keine Neuaufnahme nötig. Bohrtechnik kam aus den
USA und Kanada, Winde und Umlenkrolle aus Österreich.

**Video 3** (Juliane Koepcke, LANSA-Flug 508): **fertig, hochgeladen,
terminiert 21.–24.08.2026, drei Shorts pro Tag.** 10 Shorts (19–33 s), alle
mit Karaoke-Untertiteln, Ken-Burns, Musikbett, „TEIL X"-Leiste; Hook-Banner bei
Teil 1/3/6/7/9. Video-IDs: 01 `bEN_1Q3n4P8`, 02 `-f3bMdBpnX0`, 03 `W1OZeKHFirU`,
04 `07uFJWU3Rv4`, 05 `4lX9vaked5I`, 06 `TznE6J_LAgA`, 07 `ctu63XO4TDs`,
08 `chnVmP2o_kI`, 09 `C-4gJfRmxw4`, 10 `u9M24Fh_oeE`. Titel-Score Short 1
(vidIQ): **74/100** („92 Passagiere. 1 Überlebende. | Doku") — als Kalibrierung
für spätere Titel notiert.

**~~Idee für Video 3: Lengede.~~ → Lengede ist Video-4-Kandidat.** Am 18.08.
zugunsten **Koepcke als Video 3** verworfen (siehe Sektion 6: „einzige
Überlebende" ist gerade das heiße Format, Koepcke ist Deutsche = nativer Anker).
Lengede bleibt stark, nur nicht zuerst. Die Fénix-Kapsel geht auf die
Dahlbuschbombe zurück (1955 Gelsenkirchen, 1963 Lengede). Für ein
deutsches Publikum ist Lengede ein Erinnerungsanker, San José keiner —
und es verbindet Video 2 und 3 zu einem Thema. Als Suchbegriff wertlos,
als Geschichte stark.

## 4f. YouTube-Audit — Stand 18.08.2026

> **Aktualisiert 19.08. (kostenloser API-Audit):** Der hier genannte Top-Short
> „18s → 885" ist **überholt** — neuer Bestwert **„33 Mann fahren ein. 700 Meter
> tief." (26s → 1.286)**, ein Fakten-Kalt-Einstieg. Bindung (AVP%): bestätigt,
> dass der **Hook entscheidet, nicht die Länge** (19s lieferte 113% UND 79%;
> 22s nur 56,8%). Retention <60% = Anfang trägt nicht. San José startet stärker
> als Tham Luang (1.286/502 am ersten Tag). Warum-Sektion für die Längen-Synthese:
> Sektion 6 („Beste Short-Länge"). defaultLanguage=de gesetzt (siehe Sektion 6/0).

**Tham Luang nach 3 Tagen, Kanal nach Launch:**

| | |
|---|---|
| Aufrufe | 2.686 |
| Abonnenten | 9 |
| Videos | 15 Shorts (alle Tham Luang) |
| Traffic-Quelle | 96,1% aus Shorts-Feed |
| YouTube-Suche | 1,9% (15 Aufrufe von 623) |
| Abo-Benachrichtigungen | 0,6% (5 Aufrufe) |

**Längenlehre — Widerspruch zu alten Daten:**

Die CLAUDE.md sagt: „unter 22 Sekunden: Faktor 7,9" (gemessen an 12 Vosk-Videos). Neue Messung mit vidIQ:

| | |
|---|---|
| Platz 1 | 18s → 885 Aufrufe |
| Platz 2 | 34s → 666 Aufrufe |
| Platz 3 | 19s → 469 Aufrufe |

**Der Aufhänger trägt mehr als die Länge.** Das beste Video ist nicht der 18-Sekünder, sondern der 34-Sekünder mit dem Hook „Katastrophe abgewehrt, Opfer gerettet!" Das schlägt alle kurzen Sätze. **Länge allein erklärt nicht die Streuung.**

Folgerung: San Josés Aufhänger sind dramatischer als Tham Luangs. Erwartet: bessere Performance, auch wenn manche Shorts 33–39 Sekunden dauern.

**Shorts-Feed trägt komplett.** Die 96,1% bestätigen, dass die Strategie „2 Shorts/Tag, Langvideo zuerst" aufgeht. Search spielt bei 9 Abos noch keine Rolle; ab ~50 Abos werden Benachrichtigungen messbarer.

**Wachstum ist exponentiell:** 0 → 628 → 817 → 1.241 Aufrufe pro Tag (Aug 15–18). Das ist typisches Launch-Verhalten. San José startet morgen in dieser aufgeheizten Umgebung.

**Nächste Messpunkte:**
- Nach San-José-Teil 2 (heute 11:30): Schau, ob Video live ist. Untertitel sichtbar? Cover korrekt?
- Nach 24 Stunden: Erste aussagekräftige Engagement-Zahlen.
- Nach 4–5 Tagen: Durchschnittliche Wiedergabequote via Analytics-API (Daten sind 2–3 Tage verzögert).

---

## 6. Sitzung 18.08.2026 (abends) — Video 3 gewählt, Werkzeuge, Bildlehren

> **Nachtrag 19.08.2026 abends:** Video 3 (Koepcke) ist inzwischen **fertig
> produziert, hochgeladen und terminiert** — siehe Sektion 5 für Video-IDs
> und Sendetermine. Diese Sektion 6 bleibt als Entstehungs-Protokoll (Auswahl,
> Bild-Engine-Tests, Prompt-Lehren) unverändert stehen.

### Zugänge neu getestet
- **YouTube-Refresh-Token ist jetzt ECHT und gültig.** Die alte Notiz
  (Platzhalter `<refresh-token…>`, `invalid_grant`) ist überholt: Token-Tausch
  gegen `oauth2.googleapis.com` liefert HTTP 200, Scopes `youtube` +
  `yt-analytics.readonly`, API-Beweis Kanal Katastrophenprotokoll (17 Videos,
  4.149 Aufrufe). Kanalzugriff steht ohne Fix.
- **GitHub-Push weiterhin 403 — Diagnose 18.08.:** Der Token dieser Web-Sitzung
  hat **nur Leserecht** (`Contents: Read`). Lesen (`get_me`, klonen) geht, jeder
  Schreibweg (git-Push, `GITHUB_PAT`, GitHub-MCP `create_branch`) gibt exakt
  `403 Resource not accessible by integration` — GitHubs Wortlaut für „Schreiben
  mit Nur-Lese-Integration". **Nicht in unserem Code.** Anders als der
  Refresh-Token (Wert in UNSERER Umgebung) sitzt dieses Recht in der
  GitHub↔Claude-Verbindung im Browser — nur der Nutzer kann es umlegen. Hebel,
  der Reihe nach: (1) **code.claude.com** → Environment/GitHub-Verbindung mit
  Schreibrecht neu autorisieren (wahrscheinlichster Ort, da dies eine
  code.claude.com-Sitzung ist); (2) **github.com/settings/installations** →
  Claude-App → Contents = Read **and write**, Repo freigegeben; (3) **claude.ai →
  Connectors → GitHub** neu verbinden. Nächster Schritt: Nutzer öffnet den Screen,
  zeigt ihn, dann millimetergenaue Anleitung. Bis dahin: Upload-Datei.

### Werkzeuge — Stand dieser Sitzung
- **claude-youtube-Skill: ERLEDIGT — als claude.ai-Skill hochgeladen (18.08.).**
  Liegt jetzt im Konto, lädt automatisch in jede Sitzung. Der beste Weg, NICHT
  das Repo. Quelle ist `github.com/AgriciDaniel/claude-youtube` (14 Sub-Skills,
  9 Guides; SKILL.md-name `youtube`). In keinem Marketplace. Als **Zip mit
  SKILL.md an der Wurzel** in claude.ai → Capabilities → Skills hochladen →
  liegt dann im Konto und **lädt automatisch in JEDE Sitzung** (auch Claude
  Code Web), genau wie `prompt-master`. Das umgeht die GitHub-403-Sperre und
  schliesst Regel Nr. 1 für Skills. `setup.sh` klont ihn zusätzlich als Fallback.
- **yt-dlp läuft — mit `deno` als JS-Runtime.** Untertitel, Metadaten und
  Thumbnails kommen sauber. **Aber Video-Streams sind auf Datacenter-IPs
  bot-gesperrt** („confirm you're not a bot") → bräuchten Login-Cookies, die
  wir nicht haben. Für Konkurrenzanalyse reichen Untertitel + Cover. `deno` +
  `yt-dlp` sind in `setup.sh` als Auto-Install.
- **Remotion 4.0.513 installiert** (Linux-Compositor da), bleibt hinter dem
  `--remotion`-Flag (400 MB, nur auf Wunsch). Für unsere Pipeline **kein Muss**:
  animieren/editieren macht ffmpeg (short.py/lang.py), „Video schauen" macht
  `videoblick.py`. editly und ein „video-use"-Paket ausdrücklich NICHT
  installieren (Wrapper ohne Gewinn bzw. Namens-Wirrwarr/Schadcode-Risiko).

### Video 3 = Juliane Koepcke (LANSA-Flug 508), NICHT Lengede zuerst
Kostenlose Recherche (YouTube API + Web, keine vidIQ-Credits) ergab:
- **„Einzige Überlebende / Flugzeugabsturz" ist gerade das heisse Format** —
  auch schon auf Deutsch: ein **4-Sekunden-Short** zu Koepcke macht 872k,
  Luftfahrtfaszination 515k, international It's Aviation 13,2 Mio (15s). Nachfrage
  bewiesen, Doku-Mehrteiler-Lücke offen. **Koepcke ist Deutsche → nativer Anker.**
- **Bergwerk/verschüttet = leeres deutsches Feld** (0 DE-Treffer in 6 Monaten).
  San José/Lengede bleiben unumkämpft — Lengede also weiter gültig, nur nicht zuerst.
- **Gegenbeispiel Humantary** („Das Mädchen, das vom Himmel fiel", 26 Min):
  nur 3.222 Aufrufe, keine Tags, Boilerplate-Beschreibung, Titel = Buchtitel ohne
  Suchwort. Bestätigt hart: **Shorts-first, Langvideo schlank, Länge tötet.**
- Skript-Entwurf (5-Min-Langvideo Kalt-Einstieg beim Sturz + 10 Shorts) steht,
  vom Nutzer freigegeben. Pilot = Short „Der Freifall".

### Bild-Prompts — was Seedream/Seedance/Higgsfield gelehrt haben (18.08.)
- **Alter ist der Knackpunkt.** Seedream/Higgsfield rutschen ins Kindliche
  ODER ins Erwachsene. Fix: Altersband hart einklemmen — „17-year-old teenage
  girl, clearly a teenager, NOT a young child and NOT an adult woman" UND beide
  Extreme in den Negativ-Prompt („child, little girl, toddler, adult woman,
  middle-aged").
- **Extreme-Close-up quetscht Hände und Gesicht zusammen** → das Modell legte
  die Gurtschnalle ans Gesicht statt in den Schoss. Fix: **Medium Shot
  (Hüfte–Kopf)**, Körperzonen ausdrücklich trennen („hands rest LOW in her lap …
  face high in the frame … she holds nothing near her face").
- **Kamera-/Licht-Kürzel schlagen Adjektive**: „40mm f/2, focus on the buckle,
  3:1 contrast, motiviertes Key (kaltes Fenster) + warmes Rim (Leselampe),
  Kodak Ektachrome 1971 fine grain/halation" steuert dichter UND kürzer als Prosa.
- **Figuren-Konstanz + Look-Suffix** über alle Bilder einer Reihe („the same
  17-year-old girl …", identisches Grading) → wirkt im Schnitt wie ein Film.
- **Fünf Bild-Engines an Bild A getestet (18.08., alle über Higgsfield):**

  | Engine | Cr. | Format | Wz. | Befund |
  |---|---|---|---|---|
  | **Z-Image** | **0,15** | **9:16 nativ** | nein | **Objektiv bestes Preis-Leistung: bestes Alter (klar 16–17, kein Kind), 9:16, kein Wasserzeichen, Vintage-Schnalle, cineastisch — für 0,15 Cr.** ~~Standard-Engine~~ **Nutzer-Entscheidung darunter überstimmt: nur Landschaft/Establishing (Bild D), Figuren via Nano Banana Pro/Seedance.** |
  | Seedream 5.0 Lite | 1 | 9:16 nativ | nein | Sehr sauber, 9:16, kein Wasserzeichen, Alter+Komposition ok. Solide Reserve. |
  | WAN 2.2 | 0,5 | 9:16 nativ | nein | Billig, aber **Gesicht zu kindlich** (Nutzer-Urteil 18.08.). Nicht für Menschen. |
  | Nano Banana Pro | 2 | wählbar | ja | **Nutzer-Favorit.** Beste Detailtreue: period-korrekte Vintage-Schnalle, Alter 17, Komposition top. Wasserzeichen fällt beim 9:16-Beschnitt weg. |
  | Higgsfield Auto | 2 | wählbar (9:16 möglich) | ja | **Beste Emotion** (echte Anspannung statt benommen), Vintage-Schnalle. (1:1 im Test war eine Einstellung, kein Engine-Nachteil.) |
  | Seedance | 2 | wählbar | — | **Nutzer-Favorit** (reicher Look). Bei einem Test zu kindlich → Alter im Prompt hart einklemmen. |
  | Higgsfield Cinema | 0,125 | — | nein | Verliest komplexe Szenen (Schnalle ans Gesicht) → nur einfache Establishing-/Landschaftsbilder. |

  **NUTZER-ENTSCHEIDUNG (18.08., maßgeblich): Nano Banana Pro + Seedance sind
  ideal** — sein Auge zählt, nicht die reine Wert-Rangliste. Beide 2 Cr/Bild →
  30er-Guthaben reicht für ~ein Video (10–15 Bilder). **Budget-Strecker:**
  Nano Banana Pro/Seedance für Figur/Hero-Shots (Gesicht, Emotion), **Z-Image
  (0,15 Cr.) für reine Landschaft/Establishing** (Bild D, Canopy) — da sieht man
  den Unterschied kaum → ~10 Cr/Video statt 30. (Z-Image bleibt objektiv bestes
  Preis-Leistung, aber der Nutzer bevorzugt den reicheren Look.) Für ein Hero-Bild, wo
  Requisit+Emotion perfekt sitzen müssen, einmalig Nano Banana Pro / Higgsfield
  Auto (2 Cr., Wasserzeichen fällt beim 9:16-Beschnitt weg). Budget 30 Cr.
  reicht damit locker für Langvideo + alle Shorts.
  **Emotion nachschärfen:** „quiet dread" allein rendert oft benommen — besser
  „jaw tense, brow furrowed, eyes wide with fear" (Higgsfield-Auto traf es so).
- **Der Medium-Shot-Fix funktioniert:** Pilot-Bild A ist damit durch. Dieselbe
  Kamera-/Licht-Sprache + Altersband + Körperzonen-Trennung auf B und C übertragen.
- **Negativ-Prompt-Pflichtblock:** `triptych, panels, collage, split screen,
  borders` (gegen Panel-Collage) + `child, adult woman` (Alter) + `hands near
  face, holding object to face, deformed hands, extra fingers`.

### Beste Short-Länge — Konsolidierung ALLER Gewinner-Daten (die verstreuten Befunde an einem Ort)

Die Längen-Frage stand bisher verteilt in 4b, 4e, 4f und beim TikTok-Block,
teils widersprüchlich. Hier der Gesamtstand:

**YouTube-Shorts — die Zahlen:**
| Quelle | Befund |
|---|---|
| Vosk n=12 (4b) | bis 22 s → Ø 354 Aufrufe · über 22 s → Ø 45. „Faktor 7,9" — ABER mit Hook-Qualität vermischt. |
| vidIQ-Audit (4f) | Bestes Video **34 s** (Hook „Katastrophe abgewehrt") → 666, dann 18 s → 885, 19 s → 469. |
| Koepcke-Recherche (18.08.) | 4-s-Short → 872k · 15 s (It's Aviation) → 13,2 Mio · 1:26 → 515k. |
| Humantary (Langform) | 26 Min → 3.222. Eigenes Langvideo → 5 Aufrufe. |

**Die Synthese (das gilt):**
1. **Der Hook entscheidet, nicht die Sekundenzahl.** Ein starker 34-Sekünder
   schlägt schwache Kurze. „Faktor 7,9" ist real, aber zum Teil, weil kurze
   Videos zum Punkt kommen — nicht weil Kürze an sich gewinnt.
2. **Sichere Zone: 19–39 s** (unser erprobtes Band). Innerhalb davon nicht nach
   Sekunden optimieren, sondern **tote Sekunden killen** — verdient jede Sekunde
   ihren Platz, bleibt sie; sonst raus. „Keine toten Sekunden", nicht „unter 30 s".
3. **Ultra-kurz (4–19 s) kann explodieren**, WENN der Hook ein vollständiger
   Neugier-Bogen ist (Koepcke 4 s → 872k). Als Teaser-Schiene brauchbar, aber
   riskant — kein Erzählbogen möglich.
4. **Langform ist für diesen Kanal Gift** (Humantary 26 Min → 3.222; eigenes
   Langvideo → 5). Langvideo ≤ 5 Min, bleibt Zweitschiene; **die Shorts tragen.**
5. **TikTok kehrt es um** (4f-TikTok-Block): Gewinner-Median ~100 s, **kein
   einziger unter 60 s**. YouTube-Längenregel NICHT nach TikTok mitnehmen.
   Für TikTok Langvideo in 2–3 Stücke à 90–150 s statt zehn à 25 s.

**Messgröße, die es wirklich entscheidet** (nicht Aufrufe): der durchschnittlich
angesehene Prozentsatz + die Kurve der ersten 3 Sekunden. Unter 60 % = Anfang
trägt nicht, ab 75 % = gut. Short frühestens Tag 4–5 (YT) / in den ersten 10
Tagen (TikTok) bewerten.

---

## 7. Schnitt-Protokoll — vor JEDEM Video-/Short-Schnitt anwenden (Regel des Nutzers, 19.08.2026)

Verbindliche Reihenfolge, sobald es an Schnitt/Export geht. Zweck: an alle
Audit- und Analyse-Erkenntnisse erinnern, kostenlos aktuell halten, keine
Claude-Limits/vidIQ-Credits verschwenden.

0. **Wissen laden (gratis):** Diese CLAUDE.md ist zu Sitzungsbeginn geladen —
   ihre Längen-, Hook-, Titel-, Caption-Learnings direkt nutzen, KEIN neuer
   Abruf nötig. Nur bei **echter** Unsicherheit: genau EIN kostenloser Check
   über die YouTube Data-/Analytics-API, vergleichen, weiter. **Nie vidIQ-
   Credits oder unnötige Claude-Limits VERSCHWENDEN — vidIQ nur auf Anfrage.**
   (Das meint WASTE, nicht Qualität — siehe Ressourcen-Prinzip Sektion 0:
   fordert der Schnitt vollen Einsatz, wird voll investiert.)
1. **Erinnern, was gewinnt:** Der **Hook entscheidet, nicht die Sekundenzahl.**
   Bester eigener Short: Fakten-Kalt-Einstieg „33 Mann fahren ein. 700 Meter
   tief." (26s → 1.286). Sichere Zone **19–39s**, darin **tote Sekunden killen**.
   Retention <60% = Anfang trägt nicht. YouTube-Länge NICHT nach TikTok (90–150s).
2. **Erste 3 Sekunden (wichtigster Hebel):** Kalt-Einstieg, keine Titelansage.
   Einstellung 1 = Detail, nie Totale, ~2–3s; erster harter Schnitt ≤ Sek 3.
   Öffnen mit Hook / offener catchy Frage / packendem Fakt. **Untertitel =
   Stimme** (Ton-aus-Zuschauer!). Ein zusätzlicher Hook-**Banner** darf optional
   etwas anderes sagen — testen, kein Muss (siehe Sektion Shorts-Dramaturgie).
3. **Titel:** EIN starkes Keyword, Aussage bis Zeichen 35. Kein spezifisches da →
   starke allgemeine Genre-Keywords (Doku 230k, Katastrophe 9,9k, Bergwerk 3,3k,
   Bergbau 5,1k, wahre Geschichte, Überlebende). Keine Teilnummer/Emoji im Titel.
4. **Virale Schnitt-Technik:** Pattern-Interrupt alle paar Sekunden; ALLE
   Grenzen auf echte Sprechpausen ≥0,42s; Tonart pro Short wechseln; „TEIL X"-
   Leiste; erster Frame = stärkstes Bild (IST das Feed-Thumbnail); Mehrfach-
   Ausschnitt (ein Bild → 3–5 Einstellungen).
5. **Captions (ASS-Karaoke, selbst laufendes Learning):** 104 bei 1080, aktives
   Wort gold 118%, Umbruch nach Breite (~15 Zeichen, Ziel 85–90%), Endzeiten auf
   nächster-Start−0,02s kappen, 21 Z/s, 45 Z/Zeile, PlayResX/Y gesetzt, .srt separat hoch.
6. **Nach dem Schnitt:** jede neue Erkenntnis (welche Länge/Hook/Caption besser
   lief) SOFORT in diese Datei — Regel Nr. 1, die nächste Sitzung baut darauf auf.


## 8. Persistente Werkzeuge — wiederverwendbare Skripte im Repo (Regel des Nutzers, 19.08.2026 abends)

**Kern-Regel:** **Jedes wiederverwendbare Skript kommt SOFORT ins Repo unter
`werkzeuge/` — und wird in Folge-Sitzungen NICHT neu geschrieben, sondern
benutzt oder verbessert.** Zuwiderhandeln = Blindflug in der nächsten Sitzung.

**Warum:** Der Container ist Wegwerfware — was nur im `/tmp` oder im
Container-Home liegt, ist beim nächsten Sitzungsstart weg. In dieser Sitzung
(19.08. abends) mussten vier Skripte neu gebaut werden, die es in ausgelaufenen
Container-Sitzungen schon einmal gab. Ergebnis: 15+ Minuten Blindflug + zu
Recht verärgerter Nutzer. Genau derselbe Fehler wie beim San-José-Verlust
(Sektion 4d, „Videos vor dem Hochladen nach Drive sichern") — nur diesmal für
Code statt Videos.

**Statuswarnung (Tiefen-Audit 19.08.2026 abends, per `curl` gegen
`raw.githubusercontent.com/acydacy3/twitchclipz/main/` verifiziert):**
Die vier Skripte sind vom Nutzer inzwischen ins Repo hochgeschickt worden
— aber **im Repo-ROOT, NICHT unter `werkzeuge/`.** Der Ordner `werkzeuge/`
existiert im Remote nicht (404); `transcribe_all.py`, `build_configs.py`,
`youtube_upload.py`, `upload_all.py` liegen direkt neben `short.py` etc.
Damit gilt für Folge-Sitzungen: **im Repo-Root suchen, nicht in
`werkzeuge/`.** Solange die GitHub-Push-Sperre steht (Sektion 6, „Zugänge
neu getestet"), lässt sich die Ordner-Umbenennung nicht per API machen —
entweder beim nächsten Neubau in `werkzeuge/` konsolidieren oder die
Namens-Konvention offiziell auf „im Repo-Root neben den v1-Skripten"
umschreiben. Warum die Konfusion: die Regel wurde am 19.08. abends
angelegt, BEVOR der Nutzer die Skripte hochlud — der Ordnername war
Wunschziel, nicht Realität.

**Die vier Skripte (Stand 19.08. abends Tiefen-Audit — Pfade im REPO-ROOT):**

| Skript | Zweck |
|---|---|
| `transcribe_all.py` | Alle Voiceover-MP3s eines Videos mit `faster-whisper small-de int8` transkribieren; Ausgabe pro Short als flache Wort-Liste (Format siehe Sektion 2) für `karaoke.py`. |
| `build_configs.py` | Aus Skript + Wort-Zeiten + Bild-Zuordnung die `configs/*.json` je Short erzeugen (Titel, Beschreibung mit korrekt escapten deutschen Anführungszeichen, Tags, Hook-Banner, Cut-Grenzen an Sprechpausen ≥0,42 s). |
| `youtube_upload.py` | Einen Short zu YouTube hochladen (Resumable Upload, `privacyStatus:private` + `publishAt` für Terminierung, siehe Sektion 4d). |
| `upload_all.py` | Wrapper: alle Shorts eines Videos mit Zeitplan hochladen (3/Tag, deutsche Zeit → UTC, siehe Sektion 4d). |

**Prüfen vor Neubau:** Wenn ein Skript gebraucht wird, ZUERST `ls
/home/user/twitchclipz/` (Repo-Root) + `grep`-Suche, ob es schon
existiert. Wenn ja: benutzen. Wenn nein und wiederverwendbar: neu bauen
UND ins Repo (Root oder `werkzeuge/`, konsistent zum Bestand), nicht ins
`/tmp`.

**Google Drive → lokal per `gdown` (19.08.2026 gelernt):** Für öffentlich
freigegebene Drive-Ordner (Freigabestufe „Jeder, der über den Link verfügt")
funktioniert `gdown --folder <URL> -O <outdir>` ohne Google-API-Setup, ohne
OAuth. Ist der Ordner nur eingeschränkt geteilt, liefert Drive HTML-Anmelde-
seiten statt Dateien (siehe Buffer-Notiz Sektion 4). `gdown` gehört in
`setup.sh` als Auto-Install; für den `Katastrophenprotokoll-Pipeline`-Ordner
weiterhin **nur Unterordner freigeben**, nie den Elternordner (dort liegt
`ZUGANGSDATEN.txt`).

---
