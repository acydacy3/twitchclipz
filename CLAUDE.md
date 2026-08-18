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
- Voiceover: ElevenLabs (Nutzer). Bilder: Higgsfield Seedream 5.0 Lite
  (Nutzer, 1 Credit/Bild). Schnitt, Ton, Untertitel, SEO: hier.
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

Reihenfolge und Werkzeuge (alle im Projektordner `v2/`):

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

**Spracherkennung:** Vosk (`vosk-model-small-de-0.15`), nicht Whisper —
der Whisper-Modelldownload wird von der Netzsperre blockiert.
Vosk-Modelle über den GitHub-Spiegel `kercre123/vosk-models`.

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

### Bilder (Higgsfield Seedream 5.0 Lite)

- Ganze Sätze, kein Stichwortsalat. **Hauptmotiv zuerst** — frühe Wörter
  wiegen schwerer. 80–90 Wörter.
- **Vertikale Staffelung ausdrücklich beschreiben** (oben / Mitte /
  unten). Ohne sie gibt jedes Bild nur eine Einstellung her.
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

### Shorts-Dramaturgie

- **Auf Erzählgrenzen schneiden, nie mechanisch.** Video 1 hatte
  13 Stücke „eine Szene = ein Short" — 15–33 s, die irgendwo anfingen.
  Jeder Short braucht Aufhänger → Spannung → Auflösung/Cliffhanger.
- **Alle Grenzen auf echte Sprechpausen (≥ 0,42 s).**
- **Einstellung 1 ist ein Detail, nie eine Totale**, ~2–3 s. Erster
  harter Schnitt spätestens bei Sekunde 3.
- **Der Aufhänger-Text sagt etwas anderes als die Stimme.** Doppelte
  Information verschenkt einen Kanal.
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
- Kanal-Standardsprache und Themenkategorien waren **nicht gesetzt**.

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
| **YouTube Data API v3** | `googleapis.com` ist **erreichbar**. Freikontingent 10.000 Einheiten/Tag, nur API-Key, kein OAuth. **Der wichtigste offene Punkt.** |
| vidIQ (MCP) | **richtiger Kanal verbunden** (`UC1KCzLNlgGiYsLNQ7Z0HA-g`, „Katastrophenprotokoll", DE). Konto `kisha-ners@gmx.de`. Guthaben 170. Kostet Credits — sparsam, aber **ein gezielter Keyword-Abruf vor jeder Titelentscheidung lohnt sich immer**. |
| `YoutubeTags` (pip) | installiert; scrapt youtube.com → **hier blockiert**, auf dem PC des Nutzers nutzbar. Liefert Tags/Titel/Beschreibung fremder Videos. |
| `claude-youtube` Skill | installiert unter `~/.claude/skills/`, 14 Sub-Skills, 9 Playbooks. Als Subagent ohne unsere Regeln laufen lassen, damit er unabhängig urteilt. |
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
Gästeliste stand. Ob sich das jetzt lohnt, neu zu bewerten (z. B. Whisper
statt Vosk?), ist offen und nicht mehr durch die Netzsperre entschieden,
sondern durch echten Aufwand/Nutzen.

### Weitere geprüfte und verworfene Werkzeuge
- **`claudetube`** — nutzt yt-dlp, der README sagt selbst: „YouTube
  blocks all major cloud IPs".
- **`ZeroPointRepo/youtube-skills`** (521★) — läuft über
  `transcriptapi.com`, gesperrt.
- **Instagram/TikTok-Uploader** (alle unter 2 Sternen) — meist
  Browser-Automatisierung, bricht bei jeder Layout-Änderung und
  gefährdet das Konto. Dazu: Instagram nimmt **keine Dateien** entgegen,
  nur eine **öffentliche URL**; TikTok verlangt ein Prüfverfahren, ohne
  das nur private Entwürfe möglich sind.
- **Brauchbar, sobald die Sperre fällt:**
  `pauling-ai/youtube-mcp-server` — 40 Werkzeuge inkl. **Analytics API**.

### Bewusst NICHT installiert
- **`AgriciDaniel/claude-seo`** — 25 Skills, aber reines *Website*-SEO
  (Sitemap, Schema.org, hreflang, Core Web Vitals). Für einen Kanal ohne
  Website nutzlos. Brauchbar war genau eine Datei: die YouTube-Data-API-
  Referenz. Zurückholen, falls je eine Website entsteht.
- **`rediumvex/ai-video-generator-claude`** — Prompts für Seedance 2.0
  (Video), wir nutzen Seedream (Standbilder).
- **`Panniantong/Agent-Reach`** — kann genau, was fehlt, läuft aber über
  `mcp.exa.ai`/`r.jina.ai`, beide hier blockiert. Nur lokal sinnvoll.
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

**Zweite Lehre, gleicher Tag:** `YOUTUBE_REFRESH_TOKEN` steht in den
Umgebungsvariablen auf dem unausgefüllten Platzhalter
`<refresh-token-aus-token.json>` — ein echter Token-Tausch gegen
`oauth2.googleapis.com` antwortet mit `invalid_grant`. Client-ID und
Secret sind gesetzt, das Token nicht. Wenn eine Sitzung Kanalzugriff
braucht, ist das der erste Prüfpunkt, nicht der letzte.

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

**Idee für Video 3: Lengede.** Die Fénix-Kapsel geht auf die
Dahlbuschbombe zurück (1955 Gelsenkirchen, 1963 Lengede). Für ein
deutsches Publikum ist Lengede ein Erinnerungsanker, San José keiner —
und es verbindet Video 2 und 3 zu einem Thema. Als Suchbegriff wertlos,
als Geschichte stark.

## 4f. YouTube-Audit — Stand 18.08.2026

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
