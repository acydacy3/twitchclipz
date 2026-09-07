# Katastrophenprotokoll — Operating Context

Diese Datei lädt automatisch zu Sitzungsbeginn. Sie ist der **Einstieg**, kein
Archiv. Das eigentliche Langzeitgedächtnis liegt im **Vault**
`YouTube-Knowledge/` — reiner Markdown-Ordner mit Detailwissen (Evidenz, Confidence,
Historie), navigiert über `[[Wikilinks]]` und `Grep`/`Read`.

---

## ⚠️ ZUERST: Bin ich auf dem aktuellen Stand? (15-Sekunden-Check)

**Vault-Stand prüfen** (JEDE Session, auch mitten in einer Serie):
```bash
git fetch origin main
git log --oneline main..HEAD   # Commits die noch nicht auf main sind
```
- Commits auf main fehlen → `git pull origin main` holen (neuer Container-Start)
- Commits NUR auf Feature-Branch → Vault veraltet! → am Session-Ende ZWINGEND auf main mergen (→ `Memory-Workflow.md`)

**`YouTube-Knowledge/` fehlt oder `analyse.py` fehlt?** → `git pull origin main`.

**Dann lesen (2 Schritte, reicht für 99% aller Sessions):**
1. `YouTube-Knowledge/00-System/Current-State.md` — operativer Stand, Zahlen, nächster Schritt.
2. Gezielt retrieven was die Aufgabe braucht: `01-Learnings/`, `09-Failures/`, `05-Decisions/`. **Nicht das ganze Vault lesen.**

> **Persistenz-Regel:** Vault-Änderungen (`YouTube-Knowledge/`, `CLAUDE.md`, `.claude/`) IMMER auf `main` pushen — nicht nur auf den Feature-Branch. Neuer Container klont `main`. Details: `YouTube-Knowledge/00-System/Memory-Workflow.md`.

---

## ⛔ Regeln sind ab 07.09.2026 erzwungen, nicht aufgeschrieben

**Der Befund:** Fünf Produktionsregeln galten schriftlich, keine einzige hatte
einen Prüfpunkt im Code. Alle fünf wurden gebrochen, während sie galten —
10 Shorts gingen mit falschen Untertiteln live, 5 terminierte Shorts waren
Standbild-Diashows, zwei Serien sind dauerhaft unbewertbar, und der ganze
Kanal lief 8 dB zu leise. Vollständig: [[Decision-Harte-Gates-statt-Prosa]] ·
[[Failure-Memory]] F-V9-A…E · [[Regel-Register]].

**Der Ablauf steht nicht mehr in einer Liste — er läuft:**

```
python3 tools/kp.py status      ← sagt, was JETZT dran ist. Zuerst ausführen.
python3 tools/kp.py schritte    ← die Reihenfolge mit Befehlen
```

`kp.py` liest den tatsächlichen Zustand von Platte und API. Es glaubt keiner
Notiz — auch dieser nicht. Der Sitzungsstart ruft es automatisch auf, in jedem
frischen Container. **Der Nutzer muss nichts mehr ansprechen.**

**Die Reihenfolge — jeder Schritt prüft seinen Vorgänger:**

| # | Schritt | Werkzeug |
|---|---|---|
| 1 | Messen | `tools/kp_metrik.py --snapshot` *(läuft automatisch beim Start)* |
| 2 | Skript aufnehmen | `tools/kp_skript.py <serie> --aus <datei-vom-nutzer>` |
| 3 | Vorher-Gate | `tools/kp_gate.py <serie>` |
| 4 | Rendern | das Build-Skript der Serie |
| 5 | Animationen messen | `tools/kp_anim_qc.py` |
| 6 | Nachher-Gate | `tools/kp_gate.py <serie> --nachher` |
| 7 | Ausliefern | Upload-Skript der Serie · `tools/kp_ersetzen.py` |
| 8 | Longform | `nb_lang.py <serie>` |

**Der Riegel** (`.claude/hooks/pre-tool-use.py`) hält Render und Upload mit
Exit-Code 2 an, solange das Gate rot ist, und blockiert jeden automatischen
TikTok-Post. Er ist nicht überredbar — deshalb muss niemand mehr daran denken.

**Alle Regeln stehen in `tools/kp_regeln.py`** und werden nach
`YouTube-Knowledge/00-System/Regel-Register.md` erzeugt. Eine Regel ohne Feld
`pruefung` erscheint überall als UNGEDECKT — im Gate, im Sitzungsbericht und
in der Notiz. **Neue Regel = neue Zeile dort, mit Prüffunktion.** Prosa in
einer Notiz zählt nicht mehr als Durchsetzung.

---

