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

# ── Bildbuehne fuer Hochformat (07.09.2026) ────────────────────────────────
# Manim leitet die Buehnenhoehe aus dem Seitenverhaeltnis ab. Bei -r 1080,1920
# ergab das eine Buehne von rund 25 Einheiten Hoehe -- alle Szenen hier sind
# aber fuer rund 16 Einheiten geschrieben (Titel bei y=8.2, Achsen bei x=+-5).
# Folge: jeder Inhalt sass winzig in der Bildmitte, umgeben von Leere. Das
# betraf JEDE bisher produzierte Animation, nicht nur einzelne.
# Hier wird die Buehne fest auf 9 x 16 Einheiten gesetzt -- exakt das Mass,
# fuer das die Szenen geschrieben sind.
if config.pixel_height > config.pixel_width:          # nur im Hochformat
    config.frame_height = 16.0
    config.frame_width = 9.0

class CrossSection(Scene):
    """Slot-Canyon-Querschnitt: Felsblock fällt auf eingeklemmten Arm.
    V8 Ralston S02 — cinematic, dark, beschriftet.
    Render 9:16: manim -qh -r 1080,1920 tools/manim_scenes.py CrossSection"""
    def construct(self):
        self.camera.background_color = "#0c0806"

        # ── Hintergrund-Gestein (voller Frame) ────────────────────────────
        bg = Rectangle(width=12, height=22,
                       fill_color="#1a1008", fill_opacity=1, stroke_width=0)
        self.add(bg)

        # ── Sandstein-Schichten (horizontale Streifen) ────────────────────
        layer_colors = ["#3d2410", "#2e1c0c", "#3a2212", "#261408", "#321e0e"]
        for i, col in enumerate(layer_colors):
            y = 6.0 - i * 2.8
            bar = Rectangle(width=12, height=2.6,
                            fill_color=col, fill_opacity=0.7, stroke_width=0)
            bar.move_to([0, y, 0])
            self.add(bar)

        # ── Linke und rechte Felswand (enger Spalt) ───────────────────────
        wall_l = Rectangle(width=4.0, height=22,
                           fill_color="#241510", fill_opacity=1, stroke_width=0)
        wall_l.move_to([-4.8, 0, 0])

        wall_r = Rectangle(width=4.0, height=22,
                           fill_color="#1e1208", fill_opacity=1, stroke_width=0)
        wall_r.move_to([4.8, 0, 0])

        # Rissstruktur an den Innenkanten
        crack_l = Line([-2.8, 10, 0], [-2.8, -10, 0],
                       color="#0a0502", stroke_width=6)
        crack_r = Line([2.8, 10, 0], [2.8, -10, 0],
                       color="#0a0502", stroke_width=6)

        self.add(wall_l, wall_r, crack_l, crack_r)

        # ── Felsbrocken (oben im Spalt) ───────────────────────────────────
        boulder_w, boulder_h = 5.2, 3.0
        boulder = Rectangle(width=boulder_w, height=boulder_h,
                            fill_color="#4a3020", fill_opacity=1,
                            stroke_color="#6a4830", stroke_width=3)
        boulder.move_to([0, 9.0, 0])

        boulder_lbl = Text("360 kg", font_size=62, color="#e8c080", weight=BOLD)
        boulder_lbl.move_to(boulder.get_center())

        self.add(boulder, boulder_lbl)

        # ── Arm-Silhouette (im Spalt, eingeklemmt) ────────────────────────
        arm = RoundedRectangle(corner_radius=0.35,
                               width=5.4, height=1.1,
                               fill_color="#c87050", fill_opacity=0.9,
                               stroke_color="#e89070", stroke_width=2)
        arm.move_to([0, -1.0, 0])

        arm_lbl = Text("Unterarm", font_size=46, color="#ffddcc")
        arm_lbl.next_to(arm, RIGHT, buff=0.2)

        self.add(arm, arm_lbl)

        # ── Druckpfeile links/rechts auf den Arm ─────────────────────────
        arr_l = Arrow(start=[-3.8, -1.0, 0], end=[-2.9, -1.0, 0],
                      color="#cc4422", stroke_width=8, buff=0)
        arr_r = Arrow(start=[3.8, -1.0, 0], end=[2.9, -1.0, 0],
                      color="#cc4422", stroke_width=8, buff=0)

        # ── Titel oben ────────────────────────────────────────────────────
        title = Text("BLUE JOHN CANYON", font_size=44, color="#c8a060",
                     weight=BOLD).move_to([0, -6.5, 0])
        sub   = Text("Utah, 26. April 2003", font_size=36,
                     color="#aa8850").move_to([0, -7.5, 0])

        # ── Animation ────────────────────────────────────────────────────
        # 1) Szene einblenden
        self.play(FadeIn(boulder, shift=DOWN * 0.3),
                  FadeIn(boulder_lbl),
                  run_time=0.7)
        self.play(FadeIn(arm), FadeIn(arm_lbl), run_time=0.5)

        # 2) Boulder stürzt ab
        self.play(
            boulder.animate.move_to([0, -0.4, 0]),
            boulder_lbl.animate.move_to([0, -0.4, 0]),
            run_time=1.4,
            rate_func=rate_functions.ease_in_cubic,
        )

        # 3) Impact-Flash + Druckpfeile
        self.play(
            Flash(arm.get_center(), color=YELLOW, line_length=0.5,
                  flash_radius=1.2, num_lines=10),
            FadeIn(arr_l), FadeIn(arr_r),
            run_time=0.5,
        )

        # 4) Arm rot färben (Schmerz)
        self.play(
            arm.animate.set_fill(color="#cc2200", opacity=1.0),
            run_time=0.6,
        )

        # 5) Beschriftung einblenden
        self.play(FadeIn(title), FadeIn(sub), run_time=0.8)
        self.wait(0.5)

