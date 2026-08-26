#!/usr/bin/env python3
"""Manim-Szenen-Vorlagen fuer Katastrophen-Erklaervideos.

Render 9:16: manim -qh -r 1080,1920 tools/manim_scenes.py <ClassName>
Ergebnis in media/videos/manim_scenes/<ClassName>/...mp4 -> in short.py als {"clip":...}.

ANIMATION-BIBLIOTHEK (wachst mit jedem Video):
  CrossSection   — Querschnitt Felsspalte + Figur (Nutty Putty-Stil)
  Timeline       — Rettungs-Zeitleiste mit Stunden-Markern
  ProsperiMap    — Route-Karte Marokko→Algerien (V7)
  StatCounter    — Grosse animierte Zahl (Tage, km, Meter, Grad) — UNIVERSELL
  SurvivalDays   — Kalender-/Tages-Strip mit Ereignis-Markern — UNIVERSELL
  SearchRadius   — Expanding Suchkreis auf Karte — UNIVERSELL
  DepthDive      — Kamera taucht in Tiefe (Gruben, Hoehlen, Wasser) — UNIVERSELL

STRATEGIE: Jede neue Videoreihe fuegt >=1 neue Klasse hinzu.
           Mehrere Animations-Clips pro Reihe anstreben (nicht nur 1).
           Langfristig: weg von Standbild+VO, hin zu echter Animation."""
try:
    from manim import *
except Exception:
    import sys; print("manim nicht installiert (setup-tools.sh)"); sys.exit(0)

class CrossSection(Scene):
    """Beispiel: Fels-Querschnitt mit engem Spalt + leuchtender Figur, die hinabgleitet."""
    def construct(self):
        self.camera.background_color = "#170f0a"
        rock = Rectangle(width=10, height=18, fill_color="#2a1a11", fill_opacity=1, stroke_width=0)
        self.add(rock)
        crack = VMobject(stroke_width=0, fill_color="#050302", fill_opacity=1)
        crack.set_points_as_corners([[-5,4,0],[1,4,0],[1.2,3,0],[1.0,-2,0],[1.3,-6,0],[0.7,-6,0],[0.5,-2,0],[0.6,3,0],[-5,3.2,0]])
        self.add(crack)
        fig = Dot(color=YELLOW).scale(1.6).set_glow_factor(2)
        fig.move_to([-4.5,3.5,0])
        self.play(fig.animate.move_to([0.9,3.4,0]), run_time=2.2, rate_func=rate_functions.ease_in_out_sine)
        self.play(fig.animate.move_to([1.0,-5.5,0]), run_time=1.6, rate_func=rate_functions.ease_in_quad)
        self.wait(0.6)

class Timeline(Scene):
    """Beispiel: Rettungs-Zeitleiste (Stunden/Tage) mit Markern."""
    def construct(self):
        self.camera.background_color = "#0e0e12"
        line = Line([-5,0,0],[5,0,0], color=GREY_B)
        self.play(Create(line), run_time=0.8)
        for x,lbl in [(-4,"0 h"),(-1,"3 h"),(2,"19 h"),(4.5,"27 h")]:
            d=Dot([x,0,0],color=RED); t=Text(lbl,font_size=34).next_to(d,UP)
            self.play(FadeIn(d),FadeIn(t),run_time=0.4)
        self.wait(0.5)


