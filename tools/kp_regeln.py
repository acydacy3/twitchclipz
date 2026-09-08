#!/usr/bin/env python3
"""kp_regeln.py — das Regel-Register. Einzige Quelle der Wahrheit.

WARUM ES DAS GIBT
-----------------
Der Befund vom 07.09.2026: Fuenf Produktionsregeln galten schriftlich, keine
einzige hatte einen Pruefpunkt im Code. Alle fuenf wurden gebrochen, waehrend
sie galten. Der Grund war nicht Nachlaessigkeit, sondern Bauart: eine Regel
lebte als Satz in einer Markdown-Datei, und die Instanz, die sie befolgen
sollte, war zugleich die einzige, die ihre Einhaltung pruefte.

Dieses Register dreht das um:

    Eine Regel EXISTIERT hier nur als Datensatz mit einem Feld `pruefung`.
    Ist das Feld leer, erscheint sie ueberall als UNGEDECKT -- im Gate, im
    Sitzungsbericht und in der erzeugten Vault-Notiz. Prosa kann sich nicht
    mehr als Durchsetzung ausgeben.

Jede Regel traegt ausserdem `herkunft`: den Fehler oder das Learning, aus dem
sie entstanden ist. Damit ist im Code selbst nachlesbar, was sie gekostet hat.

VERWENDUNG
----------
    python3 tools/kp_regeln.py                Deckungsgrad + Liste
    python3 tools/kp_regeln.py --ungedeckt    nur die Regeln ohne Pruefpunkt
    python3 tools/kp_regeln.py --markdown     Vault-Notiz erzeugen
    python3 tools/kp_regeln.py --json

Andere Werkzeuge importieren `REGELN` und rufen die Pruefungen auf; sie
implementieren keine eigenen Regeln. So kann Gate und Bericht nicht
auseinanderlaufen.
"""

import argparse
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TOKEN_RE = r"[^\W_]+(?:[-'][^\W_]+)*"
CAPTION_SCHWELLE = 0.98      # Wort-Uebereinstimmung Caption <-> Skript
MUSIK_MIN_DB = -18           # darunter war das Bett in V1-V5 unhoerbar
UNTERTITEL_HELL = 200        # Spitzenhelligkeit im Caption-Band (159 ohne / 235 mit)
UNTERTITEL_ABDECKUNG = 0.60  # Anteil der Laufzeit mit Untertiteln
LUFS_ZIEL = (-20.0, -11.0)   # YouTube normalisiert auf ~-14
LAENGE_ZONE = (19, 49)       # intern belegte Zone 19-39 s, A/B bis 49 s erlaubt
TITEL_MAX = 60
SNAPSHOT_MAX_TAGE = 1


# ═══════════════════════════════════════════════════ Hilfen

def tokens(text):
    return re.findall(TOKEN_RE, text)


def norm(s):
    return re.sub(r"[\W_]", "", s.lower())


def erste_datei(*kandidaten):
    for k in kandidaten:
        if k and os.path.exists(k):
            return k
    return None


def sh_dauer(pfad):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", pfad],
                       capture_output=True, text=True)
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


class Befund:
    """Ein Pruefergebnis. `hart` = blockiert Render/Upload."""

    def __init__(self, regel_id, titel, ok, text, hart=True, stelle=None):
        self.regel_id, self.titel = regel_id, titel
        self.ok, self.text, self.hart, self.stelle = ok, text, hart, stelle

    def __str__(self):
        z = "OK  " if self.ok else ("FEHL" if self.hart else "warn")
        s = f"  [{z}] {self.regel_id:<5} {self.titel:<22} {self.text}"
        if self.stelle:
            s += f"\n              -> {self.stelle}"
        return s

    def als_dict(self):
        return {"regel": self.regel_id, "titel": self.titel, "ok": self.ok,
                "hart": self.hart, "text": self.text, "stelle": self.stelle}


# ═══════════════════════════════════════════════════ Material

class Material:
    """Alles, was zu einem Short gehoert — traege geladen.

    Die Pruefungen bekommen dieses Objekt und suchen sich, was sie brauchen.
    Der Grund fuer die Sucherei: die Serien sind historisch unterschiedlich
    aufgebaut (skript/ vs. skripte/ vs. skripte.json, configs/*.json vs. ein
    SHORTS-Dict im Build-Skript). Ein Pruefer, der nur ein Format kennt, geht
    bei allen anderen still gruen — genau so blieb die Bewegtbild-Regel bei
    ralston wirkungslos.
    """

    def __init__(self, serie, num):
        self.serie, self.num = serie.rstrip("/"), num
        self._cache = {}

    # ── Skript ────────────────────────────────────────────────
    @property
    def skript(self):
        if "skript" in self._cache:
            return self._cache["skript"]
        pfad = text = None
        p = erste_datei(os.path.join(self.serie, "skript", f"short_{self.num}.txt"))
        if p:
            roh = open(p, encoding="utf-8").read()
            zl = roh.split("\n", 1)
            # Historische Titelzeile ("short_01") wegschneiden -- aber NUR
            # wenn es wirklich eine ist. Blindes Abschneiden loeschte schon
            # einmal den gesamten Text (F-V9-D).
            text = zl[1] if len(zl) > 1 and re.fullmatch(r"short_\d+\s*", zl[0]) else roh
            pfad = p
        elif os.path.exists(os.path.join(self.serie, "skripte.json")):
            p = os.path.join(self.serie, "skripte.json")
            d = json.load(open(p, encoding="utf-8"))
            if self.num in d:
                pfad, text = f"{p}[{self.num}]", d[self.num]
        if text is None:
            p = erste_datei(os.path.join(self.serie, "skripte", f"short_{self.num}.txt"))
            if p:
                pfad, text = p, open(p, encoding="utf-8").read()
        self._cache["skript"] = (pfad, text)
        return pfad, text

    @property
    def manifest(self):
        p = os.path.join(self.serie, "skript", "QUELLE.json")
        if not os.path.exists(p):
            return p, None
        return p, json.load(open(p, encoding="utf-8"))

    # ── Wortliste / Untertitel ────────────────────────────────
    @property
    def words(self):
        p = erste_datei(
            os.path.join(self.serie, "animation", f"words_{self.num}.json"),
            os.path.join(self.serie, f"words_{self.num}.json"))
        return (p, json.load(open(p, encoding="utf-8"))) if p else (None, None)

    @property
    def ass(self):
        return erste_datei(
            os.path.join(self.serie, "animation", f"sub_{self.num}.ass"),
            os.path.join(self.serie, f"sub_{self.num}.ass"))

    # ── Shot-Konfiguration ────────────────────────────────────
    @property
    def config(self):
        if "cfg" in self._cache:
            return self._cache["cfg"]
        p = erste_datei(os.path.join(self.serie, "configs", f"short_{self.num}.json"))
        if p:
            self._cache["cfg"] = (p, json.load(open(p, encoding="utf-8")))
            return self._cache["cfg"]
        self._cache["cfg"] = self._aus_nb_build()
        return self._cache["cfg"]

    def _aus_nb_build(self):
        import ast
        p = os.path.join(self.serie, "nb_build.py")
        if not os.path.exists(p):
            return None, None
        try:
            baum = ast.parse(open(p, encoding="utf-8").read())
        except SyntaxError:
            return None, None
        for knoten in baum.body:
            if not isinstance(knoten, ast.Assign):
                continue
            if "SHORTS" not in [z.id for z in knoten.targets if isinstance(z, ast.Name)]:
                continue
            try:
                shorts = ast.literal_eval(knoten.value)
            except (ValueError, SyntaxError):
                return None, None
            e = shorts.get(self.num)
            if e is None:
                return None, None
            cfg = {"shots": [{"img": b} for b in e.get("imgs", [])]}
            if e.get("manim"):
                cfg["manim"] = e["manim"]
            if e.get("clip"):
                cfg["shots"].insert(0, {"clip": e["clip"]})
            return f"{p}:SHORTS[{self.num}]", cfg
        return None, None

    # ── Metadaten / Dateien ───────────────────────────────────
    @property
    def meta(self):
        p = os.path.join(self.serie, "metadata.json")
        if not os.path.exists(p):
            return None, None
        m = json.load(open(p, encoding="utf-8"))
        if isinstance(m.get("shorts"), list):
            for s in m["shorts"]:
                if str(s.get("id")) == self.num:
                    return p, s
        elif self.num in m:
            return p, m[self.num]
        return p, None

    @property
    def serien_meta(self):
        p = os.path.join(self.serie, "metadata.json")
        return (p, json.load(open(p, encoding="utf-8"))) if os.path.exists(p) else (p, None)

    @property
    def video(self):
        return erste_datei(
            os.path.join(self.serie, "render", f"short_{self.num}.mp4"),
            os.path.join(self.serie, "output", f"short_{self.num}.mp4"))

    @property
    def voiceover(self):
        return erste_datei(os.path.join(self.serie, "voiceover", f"short_{self.num}.mp3"))


