# Katastrophenprotokoll — Operating Context

Diese Datei lädt automatisch zu Sitzungsbeginn. Sie ist der **Einstieg**, kein
Archiv. Das eigentliche Langzeitgedächtnis liegt im **Obsidian-Vault**
`YouTube-Knowledge/` — dort steht das Detailwissen mit Evidenz, Confidence und
Historie. **Öffne `YouTube-Knowledge/` als Vault in Obsidian**, um Links/Graph zu nutzen.

---

## ⚠️ ZUERST: Bin ich auf dem aktuellen Stand? (15-Sekunden-Check)
**`YouTube-Knowledge/` fehlt oder `analyse.py` fehlt?** → veraltet, `git pull origin main` holen.

**Dann lesen (2 Schritte, reicht für 99% aller Sessions):**
1. `YouTube-Knowledge/00-System/Current-State.md` — operativer Stand, Zahlen, nächster Schritt.
2. Gezielt retrieven was die Aufgabe braucht: `01-Learnings/`, `09-Failures/`, `05-Decisions/`. **Nicht das ganze Vault lesen.**

---

## Sofort wissen (die 6 wichtigsten Constraints)
1. **Das Originalskript kommt IMMER vom Nutzer.** Kürzen/formen aus vorhandenem Material: ja. Erfinden: nein.
2. **Der Nutzer arbeitet nicht mit der Kommandozeile** und kann **keine `.md`-Dateien öffnen** → längere Ergebnisse als **Artifact-Seite** ausliefern. (Ausnahme: das Vault liest er in Obsidian.)
3. **Zahlen schlagen Vermutungen, immer.** `analyse.py` gewinnt gegen Notiertes.
4. **Retrieval before Reinvention — n+1, IMMER:** vor jeder Produktion autonom das **komplette geprüfte Learning-Paket** ziehen (SEO, Schnittstile, Retention, Viral, geprüfte Theorien, Hooks, Captions, Bilder, Musik) — jedes Video baut auf allen vorherigen auf, nichts wird vergessen, jeder Schritt wird täglich besser. Nicht ankündigen, einfach tun.
5. **Ein Learning ist nicht automatisch eine Rule.** Unsicherheit sichtbar lassen (Confidence Low/Medium/High/Very High).
6. **Erkenntnisse persistieren:** am Session-Ende `git add/commit/push` — **Push ist freigeschaltet**, das Repo trägt den vollen Stand (der nächste Container klont ihn). Drive nur optional. Ablauf: `/merken`.

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
