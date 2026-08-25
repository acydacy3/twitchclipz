---
type: learning
status: active
confidence: high
domain: bilder
created: 2026-08-24
updated: 2026-08-24
evidence_count: 4
tags: [learning, bilder, prompts, engines]
---

# Learning: Bild-Prompts (Engine-Wahl siehe Decision)

## Current Learning
Bild-Prompts werden **von Bild zu Bild detailreicher**. Kernregeln:
- Ganze Sätze, kein Stichwortsalat. **Hauptmotiv zuerst** (frühe Wörter wiegen schwerer). 80–90 Wörter.
- **Lichtrichtung und -härte immer nennen.**
- **Nationalität explizit** („Chilean", „Latin American") — sonst europäische Gesichter.
- **Keine Anführungszeichen im Prompt** — Text in Anführungszeichen wird als echter Text ins Bild gemalt. Für leere Schilder „blank".
- Querschnitte: **„single continuous image, no panel borders"** — sonst Comic-Panels.
- Gegen flaue Bilder: „most of the frame in deep black shadow", „clear crisp air, no atmospheric haze", ein Gesicht nah an der Kamera.
- **Bei neuem Sujet erst ein Bild, prüfen, dann den Rest.**

## Figur-Prompts (18.08. an Koepcke gelernt)
- **Alter hart einklemmen:** „17-year-old teenage girl, clearly a teenager, NOT a young child and NOT an adult woman" + Extreme in den Negativ-Prompt.
- **Medium Shot (Hüfte–Kopf)** statt Extreme-Close-up (quetscht Hände/Gesicht → Gurtschnalle landete am Gesicht). Körperzonen ausdrücklich trennen.
- **Kamera-/Licht-Kürzel schlagen Adjektive:** „40mm f/2, focus on the buckle, 3:1 contrast, Kodak Ektachrome 1971 fine grain/halation".
- **Figuren-Konstanz + Look-Suffix** über alle Bilder einer Reihe → wirkt im Schnitt wie ein Film.
- **Emotion nachschärfen:** „quiet dread" rendert oft benommen → „jaw tense, brow furrowed, eyes wide with fear".
- **Negativ-Prompt-Pflichtblock:** `triptych, panels, collage, split screen, borders` + `child, adult woman` + `hands near face, holding object to face, deformed hands, extra fingers`.

## Szenen-Budget pro Short (Nutzer-Regel 25.08.)
- **Pro Short 2–6 Szenen.** Claude **produziert nur die Schlüsselszene(n) per KI** (der eine Moment ohne Stock-Äquivalent);
  **der Rest wird IMMER aus dem Netz gezogen** (CC/Commons/Openverse-B-Roll, echte Umgebung). Default = Netz, KI = Ausnahme.
- **Web-Download funktioniert autonom (25.08. getestet):** Wikimedia-Commons-API-Suche + `curl` auf `upload.wikimedia.org`
  lädt frei lizenzierte Bilder (CC BY) direkt auf Platte; **Attribution mitschreiben** (Autor + Lizenz → Abspann/Beschreibung).
  Commons hostet auch CC-**Videos** (webm/ogv, direkt per curl). `yt-dlp` ist NICHT vorinstalliert (pip-installierbar), aber
  fremdes YouTube-/Nachrichtenmaterial bleibt tabu → CC-Quellen sind der saubere Weg.

## Creative-Director-Modus: Real vs. Generieren (pro Szene, 24.08.)
Bei jeder Szene **entscheiden, nicht beschreiben** — Claude liefert die Szenenliste als
Creative Director in einem Rutsch (pro Szene: Sek-Bereich + eins von zwei):
- **🎬 GENERIEREN** für Schlüsselmomente ohne Stock-Äquivalent (die Überlebende im Wrack,
  der Zettel aus 700 m Tiefe, ein Gesicht im Regen) → voller, tiefer Prompt nach den Regeln oben.
- **📹 ECHT** für Establishing-/Umgebungs-Shots (Dschungel, Höhle, Stollen, Meer) →
  generisches Stock-/Archiv-B-Roll. Billiger, glaubwürdiger, schneller.