## 📌 Stehende Anweisung: Befunde werden festgeschrieben, nicht berichtet

> Nutzer, 07.09.2026: *„Solange alle Analysen, Diagnosen, Korrekturen und
> Lösungen für immer so notiert werden, dass ich sie nicht erwähnen muss, ist
> alles gut. Du sollst immer so vorgehen, mit der Intention."*

Ein Befund, der nur im Chat steht, ist mit dem Container weg. Deshalb gilt für
**jede** Analyse, Diagnose, Korrektur und Lösung — ohne Nachfrage, ohne
Ankündigung:

| Was entsteht | Wohin es gehört | Warum dorthin |
|---|---|---|
| Fehler / Ursache | `09-Failures/Failure-Memory.md` mit ID, Beleg, Root Cause, Fix, Rule | damit er nur einmal bezahlt wird |
| Regel daraus | `tools/kp_regeln.py` **mit Prüffunktion** | sonst ist sie wieder Prosa |
| Grundsatzentscheidung | `05-Decisions/` mit Confidence, Scope, History | damit das Warum überlebt |
| Gemessene Zahl | `07-Analytics/Observations.md` + Snapshot | damit sie widersprechen kann |
| Kalibrierung / Schwellwert | als Kommentar **im Code neben dem Wert** | eine Messung ist so gut wie ihre Kalibrierung |
| Geänderter Ablauf | `CLAUDE.md` + `Produktion-Pflichtliste.md` | damit die nächste Sitzung ihn findet |

Dann `git commit` **und Merge auf `main`** — ein neuer Container klont `main`.
Ablauf: `/merken`. **Regel R25 prüft, ob Code ohne Gedächtnis geändert wurde.**

---

## Die 6 Kern-Constraints

1. **Das Originalskript kommt IMMER vom Nutzer.** Kürzen/formen: ja. Erfinden: nein.
2. **Der Nutzer arbeitet nicht mit der Kommandozeile** → Ergebnisse als **Artifact-Seite** ausliefern.
3. **Zahlen schlagen Vermutungen.** `tools/kp_metrik.py` gewinnt gegen Notiertes —
   **AVP% (gesehener Anteil je Short) ist die einzige altersunabhängige
   Qualitätszahl.** Der alte Autonomie-Score war selbst vergeben und ist stillgelegt.
