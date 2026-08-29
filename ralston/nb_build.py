#!/usr/bin/env python3
"""V8 Ralston — Build-Skript: 10 Shorts mit Progress-Bar, Karaoke, Animation.

Aufruf (aus Repo-Root):
    python3 ralston/nb_build.py [--short 01]   # einzeln testen
    python3 ralston/nb_build.py                 # alle 10
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)

BROLL    = os.path.join(BASE, "bilder", "broll")
VO_DIR   = os.path.join(BASE, "voiceover")
ANIM_DIR = os.path.join(BASE, "animation")
RENDER   = os.path.join(BASE, "render")
MEDIA    = os.path.join(ROOT, "media", "videos", "manim_scenes")

os.makedirs(ANIM_DIR, exist_ok=True)
os.makedirs(RENDER, exist_ok=True)

# ── Konfiguration je Short ──────────────────────────────────────────────────
SHORTS = {
    "01": {"img": "hf_s01_truck.jpg",    "manim": None,             "grp": "A"},
    "02": {"img": "hf_s02_arm.jpg",      "manim": "CrossSection",   "grp": "A"},
    "03": {"img": "hf_s03_supplies.jpg", "manim": None,             "grp": "A"},
    "04": {"img": "hf_s04_chipping.jpg", "manim": "StatCounter",    "grp": "B"},
    "05": {"img": "hf_s05_carving.jpg",  "manim": "SurvivalDays",   "grp": "B"},
    "06": {"img": "hf_s06_camera.jpg",   "manim": None,             "grp": "B"},
    "07": {"img": "hf_s07_stars.jpg",    "manim": None,             "grp": "B"},
    "08": {"img": "hf_s02_arm.jpg",      "manim": "RockTrap",       "grp": "C"},
    "09": {"img": "hf_s09_rappel.jpg",   "manim": "CountdownTimer", "grp": "C"},
    "10": {"img": "hf_s07_stars.jpg",    "manim": None,             "grp": "C"},
}

# Manim-Klasse → Output-Pfad
def manim_path(cls_name):
    p = os.path.join(MEDIA, cls_name, "1080p60", f"{cls_name}.mp4")
    if os.path.exists(p):
        return p
    # fallback: suche rekursiv
    for root, _, files in os.walk(MEDIA):
        for f in files:
            if f == f"{cls_name}.mp4":
                return os.path.join(root, f)
    return None

# ── Hilfsfunktionen ─────────────────────────────────────────────────────────

def get_duration(path):
    r = subprocess.run(
        ["ffprobe", "-v", "quiet", "-print_format", "json",
         "-show_streams", path],
        capture_output=True, text=True, check=True,
    )
    streams = json.loads(r.stdout)["streams"]
    return float(streams[0]["duration"])


def generate_musik(wav_path, duration):
    """Synthesetisches Musikbett via musik.py."""
    if os.path.exists(wav_path):
        return
    print(f"  ♪ Musik generieren ({duration:.1f}s)…")
    subprocess.run(
        [sys.executable, os.path.join(ROOT, "musik.py"),
         wav_path, str(duration), "--intensitaet", "1.2", "--tonart", "D"],
        check=True,
    )


def transcribe_vo(mp3_path, json_path):
    """VO mit faster-whisper transkribieren → words_XX.json."""
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
        print(f"  ⚠ Transkription fehlgeschlagen: {e} — fahre ohne Karaoke fort")
        return []


def words_to_ass(words, duration, ass_path):
    """Word-Liste → ASS-Subtiteldatei (Chunk-Karaoke: 4 Wörter pro Zeile)."""
    header = """\
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
Timer: 100.0000

[V4+ Styles]
Format: Name,Fontname,Fontsize,PrimaryColour,SecondaryColour,OutlineColour,BackColour,Bold,Italic,Underline,StrikeOut,ScaleX,ScaleY,Spacing,Angle,BorderStyle,Outline,Shadow,Alignment,MarginL,MarginR,MarginV,Encoding
Style: Default,Arial,72,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,2,0,1,3,2,2,60,60,180,1

