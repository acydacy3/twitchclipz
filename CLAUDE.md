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

### Die Netzsperre — vollständig geklärt

Die Umgebung heißt **„Default — trusted network access"**
(`env_01BD8vQ6WzwWTY1m1wUrAzj1`, angelegt 14.08.2026). Der Name führt in
die Irre: es ist eine **Gästeliste, kein Türsteher** — nur ausdrücklich
gelistete Hosts kommen durch, alles andere fällt automatisch raus. Der
Proxy meldet dazu `gateway answered 403 to CONNECT (policy denial)`.

Das erklärt das Muster: `googleapis.com` geht, `youtube.com` nicht —
beide gehören Google, aber nur einer steht auf der Liste.

**Wichtig:** Die Sperre hat nichts mit den Berechtigungen zu tun, die der
Nutzer im Chat erteilt. Sie sitzt eine Ebene tiefer, zwischen Container
und Internet. Sie wird **nur** durch eine andere Netzwerkrichtlinie der
Umgebung gelöst (claude.ai/code → Environments → Network access).
**Niemals umgehen** — die Proxy-Anleitung sagt ausdrücklich: melden,
nicht umleiten.

| erreichbar | gesperrt |
|---|---|
| `github.com` · `pypi.org` | `youtube.com` · `reddit.com` |
| `www.googleapis.com` | `trends.google.com` · `wikimedia.org` |
| `youtube.googleapis.com` | `api.elevenlabs.io` · `higgsfield.ai` |
| `youtubeanalytics.googleapis.com` | `graph.facebook.com` · `graph.instagram.com` |
| `oauth2.googleapis.com` | `open.tiktokapis.com` · `www.tiktok.com` |
| `generativelanguage.googleapis.com` | `mcp.exa.ai` · `r.jina.ai` · `transcriptapi.com` |
| WebSearch (anderer Weg) | `pixabay.com` · `freesound.org` · `api.openai.com` |
| | `api.buffer.com` · `api.blotato.com` |

**Konsequenz:** Solange die Richtlinie steht, ist der **gesamte
Google-Stapel die einzige offene Tür** — und zugleich die einzige, die
zählt: Data API (Recherche), Analytics API + OAuth (die Retentionskurve,
die uns fehlt), Gemini (Bilder als Notlösung). ElevenLabs und Higgsfield
**nicht bezahlen**, solange sie gesperrt sind — das Geld wäre wirkungslos.

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

---

## 5. Stand

**Video 1** (Tham Luang, Höhlenunglück): veröffentlicht. 640 Aufrufe,
0,85 h Wiedergabezeit, 2 Abos. Langvideo 4,4 % Haltequote, Shorts
trugen. Diagnose: die ersten 5 Sekunden, in beiden Formaten.

**Video 2** (Grubenunglück San José, Chile): **fertig produziert.**
Voiceover 5:07, 10 Bilder → **11 Shorts** (18–38 s, alle −13,6 bis
−14,3 LUFS, yuv420p) **+ Langvideo** (5:04, 1080p, 52 Einstellungen,
Schnitt alle 5,8 s, −14,1 LUFS). Skript auf 4720 Zeichen gekürzt, vier
Sachfehler korrigiert. SEO-Paket liegt als Artifact-Seite vor.

Faktenlage geprüft: „aus Deutschland kommt Spezialtechnik" ist gedeckt —
Deutschland steuerte ein **Spezialseil** bei, das die Kapsel im Schacht
am Rotieren hinderte. Keine Neuaufnahme nötig. Die Bohrtechnik kam aus
den USA und Kanada, Winde und Umlenkrolle aus Österreich.

**Idee für Video 3: Lengede.** Die Fénix-Kapsel geht auf die
Dahlbuschbombe zurück (1955 Gelsenkirchen, 1963 Lengede). Für ein
deutsches Publikum ist Lengede ein Erinnerungsanker, San José keiner —
und es verbindet Video 2 und 3 zu einem Thema. **Als Suchbegriff
wertlos** (0 Suchen), als Geschichte stark.
