"""Praeziser B-Roll-Fetch aus KURIERTEN Wikimedia-Commons-Kategorien (topisch garantiert).
Autonom + praezise (Nutzer sucht keine Bilder mehr). Resume-faehig, Magic-Byte-Pruefung."""
import json, subprocess, time, urllib.parse, pathlib, re
BASE = pathlib.Path("/home/user/twitchclipz/nuttyputty")
UA = "KatastrophenprotokollBot/1.0 (acydacy3@gmail.com)"
ATTR = BASE/"broll"/"ATTRIBUTION.txt"
# Negativ: Personen/Events/Nicht-Foto raus (z. B. Musiker "Nick Cave")
BAD = re.compile(r"map|diagram|plan|logo|icon|chart|\.svg|seal|coat of arms|poster|"
                 r"band|concert|festival|singer|tour|album|award|portrait of|"
                 r"stamp|coin|painting|drawing|statue|bust |"
                 r"banner|flag|crest|brigade|emblem|badge|"
                 r"\bkey\b|keys|pen |pencil|mummy.?clip|carabiner.*pin|product|"
                 r"museum|exhibit|book|cover", re.I)
NEED = 3   # bis zu 3 Szenen pro Short

# pro Short: kuratierte Kategorien (Prio) — topisch sicher
PLAN = {
 "01": ["Category:Cave interiors","Category:Limestone caves","Category:Caving"],
 "02": ["Category:Caving","Category:Cave entrances","Category:Speleology"],
 "03": ["Category:Caving","Category:Speleology"],
 "04": ["Category:Single Rope Technique","Category:Vertical caving","Category:Cave shafts"],
 "05": ["Category:Slot canyons","Category:Rock fractures","Category:Narrow passages"],
 "06": ["Category:Cave rescue","Category:Caving"],
 "07": ["Category:Cave rescue","Category:Speleology"],
 "08": ["Category:Mine rescue","Category:Cave rescue"],
 "09": ["Category:Carabiners","Category:Climbing equipment","Category:Climbing protection"],
 "10": ["Category:Memorial plaques","Category:Deserts of Utah","Category:Canyons of Utah"],
}

def curl(url, out=None):
    a=["curl","-s","-L","--max-time","40","-A",UA]+(["-o",out] if out else [])+[url]
    return subprocess.run(a,capture_output=True,text=(out is None))

def cat_files(cat):
    q=urllib.parse.quote(cat)
    url=(f"https://commons.wikimedia.org/w/api.php?action=query&list=categorymembers"
         f"&cmtitle={q}&cmtype=file&cmlimit=40&format=json")
    for _ in range(4):
        r=curl(url)
        try:
            d=json.loads(r.stdout); return [m["title"] for m in d.get("query",{}).get("categorymembers",[])]
        except Exception: time.sleep(4)
    return []

def info(title):
    q=urllib.parse.quote(title)
    url=(f"https://commons.wikimedia.org/w/api.php?action=query&titles={q}"
         f"&prop=imageinfo&iiprop=url|extmetadata|mime|size&iiurlwidth=1500&format=json")
    for _ in range(3):
        r=curl(url)
        try:
            d=json.loads(r.stdout); p=list(d.get("query",{}).get("pages",{}).values())[0]
            return (p.get("imageinfo") or [{}])[0]
        except Exception: time.sleep(3)
    return {}

def dl_jpeg(thumb, orig, dest):
    for url in [thumb, orig]:
        if not url: continue
        for _ in range(2):
            curl(url, dest)
            try:
                with open(dest,"rb") as f:
                    if f.read(2)==b"\xff\xd8": return True
            except Exception: pass
            time.sleep(3)
    return False

def have(short):
    d=BASE/"bilder"/f"short_{short}"
    return len(list(d.glob("[0-9][0-9].jpg"))) if d.exists() else 0

def fetch(short, cats):
    d=BASE/"bilder"/f"short_{short}"; d.mkdir(parents=True,exist_ok=True)
    got=have(short); seen=set()
    for cat in cats:
        if got>=NEED: break
        for title in cat_files(cat):
            if got>=NEED: break
            if title in seen or BAD.search(title): continue
            seen.add(title)
            ii=info(title); time.sleep(1)
            if "image/jpeg" not in ii.get("mime","") or (ii.get("width") or 0)<1000: continue
            lic=ii.get("extmetadata",{}).get("LicenseShortName",{}).get("value","?")
            if not (lic.lower().startswith("cc") or "public domain" in lic.lower()): continue
            art=re.sub("<[^>]+>","",ii.get("extmetadata",{}).get("Artist",{}).get("value","?"))[:50]
            raw=d/"raw.jpg"; out=d/f"{got+1:02d}.jpg"
            if not dl_jpeg(ii.get("thumburl"), ii.get("url"), str(raw)): continue
            r=subprocess.run(["convert",str(raw),"-resize","1600x2848^","-gravity","center",
                              "-extent","1600x2848","-quality","92",str(out)],capture_output=True)
            raw.unlink(missing_ok=True)
            if r.returncode==0 and out.exists():
                got+=1
                with open(ATTR,"a") as f:
                    f.write(f"short_{short}/{got:02d}.jpg <- Commons '{title}' [{cat}], {lic}, {art}\n")
                print(f"[{short}] {got:02d} <- {title[:55]} ({lic})",flush=True)
            time.sleep(2)
    return got

if __name__=="__main__":
    total=0
    for s,cats in PLAN.items():
        n=fetch(s,cats); total+=n; print(f"[{s}] -> {n}/{NEED}",flush=True)
    print(f"FERTIG gesamt: {total}")
