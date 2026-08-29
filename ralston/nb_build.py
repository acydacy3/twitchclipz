#!/usr/bin/env python3
"""V8 Ralston — Build-Skript v2: Multi-Shot, Karaoke-Highlight, sichtbare Progressbar.

Korrekturen ggü. v1:
  - Jedes Short hat 3-4 verschiedene Bilder (kein EIN-BILD-Problem mehr)
  - ASS-Karaoke mit \\kf-Tags: Wörter leuchten gelb beim Sprechen
  - Progressbar: h=20, voll opak, sichtbar gelb
  - KB-Zoom: wechselt zwischen 4 Presets (in/out/pan-r/pan-l)

Aufruf (aus Repo-Root):
    python3 ralston/nb_build.py [--short 01]   # einzeln testen
    python3 ralston/nb_build.py                # alle 10
"""
import argparse
import json
import os
import subprocess
import sys

BASE     = os.path.dirname(os.path.abspath(__file__))
ROOT     = os.path.dirname(BASE)
BROLL    = os.path.join(BASE, "bilder", "broll")
VO_DIR   = os.path.join(BASE, "voiceover")
ANIM_DIR = os.path.join(BASE, "animation")
RENDER   = os.path.join(BASE, "render")
MEDIA    = os.path.join(ROOT, "media", "videos", "manim_scenes")

os.makedirs(ANIM_DIR, exist_ok=True)
os.makedirs(RENDER, exist_ok=True)

# ── Multi-Shot-Config (2-4 Bilder pro Short) ────────────────────────────────
# imgs: Liste der Bilder (werden gleichmäßig über VO-Dauer aufgeteilt)
# manim: Manim-Klasse (spielt am Anfang, max 38 % der VO-Dauer)
SHORTS = {
    # ab: "A"|"B"|None — A/B-Hook-Test. Gleiches Video, verschiedener Hook im Titel (metadata.json).
    # Gleiche Produktions-Parameter, nur Titel-Variante unterscheidet sich → sauberes A/B.
    "01": {
        "imgs":  ["hf_s01_truck.jpg", "hf_s02_arm.jpg", "hf_s09_rappel.jpg"],
        "manim": None, "grp": "A", "ab": None,
    },
    "02": {
        "imgs":  ["hf_s01_truck.jpg", "hf_s04_chipping.jpg", "hf_s02_arm.jpg"],
        "manim": "CrossSection", "grp": "A", "ab": None,
    },
    "03": {
        "imgs":  ["hf_s03_supplies.jpg", "hf_s04_chipping.jpg", "hf_s02_arm.jpg"],
        "manim": None, "grp": "A", "ab": None,
    },
    "04": {
        "imgs":  ["hf_s04_chipping.jpg", "hf_s02_arm.jpg", "hf_s03_supplies.jpg"],
        "manim": "StatCounter", "grp": "B", "ab": None,
    },
    "05": {
        "imgs":  ["hf_s05_carving.jpg", "hf_s02_arm.jpg", "hf_s07_stars.jpg"],
        "manim": "SurvivalDays", "grp": "B", "ab": None,
    },
    "06": {
        "imgs":  ["hf_s06_camera.jpg", "hf_s07_stars.jpg", "hf_s02_arm.jpg"],
        "manim": None, "grp": "B", "ab": None,
    },
    "07": {
        "imgs":  ["hf_s07_stars.jpg", "hf_s02_arm.jpg", "hf_s05_carving.jpg", "hf_s07_stars.jpg"],
        "manim": None, "grp": "B", "ab": None,
    },
    "08": {
        "imgs":  ["hf_s02_arm.jpg", "hf_s04_chipping.jpg", "hf_s09_rappel.jpg", "hf_s02_arm.jpg"],
        "manim": "RockTrap", "grp": "C", "ab": None,
    },
    "09": {
        "imgs":  ["hf_s09_rappel.jpg", "hf_s02_arm.jpg", "hf_s09_rappel.jpg", "hf_s01_truck.jpg"],
        "manim": "CountdownTimer", "grp": "C", "ab": None,
    },
    "10": {
        "imgs":  ["hf_s09_rappel.jpg", "hf_s07_stars.jpg", "hf_s01_truck.jpg", "hf_s09_rappel.jpg"],
        "manim": None, "grp": "C", "ab": None,
    },
}

# Ken-Burns-Presets: abwechseln zwischen zoom-in, zoom-out, pan-rechts, pan-links
KB_PRESETS = [
    # 0: langsam reinzoomen (Standard)
    "z='min(zoom+{rate},1.12)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
    # 1: herauszoomen
    "z='if(eq(on,1),1.12,max(zoom-{rate},1.0))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'",
    # 2: reinzoomen, leicht nach unten schwenken
    "z='min(zoom+{rate},1.10)':x='iw/2-(iw/zoom/2)':y='min(ih/2-(ih/zoom/2)+{ydrift}*on,ih-(ih/zoom))'",
    # 3: reinzoomen, leicht nach oben schwenken
    "z='min(zoom+{rate},1.10)':x='iw/2-(iw/zoom/2)':y='max(ih/2-(ih/zoom/2)-{ydrift}*on,0)'",
]


