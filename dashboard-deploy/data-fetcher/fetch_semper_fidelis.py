#!/usr/bin/env python3
"""
Coleta dados para o dashboard de Semper Fidelis.
Uso: python3 fetch_semper_fidelis.py --start 2026-04-01 --end 2026-04-30
"""

import argparse, json, sys, os, subprocess
from datetime import datetime, date, timedelta
from pathlib import Path

SKILLS       = Path.home() / ".claude/skills"
GADS_READ    = SKILLS / "google-ads-ratos/scripts/read.py"

OUT_DIR = Path(__file__).parent.parent / "pages/semper-fidelis"
GADS_CUSTOMER  = "6779674397"

def run(cmd, label=""):
    try:
        result = subprocess.run([sys.executable]+cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0:
            print(f"⚠️  {label}: {result.stderr[-300:]}", file=sys.stderr); return None
        lines = [l for l in result.stdout.splitlines()
                 if l.strip() and not l.startswith(("/","Client","Token","warn"))]
        return json.loads("\n".join(lines))
    except Exception as e:
        print(f"❌ {label}: {e}", file=sys.stderr); return None

def fmt_brl(val):
    try: return round(float(val),2)
    except: return 0.0
def fmt_int(val):
    try: return int(val)
    except: return 0
def fmt_pct(val):
    try: return round(float(val),2)
    except: return 0.0

def fetch_google_ads(start, end):
    print("🔴 Google Ads — coletando...", flush=True)
    base = [str(GADS_READ)]
    campaigns_raw = run(base+["campaigns","--customer-id",GADS_CUSTOMER,"--since",start,"--until",end], "GAds campaigns")
    keywords_raw  = run(base+["keywords","--customer-id",GADS_CUSTOMER,"--since",start,"--until",end], "GAds keywords")
    search_terms_raw = run(base+["search-terms","--customer-id",GADS_CUSTOMER,"--since",start,"--until",end], "GAds search-terms")
    spend=impressions=clicks=conversions=0
    campaigns=[]
    if campaigns_raw:
        for c in campaigns_raw:
            m=c.get("metrics",{}); cp=c.get("campaign",{})
            s=fmt_brl(m.get("cost",0)); i=fmt_int(m.get("impressions",0))
            cl=fmt_int(m.get("clicks",0)); cv=fmt_int(m.get("conversions",0))
            spend+=s; impressions+=i; clicks+=cl; conversions+=cv
            if i==0: continue
            ctr=fmt_pct(m.get("ctr",0)*100)
            cpc=fmt_brl(m.get("average_cpc",0)/1_000_000) if m.get("average_cpc") else 0
            campaigns.append({"name":cp.get("name","—"),"type":cp.get("advertising_channel_type","—").title(),
                "status":cp.get("status","—").title(),"spend":s,"impressions":i,"clicks":cl,"ctr":ctr,"cpc":cpc,"conversions":cv})
    ctr_total=round(clicks/impressions*100,2) if impressions else 0
    cpc_avg=round(spend/clicks,2) if clicks else 0
    cpa=round(spend/conversions,2) if conversions else 0
    keywords=[]
    if keywords_raw:
        for kw in keywords_raw[:200]:
            k=kw.get("ad_group_criterion",{}); m=kw.get("metrics",{})
            imp=fmt_int(m.get("impressions",0))
            if imp==0: continue
            keywords.append({"keyword":k.get("keyword",{}).get("text","—"),"match":k.get("keyword",{}).get("match_type","—").title(),
                "impressions":imp,"clicks":fmt_int(m.get("clicks",0)),"ctr":fmt_pct(m.get("ctr",0)*100),
                "cpc":fmt_brl(m.get("average_cpc",0)/1_000_000) if m.get("average_cpc") else 0,"conversions":fmt_int(m.get("conversions",0))})
    search_terms=[]
    if search_terms_raw:
        for st in search_terms_raw[:50]:
            s=st.get("search_term_view",{}); m=st.get("metrics",{})
            search_terms.append({"term":s.get("search_term","—"),"keyword":s.get("keyword","—"),
                "impressions":fmt_int(m.get("impressions",0)),"clicks":fmt_int(m.get("clicks",0)),
                "ctr":fmt_pct(m.get("ctr",0)*100),"cpc":fmt_brl(m.get("average_cpc",0)/1_000_000) if m.get("average_cpc") else 0})
    return {"spend":round(spend,2),"impressions":impressions,"clicks":clicks,"ctr":ctr_total,
            "cpc":cpc_avg,"conversions":conversions,"cpa":cpa,"campaigns":campaigns,"keywords":keywords,"search_terms":search_terms}

def main():
    parser = argparse.ArgumentParser(description="Coleta dados para Semper Fidelis")
    parser.add_argument("--start", default="")
    parser.add_argument("--end",   default="")
    parser.add_argument("--preset", default="last_month",
                        choices=["last_month","this_month","last_7d","last_30d"])
    args = parser.parse_args()
    today = date.today()
    if args.start and args.end:
        start, end = args.start, args.end
    elif args.preset == "last_month":
        first=today.replace(day=1); last_m_end=first-timedelta(days=1)
        start=last_m_end.replace(day=1).isoformat(); end=last_m_end.isoformat()
    elif args.preset == "this_month":
        start=today.replace(day=1).isoformat(); end=today.isoformat()
    elif args.preset == "last_7d":
        start=(today-timedelta(days=7)).isoformat(); end=today.isoformat()
    else:
        start=(today-timedelta(days=30)).isoformat(); end=today.isoformat()
    print(f"\n📅 Período: {start} → {end}\n", flush=True)
    google = fetch_google_ads(start, end)
    data = {"cliente":"Semper Fidelis","periodo":{"start":start,"end":end},"gerado_em":datetime.now().isoformat(),
        "consolidado":None,
        "meta":None,
        "google":google,
        "ga4":None,
        "gmb":None}
    out_path = OUT_DIR / "data.json"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"\n✅ data.json salvo em {out_path}")
    print(f"   Google spend: R$ {google['spend']}")

if __name__ == "__main__":
    main()
