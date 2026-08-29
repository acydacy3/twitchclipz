"""Praeziser B-Roll-Fetch aus KURIERTEN Wikimedia-Commons-Kategorien (Sahara/Wueste).
Autonom + praezise. Resume-faehig, Magic-Byte-Pruefung."""
import json, subprocess, time, urllib.parse, pathlib, re
BASE = pathlib.Path("/home/user/twitchclipz/prosperi")
UA = "KatastrophenprotokollBot/1.0 (acydacy3@gmail.com)"
ATTR = BASE/"broll"/"ATTRIBUTION.txt"
BAD = re.compile(r"map|diagram|plan|logo|icon|chart|\.svg|seal|coat of arms|poster|"
                 r"band|concert|festival|singer|tour|album|award|portrait of|"
                 r"stamp|coin|painting|drawing|statue|bust |"
                 r"banner|flag|crest|brigade|emblem|badge|"
                 r"\bkey\b|keys|pen |pencil|mummy|product|"
                 r"museum|exhibit|book|cover|runner.*race|finish.*line", re.I)
NEED = 3

# Pro Short: kuratierte Kategorien — topisch sicher, Sahara/Wüste
PLAN = {
 "01": ["Category:Sahara","Category:Sand dunes","Category:Erg Chebbi"],
 "02": ["Category:Rome","Category:Italian police","Category:Pentathlon"],
 "03": ["Category:Sahara","Category:Desert running","Category:Morocco deserts"],
 "04": ["Category:Sandstorms","Category:Sand dunes","Category:Sahara"],
 "05": ["Category:Sahara","Category:Helicopters in Morocco","Category:Desert rescue"],
 "06": ["Category:Marabouts","Category:Desert architecture","Category:Bats"],
 "07": ["Category:Sahara","Category:Desert landscapes","Category:Sunsets in Africa"],
 "08": ["Category:Sahara","Category:Desert landscapes","Category:Tuareg people"],
 "09": ["Category:Sahara","Category:Goats in Algeria","Category:Algeria deserts"],
 "10": ["Category:Rome","Category:Italy","Category:Desert survivors"],
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
            r=subprocess.run(["curl","-s","-L","--max-time","30","-A",UA,"-o",dest,url],capture_output=True)
            if r.returncode==0 and pathlib.Path(dest).stat().st_size>10000:
                hdr=pathlib.Path(dest).read_bytes()[:4]
                if hdr[:3]==b'\xff\xd8\xff' or hdr[:4]==b'\x89PNG':
                    return True
            pathlib.Path(dest).unlink(missing_ok=True)
    return False

def resize(src, dst):
    subprocess.run(["convert",src,"-resize","1600x2848^","-gravity","center",
                    "-extent","1600x2848",dst],capture_output=True)

attr_lines=[]
for n, cats in PLAN.items():
    out_dir = BASE/"broll"/f"short_{n}"
    out_dir.mkdir(parents=True,exist_ok=True)
    existing = list(out_dir.glob("[0-9][0-9].jpg"))
    if len(existing)>=NEED:
        print(f"[{n}] bereits {len(existing)} Bilder, skip"); continue
    collected=len(existing); tried=set(str(p.name) for p in existing)
    print(f"[{n}] suche B-Roll (brauche {NEED-collected} mehr)...", flush=True)
    for cat in cats:
        if collected>=NEED: break
        titles=cat_files(cat)
        for t in titles:
            if collected>=NEED: break
            safe=re.sub(r"[^a-zA-Z0-9_.-]","_",t)[:60]
            if safe in tried or BAD.search(t): continue
            tried.add(safe)
            iv=info(t)
            mime=iv.get("mime","")
            if not mime.startswith("image/"): continue
            thumb=iv.get("thumburl"); orig=iv.get("url")
            idx=f"{collected+1:02d}"
            tmp=str(out_dir/f"tmp_{idx}.jpg")
            dst=str(out_dir/f"{idx}.jpg")
            if not dl_jpeg(thumb,orig,tmp): continue
            resize(tmp,dst); pathlib.Path(tmp).unlink(missing_ok=True)
            lic=iv.get("extmetadata",{}).get("LicenseShortName",{}).get("value","CC")
            auth=iv.get("extmetadata",{}).get("Artist",{}).get("value","unbekannt")
            auth=re.sub(r"<[^>]+>","",auth)
            attr_lines.append(f"S{n}/{idx}: {t} | {auth} | {lic} | {orig}")
            print(f"  [{n}/{idx}] {t[:60]}", flush=True)
            collected+=1
    if collected<NEED:
        print(f"  [{n}] NUR {collected}/{NEED} gefunden (kein Fehler, KI füllt)")

ATTR.write_text("\n".join(attr_lines))
print("BROLL FERTIG")
