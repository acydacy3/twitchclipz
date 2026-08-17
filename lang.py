"""
Das Langvideo bauen: 1920x1080, 16:9-Ausschnitte aus den Hochkantbildern.

    python3 lang.py

Der Kniff: die Bilder sind 1600x2848 (9:16). Ein 16:9-Ausschnitt daraus
ist 1600x900 - also nur 31 % der Bildhoehe. Jedes Bild liefert damit drei
bis vier klar unterschiedliche Einstellungen uebereinander, genau wofuer
die vertikale Staffelung in den Bildprompts gedacht war.

Gegen den "unfassbar statisch"-Eindruck von Video 1 wirken drei Dinge
zusammen: kurze Einstellungen (Schnitt ~6 s), weich beschleunigter Zoom
statt linearer Fahrt, und eine Handkamera-Mikrobewegung aus zwei
unterschiedlich schnellen Schwingungen.
"""
import json
import os
import subprocess
import sys

W, H = 1920, 1080
FPS = 30
SRC_W, SRC_H = 1600, 2848
FONT = "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Black.ttf"
VON, BIS = 3.06, 306.81          # ohne die Titelansage am Anfang


def crop_box(z, cy, cx=0.5):
    cw = SRC_W / z
    ch = cw * H / W
    x = cx * SRC_W - cw / 2
    y = cy * SRC_H - ch / 2
    x = max(0, min(SRC_W - cw, x))
    y = max(0, min(SRC_H - ch, y))
    return int(cw), int(ch), int(x), int(y)


def shot_filter(i, s):
    dur = s["end"] - s["start"]
    n = max(2, int(round(dur * FPS)))
    z0, z1 = s["z0"], s["z1"]
    cw, ch, cx, cy = crop_box(z0, s["cy"], s.get("cx", 0.5))
    bw, bh = W * 2, H * 2
    rel = z1 / z0
    base = 1.05

    t = f"(on/{n-1})"
    ease = f"({t}*{t}*(3-2*{t}))"
    zexpr = f"{base}+{base*(rel-1.0):.5f}*{ease}"

    a = s.get("drift", 12)
    dx = f"{a}*sin(on/{41+i*3})+{a*0.6:.1f}*cos(on/{89+i*5})"
    dy = f"{a*0.7:.1f}*cos(on/{59+i*4})+{a*0.5:.1f}*sin(on/{101+i*7})"

    px, py = s.get("px", 0.0), s.get("py", 0.0)
    xb = f"(iw-iw/zoom)/2+({px})*(iw-iw/zoom)*{ease}"
    yb = f"(ih-ih/zoom)/2+({py})*(ih-ih/zoom)*{ease}"

    return (
        f"[{i}:v]crop={cw}:{ch}:{cx}:{cy},"
        f"scale={bw}:{bh}:flags=lanczos,setsar=1,"
        f"zoompan=z='{zexpr}':x='{xb}+{dx}':y='{yb}+{dy}'"
        f":d={n}:s={W}x{H}:fps={FPS},"
        f"unsharp=5:5:0.50:5:5:0.0,vignette=PI/5.5,"
        f"noise=alls=5:allf=t+u,format=yuv420p[v{i}]"
    )


def b(n):
    return f"bilder/bild{n:02d}.jpg"


# (Endzeit, Bild, cy, z0, z1, py) - Endzeiten liegen auf Sprechpausen
SZENEN = [
    (  7.74, 1, 0.78, 1.15, 1.26,  0.0),
    ( 13.50, 1, 0.30, 1.00, 1.12,  0.30),
    ( 15.72, 1, 0.42, 1.22, 1.30,  0.0),
    ( 21.57, 1, 0.19, 1.05, 1.16,  0.0),
    ( 29.19, 1, 0.72, 1.18, 1.28, -0.20),
    ( 35.13, 3, 0.72, 1.18, 1.28,  0.0),
    ( 39.27, 3, 0.32, 1.06, 1.15,  0.0),
    ( 43.32, 1, 0.55, 1.14, 1.22,  0.0),
    ( 47.79, 2, 0.30, 1.04, 1.14,  0.0),
    ( 52.68, 2, 0.62, 1.22, 1.32,  0.0),
    ( 57.93, 2, 0.42, 1.00, 1.12, -0.30),
    ( 62.31, 2, 0.79, 1.16, 1.26,  0.0),
    ( 67.17, 2, 0.62, 1.28, 1.36,  0.0),
    ( 72.45, 2, 0.80, 1.10, 1.20,  0.0),
    ( 79.80, 3, 0.45, 1.05, 1.16,  0.25),
    ( 85.59, 3, 0.73, 1.24, 1.32,  0.0),
    ( 90.78, 3, 0.18, 1.10, 1.20,  0.0),
    ( 98.07, 3, 0.71, 1.26, 1.34,  0.0),
    (105.03, 3, 0.43, 1.04, 1.15, -0.20),
    (111.36, 3, 0.24, 1.16, 1.24,  0.0),
    (118.00, 4, 0.31, 1.10, 1.20,  0.0),
    (125.31, 4, 0.48, 1.22, 1.32,  0.0),
    (133.86, 4, 0.66, 1.14, 1.24,  0.20),
    (139.68, 4, 0.79, 1.12, 1.22,  0.0),
    (146.13, 5, 0.55, 1.04, 1.15,  0.0),
    (154.53, 5, 0.81, 1.18, 1.28,  0.0),
    (160.38, 5, 0.34, 1.08, 1.17,  0.0),
    (163.17, 5, 0.58, 1.26, 1.34,  0.0),
    (171.06, 6, 0.24, 1.04, 1.15, -0.30),
    (174.00, 6, 0.63, 1.16, 1.24,  0.0),
    (180.87, 6, 0.75, 1.22, 1.31,  0.0),
    (186.69, 6, 0.40, 1.08, 1.18,  0.25),
    (196.14, 7, 0.36, 1.10, 1.21,  0.0),
    (200.82, 7, 0.11, 1.16, 1.24,  0.0),
    (205.59, 7, 0.83, 1.20, 1.29,  0.0),
    (208.26, 8, 0.27, 1.04, 1.14,  0.0),
    (214.77, 8, 0.47, 1.14, 1.24,  0.0),
    (219.69, 8, 0.79, 1.22, 1.31,  0.0),
    (224.64, 8, 0.66, 1.28, 1.36,  0.0),
    (233.94, 8, 0.45, 1.08, 1.19, -0.25),
    (239.04, 9, 0.45, 1.10, 1.20,  0.0),
    (247.50, 9, 0.14, 1.16, 1.25,  0.0),
    (250.74, 9, 0.85, 1.16, 1.25,  0.0),
    (257.67, 7, 0.11, 1.13, 1.22,  0.0),
    (261.78, 7, 0.36, 1.04, 1.14,  0.0),
    (268.47, 7, 0.81, 1.20, 1.29,  0.0),
    (277.26, 6, 0.63, 1.10, 1.20,  0.0),
    (284.73, 6, 0.24, 1.04, 1.14, -0.28),
    (289.35, 10, 0.14, 1.13, 1.22,  0.0),
    (295.83, 10, 0.45, 1.16, 1.26,  0.0),
    (300.09, 10, 0.83, 1.10, 1.20,  0.0),
    (306.81, 10, 0.56, 1.22, 1.32,  0.0),
]


