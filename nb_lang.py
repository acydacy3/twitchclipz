"""
nb_lang.py — GENERISCHER Longform-Builder (verallgemeinert lang.py).

Baut aus einer fertigen Short-Serie ein 16:9-Langvideo (1920x1080), indem es
die bereits veröffentlichten VO-Segmente in Erzählreihenfolge montiert, die
9:16-Bilder per Ken-Burns in 16:9-Einstellungen schneidet, die Wort-Timings der
Shorts zu einer durchlaufenden Karaoke-Spur mergt und ein Musikbett unterlegt.

    python3 nb_lang.py <serie>                # z.B. prosperi
    python3 nb_lang.py <serie> --order 2,3,4,5,6,7,8,9,10,1   # eigene Reihenfolge
    python3 nb_lang.py <serie> --gap 0.35 --shot 6.0

Erwartet je Serie (autom. gefunden):
  <serie>/voiceover/short_NN.mp3      VO-Segmente (echte Stimme der Shorts)
  <serie>/words_NN.json  ODER  <serie>/animation/words_NN.json   Wort-Timings
  <serie>/bilder/SNN/*.jpg            Bild(er) je Short (9:16)

Ausgabe: <serie>/render/long.mp4  (+ Zwischenschritte in <serie>/_lang/)

Kein Hardcoding: Bilddimensionen, Segmentzahl, Reihenfolge, Timings kommen aus
der Serie. Wiederverwendet karaoke.py (--wide) und musik.py.
"""
import json
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools"))
try:
    from kp_regeln import ist_fremdmaterial
except Exception:                       # Werkzeug fehlt -> lieber streng sein
    def ist_fremdmaterial(name):
        n = os.path.basename(str(name or "")).lower()
        return n.startswith("ref_") or "presse" in n

W, H = 1920, 1080
FPS = 30


def sh(cmd, **kw):
    """ffmpeg-Fehler sichtbar machen.

    Vorher lief jeder Aufruf mit -loglevel error und check=True: bei einem
    Abbruch bekam man den kompletten Befehl als Python-Traceback zu sehen,
    aber nicht die eine ffmpeg-Zeile, die sagt WARUM. Debuggen war damit
    Raten. Jetzt wird stderr eingefangen und im Fehlerfall ausgegeben.
    """
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode != 0:
        print("\n--- ffmpeg meldet ---", file=sys.stderr)
        for zeile in (r.stderr or "").strip().splitlines()[-12:]:
            print("   " + zeile, file=sys.stderr)
        raise subprocess.CalledProcessError(r.returncode, cmd, r.stdout, r.stderr)
    return r


def probe_dur(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
    return float(out)


def probe_dim(path):
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", path],
        capture_output=True, text=True).stdout.strip()
    w, h = out.split(",")[:2]
    return int(w), int(h)


def crop_box(src_w, src_h, z, cy, cx=0.5):
    cw = src_w / z
    ch = cw * H / W
    x = cx * src_w - cw / 2
    y = cy * src_h - ch / 2
    x = max(0, min(src_w - cw, x))
    y = max(0, min(src_h - ch, y))
    return int(cw), int(ch), int(x), int(y)


def shot_filter(i, s, src_w, src_h):
    """Ken-Burns-Einstellung wie lang.py: sanfter Zoom + Handkamera-Drift."""
    dur = s["end"] - s["start"]
    n = max(2, int(round(dur * FPS)))
    z0, z1 = s["z0"], s["z1"]
    cw, ch, cx, cy = crop_box(src_w, src_h, z0, s["cy"], s.get("cx", 0.5))
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


def find_words(serie, nn):
    for cand in (f"{serie}/words_{nn}.json", f"{serie}/animation/words_{nn}.json"):
        if os.path.exists(cand):
            return cand
    return None


EXT = (".jpg", ".jpeg", ".png", ".webp")


def _imgs_in(d):
    if not os.path.isdir(d):
        return []
    return sorted(os.path.join(d, f) for f in os.listdir(d)
                  if f.lower().endswith(EXT))