class Timeline(Scene):
    """Zeitleiste (Stunden/Tage) mit Markern.

    Anpassen: TITLE, MARKS = [(x, "Label", "Ereignis")]. Ohne Ereignis-Text
    bleibt der Marker unbeschriftet -- aber ein Marker ohne Label ist laut
    Failure-Memory F-V8-D ein Fehler, also moeglichst immer beschriften.
    """
    TITLE = None
    MARKS = [(-4, "0 h", ""), (-1, "3 h", ""), (2, "19 h", ""), (4.5, "27 h", "")]
    BG_COLOR = "#0e0e12"
    DOT_COLOR = RED

    def construct(self):
        self.camera.background_color = self.BG_COLOR
        if self.TITLE:
            self.play(FadeIn(Text(self.TITLE, font_size=44, color="#c8a96e",
                                  weight=BOLD).move_to([0, 8.0, 0])), run_time=0.5)
        line = Line([-5, 0, 0], [5, 0, 0], color=GREY_B)
        self.play(Create(line), run_time=0.8)
        for eintrag in self.MARKS:
            x, lbl = eintrag[0], eintrag[1]
            evt = eintrag[2] if len(eintrag) > 2 else ""
            d = Dot([x, 0, 0], color=self.DOT_COLOR, radius=0.2)
            t = Text(lbl, font_size=34, color="#dddddd").next_to(d, DOWN, buff=0.25)
            grp = VGroup(d, t)
            if evt:
                grp.add(Text(evt, font_size=26, color=WHITE).next_to(d, UP, buff=0.25))
            self.play(FadeIn(grp), run_time=0.4)
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
        tracker = ValueTracker(self.START)
        num = always_redraw(
            lambda: Text(str(int(tracker.get_value())),
                         font_size=260, color=self.COLOR,
                         weight=BOLD).move_to([0, 2.0, 0])
        )
        unit = Text(self.UNIT, font_size=72, color=self.COLOR, weight=BOLD).move_to([0, -1.5, 0])
        lbl  = Text(self.LABEL, font_size=36, color="#aaaaaa").move_to([0, -3.0, 0])
        self.play(FadeIn(unit), FadeIn(lbl), run_time=0.5)
        self.add(num)
        self.play(tracker.animate.set_value(self.END), run_time=2.4,
                  rate_func=rate_functions.ease_in_out_cubic)
        self.play(num.animate.set_color(WHITE), run_time=0.3)
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
    TITLE        = None   # None = "Suchgebiet: X km Radius"

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

        title = Text(self.TITLE or f"Suchgebiet: {self.RADIUS_KM} km Radius",
                     font_size=38, color=WHITE, weight=BOLD).move_to([0, -6.5, 0])
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


