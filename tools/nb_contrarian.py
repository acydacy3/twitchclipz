"""
Contrarian-Layer: Cross-Cutting-Gate für alle Produktionsdomänen
                  + neutraler Peer-Reviewer für Hypothesen/Experimente/Observations.

Nutzung:
    python3 tools/nb_contrarian.py                   # Vollständiger Bericht
    python3 tools/nb_contrarian.py short07.json       # + Produktions-Audit gegen Konfig
    python3 tools/nb_contrarian.py --kurz             # Nur HIGH+VERY_HIGH + alle Forderungen
    python3 tools/nb_contrarian.py --wissenschaft     # Nur Hypothesen/Experimente/Observations

Ausgabe-Typen:
    FORDERUNG   — welcher Beweis noch fehlt
    GEGENTHESE  — alternative Erklärung, die ausgeschlossen werden muss
    FRAGIL      — Confidence zu hoch für die Stichprobengröße
    ÜBERFÄLLIG  — Experiment läuft zu lang ohne Auswertung
    VERALTET    — Learning seit >30 Tagen nicht aktualisiert
"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime, date

VAULT    = Path(__file__).resolve().parent.parent / "YouTube-Knowledge"
LEARN    = VAULT / "01-Learnings"
FAILURES = VAULT / "09-Failures"
HYPO     = VAULT / "07-Hypotheses"
EXP      = VAULT / "02-Experiments" / "Active"
OBS_FILE = VAULT / "07-Analytics" / "Observations.md"

CONFIDENCE_ORDER = {"very high": 4, "high": 3, "medium": 2, "low": 1}
N_FUER_HIGH      = 15   # Mindeststichprobe für High Confidence
N_FUER_VERY_HIGH = 30   # Mindeststichprobe für Very High


# ═══════════════════════════════════════════════════════════════════
# TEIL 1 — PRODUKTIONS-REGELN (automatisch + manuell)
# ═══════════════════════════════════════════════════════════════════

def _check_musik_db(cfg):
    mus = cfg.get("musik")
    if not mus:
        return True, "kein Musikbett konfiguriert"
    db = mus.get("db", -21)
    if db < -18:
        return False, f"musik.db={db} — muss ≥ -18 sein (Ziel -16), sonst unhörbar"
    return True, f"musik.db={db} ✓"

def _check_hook(cfg):
    if not cfg.get("hook"):
        return False, "kein 'hook'-Key — Hook ist Pflicht für Retention"
    txt = cfg["hook"].get("text", "")
    if len(txt) < 10:
        return False, f"Hook-Text zu kurz ({len(txt)} Zeichen)"
    return True, f"Hook: '{txt[:55]}' ✓"

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
        return None, f"Titel {len(title)} Zeichen — prüfe Keyword-Aussage bei Zeichen 35"
    return True, f"Titel {len(title)} Zeichen ✓"

def _check_no_emoji_titel(cfg):
    title = cfg.get("titel") or cfg.get("title") or cfg.get("metadata", {}).get("title", "")
    if not title:
        return True, "kein Titel"
    if re.search(r"[\U00010000-\U0010ffff]", title):
        return False, "Emoji im Titel — laut Learning verboten"
    return True, "kein Emoji im Titel ✓"

def _check_shots_count(cfg):
    n = len(cfg.get("shots", []))
    if n < 2:
        return False, f"nur {n} Shot(s) — Minimum 2, besser 3-6"
    if n > 7:
        return None, f"{n} Shots — prüfe ob alle notwendig (Richtwert 2-6)"
    return True, f"{n} Shots ✓"

def _check_audio(cfg):
    return (True, "audio ✓") if cfg.get("audio") else (False, "kein 'audio'-Key — VO fehlt")

def _check_words(cfg):
    return (True, "words ✓") if cfg.get("words") else (False, "kein 'words'-Key — Karaoke fehlt")

def _check_font(cfg):
    return (True, "font_black ✓") if cfg.get("font_black") else (False, "kein 'font_black'-Key")


PRODUKTIONS_REGELN = [
    ("Ton",      "Musik db ≥ -18 dB (Ziel -16) — V1–V5 Fehler",                           "very high", _check_musik_db),
    ("Hook",     "Jeder Short MUSS einen Hook haben",                                       "very high", _check_hook),
    ("Hook",     "Hook ≤ 4 s sichtbar",                                                     "high",      _check_hook_until),
    ("Titel",    "Aussage bei Zeichen 35 fertig — DE-Komposita brechen bei ~40 ab",        "very high", _check_titel_laenge),
    ("Titel",    "Kein Emoji im Titel",                                                     "high",      _check_no_emoji_titel),
    ("Editing",  "2–6 Shots je Short",                                                      "high",      _check_shots_count),
    ("Editing",  "VO (audio) MUSS gesetzt sein",                                            "very high", _check_audio),
    ("Captions", "words-File (Karaoke) MUSS gesetzt sein",                                 "very high", _check_words),
    ("Editing",  "font_black MUSS gesetzt sein",                                            "high",      _check_font),
    # Manuell
    ("Hook",     "Hook-Text NICHT identisch mit gesprochenem Satz",                        "very high", None),
    ("Captions", "Untertitel = Stimme 1:1 — kein abweichender Text außer als Experiment", "very high", None),
    ("Bilder",   "Schlüsselmomente IMMER generieren, nicht nur Stock",                     "high",      None),
    ("Bilder",   "Kontaktabzug QC-Check vor Upload",                                       "high",      None),
    ("SEO",      "Min. 1 starkes Keyword im Titel",                                        "very high", None),
    ("SEO",      "nb_suggest.py + nb_trends.py vor Titel-Entscheidung laufen",            "high",      None),
    ("Retention","Sichere Zone 19–39 s — tote Sekunden raus",                              "high",      None),
    ("Ton",      "volumedetect nach Render — Musik MUSS hörbar sein",                     "very high", None),
    ("Upload",   "analyse.py vor Upload prüfen: letzte terminierte Slots",                 "high",      None),
    ("Upload",   "TikTok NIE automatisch — Nutzer lädt selbst hoch",                      "very high", None),
    ("Persistenz","git commit + push nach jeder Session",                                  "very high", None),
    ("Persistenz","Neue Learnings sofort in Vault notieren",                               "high",      None),
]


# ═══════════════════════════════════════════════════════════════════
# TEIL 2 — WISSENSCHAFTS-LAYER: Hypothesen / Experimente / Observations
# ═══════════════════════════════════════════════════════════════════

def _parse_frontmatter(text):
    """Extrahiert YAML-Frontmatter als dict (nur einfache key: value-Zeilen)."""
    fm = {}
    if not text.startswith("---"):
        return fm
    end = text.find("\n---", 3)
    if end == -1:
        return fm
    for line in text[3:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def _n_aus_text(text):
    """Sucht n=XX in Text, gibt int oder None."""
    m = re.search(r"\bn\s*=\s*(\d+)", text, re.IGNORECASE)
    return int(m.group(1)) if m else None


def _tage_seit(datum_str):
    """Tage seit einem YYYY-MM-DD-String, oder None."""
    try:
        d = date.fromisoformat(datum_str.strip())
        return (date.today() - d).days
    except Exception:
        return None


# ── Hypothesen-Review ────────────────────────────────────────────

def analysiere_hypothesen():
    """
    Liest 07-Hypotheses/*.md und wertet sie gegen verfügbare Snapshot-Daten aus.
    Kein Formular-Check — direkte Gegenthesen und Datenbewertung.
    """
    findings = []
    if not HYPO.exists():
        return findings

    videos    = _lade_letzten_snapshot()
    kanal_avg = _kanal_avg(videos)

    for md in sorted(HYPO.glob("*.md")):
        if "Übersicht" in md.name or "Template" in md.name:
            continue
        text = md.read_text(encoding="utf-8")
        fm   = _parse_frontmatter(text)
        name = md.stem
        conf = fm.get("confidence", "unbekannt").lower()
        conf_level = CONFIDENCE_ORDER.get(conf, 0)
        n_doc = _n_aus_text(text)

        issues = []

        # ── Hypothesen-spezifische Datenbewertung ──────────────
        if "hook" in name.lower() and "laenge" in name.lower():
            issues.append(
                "  GEGENTHESE: 'Hook schlägt Länge' ist nicht falsifizierbar ohne "
                "Operationalisierung von Hook-Qualität. Was ist ein 'guter Hook'? "
                "Solange das nicht messbar ist, erklärt die Hypothese alles — und damit nichts."
            )
            issues.append(
                "  DATENLAGE: Hook-Qualität und Länge wurden nie sauber getrennt. "
                "Einzig valider Test: gleicher Hook-Text, zwei Schnittlängen (z.B. 18s vs. 35s), "
                "AVP% Tag 4–5 vergleichen."
            )
            if conf_level >= 3:
                issues.append(
                    f"  FRAGIL: Confidence '{conf}' ohne kontrollierten Test. "
                    "Als operative Heuristik vertretbar — nicht als bewiesene Regel behandeln."
                )

        elif "titel" in name.lower() or "formel" in name.lower() or "ueberlebens" in name.lower():
            # Daten-Check: San-José-Views vs. Kanal-Ø
            n_sj, avg_sj = _serien_views(videos, ["san jose", "jascon"])
            if avg_sj > 0 and kanal_avg > 0:
                faktor = round(avg_sj / kanal_avg, 1)
                issues.append(
                    f"  DATENLAGE: San-José-Serien (n={n_sj}) Ø {avg_sj} Views "
                    f"vs. Kanal-Ø {kanal_avg}. Faktor {faktor}x"
                )
            else:
                issues.append(
                    f"  DATENLAGE: San-José-Daten nicht im Snapshot (n={n_sj})."
                )
            issues.append(
                "  GEGENTHESE #1 — Alterseffekt: San José ist eine der ersten Serien. "
                "Mehr Zeit im Index = mehr Zeit für View-Accumulation. "
                "Kausalschluss 'Titel → Views' nicht möglich ohne Altersbereinigung."
            )
            issues.append(
                "  GEGENTHESE #2 — Themeneffekt: Luftblase unter Wasser ist physikalisch "
                "faszinierend (Okene ebenfalls Outlier). Thema schlägt möglicherweise Titel-Formel."
            )
            issues.append(
                "  BELASTBARER TEST: Gleiche Themen-Kategorie, Titel-Variante A vs. B, "
                "CTR in ersten 48 h messen — entsteht natürlich wenn V8 mit Ralston zwei "
                "parallele Titel-Tests bekommt (unterschiedliche Shorts, gleiche Geschichte)."
            )

        # Allgemein: Confidence vs. Stichprobe
        if conf_level >= 3 and n_doc and n_doc < N_FUER_HIGH:
            issues.append(
                f"  FRAGIL: n={n_doc} bei Confidence '{conf}'. "
                f"High erfordert n≥{N_FUER_HIGH} — aktuell Heuristik, kein Beweis."
            )

        if issues:
            findings.append((name, conf, issues))

    return findings


# ── Snapshot laden ───────────────────────────────────────────────

def _lade_letzten_snapshot():
    snap_dir = VAULT / "07-Analytics" / "snapshots"
    if not snap_dir.exists():
        return []
    snaps = sorted(snap_dir.glob("*.json"))
    if not snaps:
        return []
    return json.loads(snaps[-1].read_text(encoding="utf-8")).get("videos", [])


def _serien_views(videos, keywords):
    """Gibt (n, avg_views) für Videos zurück deren Titel eines der Keywords enthält."""
    treffer = [v for v in videos
               if any(k.lower() in v.get("title", "").lower() for k in keywords)
               and v.get("status") == "public" and v.get("views", 0) > 0]
    if not treffer:
        return 0, 0
    avg = sum(v["views"] for v in treffer) / len(treffer)
    return len(treffer), round(avg)


def _kanal_avg(videos):
    pub = [v for v in videos if v.get("status") == "public" and v.get("views", 0) > 0]
    if not pub:
        return 0
    return round(sum(v["views"] for v in pub) / len(pub))


# ── Experiment-Review ────────────────────────────────────────────

# Bekannte natürliche Experimente im Kanal — werden gegen echte Snapshot-Daten
# ausgewertet, nicht gegen Formular-Metadaten. Kein start_date nötig.
# Format: (name, gruppen: [(label, keywords)], frage, einschraenkung)
NATUERLICHE_EXPERIMENTE = [
    (
        "Animation-Opener vs. Ken-Burns",
        [
            ("Mit Manim/Animation", ["lengede", "nutty putty", "prosperi"]),
            ("Nur Ken-Burns",       ["tham luang", "san jose", "okene", "koepcke"]),
        ],
        "Schlagen Animations-Opener (V5/V6/V7) reine Standbild-Serien (V1–V4) in Views/Short?",
        "EINSCHRÄNKUNG: Themen-Effekt und Serienreihenfolge (ältere Serien = mehr Zeit) "
        "können nicht getrennt werden. Konfundierung hoch. Ergebnis ist Indiz, kein Beweis.",
    ),
    (
        "Überlebens-Titel vs. Chronik-Titel",
        [
            ("Überlebens-Frame", ["san jose", "okene", "prosperi", "nutty putty"]),
            ("Chronik-Frame",    ["tham luang", "koepcke", "lengede"]),
        ],
        "Performen Serien mit Überlebens-Perspektive im Titel besser als Chronik-Erzählungen?",
        "EINSCHRÄNKUNG: Themen-Effekt (physikalisch faszinierend vs. Standard) nicht trennbar. "
        "Für Beweis: gleiche Themen-Kategorie, zwei Titel-Varianten, CTR Tag 1 vergleichen.",
    ),
]

# Experimente die echte AVP%/CTR-Daten brauchen — aktuell nicht auswertbar
NICHT_AUSWERTBAR = [
    ("Hook-Banner-abweichender-Text",
     "Braucht 3-s-Retention je Short (YouTube Analytics). "
     "Wird auswertbar wenn V3-Koepcke-Daten (Tag 7+) per Analytics-API gezogen werden. "
     "Kein Nutzer-Handlungsbedarf — Daten entstehen durch Produktion."),
    ("Experiment-TikTok-Lange-Schnitte",
     "TikTok-Analytics nicht in der Snapshot-Pipeline. "
     "Wird auswertbar wenn Buffer-Insights oder manueller Export verfügbar sind."),
    ("Experiment-Remotion-Motion-Graphics",
     "Remotion noch nicht in Produktion eingesetzt. "
     "Datenpfad entsteht automatisch wenn erstes Remotion-Short live geht."),
]


def analysiere_experimente():
    """
    Wertet natürliche Experimente direkt gegen Snapshot-Daten aus.
    Kein Formular, keine Metadaten-Hygiene — nur: was sagen die Zahlen?
    """
    findings = []
    videos = _lade_letzten_snapshot()
    if not videos:
        findings.append(("KEIN SNAPSHOT", "?", ["  Kein Snapshot geladen — nb_analytics_snapshot.py laufen lassen."]))
        return findings

    kanal_avg = _kanal_avg(videos)
    findings.append((f"Kanal-Ø (Public, n≥1 View)", "Referenz",
                     [f"  Kanal-Ø: {kanal_avg} Views/Short"]))

    for name, gruppen, frage, einschraenkung in NATUERLICHE_EXPERIMENTE:
        issues = [f"  FRAGE: {frage}"]
        gruppe_results = []
        for label, keywords in gruppen:
            n, avg = _serien_views(videos, keywords)
            gruppe_results.append((label, n, avg))
            issues.append(f"  {label}: n={n} öffentliche Shorts, Ø {avg} Views")

        if len(gruppe_results) == 2:
            (la, na, aa), (lb, nb, ab) = gruppe_results
            if na >= 3 and nb >= 3 and ab > 0:
                faktor = round(aa / ab, 2) if ab else "–"
                richtung = "besser" if aa > ab else "schlechter"
                issues.append(
                    f"  VORLÄUFIGES ERGEBNIS: {la} Ø {aa} vs. {lb} Ø {ab} "
                    f"→ Faktor {faktor}× ({richtung})"
                )
                if abs(aa - ab) < 0.2 * max(aa, ab):
                    issues.append("  BEWERTUNG: Unterschied <20% — kein klares Signal.")
                elif faktor > 1.5 or faktor < 0.67:
                    issues.append("  BEWERTUNG: Deutlicher Unterschied — Hypothese prüfen.")
            else:
                issues.append(f"  DATENLAGE: zu wenig öffentliche Daten für Auswertung (min. 3 je Gruppe)")
            issues.append(f"  {einschraenkung}")

        findings.append((name, "natürlich", issues))

    # Nicht auswertbare Experimente
    for name, grund in NICHT_AUSWERTBAR:
        findings.append((name, "kein Datenpfad", [f"  DATENPFAD: {grund}"]))

    return findings


# ── Observations-Review ──────────────────────────────────────────

def analysiere_observations():
    """
    Liest 07-Analytics/Observations.md.
    Fordert für [beobachtet]-Einträge alternative Erklärungen.
    Prüft welche Observations lange keine Hypothese erzeugt haben.
    """
    findings = []
    if not OBS_FILE.exists():
        return findings

    text = OBS_FILE.read_text(encoding="utf-8")
    eintraege = re.findall(r"- \[(\d{4}-\d{2}-\d{2})\]\s+(.+?)(?=\n|$)", text)

    beobachtet_ohne_hypo = []
    muster_ohne_exp      = []

    for datum, inhalt in eintraege:
        tage = _tage_seit(datum)
        tag  = "[beobachtet]" if "[beobachtet]" in inhalt else \
               "[Muster]"     if "[Muster]"     in inhalt else \
               "[bestätigt]"  if "[bestätigt]"  in inhalt else \
               "[widerlegt]"  if "[widerlegt]"  in inhalt else None

        if tag == "[beobachtet]" and tage and tage >= 7:
            beobachtet_ohne_hypo.append((datum, inhalt[:100].strip(), tage))
        elif tag == "[Muster]":
            muster_ohne_exp.append((datum, inhalt[:100].strip()))

    if beobachtet_ohne_hypo:
        findings.append(("BEOBACHTUNGEN ohne Hypothese", beobachtet_ohne_hypo))
    if muster_ohne_exp:
        findings.append(("MUSTER ohne Experiment", muster_ohne_exp))

    # Bekannte Observations gegen-lesen
    findings.append(("GEGENTHESEN zu aktuellen Observations", [
        ("Länge-Observation 26.08.",
         "Lange Videos existieren länger → more time to accumulate views. "
         "Nicht Länge, sondern Alter. Kohortenvergleich nötig: "
         "gleich alte kurze vs. lange Videos in ersten 48 h."),
        ("San-José-Outlier 26.08.",
         "San José ist ein Themen-Outlier (Luftblase = physikalisch faszinierend), "
         "kein Titel-Formeln-Beweis. Für Titel-These: gleiche Themen-Kategorie, Titel A vs. B, "
         "CTR Day-1 vergleichen."),
        ("Tags 100% = kein A/B-Vergleich",
         "SEO-Korrelation kann nicht gemessen werden, solange alle Videos Tags haben. "
         "Entweder 2–3 Shorts ohne Tags testen, oder SEO-These als 'nicht testbar' markieren."),
    ]))

    return findings


# ── Learning-Claims-Review ───────────────────────────────────────

def analysiere_learnings():
    """
    Liest alle 01-Learnings/*.md.
    Flaggt: n zu klein für die Confidence, veraltete Learnings ohne Update,
    fehlende Counter-Evidence.
    """
    findings = []
    heute = date.today()

    for md in sorted(LEARN.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        fm   = _parse_frontmatter(text)
        name = md.stem
        conf = fm.get("confidence", "").lower()
        conf_level = CONFIDENCE_ORDER.get(conf, 0)

        # Update-Datum prüfen
        updated = fm.get("updated", "").strip()
        tage_alt = _tage_seit(updated) if updated else None

        n = _n_aus_text(text)
        has_counter = bool(re.search(r"counter.?evidence|gegenbewei|widerleg|contra|aufgelöst", text, re.IGNORECASE))

        issues = []

        if conf_level >= 3 and n and n < N_FUER_HIGH:
            issues.append(
                f"FRAGIL: Confidence '{conf}' bei n={n} — "
                f"braucht n≥{N_FUER_HIGH} für 'high'"
            )
        if conf_level >= 4 and n and n < N_FUER_VERY_HIGH:
            issues.append(
                f"FRAGIL: Confidence 'very high' bei n={n} — "
                f"braucht n≥{N_FUER_VERY_HIGH} für 'very high'"
            )
        if conf_level >= 3 and not has_counter:
            issues.append(
                "FORDERUNG: kein Counter-Evidence-Abschnitt — "
                "was würde dieses Learning widerlegen?"
            )
        if tage_alt and tage_alt > 30 and conf_level >= 3:
            issues.append(
                f"VERALTET?: letztes Update vor {tage_alt} Tagen ({updated}). "
                "Hat sich die Evidenzlage verändert?"
            )

        if issues:
            findings.append((name, conf, issues))

    return findings


# ═══════════════════════════════════════════════════════════════════
# TEIL 3 — VAULT-LEARNINGS (Kurzübersicht)
# ═══════════════════════════════════════════════════════════════════

def lade_vault_learnings():
    result = []
    for md in sorted(LEARN.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        fm   = _parse_frontmatter(text)
        conf = fm.get("confidence", "").lower()
        domain = md.parent.name if md.parent.name != "01-Learnings" else "Allgemein"
        cl_match = re.search(r"## Current Learning\s*\n(.+?)(?=\n##|\Z)", text, re.DOTALL)
        current = cl_match.group(1).strip()[:180] if cl_match else "(kein Current Learning)"
        result.append({"domain": domain, "file": md.name, "confidence": conf, "current": current})
    fm_file = FAILURES / "Failure-Memory.md"
    if fm_file.exists():
        result.append({"domain": "Failures", "file": "Failure-Memory.md",
                       "confidence": "very high",
                       "current": "→ Failure-Memory prüfen: was nicht funktioniert hat"})
    return result


# ═══════════════════════════════════════════════════════════════════
# AUSGABE
# ═══════════════════════════════════════════════════════════════════

def regeln_report(cfg=None, nur_kritisch=False, nur_wissenschaft=False):
    lines = []
    z = lines.append

    z(f"\n{'═'*64}")
    z(f"  CONTRARIAN LAYER  —  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    z(f"{'═'*64}")

    # ── A) Produktions-Gate ───────────────────────────────────────
    if not nur_wissenschaft:
        if cfg:
            z("\n▸ PRODUKTIONS-AUDIT (automatisch)")
            z(f"  Konfig: {cfg.get('out', '?')}")
            fehler, warnungen, ok_lst = [], [], []
            for domain, regel, conf, fn in PRODUKTIONS_REGELN:
                if fn is None:
                    continue
                res, detail = fn(cfg)
                entry = f"  [{conf[:2].upper()}] {domain}: {detail}"
                if res is False:
                    fehler.append(f"  ✗ {entry}")
                elif res is None:
                    warnungen.append(f"  ⚠ {entry}")
                else:
                    if not nur_kritisch:
                        ok_lst.append(f"  ✓ {entry}")
            if fehler:
                z("\n  FEHLER (blockierend):"); [z(f) for f in fehler]
            if warnungen:
                z("\n  WARNUNGEN:"); [z(w) for w in warnungen]
            if ok_lst:
                z("\n  OK:"); [z(o) for o in ok_lst]
            if not fehler and not warnungen:
                z("\n  Alle automatischen Checks bestanden ✓")

        z("\n▸ MANUELLE CHECKLISTE (vor Render/Upload abhaken)")
        domain_cur = None
        for domain, regel, conf, fn in PRODUKTIONS_REGELN:
            if fn is not None and cfg:
                continue
            conf_level = CONFIDENCE_ORDER.get(conf.lower(), 0)
            if nur_kritisch and conf_level < 3:
                continue
            if domain != domain_cur:
                z(f"\n  [{domain}]")
                domain_cur = domain
            star = "★" if conf_level >= 4 else "·"
            z(f"  {star} □ {regel}")

    # ── B) Hypothesen ─────────────────────────────────────────────
    hypo_findings = analysiere_hypothesen()
    if hypo_findings:
        z(f"\n{'─'*64}")
        z("▸ HYPOTHESEN-REVIEW (neutraler Peer-Reviewer)")
        z("  Maßstab: Medium=plausibel, High=n≥15+Test, Very High=n≥30+repliziert")
        for name, conf, issues in hypo_findings:
            if not issues:
                continue
            z(f"\n  ◆ {name}  [Confidence: {conf}]")
            for iss in issues:
                z(iss)

    # ── C) Experimente ────────────────────────────────────────────
    exp_findings = analysiere_experimente()
    if exp_findings:
        z(f"\n{'─'*64}")
        z("▸ EXPERIMENT-REVIEW")
        for name, status, issues in exp_findings:
            if not issues:
                continue
            z(f"\n  ◆ {name}  [Status: {status}]")
            for iss in issues:
                z(iss)

    # ── D) Observations ───────────────────────────────────────────
    obs_findings = analysiere_observations()
    if obs_findings:
        z(f"\n{'─'*64}")
        z("▸ OBSERVATIONS-REVIEW")
        for gruppe, eintraege in obs_findings:
            z(f"\n  ◆ {gruppe}")
            for item in eintraege:
                if isinstance(item, tuple) and len(item) == 3:
                    datum, inhalt, tage = item
                    z(f"    [{datum}, {tage}d alt] {inhalt}")
                    z(f"    → FORDERUNG: Hypothese ableiten oder als 'Artefakt' markieren")
                elif isinstance(item, tuple) and len(item) == 2:
                    label, gegenthese = item
                    z(f"    [{label}]")
                    z(f"    GEGENTHESE: {gegenthese}")

    # ── E) Learning-Claims ────────────────────────────────────────
    learning_findings = analysiere_learnings()
    if learning_findings and not nur_kritisch:
        z(f"\n{'─'*64}")
        z("▸ LEARNING-CLAIMS-REVIEW (Evidenzqualität)")
        for name, conf, issues in learning_findings:
            z(f"\n  ◆ {name}  [{conf}]")
            for iss in issues:
                z(f"    {iss}")

    # ── F) Vault-Learnings Kurzübersicht ─────────────────────────
    if not nur_kritisch and not nur_wissenschaft:
        z(f"\n{'─'*64}")
        z("▸ VAULT-LEARNINGS (Kurzfassung)")
        for l in lade_vault_learnings():
            conf_level = CONFIDENCE_ORDER.get(l["confidence"], 0)
            stars = "★" * conf_level
            z(f"\n  {stars} [{l['domain']}] {l['file']}")
            for ln in l["current"].split("\n")[:2]:
                z(f"    {ln}")

    z(f"\n{'═'*64}\n")
    return "\n".join(lines)


if __name__ == "__main__":
    args          = sys.argv[1:]
    nur_kurz      = "--kurz" in args
    nur_wiss      = "--wissenschaft" in args
    cfg_file      = next((a for a in args if a.endswith(".json") and not a.startswith("-")), None)

    cfg = None
    if cfg_file:
        try:
            cfg = json.load(open(cfg_file, encoding="utf-8"))
        except Exception as e:
            print(f"FEHLER beim Lesen von {cfg_file}: {e}")
            sys.exit(1)

    print(regeln_report(cfg=cfg, nur_kritisch=nur_kurz, nur_wissenschaft=nur_wiss))
