"""Baut short-Configs (JSON) fuer jeden der 10 Shorts.
Verteilt Bilder gleichmaessig ueber die Voiceover-Laenge, mit Ken-Burns-
Zoom und Handkamera-Drift. Hook/Banner nur bei Pilot-Shorts (1, 3, 7, 9).
Ausschnitte werden pro Bild variiert (top/middle/bottom) fuer Mehrfach-
Einstellung aus einem Bild — die zentrale Regel aus CLAUDE.md.
"""
import json
import subprocess
from pathlib import Path

BASE = Path("/home/user/twitchclipz/okene")
FONT_BLACK = "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Black.ttf"

# Hook-Banner nur fuer die vier "Banger"-Shorts (Pilot + Story-Peaks)
HOOKS = {
    "01": {"text": "12 MANN. 1 ÜBERLEBENDER.", "y": 320, "size": 78},
    "04": {"text": "LUFT, GROSS WIE EIN KOPF", "y": 320, "size": 74},
    "06": {"text": "DIE LEICHE GRIFF ZURÜCK", "y": 320, "size": 76},
    "09": {"text": "63 STUNDEN. DANN LUFT.", "y": 320, "size": 76},
}

# Ausschnitts-Muster: (cx, cy, z0, z1, px, py) - verschiedene Ken-Burns
PATTERNS = [
    # top pattern: langsamer Zoom auf obere Bildhaelfte
    {"cx": 0.5, "cy": 0.32, "z0": 1.02, "z1": 1.14, "px": 0.0, "py": -0.05, "drift": 12},
    # middle pattern: leichter Push-in Mitte
    {"cx": 0.5, "cy": 0.50, "z0": 1.04, "z1": 1.18, "px": 0.0, "py": 0.0, "drift": 14},
    # bottom pattern: unten mit Zoom
    {"cx": 0.5, "cy": 0.68, "z0": 1.02, "z1": 1.14, "px": 0.0, "py": 0.05, "drift": 12},
    # detail push
    {"cx": 0.5, "cy": 0.45, "z0": 1.10, "z1": 1.24, "px": 0.02, "py": 0.0, "drift": 10},
]

def get_duration(path):
    out = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", str(path)
    ]).decode().strip()
    return float(out)


def build_config(idx):
    n = idx
    vo = BASE / "voiceover" / f"short_{n}.mp3"
    words = BASE / f"words_{n}.json"
    bild_dir = BASE / "bilder" / f"short_{n}"
    imgs = sorted(bild_dir.glob("*.jpg"))
    if not imgs:
        return None

    total = get_duration(vo)
    # Gleichmaessige Verteilung + kleine Kalt-Einstiegs-Beschleunigung:
    # Erste Einstellung ~2.5s (Detail-Hook), Rest gleichmaessig aufteilen.
    n_shots = len(imgs)
    if n_shots == 1:
        # Nur 1 Bild: 3 Einstellungen mit verschiedenen Crops aus dem einen Bild
        segs = []
        first = 2.8
        rem = total - first
        seg_dur = rem / 2
        segs.append({"img": str(imgs[0]), "start": 0, "end": first, **PATTERNS[3]})  # detail push
        segs.append({"img": str(imgs[0]), "start": first, "end": first + seg_dur, **PATTERNS[0]})  # top
        segs.append({"img": str(imgs[0]), "start": first + seg_dur, "end": total, **PATTERNS[2]})  # bottom
    else:
        # >=2 Bilder: erstes Bild 2.5-3s als Detail-Hook, dann gleichmaessig
        first = min(3.0, total / (n_shots + 0.5))
        rem = total - first
        rest_dur = rem / (n_shots - 1) if n_shots > 1 else rem
        segs = []
        t = 0
        for i, img in enumerate(imgs):
            if i == 0:
                segs.append({"img": str(img), "start": 0, "end": first, **PATTERNS[3]})
                t = first
            else:
                end = t + rest_dur if i < n_shots - 1 else total
                pat = PATTERNS[(i - 1) % 3]  # rotieren durch top/mid/bottom
                segs.append({"img": str(img), "start": t, "end": end, **pat})
                t = end

    cfg = {
        "shots": segs,
        "start": 0.0,
        "end": total,
        "audio": str(vo),
        "words": str(words),
        "font_black": FONT_BLACK,
        "teil": f"TEIL {int(n)}",
        "tmp": str(BASE / "tmp" / f"short_{n}"),
        "out": str(BASE / "output" / f"okene_{n}.mp4"),
        "musik": {"tonart": "D", "intensitaet": 0.85, "db": -25},
    }
    if n in HOOKS:
        cfg["hook"] = HOOKS[n]
        cfg["hook_until"] = 3.2

    out_path = BASE / "configs" / f"short_{n}.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
    return out_path


if __name__ == "__main__":
    for i in range(1, 11):
        n = f"{i:02d}"
        cfg_path = build_config(n)
        print(f"Short {n}: {cfg_path.name if cfg_path else 'SKIP (keine Bilder)'}")
