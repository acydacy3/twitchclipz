"""transcribe_local.py — GRATIS-Transkription für video-use via faster-whisper.

Katastrophenprotokoll-Adapter: ersetzt den kostenpflichtigen ElevenLabs-Scribe-
Aufruf durch unser lokales faster-whisper (dasselbe Modell wie hoeren.py:
`small`, CPU, int8). Schreibt exakt das Scribe-JSON-Schema, das die video-use-
Helfer (pack_transcripts.py, render.py) erwarten:

    {"language_code": "de",
     "text": "...",
     "words": [
        {"type": "word",    "text": "Er",  "start": 2.52, "end": 2.71, "speaker_id": "S0"},
        {"type": "spacing", "text": " ",   "start": 2.71, "end": 2.78, "speaker_id": "S0"},
        ...
     ]}

Unsere Shorts sind Ein-Sprecher-Voiceover → keine Diarisierung nötig
(speaker_id fest "S0"). Word-Level-Timestamps kommen aus whisper
(word_timestamps=True). Zwischen zwei Wörtern wird ein `spacing`-Eintrag
eingefügt, damit die Stille-Lücken-Logik (Schnittkandidaten) funktioniert.

Cache: existiert die Ziel-JSON schon, wird sie zurückgegeben (nicht neu berechnet)
— identisch zur Scribe-Variante (Hard Rule 9: nie neu transkribieren).

Nutzung (Drop-in für transcribe.py):
    python helpers/transcribe_local.py <video> [--edit-dir DIR] [--language de]
                                       [--modell small] [--audio-track 0]
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def transcript_path(edit_dir: Path, video: Path, audio_track: int = 0) -> Path:
    """Gleiche Namenskonvention wie transcribe.py, damit der Cache geteilt wird."""
    suffix = "" if audio_track == 0 else f".track{audio_track}"
    return edit_dir / "transcripts" / f"{video.stem}{suffix}.json"


def extract_audio(video_path: Path, dest: Path, audio_track: int = 0) -> None:
    cmd = [
        "ffmpeg", "-y", "-i", str(video_path),
        "-map", f"0:a:{audio_track}",
        "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le",
        str(dest),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def to_scribe_words(segments) -> tuple[list[dict], str]:
    """faster-whisper-Segmente → Scribe-`words`-Liste (word + spacing).

    Fällt ein Segment ohne Word-Timestamps an (selten), wird es als ein
    einzelnes Wort mit den Segmentgrenzen übernommen — nie stumm verschluckt.
    """
    words: list[dict] = []
    text_parts: list[str] = []
    prev_end: float | None = None

    for seg in segments:
        seg_words = getattr(seg, "words", None)
        if not seg_words:
            raw = (seg.text or "").strip()
            if not raw:
                continue
            start = float(seg.start)
            end = float(seg.end)
            if prev_end is not None and start > prev_end:
                words.append({"type": "spacing", "text": " ",
                              "start": round(prev_end, 3), "end": round(start, 3),
                              "speaker_id": "S0"})
            words.append({"type": "word", "text": raw,
                          "start": round(start, 3), "end": round(end, 3),
                          "speaker_id": "S0"})
            text_parts.append(raw)
            prev_end = end
            continue

        for w in seg_words:
            raw = (w.word or "").strip()
            if not raw:
                continue
            start = float(w.start)
            end = float(w.end)
            # Stille-Lücke zwischen Wörtern als spacing-Eintrag (Schnittkandidat).
            if prev_end is not None and start > prev_end:
                words.append({"type": "spacing", "text": " ",
                              "start": round(prev_end, 3), "end": round(start, 3),
                              "speaker_id": "S0"})
            words.append({"type": "word", "text": raw,
                          "start": round(start, 3), "end": round(end, 3),
                          "speaker_id": "S0"})
            text_parts.append(raw)
            prev_end = end

    return words, " ".join(text_parts)


def transcribe_one(video: Path, edit_dir: Path, language: str | None,
                   modell: str, audio_track: int, verbose: bool = True) -> Path:
    transcripts_dir = edit_dir / "transcripts"
    transcripts_dir.mkdir(parents=True, exist_ok=True)
    out_path = transcript_path(edit_dir, video, audio_track)

    if out_path.exists():
        if verbose:
            print(f"cached: {out_path.name}")
        return out_path

    from faster_whisper import WhisperModel

    t0 = time.time()
    with tempfile.TemporaryDirectory() as tmp:
        audio = Path(tmp) / f"{video.stem}.wav"
        if verbose:
            print(f"  extrahiere Audio aus {video.name}", flush=True)
        extract_audio(video, audio, audio_track)

        if verbose:
            print(f"  faster-whisper ({modell}, cpu/int8) …", flush=True)
        model = WhisperModel(modell, device="cpu", compute_type="int8")
        segments, info = model.transcribe(
            str(audio), language=language, word_timestamps=True, vad_filter=True,
        )
        segments = list(segments)  # Generator → Liste (einmal auswerten)

    words, full_text = to_scribe_words(segments)
    payload = {
        "language_code": getattr(info, "language", language or "de"),
        "language_probability": round(float(getattr(info, "language_probability", 0.0)), 3),
        "text": full_text,
        "words": words,
        "_engine": "faster-whisper (local, gratis)",
    }
    out_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False))

    if verbose:
        n_words = sum(1 for w in words if w["type"] == "word")
        print(f"  gespeichert: {out_path.name} ({n_words} Wörter) in {time.time()-t0:.1f}s")
    return out_path


def main() -> None:
    ap = argparse.ArgumentParser(description="Gratis-Transkription für video-use (faster-whisper)")
    ap.add_argument("video", type=Path)
    ap.add_argument("--edit-dir", type=Path, default=None,
                    help="Ausgabe-Ordner (Standard: <video_parent>/edit)")
    ap.add_argument("--language", type=str, default="de",
                    help="ISO-Code (Standard 'de'). Leer/None = auto.")
    ap.add_argument("--modell", type=str, default="small",
                    help="whisper-Modell: tiny|base|small|medium|large-v3 (Standard small)")
    ap.add_argument("--audio-track", type=int, default=0)
    args = ap.parse_args()

    video = args.video.resolve()
    if not video.exists():
        sys.exit(f"Video nicht gefunden: {video}")

    edit_dir = (args.edit_dir or (video.parent / "edit")).resolve()
    lang = args.language or None
    transcribe_one(video, edit_dir, lang, args.modell, args.audio_track)


if __name__ == "__main__":
    main()