class ProsperiMap(Scene):
    """V7 Prosperi: Route-Karte Marokko → Algerien (291 km Irrweg, 9 Tage).
    Render 9:16: manim -qh -r 1080,1920 tools/manim_scenes.py ProsperiMap"""
    def construct(self):
        self.camera.background_color = "#0d0a06"
        # Hintergrund: Sandton-Gradient simuliert (großes Rechteck)
        sand = Rectangle(width=12, height=22, fill_color="#1a1206", fill_opacity=1, stroke_width=0)
        self.add(sand)

        # Titel oben
        titel = Text("MARATHON DES SABLES 1994", font_size=38, color="#c8a96e",
                     weight=BOLD).move_to([0, 8.2, 0])
        self.play(FadeIn(titel), run_time=0.5)

        # Koordinaten-Schema (schematisch, keine echte Mercator):
        # Marokko (Start) oben, Algerien (Fund) unten — vereinfacht
        # Start-Punkt: Foum Zguid / Marokko
        start_pos = [0, 5.0, 0]
        end_pos   = [1.2, -4.5, 0]  # Algerien, leicht östlich

        # Grenzlinie Marokko/Algerien (gestrichelt, horizontal)
        border = DashedLine([-4, 0.5, 0], [4, 0.5, 0], color="#666655", dash_length=0.18, stroke_width=2)
        lbl_mar = Text("MAROKKO", font_size=32, color="#888870").move_to([-2.8, 2.5, 0])
        lbl_alg = Text("ALGERIEN", font_size=32, color="#888870").move_to([-2.8, -2.5, 0])
        self.play(Create(border), FadeIn(lbl_mar), FadeIn(lbl_alg), run_time=0.8)

        # Renn-Route (geplant, gestrichelt)
        geplant = DashedLine(start_pos, [0, 1.5, 0], color="#4466aa",
                             dash_length=0.22, stroke_width=3)
        lbl_geplant = Text("geplante Route", font_size=26, color="#4466aa").move_to([2.8, 3.2, 0])
        self.play(Create(geplant), FadeIn(lbl_geplant), run_time=0.7)

        # Start-Marker
        start_dot = Dot(start_pos, color="#e8d080", radius=0.18)
        start_lbl = Text("Foum Zguid\nStart 10. April", font_size=26, color="#e8d080").next_to(start_dot, RIGHT, buff=0.2)
        self.play(FadeIn(start_dot), FadeIn(start_lbl), run_time=0.5)

        # Sandsturm-Icon (Warnsymbol)
        sturm_pos = [0.4, 1.8, 0]
        sturm = Text("⚠", font_size=54, color="#cc8833").move_to(sturm_pos)
        sturm_lbl = Text("Sandsturm\n13. April", font_size=26, color="#cc8833").next_to(sturm, RIGHT, buff=0.1)
        self.play(FadeIn(sturm), FadeIn(sturm_lbl), run_time=0.5)

        # Irrweg-Linie (rot, kurvend nach Süden)
        # Pfadpunkte: zieht sich nach Süden und leicht Ost
        irr_punkte = [
            sturm_pos,
            [0.6, 0.8, 0],
            [0.3, 0.0, 0],   # Grenze überschreiten
            [0.8, -1.5, 0],
            [1.1, -3.0, 0],
            end_pos,
        ]
        irr = VMobject(stroke_color="#cc3333", stroke_width=5, stroke_opacity=0.9)
        irr.set_points_smoothly([np.array(p) for p in irr_punkte])
        dist_lbl = Text("291 km", font_size=36, color="#cc3333", weight=BOLD).move_to([-2.0, -1.2, 0])
        self.play(Create(irr), run_time=1.8, rate_func=rate_functions.ease_in_out_sine)
        self.play(FadeIn(dist_lbl), run_time=0.4)

        # Fund-Marker
        end_dot = Dot(end_pos, color="#55cc55", radius=0.22)
        end_lbl = Text("Algerien\nGefunden 21. April", font_size=26, color="#55cc55").next_to(end_dot, RIGHT, buff=0.2)
        self.play(FadeIn(end_dot), FadeIn(end_lbl), run_time=0.6)

        # 9-Tage-Zeitleiste unten
        tl_y = -7.2
        tl_line = Line([-4.0, tl_y, 0], [4.0, tl_y, 0], color=GREY_B, stroke_width=2)
        self.play(Create(tl_line), run_time=0.5)
        events = [
            (-4.0, "13."),
            (-2.7, "14."),
            (-1.4, "15."),
            (-0.1, "16."),
            (1.2, "17."),
            (2.5, "18."),
            (3.8, "21.\nApril"),
        ]
        for x, lbl in events:
            d = Dot([x, tl_y, 0], color="#cc6633", radius=0.09)
            t = Text(lbl, font_size=22, color="#aaaaaa").next_to(d, DOWN, buff=0.1)
            self.play(FadeIn(d), FadeIn(t), run_time=0.2)

        tl_titel = Text("10 Tage allein", font_size=30, color="#cc6633", weight=BOLD).move_to([0, tl_y - 1.1, 0])
        self.play(FadeIn(tl_titel), run_time=0.4)
        self.wait(1.0)


