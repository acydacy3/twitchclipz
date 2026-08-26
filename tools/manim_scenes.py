#!/usr/bin/env python3
"""Manim-Szenen-Vorlagen fuer Katastrophen-Erklaervideos (Querschnitt, Zeitleiste, Karte).
Render 9:16: manim -qh -r 1080,1920 tools/manim_scenes.py CrossSection
(braucht manim aus setup-tools.sh). Ergebnis in media/videos/... -> in short.py als {"clip":...}."""
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