def find_images(serie, nn):
    """Hero + broll je Short — deckt die verschiedenen Serien-Layouts ab:
      prosperi: bilder/SNN/ + broll/short_NN/
      nuttyputty/lengede: bilder/short_NN/*.jpg
      ralston: bilder/broll/*sNN*  (Szenennummer im Dateinamen)
    Gibt möglichst VIELE verschiedene Kompositionen zurück (1 Bild pro Shot)."""
    n = int(nn)
    imgs = []
    imgs += _imgs_in(f"{serie}/bilder/S{nn}")
    imgs += _imgs_in(f"{serie}/bilder/short_{nn}")
    imgs += _imgs_in(f"{serie}/broll/short_{nn}")
    alt = f"{serie}/bilder/bild{nn}.jpg"
    if os.path.exists(alt):
        imgs.append(alt)
    # ralston-Stil: Dateiname trägt die Szene (hf_s03_*, ref_05_*)
    for base in (f"{serie}/bilder/broll", f"{serie}/bilder", f"{serie}/broll"):
        if os.path.isdir(base):
            for f in sorted(os.listdir(base)):
                low = f.lower()
                if low.endswith(EXT) and (f"s{n:02d}" in low or f"s{n}_" in low
                                          or f"_{n:02d}_" in low or f"_{n:02d}." in low):
                    imgs.append(os.path.join(base, f))
    # Dubletten raus: gleicher Dateistamm (hf_s01_truck.jpg == .webp) nur einmal,
    # .jpg bevorzugt vor .webp
    # Fremdmaterial raus, BEVOR dedupliziert wird. nb_lang.py zog hier
    # ref_01..ref_04 heran -- echte Pressefotos, die nur Vorlage fuer die
    # Bildgenerierung waren. Regel R24 deckte nur die Shorts ab.
    imgs = [p for p in imgs if not ist_fremdmaterial(p)]
    imgs.sort(key=lambda p: (os.path.splitext(p)[0], 0 if p.lower().endswith(".jpg") else 1))
    seen, out = set(), []
    for p in imgs:
        stem = os.path.splitext(os.path.realpath(p))[0]
        if stem not in seen:
            seen.add(stem)
            out.append(p)
    return out


# Crops MOTIV-zentriert: 9:16→16:9 zeigt nur ~31 % Bildhöhe, daher eng um die
# Bildmitte bleiben (dort sitzt bei den KI-Bildern das Motiv), sonst wird der
# Kopf/Körper abgeschnitten. Bewegung kommt aus Zoom + horizontalem Schwenk.
CY_CYCLE = [0.46, 0.52, 0.42, 0.56, 0.48, 0.50]
Z_CYCLE = [(1.05, 1.14), (1.12, 1.21), (1.08, 1.17), (1.15, 1.24), (1.06, 1.15)]