- **Harte Grenze:** „Echt" = **generische Umgebung** aus Stock. Das **konkrete Ereignis /
  echte Personen** wird generiert oder nachgestellt — **nie** fremdes Nachrichtenmaterial
  (rechtlich sauber + Marke).

## z_image (Higgsfield/HF) — bewährte Prompt-Formel (24.08., n=10 Lengede, „unfassbar toll")
Reihenfolge, die konstant starke, kohärente Bilder liefert:
1. **Hauptmotiv + Handlung zuerst**, ganzer Satz („A narrow torpedo-shaped steel rescue capsule … suspended over a borehole at a 1963 mine, workers steadying it under floodlights at night").
2. **Licht + Palette explizit** („cold desaturated industrial palette", „harsh floodlights", „deep black shadow").
3. **Epochen-Anker** gegen Anachronismen („1963 period accurate, no modern objects") — hält Handys/Autos/Logos raus.
4. **Fester Stil-Suffix über die GANZE Serie** → Look-Konstanz (ein Modell, gleicher Suffix): `heavy film grain, cinematic, no text, no watermark`.
5. **Kamera-/Stimmungswörter** wirken stark (z_image ist „stylized/fast"): „close shot", „wide cinematic", „claustrophobic", „emotional".
6. **Inline-Negatives** reichen meist (`no text, no watermark, no modern objects`); kein separates Negativfeld nötig.
- **Betrieb:** z_image drosselt Parallel-Submits → **max ~3 gleichzeitig** (sonst HTTP 429), in Häppchen mit `jobs_wait` pacen. Kosten 0,15 Cr/Bild. Ergebnis-URLs sind öffentlich → per `curl` direkt auf Platte (kein base64).
- **Weiter optimieren:** je Bild EIN klarer Fokuspunkt; bei Figuren Nationalität/Alter + Medium-Shot (siehe Figur-Prompts oben); Serien immer im selben Modell halten (Koepcke-Lehre: Modellwechsel = Konstanzverlust).

## Counter Evidence / widerlegte Annahme
Siehe [[Failure-Vertikale-Staffelung-Triptychon]]: „vertikale Staffelung
(oben/Mitte/unten) beschreiben" erzeugt echtes 3-Panel-Triptychon. **Stattdessen**
eine Kameraeinstellung, Tiefe über „foreground/midground/background", drei
Ausschnitte per Crop (→ [[Learning-Editing-Video]] Mehrfach-Ausschnitt).

## Scope
Alle Bilder des Kanals. Engine-Wahl (Nano Banana Pro/Seedance/Z-Image): [[Decision-Bild-Engine-Wahl]].

## History
- 17.08.: Grundregeln (Nationalität, Anführungszeichen, Panels).
- 18.08.: Triptychon-Bug widerlegt; Figur-Prompt-Lehren (Alter, Medium-Shot, Kamera-Kürzel).
- 24.08.: Creative-Director-Modus — Real-vs-Generieren-Entscheidung pro Szene (Nutzer-Anweisung).
- 24.08. (Korrektur): **„Faceless" bezieht sich auf den ERSTELLER** (kein Gesicht vor der Kamera), **nicht auf den Content.** Bilder DÜRFEN/SOLLEN echte Gesichter mit Emotion zeigen — stärker als Silhouetten. Silhouette nur bewusst als Stilmittel.
- 24.08.: **z_image-Prompt-Formel** etabliert (Motiv→Licht→Epoche→fester Stil-Suffix; max 3 parallel) — Lengede-Serie „unfassbar toll", volle Look-Konstanz über ein Modell.
- 24.08.: **Z-Image Turbo via HuggingFace-Space = kostenlos, ABER tägliches ZeroGPU-Kontingent** (~8 Bilder/Tag auf Free, dann „ZeroGPU quota exceeded" bis Reset; HF-PRO = 25 Min/Tag). Default für Szenen-/Umgebungsbilder; higgsfield-Credits für schwierige Figuren aufsparen. **Bewährt (n=8):** rendert Gesichter UND Hände sauber; Prompt-Formel bestätigt — ganze Sätze, Kameraobjektiv (z. B. „35mm f/2.8"), Lichtrichtung, Nationalität explizit, Suffix „single continuous image, no panel borders, no text, no watermark". 9:16 = `864x1536`.

## Related
[[Decision-Bild-Engine-Wahl]] · [[Failure-Vertikale-Staffelung-Triptychon]] · [[Learning-Editing-Video]] · [[Video-03-Koepcke]]

## Autonome, PRÄZISE B-Roll-Suche (Nutzer-Regel 25.08.: Claude sucht alle Stock/Echt-Bilder selbst)
- **Quelle:** Wikimedia Commons über **kuratierte Kategorien** (`list=categorymembers`), NICHT Freitextsuche.
  Freitext zog Fehltreffer („Nick Cave"-Musiker bei „cave", Schneckenhäuser, Schlüssel). Kategorien sind topisch sicher.
- **Trotzdem QC:** Kategorien leaken vereinzelt (Schlüssel in `Category:Carabiners`). Deshalb **immer Kontaktabzug** (`montage` aller Bilder, EIN Blick) → Ausreißer gezielt löschen + aus besserer Kategorie nachziehen. Skript: `nuttyputty/nb_fetch_broll.py` (robust: Magic-Byte-Check, Retry, Resume, Negativ-Wortfilter).
- **Bewährte Kategorien:** Cave passages, Cave interiors, Caving, Cave rescue, Mine rescue, Single Rope Technique, Slot canyons, Caves of Utah, Carabiners, Climbing equipment, Memorial plaques.
- **Standortpräzision:** „Caves of Utah" traf „natural cave near Green River, Utah" — Standort matcht. Immer lokale Kategorie mitnehmen.
- **Resize:** `convert IN -resize 1600x2848^ -gravity center -extent 1600x2848` (short.py-Format). Attribution mitschreiben.

## KORREKTUR 25.08. (Nutzer): Schlüsselmomente WERDEN generiert — nicht überspringen
- **Fehler in V6 (behoben):** „HF gratis zuerst, Higgsfield begrenzt" wurde zu „gar nicht generieren" überinterpretiert → Schlüsselmomente mit generischem Stock ersetzt (irreführend). **HF-first ist eine Reihenfolge-Regel, KEINE Erlaubnis, das Generieren zu überspringen.**
- **Regel:** Die 🎬-Schlüsselmomente ohne Stock-Äquivalent IMMER per HF Z-Image (gratis, ~8/Tag) generieren, dann Higgsfield. In V6 nachgezogen: kopfüber im Spalt verkeilt (S5), Bein aus dem Fels (S6), kopf-voran über die Kante (S4), Seilriss (S9). z_image-Formel + `864x1536`; faceless-Illustration (kein Porträt realer Toter — rechtlich sauber, generische Person).
- **Bewährt (V6):** Z-Image liefert bei diesen Cave-Prompts dramatische, kohärente Bilder (nasser Fels, Helmlicht-Kegel, tiefes Schwarz) — deutlich stärker als Stock für den Kernmoment. Als **Hero-Bild (01)** in den Short, Stock als Deko dahinter.

## Referenz-getriebenes Generieren + HF-Quota voll nutzen (Nutzer-Regel 25.08.)
- **Vor dem Generieren IMMER viele echte Referenzen aus dem Netz ziehen** (Commons/Openweb) zum konkreten Fall/Szene: Geometrie, Körperhaltung, Fels-Textur, Lichtführung, Perspektive. **Studieren (Kontaktabzug), kreativ einfließen lassen, daraus lernen** — nicht blind aus dem Kopf prompten. Die Referenzen schärfen den z_image-Prompt (echte Details schlagen generische Adjektive).
- **HF Z-Image Tageskontingent VOLL ausnutzen** (~8/Tag gratis), wenn mehr/bessere Bilder helfen: mehrere Varianten pro Schlüsselmoment generieren, per Kontaktabzug das stärkste wählen. Erst wenn HF-Quota leer → Higgsfield (Credits). Nicht geizen, Qualität vor Sparsamkeit bei den Kernbildern.
- **Workflow je Schlüsselmoment:** (1) 5–8 echte Referenzen laden + ansehen → (2) Prompt aus den Referenzen bauen (Haltung/Licht/Textur konkret) → (3) 2–3 Varianten generieren → (4) beste per QC wählen → (5) als Hero-Bild setzen.
