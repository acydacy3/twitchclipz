#!/usr/bin/env python3
"""Autonomer Beobachtungs-Motor — Observation Engine.

Vergleicht Analytics-Snapshots, generiert Observations und bewertet Experimente.

Aufruf:
    python3 tools/nb_observe.py             Voller Bericht
    python3 tools/nb_observe.py --kurz      Nur Highlights (für Statusbericht)
    python3 tools/nb_observe.py --vault     Observations in Vault schreiben

Was der Motor tut (ohne Nutzereingabe):
  1. Lädt die 2 neuesten Snapshots → berechnet Deltas (Views, Abos, Likes/View)
  2. Rankt Videos nach Views (Top-Performer / Underperformer)
  3. Korreliert Länge (<22 s vs. ≥22 s) mit Views → Längenthese prüfen
  4. Korreliert Tags-vorhanden mit Views → SEO-These prüfen
  5. Prüft aktive Experimente auf ausreichende Datenlage (≥3 Datenpunkte/≥7 Tage)
  6. Generiert Observation-Texte nach Evidenzlage
  7. Erkennt Anomalien: ein Video 5× über Kanal-Schnitt → Pattern-Interrupt?
  8. Optional: schreibt Observations nach YouTube-Knowledge/07-Analytics/
"""

import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SNAP_DIR = ROOT / "YouTube-Knowledge" / "07-Analytics" / "snapshots"
EXP_DIR = ROOT / "YouTube-Knowledge" / "02-Experiments" / "Active"
OBS_DIR = ROOT / "YouTube-Knowledge" / "07-Analytics"
OBS_DIR.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------- Hilfsfunktionen

def lade_snapshots(n=2):
    snaps = sorted(SNAP_DIR.glob("*.json"))
    if not snaps:
        return []
    auswahl = snaps[-n:]
    return [json.loads(p.read_text(encoding="utf-8")) for p in auswahl]


def iso_zu_sek(iso: str) -> int:
    if not iso:
        return 0
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso)
    if not m:
        return 0
    h, mi, s = (int(x or 0) for x in m.groups())
    return h * 3600 + mi * 60 + s


def video_alter_tage(published: str) -> float:
    if not published:
        return 999
    try:
        pub = datetime.fromisoformat(published.replace("Z", "+00:00"))
        return (datetime.now(pub.tzinfo) - pub).days
    except Exception:
        return 999


# ---------------------------------------------------------------- Analyse-Funktionen

def delta_kanal(snaps):
    """Vergleicht zwei Snapshots → Kanal-Delta."""
    if len(snaps) < 2:
        return None
    a, b = snaps[0], snaps[1]
    return {
        "zeitraum_tage": (
            datetime.fromisoformat(b["snapshot_date"]) -
            datetime.fromisoformat(a["snapshot_date"])
        ).days,
        "views_delta": b.get("total_views", 0) - a.get("total_views", 0),
        "subs_delta": b.get("subscribers", 0) - a.get("subscribers", 0),
        "video_count_delta": b.get("video_count", 0) - a.get("video_count", 0),
        "datum_a": a["snapshot_date"],
        "datum_b": b["snapshot_date"],
    }


def laengen_analyse(videos):
    """Prüft Längen-These: kurz (<22 s) vs. lang (≥22 s)."""
    kurz = [v for v in videos if iso_zu_sek(v.get("duration_iso", "")) < 22 and v.get("status") == "public"]
    lang = [v for v in videos if iso_zu_sek(v.get("duration_iso", "")) >= 22 and v.get("status") == "public"]

    def schnitt(gruppe):
        if not gruppe:
            return 0
        return sum(v.get("views", 0) for v in gruppe) / len(gruppe)

    return {
        "kurz_n": len(kurz),
        "kurz_schnitt": schnitt(kurz),
        "lang_n": len(lang),
        "lang_schnitt": schnitt(lang),
        "faktor": (schnitt(kurz) / schnitt(lang)) if schnitt(lang) > 0 else 0,
    }


