#!/usr/bin/env python3
"""Google Trends: Interesse + verwandte Suchen (DE). Nutzung: python3 nb_trends.py "nutty putty" "höhlenunglück" """
import sys
try:
    from pytrends.request import TrendReq
except Exception:
    print("pytrends nicht installiert (setup-tools.sh)"); sys.exit(0)
kws=sys.argv[1:] or ["katastrophe"]
p=TrendReq(hl="de-DE", tz=60)
p.build_payload(kws[:5], geo="DE", timeframe="today 3-m")
try:
    iot=p.interest_over_time()
    if not iot.empty:
        print("Interesse (Ø letzte 3 Monate, DE):")
        for k in kws[:5]:
            if k in iot: print(f"  {k}: Ø {iot[k].mean():.0f}, Peak {iot[k].max()}")
    rq=p.related_queries()
    for k in kws[:5]:
        top=(rq.get(k,{}) or {}).get("top")
        if top is not None and not top.empty:
            print(f"Verwandt zu '{k}':", ", ".join(top['query'].head(8)))
except Exception as e:
    print("Trends-Abruf gedrosselt/fehlgeschlagen:", str(e)[:80])