class RockTrap(Scene):
    """V8 Ralston: Klemm-Situation — Querschnitt Felsblock in Schlucht mit Druckpfeilen.

    Zeigt wie ein Bolderstein zwischen zwei Kanyonwaenden eingeklemmt ist,
    und warum er sich nicht bewegen laesst (Hebelgesetz, Schwerkraft).
    Render: manim -qh -r 1080,1920 tools/manim_scenes.py RockTrap
    """
    BOULDER_W   = 2.8
    BOULDER_H   = 2.0
    WALL_COLOR  = "#c87040"
    ROCK_COLOR  = "#8a6040"
    ARROW_COLOR = "#ff4444"
    BG_COLOR    = "#0a0806"

    def construct(self):
        self.camera.background_color = self.BG_COLOR

        # Canyon-Waende links + rechts
        wall_l = Rectangle(width=2.5, height=14, fill_color=self.WALL_COLOR,
                           fill_opacity=1, stroke_width=0).move_to([-3.5, 0, 0])
        wall_r = Rectangle(width=2.5, height=14, fill_color=self.WALL_COLOR,
                           fill_opacity=1, stroke_width=0).move_to([3.5, 0, 0])
        # Textur-Linien
        for y in [-4, -2, 0, 2, 4]:
            l_line = Line([-4.7, y, 0], [-2.3, y + 0.3, 0],
                          color="#b06030", stroke_width=1, stroke_opacity=0.5)
            r_line = Line([2.3, y, 0], [4.7, y + 0.3, 0],
                          color="#b06030", stroke_width=1, stroke_opacity=0.5)
            self.add(l_line, r_line)

        self.play(FadeIn(wall_l), FadeIn(wall_r), run_time=0.6)

        # Schlucht-Boden
        boden = Rectangle(width=2.8, height=14, fill_color="#3a2010",
                          fill_opacity=0.8, stroke_width=0).move_to([0, -5, 0])
        self.play(FadeIn(boden), run_time=0.3)

        # Boulder faellt
        boulder = RoundedRectangle(corner_radius=0.3,
                                   width=self.BOULDER_W, height=self.BOULDER_H,
                                   fill_color=self.ROCK_COLOR, fill_opacity=1,
                                   stroke_color="#6a4020", stroke_width=3)
        boulder.move_to([0, 8, 0])  # start oben
        self.play(FadeIn(boulder), run_time=0.2)
        self.play(boulder.animate.move_to([0, 2.0, 0]),
                  run_time=1.0, rate_func=rate_functions.ease_in_bounce)

        # Klemm-Effekt: Boulder wird leicht breiter als Spalt → eingeklemmt
        self.play(boulder.animate.stretch_to_fit_width(2.85), run_time=0.3)

        # Menschliche Figur (stilisiert) darunter
        arm_dot = Dot([0, 0.5, 0], color="#ffcc88", radius=0.22).set_glow_factor(1.5)
        arm_lbl = Text("Arm", font_size=32, color="#ffcc88").next_to(arm_dot, DOWN, buff=0.2)
        self.play(FadeIn(arm_dot), FadeIn(arm_lbl), run_time=0.4)

        # Druckpfeile: Waende druecken gegen Boulder
        arrow_l = Arrow(start=[-1.8, 2.0, 0], end=[-1.1, 2.0, 0],
                        color=self.ARROW_COLOR, buff=0, stroke_width=6,
                        max_tip_length_to_length_ratio=0.3)
        arrow_r = Arrow(start=[1.8, 2.0, 0], end=[1.1, 2.0, 0],
                        color=self.ARROW_COLOR, buff=0, stroke_width=6,
                        max_tip_length_to_length_ratio=0.3)
        # Schwerkraft-Pfeil nach unten
        arrow_g = Arrow(start=[0, 3.5, 0], end=[0, 2.8, 0],
                        color="#ffaa44", buff=0, stroke_width=5,
                        max_tip_length_to_length_ratio=0.4)
        grav_lbl = Text("360 kg", font_size=28, color="#ffaa44").next_to(arrow_g, RIGHT, buff=0.1)

        self.play(GrowArrow(arrow_l), GrowArrow(arrow_r), run_time=0.6)
        self.play(GrowArrow(arrow_g), FadeIn(grav_lbl), run_time=0.5)

        # Klemm-Text
        klemm = Text("Eingeklemmt", font_size=52, color="#ff4444",
                     weight=BOLD).move_to([0, -3.5, 0])
        self.play(FadeIn(klemm), run_time=0.5)

        # Pulse-Effekt (einmal)
        self.play(boulder.animate.set_color("#aa5533"), run_time=0.3)
        self.play(boulder.animate.set_color(self.ROCK_COLOR), run_time=0.3)
        self.wait(0.5)


class CountdownTimer(Scene):
    """UNIVERSELL: Zeit zaehlt runter oder hoch — fuer Stunden/Minuten-Dramatik.

    V8 Ralston: 127 Stunden runterwaerts.
    Render: manim -qh -r 1080,1920 tools/manim_scenes.py CountdownTimer
    """
    START_H  = 127
    END_H    = 0
    UNIT     = "STUNDEN"
    LABEL    = "gefangen"
    COLOR    = "#cc3333"
    BG_COLOR = "#0d0a06"
    COUNT_UP = False   # True = hochzaehlen

    def construct(self):
        self.camera.background_color = self.BG_COLOR

        # Rahmen
        box = RoundedRectangle(corner_radius=0.4, width=7, height=4,
                               stroke_color=self.COLOR, stroke_width=4,
                               fill_color="#1a0505", fill_opacity=0.8).move_to([0, 2.5, 0])
        self.play(FadeIn(box), run_time=0.3)

        start_val = self.START_H if not self.COUNT_UP else self.END_H
        target    = self.END_H   if not self.COUNT_UP else self.START_H
        tracker   = ValueTracker(start_val)
        num = always_redraw(
            lambda: Text(str(int(tracker.get_value())),
                         font_size=240, color=self.COLOR,
                         weight=BOLD).move_to([0, 2.5, 0])
        )
        unit = Text(self.UNIT, font_size=60, color=self.COLOR,
                    weight=BOLD).move_to([0, -0.5, 0])
        lbl  = Text(self.LABEL, font_size=40, color="#888888").move_to([0, -2.5, 0])

        self.play(FadeIn(unit), FadeIn(lbl), run_time=0.5)
        self.add(num)
        self.play(tracker.animate.set_value(target),
                  run_time=2.5, rate_func=rate_functions.ease_in_out_sine)

        if target == 0:
            for _ in range(2):
                self.play(box.animate.set_stroke(color=WHITE), run_time=0.15)
                self.play(box.animate.set_stroke(color=self.COLOR), run_time=0.15)

        self.wait(0.8)


