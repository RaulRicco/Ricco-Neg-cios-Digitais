#!/usr/bin/env python3
"""
Coleta dados para o dashboard de Supermercado Bistecão.
Uso: python3 fetch_bistecao.py --start 2026-04-01 --end 2026-04-30
"""

import argparse, json, sys, os, subprocess
from datetime import datetime, date, timedelta
from pathlib import Path

SKILLS       = Path.home() / ".claude/skills"
META_INSIGHTS = SKILLS / "meta-ads-ratos/scripts/insights.py"
GADS_READ    = SKILLS / "google-ads-ratos/scripts/read.py"
GA4_REPORTS  = SKILLS / "ga4-ratos/scripts/reports.py"

OUT_DIR = Path(__file__).parent.parent / "pages/bistecao"
META_ACCOUNT   = "act_164474806974058"

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

OBJECTIVE_MAP = {
    "MESSAGES":           ("onsite_conversion.messaging_conversation_started_7d", "Mensagens"),
    "LEAD_GENERATION":    ("lead",                                                "Leads"),
    "OUTCOME_SALES":      ("purchase",                                            "Vendas"),
    "OUTCOME_LEADS":      ("lead",                                                "Leads"),
    "OUTCOME_ENGAGEMENT": ("post_engagement",                                     "Engajamentos"),
    "OUTCOME_TRAFFIC":    ("link_click",                                          "Cliques"),
    "LINK_CLICKS":        ("link_click",                                          "Cliques"),
    "CONVERSIONS":        ("purchase",                                            "Conversões"),
    "REACH":              ("reach",                                               "Alcance"),
    "BRAND_AWARENESS":    ("reach",                                               "Alcance"),
    "VIDEO_VIEWS":        ("video_view",                                          "Views"),
    "POST_ENGAGEMENT":    ("post_engagement",                                     "Engajamentos"),
}

def extract_result(obj, actions, spend):
    action_map = {a["action_type"]: int(float(a.get("value", 0)))
                  for a in (actions or []) if isinstance(a, dict)}
    msg_key = "onsite_conversion.messaging_conversation_started_7d"
    if msg_key in action_map and action_map[msg_key] > 0:
        qty = action_map[msg_key]
        cpr = round(spend / qty, 2) if qty else 0
        return "Mensagens", qty, cpr
    action_key, label = OBJECTIVE_MAP.get(obj, ("link_click", "Cliques"))
    qty = action_map.get(action_key, 0)
    cpr = round(spend / qty, 2) if qty else 0
    return label, qty, cpr

def fetch_meta(start, end):
    print("📘 Meta Ads — coletando...", flush=True)
    base = [str(META_INSIGHTS)]
    time_range = ["--time-range", f'{{"since":"{start}","until":"{end}"}}']
    account = run(base+["account","--account",META_ACCOUNT,
        "--fields","spend,reach,impressions,clicks,cpm,cpc,ctr,frequency"]+time_range, "Meta account")
    campaigns_raw = run(base+["account","--account",META_ACCOUNT,
        "--fields","spend,reach,impressions,clicks,cpm,cpc,ctr,campaign_name,objective,actions",
        "--level","campaign"]+time_range, "Meta campaigns")
    ads_raw = run(base+["account","--account",META_ACCOUNT,
        "--fields","spend,impressions,clicks,ctr,cpc,frequency,ad_name,campaign_name,objective,actions",
        "--level","ad"]+time_range, "Meta ads")
    totals = account[0] if account else {}
    campaigns = []
    if campaigns_raw:
        for c in campaigns_raw[:20]:
            imp = fmt_int(c.get("impressions",0))
            if imp == 0: continue
            spend = fmt_brl(c.get("spend",0))
            obj = c.get("objective","")
            label, qty, cpr = extract_result(obj, c.get("actions",[]), spend)
            campaigns.append({"name":c.get("campaign_name","—"),"objective":obj,"spend":spend,
                "reach":fmt_int(c.get("reach",0)),"impressions":imp,"clicks":fmt_int(c.get("clicks",0)),
                "ctr":fmt_pct(c.get("ctr",0)),"cpc":fmt_brl(c.get("cpc",0)),
                "result_label":label,"result_qty":qty,"result_cpr":cpr})
    ads = []
    if ads_raw:
        for a in ads_raw[:50]:
            if fmt_int(a.get("impressions",0)) == 0: continue
            spend = fmt_brl(a.get("spend",0))
            obj = a.get("objective","")
            label, qty, cpr = extract_result(obj, a.get("actions",[]), spend)
            ads.append({"name":a.get("ad_name","—"),"campaign":a.get("campaign_name","—"),
                "spend":spend,"impressions":fmt_int(a.get("impressions",0)),"clicks":fmt_int(a.get("clicks",0)),
                "ctr":fmt_pct(a.get("ctr",0)),"cpc":fmt_brl(a.get("cpc",0)),"frequency":fmt_pct(a.get("frequency",0)),
                "result_label":label,"result_qty":qty,"result_cpr":cpr})
    return {"spend":fmt_brl(totals.get("spend",0)),"reach":fmt_int(totals.get("reach",0)),
            "impressions":fmt_int(totals.get("impressions",0)),"clicks":fmt_int(totals.get("clicks",0)),
            "cpm":fmt_brl(totals.get("cpm",0)),"cpc":fmt_brl(totals.get("cpc",0)),
            "ctr":fmt_pct(totals.get("ctr",0)),"frequency":fmt_pct(totals.get("frequency",0)),
            "campaigns":campaigns,"ads":ads}

def main():
    parser = argparse.ArgumentParser(description="Coleta dados para Supermercado Bistecão")
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
    meta   = fetch_meta(start, end)
    data = {"cliente":"Supermercado Bistecão","periodo":{"start":start,"end":end},"gerado_em":datetime.now().isoformat(),
        "consolidado":None,
        "meta":meta,
        "google":None,
        "ga4":None,
        "gmb":None}
    out_path = OUT_DIR / "data.json"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    print(f"\n✅ data.json salvo em {out_path}")
    print(f"   Meta spend:   R$ {meta['spend']}")

if __name__ == "__main__":
    main()