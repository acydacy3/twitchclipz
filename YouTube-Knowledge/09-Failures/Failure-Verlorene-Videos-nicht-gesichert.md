---
type: failure
status: failed-under-conditions
confidence: very high
created: 2026-08-24
updated: 2026-08-24
tags: [failure, prozess, upload, drive]
---

# Failure: Fertige Videos gingen verloren (nicht gesichert)

- **Was passierte:** 11 fertige San-José-Shorts + Cover wurden direkt zu YouTube hochgeladen, **nie nach Drive/Repo gesichert**. Einen Tag später (für TikTok gebraucht) waren sie weg — Container fort.
- **Warum unrettbar:** Die YouTube Data API hat **keinen Download-Befehl**; hochgeladene Videos sind nur per Studio-Browser-Knopf (Handarbeit) zurückholbar. Die Artefakt-Seite half nicht (keine Dateipfade/IDs).
- **Learning / Fix:** Jedes fertige Video/Cover nach `Katastrophenprotokoll-Pipeline` (Drive), benannt nach Teilnummer, **bevor** irgendetwas hochgeladen wird. Container = Wegwerfware.
- **Do not repeat unless:** nie — die Sicherung ist immer Pflicht. (Gilt analog für Code → [[Decision-Persistente-Werkzeuge-im-Repo]].)

## Related
[[Learning-Editing-Video]] · [[Decision-Persistente-Werkzeuge-im-Repo]]