# ═══════════════════════════════════════════════════════════════════════════
# V8 Ralston — reihen-spezifische Auspraegungen (07.09.2026)
#
# Angelegt, weil kp_gate.py aufdeckte: 5 der 10 Ralston-Shorts (01, 03, 06,
# 07, 10) waren reine Ken-Burns-Standbilder — die Bewegtbild-Pflicht vom
# 31.08. war bei ihnen nie umgesetzt. Die Bewegung ist hier nicht Dekoration:
# jede Szene zeigt genau die Groesse, die der gesprochene Text nennt.
# ═══════════════════════════════════════════════════════════════════════════

# ── Gemeinsame Grundlage der V8-Szenen ─────────────────────────────────────
# Buehne im Hochformat: x von -4.5 bis 4.5, y von -8 bis 8.
# Das untere Drittel (y < -3.0) bleibt FREI — dort liegen die Karaoke-Captions.
# Alles Erklaerende gehoert nach oben.

SAND_HELL = "#c8925a"
SAND      = "#8a5326"
SAND_TIEF = "#3d2410"
FELS_BG   = "#0d0a06"
LICHT     = "#e0b060"


def _felswand(links, oben_x, unten_x, hoehe=16.0, farbe=SAND_TIEF, opak=1.0):
    """Eine Schluchtwand als Flaeche — enger werdend nach unten.

    Kein Ornament: die Enge IST die Geschichte. Ein Punkt vor schwarzem
    Hintergrund erzaehlt sie nicht (Failure-Memory F-V8-D).
    """
    rand = -4.6 if links else 4.6
    pts = [[rand, hoehe / 2, 0], [oben_x, hoehe / 2, 0],
           [unten_x, -hoehe / 2, 0], [rand, -hoehe / 2, 0]]
    return Polygon(*pts, fill_color=farbe, fill_opacity=opak,
                   stroke_color=SAND, stroke_width=2, stroke_opacity=0.5)


class RalstonNiemandWeiss(Scene):
    """S01 — 'Kein Wort, keine Notiz. Niemand wusste, wo er war.'

    Die Ringe wachsen, aber der Zaehler bleibt auf null. Das ist die Aussage
    des Shorts: es gab kein Suchgebiet, weil niemand suchte.
    """

    def construct(self):
        self.camera.background_color = FELS_BG

        boden = Rectangle(width=9.2, height=9, fill_color="#1a1208",
                          fill_opacity=1, stroke_width=0).move_to([0, 1.5, 0])
        self.add(boden)

        datum = Text("26. APRIL 2003", font_size=40, color=SAND_HELL,
                     weight=BOLD).move_to([0, 7.0, 0])
        self.play(FadeIn(datum), run_time=0.4)

        # Auto am Rand, Schlucht in der Mitte — die Strecke dazwischen
        auto = VGroup(
            RoundedRectangle(width=0.9, height=0.42, corner_radius=0.08,
                             fill_color="#aa9977", fill_opacity=1, stroke_width=0),
            Text("Auto", font_size=26, color="#aa9977"),
        )
        auto[1].next_to(auto[0], UP, buff=0.15)
        auto.move_to([-2.9, 4.4, 0])

        schlucht = Dot([0.6, 1.6, 0], color=LICHT, radius=0.22)
        schlucht_t = Text("Blue John Canyon", font_size=30, color=LICHT,
                          weight=BOLD).next_to(schlucht, UP, buff=0.3)

        weg = DashedLine(auto[0].get_center(), schlucht.get_center(),
                         color="#6b4a28", stroke_width=3, dash_length=0.16)

        self.play(FadeIn(auto), run_time=0.4)
        self.play(Create(weg), run_time=0.6)
        self.play(FadeIn(schlucht), FadeIn(schlucht_t), run_time=0.4)

        # Ringe: Beschriftung UNTER dem Ring, nicht rechts daneben —
        # nebeneinander ueberlagerten sich die km-Angaben.
        for r, km, deck in [(1.1, 10, 0.7), (1.9, 20, 0.5), (2.7, 30, 0.35)]:
            ring = Circle(radius=r, color=SAND, stroke_width=4,
                          stroke_opacity=deck).move_to(schlucht.get_center())
            t = Text(f"{km} km", font_size=26, color=SAND_HELL).move_to(
                schlucht.get_center() + DOWN * (r - 0.02))
            self.play(Create(ring), FadeIn(t), run_time=0.55)

        # Der Zaehler, der auf null bleibt
        null = Text("0", font_size=140, color="#cc4433",
                    weight=BOLD).move_to([0, -3.0, 0])
        unter = Text("Menschen wussten davon", font_size=32,
                     color="#cc4433").next_to(null, DOWN, buff=0.25)
        self.play(FadeIn(null, scale=1.3), run_time=0.5)
        self.play(FadeIn(unter), run_time=0.4)
        self.wait(0.9)


