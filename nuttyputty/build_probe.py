#!/usr/bin/env python3
"""Probe-Short TEIL 1: Animation-Opener + CC-B-Roll (Ken-Burns) + Captions -> 9:16 mp4.
Zeigt den Zusammenbau (Animation + selbst aus dem Netz gezogene echte Bilder).
Ohne finale VO (kommt spaeter) -> Captions als Platzhalter im Kanal-Stil (Text = Stimme)."""
import subprocess, pathlib
BASE = pathlib.Path("/home/user/twitchclipz/nuttyputty")
ANIM = BASE/"animation/querschnitt_demo.mp4"
BROLL = BASE/"broll"
TMP = BASE/"_probe_tmp"; TMP.mkdir(exist_ok=True)
FONT = "/usr/share/fonts/truetype/roboto/unhinted/RobotoTTF/Roboto-Black.ttf"
FPS = 25
def run(args): subprocess.run(args, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def esc(t): return t.replace(":","\\:").replace("'","\u2019")

def caption(lines, y0=1360):
    # zwei Zeilen weisser Fettschrift mit schwarzer Kontur (Kanal-Stil)
    out=[]
    for i,l in enumerate(lines):
        out.append(f"drawtext=fontfile={FONT}:text='{esc(l)}':fontcolor=white:fontsize=64:"
                   f"borderw=7:bordercolor=black:x=(w-tw)/2:y={y0+i*84}")
    return ",".join(out)

def broll_seg(img, lines, dur, out, zdir=1):
    n=int(dur*FPS)
    z = "min(zoom+0.0009,1.16)" if zdir>0 else "if(eq(on,0),1.16,max(zoom-0.0009,1.0))"
    vf=(f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
        f"zoompan=z='{z}':d={n}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1080x1920:fps={FPS},"
        f"eq=brightness=-0.06:saturation=0.9,"
        f"drawbox=x=0:y=1240:w=1080:h=680:color=black@0.45:t=fill,"
        f"{caption(lines)}")
    run(["ffmpeg","-y","-loop","1","-i",str(img),"-vf",vf,"-frames:v",str(n),
         "-r",str(FPS),"-c:v","libx264","-pix_fmt","yuv420p","-crf","19",str(out)])

def anim_seg(start, dur, lines, out, banner=True):
    vf=f"drawbox=x=0:y=1240:w=1080:h=680:color=black@0.35:t=fill,{caption(lines)}" if lines else "null"
    run(["ffmpeg","-y","-ss",str(start),"-t",str(dur),"-i",str(ANIM),
         "-vf",vf,"-r",str(FPS),"-c:v","libx264","-pix_fmt","yuv420p","-crf","19",str(out)])

# --- Segmente (TEIL 1 Sprechtext als Captions) ---
segs=[]
# 1) Animations-Opener (Hook, eigener gelber Banner in der Animation) 0-3.4s
anim_seg(0.0, 3.4, [], TMP/"s1.mp4"); segs.append(TMP/"s1.mp4")
# 2) B-Roll Höhleneingang
broll_seg(BROLL/"cave_entrance.jpg", ["Eine Höhle, die als","Anfängerhöhle gilt."], 3.2, TMP/"s2.mp4", 1); segs.append(TMP/"s2.mp4")
# 3) B-Roll enger Kriechgang
broll_seg(BROLL/"passage_crawl.jpg", ["John Jones, 26 — erfahren.","Er zwängt sich in einen Spalt."], 3.4, TMP/"s3.mp4", -1); segs.append(TMP/"s3.mp4")
# 4) Animation Verkeilen (Kippen+Rutschen+Fest) ~5.0-8.9s
anim_seg(5.0, 3.9, ["Kopfüber. 18 × 10 cm.","Nicht größer als ein Laptop."], TMP/"s4.mp4"); segs.append(TMP/"s4.mp4")
# 5) B-Roll Höhle dunkel — Schluss
broll_seg(BROLL/"cave_mammoth_1.jpg", ["Er kam da nie","wieder heraus."], 3.0, TMP/"s5.mp4", 1); segs.append(TMP/"s5.mp4")

# concat
lst=TMP/"list.txt"; lst.write_text("".join(f"file '{s}'\n" for s in segs))
out=BASE/"probe_short_teil1.mp4"
run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(lst),
     "-c:v","libx264","-pix_fmt","yuv420p","-crf","19","-movflags","+faststart",str(out)])
print("OK ->", out)