# ═══════════════════════════════════════════ Pruefungen VORHER

def p_herkunft(m):
    pfad, text = m.skript
    if text is None:
        return Befund("R01", "Skript-Herkunft", False, f"Short {m.num}: kein Skript gefunden",
                      stelle=f"erwartet {m.serie}/skript/short_{m.num}.txt")
    mp, man = m.manifest
    if man is None:
        return Befund("R01", "Skript-Herkunft", False,
                      f"Short {m.num}: Herkunft von '{pfad}' nicht belegt",
                      stelle=f"{mp} fehlt — anlegen: "
                             f"python3 tools/kp_skript.py {m.serie} --aus <nutzer-datei>")
    e = man.get("shorts", {}).get(m.num)
    if not e:
        return Befund("R01", "Skript-Herkunft", False,
                      f"Short {m.num}: nicht in QUELLE.json eingetragen", stelle=mp)
    ist = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
    if ist != e.get("sha256"):
        return Befund("R01", "Skript-Herkunft", False,
                      f"Short {m.num}: Skript seit der Aufnahme veraendert",
                      stelle=f"{pfad}\n                 jetzt {ist[:16]}, "
                             f"aufgenommen {e.get('sha256','?')[:16]}")
    stufe = {"nutzer": "vom Nutzer geliefert",
             "repo-historisch": "aus dem Repo uebernommen"}.get(
                 e.get("vertrauen"), f"Stufe '{e.get('vertrauen')}'")
    return Befund("R01", "Skript-Herkunft", True,
                  f"Short {m.num}: {stufe}, unveraendert ({e.get('geliefert_am','?')})")


def p_captions(m):
    wp, words = m.words
    _, text = m.skript
    if words is None:
        return Befund("R02", "Captions=Skript", True,
                      f"Short {m.num}: noch keine Wortliste (entsteht beim Render) "
                      f"— verbindlich in --nachher", hart=False)
    if text is None:
        return Befund("R02", "Captions=Skript", False, f"Short {m.num}: kein Skript zum Vergleich")
    cap = [norm(w["word"]) for w in words if norm(w["word"])]
    skr = [norm(t) for t in tokens(text) if norm(t)]
    if not cap or not skr:
        return Befund("R02", "Captions=Skript", False, f"Short {m.num}: leere Wort- oder Skriptliste")
    sm = difflib.SequenceMatcher(a=cap, b=skr, autojunk=False)
    quote = sm.ratio()
    if quote >= CAPTION_SCHWELLE:
        return Befund("R02", "Captions=Skript", True, f"Short {m.num}: {quote:.0%} Uebereinstimmung")
    roh_c = [w["word"] for w in words if norm(w["word"])]
    roh_s = [t for t in tokens(text) if norm(t)]
    ab = [(" ".join(roh_c[i1:i2]) or "(fehlt)", " ".join(roh_s[j1:j2]) or "(fehlt)")
          for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]
    zeilen = [f"{wp}  ({quote:.0%}, noetig {CAPTION_SCHWELLE:.0%})"]
    zeilen += [f'                 im Video "{a}"  — im Skript "{b}"' for a, b in ab[:8]]
    if len(ab) > 8:
        zeilen.append(f"                 … und {len(ab)-8} weitere")
    return Befund("R02", "Captions=Skript", False,
                  f"Short {m.num}: {len(ab)} Abweichung(en)", stelle="\n".join(zeilen))


def _bewegte(cfg):
    shots = cfg.get("shots", [])
    bewegt = [s for s in shots if s.get("clip") or s.get("manim") or s.get("video")]
    vorne = bool(cfg.get("manim"))
    if vorne:
        bewegt.append({"manim": cfg["manim"]})
    return shots, bewegt, vorne


def p_hook_bewegt(m):
    cp, cfg = m.config
    if cfg is None:
        return Befund("R03", "Hook bewegt", False, f"Short {m.num}: keine Shot-Konfiguration",
                      hart=False, stelle="ohne Konfig ist die Bewegtbild-Regel nicht pruefbar")
    shots, bewegt, vorne = _bewegte(cfg)
    erster = shots[0] if shots else {}
    if vorne or erster.get("clip") or erster.get("manim") or erster.get("video"):
        return Befund("R03", "Hook bewegt", True, f"Short {m.num}: Sekunde 1 ist bewegt")
    return Befund("R03", "Hook bewegt", False,
                  f"Short {m.num}: Sekunde 1 ist ein Standbild",
                  stelle=f"{cp}\n                 Ken-Burns zaehlt nicht. "
                         f"Der Hook-Shot muss bewegt sein.")


def p_bewegtshot(m):
    cp, cfg = m.config
    if cfg is None:
        return Befund("R04", "Bewegtshot", False, f"Short {m.num}: keine Shot-Konfiguration",
                      hart=False)
    shots, bewegt, _ = _bewegte(cfg)
    if bewegt:
        return Befund("R04", "Bewegtshot", True,
                      f"Short {m.num}: {len(bewegt)}/{len(shots)} Shots bewegt")
    return Befund("R04", "Bewegtshot", False,
                  f"Short {m.num}: {len(shots)} Shots, davon 0 bewegt — Standbild-Diashow",
                  stelle=f"{cp}\n                 Noetig: >=1 Shot mit \"clip\" "
                         f"(Remotion/Wan2.1-I2V) oder \"manim\".")