class RalstonTiefe(Scene):
    """S03 — '30 Meter unter der Erdoberfläche. Nächste Straße 30 Kilometer.'

    Die Schlucht wird nach unten enger, waehrend die Figur faellt. Rechts
    laeuft eine Tiefenskala mit. Am Ende steht, was er dabeihatte.
    """

    def construct(self):
        self.camera.background_color = "#050403"

        self.add(_felswand(True, -2.4, -0.75), _felswand(False, 2.4, 0.75))
        himmel = Rectangle(width=4.6, height=1.2, fill_color="#5a7a9a",
                           fill_opacity=0.35, stroke_width=0).move_to([0, 7.4, 0])
        self.add(himmel)

        titel = VGroup(
            Text("30 METER", font_size=56, color=SAND_HELL, weight=BOLD),
            Text("unter der Oberfläche", font_size=25, color="#9a7a55"),
        ).arrange(DOWN, buff=0.18).move_to([0, 6.6, 0])
        self.play(FadeIn(titel), run_time=0.4)

        skala = Line([3.6, 6.0, 0], [3.6, -2.2, 0], color=SAND,
                     stroke_width=3, stroke_opacity=0.6)
        self.play(Create(skala), run_time=0.5)

        fig = VGroup(
            Circle(radius=0.13, fill_color=LICHT, fill_opacity=1, stroke_width=0),
            Line([0, -0.13, 0], [0, -0.55, 0], color=LICHT, stroke_width=5),
        ).move_to([0, 6.0, 0])
        self.play(FadeIn(fig), run_time=0.3)

        for meter, y in [(0, 6.0), (10, 3.4), (20, 0.8), (30, -1.8)]:
            strich = Line([3.35, y, 0], [3.85, y, 0], color=SAND_HELL, stroke_width=4)
            lbl = Text(f"{meter} m", font_size=28,
                       color=SAND_HELL if meter == 30 else "#9a7a55",
                       weight=BOLD if meter == 30 else NORMAL)
            lbl.next_to(strich, LEFT, buff=0.2)
            self.play(FadeIn(strich), FadeIn(lbl),
                      fig.animate.move_to([0, y, 0]),
                      run_time=0.55, rate_func=rate_functions.ease_in_out_sine)

        habe = VGroup(
            Text("2 Burritos", font_size=28, color="#bbaa99"),
            Text("300 ml Wasser", font_size=28, color="#bbaa99"),
            Text("1 Taschenmesser", font_size=28, color="#cc4433", weight=BOLD),
        ).arrange(DOWN, buff=0.28).move_to([-1.4, -0.6, 0])
        self.play(LaggedStart(*[FadeIn(z, shift=RIGHT * 0.25) for z in habe],
                              lag_ratio=0.3), run_time=1.0)
        self.wait(0.8)


class RalstonAbschied(Scene):
    """S06 — der Abschiedsfilm. Eine senkrechte 127-Stunden-Leiste.

    Senkrecht, weil das Bild senkrecht ist: eine liegende Zeitleiste
    verschenkt im Hochformat die Haelfte der Flaeche.
    """

    MARKEN = [
        (0,   "0 h",   "eingeklemmt",   "#cc4433"),
        (24,  "24 h",  "",              SAND),
        (72,  "72 h",  "Wasser leer",   SAND_HELL),
        (96,  "96 h",  "Abschiedsfilm", LICHT),
        (127, "127 h", "",              SAND),
    ]

    def construct(self):
        self.camera.background_color = FELS_BG
        self.add(_felswand(True, -3.2, -2.6, farbe="#150e07"),
                 _felswand(False, 3.2, 2.6, farbe="#150e07"))

        titel = Text("127 STUNDEN", font_size=44, color=SAND_HELL,
                     weight=BOLD).move_to([0, 7.0, 0])
        self.play(FadeIn(titel), run_time=0.4)

        oben, unten = 5.6, -2.4
        achse = Line([-1.9, oben, 0], [-1.9, unten, 0], color=SAND,
                     stroke_width=4, stroke_opacity=0.7)
        self.play(Create(achse), run_time=0.7)

        for stunde, lbl, ereignis, farbe in self.MARKEN:
            y = oben - (stunde / 127.0) * (oben - unten)
            gross = bool(ereignis)
            punkt = Dot([-1.9, y, 0], color=farbe, radius=0.2 if gross else 0.13)
            stunden_t = Text(lbl, font_size=28, color=farbe).next_to(
                punkt, LEFT, buff=0.25)
            grp = VGroup(punkt, stunden_t)
            if ereignis:
                grp.add(Text(ereignis, font_size=30, color=farbe,
                             weight=BOLD).next_to(punkt, RIGHT, buff=0.3))
            self.play(FadeIn(grp), run_time=0.45)

        # Kamera auf dem Fels — das Bild des Shorts
        kamera = VGroup(
            RoundedRectangle(width=1.15, height=0.7, corner_radius=0.1,
                             fill_color="#2a2a2e", fill_opacity=1,
                             stroke_color="#666", stroke_width=2),
            Circle(radius=0.2, fill_color="#111", fill_opacity=1,
                   stroke_color=LICHT, stroke_width=3),
            Dot(radius=0.07, color="#cc4433"),
        )
        kamera[1].move_to(kamera[0].get_center() + LEFT * 0.15)
        kamera[2].move_to(kamera[0].get_corner(UR) + LEFT * 0.18 + DOWN * 0.16)
        kamera.move_to([1.2, 3.0, 0])
        self.play(FadeIn(kamera, shift=UP * 0.3), run_time=0.5)
        for _ in range(2):                       # Aufnahme laeuft
            self.play(kamera[2].animate.set_opacity(0.15), run_time=0.28)
            self.play(kamera[2].animate.set_opacity(1.0), run_time=0.28)
        self.wait(0.6)


