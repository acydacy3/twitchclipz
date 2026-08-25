#!/usr/bin/env python3
"""Openverse CC-Bildsuche + Download. Nutzung: python3 nb_openverse.py "cave rescue rope" out_dir [n]"""
import sys, json, subprocess, urllib.parse, pathlib
def search(q, n=5):
    u=("https://api.openverse.org/v1/images/?format=json&license_type=commercial,modification"
       f"&page_size={n}&q={urllib.parse.quote(q)}")
    r=subprocess.run(["curl","-s","--max-time","30","-A","KatastrophenprotokollBot/1.0",u],capture_output=True,text=True)
    try: return json.loads(r.stdout).get("results",[])
    except Exception: return []
if __name__=="__main__":
    q=sys.argv[1]; out=pathlib.Path(sys.argv[2] if len(sys.argv)>2 else "."); out.mkdir(parents=True,exist_ok=True)
    n=int(sys.argv[3]) if len(sys.argv)>3 else 5; got=0
    for r in search(q,n*2):
        if got>=n: break
        url=r.get("url"); 
        if not url: continue
        raw=out/f"ov_{got+1}.raw"
        subprocess.run(["curl","-sL","--max-time","40","-o",str(raw),url])
        o=out/f"ov_{got+1:02d}.jpg"
        rr=subprocess.run(["convert",str(raw),"-resize","1600x2848^","-gravity","center","-extent","1600x2848","-quality","92",str(o)],capture_output=True)
        raw.unlink(missing_ok=True)
        if rr.returncode==0:
            got+=1; print(f"{o.name} <- {r.get('title','')[:40]} [{r.get('license','')} {r.get('license_version','')}] {r.get('creator','')}")
    print(f"Openverse: {got} Bilder")
