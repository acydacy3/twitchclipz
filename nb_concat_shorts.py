"""
nb_concat_shorts.py — montiert die fertigen Shorts einer Serie zu EINEM Langvideo.

Der pragmatische Longform-Weg (Nutzer 06.09.): keine Ken-Burns-Diashow aus
Standbildern, sondern die bereits gebauten Shorts (mit ihrer Bewegung, ihren
Schnitten und Captions) in Erzählreihenfolge aneinanderfügen.

    python3 nb_concat_shorts.py <serie> [--order 2,3,4,...,1] [--wide]
                                [--kopf-weg 9]   Kopfzeile oben abschneiden
                                [--hintergrund dunkel|blur]

Liest <serie>/output/*.mp4 (aufsteigend sortiert = 01..10) und schreibt
<serie>/render/long.mp4. Re-Encode für einheitliche Parameter (die Shorts
können minimal driften). Standard 9:16 (wie die Shorts); --wide legt sie
mittig auf einen 16:9-Rahmen mit weichem, gezoomtem Hintergrund.

--hintergrund waehlt, was neben dem 9:16-Bild steht:
  blur    (Standard) weichgezeichneter Zoom desselben Bildes
  dunkel  ruhige, fast schwarze Flaeche
Fuer Shorts mit EINGEBRANNTEN Untertiteln ist "dunkel" die richtige Wahl. Der
weichgezeichnete Zoom vergroessert die Untertitel mit und legt sie als
lesbare Geisterschrift an beide Bildraender -- bei San Jose standen dort
"Die", "aufgeteilt", "zuerst" in halber Bildhoehe. Weichzeichnen loescht
Schrift nicht, es macht sie nur gross.

--kopf-weg <prozent> schneidet oben ab, BEVOR montiert wird. Grund: die
San-Jose-Shorts tragen oben ein eingebranntes "TEIL 2", "TEIL 9" — in einem
Langvideo liest sich das als aneinandergeklebte Shorts-Rolle, nicht als
Dokumentation. Was im Short die Reihe zusammenhält, zerlegt das Langvideo.
"""
import glob
import os
import subprocess
import sys


def find_shorts(serie, order):
    files = (sorted(glob.glob(f"{serie}/output/*.mp4"))
             or sorted(glob.glob(f"{serie}/render/short_*.mp4"))
             or [f for f in sorted(glob.glob(f"{serie}/render/*.mp4"))
                 if "long" not in os.path.basename(f).lower()])
    if not files:
        sys.exit(f"Keine Shorts in {serie}/output|render — erst nb_build.py laufen lassen.")
    if order:
        # order = Liste von Short-Nummern; ordne die gefundenen Dateien danach
        by_num = {}
        for f in files:
            digits = "".join(c for c in os.path.basename(f) if c.isdigit())
            by_num[digits.zfill(2)[-2:]] = f
        picked = [by_num[f"{n:02d}"] for n in order if f"{n:02d}" in by_num]
        return picked or files
    return files


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit("Nutzung: python3 nb_concat_shorts.py <serie> [--order ...] [--wide]")
    serie = args[0].rstrip("/")
    order = None
    if "--order" in sys.argv:
        order = [int(x) for x in sys.argv[sys.argv.index("--order") + 1].split(",")]
    wide = "--wide" in sys.argv
    hintergrund = "blur"
    if "--hintergrund" in sys.argv:
        hintergrund = sys.argv[sys.argv.index("--hintergrund") + 1]
        if hintergrund not in ("blur", "dunkel"):
            sys.exit("--hintergrund erwartet blur oder dunkel")
    kopf = 0.0
    if "--kopf-weg" in sys.argv:
        kopf = float(sys.argv[sys.argv.index("--kopf-weg") + 1]) / 100.0
        if not 0 <= kopf < 0.4:
            sys.exit("--kopf-weg erwartet 0 bis 39 (Prozent der Bildhöhe)")

    shorts = find_shorts(serie, order)
    os.makedirs(f"{serie}/render", exist_ok=True)
    os.makedirs(f"{serie}/_lang", exist_ok=True)
    out = f"{serie}/render/long.mp4"
    print(f"{len(shorts)} Shorts → {out}" + (f"   [16:9, Hintergrund {hintergrund}]" if wide else ""))
    for s in shorts:
        print("  +", os.path.basename(s))

    # Re-Encode-Concat über concat-Filter (robust gegen Parameter-Drift).
    inputs = []
    for s in shorts:
        inputs += ["-i", s]
    n = len(shorts)
    # Kopfzeile wegschneiden, bevor irgendetwas skaliert wird: sonst waere sie
    # im weichgezeichneten Hintergrund noch als Streifen zu erkennen.
    schnitt = (f"crop=iw:ih*{1 - kopf:.4f}:0:ih*{kopf:.4f}," if kopf else "")
    if kopf:
        print(f"  Kopfzeile: obere {kopf*100:.0f} % abgeschnitten")

    if wide:
        # jeder Clip: 9:16 mittig auf 1920x1080, dahinter geblurrter Zoom
        per = []
        for i in range(n):
            if hintergrund == "dunkel":
                # pad statt overlay auf einer color-Quelle: die erste Fassung
                # erzeugte je Short einen eigenen Farbgenerator und wurde vom
                # Kernel abgeschossen (SIGKILL, 10 Dekoder + 10 Generatoren).
                # pad braucht keinen zweiten Eingang und keinen Puffer.
                per.append(
                    f"[{i}:v]{schnitt}scale=-1:1080,"
                    f"pad=1920:1080:(ow-iw)/2:0:color=0x0B0D10,"
                    f"setsar=1,fps=30[v{i}]"
                )
            else:
                per.append(
                    f"[{i}:v]{schnitt}split=2[a{i}][b{i}];"
                    f"[a{i}]scale=1920:1080:force_original_aspect_ratio=increase,"
                    f"crop=1920:1080,gblur=sigma=48,eq=brightness=-0.22:saturation=0.7"
                    f"[bg{i}];"
                    f"[b{i}]scale=-1:1080[fg{i}];"
                    f"[bg{i}][fg{i}]overlay=(W-w)/2:0,setsar=1,fps=30[v{i}]"
                )
        vchain = ";".join(per)
        concat_in = "".join(f"[v{i}][{i}:a]" for i in range(n))
        chain = f"{vchain};{concat_in}concat=n={n}:v=1:a=1[vout][aout]"
    else:
        # 9:16 direkt aneinander (Shorts sind bereits 1080x1920)
        norm = ";".join(
            f"[{i}:v]{schnitt}scale=1080:1920:force_original_aspect_ratio=decrease,"
            f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30[v{i}]"
            for i in range(n))
        concat_in = "".join(f"[v{i}][{i}:a]" for i in range(n))
        chain = f"{norm};{concat_in}concat=n={n}:v=1:a=1[vout][aout]"

    cmd = (["ffmpeg", "-y", "-loglevel", "error"] + inputs +
           ["-filter_complex", chain, "-map", "[vout]", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart", out])
    subprocess.run(cmd, check=True)
    dur = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip()
    print(f"fertig: {out} ({float(dur):.1f}s)")


if __name__ == "__main__":
    main()
