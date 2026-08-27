"""
Contrarian-Layer: Aktive Pflichtprüfung aller bewiesenen Learnings.

Funktioniert als Cross-Cutting-Layer für ALLE Produktionsdomänen:
- Editing (Ton, Video, Musik)
- Hooks + Storytelling
- Captions + Titel + SEO
- Retention + Länge
- Bilder-Sourcing

Nutzung:
    python3 tools/nb_contrarian.py                  # Vollständiger Regel-Report
    python3 tools/nb_contrarian.py short07.json      # Produktions-Audit gegen Konfig
    python3 tools/nb_contrarian.py --kurz            # Nur Warnstufen: HIGH+VERY_HIGH
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime

VAULT = Path(__file__).resolve().parent.parent / "YouTube-Knowledge"
LEARNINGS_DIR = VAULT / "01-Learnings"
FAILURES_DIR = VAULT / "09-Failures"

CONFIDENCE_ORDER = {"very high": 4, "high": 3, "medium": 2, "low": 1}


# ── Hartcodierte Produktions-Regeln (aus Learnings destilliert) ──────────────
# Format: (domain, rule_text, confidence, check_fn_or_None)
# check_fn erhält cfg-dict und gibt (ok: bool, detail: str) zurück.

def _check_musik_db(cfg):
    mus = cfg.get("musik")
    if not mus:
        return True, "kein Musikbett konfiguriert (ok wenn gewollt)"
    db = mus.get("db", -21)
    if db < -18:
        return False, f"musik.db={db} — muss ≥ -18 sein (Ziel: -16), sonst unhörbar"
    return True, f"musik.db={db} ✓"


def _check_hook(cfg):
    if not cfg.get("hook"):
        return False, "kein 'hook'-Key in Konfig — Hook ist Pflicht für Retention"
    txt = cfg["hook"].get("text", "")
    if len(txt) < 10:
        return False, f"Hook-Text zu kurz ({len(txt)} Zeichen)"
    return True, f"Hook: '{txt[:60]}' ✓"


def _check_hook_until(cfg):
    if not cfg.get("hook"):
        return True, "kein Hook gesetzt"
    ht = cfg.get("hook_until", 3.2)
    if ht > 4.0:
        return False, f"hook_until={ht}s — Hook sollte ≤ 4 s sichtbar bleiben"
    return True, f"hook_until={ht}s ✓"


def _check_titel_laenge(cfg):
    title = cfg.get("titel") or cfg.get("title") or cfg.get("metadata", {}).get("title", "")
    if not title:
        return True, "kein Titel in Konfig"
    if len(title) > 60:
        return False, f"Titel {len(title)} Zeichen — Aussage muss bei Zeichen 35 fertig sein"
    if len(title) > 40:
        return None, f"Titel {len(title)} Zeichen — prüfe ob Keyword-Aussage bei Zeichen 35 fertig"
    return True, f"Titel {len(title)} Zeichen ✓"


def _check_no_emoji_titel(cfg):
    title = cfg.get("titel") or cfg.get("title") or cfg.get("metadata", {}).get("title", "")
    if not title:
        return True, "kein Titel"
    emoji_re = re.compile(r"[\U00010000-\U0010ffff]", re.UNICODE)
    if emoji_re.search(title):
        return False, f"Emoji im Titel gefunden — laut Learning verboten"
    return True, "kein Emoji im Titel ✓"


def _check_shots_count(cfg):
    shots = cfg.get("shots", [])
    n = len(shots)
    if n < 2:
        return False, f"nur {n} Shot(s) — Minimum 2, besser 3-6"
    if n > 7:
        return None, f"{n} Shots — prüfe ob alle notwendig (Richtwert 2-6)"
    return True, f"{n} Shots ✓"


def _check_audio(cfg):
    if not cfg.get("audio"):
        return False, "kein 'audio'-Key — VO fehlt"
    return True, "audio gesetzt ✓"


def _check_words(cfg):
    if not cfg.get("words"):
        return False, "kein 'words'-Key — Karaoke-Untertitel fehlen"
    return True, "words gesetzt ✓"


def _check_font(cfg):
    if not cfg.get("font_black"):
        return False, "kein 'font_black'-Key — Untertitel-Font fehlt"
    return True, "font_black gesetzt ✓"


PRODUKTIONS_REGELN = [
    # (domain, text, confidence, check_fn_or_None)
    ("Ton",      "Musik db ≥ -18 dB (Ziel -16), sonst unhörbar — V1-V5 Fehler",           "very high",  _check_musik_db),
    ("Hook",     "Jeder Short MUSS einen Hook haben — Hook entscheidet, nicht Länge",       "very high",  _check_hook),
    ("Hook",     "Hook ≤ 4 s sichtbar — danach Story, kein zweiter Hook-Moment",            "high",       _check_hook_until),
    ("Titel",    "Aussage bei Zeichen 35 fertig — DE-Komposita brechen bei ~40 ab",        "very high",  _check_titel_laenge),
    ("Titel",    "Kein Emoji im Titel",                                                     "high",       _check_no_emoji_titel),
    ("Editing",  "2-6 Shots je Short — tote Sekunden killen",                               "high",       _check_shots_count),
    ("Editing",  "VO (audio) MUSS gesetzt sein",                                            "very high",  _check_audio),
    ("Captions", "words-File (Karaoke) MUSS gesetzt sein — Ton-aus-Publikum",              "very high",  _check_words),
    ("Editing",  "font_black MUSS gesetzt sein",                                            "high",       _check_font),

    # Regeln ohne automatische Prüfbarkeit (manuell abhaken)
    ("Hook",     "Hook-Text NICHT identisch mit gesprochenem Satz — verschenkt den Kanal", "very high",  None),
    ("Captions", "Untertitel = Stimme (1:1) — kein abweichender Text außer als Experiment","very high",  None),
    ("Bilder",   "Schlüsselmomente IMMER generieren, nicht nur Stock-Bilder",               "high",       None),
    ("Bilder",   "Kontaktabzug (montage) QC-Check vor Upload",                             "high",       None),
    ("SEO",      "Min. 1 starkes Keyword im Titel (Doku/Katastrophe/wahre Geschichte)",     "very high",  None),
    ("SEO",      "nb_suggest.py + nb_trends.py vor Titel-Entscheidung laufen",             "high",       None),
    ("Retention","Sichere Zone 19-39 s — tote Sekunden rausschneiden",                      "high",       None),
    ("Ton",      "volumedetect nach Render — Musik MUSS hörbar sein",                       "very high",  None),
    ("Upload",   "analyse.py prüfen vor Upload: letzte terminierte Slots",                  "high",       None),
    ("Upload",   "TikTok NIE automatisch — Nutzer lädt selbst hoch",                       "very high",  None),
    ("Persistenz","git commit + push nach jeder Session",                                   "very high",  None),
    ("Persistenz","Neue Learnings sofort in Vault (nicht am Session-Ende aufsparen)",       "high",       None),
]


# ── Vault-Learnings lesen ────────────────────────────────────────────────────

def lade_vault_learnings():
    """Liest alle 01-Learnings + Failure-Memory, extrahiert Kurzfassung + Confidence."""
    result = []
    for md in sorted(LEARNINGS_DIR.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        # Confidence aus Frontmatter
        conf_match = re.search(r"^confidence:\s*(.+)$", text, re.MULTILINE | re.IGNORECASE)
        conf = conf_match.group(1).strip().lower() if conf_match else "unbekannt"
        # Domäne aus Dateiname
        domain = md.parent.name if md.parent.name != "01-Learnings" else "Allgemein"
        # Current Learning extrahieren
        cl_match = re.search(r"## Current Learning\s*\n(.+?)(?=\n##|\Z)", text, re.DOTALL)
        current = cl_match.group(1).strip()[:200] if cl_match else "(kein Current Learning)"
        result.append({"domain": domain, "file": md.name, "confidence": conf, "current": current})
    # Failure-Memory
    fm = FAILURES_DIR / "Failure-Memory.md"
    if fm.exists():
        result.append({"domain": "Failures", "file": "Failure-Memory.md",
                       "confidence": "very high",
                       "current": "→ Failure-Memory prüfen: was in der Vergangenheit gescheitert ist"})
    return result


# ── Report ───────────────────────────────────────────────────────────────────

def regeln_report(cfg=None, nur_kritisch=False):
    lines = []
    z = lines.append
    z(f"\n{'═'*64}")
    z(f"  CONTRARIAN LAYER — Produktions-Pflichtprüfung")
    z(f"  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    z(f"{'═'*64}")

    # 1) Automatische Checks gegen cfg
    if cfg:
        z("\n▸ AUTOMATISCHE KONFIG-PRÜFUNG")
        z(f"  Konfig: {cfg.get('out', '?')}")
        fehler, warnungen, ok = [], [], []
        for domain, regel, conf, fn in PRODUKTIONS_REGELN:
            if fn is None:
                continue
            result, detail = fn(cfg)
            entry = f"  [{conf.upper()[:2]}] {domain}: {detail}"
            if result is False:
                fehler.append(f"  ✗ {entry}")
            elif result is None:
                warnungen.append(f"  ⚠ {entry}")
            else:
                if not nur_kritisch:
                    ok.append(f"  ✓ {entry}")

        if fehler:
            z("\n  FEHLER (blockierend):"); [z(f) for f in fehler]
        if warnungen:
            z("\n  WARNUNGEN:"); [z(w) for w in warnungen]
        if ok:
            z("\n  OK:"); [z(o) for o in ok]
        if not fehler and not warnungen:
            z("\n  Alle automatischen Checks bestanden ✓")

    # 2) Manuelle Checkliste
    z("\n▸ MANUELLE CHECKLISTE (vor Render/Upload abhaken)")
    domain_cur = None
    for domain, regel, conf, fn in PRODUKTIONS_REGELN:
        if fn is not None and cfg:
            continue  # auto-geprüft
        conf_level = CONFIDENCE_ORDER.get(conf.lower(), 0)
        if nur_kritisch and conf_level < 3:
            continue
        if domain != domain_cur:
            z(f"\n  [{domain}]")
            domain_cur = domain
        star = "★" if conf_level >= 4 else "·"
        z(f"  {star} □ {regel}")

    # 3) Vault-Learnings Kurzübersicht
    if not nur_kritisch:
        z("\n▸ VAULT-LEARNINGS (aktuelle Kurzfassung)")
        for l in lade_vault_learnings():
            conf_level = CONFIDENCE_ORDER.get(l["confidence"], 0)
            stars = "★" * conf_level
            z(f"\n  {stars} [{l['domain']}] {l['file']}")
            for ln in l["current"][:120].split("\n")[:3]:
                z(f"    {ln}")

    z(f"\n{'═'*64}\n")
    return "\n".join(lines)


if __name__ == "__main__":
    args = sys.argv[1:]
    nur_kurz = "--kurz" in args
    cfg_file = next((a for a in args if a.endswith(".json") and not a.startswith("-")), None)

    cfg = None
    if cfg_file:
        try:
            cfg = json.load(open(cfg_file, encoding="utf-8"))
        except Exception as e:
            print(f"FEHLER beim Lesen von {cfg_file}: {e}")
            sys.exit(1)

    print(regeln_report(cfg=cfg, nur_kritisch=nur_kurz))