def top_performer(videos, n=3):
    """Top-N öffentliche Videos nach Views."""
    oeffentlich = [v for v in videos if v.get("status") == "public"]
    return sorted(oeffentlich, key=lambda v: v.get("views", 0), reverse=True)[:n]


def underperformer(videos, n=3):
    """Bottom-N öffentliche Videos nach Views (≥7 Tage alt)."""
    oeffentlich = [
        v for v in videos
        if v.get("status") == "public" and video_alter_tage(v.get("published", "")) >= 7
    ]
    return sorted(oeffentlich, key=lambda v: v.get("views", 0))[:n]


def anomalie_check(videos):
    """Videos die 5× über Kanal-Schnitt → Outlier / Muster-Kandidaten."""
    oeffentlich = [v for v in videos if v.get("status") == "public"]
    if not oeffentlich:
        return []
    schnitt = sum(v.get("views", 0) for v in oeffentlich) / len(oeffentlich)
    return [v for v in oeffentlich if v.get("views", 0) >= 5 * schnitt]


def seo_korrelation(videos):
    """Views bei Videos mit Tags vs. ohne Tags."""
    mit = [v for v in videos if v.get("status") == "public" and v.get("tags")]
    ohne = [v for v in videos if v.get("status") == "public" and not v.get("tags")]

    def schnitt(g):
        return sum(v.get("views", 0) for v in g) / len(g) if g else 0

    return {
        "mit_tags_n": len(mit),
        "mit_tags_schnitt": schnitt(mit),
        "ohne_tags_n": len(ohne),
        "ohne_tags_schnitt": schnitt(ohne),
    }


def experimente_bewerten():
    """Liest aktive Experimente und prüft Datenlage."""
    if not EXP_DIR.exists():
        return []

    ergebnisse = []
    for pfad in EXP_DIR.glob("*.md"):
        text = pfad.read_text(encoding="utf-8", errors="replace")
        # Status aus Frontmatter
        status_m = re.search(r"^status:\s*(\w+)", text, re.MULTILINE)
        status = status_m.group(1) if status_m else "unknown"
        if status not in ("active", "planned"):
            continue

        # Startdatum
        start_m = re.search(r"^start_date:\s*(.+)", text, re.MULTILINE)
        start_raw = start_m.group(1).strip() if start_m else ""
        alter_tage = 0
        if start_raw and start_raw not in ("", "null", "None"):
            try:
                start = datetime.fromisoformat(start_raw)
                alter_tage = (datetime.now() - start).days
            except Exception:
                pass

        # Hat bereits Ergebnis?
        result_m = re.search(r"^result:\s*[\"']?(.+)[\"']?", text, re.MULTILINE)
        hat_ergebnis = bool(result_m and result_m.group(1).strip() not in ("", '""', "''"))

        name = pfad.stem
        bereit = alter_tage >= 7 and not hat_ergebnis
        ergebnisse.append({
            "name": name,
            "status": status,
            "alter_tage": alter_tage,
            "hat_ergebnis": hat_ergebnis,
            "bereit_fuer_auswertung": bereit,
        })

    return ergebnisse


# ---------------------------------------------------------------- Observation-Generator

