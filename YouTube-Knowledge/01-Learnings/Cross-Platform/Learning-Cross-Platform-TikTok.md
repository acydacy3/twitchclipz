---
type: learning
status: active
confidence: medium
domain: cross-platform
created: 2026-08-24
updated: 2026-08-24
evidence_count: 3
tags: [learning, tiktok, cross-platform, buffer]
---

# Learning: Cross-Platform / TikTok

## Current Learning
TikTok folgt **anderen** Regeln als YouTube — die YouTube-Lehren dürfen **nicht
blind** übertragen werden. Quelle: Zwei-Agenten-Lauf 18.08. (n teils klein → Medium).

## Reichweiten-Verteilung (2,3 Mio Beiträge, 92k Konten)
For-You-Feed **72,7 %** · eigenes Profil **11 %** · Hashtags **10 %** · Suche **4 %** · Following **2 %**.
→ „TikTok-SEO" ist viertgrößte Quelle. Die **ersten 3 Sekunden im Bild** sind der Hebel.

## Übertragene / umgekehrte Regeln
- **Länge kehrt sich um:** Gewinner-Median ~100 s, **kein einziger < 60 s**. Für TikTok Langvideo in 2–3 Stücke à 90–150 s statt zehn à 25 s → Test. (Widerspricht [[Learning-Retention-und-Laenge]] — bewusst getrennt halten.)
- **Kein Titelfeld** → Teilnummer ans **Ende** der Bildunterschrift (kehrt YouTube-Regel um).
- **`#chile` NICHT** unter deutsche Clips (spanischsprachiger Pool → Wegwischen würgt Verteilung). „Chile" als normales Wort in die Caption.
- **Hashtag-Menge fast wirkungslos** (+~4 % für „überhaupt Tags"), **Konstanz ist der Hebel**: TikTok ordnet ein Konto anhand der ersten 5–10 Videos einem Thema zu → 4 feste Tags (`#doku #wahregeschichte #katastrophe #bergwerk`) + 1 wechselnder.
- **`#fyp` weglassen** (verwässert Themenzuordnung; kein Primärbeleg für Wirkung).
- **Frage in der Caption → +26,2 % Kommentare**, aber nur 2 von 10, nie auf Leid.
- Sichtbar vor „mehr": ~70 Zeichen. Caption-Grenze 2.200. Keine 3/24 h-Deckel. Links nicht klickbar.
- **Bedienoberfläche verdeckt Untertitel** (tiefer/linker als YT) → MARGIN anheben, rechte ~15 % frei.
- **Bewertungsfenster:** 96 % Reichweite in den ersten 10 Tagen; nach 24 h ist jede Zahl Rauschen.
- Zwei Hebel außerhalb der Caption: **Playlist** für die Reihe + **Bio mit Suchwörtern**.

## Counter Evidence / Warnung
- **OCR-Indexierung von eingebranntem Text: unbelegt.** Zunächst als Fakt behauptet, keine Primärquelle → als [[Failure-OCR-Behauptung-TikTok]] geführt. Taktik gilt trotzdem beidseitig: Caption liefert, was im Voiceover fehlt.
- Längen-Stichprobe auf Gewinner gefiltert (n=12) → beweist NICHT, dass kurze DE-Doku-Clips scheitern.
- **Offen:** Hashtag-Wahl stützt sich auf YouTube-Volumen → [[Frage-TikTok-Hashtag-Volumen]].

## Technik (Buffer)
Buffer holt Medien über **öffentliche URL** (keine Datei); Drive-Freigabe „Jeder mit Link" Pflicht, sonst HTML-Login statt Video. Gratis: 3 Kanäle, 10 Beiträge/Kanal. `create_post` braucht `channelId`, `schedulingType:"automatic"`, `mode:"customScheduled"`, `dueAt` mit Zeitzonen-Versatz. Nie Elternordner freigeben (`ZUGANGSDATEN.txt`).

## Related
[[Learning-Retention-und-Laenge]] · [[Learning-SEO]] · [[Learning-Captions]] · [[Failure-OCR-Behauptung-TikTok]]
