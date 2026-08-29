
---
## V7 Broll-Learnings (26.08.2026) — Confidence: High

**Problem:** Gleiche 3 Sahara-Bilder in 7 von 10 Shorts (Category:Sahara gibt immer dieselben Top-Treffer zurück).
**Fix:** Globaler `used_globally`-Set in nb_fetch_broll — kein Bild darf in 2 Shorts vorkommen. Pro Short eigene spezifische Kategorien (Erg Chebbi, Dust storms, Ténéré, Tuareg people statt einfach "Sahara").
**Chiroptera-Falle:** Die Commons-Kategorie gibt wissenschaftliche Paper-Figuren zurück, keine Fotos. Fix: `Category:Bats in flight`, `Category:Cave-dwelling bats` mit JPEG-Mime-Filter.
**Category:Happiness = Sports-Fotos.** Immer topisch-spezifische Kategorien, nie generische Emotions-Kategorien.

**Regel:** short.py erwartet Bilder in 1600×2848. Higgsfield-Downloads immer mit `convert -resize 1600x2848^ -gravity center -extent 1600x2848` konvertieren.

**Regel:** musik.py `--tonart` erwartet Großbuchstaben ohne "m" (D, nicht Dm). Moll ist immer implizit (bett() ist immer Moll-Atmosphäre).

**Schlüsselszenen-Regel (26.08.):** Higgsfield KI-Generierung nur für echte Schlüsselmomente (max. 4–5 pro Video). Broll = Hauptquelle (kostenlos). KI = gezielter Akzent.
