---
type: experiment
status: planned
hypothesis: "Ein animiertes Motion-Graphics-Element (Remotion) an EINEM Schlüsselbeat hebt AVP%/Retention gegenüber statischem Ken-Burns."
domain: editing
variables: "Motion-Graphics-Clip (Remotion) statt statischem Bild an 1 Beat"
control: "restliche Shorts desselben Videos = normale ffmpeg-Pipeline (Ken-Burns)"
test: "nächstes Video: 1 Short mit Remotion-Element bauen (z. B. animierte Karte/Querschnitt/Timeline)"
dependent: "AVP% + 3-s-Retention (Tag 4-5), sekundär Aufrufe"
start_date:
end_date:
sample_size: 1
result: ""
confidence: low
decision: ""
tags: [experiment, remotion, editing, motion-graphics]
---

# Experiment: Remotion Motion-Graphics an einem Schlüsselbeat

## Warum (Retrieval before Reinvention)
[[Decision-Remotion-Video-Stack]]: Remotion vorerst zurückgestellt (Guardrail #8), Trigger =
„sobald Motion-Graphics wiederkehrend nützt". Nutzer will es beim **nächsten Video testen** →
sauberes Experiment statt blindem Einbau.

## Aufbau (Experiment-Manager, ein Variable)
- **Kandidat-Beats (Motion-Graphics glänzt):** animierte **Karte** (Prosperi: 291-km-Irrweg) oder
  **Querschnitt/Timeline** (Nutty Putty: 25-cm-Spalt, Stunde 1→27). Beides sind genau die Fälle,
  wo statische Bilder schwach sind.
- **Vorgehen:** EIN Short bekommt das Remotion-Element (Rest bleibt ffmpeg-Pipeline).
  Remotion isoliert rendern → Clip als Segment in `short.py`/Schnitt einspeisen (kein Ersatz der Pipeline).
- **Messung:** Tag 4–5 AVP%/Retention dieses Shorts vs. der statischen Shorts desselben Videos → [[Analytics-Loop]].

## Entscheidung danach
- Deutlich besser → Remotion für Karten/Timelines als Standard-Werkzeug (Motion-Graphics-Beats).
- Kein Unterschied / mehr Aufwand als Nutzen → bei ffmpeg bleiben (Guardrail #8 bestätigt).

## Betrieb (Runbook-Ergänzung nach Test)
Remotion-Skills sind installiert (`remotion:remotion-*`). Node v22 + Chromium vorhanden.
Isolierter Render, dann Clip in die Pipeline — nicht die Skripte ersetzen.

## Related
[[Decision-Remotion-Video-Stack]] · [[Experiment-Manager]] · [[Analytics-Loop]] · [[Produktions-Runbook]] · [[Ideen-Pipeline]]
