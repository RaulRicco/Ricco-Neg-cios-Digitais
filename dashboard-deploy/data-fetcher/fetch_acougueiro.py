#!/usr/bin/env python3
"""
Coleta dados reais das APIs e gera dashboard_data.json
para o Bar do Açougueiro — Água Verde.

Uso:
  python3 fetch_acougueiro.py --start 2026-04-01 --end 2026-04-30
  python3 fetch_acougueiro.py --preset last_month   (padrão)

O JSON gerado é copiado automaticamente para:
  ../pages/acougueiro-agua-verde/data.json
"""

import argparse
import json
import sys
import os
import subprocess
from datetime import datetime, date, timedelta
from pathlib import Path

# ─── Caminhos das skills ──────────────────────────────────────────────────────
SKILLS = Path.home() / ".claude/skills"
META_INSIGHTS  = SKILLS / "meta-ads-ratos/scripts/insights.py"
GADS_READ      = SKILLS / "google-ads-ratos/scripts/read.py"
GA4_REPORTS    = SKILLS / "ga4-ratos/scripts/reports.py"

OUT_DIR = Path(__file__).parent.parent / "pages/acougueiro-agua-verde"

# ─── Configuração do cliente ──────────────────────────────────────────────────
META_ACCOUNT   = "act_1539242697230772"
GADS_CUSTOMER  = "6349696749"
GA4_PROPERTY   = "513684569"