class StatCounter(Scene):
    """UNIVERSELL: Grosse animierte Zahl zaehlt hoch + Einheit darunter.

    Anpassen: START, END, UNIT, LABEL, COLOR.
    Beispiele: 9 Tage / 291 km / 47 Verschuettete / 33 Tage / 600m Tiefe.
    Render: manim -qh -r 1080,1920 tools/manim_scenes.py StatCounter
    """
    # --- anpassen je Video ---
    START = 0
    END   = 9
    UNIT  = "TAGE"
    LABEL = "allein in der Sahara"
    COLOR = "#e85c33"
    # --------------------------

    def construct(self):
        self.camera.background_color = "#0d0a06"
        num = Integer(self.START, color=self.COLOR).scale(5.5).move_to([0, 2.0, 0])
        unit = Text(self.UNIT, font_size=72, color=self.COLOR, weight=BOLD).next_to(num, DOWN, buff=0.3)
        lbl  = Text(self.LABEL, font_size=36, color="#aaaaaa").next_to(unit, DOWN, buff=0.5)
        self.play(FadeIn(unit), FadeIn(lbl), run_time=0.5)
        self.play(
            ChangeDecimalToValue(num, self.END),
            run_time=2.4,
            rate_func=rate_functions.ease_in_out_cubic,
        )
        self.play(num.animate.set_color(WHITE).scale(1.08), run_time=0.3)
        self.wait(0.8)


class SurvivalDays(Scene):
    """UNIVERSELL: Tag-fuer-Tag-Strip mit Ereignis-Markern.

    DAYS: Liste von (Tag-Nr, Kuerzel, Farbe, Ereignis-Text).
    Render: manim -qh -r 1080,1920 tools/manim_scenes.py SurvivalDays
    """
    TITLE = "10 Tage — Mauro Prosperi"
    DAYS = [
        (1,  "13.4", "#4488cc", "Sandsturm"),
        (2,  "14.4", "#cc4433", "verirrt"),
        (3,  "15.4", "#cc4433", ""),
        (4,  "16.4", "#cc4433", "Marabout"),
        (5,  "17.4", "#cc4433", "Fledermäuse"),
        (6,  "18.4", "#cc4433", "Flugzeug"),
        (7,  "19.4", "#cc4433", ""),
        (8,  "20.4", "#cc4433", "Nomaden"),
        (9,  "21.4", "#55cc55", "gerettet"),
    ]

    def construct(self):
        self.camera.background_color = "#0d0a06"
        title = Text(self.TITLE, font_size=44, color="#c8a96e", weight=BOLD).move_to([0, 8.0, 0])
        self.play(FadeIn(title), run_time=0.5)

        n = len(self.DAYS)
        xs = [i * (8.0 / max(n - 1, 1)) - 4.0 for i in range(n)]
        line = Line([xs[0], 0, 0], [xs[-1], 0, 0], color=GREY_B, stroke_width=2)
        self.play(Create(line), run_time=0.6)

        for i, (day, date, col, evt) in enumerate(self.DAYS):
            x = xs[i]
            d = Dot([x, 0, 0], color=col, radius=0.22)
            date_t = Text(date, font_size=26, color="#aaaaaa").next_to(d, DOWN, buff=0.2)
            day_t  = Text(f"Tag {day}", font_size=22, color=col).next_to(d, UP, buff=0.2)
            grp = VGroup(d, date_t, day_t)
            if evt:
                evt_t = Text(evt, font_size=24, color=WHITE).next_to(day_t, UP, buff=0.15)
                grp.add(evt_t)
            self.play(FadeIn(grp), run_time=0.25)

        self.wait(1.0)


