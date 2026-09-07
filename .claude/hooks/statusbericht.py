#!/usr/bin/env python3
"""Sitzungsbericht fuer das Katastrophenprotokoll.

Gibt beim Session-Start den VOLLSTAENDIGEN Ueberblick aus — nicht als
Hinweis auf Dateien die gelesen werden sollen, sondern als direkten Inhalt.
Neue Tools/Skills werden automatisch erkannt. Kein manuelles Update noetig.
"""

import ast
import os
import re
import shutil
import socket
import subprocess
import sys
from pathlib import Path

# Pfad-Aufloesung: Script liegt in .claude/hooks/ → 2 Eltern = Projekt-Root
_SCRIPT = Path(__file__).resolve()
_ENV    = os.environ.get("CLAUDE_PROJECT_DIR", "")
PROJEKT = (Path(_ENV) if (_ENV and Path(_ENV).is_dir()) else _SCRIPT.parent.parent.parent)
VAULT   = PROJEKT / "YouTube-Knowledge"

# ─── Bekannte Pipeline-Skripte ──────────────────────────────────────────────
PIPELINE = [
    "transcribe_vosk.py", "align.py", "pauses.py", "bildcheck.py",
    "karaoke.py", "musik.py", "short.py", "serie.py", "lang.py",
    "videocheck.py", "analyse.py",
]

WERKZEUGE_BIN = ["ffmpeg", "ffprobe", "convert"]
PAKETE = [
    ("vosk", "vosk"), ("PIL", "pillow"), ("numpy", "numpy"),
    ("googleapiclient", "google-api-python-client"),
]
ZUGANG = ["YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"]
HOSTS  = [
    ("www.googleapis.com", "YouTube API"),
    ("www.youtube.com",    "Recherche"),
    ("api.elevenlabs.io",  "ElevenLabs"),
    ("higgsfield.ai",      "Higgsfield"),
]

# ─── MCP-Konnektoren (vollstaendig, inkl. Einsatzzweck und Kosten) ──────────
# Wenn ein neuer Konnektor in claude.ai verbunden wird:
# Diese Liste am Ende der Session ergaenzen + pushen.
MCP = [
    ("huggingface",    "Z-Image(IMMER ZUERST,gratis,~8/Tag) · Hub · Recherche",        "gratis"),
    ("higgsfield",     "Bild/Video-Gen · Upscale · Motion · Virality · TikTok-Pub",    "Credits"),
    ("ElevenLabs",     "VO-Peak · SFX · Transkription",                                "Credits sparsam"),
    ("Buffer",         "Social-Scheduling  (TikTok IMMER manuell durch Nutzer!)",       "gratis"),
    ("vidiq",          "Keywords · Outlier · Competitor · Score",                       "Credits schonen"),
    ("Canva",          "Thumbnails · Cover · Grafik-Vorlagen",                          "Konto"),
    ("ssemble",        "Shorts · Meme-Hooks · Templates",                               "Konto"),
    ("Google Drive",   "Assets holen/ablegen via gdown",                               "gratis"),
    ("github",         "Repos · PRs · Issues · CI",                                    "gratis"),
    ("claude-remote",  "Sessions · Trigger · Zeitplaene",                              "gratis"),
]

# ─── Skills (produktionsrelevant) ───────────────────────────────────────────
SKILLS_KERN = [
    "/video", "/merken", "/neubeginn",
    "youtube", "dataviz", "canvas-design",
    "design", "theme-factory", "prompt-master",
    "code-review", "skill-creator",
]

# ─── Lokale Tools: bekannte Beschreibungen (Fallback: Dateiname) ─────────────
TOOL_BESCHR = {
    "nb_suggest.py":    "YouTube-Keywords recherchieren",
    "nb_trends.py":     "Google Trends Vergleich",
    "nb_openverse.py":  "CC-Bild-Pool (Openverse)",
    "nb_upscale.py":    "Bilder schaerfen / freistellen (--cutout, rembg)",
    "nb_tts.py":        "Piper-TTS Scratch-VO (deutsch, gratis)",
    "nb_views90.py":    "90-Tage-Views -> YPP-Log",
    "nb_fetch_broll.py":"Wikimedia-Commons-Kategorien als Broll",
}

