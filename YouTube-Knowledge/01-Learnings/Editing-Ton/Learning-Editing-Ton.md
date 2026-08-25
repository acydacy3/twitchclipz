---
type: learning
status: active
confidence: high
domain: editing-ton
created: 2026-08-24
updated: 2026-08-24
evidence_count: 2
tags: [learning, ton, audio, ffmpeg, musik]
---

# Learning: Ton

## Current Learning
- **Ziel −14 LUFS, Spitze unter −1,5 dBTP.**
- `loudnorm` allein reicht nicht (bei dichter Stimme, LRA ~4, bremst die Spitzengrenze das Gain). Kette, die trifft: **zweistufiges `loudnorm` → `volume=1.6dB` → `alimiter=limit=0.84:level=false`**.
- **`level=false` beim `alimiter` ist Pflicht** — sonst zieht er auf Vollaussteuerung (gemessen +0,1 dBFS).

## Musik
- **Selbst erzeugen, nicht aus der YouTube-Bibliothek.** Bei Shorts teilt YouTube die Einnahmen je Musikstück (1 Track = 50 %, 2 = 33 %) + Content-ID-Sperren. `musik.py` erzeugt ein Moll-Bett (Drone, Pad, Herzschlag, Schimmer, Rauschen).
- **Sidechain-Ducking** unter die Stimme (nicht pauschal leise), in Sprechpausen kommt sie hoch.

## Scope
Alle Videos des Kanals.

## Counter Evidence
Keine. −14-LUFS-Ziel ohne explizites „Warum" dokumentiert (Broadcast-Standard, unkritisch).

## Operational Implication
Vor Export via `videocheck.py` prüfen.

## History
- 17.08. (Video 1 lag bei −15,7 LUFS → Kette entwickelt).

## Related
[[Learning-Editing-Video]] · [[Learning-Captions]]

## Musik war in V1–V5 nie hörbar (Nutzer-Befund 25.08.) — GELÖST
Zwei Ursachen, beide gefixt:
1. **Pegel zu tief:** Config `musik.db = -25` → unter dem Sidechain-Ducking praktisch unhörbar. **Fix: db ≈ -16** (Musik-Bett liegt bei ~-12 dB, bei -16 dB klar präsent unter der Stimme). Gegenprobe: `ffmpeg -af volumedetect` am fertigen Short.
2. **Falsches CWD:** `short.py` ruft `musik.py`/`karaoke.py` **relativ** auf → **Render IMMER aus Repo-Root** (`/home/user/twitchclipz`) starten, sonst bricht `musik.py` (bzw. es lief bei falschem CWD gar nicht). 
**Regel:** Musik nach jedem Video mit volumedetect verifizieren (mean sollte ~-16…-18 dB, nicht nur Stimme).

## Piper-TTS (deutsch) ist LEGITIM als finale Video-Stimme (Nutzer 25.08.)
- **`de_DE-thorsten-medium` (Piper) taugt als vollwertige Voiceover-Stimme**, nicht nur Scratch — dem Nutzer „sehr sehr gut" gefallen. Der ruhige, gleichmäßige Klang passt zum nüchternen Fascinating-Horror-Ton.
- **Default-Strategie (kostenlos skalieren):** Piper = **kostenloser Standard-VO** für die meisten Shorts → spart ElevenLabs-Credits. **ElevenLabs nur für dramatische Peak-Videos** (mehr Emotion/Pausen/Betonung).
- **Upgrade offen:** `de_DE-thorsten-high` (auch gratis) klingt nochmal etwas runder — bei Bedarf statt medium. Nutzung: `tools/nb_tts.py "text" out.mp3`.