class SearchRadius(Scene):
    """UNIVERSELL: Suchkreis waechst auf Karte — fuer Such+Rettungs-Szenen.

    Anpassen: CENTER_LABEL, RADIUS_KM, COLOR.
    Render: manim -qh -r 1080,1920 tools/manim_scenes.py SearchRadius
    """
    CENTER_LABEL = "letzter bekannter Standort"
    RADIUS_KM    = 200
    RING_COLOR   = "#cc3333"
    BG_COLOR     = "#0d1a0d"

    def construct(self):
        self.camera.background_color = self.BG_COLOR
        center = Dot([0, 1, 0], color=YELLOW, radius=0.18).set_glow_factor(2)
        lbl    = Text(self.CENTER_LABEL, font_size=32, color=YELLOW).next_to(center, UP, buff=0.3)
        self.play(FadeIn(center), FadeIn(lbl), run_time=0.5)

        for r, alpha in [(1.2, 0.5), (2.4, 0.35), (3.6, 0.2)]:
            ring = Circle(radius=r, color=self.RING_COLOR, stroke_opacity=alpha, stroke_width=3)
            ring.move_to(center.get_center())
            km_val = int(self.RADIUS_KM * r / 3.6)
            km_t   = Text(f"{km_val} km", font_size=26, color=self.RING_COLOR).next_to(ring, RIGHT, buff=0.1)
            self.play(Create(ring), FadeIn(km_t), run_time=0.7)

        title = Text(f"Suchgebiet: {self.RADIUS_KM} km Radius", font_size=38,
                     color=WHITE, weight=BOLD).move_to([0, -6.5, 0])
        self.play(FadeIn(title), run_time=0.5)
        self.wait(1.0)


class DepthDive(Scene):
    """UNIVERSELL: Kamera-Tauchgang in Tiefe — Gruben, Hoehlen, Wasser.

    Anpassen: LAYERS (Tiefe, Label, Farbe).
    Render: manim -qh -r 1080,1920 tools/manim_scenes.py DepthDive
    """
    TITLE = "600 Meter unter der Erde"
    LAYERS = [
        (0,   "Oberfläche",    "#3a5a3a"),
        (2.2, "100 m",         "#2a3a2a"),
        (4.4, "300 m",         "#1a2a1a"),
        (6.8, "600 m — Mine",  "#0a1a0a"),
    ]
    DOT_COLOR = "#ffee88"

    def construct(self):
        self.camera.background_color = "#050805"
        title = Text(self.TITLE, font_size=44, color="#aaaaaa", weight=BOLD).move_to([0, 8.2, 0])
        self.play(FadeIn(title), run_time=0.4)

        fig = Dot([0, 7.2, 0], color=self.DOT_COLOR, radius=0.22).set_glow_factor(2)
        self.play(FadeIn(fig), run_time=0.3)

        for depth_y, lbl_text, col in self.LAYERS:
            y = 7.2 - depth_y * 2.0
            layer = Rectangle(width=12, height=0.06,
                              fill_color=col, fill_opacity=0.7, stroke_width=0).move_to([0, y, 0])
            lbl   = Text(lbl_text, font_size=28, color="#888888").move_to([-3.5, y + 0.4, 0])
            self.play(FadeIn(layer), FadeIn(lbl), run_time=0.4)
            self.play(fig.animate.move_to([0, y - 0.3, 0]),
                      run_time=0.8, rate_func=rate_functions.ease_in_out_sine)

        flash = fig.copy().set_color(WHITE).scale(2)
        self.play(Transform(fig, flash), run_time=0.4)
        self.wait(0.8)
