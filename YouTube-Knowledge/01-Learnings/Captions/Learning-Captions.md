---
type: learning
status: active
confidence: very high
domain: captions
created: 2026-08-24
updated: 2026-08-24
evidence_count: 4
tags: [learning, captions, untertitel, ass, karaoke]
---

# Learning: Untertitel (ASS-Karaoke)

## Current Learning
Untertitel spiegeln **immer die Stimme** (Ton-aus-Publikum). Technische Werte,
mehrfach an realen Fehlern kalibriert:

### Shorts (1080 Breite)
- **Größe 104.** 58 war zu klein (vidIQ bemängelt), 78 immer noch zu klein.
- Kontur 9, Schatten 5, aktives Wort **gold** (`&H0047D4FF`, ASS ist **BGR**) auf 118 % skaliert.
- **Umbruch nach Breite (~15 Zeichen), nicht nach Wortzahl** (Ziel 85–90 % Breite).
- **Überlappende Ereignisse** stapelt libass übereinander (Ruckel-Effekt) → Endzeiten hart auf `nächster Start − 0,02 s` kappen.
- `PlayResX`/`PlayResY` müssen gesetzt sein, sonst verschwinden die Untertitel.
- Lesegrenze: **21 Zeichen/Sekunde, 45 Zeichen/Zeile.**

### Breitbild (16:9, 1920)
- **76 Punkt, nicht 60.** (60 auf 1920 = 34 auf 1080 → dreimal zu klein; derselbe Fehler wie Video 1.) Dazu `MAX_CHARS 28`, `MAX_WORDS 5`, `MARGIN_V 105`.

### .srt separat hochladen
Eingebrannte Untertitel sind für YouTube Pixel, kein Text. **.srt-Datei
hochladen** — bei einem Kanal ohne Verhaltenssignale mehr wert als Titel,
Beschreibung und Tags zusammen. → [[Learning-SEO]].

## Datenformat für karaoke.py
`karaoke.py` liest Wort-Zeiten als **flache Liste** `[{"word":…,"start":…,"end":…}, …]`,
NICHT `{"words":[...]}`. Whisper-Ausgabe ohne `words`-Wrapper speichern, sonst
bricht der Renderer **stumm**.

## Scope
Alle Shorts (104) und Langvideos (76). TikTok: MARGIN anheben, rechte ~15 % frei
(Bedienoberfläche verdeckt) → [[Learning-Cross-Platform-TikTok]].

## Operational Implication
[[Schnitt-Protokoll]] Schritt 5.

## History
- 17.08.: Größe 104 (Shorts), 76 (Breitbild); Stapel-Bug; PlayRes.
- 19.08.: flache-Liste-Format für Whisper-Ausgabe.

## Related
[[Learning-Editing-Video]] · [[Learning-Hooks]] · [[Learning-SEO]]
