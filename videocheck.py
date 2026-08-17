"""
Qualitaetskontrolle vor dem Upload: Ton, Untertitel, Bild.

    python3 videocheck.py final_video.mp4 [captions_de.srt]

Prueft:
  TON        Lautheit (LUFS), Spitzenpegel, Uebersteuerung, Stille-Luecken
  BILD       Aufloesung, Bildrate, Pixelformat (faengt den yuv444p-Bug)
  UNTERTITEL Lesegeschwindigkeit, Zeilenlaenge, Ueberlappungen
  FRAMES     zieht Standbilder zur Sichtpruefung
"""
import subprocess
import sys
import os
import re

YT_TARGET_LUFS = -14.0     # YouTube normalisiert auf ~-14 LUFS
MAX_CPS = 21               # Zeichen pro Sekunde, Lesbarkeitsgrenze
MAX_LINE = 45              # Zeichen pro Zeile


def sh(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stderr


def ton(path):
    print("\n--- TON " + "-" * 54)
    out = sh(["ffmpeg", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"])
    tail = out[-2500:]

    def grab(label):
        m = re.findall(rf"{label}:\s*(-?[\d.]+|-inf)", tail)
        return m[-1] if m else None

    lufs = grab("I")
    lra = grab("LRA")
    peak = grab("Peak")

    if lufs and lufs != "-inf":
        v = float(lufs)
        diff = v - YT_TARGET_LUFS
        note = "OK" if abs(diff) <= 1.5 else (
            f"{abs(diff):.1f} LU zu leise -> YouTube dreht hoch" if diff < 0
            else f"{diff:.1f} LU zu laut -> YouTube dreht runter")
        print(f"  Lautheit        {v:6.1f} LUFS   (Ziel {YT_TARGET_LUFS})  {note}")
    if lra:
        print(f"  Dynamikumfang   {float(lra):6.1f} LU     "
              f"{'OK' if 3 <= float(lra) <= 12 else 'auffaellig (sehr flach oder sehr sprunghaft)'}")
    if peak and peak != "-inf":
        p = float(peak)
        print(f"  Spitzenpegel    {p:6.1f} dBTP   "
              f"{'OK' if p <= -1.0 else 'UEBERSTEUERT -> hoerbare Verzerrung moeglich'}")

    # Stille-Luecken
    out2 = sh(["ffmpeg", "-i", path, "-af", "silencedetect=n=-40dB:d=1.5", "-f", "null", "-"])
    gaps = re.findall(r"silence_start:\s*([\d.]+)[\s\S]*?silence_duration:\s*([\d.]+)", out2)
    if gaps:
        print(f"  Stille >1,5s    {len(gaps)} Stelle(n):")
        for s, d in gaps[:6]:
            t = float(s)
            print(f"                  bei {int(t)//60}:{t%60:05.2f}  ({float(d):.1f}s)")
    else:
        print("  Stille >1,5s    keine  OK")


def bild(path):
    print("\n--- BILD " + "-" * 53)
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height,r_frame_rate,pix_fmt,profile",
         "-show_entries", "format=duration,size", "-of", "default=noprint_wrappers=1",
         path],
        capture_output=True, text=True).stdout
    d = dict(l.split("=", 1) for l in out.strip().splitlines() if "=" in l)
    w, h = d.get("width"), d.get("height")
    pix = d.get("pix_fmt", "?")
    dur = float(d.get("duration", 0))
    print(f"  Aufloesung      {w}x{h}")
    print(f"  Bildrate        {d.get('r_frame_rate','?')}")
    print(f"  Pixelformat     {pix}  "
          f"{'OK' if pix == 'yuv420p' else 'ACHTUNG -> viele Player koennen das nicht abspielen'}")
    print(f"  Profil          {d.get('profile','?')}")
    print(f"  Laenge          {int(dur)//60}:{dur%60:05.2f}")
    print(f"  Dateigroesse    {int(d.get('size',0))/1e6:.1f} MB")


def untertitel(path):
    print("\n--- UNTERTITEL " + "-" * 47)
    import pysubs2
    subs = pysubs2.load(path)
    lang, fast, ovl = [], [], 0
    prev_end = -1
    for i, l in enumerate(subs):
        txt = l.text.replace("\\N", " ")
        dur = (l.end - l.start) / 1000.0
        if len(txt) > MAX_LINE:
            lang.append((i + 1, len(txt), txt[:40]))
        if dur > 0 and len(txt) / dur > MAX_CPS:
            fast.append((i + 1, len(txt) / dur, txt[:40]))
        if l.start < prev_end:
            ovl += 1
        prev_end = l.end
    print(f"  Bloecke         {len(subs)}")
    print(f"  zu lange Zeilen {len(lang)}  (>{MAX_LINE} Zeichen)")
    for n, c, t in lang[:5]:
        print(f"                  #{n}: {c} Zeichen  \"{t}...\"")
    print(f"  zu schnell      {len(fast)}  (>{MAX_CPS} Zeichen/Sek.)")
    for n, c, t in fast[:5]:
        print(f"                  #{n}: {c:.0f} Z/s  \"{t}...\"")
    print(f"  Ueberlappungen  {ovl}  {'OK' if ovl == 0 else 'pruefen'}")


def frames(path, n=6):
    print("\n--- FRAMES " + "-" * 51)
    dur = float(subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", path],
        capture_output=True, text=True).stdout.strip())
    outdir = "qc_frames"
    os.makedirs(outdir, exist_ok=True)
    for i in range(n):
        t = dur * (i + 0.5) / n
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t),
                        "-i", path, "-frames:v", "1",
                        f"{outdir}/qc_{int(t):04d}s.jpg"])
    print(f"  {n} Standbilder in {outdir}/ zur Sichtpruefung")


if __name__ == "__main__":
    v = sys.argv[1]
    print("=" * 62 + f"\n{v}\n" + "=" * 62)
    bild(v)
    ton(v)
    if len(sys.argv) > 2:
        untertitel(sys.argv[2])
    frames(v)