def manim_path(cls_name):
    for root, _, files in os.walk(MEDIA):
        for f in files:
            if f == f"{cls_name}.mp4":
                return os.path.join(root, f)
    return None


def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", path],
        capture_output=True, text=True, check=True,
    )
    return float(json.loads(r.stdout)["streams"][0]["duration"])


def generate_musik(wav_path, duration):
    if os.path.exists(wav_path):
        return
    print(f"  ♪ Musik generieren ({duration:.1f}s)…")
    subprocess.run(
        [sys.executable, os.path.join(ROOT, "musik.py"),
         wav_path, str(duration), "--intensitaet", "1.2", "--tonart", "D"],
        check=True,
    )


def transcribe_vo(mp3_path, json_path):
    if os.path.exists(json_path):
        with open(json_path) as f:
            return json.load(f)
    print(f"  ✍ Transkribiere {os.path.basename(mp3_path)}…")
    try:
        from faster_whisper import WhisperModel
        model = WhisperModel("base", device="cpu", compute_type="int8")
        segs, _ = model.transcribe(mp3_path, word_timestamps=True, language="de")
        words = []
        for seg in segs:
            for w in (seg.words or []):
                words.append({"word": w.word.strip(), "start": w.start, "end": w.end})
        with open(json_path, "w") as f:
            json.dump(words, f, ensure_ascii=False, indent=2)
        return words
    except Exception as e:
        print(f"  ⚠ Transkription fehlgeschlagen: {e}")
        return []