# ─── Geltende Kern-Regeln (aus Learnings destilliert, hier direkt lesbar) ──
# NICHT 'go read 14 files' — das sind die aktuellen Regeln selbst.
# Update wenn eine Rule sich aendert (selten).
REGELN = [
    "Hook: Sekunde 1 = BEWEGUNG (Bewegtshot/Animation, kein Standbild-Establishing)  |  Zone 19-39 s",
    "Untertitel = Stimme des Publikums  |  Hook-Banner nur als Test",
    "Keyword stark in Titel, Aussage fertig bis Zeichen 35",
    "Bewegtbild-PFLICHT: >=1 bewegter Schluessel-Shot je Short (Manim/Remotion/Wan2.1-I2V), nie reine Diashow",
    "Musik -16 LUFS  |  db=-16 hoerig verifizieren (volumedetect nach Render)",
    "TikTok NIE automatisch  |  Claude liefert, Nutzer laedt hoch",
    "Bilder: global Dedup-Set pro Produktion, alle auf 1600x2848",
    "Broll autonom sourcing: Commons-Kategorien + Openverse (Nutzer sucht nie selbst)",
    "Schnitt buerdig 3/Tag, Slots 10:30/14:30/18:00 UTC, kein Reihen-Bruch",
    "Captions aus Nutzer-Skript via align.py, NIE aus roher ASR (F-V8-E)",
    "Analytics-Loop: Tag 4-5 AVP%/CTR ziehen -> Post-Mortem -> naechstes Video steuern",
]


def haken(ok):
    return "ja " if ok else "NEIN"


def erreichbar(host, timeout=5):
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if not proxy:
        try:
            socket.create_connection((host, 443), timeout=timeout).close()
            return True
        except OSError:
            return False
    try:
        r = subprocess.run(
            ["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}",
             "--max-time", str(timeout), f"https://{host}/"],
            capture_output=True, text=True, timeout=timeout + 4,
        )
        return r.stdout.strip() not in ("", "000")
    except Exception:
        return False


def auto_scan_tools():
    """Scannt nur tools/ nach *.py — damit keine Reihen-Skripte mit falschen Beschr. erscheinen."""
    ergebnis = []
    tools_dir = PROJEKT / "tools"
    if not tools_dir.is_dir():
        return ergebnis
    for p in sorted(tools_dir.glob("*.py")):
        if p.name.startswith("_"):
            continue
        beschr = TOOL_BESCHR.get(p.name, "")
        if not beschr:
            try:
                src = p.read_text(errors="ignore")
                tree = ast.parse(src)
                doc = ast.get_docstring(tree)
                if doc:
                    beschr = doc.split("\n")[0].strip()[:60]
            except Exception:
                pass
        if not beschr:
            beschr = "—"
        ergebnis.append((p.name, beschr))
    return ergebnis


