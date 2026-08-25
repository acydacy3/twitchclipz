#!/usr/bin/env python3
"""Piper Scratch-VO (deutsch) zum Timen der Animation. Nutzung: python3 nb_tts.py "Text" out.mp3"""
import sys, subprocess, pathlib, tempfile
P=pathlib.Path("/home/user/twitchclipz/tools/piper")
BIN=P/"piper"/"piper"; VOICE=P/"de_DE-thorsten-medium.onnx"
if not BIN.exists() or not VOICE.exists():
    print("Piper nicht installiert (setup-tools.sh)"); sys.exit(1)
text=sys.argv[1]; out=sys.argv[2] if len(sys.argv)>2 else "scratch.mp3"
wav=tempfile.mktemp(suffix=".wav")
subprocess.run([str(BIN),"--model",str(VOICE),"--output_file",wav],input=text,text=True,check=True)
subprocess.run(["ffmpeg","-y","-loglevel","error","-i",wav,"-ar","48000","-b:a","192k",out],check=True)
print("Scratch-VO ->",out)