# ─── Helpers ─────────────────────────────────────────────────────────────────
def run(cmd, label=""):
    """Executa comando Python e retorna parsed JSON."""
    try:
        result = subprocess.run(
            [sys.executable] + cmd,
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            print(f"⚠️  {label}: {result.stderr[-300:]}", file=sys.stderr)
            return None
        # Filtra linhas que não são JSON (warnings do Python)
        lines = [l for l in result.stdout.splitlines()
                 if l.strip() and not l.startswith(("/", "Client", "Token", "warn"))]
        return json.loads("\n".join(lines))
    except Exception as e:
        print(f"❌ {label}: {e}", file=sys.stderr)
        return None

def fmt_brl(val):
    try: return round(float(val), 2)
    except: return 0.0

def fmt_int(val):
    try: return int(val)
    except: return 0

def fmt_pct(val):
    try: return round(float(val), 2)
    except: return 0.0

# ─── Coleta META ADS ─────────────────────────────────────────────────────────
def fetch_meta(start, end):
    print("📘 Meta Ads — coletando...", flush=True)
    base = [str(META_INSIGHTS)]
    period = ["--since", start, "--until", end]

    # Conta (totais)
    account = run(
        base + ["account", "--account", META_ACCOUNT,
                "--fields", "spend,reach,impressions,clicks,cpm,cpc,ctr,frequency"] + period,
        "Meta account"
    )

    # Campanhas
    campaigns_raw = run(
        base + ["account", "--account", META_ACCOUNT,
                "--fields", "spend,reach,impressions,clicks,cpm,cpc,ctr,campaign_name,objective",
                "--level", "campaign"] + period,
        "Meta campaigns"
    )

    # Anúncios
    ads_raw = run(
        base + ["account", "--account", META_ACCOUNT,
                "--fields", "spend,impressions,clicks,ctr,cpc,frequency,ad_name,campaign_name",
                "--level", "ad"] + period,
        "Meta ads"
    )

    totals = account[0] if account else {}

    campaigns = []
    if campaigns_raw:
        for c in campaigns_raw[:20]:
            campaigns.append({
                "name":        c.get("campaign_name", "—"),
                "spend":       fmt_brl(c.get("spend", 0)),
                "reach":       fmt_int(c.get("reach", 0)),
                "impressions": fmt_int(c.get("impressions", 0)),
                "clicks":      fmt_int(c.get("clicks", 0)),
                "ctr":         fmt_pct(c.get("ctr", 0)),
                "cpc":         fmt_brl(c.get("cpc", 0)),
            })

    ads = []
    if ads_raw:
        for a in ads_raw[:20]:
            ads.append({
                "name":        a.get("ad_name", "—"),
                "campaign":    a.get("campaign_name", "—"),
                "impressions": fmt_int(a.get("impressions", 0)),
                "clicks":      fmt_int(a.get("clicks", 0)),
                "ctr":         fmt_pct(a.get("ctr", 0)),
                "cpc":         fmt_brl(a.get("cpc", 0)),
                "frequency":   fmt_pct(a.get("frequency", 0)),
            })

    return {
        "spend":       fmt_brl(totals.get("spend", 0)),
        "reach":       fmt_int(totals.get("reach", 0)),
        "impressions": fmt_int(totals.get("impressions", 0)),
        "clicks":      fmt_int(totals.get("clicks", 0)),
        "cpm":         fmt_brl(totals.get("cpm", 0)),
        "cpc":         fmt_brl(totals.get("cpc", 0)),
        "ctr":         fmt_pct(totals.get("ctr", 0)),
        "frequency":   fmt_pct(totals.get("frequency", 0)),
        "campaigns":   campaigns,
        "ads":         ads,
    }

# ─── Coleta GOOGLE ADS ────────────────────────────────────────────────────────
def fetch_google_ads(start, end):
    print("🔴 Google Ads — coletando...", flush=True)
    base = [str(GADS_READ)]

    campaigns_raw = run(
        base + ["campaigns", "--customer-id", GADS_CUSTOMER,
                "--since", start, "--until", end],
        "GAds campaigns"
    )

    keywords_raw = run(
        base + ["keywords", "--customer-id", GADS_CUSTOMER,
                "--since", start, "--until", end],
        "GAds keywords"
    )

    search_terms_raw = run(
        base + ["search-terms", "--customer-id", GADS_CUSTOMER,
                "--since", start, "--until", end],
        "GAds search-terms"
    )

    # Agrega totais das campanhas
    spend = impressions = clicks = conversions = 0
    campaigns = []
    if campaigns_raw:
        for c in campaigns_raw:
            m  = c.get("metrics", {})
            cp = c.get("campaign", {})
            s  = fmt_brl(m.get("cost", 0))
            i  = fmt_int(m.get("impressions", 0))
            cl = fmt_int(m.get("clicks", 0))
            cv = fmt_int(m.get("conversions", 0))
            spend       += s
            impressions += i
            clicks      += cl
            conversions += cv
            ctr = fmt_pct(m.get("ctr", 0) * 100)
            cpc = fmt_brl(m.get("average_cpc", 0) / 1_000_000) if m.get("average_cpc") else 0
            campaigns.append({
                "name":        cp.get("name", "—"),
                "type":        cp.get("advertising_channel_type", "—").title(),
                "status":      cp.get("status", "—").title(),
                "spend":       s,
                "impressions": i,
                "clicks":      cl,
                "ctr":         ctr,
                "cpc":         cpc,
                "conversions": cv,
            })

    ctr_total = round(clicks / impressions * 100, 2) if impressions else 0
    cpc_avg   = round(spend / clicks, 2) if clicks else 0
    cpa       = round(spend / conversions, 2) if conversions else 0

    keywords = []
    if keywords_raw:
        for kw in keywords_raw[:50]:
            k = kw.get("ad_group_criterion", {})
            m = kw.get("metrics", {})
            keywords.append({
                "keyword":     k.get("keyword", {}).get("text", "—"),
                "match":       k.get("keyword", {}).get("match_type", "—").title(),
                "impressions": fmt_int(m.get("impressions", 0)),
                "clicks":      fmt_int(m.get("clicks", 0)),
                "ctr":         fmt_pct(m.get("ctr", 0) * 100),
                "cpc":         fmt_brl(m.get("average_cpc", 0) / 1_000_000) if m.get("average_cpc") else 0,
                "conversions": fmt_int(m.get("conversions", 0)),
            })

    search_terms = []
    if search_terms_raw:
        for st in search_terms_raw[:50]:
            s = st.get("search_term_view", {})
            m = st.get("metrics", {})
            search_terms.append({
                "term":        s.get("search_term", "—"),
                "keyword":     s.get("keyword", "—"),
                "impressions": fmt_int(m.get("impressions", 0)),
                "clicks":      fmt_int(m.get("clicks", 0)),
                "ctr":         fmt_pct(m.get("ctr", 0) * 100),
                "cpc":         fmt_brl(m.get("average_cpc", 0) / 1_000_000) if m.get("average_cpc") else 0,
            })

    return {
        "spend":        round(spend, 2),
        "impressions":  impressions,
        "clicks":       clicks,
        "ctr":          ctr_total,
        "cpc":          cpc_avg,
        "conversions":  conversions,
        "cpa":          cpa,
        "campaigns":    campaigns,
        "keywords":     keywords,
        "search_terms": search_terms,
    }

# ─── Coleta GA4 ───────────────────────────────────────────────────────────────
def fetch_ga4(start, end):
    print("🟡 GA4 — coletando...", flush=True)
    base = [str(GA4_REPORTS)]
    period = ["--property", GA4_PROPERTY, "--start", start, "--end", end]

    overview_raw = run(base + ["overview"] + period, "GA4 overview")
    sources_raw  = run(base + ["traffic-sources"] + period, "GA4 sources")

    totals = {}
    if overview_raw and overview_raw.get("rows"):
        totals = overview_raw["rows"][0]

    sessions    = fmt_int(totals.get("sessions", 0))
    users       = fmt_int(totals.get("totalUsers", 0))
    new_users   = fmt_int(totals.get("newUsers", 0))
    pageviews   = fmt_int(totals.get("screenPageViews", 0))
    bounce      = fmt_pct(float(totals.get("bounceRate", 0)) * 100)
    duration_s  = float(totals.get("averageSessionDuration", 0))
    duration    = f"{int(duration_s//60)}m {int(duration_s%60)}s"
    events      = fmt_int(totals.get("eventCount", 0))
    conversions = fmt_int(totals.get("conversions", 0))

    sources = []
    if sources_raw and sources_raw.get("rows"):
        total_s = sum(int(r.get("sessions", 0)) for r in sources_raw["rows"])
        for r in sources_raw["rows"][:20]:
            s = fmt_int(r.get("sessions", 0))
            sources.append({
                "source":  r.get("sessionSource", "—"),
                "medium":  r.get("sessionMedium", "—"),
                "sessions": s,
                "pct":     round(s / total_s * 100, 1) if total_s else 0,
            })

    return {
        "sessions":    sessions,
        "users":       users,
        "new_users":   new_users,
        "pageviews":   pageviews,
        "bounce_rate": bounce,
        "duration":    duration,
        "events":      events,
        "conversions": conversions,
        "sources":     sources,
    }

# ─── Main ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Coleta dados para o dashboard do Açougueiro")
    parser.add_argument("--start",  default="", help="YYYY-MM-DD")
    parser.add_argument("--end",    default="", help="YYYY-MM-DD")
    parser.add_argument("--preset", default="last_month",
                        choices=["last_month","this_month","last_7d","last_30d"])
    args = parser.parse_args()

    # Resolve datas
    today = date.today()
    if args.start and args.end:
        start, end = args.start, args.end
    elif args.preset == "last_month":
        first = today.replace(day=1)
        last_m_end = first - timedelta(days=1)
        start = last_m_end.replace(day=1).isoformat()
        end   = last_m_end.isoformat()
    elif args.preset == "this_month":
        start = today.replace(day=1).isoformat()
        end   = today.isoformat()
    elif args.preset == "last_7d":
        start = (today - timedelta(days=7)).isoformat()
        end   = today.isoformat()
    else:  # last_30d
        start = (today - timedelta(days=30)).isoformat()
        end   = today.isoformat()

    print(f"\n📅 Período: {start} → {end}\n", flush=True)

    meta   = fetch_meta(start, end)
    google = fetch_google_ads(start, end)
    ga4    = fetch_ga4(start, end)

    data = {
        "cliente":   "Bar do Açougueiro — Água Verde",
        "periodo":   {"start": start, "end": end},
        "gerado_em": datetime.now().isoformat(),
        "consolidado": {
            "spend":       round(meta["spend"] + google["spend"], 2),
            "reach":       meta["reach"],
            "impressions": meta["impressions"] + google["impressions"],
            "clicks":      meta["clicks"] + google["clicks"],
            "meta_spend":  meta["spend"],
            "google_spend":google["spend"],
        },
        "meta":   meta,
        "google": google,
        "ga4":    ga4,
    }

    out_path = OUT_DIR / "data.json"
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(data, ensure_ascii=False, indent=2))

    print(f"\n✅ data.json salvo em {out_path}")
    print(f"   Meta spend:   R$ {meta['spend']}")
    print(f"   Google spend: R$ {google['spend']}")
    print(f"   GA4 sessões:  {ga4['sessions']}")

if __name__ == "__main__":
    main()