def p_multishot(m):
    cp, cfg = m.config
    if cfg is None:
        return Befund("R05", "Multi-Shot", True, f"Short {m.num}: keine Konfig", hart=False)
    bilder = [s for s in cfg.get("shots", []) if s.get("img")]
    if len(bilder) >= 2:
        return Befund("R05", "Multi-Shot", True, f"Short {m.num}: {len(bilder)} Bilder")
    return Befund("R05", "Multi-Shot", False,
                  f"Short {m.num}: nur {len(bilder)} Bild — Einzelbild-Short (F-V8-A)",
                  stelle=cp)


def p_bild_dedup(m):
    cp, cfg = m.config
    if cfg is None:
        return Befund("R07", "Bild-Dedup", True, f"Short {m.num}: keine Konfig", hart=False)
    bilder = [os.path.basename(str(s.get("img"))) for s in cfg.get("shots", []) if s.get("img")]
    doppelt = [b for i, b in enumerate(bilder[:-1]) if b == bilder[i + 1]]
    if doppelt:
        return Befund("R07", "Bild-Dedup", False,
                      f"Short {m.num}: gleiches Bild direkt hintereinander: "
                      f"{', '.join(sorted(set(doppelt)))}", hart=False, stelle=cp)
    return Befund("R07", "Bild-Dedup", True, f"Short {m.num}: keine direkte Wiederholung")


def p_musik(m):
    cp, cfg = m.config
    if cfg is None or not cfg.get("musik"):
        return Befund("R06", "Musikpegel", True, f"Short {m.num}: kein Musikbett in der Konfig",
                      hart=False)
    db = cfg["musik"].get("db")
    if db is None:
        return Befund("R06", "Musikpegel", False, f"Short {m.num}: musik ohne db-Wert", stelle=cp)
    if db < MUSIK_MIN_DB:
        return Befund("R06", "Musikpegel", False,
                      f"Short {m.num}: musik.db={db} — unter {MUSIK_MIN_DB} unhoerbar (V1-V5)",
                      stelle=cp)
    return Befund("R06", "Musikpegel", True, f"Short {m.num}: musik.db={db}")


def p_titel(m):
    mp, meta = m.meta
    if not meta or not meta.get("title"):
        return Befund("R08", "Titel", True, f"Short {m.num}: kein Titel hinterlegt", hart=False)
    t = meta["title"]
    if len(t) > TITEL_MAX:
        return Befund("R08", "Titel", False,
                      f"Short {m.num}: {len(t)} Zeichen (max {TITEL_MAX}) — "
                      f"die Aussage muss bis Zeichen 35 stehen", stelle=mp)
    return Befund("R08", "Titel", True, f"Short {m.num}: {len(t)} Zeichen")


def p_titel_sauber(m):
    mp, meta = m.meta
    if not meta or not meta.get("title"):
        return Befund("R09", "Titel sauber", True, f"Short {m.num}: kein Titel", hart=False)
    t = meta["title"]
    fehler = []
    if re.search(r"\|\s*doku\b", t, re.I):
        fehler.append("Genre-Label „| Doku" + "\" im Titel (Competitor-Analyse 27.08.)")
    if re.search(r"[\U00010000-\U0010ffff\u2600-\u27bf]", t):
        fehler.append("Emoji im Titel")
    if fehler:
        return Befund("R09", "Titel sauber", False,
                      f"Short {m.num}: {'; '.join(fehler)}", stelle=f"{mp}: \"{t}\"")
    return Befund("R09", "Titel sauber", True, f"Short {m.num}: kein Genre-Label, kein Emoji")


def p_laenge(m):
    vo = m.voiceover
    if not vo:
        return Befund("R11", "Laengenzone", True, f"Short {m.num}: kein Voiceover", hart=False)
    d = sh_dauer(vo)
    lo, hi = LAENGE_ZONE
    if lo <= d <= hi:
        return Befund("R11", "Laengenzone", True, f"Short {m.num}: {d:.0f}s")
    return Befund("R11", "Laengenzone", False,
                  f"Short {m.num}: {d:.0f}s — ausserhalb der belegten Zone {lo}-{hi}s",
                  hart=False, stelle="n=44 intern belegt; bewusste Ausnahme ist erlaubt")


def p_longform(m):
    mp, sm = m.serien_meta
    if sm is None:
        return Befund("R12", "Longform", False, f"{m.serie}: keine metadata.json", hart=False)
    if sm.get("longform"):
        return Befund("R12", "Longform", True, f"{m.serie}: Longform hinterlegt")
    return Befund("R12", "Longform", False,
                  f"{m.serie}: kein \"longform\" in metadata.json — "
                  f"6 von 8 Serien haben bis heute keines", hart=False, stelle=mp)


# ═══════════════════════════════════════════ Pruefungen NACHHER

def _ass_zeiten(pfad):
    n, letzte = 0, 0.0
    for z in open(pfad, encoding="utf-8", errors="ignore"):
        if not z.startswith("Dialogue:"):
            continue
        n += 1
        t = z.split(",")
        if len(t) > 2:
            try:
                h, mi, s = t[2].strip().split(":")
                letzte = max(letzte, int(h) * 3600 + int(mi) * 60 + float(s))
            except ValueError:
                pass
    return n, letzte


def _band_hell(video, sekunde, oben=0.72, hoehe=5):
    """Spitzenhelligkeit in einem waagerechten Band. -v info ist Pflicht:
    unter -v error unterdrueckt ffmpeg die metadata-Ausgabe, und die Messung
    meldete dann immer 0 — eine Messung, die immer dasselbe sagt, misst nichts."""
    r = subprocess.run(
        ["ffmpeg", "-v", "info", "-ss", f"{sekunde:.2f}", "-i", video, "-frames:v", "1",
         "-vf", f"crop=iw:ih/{hoehe}:0:ih*{oben},signalstats,"
                f"metadata=print:key=lavfi.signalstats.YMAX", "-f", "null", "-"],
        capture_output=True, text=True)
    w = [int(x) for x in re.findall(r"YMAX=(\d+)", r.stderr + r.stdout)]
    return max(w) if w else -1


def p_render_dauer(m):
    v = m.video
    if not v:
        return Befund("R13", "Render-Dauer", False, f"Short {m.num}: kein gerendertes Video",
                      stelle=f"erwartet {m.serie}/render/short_{m.num}.mp4")
    d, vo = sh_dauer(v), m.voiceover
    if vo:
        vd = sh_dauer(vo)
        if abs(d - vd) > 1.5:
            return Befund("R13", "Render-Dauer", False,
                          f"Short {m.num}: Video {d:.1f}s, Voiceover {vd:.1f}s", stelle=v)
    return Befund("R13", "Render-Dauer", True, f"Short {m.num}: {d:.1f}s, deckt das Voiceover")


def p_untertitel_abdeckung(m):
    v, a = m.video, m.ass
    if not v:
        return Befund("R14", "UT-Abdeckung", False, f"Short {m.num}: kein Video")
    if not a:
        return Befund("R14", "UT-Abdeckung", False, f"Short {m.num}: keine ASS-Datei")
    n, letzte = _ass_zeiten(a)
    if n == 0:
        return Befund("R14", "UT-Abdeckung", False,
                      f"Short {m.num}: ASS ohne eine einzige Dialogzeile", stelle=a)
    d = sh_dauer(v)
    q = letzte / d if d else 0
    if q < UNTERTITEL_ABDECKUNG:
        return Befund("R14", "UT-Abdeckung", False,
                      f"Short {m.num}: Untertitel enden bei {letzte:.1f}s von {d:.1f}s ({q:.0%})",
                      stelle=a)
    return Befund("R14", "UT-Abdeckung", True, f"Short {m.num}: {n} Zeilen, {q:.0%} Abdeckung")


