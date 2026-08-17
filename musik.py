"""
Musikbett fuer Katastrophenprotokoll erzeugen - synthetisch, lizenzfrei.

    python3 musik.py bett.wav 33.0 [--intensitaet 1.0] [--tonart D]

Warum selbst erzeugt statt Bibliothek: bei Shorts teilt YouTube die
Einnahmen mit jedem verwendeten Musikstueck. Ein Track halbiert den
Anteil, zwei dritteln ihn. Eigenes Material faellt nicht darunter - und
es gibt keine Content-ID-Sperre in einzelnen Laendern.

Aufbau (von unten nach oben):
  1. Subdrone    Grundton + Oktave, sehr langsam schwebend
  2. Pad         Quinte und kleine Terz, gegenlaeufig atmend
  3. Puls        weicher Herzschlag alle zwei Sekunden
  4. Schimmer    hohe Obertoene, kaum hoerbar, gibt "Weite"
  5. Rauschbett  tiefpassgefiltertes Rauschen als Kleber
"""
import sys
import wave
import numpy as np

SR = 48000

# Halbtonabstaende einer natuerlichen Molltonleiter ueber dem Grundton
GRUND = {"C": 32.70, "D": 36.71, "E": 41.20, "F": 43.65,
         "G": 49.00, "A": 55.00, "H": 61.74}


def halbton(f, n):
    return f * 2 ** (n / 12.0)


def lfo(t, hz, tief=0.0, hoch=1.0, phase=0.0):
    """Langsame Schwingung zwischen tief und hoch."""
    s = 0.5 + 0.5 * np.sin(2 * np.pi * hz * t + phase)
    return tief + (hoch - tief) * s


def ton(t, f, amp, detune=0.0):
    """Sinus mit leichter Verstimmung - zwei Stimmen schweben gegeneinander."""
    a = np.sin(2 * np.pi * f * t)
    if detune:
        a = 0.5 * a + 0.5 * np.sin(2 * np.pi * f * (1 + detune) * t)
    return amp * a


def tiefpass(x, fc):
    """Einpoliger Tiefpass - reicht fuer ein Rauschbett vollkommen."""
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a) * x[i] + a * acc
        y[i] = acc
    return y


def bett(dauer, tonart="D", intens=1.0, seed=7):
    rng = np.random.default_rng(seed)
    n = int(dauer * SR)
    t = np.arange(n) / SR

    f0 = GRUND[tonart]              # Grundton, Oktave 1
    quinte = halbton(f0, 7)
    terz = halbton(f0, 3)           # kleine Terz -> Moll, ernster Grundton
    septime = halbton(f0, 10)

    out = np.zeros(n)

    # 1. Subdrone: traegt alles, darf nie auffallen
    out += ton(t, f0, 0.30 * lfo(t, 0.031, 0.75, 1.0), detune=0.0007)
    out += ton(t, f0 * 2, 0.16 * lfo(t, 0.019, 0.6, 1.0), detune=0.0011)

    # 2. Pad: Quinte und Terz atmen gegenlaeufig, damit nichts steht
    out += ton(t, quinte * 2, 0.085 * lfo(t, 0.024, 0.25, 1.0), detune=0.0016)
    out += ton(t, terz * 4, 0.045 * lfo(t, 0.017, 0.0, 1.0, phase=np.pi),
               detune=0.0022)
    out += ton(t, septime * 4, 0.026 * lfo(t, 0.013, 0.0, 1.0, phase=2.1),
               detune=0.0019)

    # 3. Puls: weicher Herzschlag. Kein Beat - eine Erinnerung daran,
    #    dass Zeit vergeht. Alle 2 s, mit exponentiellem Abfall.
    periode = 2.0
    ph = (t % periode) / periode
    huell = np.exp(-ph * 14.0)
    # zweiter, leiserer Schlag kurz danach (Herzschlag statt Metronom)
    ph2 = ((t - 0.28) % periode) / periode
    huell += 0.45 * np.exp(-ph2 * 16.0) * (t > 0.28)
    puls = np.sin(2 * np.pi * f0 * 1.5 * t) * huell
    out += 0.19 * intens * puls

    # 4. Schimmer: hohe Toene, einzeln kaum hoerbar, zusammen "Raum"
    for k, (mult, hz, amp) in enumerate([(8, 0.011, 0.020),
                                         (12, 0.008, 0.013),
                                         (16, 0.006, 0.008)]):
        out += ton(t, f0 * mult, amp * lfo(t, hz, 0.0, 1.0, phase=k * 1.7),
                   detune=0.003)

    # 5. Rauschbett: klebt die Sinusse zusammen, nimmt das Synthetische raus
    rausch = tiefpass(rng.normal(0, 1, n), 240.0)
    rausch /= (np.abs(rausch).max() + 1e-9)
    out += 0.055 * rausch * lfo(t, 0.009, 0.5, 1.0)

    # Aufbau ueber die ersten 12 %: der Anfang gehoert der Stimme
    ramp = np.clip(t / max(dauer * 0.12, 0.6), 0, 1) ** 1.5
    out *= 0.35 + 0.65 * ramp

    # Ein- und Ausblende
    ein = int(0.8 * SR)
    aus = int(1.6 * SR)
    out[:ein] *= np.linspace(0, 1, ein) ** 2
    out[-aus:] *= np.linspace(1, 0, aus) ** 1.5

    out *= intens
    spitze = np.abs(out).max()
    if spitze > 0:
        out *= 0.72 / spitze
    return out


def schreiben(pfad, mono):
    stereo = np.empty((len(mono), 2))
    # winzige Laufzeitdifferenz erzeugt Breite, ohne Mono-Ausloeschung
    ver = 220
    stereo[:, 0] = mono
    stereo[:, 1] = np.concatenate([mono[ver:], np.zeros(ver)])
    dat = (np.clip(stereo, -1, 1) * 32767).astype(np.int16)
    with wave.open(pfad, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(dat.tobytes())


if __name__ == "__main__":
    pfad = sys.argv[1]
    dauer = float(sys.argv[2])
    intens = 1.0
    tonart = "D"
    if "--intensitaet" in sys.argv:
        intens = float(sys.argv[sys.argv.index("--intensitaet") + 1])
    if "--tonart" in sys.argv:
        tonart = sys.argv[sys.argv.index("--tonart") + 1]
    schreiben(pfad, bett(dauer, tonart, intens))
    print(f"{pfad}: {dauer:.1f}s, Tonart {tonart}-Moll, Intensitaet {intens}")
