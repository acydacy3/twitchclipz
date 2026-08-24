"""
Einen Short bauen: Ausschnitte aus wenigen Bildern, weiche Fahrt,
Handkamera-Drift, Filmkorn, Karaoke-Untertitel, TEIL-Leiste, Aufhaenger.

    python3 short.py short07.json

Grundgedanke: ein Bild liefert nicht eine Einstellung, sondern drei bis
vier. Der Ausschnitt macht den Schnitt, nicht das Bildmaterial.
"""
import json
import subprocess
import sys
import os

W, H = 1080, 1920
FPS = 30
SRC_W, SRC_H = 1600, 2848        # Higgsfield 9:16


def crop_box(z, cx, cy):
    """Ausschnitt bei Zoomfaktor z um den Mittelpunkt (cx, cy), 9:16.

    cx/cy sind normiert (0..1). Der Kasten wird ins Bild geschoben,
    wenn er ueber den Rand ragt.
    """
    cw = SRC_W / z
    ch = cw * H / W
    if ch > SRC_H:                # Bild ist nicht hoch genug -> Breite kappen
        ch = SRC_H
        cw = ch * W / H
    x = cx * SRC_W - cw / 2
    y = cy * SRC_H - ch / 2
    x = max(0, min(SRC_W - cw, x))
    y = max(0, min(SRC_H - ch, y))
    return int(cw), int(ch), int(x), int(y)


def shot_filter(i, s):
    """Filterkette fuer eine Einstellung."""
    dur = s["end"] - s["start"]
    n = max(2, int(round(dur * FPS)))
    z0, z1 = s.get("z0", 1.0), s.get("z1", 1.12)
    cw, ch, cx, cy = crop_box(z0, s["cx"], s["cy"])

    # Arbeitsflaeche: doppelte Zielgroesse, damit zoompan nicht ruckelt
    # (zoompan rechnet ganzzahlig - auf kleiner Flaeche sieht man Stufen)
    bw, bh = W * 2, H * 2
    rel = z1 / z0

    # Grundzoom minimal ueber 1: bei genau 1 ist der Schwenkbereich null,
    # dann verschluckt zoompan die Handkamera-Bewegung komplett.
    base = 1.05

    # weiche Kurve statt linearem Zoom: smoothstep 3t^2-2t^3.
    # Linear faengt hart an und hoert hart auf - genau das wirkt "statisch".
    t = f"(on/{n-1})"
    ease = f"({t}*{t}*(3-2*{t}))"
    zexpr = f"{base}+{base*(rel-1.0):.5f}*{ease}"

    # Handkamera: zwei unterschiedlich schnelle Schwingungen, damit die
    # Bewegung nicht periodisch aussieht. Amplitude in Arbeitspixeln.
    a = s.get("drift", 14)
    dx = f"{a}*sin(on/{37+i*3})+{a*0.6:.1f}*cos(on/{83+i*5})"
    dy = f"{a*0.8:.1f}*cos(on/{53+i*4})+{a*0.5:.1f}*sin(on/{97+i*7})"

    # Grundfahrt zusaetzlich zum Zoom (Schwenk), normiert 0..1
    px = s.get("px", 0.0)
    py = s.get("py", 0.0)
    xbase = f"(iw-iw/zoom)/2+({px})*(iw-iw/zoom)*{ease}"
    ybase = f"(ih-ih/zoom)/2+({py})*(ih-ih/zoom)*{ease}"

    return (
        f"[{i}:v]crop={cw}:{ch}:{cx}:{cy},"
        f"scale={bw}:{bh}:flags=lanczos,setsar=1,"
        f"zoompan=z='{zexpr}':x='{xbase}+{dx}':y='{ybase}+{dy}'"
        f":d={n}:s={W}x{H}:fps={FPS},"
        f"unsharp=5:5:0.55:5:5:0.0,"
        f"vignette=PI/5,"
        f"noise=alls=6:allf=t+u,"
        f"format=yuv420p[v{i}]"
    )