def p_untertitel_im_bild(m):
    v, a = m.video, m.ass
    if not v or not a:
        return Befund("R15", "UT im Bild", False, f"Short {m.num}: Video oder ASS fehlt")
    n, letzte = _ass_zeiten(a)
    if n == 0:
        return Befund("R15", "UT im Bild", False, f"Short {m.num}: ASS ohne Dialogzeilen")
    proben = [letzte * f for f in (0.25, 0.5, 0.8)]
    hell = max(_band_hell(v, t) for t in proben)
    if hell < 0:
        return Befund("R15", "UT im Bild", False,
                      f"Short {m.num}: Helligkeit nicht messbar", stelle=v)
    if hell < UNTERTITEL_HELL:
        return Befund("R15", "UT im Bild", False,
                      f"Short {m.num}: im Untertitel-Band keine Schrift "
                      f"(Helligkeit {hell}, noetig {UNTERTITEL_HELL})",
                      stelle=f"{v}\n                 {n} ASS-Zeilen vorhanden, "
                             f"aber nicht ins Bild gebrannt (F-V9-D)")
    return Befund("R15", "UT im Bild", True,
                  f"Short {m.num}: Untertitel sichtbar (Helligkeit {hell})")


def p_progressbar(m):
    """Die Leiste sitzt in den untersten 20 px und ist voll deckend gelb."""
    v = m.video
    if not v:
        return Befund("R16", "Fortschritt", False, f"Short {m.num}: kein Video")
    d = sh_dauer(v)
    # Bei 60 % Laufzeit muss die Leiste ueber mehr als die halbe Breite laufen.
    r = subprocess.run(
        ["ffmpeg", "-v", "info", "-ss", f"{d*0.6:.2f}", "-i", v, "-frames:v", "1",
         "-vf", "crop=iw/2:12:0:ih-14,signalstats,metadata=print:key=lavfi.signalstats.YMAX",
         "-f", "null", "-"], capture_output=True, text=True)
    w = [int(x) for x in re.findall(r"YMAX=(\d+)", r.stderr + r.stdout)]
    hell = max(w) if w else -1
    if hell < 180:
        return Befund("R16", "Fortschritt", False,
                      f"Short {m.num}: Fortschrittsleiste bei 60 % nicht erkennbar "
                      f"(Helligkeit {hell})", hart=False,
                      stelle=f"{v}\n                 h>=18 px, gelb, kein Alpha (F-V8-C)")
    return Befund("R16", "Fortschritt", True, f"Short {m.num}: Leiste sichtbar ({hell})")


def p_cta(m):
    """„Kanal folgen" muss in den letzten Sekunden im Bild stehen."""
    v = m.video
    if not v:
        return Befund("R17", "CTA", False, f"Short {m.num}: kein Video")
    d = sh_dauer(v)
    hell = _band_hell(v, max(d - 2.0, 0.0), oben=0.60, hoehe=8)
    if hell < 170:
        return Befund("R17", "CTA", False,
                      f"Short {m.num}: kein CTA in den letzten Sekunden erkennbar "
                      f"(Helligkeit {hell})", hart=False, stelle=v)
    return Befund("R17", "CTA", True, f"Short {m.num}: CTA-Bereich hell ({hell})")


def p_lautheit(m):
    v = m.video
    if not v:
        return Befund("R18", "Lautheit", False, f"Short {m.num}: kein Video")
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", v, "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True)
    mm = re.findall(r"^\s+I:\s+(-?[\d.]+)\s+LUFS", r.stderr, re.M)
    if not mm:
        return Befund("R18", "Lautheit", True, f"Short {m.num}: nicht messbar", hart=False)
    lufs = float(mm[-1])
    lo, hi = LUFS_ZIEL
    if lo <= lufs <= hi:
        return Befund("R18", "Lautheit", True, f"Short {m.num}: {lufs:.1f} LUFS")
    return Befund("R18", "Lautheit", False,
                  f"Short {m.num}: {lufs:.1f} LUFS — ausserhalb {lo}…{hi}", hart=False, stelle=v)


def ist_fremdmaterial(dateiname):
    """Darf dieses Bild NICHT ins Sendematerial?

    Konvention im Repo:
        hf_*    selbst erzeugt (Z-Image/Higgsfield)  -> erlaubt
        ref_*   fremde Vorlage fuer die Generierung  -> NIE ins Video

    Diese Funktion ist die einzige Stelle, an der das entschieden wird. Sowohl
    die Regel R24 als auch der Longform-Bauer nb_lang.py rufen sie auf. Der
    Grund fuer die Zusammenlegung: nb_lang.py suchte sich seine Bilder selbst
    und zog dabei ref_01 bis ref_04 heran -- echte Pressefotos von Aron
    Ralston. Die Regel galt fuer die Shorts und lief am Langvideo vorbei.
    Genau dieses Muster -- Regel an einer Stelle, Umgehung an der naechsten --
    ist der Kern des Befundes vom 07.09.
    """
    name = os.path.basename(str(dateiname or "")).lower()
    return name.startswith("ref_") or "presse" in name or "getty" in name


_AUSSORTIERT_CACHE = {}


def aussortierte_bilder(serie):
    """Bilder, die eine Serie ausdruecklich NICHT verwenden soll — mit Grund.

    Datei: <serie>/bilder/AUSSORTIERT.json
        {"short_08/01.jpg": "Historisches Schwarzweiss, Soldaten — 1917, nicht 2009"}

    WARUM NICHT LOESCHEN
    --------------------
    Guardrail #1 schuetzt bestehendes Material. Ein geloeschtes Bild ist eine
    Entscheidung ohne Begruendung und ohne Rueckweg. Ein ausgetragenes Bild
    bleibt liegen, traegt seinen Grund neben sich und kann jederzeit wieder
    aufgenommen werden — indem die Zeile verschwindet.

    HERKUNFT
    --------
    Im Nutty-Putty-Langvideo (08.09.2026) liefen acht themenfremde Bilder mit:
    ein lachendes Hoehlen-Zeltlager mit rosa Schlafsaecken waehrend der Satz
    lief, dass die Reibung im Fels jeden Zug auffrass; drei historische
    Schwarzweissfotos von Soldaten mit Tragen; ein Strassen-Schrein zu dem Satz,
    dass die Hoehle mit Beton versiegelt wurde. Keine Regel und kein Riegel hat
    das gesehen — Regeln messen Dateieigenschaften, nicht Bildinhalt. Der Blick
    bleibt hier zustaendig; was der Blick entscheidet, wird hier festgehalten,
    damit er es nur einmal entscheiden muss.
    """
    serie = str(serie or "").rstrip("/")
    if serie in _AUSSORTIERT_CACHE:
        return _AUSSORTIERT_CACHE[serie]
    pfad = os.path.join(serie, "bilder", "AUSSORTIERT.json")
    daten = {}
    if os.path.exists(pfad):
        try:
            daten = json.load(open(pfad, encoding="utf-8"))
        except Exception as e:
            print(f"  ! {pfad} ist unlesbar ({e}) — kein Bild ausgeschlossen")
    _AUSSORTIERT_CACHE[serie] = daten
    return daten