def bauen():
    tmp = "_tmp/lang"
    os.makedirs(tmp, exist_ok=True)
    os.makedirs("langvideo", exist_ok=True)
    out = "langvideo/san_jose_1080p.mp4"
    dur = BIS - VON

    # --- Ton -------------------------------------------------------------
    m = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-ss", str(VON), "-to", str(BIS),
         "-i", "voiceover.mp3", "-af",
         "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    js = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
    ln = ("loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={input_i}:"
          "measured_TP={input_tp}:measured_LRA={input_lra}:"
          "measured_thresh={input_thresh}:offset={target_offset}:"
          "linear=true").format(**js)
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error", "-ss", str(VON), "-to", str(BIS),
        "-i", "voiceover.mp3", "-af",
        f"{ln},volume=1.6dB,alimiter=limit=0.84:level=false:attack=2:release=60,"
        f"afade=t=in:st=0:d=0.08,afade=t=out:st={dur-1.2:.2f}:d=1.2",
        "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
        f"{tmp}/stimme.m4a"], check=True)

    subprocess.run([sys.executable, "musik.py", f"{tmp}/bett.wav",
                    f"{dur:.2f}", "--tonart", "D",
                    "--intensitaet", "0.85"], check=True)
    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", f"{tmp}/stimme.m4a", "-i", f"{tmp}/bett.wav",
        "-filter_complex",
        "[1:a]volume=-23dB,aformat=channel_layouts=stereo[m];"
        "[0:a]aformat=channel_layouts=stereo,asplit=2[v1][sc];"
        "[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=15:"
        "release=400:makeup=1[md];"
        "[v1][md]amix=inputs=2:normalize=0:duration=first[mx];"
        "[mx]alimiter=limit=0.84:level=false:attack=2:release=60[aout]",
        "-map", "[aout]", "-ar", "48000", "-c:a", "aac", "-b:a", "192k",
        f"{tmp}/mix.m4a"], check=True)

    # --- Untertitel (breit) ---------------------------------------------
    ass = f"{tmp}/cap.ass"
    subprocess.run([sys.executable, "karaoke.py", "words_fixed.json", ass,
                    str(VON), str(BIS), "--wide"], check=True)

    # --- Einstellungen ---------------------------------------------------
    shots, t = [], VON
    for bis, img, cy, z0, z1, py in SZENEN:
        shots.append({"img": b(img), "start": t - VON, "end": bis - VON,
                      "cy": cy, "z0": z0, "z1": z1, "py": py,
                      "drift": 11 + (len(shots) % 5) * 2})
        t = bis

    inputs, filters, labels = [], [], []
    for i, s in enumerate(shots):
        inputs += ["-i", s["img"]]
        filters.append(shot_filter(i, s))
        labels.append(f"[v{i}]")

    chain = ";".join(filters)
    chain += f";{''.join(labels)}concat=n={len(shots)}:v=1:a=0[cat]"
    chain += f";[cat]subtitles={ass}:fontsdir=/usr/share/fonts[vout]"

    cmd = (["ffmpeg", "-y", "-loglevel", "error"] + inputs +
           ["-i", f"{tmp}/mix.m4a", "-filter_complex", chain,
            "-map", "[vout]", "-map", f"{len(shots)}:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            "-shortest", out])
    print(f"{len(shots)} Einstellungen, Schnitt alle "
          f"{dur/len(shots):.1f}s, Laenge {dur:.1f}s")
    subprocess.run(cmd, check=True)
    print(f"fertig: {out}")


if __name__ == "__main__":
    bauen()