class RalstonFuenfteNacht(Scene):
    """S07 — 'In der fünften Nacht ließ Ralston los.'

    Fuenf Naechte als fuenf Balken. Vier fuellen sich dunkel, der fuenfte
    hell — dort kippt die Geschichte.
    """

    NAECHTE = [("Nacht 1", "eingeklemmt"), ("Nacht 2", ""),
               ("Nacht 3", "Wasser knapp"), ("Nacht 4", "Abschiedsfilm"),
               ("Nacht 5", "die Vision")]

    def construct(self):
        self.camera.background_color = "#06070c"

        titel = Text("5 NÄCHTE IM CANYON", font_size=40, color="#8a9ab0",
                     weight=BOLD).move_to([0, 7.0, 0])
        self.play(FadeIn(titel), run_time=0.4)

        oben, unten = 5.2, -1.6
        breite, luecke = 1.25, 0.35
        gesamt = len(self.NAECHTE) * breite + 4 * luecke
        x0 = -gesamt / 2 + breite / 2

        for i, (name, ereignis) in enumerate(self.NAECHTE):
            x = x0 + i * (breite + luecke)
            letzte = i == len(self.NAECHTE) - 1
            farbe = LICHT if letzte else "#26303f"

            rahmen = Rectangle(width=breite, height=oben - unten,
                               stroke_color="#3a4658", stroke_width=2,
                               fill_opacity=0).move_to([x, (oben + unten) / 2, 0])
            self.add(rahmen)

            fuellung = Rectangle(width=breite, height=0.01, fill_color=farbe,
                                 fill_opacity=0.9 if letzte else 0.55,
                                 stroke_width=0).move_to([x, unten, 0])
            self.add(fuellung)
            ziel = Rectangle(width=breite, height=oben - unten,
                             fill_color=farbe,
                             fill_opacity=0.9 if letzte else 0.55,
                             stroke_width=0).move_to([x, (oben + unten) / 2, 0])
            self.play(Transform(fuellung, ziel), run_time=0.5,
                      rate_func=rate_functions.ease_out_sine)

            lbl = Text(name, font_size=25, color="#8a9ab0" if not letzte else LICHT,
                       weight=BOLD if letzte else NORMAL)
            lbl.next_to(rahmen, DOWN, buff=0.22)
            self.play(FadeIn(lbl), run_time=0.2)
            if ereignis:
                ev = Text(ereignis, font_size=22,
                          color="#c8d2e0" if not letzte else LICHT)
                ev.rotate(PI / 2).move_to(rahmen.get_center())
                self.play(FadeIn(ev), run_time=0.25)

        schluss = Text("Er sah seinen Sohn.", font_size=46, color=WHITE,
                       weight=BOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(schluss), run_time=0.5)
        self.wait(0.8)


