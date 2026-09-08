---
type: system
title: Regel-Register
status: active
updated: 2026-09-07
tags: [system, regeln, durchsetzung, generiert]
---

# Regel-Register — erzeugt aus `tools/kp_regeln.py`

> **Diese Datei wird erzeugt, nicht von Hand gepflegt.**
> `python3 tools/kp_regeln.py --markdown > YouTube-Knowledge/00-System/Regel-Register.md`
>
> Der Grund: Bis zum 07.09.2026 standen die Regeln in Prosa und die
> Durchsetzung nirgends. Ein Commit durfte „pipeline-weit erzwungen" heissen,
> ohne eine Zeile Code zu aendern. Jetzt ist die Liste ein Abbild des Codes —
> sie kann nicht mehr behaupten, was das Programm nicht tut.

**Deckungsgrad: 26 von 28 Regeln haben einen Pruefpunkt (93%).**

## Vor dem Render

*Aus Skript, Shot-Konfiguration und Metadaten. Blockiert per `kp_gate.py <serie>`.*

| ID | Regel | Prüfpunkt | Entstanden aus |
|---|---|---|---|
| R01 | Kein Text ist ein Skript, solange seine Herkunft nicht per Pruefsumme belegt ist. | `p_herkunft()` | F-V9-A — prosperi/nb_transcribe.py schrieb ASR nach skripte/short_XX.txt |
| R02 | Caption-Woerter kommen aus dem Nutzer-Skript, ASR nur fuers Timing. | `p_captions()` | F-V8-E / F-V9-A — „Marathon des Apples" statt „Sables", live in 10 Shorts |
| R03 | Sekunde 1 ist bewegt. Ken-Burns ueber ein Standbild zaehlt nicht. | `p_hook_bewegt()` | Short-Konzept-Blueprint 31.08. — virale Hits fahren ~90 % Bewegtbild |
| R04 | Mindestens ein echter Bewegtshot je Short (Manim/Remotion/I2V). | `p_bewegtshot()` | Bewegtbild-Pflicht 31.08. — 5 von 10 Ralston-Shorts verletzten sie unbemerkt |
| R05 | Mindestens 2 Bilder je Short, nie ein einzelnes Standbild. | `p_multishot()` | F-V8-A — alle 10 Shorts bestanden aus EINEM Ken-Burns-Clip |
| R06 | Musikbett db >= -18 (Ziel -16), sonst unhoerbar. | `p_musik()` | Nutzer-Befund 25.08. — V1-V5 hatten ein unhoerbares Bett |
| R07 | Kein Bild zweimal direkt hintereinander im selben Short. | `p_bild_dedup()` | Learning-Bilder-Prompts — globaler Dedup-Set je Produktion |
| R08 | Titel hoechstens 60 Zeichen, Aussage bis Zeichen 35 fertig. | `p_titel()` | Learning-Titel — CTR-Beleg |
| R09 | Kein Genre-Label („| Doku") und kein Emoji im Titel. | `p_titel_sauber()` | Competitor-Analyse 27.08. — kein Top-Performer nutzt Genre-Labels |
| R11 | Zielzone 19-49 s (intern belegt 19-39, A/B bis 49). | `p_laenge()` | Learning-Retention — n=44 intern belegt; Competitor-Zone nur Hypothese |
| R12 | Jede Serie hinterlegt ein Longform in metadata.json. | `p_longform()` | Pflichtliste §6 — 6 von 8 Serien haben bis heute keines |
| R21 | Untertitel spiegeln die gesprochene Stimme, kein abweichender Text. | **— ungedeckt** | Learning-Captions — abweichender Hook-Banner nur als Experiment |
| R22 | Schluesselmomente werden erzeugt, Establishing kommt aus Stock. | **— ungedeckt** | Learning-Bilder-Prompts |
| R24 | Kein fremdes Material im Schnitt: ref_*-Vorlagen bleiben Vorlagen. | `p_fremdmaterial()` | /video „Nie"-Liste — ralston/bilder/broll/ref_*.jpg sind echte Pressefotos |

## Am fertigen Video

*Gemessen an der Datei, nicht an der Absicht. Blockiert per `kp_gate.py <serie> --nachher`.*

| ID | Regel | Prüfpunkt | Entstanden aus |
|---|---|---|---|
| R13 | Das Video deckt das Voiceover (Abweichung < 1,5 s). | `p_render_dauer()` | Grundpruefung — faengt abgebrochene Renders |
| R14 | Untertitel decken mindestens 60 % der Laufzeit. | `p_untertitel_abdeckung()` | F-V9-D — leere Wortliste erzeugte Videos ohne Untertitel |
| R15 | Im fertigen Bild steht wirklich Schrift im Untertitel-Band. | `p_untertitel_im_bild()` | F-V9-D — der Build meldete „Captions aus Skript" bei 0 Untertiteln |
| R16 | Fortschrittsleiste sichtbar: >=18 px, gelb, kein Alpha. | `p_progressbar()` | F-V8-C — 10 px halbtransparent war auf dem Handy unsichtbar |
| R17 | „Kanal folgen" steht in den letzten Sekunden im Bild. | `p_cta()` | CTA-Overlay 27.08. |
| R18 | Gesamtlautheit im Band -20 bis -11 LUFS. | `p_lautheit()` | Learning-Editing-Ton — YouTube normalisiert auf ~-14 |

## Am Langvideo

*Gemessen an <serie>/render/long.mp4. Blockiert per `kp_gate.py <serie> --langform`.*

| ID | Regel | Prüfpunkt | Entstanden aus |
|---|---|---|---|
| R26 | Ein Langvideo ist mindestens 3 Minuten lang. | `p_longform_laenge()` | 6 von 8 Serien hatten am 07.09. gar keines; die zwei vorhandenen sind 4:29 und 5:39 lang |
| R27 | Ein Langvideo ist Querformat — Hochformat wertet YouTube als Short. | `p_longform_format()` | Longform bedient den Suchtraffic, nicht den Shorts-Feed |
| R28 | Langvideo im selben Lautheitsband wie die Shorts (-20 bis -11 LUFS). | `p_longform_ton()` | F-V9-G — der ganze Kanal lief bei -22 LUFS |
| R29 | Im Langvideo wechselt das Bild — mindestens ein Schnitt je 30 Sekunden. | `p_longform_bildwechsel()` | F-V9-O — nb_lang.py lieferte 5:55 aus EINEM Bild; Laenge, Format und Ton gingen alle gruen durch |

## Systemzustand

*Unabhaengig von einer einzelnen Serie.*

| ID | Regel | Prüfpunkt | Entstanden aus |
|---|---|---|---|
| R19 | Taeglich ein Analytics-Snapshot. Ein fehlender Tag ist dauerhaft verloren. | `p_snapshot()` | Befund 4 — V5 und V6 (20 Videos) sind ohne Ergebnis geblieben |
| R20 | Animationen fuellen das Bild und laufen nicht ueber den Rand. | `p_animationen()` | F-V9-E — jede Animation lief in einer 3x zu grossen Buehne |
| R25 | Jede Analyse, Diagnose, Korrektur und Loesung wird festgeschrieben — Code aendert sich nie ohne Vault. | `p_gedaechtnis()` | Stehende Anweisung des Nutzers 07.09.2026: „damit ich sie nicht erwaehnen muss" |
| R23 | TikTok wird NIE automatisch bespielt — der Nutzer laedt selbst hoch. | `p_tiktok_riegel()` | Beleg: Auto-Schedule = 1 View/Video, manuell = Tausende |

## Ungedeckt — bewusst als solche gefuehrt

Diese Regeln gelten, werden aber von keinem Programm erzwungen.
Sie stehen hier, damit die Luecke sichtbar bleibt statt zu verschwinden.

- **R21 Untertitel=Stimme** — Untertitel spiegeln die gesprochene Stimme, kein abweichender Text.  
  *Learning-Captions — abweichender Hook-Banner nur als Experiment*
- **R22 Schluesselszene** — Schluesselmomente werden erzeugt, Establishing kommt aus Stock.  
  *Learning-Bilder-Prompts*

## Related
[[Decision-Harte-Gates-statt-Prosa]] · [[Failure-Memory]] · [[Produktion-Pflichtliste]] · [[Current-State]]

