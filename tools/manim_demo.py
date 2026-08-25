"""Demo-Short (Manim): Nutty Putty in 3 Beats — Querschnitt + Zeitleiste. 9:16.
Render: manim -qm -r 1080,1920 --fps 30 tools/manim_demo.py Demo"""
from manim import *

class Demo(Scene):
    def construct(self):
        self.camera.background_color = "#140d08"
        # --- Beat 1: Titel/Hook ---
        t1 = Text("NUTTY PUTTY", weight=BOLD, font_size=96, color="#ffd400")
        t2 = Text("27 Stunden kopfüber", font_size=52, color=WHITE).next_to(t1, DOWN, buff=0.4)
        self.play(FadeIn(t1, shift=UP*0.3), run_time=0.7)
        self.play(Write(t2), run_time=0.7)
        self.wait(0.6)
        self.play(FadeOut(t1), FadeOut(t2), run_time=0.4)

        # --- Beat 2: Querschnitt, Figur gleitet in den Spalt ---
        rock = Rectangle(width=10.8, height=19.2, fill_color="#2a1a11", fill_opacity=1, stroke_width=0)
        self.add(rock)
        crack = Polygon(
            [-5.4,2.2,0],[0.6,2.4,0],[0.85,1.2,0],[0.7,-3.5,0],[1.0,-7.5,0],
            [0.3,-7.5,0],[0.15,-3.5,0],[0.25,1.2,0],[-5.4,1.4,0],
            color="#050302", fill_color="#050302", fill_opacity=1, stroke_width=0)
        self.add(crack)
        glow = Circle(radius=0.45, color=YELLOW, fill_opacity=0.25, stroke_width=0)
        fig = Dot(color=YELLOW, radius=0.16)
        grp = VGroup(glow, fig).move_to([-4.8,1.8,0])
        self.add(grp)
        self.play(grp.animate.move_to([0.5,1.7,0]), run_time=1.6, rate_func=rate_functions.ease_in_out_sine)
        self.play(grp.animate.move_to([0.6,-6.8,0]), run_time=1.3, rate_func=rate_functions.ease_in_quad)
        lbl = Text("18 × 10 cm", font_size=46, color=WHITE, weight=BOLD).move_to([-2.4,-6.8,0])
        self.play(FadeIn(lbl), Flash(fig, color=YELLOW, line_length=0.3), run_time=0.6)
        self.wait(0.5)
        self.play(FadeOut(VGroup(rock,crack,grp,lbl)), run_time=0.4)

        # --- Beat 3: Zeitleiste ---
        line = Line([-4.5,0,0],[4.5,0,0], color=GREY_B, stroke_width=6)
        self.play(Create(line), run_time=0.7)
        for x,lbl in [(-4.5,"0 h"),(-1.5,"3 h"),(2.0,"19 h"),(4.5,"27 h")]:
            d = Dot([x,0,0], color=RED, radius=0.12)
            tx = Text(lbl, font_size=40, color=WHITE).next_to(d, UP, buff=0.25)
            self.play(GrowFromCenter(d), FadeIn(tx), run_time=0.35)
        end = Text("Das Wunder blieb aus.", font_size=54, color="#ffd400", weight=BOLD).move_to([0,-2.5,0])
        self.play(Write(end), run_time=0.8)
        self.wait(0.8)