class StundenBogen(Scene):
    """NEU (V8, 07.09.2026) — S10: die 127 Stunden schliessen sich, und
    danach geht es weiter. 'Nicht das Ende. Der Anfang.'

    Ein Bogen fuellt sich auf 127 Stunden, blitzt auf und oeffnet sich dann
    nach vorn in eine Linie mit drei beschrifteten Marken. Bewusst nuechtern:
    keine Effekte ohne Aussage, jede Form traegt eine Beschriftung
    (Failure-Memory F-V8-D: keine anonymen Punkte).

    Render: manim -qh -r 1080,1920 tools/manim_scenes.py StundenBogen
    """
    STUNDEN = 127
    DANACH = [("Buch", "#b8763a"), ("Film", "#c8925a"), ("Sohn Leo", "#e0b060")]
    BG_COLOR = "#0d0a06"

    def construct(self):
        self.camera.background_color = self.BG_COLOR

        titel = Text("127 STUNDEN", font_size=52, color="#c8a96e",
                     weight=BOLD).move_to([0, 7.6, 0])
        self.play(FadeIn(titel), run_time=0.4)

        # ── Der Bogen fuellt sich ──────────────────────────────────────────
        spur = Circle(radius=3.3, color="#332214", stroke_width=20)
        spur.move_to([0, 3.0, 0])
        self.add(spur)

        bogen = Arc(radius=3.3, start_angle=PI / 2, angle=-0.001,
                    color="#e0b060", stroke_width=20).move_arc_center_to([0, 3.0, 0])
        # Zaehler bewusst als Text, nicht als Integer/DecimalNumber: die
        # rendern ueber LaTeX, und LaTeX ist im Container nicht installiert.
        # Ein Werkzeug, das nur auf einer Maschine laeuft, ist kein Werkzeug.
        fortschritt = ValueTracker(0.0)
        zaehler = always_redraw(lambda: Text(
            f"{int(fortschritt.get_value() * self.STUNDEN)}",
            font_size=100, color=WHITE, weight=BOLD).move_to([0, 3.2, 0]))
        einheit = Text("Stunden", font_size=34,
                       color="#998877").move_to([0, 1.7, 0])
        bogen.add_updater(lambda m: m.become(
            Arc(radius=3.3, start_angle=PI / 2,
                angle=-max(TAU * fortschritt.get_value(), 0.001),
                color="#e0b060", stroke_width=20
                ).move_arc_center_to([0, 3.0, 0])))
        self.add(bogen, zaehler, einheit)

        self.play(fortschritt.animate.set_value(1.0), run_time=2.4,
                  rate_func=rate_functions.ease_in_out_sine)
        bogen.clear_updaters()
        zaehler.clear_updaters()

        # ── Der Moment, in dem es kippt ────────────────────────────────────
        blitz = Circle(radius=3.3, color=WHITE, stroke_width=24)
        blitz.move_to([0, 3.0, 0])
        self.play(FadeIn(blitz, scale=1.15), run_time=0.2)
        self.play(FadeOut(blitz), run_time=0.25)

        # ── ... und danach geht es weiter ──────────────────────────────────
        linie = Line([-4.2, -2.2, 0], [4.2, -2.2, 0],
                     color="#554433", stroke_width=4)
        self.play(Create(linie), run_time=0.6)

        for i, (text, farbe) in enumerate(self.DANACH):
            x = -2.6 + i * 2.6
            marke = Dot([x, -2.2, 0], color=farbe, radius=0.2)
            beschriftung = Text(text, font_size=32, color=farbe,
                                weight=BOLD).next_to(marke, DOWN, buff=0.35)
            self.play(FadeIn(marke), FadeIn(beschriftung), run_time=0.45)

        schluss = Text("Nicht das Ende.", font_size=44, color=WHITE,
                       weight=BOLD).move_to([0, -6.4, 0])
        self.play(FadeIn(schluss), run_time=0.5)
        self.wait(0.8)


# ═══════════════════════════════════════════════════════════════════════════
# V8 Ralston, zweite Haelfte (07.09.2026)
#
# Angelegt, weil die Animations-QC zeigte: Short 04 und 05 liefen mit den
# VORGABEWERTEN der universellen Klassen — im Bild stand "0 TAGE allein in der
# Sahara" und "10 Tage — Mauro Prosperi". Das ist Mauro Prosperis Geschichte
# in einem Video ueber Aron Ralston in einer Schlucht in Utah. Die Klassen
# waren richtig gebaut und nie auf die Reihe angepasst worden.
#
# Lehre: eine universelle Klasse ohne reihen-spezifische Auspraegung ist eine
# Falle. Deshalb traegt ab jetzt jede Reihe ihre eigenen Unterklassen.
# ═══════════════════════════════════════════════════════════════════════════

class RalstonMeissel(StatCounter):
    """S04 — 'Nach 15 Stunden war der Fels kaum angekratzt.'"""
    START = 0
    END   = 15
    UNIT  = "STUNDEN"
    LABEL = "gemeißelt — kein Millimeter"
    COLOR = "#e0b060"