def auto_scan_skills():
    """Scannt .claude/skills/ nach SKILL.md und extrahiert erste Inhaltszeile."""
    skills_dir = PROJEKT / ".claude" / "skills"
    gefunden = []
    if not skills_dir.is_dir():
        return gefunden
    for skill_dir in sorted(skills_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        name = skill_dir.name
        beschr = ""
        try:
            for line in skill_md.read_text(errors="ignore").splitlines():
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                beschr = line[:70]
                break
        except Exception:
            pass
        gefunden.append((name, beschr))
    return gefunden


def auto_scan_manim():
    """Findet alle Scene-Klassen in tools/manim_scenes.py."""
    manim_py = PROJEKT / "tools" / "manim_scenes.py"
    if not manim_py.exists():
        return []
    klassen = []
    try:
        src = manim_py.read_text(errors="ignore")
        for m in re.finditer(r"^class\s+(\w+)\s*\(.*Scene", src, re.MULTILINE):
            klassen.append(m.group(1))
    except Exception:
        pass
    return klassen


def auto_scan_neue_skills(bekannte):
    """Meldet Skills die in .claude/skills/ liegen aber nicht in SKILLS_KERN."""
    neue = []
    for name, _ in auto_scan_skills():
        if name not in bekannte and "/" + name not in bekannte:
            neue.append(name)
    return neue


def lese_autonomie_log():
    """Liest neuesten Score + User-Prompts (erste ### Zeile = neueste)."""
    log_path = VAULT / "00-System" / "Autonomie-Log.md"
    if not log_path.exists():
        return None, None, []
    lines = log_path.read_text(errors="ignore").splitlines()
    score = label = None
    user_prompts = []
    in_entry = False
    for line in lines:
        m = re.match(r"^###\s+(\S+)\s*\|\s*(.+?)\s*\|\s*\S+\s*\|\s*Score:\s*(\d+)", line)
        if m:
            if score is not None:
                break  # Nur neueste Session (erste Zeile)
            label = f"{m.group(1)} {m.group(2).strip()}"
            score = int(m.group(3))
            in_entry = True
            continue
        if in_entry:
            pm = re.search(r"User-Prompts:\s*\[(.+?)\]", line)
            if pm:
                user_prompts = [p.strip().strip('"\'') for p in pm.group(1).split(",")]
                break
    return score, label, user_prompts


def lese_experimente():
    """Liest Experimente — gibt (bereit, laufend, nie_gestartet) zurueck.

    Aenderung 07.09.: Frueher wurde das Alter aus start_date berechnet. Ist
    start_date leer, ergab das Alter 0 — das Experiment landete fuer immer im
    Topf "laeuft" und konnte NIE ueberfaellig werden. Genau so war es: alle
    vier Experimente hatten ein leeres start_date, der Bericht meldete
    wochenlang "Experimente aktiv" fuer Experimente, die nie begonnen hatten.
    Ein Experiment ohne Startdatum laeuft nicht — es steht still, und das
    muss sichtbar sein.
    """
    exp_dir = VAULT / "02-Experiments" / "Active"
    if not exp_dir.exists():
        return [], [], []
    bereit, laufend, nie_gestartet = [], [], []
    for pfad in sorted(exp_dir.glob("*.md")):
        text = pfad.read_text(errors="ignore")
        status_m = re.search(r"^status:\s*(\w+)", text, re.MULTILINE)
        status = status_m.group(1) if status_m else "unknown"
        if status not in ("active", "planned"):
            continue
        start_m = re.search(r"^start_date:\s*(.+)", text, re.MULTILINE)
        start_raw = (start_m.group(1).strip() if start_m else "").strip()
        name = pfad.stem[:40]

        if not start_raw or start_raw in ("null", "None"):
            nie_gestartet.append(name)
            continue

        alter = 0
        try:
            import datetime as _dt
            start = _dt.datetime.fromisoformat(start_raw)
            alter = (_dt.datetime.now() - start).days
        except Exception:
            nie_gestartet.append(name)   # unlesbares Datum = kein Startbeleg
            continue

        hat_result = bool(re.search(r"^result:\s*[^\"'\s]", text, re.MULTILINE))
        if alter >= 7 and not hat_result:
            bereit.append(f"{name} ({alter}T)")
        else:
            laufend.append(name)
    return bereit, laufend, nie_gestartet


def lese_neueste_observation():
    """Liest die juengste Zeile aus Observations.md."""
    obs_pfad = VAULT / "07-Analytics" / "Observations.md"
    if not obs_pfad.exists():
        return None
    for line in obs_pfad.read_text(errors="ignore").splitlines():
        line = line.strip()
        if line.startswith("- ["):
            return line[2:80]  # Erster Treffer = neueste Observation
    return None


def regel_deckung():
    """Wie viele Produktionsregeln haben einen echten Pruefpunkt?

    Diese Zeile ist der Ersatz fuer den alten Selbst-Score. Sie kann nicht
    geschoent werden: sie zaehlt Funktionen im Code, nicht Absichten. Legt
    jemand eine neue Regel als Prosa an, sinkt die Zahl sofort sichtbar.
    """
    try:
        sys.path.insert(0, str(PROJEKT / "tools"))
        import kp_regeln as R
        g, n = R.deckung()
        offen = [r["id"] + " " + r["titel"] for r in R.REGELN if not r["pruefung"]]
        zeilen = [f"  Regeln: {g}/{n} erzwungen ({g/n:.0%})"
                  f"  ->  YouTube-Knowledge/00-System/Regel-Register.md"]
        if offen:
            zeilen.append(f"  ohne Pruefpunkt: {', '.join(offen)}")
        return zeilen
    except Exception as e:
        return [f"  Regel-Register nicht lesbar ({e}) — python3 tools/kp_regeln.py"]


def gemessener_stand():
    """Die Zahlen, die NICHT von Claude selbst kommen.

    Ersetzt die Zeile "Score: 88/100 [BLAU — nahe Ziel!]". Dieser Score stand
    in Autonomie-Log.md, wo Claude ihn selbst eintrug. Er stieg von 48 auf 88,
    waehrend der gesehene Anteil je Short von 76 % auf 54 % fiel. Eine Zahl,
    die man sich selbst gibt, kann nicht widersprechen.

    Gelesen wird der letzte gespeicherte Snapshot -- ohne Netzabruf, damit der
    Sitzungsstart nicht haengt. Frische Zahlen: tools/kp_metrik.py.
    """
    import datetime as _dt
    import json as _json
    zeilen = []
    snap_dir = VAULT / "07-Analytics" / "snapshots"
    snaps = sorted(snap_dir.glob("*.json")) if snap_dir.is_dir() else []
    if not snaps:
        zeilen.append("  Kanalstand: kein Snapshot vorhanden "
                      "-> python3 tools/kp_metrik.py --snapshot")
        return zeilen
    try:
        d = _json.loads(snaps[-1].read_text(errors="ignore"))
    except Exception:
        return ["  Kanalstand: Snapshot unlesbar."]

    datum = d.get("snapshot_date", "?")
    alter = "?"
    try:
        alter = (_dt.date.today() - _dt.date.fromisoformat(datum)).days
    except Exception:
        pass
    zeilen.append(f"  Gemessen ({datum}): {d.get('subscribers','?')} Abos · "
                  f"{d.get('total_views','?')} Aufrufe · "
                  f"{d.get('video_count','?')} Videos")
    if isinstance(alter, int) and alter >= 2:
        zeilen.append(f"  ACHTUNG: Snapshot ist {alter} Tage alt. Ohne taegliche "
                      f"Snapshots sind Serien nicht mehr vergleichbar")
        zeilen.append(f"  (V5 und V6 sind genau so dauerhaft unmessbar geworden) "
                      f"-> tools/kp_metrik.py --snapshot")
    return zeilen


def anti_stall_check():
    """Videos seit letzter neuer Technik.

    Log-Format: ### ID | Label | Datum | Score: N | neue Technik: X
    Neueste zuerst — beim ersten Fund stoppen.
    """
    log_path = VAULT / "00-System" / "Autonomie-Log.md"
    if not log_path.exists():
        return 0, "unbekannt"
    videos_seit_technik = 0
    letzte_technik = None
    for line in log_path.read_text(errors="ignore").splitlines():
        m = re.match(r"^###\s+(\S+)\s*\|(.+)", line)
        if not m:
            continue
        session_id = m.group(1)
        rest       = m.group(2)
        # Aenderung 07.09.: Eine System-Session (SYS) setzt den Anti-Stall
        # NICHT mehr zurueck. Vorher genuegte ein "neue Technik"-Eintrag in
        # einer reinen Meta-Session, um "Anti-Stall: OK" zu melden -- und
        # genau das stand dort, waehrend vom 31.08. bis 06.09. kein einziges
        # Video entstand. Der Zaehler soll Produktion messen, nicht Betrieb.
        if session_id.startswith("SYS"):
            continue
        tm = re.search(r"neue Technik:\s*(.+?)(?:\s*\|.*)?$", rest)
        if tm:
            letzte_technik = tm.group(1).strip()[:40]
            break
        videos_seit_technik += 1
    return videos_seit_technik, letzte_technik or "unbekannt"


def main():
    zeilen = []
    z = zeilen.append

    # ── System-Checks (immer, kompakt) ────────────────────────────────────
    fehlend   = [d for d in PIPELINE if not (PROJEKT / d).is_file()]
    fehlt_w   = [w for w in WERKZEUGE_BIN if not shutil.which(w)]
    fehlt_p   = []
    for modul, paket in PAKETE:
        try: __import__(modul)
        except ImportError: fehlt_p.append(paket)
    modell = next(
        (p for p in (Path("/opt/vosk-model-small-de-0.15"),
                     PROJEKT / "vosk-model-small-de-0.15") if p.is_dir()),
        PROJEKT / "vosk-model-small-de-0.15",
    )
    gesetzt = [v for v in ZUGANG if os.environ.get(v)]
    infra_ok = not fehlend and not fehlt_w and not fehlt_p and modell.is_dir()
    yt_ok    = len(gesetzt) == len(ZUGANG)

    # ── Detailtiefe ist NICHT mehr an den Selbst-Score gekoppelt ─────────
    # Vorher: Score >= 85 -> "kompakt" -> die Kern-Regeln verschwanden aus dem
    # Bericht. Der Score wurde aber von Claude selbst eingetragen. Ein hoher
    # selbstvergebener Score liess also genau die Regeln ausblenden, deren
    # Einhaltung er behauptete. Am 07.09. stand dort 88/100, waehrend fuenf
    # terminierte Shorts reine Standbild-Diashows waren und alle zehn
    # Prosperi-Shorts falsche Untertitel trugen.
    # Regeln stehen ab jetzt IMMER im Bericht.
    score, label, user_prompts = lese_autonomie_log()
    detail = "voll"

    z("")
    z("=" * 68)
    z("  KATASTROPHENPROTOKOLL — Sitzungsstart")
    z("=" * 68)

    # Status-Zeile
    pipeline_s = f"OK ({len(PIPELINE)})" if not fehlend else f"FEHLT {fehlend}"
    werkzeug_s = "OK" if infra_ok else f"FEHLT {fehlt_w + fehlt_p}"
    yt_s       = "OAuth OK" if yt_ok else ("API-Key" if os.environ.get("YOUTUBE_API_KEY") else "KEIN ZUGANG")
    z(f"  Pipeline: {pipeline_s}  |  System: {werkzeug_s}  |  YouTube: {yt_s}")

    # Netz — nur Ausfaelle zeigen wenn kompakt, sonst alle
    netz_results = [(h, w, erreichbar(h)) for h, w in HOSTS]
    ausfaelle = [(h, w) for h, w, ok in netz_results if not ok]
    if detail == "kompakt" and not ausfaelle:
        z(f"  Netz: alle {len(HOSTS)} Hosts erreichbar")
    else:
        z("  Netz:")
        for h, w, ok in netz_results:
            z(f"    {haken(ok)}  {h:<22}  {w}")

    # ── Autonomie-Score (immer sichtbar) ──────────────────────────────────
    z("-" * 68)
    for zeile in gemessener_stand():
        z(zeile)
    for zeile in regel_deckung():
        z(zeile)
    if score is not None:
        z(f"  (Selbst-Score {score} aus Autonomie-Log.md — selbst vergeben, "
          f"misst nichts. Nur Historie.)")

    # Anti-Stall (immer, einzeilig)
    try:
        vs, lt = anti_stall_check()
        if vs >= 3:
            z(f"  ANTI-STALL: {vs} Videos ohne neue Technik — naechste Session: neue Klasse!")
        else:
            z(f"  Anti-Stall: OK  (letzte Technik: {lt})")
    except Exception:
        pass

    # ── Experimente + Observations (immer sichtbar) ───────────────────────
    try:
        exp_bereit, exp_laufend, exp_nie = lese_experimente()
        if exp_bereit:
            z(f"  EXPERIMENTE BEREIT: {', '.join(exp_bereit)} <- JETZT auswerten!")
        if exp_nie:
            z(f"  NIE GESTARTET ({len(exp_nie)}): {', '.join(e[:34] for e in exp_nie[:3])}")
            z(f"  -> ohne start_date laeuft kein Experiment. Starten oder schliessen.")
        if exp_laufend:
            z(f"  Experimente laufen: {', '.join(exp_laufend[:3])}")
        neueste_obs = lese_neueste_observation()
        if neueste_obs:
            z(f"  Letzte Observation: {neueste_obs[:90]}")
    except Exception:
        pass

    # ── Repertoire — adaptiv ──────────────────────────────────────────────
    z("=" * 68)

    if detail == "kompakt":
        # Score >= 85: System funktioniert. Nur das Wesentlichste.
        z("REPERTOIRE (Score hoch — System laeuft):")
        z(f"  MCP: {', '.join(n for n,_,_ in MCP)}")
        z(f"  Skills: {', '.join(SKILLS_KERN)}")
        tools = auto_scan_tools()
        z(f"  Tools: {', '.join(n for n, _ in tools)}")
        mk = auto_scan_manim()
        z(f"  Manim ({len(mk)}): {', '.join(mk)}")
        z("  Regeln: alle in Pflichtliste §2 gelistet — bei Produktion lesen")
    else:
        # Score < 85: Volle Ausgabe — jede Information direkt im Kontext
        z("VOLLSTAENDIGES REPERTOIRE — autonom nutzen, nie ankuendigen:")
        z("")
        z(f"MCP ({len(MCP)}):")
        for name, zweck, kosten in MCP:
            z(f"  {name:<13} {zweck}  [{kosten}]")

        extra = auto_scan_neue_skills(SKILLS_KERN)
        z(f"\nSKILLS: {', '.join(SKILLS_KERN)}")
        if extra:
            z(f"  NEU erkannt: {', '.join(extra)}  <- in SKILLS_KERN aufnehmen!")

        tools = auto_scan_tools()
        z(f"\nLOKALE TOOLS ({len(tools)}, auto-erkannt aus tools/):")
        for name, beschr in tools:
            z(f"  {name:<22}  {beschr}")

        mk = auto_scan_manim()
        z(f"\nANIMATION — manim_scenes.py ({len(mk)} Klassen):")
        z("  " + "  ·  ".join(mk) if mk else "  (keine)")
        z("  Remotion: tools/remotion/ (naechster Schritt: WordReveal)")
        z("  Baum: Zahl->StatCounter  Route->Map  Tage->SurvivalDays")
        z("        Suche->SearchRadius  Tiefe->DepthDive  Tunnel->CrossSection")

        z("\nKERN-REGELN (destilliert — ERINNERUNG, ersetzt NICHT das Lesen der §2-Pflicht-Dateien):")
        for i, r in enumerate(REGELN, 1):
            z(f"  {i:>2}. {r}")

    # ── Vor-Produktion (immer, kompakt) ───────────────────────────────────
    z("-" * 68)
    z("VOR PRODUKTION: nb_analytics_snapshot.py -> nb_observe.py -> Pflichtliste §2 -> HF-Quota")
    z("SESSION-ENDE:   Autonomie-Log updaten + commit + auf main mergen + push (main = naechster Container)")
    z("Originalskript kommt vom Nutzer. Nutzer arbeitet nicht mit der Kommandozeile.")
    z("=" * 68)
    z("")

    print("\n".join(zeilen))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Statusbericht fehlgeschlagen: {e}", file=sys.stderr)
        sys.exit(0)