def bild_ausgeschlossen(serie, pfad):
    """Zusammengefasste Pruefung: Fremdmaterial ODER begruendet aussortiert.

    Jeder Bauer ruft NUR diese Funktion auf. Zwei getrennte Pruefungen an zwei
    Stellen sind genau das Muster, das F-V9-B/K/Q erzeugt hat.
    """
    if ist_fremdmaterial(pfad):
        return "Fremdmaterial (ref_/presse/getty)"
    aus = aussortierte_bilder(serie)
    if not aus:
        return None
    p = str(pfad).replace(os.sep, "/")
    for schluessel, grund in aus.items():
        k = str(schluessel).replace(os.sep, "/").lstrip("./")
        if p == k or p.endswith("/" + k) or os.path.basename(p) == k:
            return grund
    return None


def p_fremdmaterial(m):
    """Referenzfotos duerfen nie im Video landen.

    In ralston/bilder/broll/ liegen neben den selbst erzeugten hf_*-Bildern
    auch ref_*.jpg — echte Pressefotos von Aron Ralston, die als Vorlage fuer
    die Bildgenerierung dienten. Als Vorlage sind sie richtig; im Video waeren
    sie fremdes Material. Die Konvention ist damit pruefbar:

        hf_*   selbst erzeugt   -> darf in den Schnitt
        ref_*  fremde Vorlage   -> NIE in den Schnitt
    """
    cp, cfg = m.config
    if cfg is None:
        return Befund("R24", "Fremdmaterial", True, f"Short {m.num}: keine Konfig", hart=False)
    verdaechtig = [os.path.basename(str(s.get("img")))
                   for s in cfg.get("shots", [])
                   if s.get("img") and ist_fremdmaterial(s["img"])]
    if verdaechtig:
        return Befund("R24", "Fremdmaterial", False,
                      f"Short {m.num}: Referenz-/Fremdmaterial im Schnitt: "
                      f"{', '.join(verdaechtig)}",
                      stelle=f"{cp}\n                 ref_* sind Vorlagen fuer die "
                             f"Bildgenerierung, kein Sendematerial.")
    return Befund("R24", "Fremdmaterial", True,
                  f"Short {m.num}: nur selbst erzeugte Bilder im Schnitt")


# ═══════════════════════════════════════════ Pruefungen DAUERHAFT

def p_snapshot(_m=None):
    """Ohne taeglichen Messpunkt wird eine Serie dauerhaft unvergleichbar.
    V5 und V6 (20 Videos) sind genau so verloren gegangen."""
    import datetime as dt
    import glob as g
    d = os.path.join(ROOT, "YouTube-Knowledge", "07-Analytics", "snapshots")
    snaps = sorted(g.glob(os.path.join(d, "*.json")))
    if not snaps:
        return Befund("R19", "Messpunkt", False, "kein Snapshot vorhanden", hart=False,
                      stelle="python3 tools/kp_metrik.py --snapshot")
    datum = os.path.splitext(os.path.basename(snaps[-1]))[0]
    try:
        alter = (dt.date.today() - dt.date.fromisoformat(datum)).days
    except ValueError:
        return Befund("R19", "Messpunkt", False, f"Snapshot-Datum unlesbar: {datum}", hart=False)
    if alter > SNAPSHOT_MAX_TAGE:
        return Befund("R19", "Messpunkt", False,
                      f"letzter Messpunkt {datum} ({alter} Tage alt)", hart=False,
                      stelle="jeder fehlende Tag ist dauerhaft verloren "
                             "-> python3 tools/kp_metrik.py --snapshot")
    return Befund("R19", "Messpunkt", True, f"Messpunkt {datum} ist aktuell")


def p_animationen(_m=None):
    """Animationen duerfen nicht ueber den Rand laufen oder im Bild untergehen."""
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "kp_anim_qc.py"),
                        "--json"], cwd=ROOT, capture_output=True, text=True)
    try:
        erg = json.loads(r.stdout)
    except Exception:
        return Befund("R20", "Animationen", True, "keine gerenderten Szenen", hart=False)
    schlecht = [e["szene"] for e in erg if not e["ok"]]
    if schlecht:
        return Befund("R20", "Animationen", False,
                      f"{len(schlecht)} auffaellig: {', '.join(schlecht[:4])}", hart=False,
                      stelle="python3 tools/kp_anim_qc.py")
    return Befund("R20", "Animationen", True, f"{len(erg)} Szenen fuellen das Bild")


def p_tiktok_riegel(_m=None):
    """R23 wird nicht am Material geprueft, sondern am Riegel selbst.

    Die Regel lautet: TikTok wird nie automatisch bespielt. Durchgesetzt wird
    sie im PreToolUse-Hook, der Buffer-Posts auf TikTok-Kanaele mit Exit 2
    anhaelt. Diese Pruefung stellt sicher, dass der Riegel dafuer ueberhaupt
    noch zustaendig ist -- eine Durchsetzung, die still verschwindet, ist
    schlimmer als eine, die es nie gab.
    """
    hook = os.path.join(ROOT, ".claude", "hooks", "pre-tool-use.py")
    if not os.path.exists(hook):
        return Befund("R23", "TikTok manuell", False,
                      "PreToolUse-Riegel fehlt — R23 waere wieder nur Prosa",
                      stelle=hook)
    quelle = open(hook, encoding="utf-8").read()
    if "pruefe_tiktok" not in quelle or "R23" not in quelle:
        return Befund("R23", "TikTok manuell", False,
                      "Riegel enthaelt keine TikTok-Pruefung mehr", stelle=hook)
    einstellungen = os.path.join(ROOT, ".claude", "settings.json")
    if "PreToolUse" not in open(einstellungen, encoding="utf-8").read():
        return Befund("R23", "TikTok manuell", False,
                      "PreToolUse ist in settings.json nicht eingehaengt",
                      stelle=einstellungen)
    return Befund("R23", "TikTok manuell", True,
                  "Riegel haelt Buffer-Posts auf TikTok-Kanaele an")


def p_gedaechtnis(_m=None):
    """R25 — wurde Code geaendert, ohne dass das Gedaechtnis mitgewachsen ist?

    Stehende Anweisung des Nutzers (07.09.2026): jede Analyse, Diagnose,
    Korrektur und Loesung wird so festgeschrieben, dass er sie nie erwaehnen
    muss. Ein Befund, der nur im Chat steht, ist mit dem Container weg.

    Geprueft wird der einfachste harte Fall: Es liegen Aenderungen an
    Werkzeugen oder Hooks vor, aber keine einzige am Vault. Dann ist etwas
    gelernt worden, das niemand wiederfindet.

    Bewusst als Hinweis (nicht blockierend): waehrend der Arbeit ist dieser
    Zustand normal. Er darf nur das Sitzungsende nicht ueberleben.
    """
    r = subprocess.run(["git", "status", "--porcelain"], cwd=ROOT,
                       capture_output=True, text=True)
    if r.returncode != 0:
        return Befund("R25", "Gedaechtnis", True, "kein Git-Status verfuegbar", hart=False)
    code, vault = [], []
    for zeile in r.stdout.splitlines():
        pfad = zeile[3:].strip().strip('"')
        if pfad.startswith(("tools/", ".claude/")) and pfad.endswith((".py", ".sh", ".json")):
            code.append(pfad)
        elif pfad.startswith("YouTube-Knowledge/") or pfad == "CLAUDE.md":
            vault.append(pfad)
    if code and not vault:
        return Befund("R25", "Gedaechtnis", False,
                      f"{len(code)} Code-Aenderung(en) ohne eine einzige "
                      f"Vault-Aenderung", hart=False,
                      stelle=f"{', '.join(code[:4])}\n"
                             f"                 Befund -> Failure-Memory, Regel -> "
                             f"kp_regeln.py, Zahl -> Observations. Dann /merken.")
    if code:
        return Befund("R25", "Gedaechtnis", True,
                      f"{len(code)} Code- und {len(vault)} Vault-Aenderung(en) — "
                      f"waechst mit")
    return Befund("R25", "Gedaechtnis", True, "keine offenen Code-Aenderungen")


