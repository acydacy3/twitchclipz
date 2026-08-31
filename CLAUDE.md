# Katastrophenprotokoll — Operating Context

Diese Datei lädt automatisch zu Sitzungsbeginn. Sie ist der **Einstieg**, kein
Archiv. Das eigentliche Langzeitgedächtnis liegt im **Obsidian-Vault**
`YouTube-Knowledge/` — dort steht das Detailwissen mit Evidenz, Confidence und
Historie. **Öffne `YouTube-Knowledge/` als Vault in Obsidian**, um Links/Graph zu nutzen.

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

## Die 6 Kern-Constraints

1. **Das Originalskript kommt IMMER vom Nutzer.** Kürzen/formen: ja. Erfinden: nein.
2. **Der Nutzer arbeitet nicht mit der Kommandozeile** → Ergebnisse als **Artifact-Seite** ausliefern.
3. **Zahlen schlagen Vermutungen.** `analyse.py` gewinnt gegen Notiertes.
4. **n+1 — vor JEDEM Produktionsschritt:** `YouTube-Knowledge/00-System/Produktion-Pflichtliste.md` **lesen und abarbeiten** — alle 15 Pflicht-Dateien (13 Learnings + Failure-Memory + Animation-Library), alle Werkzeuge, Konkurrenz-Check. Nicht ankündigen, einfach tun. Der Nutzer soll HF-Quota, Manim, Remotion, Stock-Bilder, SEO **niemals selbst ansprechen müssen**. **Selbst-Fortschritt ist Pflicht:** jede Reihe integriert autonom **≥1 neue kostenlose Fähigkeit** (Capability-Gate §0c) und **prüft das fertige Rendern per Selbst-QC — ansehen (`videoblick.py`) + hören (`hoeren.py`) — vor jedem Upload** (§0d). Ohne diese zwei Riegel wiederholt sich V8 (Werkzeug war da, wurde nicht genutzt / Ergebnis nie geprüft).
   - **STEHENDE REGEL (31.08., bis zum nächsten Learning): Bewegtbild-Pflicht für Hook & Retention.** Jeder Short öffnet mit **Bewegung in Sekunde 1** und nutzt das **volle kostenlose Bewegtbild-Repertoire** (Manim · **Remotion** · **Wan2.1-I2V** · SVG) — nie reine Standbild-Diashow. ≥1 bewegter Schlüssel-Shot je Short, blockierend im §0d-QC. Autonom — der Nutzer spricht das nie an. Details: [[Short-Konzept-Blueprint]], Pflichtliste §5.
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
