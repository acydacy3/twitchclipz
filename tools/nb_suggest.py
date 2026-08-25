#!/usr/bin/env python3
"""YouTube-Suggest: Keyword-Ideen fuer Titel/Tags. Nutzung: python3 nb_suggest.py "höhle unglück" """
import sys, json, subprocess, urllib.parse
def suggest(q, hl="de"):
    u=("https://clients1.google.com/complete/search?client=youtube&ds=yt"
       f"&hl={hl}&q={urllib.parse.quote(q)}")
    r=subprocess.run(["curl","-s","--max-time","20",u],capture_output=True)
    txt=r.stdout.decode("latin-1","replace")
    i,j=txt.find("["), txt.rfind("]")
    try:
        data=json.loads(txt[i:j+1]); return [s[0] for s in data[1]]
    except Exception: return []
if __name__=="__main__":
    q=" ".join(sys.argv[1:]) or "katastrophe doku"
    for s in suggest(q)[:12]: print(s)