# ═══════════════════════════════════════════ Pruefungen LANGVIDEO

def _longform_datei(serie):
    return erste_datei(os.path.join(serie, "render", "long.mp4"),
                       os.path.join(serie, "output", "long.mp4"))


def p_longform_laenge(m):
    """R26 — ein Langvideo muss lang sein.

    Die beiden vorhandenen Langvideos des Kanals sind 5:39 und 4:29 lang und
    haben 13 bzw. 64 Aufrufe. Zu kurz geratene Zusammenschnitte sind weder
    Short noch Longform und bedienen keinen der beiden Feeds.
    """
    serie = m.serie if hasattr(m, "serie") else str(m)
    v = _longform_datei(serie)
    if not v:
        return Befund("R26", "Langvideo-Laenge", False,
                      f"{serie}: kein render/long.mp4", hart=False,
                      stelle=f"bauen: python3 nb_lang.py {os.path.basename(serie)}")
    d = sh_dauer(v)
    if d < 180:
        return Befund("R26", "Langvideo-Laenge", False,
                      f"{serie}: nur {int(d)//60}:{int(d)%60:02d} — unter 3 Minuten",
                      stelle=v)
    return Befund("R26", "Langvideo-Laenge", True,
                  f"{serie}: {int(d)//60}:{int(d)%60:02d}")


def p_longform_format(m):
    """R27 — Querformat, sonst konkurriert das Langvideo mit dem Shorts-Feed."""
    serie = m.serie if hasattr(m, "serie") else str(m)
    v = _longform_datei(serie)
    if not v:
        return Befund("R27", "Langvideo-Format", True, f"{serie}: kein Langvideo",
                      hart=False)
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0",
                        "-show_entries", "stream=width,height", "-of", "csv=p=0", v],
                       capture_output=True, text=True).stdout.strip()
    try:
        w, h = (int(x) for x in r.split(",")[:2])
    except Exception:
        return Befund("R27", "Langvideo-Format", False,
                      f"{serie}: Bildmasse nicht lesbar", stelle=v)
    if w <= h:
        return Befund("R27", "Langvideo-Format", False,
                      f"{serie}: {w}x{h} ist Hochformat — YouTube wertet das als Short",
                      stelle=v)
    return Befund("R27", "Langvideo-Format", True, f"{serie}: {w}x{h}")


def p_longform_ton(m):
    """R28 — dieselbe Lautheit wie die Shorts (F-V9-G)."""
    serie = m.serie if hasattr(m, "serie") else str(m)
    v = _longform_datei(serie)
    if not v:
        return Befund("R28", "Langvideo-Ton", True, f"{serie}: kein Langvideo",
                      hart=False)
    r = subprocess.run(["ffmpeg", "-v", "info", "-i", v, "-af", "ebur128=peak=true",
                        "-f", "null", "-"], capture_output=True, text=True)
    mm = re.findall(r"^\s+I:\s+(-?[\d.]+)\s+LUFS", r.stderr, re.M)
    if not mm:
        return Befund("R28", "Langvideo-Ton", True, f"{serie}: nicht messbar", hart=False)
    lufs = float(mm[-1])
    lo, hi = LUFS_ZIEL
    if lo <= lufs <= hi:
        return Befund("R28", "Langvideo-Ton", True, f"{serie}: {lufs:.1f} LUFS")
    return Befund("R28", "Langvideo-Ton", False,
                  f"{serie}: {lufs:.1f} LUFS — ausserhalb {lo}…{hi}", stelle=v)