class RalstonInschrift(Scene):
    """S05 — 'Er ritzte vier Dinge in den Fels: seinen Namen, sein
    Geburtsdatum und sein Todesdatum.'

    Das staerkste Bild der ganzen Reihe. Nuechtern umgesetzt: die Zeilen
    erscheinen, als wuerden sie eingeritzt, ohne Effekt und ohne Musikgeste.
    Das Todesdatum kommt zuletzt und bleibt stehen.
    """

    ZEILEN = [("ARON RALSTON", 54), ("27. OKT 1975", 40), ("APRIL 2003", 40)]

    def construct(self):
        self.camera.background_color = "#0a0705"

        # Felswand als Flaeche mit Schichtung — kein leerer Hintergrund
        wand = Rectangle(width=9.2, height=16.4, fill_color="#2e1c0c",
                         fill_opacity=1, stroke_width=0)
        self.add(wand)
        for i in range(9):
            y = 7.0 - i * 1.7
            self.add(Line([-4.6, y, 0], [4.6, y + 0.22, 0], color="#3d2410",
                          stroke_width=3, stroke_opacity=0.55))

        kopf = Text("TAG 3", font_size=34, color="#8a6a45",
                    weight=BOLD).move_to([0, 6.6, 0])
        self.play(FadeIn(kopf), run_time=0.4)

        unter = Text("unter null Grad · Wasser leer", font_size=26,
                     color="#7a6047").move_to([0, 5.7, 0])
        self.play(FadeIn(unter), run_time=0.4)

        y = 3.0
        for text, groesse in self.ZEILEN:
            zeile = Text(text, font_size=groesse, color="#d8c4a0",
                         weight=BOLD).move_to([0, y, 0])
            # Ritzen: die Zeile wird von links nach rechts freigelegt
            self.play(Write(zeile), run_time=0.85)
            self.add(Line(zeile.get_corner(DL) + DOWN * 0.18,
                          zeile.get_corner(DR) + DOWN * 0.18,
                          color="#6b4a28", stroke_width=2, stroke_opacity=0.7))
            y -= 1.9

        schluss = Text("Er hielt es für sein Grab.", font_size=34, color="#c8a96e",
                       weight=BOLD).move_to([0, -3.0, 0])
        self.play(FadeIn(schluss), run_time=0.6)
        self.wait(0.9)


class Ralston65Minuten(Scene):
    """S08 — 'Er griff zum Messer. 65 Minuten, bis der Arm ab war.'

    Ersetzt RockTrap fuer diesen Short. RockTrap zeigte einen gelben Punkt
    namens "Arm" zwischen zwei Balken und nutzte 14 % der Bildbreite — beides
    ist genau das, was Failure-Memory F-V8-D verbietet.

    Hier laeuft ein Balken ueber 65 Minuten mit drei benannten Marken. Nichts
    Blutiges: die Zahlen tragen die Szene.
    """

    MARKEN = [(0, "Knochen 1"), (12, "Knochen 2"), (65, "frei")]

    def construct(self):
        self.camera.background_color = "#0a0705"

        titel = Text("65 MINUTEN", font_size=58, color="#cc4433",
                     weight=BOLD).move_to([0, 6.4, 0])
        unter = Text("mit einem stumpfen Taschenmesser", font_size=26,
                     color="#8a6a55").move_to([0, 5.4, 0])
        self.play(FadeIn(titel), FadeIn(unter), run_time=0.5)

        links, rechts, y = -3.6, 3.6, 1.6
        spur = Rectangle(width=rechts - links, height=0.85, fill_color="#241610",
                         fill_opacity=1, stroke_color="#4a2c1c",
                         stroke_width=2).move_to([0, y, 0])
        self.add(spur)

        fortschritt = ValueTracker(0.0)

        def balken():
            b = max(fortschritt.get_value() * (rechts - links), 0.02)
            r = Rectangle(width=b, height=0.85, fill_color="#cc4433",
                          fill_opacity=0.9, stroke_width=0)
            r.move_to([links + b / 2, y, 0])
            return r

        self.add(always_redraw(balken))

        minute = always_redraw(lambda: Text(
            f"{int(fortschritt.get_value() * 65)} min", font_size=40,
            color=WHITE, weight=BOLD).move_to([0, 3.1, 0]))
        self.add(minute)

        vorher = 0.0
        for i, (m, name) in enumerate(self.MARKEN):
            ziel = m / 65.0
            self.play(fortschritt.animate.set_value(ziel),
                      run_time=max(0.5, (ziel - vorher) * 3.2),
                      rate_func=rate_functions.linear)
            vorher = ziel
            x = links + ziel * (rechts - links)
            marke = Line([x, y - 0.62, 0], [x, y + 0.62, 0],
                         color="#e0b060", stroke_width=4)
            lbl = Text(name, font_size=28, color="#e0b060", weight=BOLD)
            # Marken bei 0 und 12 min liegen dicht beieinander -> abwechselnd
            # ueber und unter den Balken setzen, sonst ueberlagern sich die
            # Beschriftungen (die Animations-QC hat genau das gemessen).
            lbl.next_to(marke, DOWN if i % 2 == 0 else UP, buff=0.3)
            # ... und in den Bildrand klemmen, sonst laeuft "Knochen 1" links
            # aus dem Bild. Die Buehne ist 9 Einheiten breit: x von -4.5 bis 4.5.
            halb = lbl.width / 2 + 0.15
            lbl.move_to([min(max(x, -4.5 + halb), 4.5 - halb),
                         lbl.get_center()[1], 0])
            self.play(FadeIn(marke), FadeIn(lbl), run_time=0.4)

        schluss = Text("Dann fiel er rückwärts. Frei.", font_size=36, color=WHITE,
                       weight=BOLD).move_to([0, -2.6, 0])
        self.play(FadeIn(schluss), run_time=0.6)
        self.wait(0.8)