def words_to_ass(words, ass_path):
    """Karaoke-ASS mit \\kf: Wörter leuchten gelb beim Sprechen auf.

    ASS-Farb-Convention: &HAABBGGRR (Alpha, Blue, Green, Red)
    Gelb (RGB 255,255,0) = &H0000FFFF
    Weiß = &H00FFFFFF
    Dunkelgrau (halb-transparent) = &H80AAAAAA
    """
    header = """\
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
Timer: 100.0000

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Arial,76,&H0000FFFF,&H00FFFFFF,&H00000000,&H99000000,-1,0,0,0,100,100,1,0,1,4,2,2,60,60,220,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""
    # PrimaryColour=Gelb (aktiv/gesprochen), SecondaryColour=Weiß (noch nicht gesprochen)
    # \\kf<cs>: smooth-fill-Karaoke, cs = Centisekunden Dauer dieses Wortes

    def ts(t):
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = t % 60
        return f"{h}:{m:02d}:{s:05.2f}"

    CHUNK = 4
    lines = []
    for i in range(0, len(words), CHUNK):
        chunk = words[i:i + CHUNK]
        start = chunk[0]["start"]
        end   = chunk[-1]["end"]
        parts = []
        for w in chunk:
            cs = max(1, int((w["end"] - w["start"]) * 100))
            esc = w["word"].replace("{", r"\{").replace("}", r"\}")
            parts.append(f"{{\\kf{cs}}}{esc}")
        text = " ".join(parts)
        lines.append(f"Dialogue: 0,{ts(start)},{ts(end)},Default,,0,0,0,,{text}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header)
        f.write("\n".join(lines))


def render_short(num, cfg):
    vo_path    = os.path.join(VO_DIR,   f"short_{num}.mp3")
    wav_path   = os.path.join(ANIM_DIR, f"musik_{num}.wav")
    words_path = os.path.join(ANIM_DIR, f"words_{num}.json")
    ass_path   = os.path.join(ANIM_DIR, f"sub_{num}.ass")
    out_path   = os.path.join(RENDER,   f"short_{num}.mp4")

    print(f"\n{'='*55}")
    print(f"  S{num} | Gruppe {cfg['grp']} | {len(cfg['imgs'])} Bilder | Manim: {cfg.get('manim') or '—'}")
    print(f"{'='*55}")

    if os.path.exists(out_path):
        os.remove(out_path)
        print(f"  ↺ Alter Render gelöscht.")

    dur = get_duration(vo_path)
    print(f"  VO-Dauer: {dur:.2f}s")

    generate_musik(wav_path, dur + 1.0)

    words = transcribe_vo(vo_path, words_path)
    # ASS immer neu generieren (korrekte \\kf-Karaoke)
    if words:
        words_to_ass(words, ass_path)

    # Manim suchen
    manim_cls = cfg.get("manim")
    anim_clip = manim_path(manim_cls) if manim_cls else None
    has_anim  = bool(anim_clip and os.path.exists(anim_clip))
    anim_dur  = 0.0
    if has_anim:
        anim_dur = min(get_duration(anim_clip), dur * 0.38)
        print(f"  ✓ Animation: {os.path.basename(anim_clip)} ({anim_dur:.1f}s)")
    elif manim_cls:
        print(f"  ⚠ Animation '{manim_cls}' nicht gefunden — nur Bilder")

    imgs         = cfg["imgs"]
    img_total    = dur - anim_dur
    seg_dur      = img_total / len(imgs)
    print(f"  Bildsequenz: {len(imgs)} × {seg_dur:.1f}s")

    # ── ffmpeg-Inputs ──────────────────────────────────────────────────────
    # Reihenfolge: [0]=VO, [1..N]=Bilder, [N+1]=Musik, [N+2]=Anim(opt)
    inputs = ["-i", vo_path]
    for img in imgs:
        inputs += ["-i", os.path.join(BROLL, img)]
    mus_idx  = len(imgs) + 1
    inputs  += ["-i", wav_path]
    anim_idx = None
    if has_anim:
        anim_idx = len(imgs) + 2
        inputs  += ["-i", anim_clip]

    # ── Filtergraph ────────────────────────────────────────────────────────
    flt      = ""
    seg_lbls = []
    fps      = 25

    for i, img in enumerate(imgs):
        frames  = max(fps, int(seg_dur * fps))
        preset  = KB_PRESETS[i % len(KB_PRESETS)]
        rate    = round(0.12 / frames, 6)   # von 1.0 auf ~1.12 über die Segmentdauer
        ydrift  = round(0.3 / frames, 6)
        kb_expr = preset.format(rate=rate, ydrift=ydrift)
        lbl     = f"[kb{i}]"
        flt    += (
            f"[{i+1}:v]scale=1296:2304,setsar=1,"
            f"zoompan={kb_expr}:d={frames}:s=1080x1920,"
            f"fps={fps},trim=0:{seg_dur:.4f},setpts=PTS-STARTPTS{lbl};"
        )
        seg_lbls.append(lbl)

    # Bilder zusammenführen
    concat_in = "".join(seg_lbls)
    flt += f"{concat_in}concat=n={len(imgs)}:v=1:a=0[imgs];"

    if has_anim:
        flt += (
            f"[{anim_idx}:v]scale=1080:1920,setsar=1,fps={fps},"
            f"trim=0:{anim_dur:.4f},setpts=PTS-STARTPTS[an];"
            f"[an][imgs]concat=n=2:v=1:a=0[vid_raw];"
        )
    else:
        flt += "[imgs]copy[vid_raw];"

    # Karaoke-Subtitles
    if words and os.path.exists(ass_path):
        ass_esc = ass_path.replace("\\", "\\\\").replace(":", "\\:")
        flt += f"[vid_raw]ass={ass_esc}[vid_sub];"
    else:
        flt += "[vid_raw]copy[vid_sub];"

    # Progressbar: 20 px, gelb, voll opak, wächst mit t
    flt += (
        f"[vid_sub]drawbox="
        f"x=0:y=ih-20:"
        f"w='trunc(t/{dur:.4f}*iw)':"
        f"h=20:"
        f"color=yellow:"
        f"t=fill[vid_pb];"
    )

    # CTA-Overlay: letzte 4 Sekunden (min. ab 75% Laufzeit)
    # "Kanal folgen" eingebrannt — kein Laufzeit-Fehler auch bei sehr kurzen Clips
    cta_start = round(max(dur - 4.0, dur * 0.75), 4)
    cta_end   = round(dur - 0.1, 4)
    flt += (
        f"[vid_pb]drawtext="
        f"text='► Kanal folgen':"
        f"fontsize=40:fontcolor=white@0.95:"
        f"x=(w-text_w)/2:y=h*0.78:"
        f"enable='between(t,{cta_start},{cta_end})':"
        f"box=1:boxcolor=black@0.50:boxborderw=12"
        f"[vout];"
    )

    # Audio: VO laut, Musik leise im Hintergrund
    flt += (
        f"[{mus_idx}:a]volume=0.12[mus];"
        "[0:a][mus]amix=inputs=2:duration=first:dropout_transition=2[aout]"
    )

    cmd = (
        ["ffmpeg", "-y"]
        + inputs
        + [
            "-filter_complex", flt,
            "-map", "[vout]",
            "-map", "[aout]",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            "-t", str(dur),
            "-pix_fmt", "yuv420p",
            out_path,
        ]
    )

    print(f"  ▶ ffmpeg render…")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=360)
    if result.returncode != 0:
        print(f"  ✗ FEHLER:\n{result.stderr[-3000:]}")
    else:
        size = os.path.getsize(out_path) // 1024
        print(f"  ✓ {out_path}  ({size} KB, {dur:.1f}s)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--short", help="Nur dieses Short (z.B. 01)")
    args = parser.parse_args()

    targets = [args.short] if args.short else sorted(SHORTS.keys())
    for num in targets:
        cfg = SHORTS.get(num)
        if not cfg:
            print(f"Unbekanntes Short: {num}")
            continue
        render_short(num, cfg)

    print("\n✅ Alle Shorts fertig → ralston/render/")
