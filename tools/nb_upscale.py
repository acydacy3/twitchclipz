#!/usr/bin/env python3
"""Upscale (Real-ESRGAN falls da, sonst Lanczos) + optional rembg-Cutout.
Nutzung: python3 nb_upscale.py in.jpg out.jpg [--cutout cutout.png]"""
import sys, subprocess
inp=sys.argv[1]; out=sys.argv[2]
try:
    import torch, numpy as np, cv2
    from realesrgan import RealESRGANer
    from basicsr.archs.rrdbnet_arch import RRDBNet
    m=RRDBNet(num_in_ch=3,num_out_ch=3,num_feat=64,num_block=23,num_grow_ch=32,scale=4)
    up=RealESRGANer(scale=4,model_path="https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth",model=m,half=False)
    img=cv2.imread(inp); o,_=up.enhance(img,outscale=2); cv2.imwrite(out,o); print("Real-ESRGAN ->",out)
except Exception as e:
    subprocess.run(["convert",inp,"-filter","Lanczos","-resize","200%","-unsharp","0x1.0+1.0+0.02",out],check=True)
    print("Fallback Lanczos+sharpen ->",out,"(",str(e)[:50],")")
if "--cutout" in sys.argv:
    cut=sys.argv[sys.argv.index("--cutout")+1]
    try:
        from rembg import remove; from PIL import Image
        Image.open(out); open(cut,"wb").write(remove(open(out,"rb").read())); print("Cutout ->",cut)
    except Exception as e: print("rembg nicht verfuegbar:",str(e)[:50])
