#!/usr/bin/env python3
"""hoeren.py — damit Claude ein Video oder eine Tonspur HOEREN kann.

Das ist "Whisper" aus der Werkzeugliste, aber als faster-whisper. Grund:
das originale openai-whisper zieht PyTorch mit (~2,5 GB), faster-whisper
macht dasselbe ueber CTranslate2 in einem Bruchteil und laeuft auf der CPU
schneller. Gleiches Modell, gleiche Qualitaet.

VERHAELTNIS ZU VOSK: Vosk (transcribe_vosk.py) bleibt das Arbeitspferd der
Pipeline, weil es Wortzeiten fuer die Karaoke-Untertitel liefert und weil
die ganze Pipeline darauf aufgebaut ist. Whisper ist fuer das gedacht, was
Vosk nicht kann:
  - fremdsprachiges Material verstehen (Vosk-Modell ist rein deutsch)
  - Konkurrenzvideos abhoeren, um deren Aufbau zu lernen
  - schnell mal wissen, was in einer Datei gesagt wird

BENUTZUNG:
  python3 werkzeuge/hoeren.py tonspur.mp3
  python3 werkzeuge/hoeren.py video.mp4 --modell small
  python3 werkzeuge/hoeren.py video.mp4 --sprache en --srt
  python3 werkzeuge/hoeren.py https://www.youtube.com/watch?v=...   (laedt via yt-dlp)

Modelle: tiny, base, small (Standard), medium, large-v3.
Das Modell wird beim ersten Mal heruntergeladen und liegt dann im Cache.
"""
import argparse, sys, os, subprocess, tempfile, shutil

def hole_wenn_url(quelle):
    if not quelle.startswith(("http://", "https://")):
        return quelle, None
    if not shutil.which("yt-dlp"):
        sys.exit("yt-dlp fehlt — bitte werkzeuge/setup.sh laufen lassen.")
    tmp = tempfile.mkdtemp(prefix="hoeren_")
    ziel = os.path.join(tmp, "ton.m4a")
    print(f"Lade Ton von: {quelle}", file=sys.stderr)
    r = subprocess.run(["yt-dlp", "-q", "--no-warnings", "-f", "bestaudio",
                        "-o", ziel, quelle], capture_output=True, text=True)
    if r.returncode != 0 or not os.path.exists(ziel):
        shutil.rmtree(tmp, ignore_errors=True)
        sys.exit("Download fehlgeschlagen:\n" + r.stderr[:600])
    return ziel, tmp

def zeit(s):
    h, r = divmod(int(s), 3600)
    m, sek = divmod(r, 60)
    ms = int((s - int(s)) * 1000)
    return f"{h:02d}:{m:02d}:{sek:02d},{ms:03d}"

def main():
    p = argparse.ArgumentParser(description="Tonspur transkribieren (faster-whisper)")
    p.add_argument("quelle", help="Datei oder URL")
    p.add_argument("--modell", default="small")
    p.add_argument("--sprache", default=None, help="z.B. de, en. Leer = automatisch erkennen")
    p.add_argument("--srt", action="store_true", help="zusaetzlich .srt schreiben")
    p.add_argument("--ausgabe", default=None)
    a = p.parse_args()

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("faster-whisper fehlt — bitte werkzeuge/setup.sh laufen lassen.")

    pfad, tmp = hole_wenn_url(a.quelle)
    try:
        print(f"Modell {a.modell} wird geladen ...", file=sys.stderr)
        m = WhisperModel(a.modell, device="cpu", compute_type="int8")
        seg, info = m.transcribe(pfad, language=a.sprache, vad_filter=True)
        print(f"Sprache: {info.language} (Sicherheit {info.language_probability:.2f})",
              file=sys.stderr)
        print(f"Laenge:  {info.duration:.1f} s\n", file=sys.stderr)

        stuecke, text = [], []
        for s in seg:
            stuecke.append(s)
            text.append(s.text.strip())
            print(f"[{s.start:7.2f} - {s.end:7.2f}] {s.text.strip()}")

        basis = a.ausgabe or os.path.splitext(os.path.basename(
            a.quelle if tmp is None else "transkript"))[0]
        with open(basis + ".txt", "w", encoding="utf-8") as f:
            f.write(" ".join(text))
        print(f"\nGeschrieben: {basis}.txt", file=sys.stderr)

        if a.srt:
            with open(basis + ".srt", "w", encoding="utf-8") as f:
                for i, s in enumerate(stuecke, 1):
                    f.write(f"{i}\n{zeit(s.start)} --> {zeit(s.end)}\n{s.text.strip()}\n\n")
            print(f"Geschrieben: {basis}.srt", file=sys.stderr)
    finally:
        if tmp:
            shutil.rmtree(tmp, ignore_errors=True)

if __name__ == "__main__":
    main()
