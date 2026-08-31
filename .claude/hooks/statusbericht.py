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
    "Obsidian: NICHT einfuehren (kein Connector, Direktzugriff besser)",
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
    """Liest aktive Experimente — gibt (bereit, aktiv) zurueck."""
    exp_dir = VAULT / "02-Experiments" / "Active"
    if not exp_dir.exists():
        return [], []
    bereit, aktiv = [], []
    for pfad in sorted(exp_dir.glob("*.md")):
        text = pfad.read_text(errors="ignore")
        status_m = re.search(r"^status:\s*(\w+)", text, re.MULTILINE)
        status = status_m.group(1) if status_m else "unknown"
        if status not in ("active", "planned"):
            continue
        start_m = re.search(r"^start_date:\s*(.+)", text, re.MULTILINE)
        start_raw = (start_m.group(1).strip() if start_m else "").strip()
        alter = 0
        if start_raw and start_raw not in ("", "null", "None"):
            try:
                import datetime as _dt
                start = _dt.datetime.fromisoformat(start_raw)
                alter = (_dt.datetime.now() - start).days
            except Exception:
                pass
        hat_result = bool(re.search(r"^result:\s*[^\"'\s]", text, re.MULTILINE))
        name = pfad.stem[:40]
        if alter >= 7 and not hat_result:
            bereit.append(name)
        else:
            aktiv.append(name)
    return bereit, aktiv


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
        # Hat diese Session eine neue Technik? -> Stopp
        tm = re.search(r"neue Technik:\s*(.+?)(?:\s*\|.*)?$", rest)
        if tm:
            letzte_technik = tm.group(1).strip()[:40]
            break  # Neueste Technik gefunden — alles davor zaehlt nicht
        # Kein Video? (SYS-Eintrag ohne neue Technik) -> uebergehen
        if session_id.startswith("SYS"):
            continue
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

    # ── Score lesen — bestimmt Detailtiefe ────────────────────────────────
    score, label, user_prompts = lese_autonomie_log()
    score_val = score or 0
    # Hoch (≥85) → kompakt. Mittel (70-84) → Gaps zeigen. Niedrig → voll
    detail = "kompakt" if score_val >= 85 else ("mittel" if score_val >= 70 else "voll")

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
    if score is not None:
        band = ("ROT" if score_val < 50 else "AMBER" if score_val < 70
                else "GRUEN" if score_val < 85 else "BLAU — nahe Ziel!")
        z(f"  Score: {score_val}/100 [{band}]  ({label})  Ziel: 90+")
        if user_prompts:
            z(f"  Gaps letzte Session: {', '.join(user_prompts[:5])}")
            z(f"  -> Diese Session: Gaps oben ZUERST autonom schliessen!")
    else:
        z("  Score: noch kein Eintrag — Autonomie-Log.md anlegen nach erster Produktion")

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
        exp_bereit, exp_aktiv = lese_experimente()
        if exp_bereit:
            z(f"  EXPERIMENTE BEREIT: {', '.join(exp_bereit)} <- JETZT auswerten!")
        elif exp_aktiv:
            z(f"  Experimente aktiv: {', '.join(exp_aktiv[:3])}")
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
        z("  Regeln: alle in Pflichtliste §2 (15 Dateien) — bei Produktion lesen")
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

        z("\nKERN-REGELN (destilliert — ERINNERUNG, ersetzt NICHT das Lesen der 15 Pflicht-Dateien):")
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