[Events]
Format: Layer,Start,End,Style,Name,MarginL,MarginR,MarginV,Effect,Text
"""

    def ts(t):
        h = int(t // 3600)
        m = int((t % 3600) // 60)
        s = t % 60
        return f"{h}:{m:02d}:{s:05.2f}"

    CHUNK = 4
    lines = []
    for i in range(0, len(words), CHUNK):
        chunk = words[i:i+CHUNK]
        start = chunk[0]["start"]
        end   = chunk[-1]["end"]
        text  = " ".join(w["word"] for w in chunk).strip()
        # ASS-Karaoke: ganze Zeile weiß, aktives Wort gelb
        # Vereinfacht: ganze Zeile in Caps+weiß
        text_esc = text.replace("{", r"\{").replace("}", r"\}")
        lines.append(f"Dialogue: 0,{ts(start)},{ts(end)},Default,,0,0,0,,{text_esc}")

    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(header)
        f.write("\n".join(lines))


def render_short(num, cfg):
    vo_path   = os.path.join(VO_DIR, f"short_{num}.mp3")
    img_path  = os.path.join(BROLL, cfg["img"])
    wav_path  = os.path.join(ANIM_DIR, f"musik_{num}.wav")
    words_path= os.path.join(ANIM_DIR, f"words_{num}.json")
    ass_path  = os.path.join(ANIM_DIR, f"sub_{num}.ass")
    out_path  = os.path.join(RENDER, f"short_{num}.mp4")

    print(f"\n{'='*50}")
    print(f"  S{num} | Gruppe {cfg['grp']} | Manim: {cfg['manim'] or '—'}")
    print(f"{'='*50}")

    if os.path.exists(out_path):
        print(f"  ✓ Bereits vorhanden: {out_path}")
        return

    dur = get_duration(vo_path)
    print(f"  VO-Dauer: {dur:.2f}s")

    generate_musik(wav_path, dur + 1.0)

    words = transcribe_vo(vo_path, words_path)
    if words:
        words_to_ass(words, dur, ass_path)

    # Manim-Animation suchen
    anim_clip = None
    if cfg["manim"]:
        anim_clip = manim_path(cfg["manim"])
        if anim_clip:
            print(f"  ✓ Animation: {anim_clip}")
        else:
            print(f"  ⚠ Animation {cfg['manim']} nicht gefunden — überspringe")

    # ── ffmpeg-Filtergraph bauen ───────────────────────────────────────────
    # Inputs: [0] VO, [1] Bild, [2] Musik, [3] Anim (optional)
    inputs = [
        "-i", vo_path,
        "-loop", "1", "-i", img_path,
        "-i", wav_path,
    ]

    has_anim = anim_clip and os.path.exists(anim_clip)
    anim_dur = 0.0
    if has_anim:
        anim_dur = min(get_duration(anim_clip), dur * 0.40)  # max 40% der Shortlänge
        inputs += ["-i", anim_clip]

    # Ken-Burns-Zoom auf dem Standbild
    kb = (
        f"[1:v]scale=1200:2133,setsar=1,"
        f"zoompan=z='min(zoom+0.0003,1.12)':d={int(dur*25)}:s=1080x1920,"
        f"fps=25[kb];"
    )

    if has_anim:
        # Anim für ersten Teil, danach Standbild
        split_t = anim_dur
        flt = (
            kb +
            f"[3:v]scale=1080:1920,setsar=1,fps=25[an];"
            f"[an]trim=0:{split_t:.2f},setpts=PTS-STARTPTS[an_part];"
            f"[kb]trim=0:{dur - split_t:.2f},setpts=PTS-STARTPTS[kb_part];"
            f"[an_part][kb_part]concat=n=2:v=1:a=0[vid_raw];"
        )
    else:
        flt = (
            kb +
            f"[kb]trim=0:{dur:.2f},setpts=PTS-STARTPTS[vid_raw];"
        )

    # Subtitle-Filter
    if words and os.path.exists(ass_path):
        ass_esc = ass_path.replace("\\", "\\\\").replace(":", "\\:")
        flt += f"[vid_raw]ass={ass_esc}[vid_sub];"
    else:
        flt += "[vid_raw]copy[vid_sub];"

    # Progress-Bar (gelb, 10px, unten)
    flt += (
        f"[vid_sub]drawbox="
        f"x=0:y=ih-10:"
        f"w='trunc(t/{dur:.3f}*iw)':"
        f"h=10:"
        f"color=0xFFD400@0.85:"
        f"t=fill[vout];"
    )

    # Audio-Mix: VO laut, Musik leise
    flt += (
        "[2:a]volume=0.12[mus];"
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
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  ✗ FEHLER:\n{result.stderr[-2000:]}")
    else:
        size = os.path.getsize(out_path) // 1024
        print(f"  ✓ Fertig: {out_path} ({size} KB)")


# ── Main ────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--short", help="Nur dieses Short rendern (z.B. 01)")
    args = parser.parse_args()

    targets = [args.short] if args.short else sorted(SHORTS.keys())
    for num in targets:
        cfg = SHORTS.get(num)
        if not cfg:
            print(f"Unbekanntes Short: {num}")
            continue
        render_short(num, cfg)

    print("\n✅ Alle Shorts fertig → ralston/render/")