def p_longform_bildwechsel(m):
    """R29 — wechselt im Langvideo ueberhaupt das Bild?

    Am 08.09.2026 lieferte nb_lang.py ein 5:55 langes Video, das ueber die
    volle Laenge EIN Bild zeigte — sanft geschwenkt, aber nie gewechselt.
    R26 (Laenge), R27 (Format) und R28 (Ton) gingen alle gruen durch: die
    Datei war 5:55 lang, 1920x1080 und bei -14,1 LUFS. Kein Messwert sagte,
    dass sechs Minuten lang dasselbe Motiv laeuft.

    Gemessen wird mit ffmpeg-Szenenerkennung. Ein Langvideo aus 60 geplanten
    Einstellungen muss deutlich mehr als eine Handvoll harter Schnitte haben;
    bei einem Ein-Bild-Video sind es null.
    """
    serie = m.serie if hasattr(m, "serie") else str(m)
    v = _longform_datei(serie)
    if not v:
        return Befund("R29", "Bildwechsel", True, f"{serie}: kein Langvideo", hart=False)
    d = sh_dauer(v)
    if d < 30:
        return Befund("R29", "Bildwechsel", True, f"{serie}: zu kurz zum Messen", hart=False)
    r = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", v, "-vf",
         "select='gt(scene,0.25)',metadata=print", "-an", "-f", "null", "-"],
        capture_output=True, text=True)
    wechsel = len(re.findall(r"pts_time", r.stderr + r.stdout))
    # Faustregel: mindestens ein Schnitt je 30 Sekunden.
    noetig = max(3, int(d // 30))
    if wechsel < noetig:
        return Befund("R29", "Bildwechsel", False,
                      f"{serie}: nur {wechsel} Bildwechsel in "
                      f"{int(d)//60}:{int(d)%60:02d} (noetig >= {noetig})",
                      stelle=f"{v}\n                 Ein Video aus einem einzigen "
                             f"Bild besteht jede andere Pruefung (F-V9-O).")
    return Befund("R29", "Bildwechsel", True,
                  f"{serie}: {wechsel} Bildwechsel in {int(d)//60}:{int(d)%60:02d}")


# ═══════════════════════════════════════════════ Das Register

# phase: "vorher"  = vor dem Render, aus Skript/Konfig/Metadaten
#        "nachher" = am fertigen Video gemessen
#        "dauerhaft" = Systemzustand, unabhaengig von einer Serie
REGELN = [
    dict(id="R01", phase="vorher", titel="Skript-Herkunft", pruefung=p_herkunft,
         regel="Kein Text ist ein Skript, solange seine Herkunft nicht per Pruefsumme belegt ist.",
         herkunft="F-V9-A — prosperi/nb_transcribe.py schrieb ASR nach skripte/short_XX.txt"),
    dict(id="R02", phase="vorher", titel="Captions=Skript", pruefung=p_captions,
         regel="Caption-Woerter kommen aus dem Nutzer-Skript, ASR nur fuers Timing.",
         herkunft="F-V8-E / F-V9-A — „Marathon des Apples\" statt „Sables\", live in 10 Shorts"),
    dict(id="R03", phase="vorher", bauart="shorts", titel="Hook bewegt", pruefung=p_hook_bewegt,
         regel="Sekunde 1 ist bewegt. Ken-Burns ueber ein Standbild zaehlt nicht.",
         herkunft="Short-Konzept-Blueprint 31.08. — virale Hits fahren ~90 % Bewegtbild"),
    dict(id="R04", phase="vorher", bauart="shorts", titel="Bewegtshot", pruefung=p_bewegtshot,
         regel="Mindestens ein echter Bewegtshot je Short (Manim/Remotion/I2V).",
         herkunft="Bewegtbild-Pflicht 31.08. — 5 von 10 Ralston-Shorts verletzten sie unbemerkt"),
    dict(id="R05", phase="vorher", bauart="shorts", titel="Multi-Shot", pruefung=p_multishot,
         regel="Mindestens 2 Bilder je Short, nie ein einzelnes Standbild.",
         herkunft="F-V8-A — alle 10 Shorts bestanden aus EINEM Ken-Burns-Clip"),
    dict(id="R06", phase="vorher", bauart="shorts", titel="Musikpegel", pruefung=p_musik,
         regel="Musikbett db >= -18 (Ziel -16), sonst unhoerbar.",
         herkunft="Nutzer-Befund 25.08. — V1-V5 hatten ein unhoerbares Bett"),
    dict(id="R07", phase="vorher", bauart="shorts", titel="Bild-Dedup", pruefung=p_bild_dedup,
         regel="Kein Bild zweimal direkt hintereinander im selben Short.",
         herkunft="Learning-Bilder-Prompts — globaler Dedup-Set je Produktion"),
    dict(id="R08", phase="vorher", bauart="shorts", titel="Titel", pruefung=p_titel,
         regel="Titel hoechstens 60 Zeichen, Aussage bis Zeichen 35 fertig.",
         herkunft="Learning-Titel — CTR-Beleg"),
    dict(id="R09", phase="vorher", bauart="shorts", titel="Titel sauber", pruefung=p_titel_sauber,
         regel="Kein Genre-Label („| Doku\") und kein Emoji im Titel.",
         herkunft="Competitor-Analyse 27.08. — kein Top-Performer nutzt Genre-Labels"),
    dict(id="R11", phase="vorher", bauart="shorts", titel="Laengenzone", pruefung=p_laenge,
         regel="Zielzone 19-49 s (intern belegt 19-39, A/B bis 49).",
         herkunft="Learning-Retention — n=44 intern belegt; Competitor-Zone nur Hypothese"),
    dict(id="R12", phase="vorher", titel="Longform", pruefung=p_longform,
         regel="Jede Serie hinterlegt ein Longform in metadata.json.",
         herkunft="Pflichtliste §6 — 6 von 8 Serien haben bis heute keines"),

    dict(id="R13", phase="nachher", titel="Render-Dauer", pruefung=p_render_dauer,
         regel="Das Video deckt das Voiceover (Abweichung < 1,5 s).",
         herkunft="Grundpruefung — faengt abgebrochene Renders"),
    dict(id="R14", phase="nachher", titel="UT-Abdeckung", pruefung=p_untertitel_abdeckung,
         regel="Untertitel decken mindestens 60 % der Laufzeit.",
         herkunft="F-V9-D — leere Wortliste erzeugte Videos ohne Untertitel"),
    dict(id="R15", phase="nachher", titel="UT im Bild", pruefung=p_untertitel_im_bild,
         regel="Im fertigen Bild steht wirklich Schrift im Untertitel-Band.",
         herkunft="F-V9-D — der Build meldete „Captions aus Skript\" bei 0 Untertiteln"),
    dict(id="R16", phase="nachher", titel="Fortschritt", pruefung=p_progressbar,
         regel="Fortschrittsleiste sichtbar: >=18 px, gelb, kein Alpha.",
         herkunft="F-V8-C — 10 px halbtransparent war auf dem Handy unsichtbar"),
    dict(id="R17", phase="nachher", titel="CTA", pruefung=p_cta,
         regel="„Kanal folgen\" steht in den letzten Sekunden im Bild.",
         herkunft="CTA-Overlay 27.08."),
    dict(id="R18", phase="nachher", titel="Lautheit", pruefung=p_lautheit,
         regel="Gesamtlautheit im Band -20 bis -11 LUFS.",
         herkunft="Learning-Editing-Ton — YouTube normalisiert auf ~-14"),

    dict(id="R19", phase="dauerhaft", titel="Messpunkt", pruefung=p_snapshot,
         regel="Taeglich ein Analytics-Snapshot. Ein fehlender Tag ist dauerhaft verloren.",
         herkunft="Befund 4 — V5 und V6 (20 Videos) sind ohne Ergebnis geblieben"),
    dict(id="R20", phase="dauerhaft", titel="Animationen", pruefung=p_animationen,
         regel="Animationen fuellen das Bild und laufen nicht ueber den Rand.",
         herkunft="F-V9-E — jede Animation lief in einer 3x zu grossen Buehne"),

    dict(id="R25", phase="dauerhaft", titel="Gedaechtnis", pruefung=p_gedaechtnis,
         regel="Jede Analyse, Diagnose, Korrektur und Loesung wird festgeschrieben — "
               "Code aendert sich nie ohne Vault.",
         herkunft="Stehende Anweisung des Nutzers 07.09.2026: „damit ich sie nicht "
                  "erwaehnen muss\""),
    dict(id="R26", phase="langform", titel="Langvideo-Laenge", pruefung=p_longform_laenge,
         regel="Ein Langvideo ist mindestens 3 Minuten lang.",
         herkunft="6 von 8 Serien hatten am 07.09. gar keines; die zwei vorhandenen "
                  "sind 4:29 und 5:39 lang"),
    dict(id="R27", phase="langform", titel="Langvideo-Format", pruefung=p_longform_format,
         regel="Ein Langvideo ist Querformat — Hochformat wertet YouTube als Short.",
         herkunft="Longform bedient den Suchtraffic, nicht den Shorts-Feed"),
    dict(id="R28", phase="langform", titel="Langvideo-Ton", pruefung=p_longform_ton,
         regel="Langvideo im selben Lautheitsband wie die Shorts (-20 bis -11 LUFS).",
         herkunft="F-V9-G — der ganze Kanal lief bei -22 LUFS"),
    dict(id="R29", phase="langform", titel="Bildwechsel", pruefung=p_longform_bildwechsel,
         regel="Im Langvideo wechselt das Bild — mindestens ein Schnitt je 30 Sekunden.",
         herkunft="F-V9-O — nb_lang.py lieferte 5:55 aus EINEM Bild; Laenge, Format "
                  "und Ton gingen alle gruen durch"),
    # ── Regeln ohne Pruefpunkt: ehrlich als ungedeckt gefuehrt ────────────
    dict(id="R21", phase="vorher", titel="Untertitel=Stimme", pruefung=None,
         regel="Untertitel spiegeln die gesprochene Stimme, kein abweichender Text.",
         herkunft="Learning-Captions — abweichender Hook-Banner nur als Experiment",
         durchsetzung="mittelbar durch R02: die Woerter kommen aus dem gesprochenen Skript"),
    dict(id="R22", phase="vorher", titel="Schluesselszene", pruefung=None,
         regel="Schluesselmomente werden erzeugt, Establishing kommt aus Stock.",
         herkunft="Learning-Bilder-Prompts"),
    dict(id="R23", phase="dauerhaft", titel="TikTok manuell", pruefung=p_tiktok_riegel,
         regel="TikTok wird NIE automatisch bespielt — der Nutzer laedt selbst hoch.",
         herkunft="Beleg: Auto-Schedule = 1 View/Video, manuell = Tausende",
         durchsetzung="PreToolUse-Riegel blockiert Buffer-Posts auf TikTok-Kanaele"),
    dict(id="R24", phase="vorher", titel="Fremdmaterial", pruefung=p_fremdmaterial,
         regel="Kein fremdes Material im Schnitt: ref_*-Vorlagen bleiben Vorlagen.",
         herkunft="/video „Nie\"-Liste — ralston/bilder/broll/ref_*.jpg sind echte Pressefotos"),
]

NACH_ID = {r["id"]: r for r in REGELN}


def regeln_der_phase(phase, bauart=None):
    """Regeln einer Phase, optional auf eine Bauart eingegrenzt.

    Warum es die Bauart gibt: Am 08.09.2026 blockierte das Gate den Bau eines
    LANGVIDEOS, weil die SHORTS derselben Serie die Bewegtbild- und
    Titel-Regeln verletzen. Diese Shorts waren laengst veroeffentlicht und
    wurden gar nicht angefasst — der Longform-Bauer nutzt nur Voiceover und
    Bilder. Das war ein Fehlalarm, und Fehlalarme sind das, woran Riegel
    sterben: man schaltet sie ab, und danach schuetzen sie nichts mehr.

    Eine Regel ohne `bauart` gilt weiterhin fuer alles. Nur wer ausdruecklich
    "shorts" traegt, wird beim Longform-Bau uebersprungen. Das ist eine
    Praezisierung des Geltungsbereichs, keine Aufweichung: keine Regel
    verliert ihre Wirkung dort, wo sie hingehoert.
    """
    treffer = [r for r in REGELN if r["phase"] == phase and r["pruefung"]]
    if bauart:
        treffer = [r for r in treffer
                   if r.get("bauart") in (None, bauart)]
    return treffer


def deckung():
    gedeckt = [r for r in REGELN if r["pruefung"]]
    return len(gedeckt), len(REGELN)


def markdown():
    g, n = deckung()
    z = [
        "---", "type: system", "title: Regel-Register",
        "status: active", "updated: 2026-09-07",
        "tags: [system, regeln, durchsetzung, generiert]", "---", "",
        "# Regel-Register — erzeugt aus `tools/kp_regeln.py`", "",
        "> **Diese Datei wird erzeugt, nicht von Hand gepflegt.**",
        "> `python3 tools/kp_regeln.py --markdown > YouTube-Knowledge/00-System/Regel-Register.md`",
        ">",
        "> Der Grund: Bis zum 07.09.2026 standen die Regeln in Prosa und die",
        "> Durchsetzung nirgends. Ein Commit durfte „pipeline-weit erzwungen\" heissen,",
        "> ohne eine Zeile Code zu aendern. Jetzt ist die Liste ein Abbild des Codes —",
        "> sie kann nicht mehr behaupten, was das Programm nicht tut.", "",
        f"**Deckungsgrad: {g} von {n} Regeln haben einen Pruefpunkt "
        f"({g/n:.0%}).**", "",
    ]
    for phase, ueberschrift, erklaerung in [
        ("vorher", "Vor dem Render", "Aus Skript, Shot-Konfiguration und Metadaten. "
         "Blockiert per `kp_gate.py <serie>`."),
        ("nachher", "Am fertigen Video", "Gemessen an der Datei, nicht an der Absicht. "
         "Blockiert per `kp_gate.py <serie> --nachher`."),
        ("langform", "Am Langvideo", "Gemessen an <serie>/render/long.mp4. "
         "Blockiert per `kp_gate.py <serie> --langform`."),
        ("dauerhaft", "Systemzustand", "Unabhaengig von einer einzelnen Serie."),
    ]:
        z += [f"## {ueberschrift}", "", f"*{erklaerung}*", "",
              "| ID | Regel | Prüfpunkt | Entstanden aus |", "|---|---|---|---|"]
        for r in [x for x in REGELN if x["phase"] == phase]:
            p = f"`{r['pruefung'].__name__}()`" if r["pruefung"] else "**— ungedeckt**"
            bereich = {"shorts": " *(nur Shorts)*"}.get(r.get("bauart"), "")
            z.append(f"| {r['id']} | {r['regel']}{bereich} | {p} | {r['herkunft']} |")
        z.append("")
    offen = [r for r in REGELN if not r["pruefung"]]
    if offen:
        z += ["## Ungedeckt — bewusst als solche gefuehrt", "",
              "Diese Regeln gelten, werden aber von keinem Programm erzwungen.",
              "Sie stehen hier, damit die Luecke sichtbar bleibt statt zu verschwinden.", ""]
        for r in offen:
            z.append(f"- **{r['id']} {r['titel']}** — {r['regel']}  ")
            z.append(f"  *{r['herkunft']}*")
        z.append("")
    z += ["## Related", "[[Decision-Harte-Gates-statt-Prosa]] · [[Failure-Memory]] · "
          "[[Produktion-Pflichtliste]] · [[Current-State]]", ""]
    return "\n".join(z)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ungedeckt", action="store_true")
    ap.add_argument("--markdown", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.markdown:
        print(markdown())
        return 0
    if a.json:
        print(json.dumps([{k: (v.__name__ if callable(v) else v)
                           for k, v in r.items()} for r in REGELN],
                         ensure_ascii=False, indent=1))
        return 0

    g, n = deckung()
    if a.ungedeckt:
        for r in REGELN:
            if not r["pruefung"]:
                print(f"  {r['id']}  {r['titel']:<20} {r['regel']}")
        print(f"\n{n-g} von {n} Regeln ohne Pruefpunkt.")
        return 0

    print("=" * 74)
    print(f"  REGEL-REGISTER  —  {g} von {n} Regeln erzwungen ({g/n:.0%})")
    print("=" * 74)
    for phase, titel in [("vorher", "VOR DEM RENDER"), ("nachher", "AM FERTIGEN VIDEO"),
                         ("langform", "AM LANGVIDEO"), ("dauerhaft", "SYSTEMZUSTAND")]:
        print(f"\n{titel}")
        for r in [x for x in REGELN if x["phase"] == phase]:
            zeichen = "erzwungen" if r["pruefung"] else "UNGEDECKT"
            print(f"  {r['id']}  [{zeichen:^9}]  {r['titel']:<18} {r['regel'][:52]}")
    print("\n" + "=" * 74)
    if g < n:
        print(f"  {n-g} Regel(n) ohne Pruefpunkt — sichtbar gefuehrt, nicht verschwiegen.")
    print("=" * 74)
    return 0


if __name__ == "__main__":
    sys.exit(main())
