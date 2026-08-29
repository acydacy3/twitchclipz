"""V2: Fixes broll-Duplikat-Problem durch globalen used-Set.
Pro Short eigene, spezifische Kategorien — keine Datei doppelt."""
import json, subprocess, time, urllib.parse, pathlib, re, shutil

BASE = pathlib.Path("/home/user/twitchclipz/prosperi")
UA   = "KatastrophenprotokollBot/1.0 (acydacy3@gmail.com)"
ATTR = BASE/"broll"/"ATTRIBUTION.txt"
NEED = 3

BAD = re.compile(
    r"map|diagram|plan|logo|icon|chart|\.svg|seal|coat.of.arms|poster|"
    r"band|concert|festival|singer|tour|album|award|portrait.of|"
    r"stamp|coin|painting|drawing|statue|bust |banner|flag|crest|brigade|"
    r"emblem|badge|\bkey\b|keys|pen |pencil|mummy|product|museum|exhibit|"
    r"book|cover|\.pdf|stamp|IA_|IA |IA-|ia_", re.I)

# Globaler Dedup-Set: kein Bild darf in zwei Shorts vorkommen
used_globally: set[str] = set()

# Sehr spezifische Kategorien pro Short — topisch passend + keine Überschneidungen
PLAN = {
    "01": [
        "Category:Erg Chebbi",           # echte Sahara-Dünen (Marokko)
        "Category:Draa Valley",           # Marokkanische Wüstenlandschaft
        "Category:Merzouga",              # Dorf nahe Erg Chebbi
        "Category:Desert landscapes of Morocco",
        "Category:Sand dunes of Morocco",
    ],
    "02": [
        "Category:Rome",
        "Category:Piazza Navona",
        "Category:Colosseum",
        "Category:Italian Police",
        "Category:Athletics",
    ],
    "03": [
        "Category:Marathon des Sables",   # echte Rennfotos inkl. 1994!
        "Category:Desert running",
        "Category:Zagora Province",       # Marokkanische Wüste (MdS-Gebiet)
        "Category:Runners in Morocco",
        "Category:Draa-Tafilalet",
    ],
    "04": [
        "Category:Dust storms",
        "Category:Harmattan",
        "Category:Sandstorms",
        "Category:Erg Chech",             # Algerische Wüste – andere Dünen
        "Category:Tassili n'Ajjer",
    ],
    "05": [
        "Category:Helicopters in Africa",
        "Category:Search and rescue",
        "Category:Saharan landscapes",
        "Category:Timimoun",              # Algerische Oasenstadt
        "Category:In Salah",
    ],
    "06": [
        "Category:Bats",
        "Category:Chiroptera",
        "Category:Marabouts",
        "Category:Desert architecture of Algeria",
        "Category:Tamanrasset Province",
    ],
    "07": [
        "Category:Ténéré",               # Niger-Sahara — ganz andere Bilder
        "Category:Fezzan",               # Libyscher Wüstenteil
        "Category:Ahaggar Mountains",
        "Category:Grand Erg Oriental",
        "Category:Sahara night",
    ],
    "08": [
        "Category:Tuareg people",
        "Category:Nomads in Algeria",
        "Category:Nomadic people of Africa",
        "Category:Desert people",
        "Category:Berber people",
    ],
    "09": [
        "Category:Goats in Africa",
        "Category:Goats in Algeria",
        "Category:Nomad camps",
        "Category:Tent camps",
        "Category:Beduins",
    ],
    "10": [
        "Category:Piazza del Popolo",
        "Category:Vatican",
        "Category:Italian families",
        "Category:Happiness",
        "Category:Homecoming",
    ],
}

def curl(url):
    r = subprocess.run(
        ["curl","-s","-L","--max-time","30","-A",UA,url],
        capture_output=True, text=True)
    return r

