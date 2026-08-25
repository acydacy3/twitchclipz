"""Baut V6-Configs + rendert alle 10 Shorts via short.py.
- Musik db=-16 (HÖRBAR – war vorher -25 = unhörbar, Nutzer-Befund).
- Animation-Clips wo passend (Short 1 Opener, Short 5 Verkeilen).
- Hooks 1/5/9, TEIL-Leisten, Karaoke aus words_XX.json."""
import json, subprocess, sys, os
from pathlib import Path
sys.path.insert(0, "/home/user/twitchclipz")
import short as short_mod

BASE = Path("/home/user/twitchclipz/nuttyputty")
FONT = "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Black.ttf"
ANIM = BASE/"animation/querschnitt_demo.mp4"   # Banner+TEIL eingebrannt (gut f. Retention)

PATTERNS = [
    {"cx":0.5,"cy":0.32,"z0":1.02,"z1":1.14,"px":0.0,"py":-0.05,"drift":12},
    {"cx":0.5,"cy":0.50,"z0":1.04,"z1":1.18,"px":0.0,"py":0.0,"drift":14},
    {"cx":0.5,"cy":0.68,"z0":1.02,"z1":1.14,"px":0.0,"py":0.05,"drift":12},
    {"cx":0.5,"cy":0.45,"z0":1.10,"z1":1.24,"px":0.02,"py":0.0,"drift":10},
]
HOOKS = {
    "01": {"text":"18 x 10 CM. KOPFUEBER.","y":330,"size":74},
    "05": {"text":"70 GRAD KOPFUEBER","y":330,"size":76},
    "09": {"text":"DANN RISS DAS SEIL.","y":330,"size":76},
}
# Animation-Clip als Opener – nur Short 1 (Banner+TEIL eingebrannt -> short.py laesst die dort weg)
CLIPS = {
    "01": (0.0, 5.0),    # kriechen -> in den Spalt
}

def dur(p):
    return float(subprocess.check_output(["ffprobe","-v","error","-show_entries",
        "format=duration","-of","csv=p=0",str(p)]).decode().strip())

def build_cfg(n):
    vo = BASE/"voiceover"/f"short_{n}.mp3"
    words = BASE/f"words_{n}.json"
    imgs = sorted((BASE/"bilder"/f"short_{n}").glob("[0-9][0-9].jpg"))
    total = dur(vo)
    shots = []
    t = 0.0
    clip = CLIPS.get(n)
    if clip and ANIM.exists():
        cs, cd = clip
        cd = min(cd, total*0.5)
        shots.append({"clip":str(ANIM),"clip_start":cs,"start":0,"end":cd})
        t = cd
    # restliche Zeit auf Bilder verteilen
    if imgs:
        rem = total - t
        first = min(3.0, rem/(len(imgs)+0.3)) if not shots else rem/len(imgs)
        per = (rem-first)/(len(imgs)-1) if len(imgs) > 1 else rem
        for i, img in enumerate(imgs):
            if i == 0 and not shots:
                seg_end = t+first; pat = PATTERNS[3]
            elif i == 0:
                seg_end = t+first; pat = PATTERNS[i%3]
            else:
                seg_end = t+per; pat = PATTERNS[(i-1)%3] if not shots else PATTERNS[i%3]
            if i == len(imgs)-1: seg_end = total
            shots.append({"img":str(img), "start":t, "end":seg_end, **pat})
            t = seg_end
    if not shots:
        raise SystemExit(f"Short {n}: keine Bilder und kein Clip!")
    # letzten Shot bis total ziehen
    shots[-1]["end"] = total
    cfg = {
        "shots":shots, "start":0.0, "end":total,
        "audio":str(vo), "words":str(words), "font_black":FONT,
        "tmp":str(BASE/"tmp"/f"short_{n}"),
        "out":str(BASE/"output"/f"nutty_{n}.mp4"),
        "musik":{"tonart":"D","intensitaet":0.85,"db":-16},  # HÖRBAR (war -25 = unhörbar)
    }
    # Short 1 hat Banner+TEIL im Clip eingebrannt -> nicht doppeln
    if n not in CLIPS:
        cfg["teil"] = f"TEIL {int(n)}"
        if n in HOOKS:
            cfg["hook"]=HOOKS[n]; cfg["hook_until"]=3.2
    (BASE/"configs").mkdir(exist_ok=True)
    (BASE/"configs"/f"short_{n}.json").write_text(json.dumps(cfg,indent=2,ensure_ascii=False))
    return cfg

if __name__=="__main__":
    (BASE/"output").mkdir(exist_ok=True)
    only = sys.argv[1:] or [f"{i:02d}" for i in range(1,11)]
    for n in only:
        cfg = build_cfg(n)
        print(f"[{n}] render {len(cfg['shots'])} shots, {cfg['end']:.1f}s ...", flush=True)
        short_mod.build(cfg)
    print("ALLE FERTIG", flush=True)
