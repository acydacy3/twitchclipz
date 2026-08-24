---
type: decision
status: active
confidence: very high
created: 2026-08-24
updated: 2026-08-24
tags: [decision, umgebung, obsidian, drive, persistenz]
---

# Decision: Umgebungs-Realität & Obsidian-Brücke

## Hart verifizierte Fakten (24.08.2026)
- **Diese Sitzung läuft auf einem entfernten Linux-Server** (`hostname vm`, `root`), **nicht** auf dem PC des Nutzers. Belegt: kein `Desktop`, kein `zippo`, keine Windows-/Mac-Laufwerke auffindbar.
- **Es gibt KEINEN Obsidian-Connector** im Konto (verbunden: Buffer, Canva, Google Drive, ssemble, vidiq). Ich kann Obsidian **nicht** fernsteuern.
- **`git push` = 403** (kein GitHub-Schreibzugriff für `acydacy3/twitchclipz`).
- **Google Drive ist nur-Website** beim Nutzer (kein „Drive für Desktop") → Dateien in Drive erscheinen **nicht automatisch** auf seinem PC.

## Was daraus folgt (damit keine Session das neu durchleidet)
Obsidian ist **kein** Programm, das man „anbindet" — es ist ein Betrachter für
Markdown-Dateien. „Claude nutzt Obsidian" = Claude liest/schreibt dieselben
Dateien an einem Ort, den es erreicht.

**Erreichbare Orte von diesem Server aus:** nur **Google Drive** (Connector) —
GitHub ist wegen 403 zu, der lokale PC ist unerreichbar.

## Funktionierender Weg (24.08. erfolgreich getestet)
1. **Für den Nutzer → Obsidian:** Vault als **Zip** via `SendUserFile` → er entpackt
   es und öffnet den Ordner in Obsidian („Open folder as vault"). **Hat funktioniert**
   — er sieht den vollen Graph/Mindmap.
2. **Für Claude → Persistenz/Retrieval:** Vault liegt im Drive-Ordner
   `Katastrophenprotokoll-Pipeline/YouTube-Knowledge`
   (id `1rafUqiSsVYPeMJh_1IoNfj3zeoGd5TJZ`, **kanonisch seit Aufräumen 24.08.**; die alte
   `174lpTb…`-Kopie + ~5 Dubletten/„YouTubeKnowledgeFull" wurden getrasht). Ich lese/schreibe
   ihn über den Drive-Connector.

## Empfehlung für echte Auto-Sync (offen, Nutzer-Entscheidung)
**„Google Drive für Desktop"** installieren und das Obsidian-Vault in den
Drive-Ordner legen → dann erscheinen meine Änderungen automatisch in seinem
Obsidian, ohne Datei-Handoff. Alternativ Claude lokal ausführen. → [[Frage-Auto-Sync-Obsidian]]

## Related
[[Decision-Git-vs-Drive-Persistenz]] · [[Memory-Workflow]] · [[Audit-2026-08-24]]
