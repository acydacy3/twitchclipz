# Katastrophenprotokoll — Produktions-Konstrukt

Diese Datei wird zu Sitzungsbeginn automatisch geladen. Sie ist das
Gedächtnis des Projekts: alles, was wir durch Versuch und Irrtum gelernt
haben, steht hier, damit es nicht in jeder neuen Sitzung neu erarbeitet
werden muss.

**Regel für dieses Dokument:** Erkenntnisse werden ergänzt, nie
überschrieben. Wenn eine Regel sich als falsch erweist, wird sie
durchgestrichen und begründet — der Irrweg ist Teil des Wissens.

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

---

## 4. Werkzeuge und Zugänge

| Werkzeug | Stand |
|---|---|
| **YouTube Data API v3** | `googleapis.com` ist **erreichbar**. Freikontingent 10.000 Einheiten/Tag, nur API-Key, kein OAuth. **Der wichtigste offene Punkt.** |
| vidIQ (MCP) | läuft, aber authentifiziert als `manokano3333@gmail.com`, **nicht** als `acydacy3@gmail.com`. Kostet Credits — sparsam. |
| `YoutubeTags` (pip) | installiert; scrapt youtube.com → **hier blockiert**, auf dem PC des Nutzers nutzbar. Liefert Tags/Titel/Beschreibung fremder Videos. |
| `claude-youtube` Skill | installiert unter `~/.claude/skills/`, 14 Sub-Skills, 9 Playbooks. Als Subagent ohne unsere Regeln laufen lassen, damit er unabhängig urteilt. |
| Google Drive | Ordner `Katastrophenprotokoll-Pipeline` (`1MFz5gNIBQfcXWBw8evnop_oUJ-9TnWtX`) |

### Was blockiert ist
`youtube.com`, `reddit.com`, `trends.google.com`, `wikimedia.org`,
`huggingface.co`, `pixabay.com`, `freesound.org`, `mcp.exa.ai`,
`r.jina.ai`. **Erreichbar:** `github.com`, `pypi.org`,
`googleapis.com`, WebSearch.

Die Netzsperre gehört zur Umgebung und wird beim Anlegen gewählt —
eine offenere Richtlinie löst das an der Wurzel, statt drumherum zu
bauen. Siehe code.claude.com/docs/en/claude-code-on-the-web.

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

**Video 2** (Grubenunglück San José, Chile): Voiceover 5:07, 10 Bilder,
11 Shorts + Langvideo. Skript auf 4720 Zeichen gekürzt, vier
Sachfehler korrigiert.