def generiere_observations(snaps, videos):
    """Erzeugt Observation-Texte aus den Analysedaten."""
    obs = []
    heute = date.today().isoformat()

    # Delta
    delta = delta_kanal(snaps)
    if delta and delta["zeitraum_tage"] > 0:
        views_pro_tag = delta["views_delta"] / delta["zeitraum_tage"]
        obs.append(
            f"[{heute}] Kanal-Delta {delta['datum_a']}→{delta['datum_b']}: "
            f"+{delta['views_delta']} Views in {delta['zeitraum_tage']} Tagen "
            f"({views_pro_tag:.0f}/Tag), +{delta['subs_delta']} Abos, "
            f"+{delta['video_count_delta']} Videos."
        )

    # Längen-These
    la = laengen_analyse(videos)
    if la["kurz_n"] >= 3 and la["lang_n"] >= 3:
        if la["faktor"] > 1.2:
            obs.append(
                f"[{heute}] OBSERVATION: Kurze Videos (<22 s, n={la['kurz_n']}) "
                f"zeigen {la['faktor']:.1f}× mehr Views als lange (n={la['lang_n']}). "
                f"Stärkt Längenthese."
            )
        elif la["faktor"] < 0.8:
            obs.append(
                f"[{heute}] OBSERVATION: Lange Videos (≥22 s, n={la['lang_n']}) "
                f"outperformen kurze (Faktor {1/la['faktor']:.1f}×). "
                f"Widerspricht Längenthese — Counter-Evidence prüfen."
            )
        else:
            obs.append(
                f"[{heute}] Kein klarer Längeneffekt (Faktor {la['faktor']:.2f}, "
                f"kurz n={la['kurz_n']}, lang n={la['lang_n']}). Mehr Daten nötig."
            )

    # Anomalien
    outlier = anomalie_check(videos)
    for v in outlier:
        obs.append(
            f"[{heute}] OUTLIER: '{v['title'][:60]}' — {v['views']} Views "
            f"(≥5× Kanal-Schnitt). Hypothese: Was macht dieses Video anders?"
        )

    # SEO
    seo = seo_korrelation(videos)
    if seo["mit_tags_n"] >= 2 and seo["ohne_tags_n"] >= 2:
        if seo["mit_tags_schnitt"] > seo["ohne_tags_schnitt"] * 1.3:
            obs.append(
                f"[{heute}] SEO-Korrelation: Videos MIT Tags "
                f"({seo['mit_tags_n']}×): {seo['mit_tags_schnitt']:.0f} Views/Ø vs. "
                f"OHNE ({seo['ohne_tags_n']}×): {seo['ohne_tags_schnitt']:.0f} Views/Ø. "
                f"Positiver SEO-Effekt sichtbar."
            )

    # Top + Under
    tops = top_performer(videos)
    if tops:
        top_titel = [f"'{v['title'][:40]}' ({v['views']} Views)" for v in tops]
        obs.append(f"[{heute}] Top-Performer: {' | '.join(top_titel)}")

    under = underperformer(videos, n=2)
    if under:
        under_titel = [f"'{v['title'][:40]}' ({v['views']} Views)" for v in under]
        obs.append(f"[{heute}] Underperformer (≥7 Tage alt): {' | '.join(under_titel)}")

    return obs


# ---------------------------------------------------------------- Vault-Schreiben

def schreibe_vault(observations, experimente):
    """Fügt neue Observations in YouTube-Knowledge/07-Analytics/Observations.md ein."""
    pfad = OBS_DIR / "Observations.md"
    heute = date.today().isoformat()

    neu_block = f"\n## {heute} (automatisch)\n\n"
    for obs in observations:
        neu_block += f"- {obs}\n"

    # Experiment-Hinweise
    bereit = [e for e in experimente if e["bereit_fuer_auswertung"]]
    if bereit:
        neu_block += "\n**Experimente bereit zur Auswertung:**\n"
        for e in bereit:
            neu_block += f"- `{e['name']}` ({e['alter_tage']} Tage aktiv) → Daten jetzt auswerten!\n"

    if pfad.exists():
        bestehend = pfad.read_text(encoding="utf-8")
        # Neue Section direkt nach dem ersten '---' Block (YAML-Front-Matter Ende) einfügen
        # Suche die erste Leerzeile nach dem zweiten '---'
        teile = bestehend.split("---", 2)
        if len(teile) >= 3:
            inhalt = teile[0] + "---" + teile[1] + "---" + neu_block + teile[2]
        else:
            inhalt = bestehend + "\n" + neu_block
    else:
        header = (
            "---\ntype: analytics\ntitle: Observations\n"
            f"updated: {heute}\ntags: [analytics, observations, auto]\n---\n\n"
            "# Observations\n\n*Automatisch generiert von nb_observe.py*\n"
        )
        inhalt = header + neu_block

    pfad.write_text(inhalt, encoding="utf-8")
    print(f"Observations geschrieben: {pfad}")


# ---------------------------------------------------------------- Hauptprogramm

