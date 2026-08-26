"""Baut V7-Configs + rendert alle 10 Prosperi-Shorts via short.py.
- Musik db=-16 (hoerbar).
- Manim-Karte als Opener fuer Short 09 (Algerien-Reveal).
- Hooks, TEIL-Leisten, Karaoke aus words_XX.json."""
import json, subprocess, sys, os
from pathlib import Path
sys.path.insert(0, "/home/user/twitchclipz")
import short as short_mod

BASE = Path("/home/user/twitchclipz/prosperi")
FONT = "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Black.ttf"
# Manim-Karte: nach Render aus media/videos/manim_scenes/... hierher kopiert
ANIM_MAP = BASE/"animation/prosperi_map.mp4"

PATTERNS = [
    {"cx":0.5,"cy":0.32,"z0":1.02,"z1":1.14,"px":0.0,"py":-0.05,"drift":12},
    {"cx":0.5,"cy":0.50,"z0":1.04,"z1":1.18,"px":0.0,"py":0.0,"drift":14},
    {"cx":0.5,"cy":0.68,"z0":1.02,"z1":1.14,"px":0.0,"py":0.05,"drift":12},
    {"cx":0.5,"cy":0.45,"z0":1.10,"z1":1.24,"px":0.02,"py":0.0,"drift":10},
]
# Hook-Banner (erste 3 s, großes Bild oben, darf vom VO abweichen)
HOOKS = {
    "01": {"text":"10 TAGE. ALLEIN. SAHARA.","y":330,"size":68},
    "07": {"text":"ER RITZTE SICH DIE HANDGELENKE.","y":330,"size":56},
    "09": {"text":"291 KM. ALGERIEN.","y":330,"size":72},
}
# Animation-Clip: Karte als Opener nur in Short 09
CLIPS = {
    "09": (0.0, 5.0),  # erste 5 s der Manim-Karte
}

def dur(p):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries",
        "format=duration","-of","csv=p=0",str(p)]).decode().strip())

def build_cfg(n):
    vo = BASE/"voiceover"/f"short_{n}.mp3"
    words = BASE/f"words_{n}.json"
    # KI-Bilder (bilder/SXX/) priorisiert, B-Roll (broll/short_XX/) als Fallback
    ki_imgs  = sorted((BASE/"bilder"/f"S{n}").glob("[0-9][0-9].jpg")) if (BASE/"bilder"/f"S{n}").exists() else []
    brl_imgs = sorted((BASE/"broll"/f"short_{n}").glob("[0-9][0-9].jpg"))
    imgs = ki_imgs + brl_imgs
    if not imgs:
        # fallback: nimm was in bilder/SXX oder broll/short_XX da ist
        imgs = sorted((BASE/"bilder").glob(f"S{n}/*.jpg")) + sorted((BASE/"broll").glob(f"short_{n}/*.jpg"))
    total = dur(vo)
    shots = []
    t = 0.0
    clip = CLIPS.get(n)
    if clip and ANIM_MAP.exists():
        cs, cd = clip
        cd = min(cd, total * 0.45)
        shots.append({"clip":str(ANIM_MAP),"clip_start":cs,"start":0,"end":cd})
        t = cd
    if imgs:
        rem = total - t
        first = min(3.0, rem / (len(imgs) + 0.3)) if not shots else rem / len(imgs)
        per = (rem - first) / (len(imgs) - 1) if len(imgs) > 1 else rem
        for i, img in enumerate(imgs):
            if i == 0 and not shots:
                seg_end = t + first; pat = PATTERNS[3]
            elif i == 0:
                seg_end = t + first; pat = PATTERNS[i % 3]
            else:
                seg_end = t + per; pat = PATTERNS[(i - 1) % 3] if not shots else PATTERNS[i % 3]
            if i == len(imgs) - 1: seg_end = total
            shots.append({"img": str(img), "start": t, "end": seg_end, **pat})
            t = seg_end
    if not shots:
        raise SystemExit(f"Short {n}: keine Bilder und kein Clip! Bitte Bilder in bilder/S{n}/ legen.")
    shots[-1]["end"] = total
    cfg = {
        "shots": shots, "start": 0.0, "end": total,
        "audio": str(vo), "words": str(words), "font_black": FONT,
        "tmp": str(BASE/"tmp"/f"short_{n}"),
        "out": str(BASE/"output"/f"prosperi_{n}.mp4"),
        "musik": {"tonart": "D", "intensitaet": 0.80, "db": -16},
    }
    if n not in CLIPS:
        cfg["teil"] = f"TEIL {int(n)}"
        if n in HOOKS:
            cfg["hook"] = HOOKS[n]; cfg["hook_until"] = 3.2
    else:
        # Short 09 hat Manim als Opener -> TEIL-Leiste trotzdem zeigen
        cfg["teil"] = f"TEIL {int(n)}"
        if n in HOOKS:
            cfg["hook"] = HOOKS[n]; cfg["hook_until"] = 3.2
    (BASE/"configs").mkdir(exist_ok=True)
    (BASE/"configs"/f"short_{n}.json").write_text(json.dumps(cfg, indent=2, ensure_ascii=False))
    return cfg

if __name__ == "__main__":
    (BASE/"output").mkdir(exist_ok=True)
    (BASE/"tmp").mkdir(exist_ok=True)
    only = sys.argv[1:] or [f"{i:02d}" for i in range(1, 11)]
    for n in only:
        cfg = build_cfg(n)
        print(f"[{n}] render {len(cfg['shots'])} shots, {cfg['end']:.1f}s ...", flush=True)
        short_mod.build(cfg)
    print("ALLE FERTIG", flush=True)
