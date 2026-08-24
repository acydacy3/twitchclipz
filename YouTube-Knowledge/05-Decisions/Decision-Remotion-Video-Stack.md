---
type: decision
status: active
confidence: high
created: 2026-08-24
updated: 2026-08-24
tags: [decision, tooling, video, remotion, guardrail-8]
---

# Decision: Remotion (React-Video-Stack) vorerst NICHT einführen

## Frage
Nützt der „Remotion-Skill" für Video-Animation/Schnitt, und soll er installiert werden?

## Hart geprüfte Fakten (24.08.2026)
- **Es existiert kein Remotion-*Skill/Plugin*** (Konto + Marktplatz durchsucht) — nur das
  **npm-Framework** `remotion`. „Skill installieren" ist also gegenstandslos.
- **Umgebung trägt es:** Node v22, npm 10, Chromium vorhanden (`/opt/pw-browsers`).
- **Bestehende Pipeline funktioniert:** `karaoke.py` (Captions/ASS), `short.py` (Assembly),
  zoompan (Ken-Burns), Audio-Kette (loudnorm→volume→alimiter). Deckt das aktuelle
  Bild+Zoom+Untertitel-Format ab.

## Bewertung nach [[Guardrails]] #8 (Minimale Komplexität)
- **Nötig?** Nein — ffmpeg+Python deckt den aktuellen Output.
- **Wo wäre Remotion überlegen?** Nur **Motion-Graphics**: animierte Karten, Rettungs-
  Zeitleisten, kinetische Typografie, datengetriebene Reveals. **Kein etablierter Bedarf** bisher.
- **Wartung:** unverhältnismäßig — paralleler React/Node/TS-Stack, Chromium-Render
  langsamer/schwerer als ffmpeg, zwei Toolchains.
- **#9 (Human Control):** Architektur-Änderung an der Produktion → erst vorschlagen, nicht
  eigenmächtig einführen.

## Entscheidung
**Vorerst NICHT installieren.** ffmpeg+Python bleibt die Haupt-Pipeline.

## Trigger, ab wann es sich lohnt (Re-Evaluation)
Sobald **animierte Karten / Zeitleisten / kinetische Text-Reveals** als **wiederkehrendes**
Stilmittel gewünscht sind (z. B. „wo liegt das Bergwerk", Timeline der Rettung). Dann:
Remotion **isoliert nur für diese Motion-Graphics-Clips** installieren
(`npm i remotion @remotion/cli`), Output als Clip in die ffmpeg-Pipeline einspeisen —
**kein** Ersatz der bestehenden Skripte.

## Related
[[Guardrails]] · [[Learning-Editing-Video]] · [[Agent-Architecture]]