def main():
    kurz = "--kurz" in sys.argv
    vault = "--vault" in sys.argv

    snaps = lade_snapshots(2)
    if not snaps:
        print("Kein Snapshot vorhanden. Zuerst: python3 tools/nb_analytics_snapshot.py")
        return

    neuester = snaps[-1]
    videos = neuester.get("videos", [])
    heute = neuester.get("snapshot_date", date.today().isoformat())

    observations = generiere_observations(snaps, videos)
    experimente = experimente_bewerten()

    if kurz:
        print(f"=== Observation-Snapshot {heute} ===")
        oeffentlich = [v for v in videos if v.get("status") == "public"]
        kanal_schnitt = (
            sum(v.get("views", 0) for v in oeffentlich) / len(oeffentlich)
            if oeffentlich else 0
        )
        print(f"  Videos öffentlich: {len(oeffentlich)}  |  Ø {kanal_schnitt:.0f} Views")

        bereit = [e for e in experimente if e["bereit_fuer_auswertung"]]
        if bereit:
            print(f"  EXPERIMENTE BEREIT: {', '.join(e['name'] for e in bereit)}")
        outlier = anomalie_check(videos)
        if outlier:
            print(f"  OUTLIER: {outlier[0]['title'][:50]} ({outlier[0]['views']} Views)")
        for obs in observations[:3]:
            print(f"  {obs[:120]}")
        return

    # Voller Bericht
    print(f"\n{'='*64}")
    print(f"  OBSERVATION ENGINE — {heute}")
    print(f"{'='*64}")

    delta = delta_kanal(snaps)
    if delta:
        print(f"\n[KANAL-DELTA] {delta['datum_a']} → {delta['datum_b']}")
        print(f"  +{delta['views_delta']:,} Views in {delta['zeitraum_tage']} Tagen")
        print(f"  +{delta['subs_delta']} Abos  |  +{delta['video_count_delta']} Videos")

    la = laengen_analyse(videos)
    print(f"\n[LÄNGENDATEN]")
    print(f"  kurz (<22 s): n={la['kurz_n']}, Ø {la['kurz_schnitt']:.0f} Views")
    print(f"  lang (≥22 s): n={la['lang_n']}, Ø {la['lang_schnitt']:.0f} Views")
    if la["faktor"] > 0:
        print(f"  Faktor kurz/lang: {la['faktor']:.2f}")

    tops = top_performer(videos)
    print(f"\n[TOP-PERFORMER]")
    for v in tops:
        print(f"  {v['views']:>6} Views  {v['title'][:55]}")

    under = underperformer(videos, 3)
    print(f"\n[UNDERPERFORMER (≥7 Tage)]")
    for v in under:
        print(f"  {v['views']:>6} Views  {v['title'][:55]}")

    outlier = anomalie_check(videos)
    if outlier:
        print(f"\n[OUTLIER — 5× über Schnitt]")
        for v in outlier:
            print(f"  {v['views']:>6} Views  {v['title'][:55]}")
            print(f"           → Hypothese ableiten: Was macht dieses Video besonders?")

    seo = seo_korrelation(videos)
    print(f"\n[SEO-KORRELATION]")
    print(f"  mit Tags:  n={seo['mit_tags_n']}, Ø {seo['mit_tags_schnitt']:.0f} Views")
    print(f"  ohne Tags: n={seo['ohne_tags_n']}, Ø {seo['ohne_tags_schnitt']:.0f} Views")

    print(f"\n[EXPERIMENTE]")
    if experimente:
        for e in experimente:
            bereit_txt = " ← JETZT AUSWERTEN" if e["bereit_fuer_auswertung"] else ""
            print(f"  [{e['status']:8}] {e['name']}  ({e['alter_tage']} Tage){bereit_txt}")
    else:
        print("  Keine aktiven Experimente.")

    print(f"\n[OBSERVATIONS — automatisch generiert]")
    for obs in observations:
        print(f"  {obs[:120]}")

    print(f"\n{'='*64}")
    print("Tipp: --vault schreibt Observations in YouTube-Knowledge/07-Analytics/")
    print(f"{'='*64}\n")

    if vault:
        schreibe_vault(observations, experimente)


if __name__ == "__main__":
    main()
