#!/usr/bin/env python3
"""Rendert querschnitt.html deterministisch zu Frames (9:16) -> ffmpeg -> mp4."""
import pathlib, sys
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
HTML = (HERE / "querschnitt.html").resolve().as_uri()
FRAMES = HERE / "frames"
FRAMES.mkdir(exist_ok=True)
CHROME = "/opt/pw-browsers/chromium-1194/chrome-linux/chrome"
FPS = 25
DUR_MS = 9000
N = int(FPS * DUR_MS / 1000)

with sync_playwright() as p:
    b = p.chromium.launch(executable_path=CHROME, args=["--no-sandbox", "--force-color-profile=srgb"])
    pg = b.new_page(viewport={"width": 1080, "height": 1920}, device_scale_factor=1)
    pg.add_init_script("window.__CAPTURE=true;" + ("window.__CLEAN=true;" if __import__("os").environ.get("CLEAN") else ""))
    pg.goto(HTML)
    pg.wait_for_function("typeof window.__seek === 'function'")
    for i in range(N):
        ms = i * 1000 / FPS
        pg.evaluate("(ms)=>window.__seek(ms)", ms)
        pg.screenshot(path=str(FRAMES / f"f{i:04d}.png"))
    b.close()
print(f"{N} Frames gerendert nach {FRAMES}")
