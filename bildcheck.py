"""
Bildpruefung vor der Pipeline.

Prueft objektiv genau die Punkte, die bei Bild 1 (Mine) nur per Auge
auffielen: zu flaches Licht, keine Nahdetails, Baender zu aehnlich.

    python3 bildcheck.py bild01.png [bild02.png ...]
"""
import sys
import numpy as np
from PIL import Image

MIN_W_9x16 = 2000          # 4K-9:16 ist ~2304 breit
TARGET_RATIO = 9 / 16


def analyse(path):
    im = Image.open(path).convert("RGB")
    w, h = im.size
    a = np.asarray(im).astype(np.float32) / 255.0
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]

    print(f"\n{'='*62}\n{path}\n{'='*62}")

    # --- 1. Aufloesung -------------------------------------------------
    ratio = w / h
    ok_res = w >= MIN_W_9x16
    ok_ratio = abs(ratio - TARGET_RATIO) < 0.02
    crop_w, crop_h = w, int(w * 9 / 16)
    print(f"Aufloesung   {w}x{h}  (Seitenverhaeltnis {ratio:.3f})")
    print(f"  9:16?      {'OK' if ok_ratio else 'ABWEICHUNG (erwartet 0.563)'}")
    print(f"  4K genug?  {'OK' if ok_res else f'ZU KLEIN (<{MIN_W_9x16}px breit)'}")
    print(f"  16:9-Ausschnitt fuers Langvideo: {crop_w}x{crop_h}"
          f"  {'-> ueber 1080p, scharf' if crop_h >= 1080 else '-> muss hochgerechnet werden, wird weich'}")

    # --- 2. Kontrast / Lichtfuehrung ------------------------------------
    p1, p50, p99 = np.percentile(lum, [1, 50, 99])
    deep_shadow = float((lum < 0.12).mean())
    highlight = float((lum > 0.85).mean())
    spread = p99 - p1
    print(f"\nKontrast     Spanne {spread:.2f}  Median {p50:.2f}")
    print(f"  tiefe Schatten (<0.12): {deep_shadow*100:5.1f} %  "
          f"{'OK' if deep_shadow >= 0.06 else 'ZU WENIG -> Bild wirkt flach/dunstig'}")
    print(f"  Lichter       (>0.85): {highlight*100:5.1f} %  "
          f"{'OK' if highlight >= 0.01 else 'wenig Spitzlichter'}")

    # --- 3. Baender: oben / Mitte / unten unterscheidbar? ----------------
    bands = [lum[0:h//3], lum[h//3:2*h//3], lum[2*h//3:h]]
    names = ["oben  ", "mitte ", "unten "]
    means = [float(b.mean()) for b in bands]
    # Detaildichte per Gradient = Proxy fuer "gibt es hier was zu sehen"
    dets = []
    for b in bands:
        gy, gx = np.gradient(b)
        dets.append(float(np.sqrt(gx**2 + gy**2).mean()))
    print("\nBaender (Basis fuers Mehrfach-Ausschneiden)")
    for n, m, d in zip(names, means, dets):
        print(f"  {n} Helligkeit {m:.2f}   Detaildichte {d:.4f}")
    spread_band = max(means) - min(means)
    print(f"  Helligkeits-Unterschied: {spread_band:.2f}  "
          f"{'OK' if spread_band >= 0.10 else 'ZU AEHNLICH -> Ausschnitte wirken gleich'}")
    weakest = names[int(np.argmin(dets))].strip()
    if min(dets) < 0.020:
        print(f"  schwaechstes Band: {weakest} (kaum Detail -> tote Einstellung)")

    # --- 4. Nahdetail vorhanden? ----------------------------------------
    # hohe lokale Varianz irgendwo = es gibt etwas zum Nah-Ranfahren
    small = np.asarray(im.convert("L").resize((w//8, h//8))).astype(np.float32)/255.
    gy, gx = np.gradient(small)
    mag = np.sqrt(gx**2 + gy**2)
    k = 8
    tiles = [mag[y:y+k, x:x+k].mean()
             for y in range(0, mag.shape[0]-k, k)
             for x in range(0, mag.shape[1]-k, k)]
    top_tile = float(np.percentile(tiles, 97)) if tiles else 0.0
    print(f"\nNahdetail    staerkste Region {top_tile:.4f}  "
          f"{'OK' if top_tile >= 0.055 else 'SCHWACH -> keine echte Nahaufnahme moeglich'}")


for p in sys.argv[1:]:
    try:
        analyse(p)
    except Exception as e:
        print(f"{p}: FEHLER {e}")