def cat_files(cat):
    q = urllib.parse.quote(cat)
    url = (f"https://commons.wikimedia.org/w/api.php?action=query"
           f"&list=categorymembers&cmtitle={q}&cmtype=file"
           f"&cmlimit=50&format=json")
    for _ in range(3):
        r = curl(url)
        try:
            d = json.loads(r.stdout)
            return [m["title"] for m in d.get("query",{}).get("categorymembers",[])]
        except Exception:
            time.sleep(4)
    return []

def info(title):
    q = urllib.parse.quote(title)
    url = (f"https://commons.wikimedia.org/w/api.php?action=query"
           f"&titles={q}&prop=imageinfo"
           f"&iiprop=url|extmetadata|mime|size&iiurlwidth=1600&format=json")
    for _ in range(3):
        r = curl(url)
        try:
            d = json.loads(r.stdout)
            p = list(d.get("query",{}).get("pages",{}).values())[0]
            return (p.get("imageinfo") or [{}])[0]
        except Exception:
            time.sleep(3)
    return {}

def dl_ok(url, dest):
    r = subprocess.run(
        ["curl","-s","-L","--max-time","30","-A",UA,"-o",dest,url],
        capture_output=True)
    p = pathlib.Path(dest)
    if r.returncode == 0 and p.exists() and p.stat().st_size > 15000:
        hdr = p.read_bytes()[:4]
        if hdr[:3] == b'\xff\xd8\xff' or hdr[:4] == b'\x89PNG':
            return True
    p.unlink(missing_ok=True)
    return False

def resize(src, dst):
    subprocess.run(
        ["convert", src, "-resize","1600x2848^","-gravity","center",
         "-extent","1600x2848", dst], capture_output=True)

# Bestehende broll-Ordner löschen (Neustart sauber)
broll_root = BASE/"broll"
for d in broll_root.glob("short_*/"):
    shutil.rmtree(d, ignore_errors=True)
broll_root.mkdir(parents=True, exist_ok=True)

attr_lines: list[str] = []

for n, cats in PLAN.items():
    out_dir = BASE/"broll"/f"short_{n}"
    out_dir.mkdir(parents=True, exist_ok=True)
    collected = 0
    print(f"\n[S{n}] suche B-Roll ({NEED} Bilder)...", flush=True)
    for cat in cats:
        if collected >= NEED:
            break
        titles = cat_files(cat)
        print(f"  {cat}: {len(titles)} Dateien", flush=True)
        for t in titles:
            if collected >= NEED:
                break
            # Globaler Dedup-Check
            canonical = t.lower().strip()
            if canonical in used_globally:
                continue
            if BAD.search(t):
                continue
            iv = info(t)
            mime = iv.get("mime","")
            if not mime.startswith("image/"):
                continue
            # Größe prüfen (min 200×200)
            w = iv.get("width", 0); h = iv.get("height", 0)
            if w < 200 or h < 200:
                continue
            thumb = iv.get("thumburl")
            orig  = iv.get("url")
            if not thumb and not orig:
                continue
            idx = f"{collected+1:02d}"
            tmp = str(out_dir/f"tmp_{idx}.jpg")
            dst = str(out_dir/f"{idx}.jpg")
            ok = False
            for url in [thumb, orig]:
                if url and dl_ok(url, tmp):
                    ok = True; break
            if not ok:
                continue
            resize(tmp, dst)
            pathlib.Path(tmp).unlink(missing_ok=True)
            used_globally.add(canonical)
            lic  = iv.get("extmetadata",{}).get("LicenseShortName",{}).get("value","CC")
            auth = iv.get("extmetadata",{}).get("Artist",{}).get("value","?")
            auth = re.sub(r"<[^>]+>","",auth)
            attr_lines.append(f"S{n}/{idx}: {t} | {auth} | {lic}")
            print(f"    [{idx}] OK: {t[:70]}", flush=True)
            collected += 1
    print(f"  → S{n}: {collected}/{NEED} Bilder", flush=True)

ATTR.write_text("\n".join(attr_lines))
print("\nBROLL V2 FERTIG")