def build(cfg):
    shots = cfg["shots"]
    t0, t1 = cfg["start"], cfg["end"]
    out = cfg["out"]
    tmp = cfg.get("tmp", "_tmp")
    os.makedirs(tmp, exist_ok=True)

    # --- 1. Ton: Fenster schneiden, auf -14 LUFS bringen ----------------
    # videocheck.py hat bei Video 1 -15,7 LUFS gemessen; YouTube dreht
    # dann hoch und das Rauschen kommt mit.
    aud = f"{tmp}/a.m4a"
    fade = ("afade=t=in:st=0:d=0.05,"
            f"afade=t=out:st={t1-t0-0.25:.2f}:d=0.25")

    # Zweistufig: erst messen, dann mit den gemessenen Werten normalisieren.
    # Einstufiges loudnorm schaetzt vorwaerts und lag bei Video 1 um 1,5 LU
    # daneben - genau der Fehler, den videocheck.py angemeckert hat.
    m = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats",
         "-ss", str(t0), "-to", str(t1), "-i", cfg["audio"],
         "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json",
         "-f", "null", "-"], capture_output=True, text=True).stderr
    js = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
    ln = ("loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={input_i}:"
          "measured_TP={input_tp}:measured_LRA={input_lra}:"
          "measured_thresh={input_thresh}:offset={target_offset}:"
          "linear=true:print_format=summary").format(**js)

    subprocess.run([
        "ffmpeg", "-y", "-loglevel", "error",
        "-ss", str(t0), "-to", str(t1), "-i", cfg["audio"],
        # loudnorm allein kommt nur auf -15,2 LUFS: die Rohspur liegt bei
        # -22,4 LUFS mit -3,7 dBTP, mehr Gain wuerde die Spitzengrenze
        # reissen. Der Limiter schafft die letzten 1,6 dB.
        # level=false ist Pflicht - sonst zieht alimiter das Ergebnis
        # selbsttaetig auf Vollaussteuerung hoch (gemessen: +0,1 dBFS).
        "-af", f"{ln},volume=1.6dB,"
               f"alimiter=limit=0.84:level=false:attack=2:release=60,{fade}",
        "-ar", "48000", "-c:a", "aac", "-b:a", "192k", f"{tmp}/stimme.m4a"],
        check=True)

    # --- 1b. Musikbett darunterlegen ------------------------------------
    mus = cfg.get("musik")
    if not mus:
        aud = f"{tmp}/stimme.m4a"
    else:
        bett = f"{tmp}/bett.wav"
        subprocess.run([sys.executable, "musik.py", bett, f"{t1-t0:.2f}",
                        "--tonart", mus.get("tonart", "D"),
                        "--intensitaet", str(mus.get("intensitaet", 1.0))],
                       check=True)
        # Ducking: die Musik weicht der Stimme aus, statt dass man die
        # Musik pauschal leise dreht. In Sprechpausen kommt sie hoch -
        # das ist der Effekt, den man aus guten Doku-Shorts kennt.
        db = mus.get("db", -21)
        mix = (
            f"[1:a]volume={db}dB,aformat=channel_layouts=stereo[m];"
            f"[0:a]aformat=channel_layouts=stereo,asplit=2[v1][sc];"
            f"[m][sc]sidechaincompress=threshold=0.03:ratio=8:"
            f"attack=15:release=400:makeup=1[md];"
            f"[v1][md]amix=inputs=2:normalize=0:duration=first[mx];"
            f"[mx]alimiter=limit=0.84:level=false:attack=2:release=60[aout]"
        )
        aud = f"{tmp}/mix.m4a"
        subprocess.run([
            "ffmpeg", "-y", "-loglevel", "error",
            "-i", f"{tmp}/stimme.m4a", "-i", bett,
            "-filter_complex", mix, "-map", "[aout]",
            "-ar", "48000", "-c:a", "aac", "-b:a", "192k", aud], check=True)

    # --- 2. Untertitel --------------------------------------------------
    ass = f"{tmp}/cap.ass"
    subprocess.run([sys.executable, "karaoke.py", cfg["words"], ass,
                    str(t0), str(t1)], check=True)

    # --- 3. Einstellungen ------------------------------------------------
    # Jedes Bild geht als EIN Frame hinein. zoompan erzeugt daraus d Frames.
    # (Mit -loop 1 bekaeme zoompan d Frames je Eingangsframe - das sprengt
    #  die Zeitachse und war der Grund, warum sich Einstellungen wiederholten.)
    inputs, filters, labels = [], [], []
    for i, s in enumerate(shots):
        inputs += ["-i", s["img"]]
        filters.append(shot_filter(i, s))
        labels.append(f"[v{i}]")

    chain = ";".join(filters)
    chain += f";{''.join(labels)}concat=n={len(shots)}:v=1:a=0[cat]"

    # --- 4. TEIL-Leiste, Aufhaenger, Pfeil, Untertitel -------------------
    bar_h = 130
    teil = cfg.get("teil")
    cur = "[cat]"
    if teil:
        chain += (
            f";{cur}drawbox=x=0:y=70:w={W}:h={bar_h}:color=black@0.72:t=fill,"
            f"drawtext=text='{teil}':fontfile={cfg['font_black']}:"
            f"fontsize=62:fontcolor=white:x=(w-text_w)/2:y=104[bar]"
        )
        cur = "[bar]"

    # Aufhaenger: grosse Zeile in den ersten Sekunden, inhaltlich NICHT
    # dasselbe wie der gesprochene Satz - sonst verschenkt man einen Kanal.
    hook = cfg.get("hook")
    if hook:
        ht = cfg.get("hook_until", 3.2)
        htext = hook["text"]
        # Groesse automatisch an die Laenge anpassen. Roboto Black belegt
        # rund 0,49 px je Zeichen und Groessenpunkt; dazu 2x26 px
        # Kastenrand. Bei 1080 Breite und 40 px Luft links und rechts
        # bleiben 1000 px. Ohne diese Rechnung lief der Text bei langen
        # Aufhaengern ueber den Rand hinaus (Teil 3, 6, 10 im 1. Lauf).
        auto = int((840 - 52) / (0.49 * max(len(htext), 8)))
        hsize = min(hook.get("size", 78), auto)
        chain += (
            f";{cur}drawtext=text='{htext}':fontfile={cfg['font_black']}:"
            f"fontsize={hsize}:fontcolor=white:"
            f"borderw=8:bordercolor=black:"
            f"box=1:boxcolor=#C81E1E@0.92:boxborderw=26:"
            f"x=(w-text_w)/2:y={hook.get('y',330)}:"
            f"enable='lt(t,{ht})'[hook]"
        )
        cur = "[hook]"

    # roter Pfeil als eigenes Bild (drawtext kann keine Formen)
    arrow = cfg.get("arrow")
    if arrow:
        inputs += ["-i", arrow["img"]]
        ai = len(shots)
        chain += (
            f";[{ai}:v]format=rgba,scale={arrow.get('w',300)}:-1[arw]"
            f";{cur}[arw]overlay=x={arrow['x']}:y={arrow['y']}:"
            f"enable='lt(t,{cfg.get('hook_until',3.2)})'[ov]"
        )
        cur = "[ov]"

    chain += f";{cur}subtitles={ass}:fontsdir=/usr/share/fonts[vout]"

    cmd = (["ffmpeg", "-y", "-loglevel", "error"] + inputs + ["-i", aud] +
           ["-filter_complex", chain, "-map", "[vout]",
            "-map", f"{len(shots)+(1 if arrow else 0)}:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "19",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "192k", "-shortest", out])
    subprocess.run(cmd, check=True)
    print(f"fertig: {out}")


if __name__ == "__main__":
    build(json.load(open(sys.argv[1], encoding="utf-8")))