4. **n+1 — vor JEDEM Produktionsschritt:** `YouTube-Knowledge/00-System/Produktion-Pflichtliste.md` **lesen und abarbeiten** — alle in Pflichtliste §2 gelisteten Pflicht-Dateien (Learnings + Failure-Memory + Animation-Library), alle Werkzeuge, Konkurrenz-Check. Nicht ankündigen, einfach tun. Der Nutzer soll HF-Quota, Manim, Remotion, Stock-Bilder, SEO **niemals selbst ansprechen müssen**. **Selbst-Fortschritt ist Pflicht:** jede Reihe integriert autonom **≥1 neue kostenlose Fähigkeit** (Capability-Gate §0c) und **prüft das fertige Rendern per Selbst-QC — ansehen (`videoblick.py`) + hören (`hoeren.py`) — vor jedem Upload** (§0d). Ohne diese zwei Riegel wiederholt sich V8 (Werkzeug war da, wurde nicht genutzt / Ergebnis nie geprüft).
   - **STEHENDE REGEL (verschärft 06.09.): Bewegtbild in JEDEM Short — Standbild-Diashow ausnahmslos raus.** Nicht mehr „≥1 Schlüssel-Shot", sondern **echte Bewegung in jedem Short und möglichst jedem Shot**: Bewegung in Sekunde 1 + durchgehend bewegte Shots. Genutzt wird das **volle Engine-Repertoire**: **video-shotcraft** (Remotion-Motion/Kinetic-Typo/2.5D-Kamerafahrten/Beat-Cuts), **OpenMontage HyperFrames (GSAP)** für bewegte Erklär-Shots, **video-use** für Schnitt/Grade/Overlay, dazu Manim/Wan2.1-I2V/SVG. **Ken-Burns-Zoom über Standbilder zählt NICHT als „bewegt".** Blockierend im §0d-QC. **Das muss geübt werden, bis es in jedem Short sitzt** (Nutzer 06.09.: „das muss langsam sitzen, weg vom Standbild"). Autonom — der Nutzer spricht das nie an. Details: [[Short-Konzept-Blueprint]], Pflichtliste §5, [[Werkzeug-Register]] §H.
5. **Ein Learning ist nicht automatisch eine Rule.** Confidence sichtbar lassen (Low/Medium/High/Very High).
6. **Erkenntnisse persistieren:** `git add/commit/push` — **Push ist freigeschaltet**. Ablauf: `/merken`.

## So arbeitet dieses System (Kurzfassung)
- **Ziel ist bessere Entscheidungsqualität je Produktionszyklus**, nicht mehr Output → `YouTube-Knowledge/00-System/Mission.md`.
- **Epistemik:** Observation → Hypothesis → Experiment → Result → Learning → Rule; Widersprüche werden bewahrt, nicht überschrieben → `.../Knowledge-Architecture.md`.
- **Leitplanken (Vorrang):** `.../Guardrails.md` — u. a. #1 Bestehendes schützen, #8 minimale Komplexität (neue Agenten nur, wenn der #8-Test sie rechtfertigt), #9 bei irreversiblen Änderungen erst analysieren + vorschlagen.

## Einstiegspunkte im Vault
- **Start / Karte:** `YouTube-Knowledge/HOME.md`
- **Nordstern-Ziel (messbar):** `YouTube-Knowledge/00-System/Ziel-YPP-Monetarisierung.md` — YPP: 1.000 Abos + 10 Mio Shorts-Views/90 Tage. Fortschritt jede Session loggen.
- **Aktueller Stand:** `YouTube-Knowledge/00-System/Current-State.md`
- **Was tun bei Session-Start / -Ende:** `YouTube-Knowledge/00-System/Memory-Workflow.md`
- **Vor jedem Schnitt:** `YouTube-Knowledge/00-System/Schnitt-Protokoll.md`
- **Learnings** (Hooks, Retention/Länge, Captions, Titel, SEO, Bilder, TikTok …): `YouTube-Knowledge/01-Learnings/`
- **Gescheiterte Ansätze** (nicht wiederholen): `YouTube-Knowledge/09-Failures/Failure-Memory.md`

## Kanal in einem Satz
Deutscher Faceless-Kanal *Katastrophenprotokoll* (`UC1KCzLNlgGiYsLNQ7Z0HA-g`),
Nische Katastrophen nüchtern erklärt, Vorbild *Fascinating Horror*. Takt: alle 48 h
ein Langvideo (~5 min) + täglich 2–5 Shorts; **die Shorts tragen**.

## Pipeline (Skripte im Repo-Root)
`transcribe_all.py`/`transcribe_vosk.py` → `align.py` → `pauses.py` → `bildcheck.py`
→ `karaoke.py` → `musik.py` → `short.py` → `serie.py` → `lang.py` → `videocheck.py`;
dazu `build_configs.py`, `youtube_upload.py`, `upload_all.py`, `analyse.py`.
**Wahrnehmung (Claude selbst):** `hoeren.py` (faster-whisper — Tonspur/Video hören, für QC/Transkript-Abgleich) · `videoblick.py` (Video in Einzelbilder zerlegen → mit Read ansehen).
Details + Werkzeug-Regel: `YouTube-Knowledge/00-System/Agent-Architecture.md`.

## Zusatz-Werkzeuge — AUTONOM einsetzen (installiert, 0 Token)
Nicht nur vorhanden, sondern **in jeder Produktion selbstständig nutzen** (Details: `YouTube-Knowledge/00-System/Werkzeuge-Installiert.md`):
- **Animation-Upgrade Manim:** `manim -qh -r 1080,1920 tools/manim_scenes.py CrossSection` → Querschnitt/Zeitleiste/Karte als `{"clip":...}` in `short.py`. **Standard-Weg für Erklär-Animation.**
- **SEO/Themen:** `tools/nb_suggest.py "<q>"` (YT-Keywords) · `tools/nb_trends.py "<kw>"` (Trends).
- **Bilder:** `tools/nb_openverse.py "<q>" <dir>` (CC-Pool) · `tools/nb_upscale.py in out --cutout c.png` (schärfen/freistellen).
- **Scratch-VO (Timing vor finaler VO):** `tools/nb_tts.py "text" out.mp3` (Piper de).
- **Ziel messen:** `tools/nb_views90.py` (90-Tage-Views → YPP-Log).
- **Ganze Pipeline:** Skill **`/video`**.
- **VOLLES Repertoire (MCP-Konnektoren + Skills + Tools + Engines): `YouTube-Knowledge/00-System/Werkzeug-Register.md` — bei JEDER Produktion konsultieren, je Bedarf wählen (kostenlos zuerst).**

## Am Ende jeder Sitzung
Neue Erkenntnisse in die passende Vault-Note (mit Confidence + Scope + Historie),
dann `git add/commit/push`. Ablauf: `YouTube-Knowledge/00-System/Memory-Workflow.md`
(bzw. `/merken`). Prüfen, ob daraus eine Rule wird → dann `Current-State.md`/diese Datei anpassen.