def bauen(serie, order, gap, shot_len):
    serie = serie.rstrip("/")
    tmp = f"{serie}/_lang"
    os.makedirs(tmp, exist_ok=True)
    os.makedirs(f"{serie}/render", exist_ok=True)
    out = f"{serie}/render/long.mp4"

    # 1) Segmente + Timings + Bilder je Short in Reihenfolge sammeln
    segs = []
    for num in order:
        nn = f"{num:02d}"
        vo = f"{serie}/voiceover/short_{nn}.mp3"
        if not os.path.exists(vo):
            print(f"  ! VO fehlt: {vo} — übersprungen")
            continue
        segs.append({"nn": nn, "vo": vo, "dur": probe_dur(vo),
                     "words": find_words(serie, nn),
                     "imgs": find_images(serie, nn)})
    if not segs:
        sys.exit(f"Keine VO-Segmente in {serie}/voiceover/ gefunden.")

    # 2) Stimme bauen: Segmente + Stille dazwischen, Offsets merken
    sil = f"{tmp}/sil.wav"
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi",
        "-i", f"anullsrc=r=48000:cl=mono", "-t", f"{gap}", sil])
    concat_list = f"{tmp}/voice_concat.txt"
    with open(concat_list, "w") as fh:
        for i, s in enumerate(segs):
            wav = f"{tmp}/seg_{s['nn']}.wav"
            sh(["ffmpeg", "-y", "-loglevel", "error", "-i", s["vo"],
                "-ar", "48000", "-ac", "1", wav])
            s["offset"] = sum(x["dur"] for x in segs[:i]) + gap * i
            fh.write(f"file '{os.path.abspath(wav)}'\n")
            if i < len(segs) - 1:
                fh.write(f"file '{os.path.abspath(sil)}'\n")
    voice = f"{tmp}/voice.wav"
    sh(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
        "-i", concat_list, "-c", "copy", voice])
    total = probe_dur(voice)
    print(f"  Stimme: {len(segs)} Segmente, {total:.1f}s gesamt")

    # 3) Wort-Timings mergen (mit Offset) -> durchlaufende Karaoke-Spur
    merged = []
    for s in segs:
        if not s["words"]:
            continue
        for w in json.load(open(s["words"], encoding="utf-8")):
            merged.append({"word": w["word"],
                           "start": round(w["start"] + s["offset"], 3),
                           "end": round(w["end"] + s["offset"], 3),
                           "conf": w.get("conf", 1.0)})
    words_path = f"{tmp}/words_merged.json"
    json.dump(merged, open(words_path, "w", encoding="utf-8"), ensure_ascii=False)
    ass = f"{tmp}/cap.ass"
    sh([sys.executable, "karaoke.py", words_path, ass, "0", f"{total:.2f}", "--wide"])

    # 4) Musikbett + Mix (Sidechain-Ducking wie lang.py)
    m = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", voice, "-af",
         "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    js = json.loads(m[m.rindex("{"):m.rindex("}") + 1])
    ln = ("loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={input_i}:"
          "measured_TP={input_tp}:measured_LRA={input_lra}:"
          "measured_thresh={input_thresh}:offset={target_offset}:"
          "linear=true").format(**js)
    stimme = f"{tmp}/stimme.m4a"
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", voice, "-af",
        f"{ln},volume=1.6dB,alimiter=limit=0.84:level=false:attack=2:release=60,"
        f"afade=t=in:st=0:d=0.08,afade=t=out:st={total-1.2:.2f}:d=1.2",
        "-ar", "48000", "-c:a", "aac", "-b:a", "192k", stimme])
    bett = f"{tmp}/bett.wav"
    sh([sys.executable, "musik.py", bett, f"{total:.2f}",
        "--tonart", "D", "--intensitaet", "0.85"])
    mix = f"{tmp}/mix.m4a"
    sh(["ffmpeg", "-y", "-loglevel", "error", "-i", stimme, "-i", bett,
        "-filter_complex",
        "[1:a]volume=-23dB,aformat=channel_layouts=stereo[m];"
        "[0:a]aformat=channel_layouts=stereo,asplit=2[v1][sc];"
        "[m][sc]sidechaincompress=threshold=0.03:ratio=8:attack=15:"
        "release=400:makeup=1[md];"
        "[v1][md]amix=inputs=2:normalize=0:duration=first[mx];"
        "[mx]alimiter=limit=0.84:level=false:attack=2:release=60[aout]",
        "-map", "[aout]", "-ar", "48000", "-c:a", "aac", "-b:a", "192k", mix])

    # Gesamt-Bildpool als Fallback für Segmente ohne eigenes Bild
    pool = []
    for s in segs:
        pool += s["imgs"]
    if not pool:
        sys.exit("Keine Bilder in der Serie gefunden.")

    # 5) Einstellungen: je Segment mehrere Ken-Burns-Shots aus seinen Bildern
    shots = []
    ci = 0
    for si, s in enumerate(segs):
        if not s["imgs"]:
            # Fallback: rotierender Ausschnitt aus dem Gesamtpool (nie leer lassen)
            s["imgs"] = [pool[(si + k) % len(pool)] for k in range(2)]
            print(f"  ~ Short {s['nn']}: keine eigenen Bilder → Fallback aus Pool")
        n_shots = max(1, int(math.ceil(s["dur"] / shot_len)))
        seg_start = s["offset"]
        sub = s["dur"] / n_shots
        src_w, src_h = probe_dim(s["imgs"][0])
        for k in range(n_shots):
            img = s["imgs"][k % len(s["imgs"])]
            z0, z1 = Z_CYCLE[ci % len(Z_CYCLE)]
            shots.append({
                "img": img,
                "start": seg_start + k * sub,
                "end": seg_start + (k + 1) * sub,
                "cy": CY_CYCLE[ci % len(CY_CYCLE)],
                "z0": z0, "z1": z1,
                # sanfter horizontaler Schwenk (abwechselnd L/R), minimaler
                # vertikaler Drift — Motiv bleibt im Bild
                "px": (0.16 if ci % 2 == 0 else -0.16),
                "py": (0.06 if ci % 3 == 0 else (-0.05 if ci % 3 == 1 else 0.0)),
                "drift": 9 + (ci % 4) * 2,
                "src_w": src_w, "src_h": src_h,
            })
            ci += 1

    inputs, filters, labels = [], [], []
    for i, s in enumerate(shots):
        # KEIN "-loop 1 -t <dauer>" hier. zoompan mit d=<frames> erzeugt aus
        # EINEM Eingangsbild bereits genau so viele Ausgabeframes. Mit -loop
        # liefert der Eingang unendlich viele Frames, und jeder davon wird
        # nochmals zu d Frames aufgeblasen: die erste Einstellung fuellt dann
        # das ganze Video, -shortest schneidet am Ton ab, und heraus kommt ein
        # Film aus einem einzigen Bild. Genau das passierte am 08.09. — 5:55
        # Ralston-Langvideo, 62 geplante Einstellungen, null Szenenwechsel.
        # lang.py (das Original) machte es richtig; der Fehler kam erst mit der
        # Verallgemeinerung zu nb_lang.py am 06.09. hinein und wurde nie geprueft.
        inputs += ["-i", s["img"]]
        filters.append(shot_filter(i, s, s["src_w"], s["src_h"]))
        labels.append(f"[v{i}]")
    chain = ";".join(filters)
    chain += f";{''.join(labels)}concat=n={len(shots)}:v=1:a=0[cat]"
    chain += f";[cat]subtitles={ass}:fontsdir=/usr/share/fonts[vout]"

    cmd = (["ffmpeg", "-y", "-loglevel", "error"] + inputs +
           ["-i", mix, "-filter_complex", chain,
            "-map", "[vout]", "-map", f"{len(shots)}:a",
            "-c:v", "libx264", "-preset", "medium", "-crf", "20",
            "-pix_fmt", "yuv420p", "-r", str(FPS),
            "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
            "-shortest", out])
    print(f"  {len(shots)} Einstellungen, Schnitt ~{total/len(shots):.1f}s, "
          f"Länge {total:.1f}s → rendere …")
    sh(cmd)
    print(f"fertig: {out}")
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit("Nutzung: python3 nb_lang.py <serie> [--order n,n,..] [--gap s] [--shot s]")
    serie = args[0]
    order = list(range(1, 11))
    gap, shot_len = 0.35, 6.0
    if "--order" in sys.argv:
        order = [int(x) for x in sys.argv[sys.argv.index("--order") + 1].split(",")]
    if "--gap" in sys.argv:
        gap = float(sys.argv[sys.argv.index("--gap") + 1])
    if "--shot" in sys.argv:
        shot_len = float(sys.argv[sys.argv.index("--shot") + 1])
    bauen(serie, order, gap, shot_len)


if __name__ == "__main__":
    main()
