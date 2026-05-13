#!/usr/bin/env python3
"""
Coleta métricas do Google Business Profile para o Bar do Açougueiro — Água Verde.

Pré-requisito: rodar auth_gmb.py uma vez para gerar gmb_token.txt.

Uso:
  python3 fetch_gmb.py --start 2026-04-01 --end 2026-04-30
  python3 fetch_gmb.py  (usa last_month por padrão)

Retorna JSON com:
  - visitas ao perfil (BUSINESS_IMPRESSIONS_DESKTOP + MOBILE)
  - rotas solicitadas (BUSINESS_DIRECTION_REQUESTS)
  - cliques no site (WEBSITE_CLICKS)
  - chamadas (CALL_CLICKS)
  - avaliações do mês (via My Business Reviews API)
  - nota atual
"""

import argparse, json, os, sys, urllib.parse, urllib.request
from datetime import date, timedelta

SCRIPT_DIR    = os.path.dirname(os.path.abspath(__file__))
TOKEN_FILE    = os.path.join(SCRIPT_DIR, "gmb_token.txt")
GADS_ENV      = os.path.expanduser("~/.claude/skills/google-ads-ratos/.env")

# Location Name do Açougueiro Água Verde
# Formato: locations/XXXXXXXXXXXXXXXXX
# Será descoberto automaticamente na primeira execução
LOCATION_NAME_FILE = os.path.join(SCRIPT_DIR, "location_name.txt")

def load_env(path):
    env = {}
    if not os.path.isfile(path): return env
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                env[k.strip()] = v.strip().strip('"')
    return env

def get_access_token():
    if not os.path.isfile(TOKEN_FILE):
        print("❌ gmb_token.txt não encontrado. Rode auth_gmb.py primeiro.")
        sys.exit(1)

    refresh_token = open(TOKEN_FILE).read().strip()
    env = load_env(GADS_ENV)
    client_id     = env.get("GOOGLE_ADS_CLIENT_ID", "")
    client_secret = env.get("GOOGLE_ADS_CLIENT_SECRET", "")

    data = urllib.parse.urlencode({
        "client_id":     client_id,
        "client_secret": client_secret,
        "refresh_token": refresh_token,
        "grant_type":    "refresh_token",
    }).encode()

    req  = urllib.request.Request("https://oauth2.googleapis.com/token", data=data)
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read()).get("access_token", "")

def api_get(url, token):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP {e.code} em {url}: {e.read().decode()[:300]}")
        return {}

def api_post(url, body, token):
    data = json.dumps(body).encode()
    req  = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json",
    })
    try:
        resp = urllib.request.urlopen(req)
        return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP {e.code} em {url}: {e.read().decode()[:300]}")
        return {}

def discover_location(token):
    """Descobre o location name do Açougueiro Água Verde e salva localmente."""
    if os.path.isfile(LOCATION_NAME_FILE):
        return open(LOCATION_NAME_FILE).read().strip()

    print("🔍 Descobrindo location name do Açougueiro Água Verde...")

    # Lista contas GMB
    accounts = api_get(
        "https://mybusinessaccountmanagement.googleapis.com/v1/accounts",
        token
    )
    if not accounts.get("accounts"):
        print("❌ Nenhuma conta GMB encontrada.")
        sys.exit(1)

    account_name = accounts["accounts"][0]["name"]
    print(f"   Conta: {account_name}")

    # Lista locations
    locations = api_get(
        f"https://mybusinessbusinessinformation.googleapis.com/v1/{account_name}/locations"
        "?readMask=name,title,storefrontAddress",
        token
    )

    locs = locations.get("locations", [])
    if not locs:
        print("❌ Nenhuma localização encontrada.")
        sys.exit(1)

    print("\n   Localizações disponíveis:")
    for i, loc in enumerate(locs):
        addr = loc.get("storefrontAddress", {})
        city = addr.get("locality", "")
        print(f"   [{i}] {loc.get('title','')} — {city} ({loc['name']})")

    # Tenta encontrar Água Verde automaticamente
    target = None
    for loc in locs:
        title = loc.get("title", "").lower()
        addr  = str(loc.get("storefrontAddress", "")).lower()
        if "água verde" in title or "agua verde" in title or "água verde" in addr or "agua verde" in addr:
            target = loc
            break

    if not target:
        # Pega a primeira se não encontrar
        idx = int(input("\n   Qual índice usar? "))
        target = locs[idx]

    location_name = target["name"]
    print(f"\n   ✅ Usando: {target.get('title','')} ({location_name})")
    open(LOCATION_NAME_FILE, "w").write(location_name)
    return location_name

def fetch_performance(location_name, start, end, token):
    """Busca métricas de performance via Business Profile Performance API."""

    # Converte datas
    s = date.fromisoformat(start)
    e = date.fromisoformat(end)

    url = f"https://businessprofileperformance.googleapis.com/v1/{location_name}:fetchMultiDailyMetricsTimeSeries"
    params = urllib.parse.urlencode({
        "dailyMetrics": [
            "BUSINESS_IMPRESSIONS_DESKTOP_MAPS",
            "BUSINESS_IMPRESSIONS_DESKTOP_SEARCH",
            "BUSINESS_IMPRESSIONS_MOBILE_MAPS",
            "BUSINESS_IMPRESSIONS_MOBILE_SEARCH",
            "BUSINESS_DIRECTION_REQUESTS",
            "WEBSITE_CLICKS",
            "CALL_CLICKS",
        ],
        "dailyRange.startDate.year":  s.year,
        "dailyRange.startDate.month": s.month,
        "dailyRange.startDate.day":   s.day,
        "dailyRange.endDate.year":    e.year,
        "dailyRange.endDate.month":   e.month,
        "dailyRange.endDate.day":     e.day,
    }, doseq=True)

    data = api_get(f"{url}?{params}", token)

    totals = {
        "impressions_maps_desktop":   0,
        "impressions_search_desktop": 0,
        "impressions_maps_mobile":    0,
        "impressions_search_mobile":  0,
        "directions":                 0,
        "website_clicks":             0,
        "call_clicks":                0,
    }

    metric_map = {
        "BUSINESS_IMPRESSIONS_DESKTOP_MAPS":    "impressions_maps_desktop",
        "BUSINESS_IMPRESSIONS_DESKTOP_SEARCH":  "impressions_search_desktop",
        "BUSINESS_IMPRESSIONS_MOBILE_MAPS":     "impressions_maps_mobile",
        "BUSINESS_IMPRESSIONS_MOBILE_SEARCH":   "impressions_search_mobile",
        "BUSINESS_DIRECTION_REQUESTS":          "directions",
        "WEBSITE_CLICKS":                       "website_clicks",
        "CALL_CLICKS":                          "call_clicks",
    }

    for series in data.get("multiDailyMetricTimeSeries", []):
        for item in series.get("dailyMetricTimeSeries", []):
            metric_key = metric_map.get(item.get("dailyMetric", ""))
            if not metric_key: continue
            for point in item.get("timeSeries", {}).get("datedValues", []):
                totals[metric_key] += int(point.get("value", 0) or 0)

    totals["impressions_total"] = (
        totals["impressions_maps_desktop"] +
        totals["impressions_search_desktop"] +
        totals["impressions_maps_mobile"] +
        totals["impressions_search_mobile"]
    )

    return totals

def fetch_reviews(location_name, start, end, token):
    """Busca avaliações do período usando a API de reviews."""
    s = date.fromisoformat(start)
    e = date.fromisoformat(end)

    reviews_total = 0
    avg_rating    = 0.0
    total_reviews = 0
    monthly_reviews = []
    page_token = ""

    # Paginação
    for _ in range(10):  # máx 10 páginas
        url = (f"https://mybusiness.googleapis.com/v4/{location_name}/reviews"
               f"?pageSize=50" + (f"&pageToken={page_token}" if page_token else ""))
        data = api_get(url, token)

        if not data and not data.get("reviews"):
            break

        avg_rating    = float(data.get("averageRating", 0))
        total_reviews = int(data.get("totalReviewCount", 0))

        for review in data.get("reviews", []):
            create_time = review.get("createTime", "")
            try:
                review_date = date.fromisoformat(create_time[:10])
                if s <= review_date <= e:
                    reviews_total += 1
                    monthly_reviews.append({
                        "author":  review.get("reviewer", {}).get("displayName", "Anônimo"),
                        "rating":  review.get("starRating", "FIVE"),
                        "text":    review.get("comment", ""),
                        "date":    review_date.strftime("%d/%m/%Y"),
                        "replied": bool(review.get("reviewReply")),
                    })
            except Exception:
                pass

        page_token = data.get("nextPageToken", "")
        if not page_token:
            break

    # Converte rating string para número
    rating_map = {"ONE":1,"TWO":2,"THREE":3,"FOUR":4,"FIVE":5}
    for r in monthly_reviews:
        r["stars"] = rating_map.get(r["rating"], 5)
        r.pop("rating")

    # Ordena por data (mais recentes primeiro)
    monthly_reviews.sort(key=lambda x: x["date"], reverse=True)

    return {
        "total_accumulated": total_reviews,
        "avg_rating":        round(avg_rating, 1),
        "month_count":       reviews_total,
        "reviews":           monthly_reviews[:10],  # máx 10 no dashboard
    }

def main():
    parser = argparse.ArgumentParser(description="Coleta GMB para o Açougueiro Água Verde")
    parser.add_argument("--start",  default="")
    parser.add_argument("--end",    default="")
    parser.add_argument("--preset", default="last_month",
                        choices=["last_month","this_month","last_7d","last_30d"])
    args = parser.parse_args()

    today = date.today()
    if args.start and args.end:
        start, end = args.start, args.end
    elif args.preset == "last_month":
        first = today.replace(day=1)
        last_end = first - timedelta(days=1)
        start = last_end.replace(day=1).isoformat()
        end   = last_end.isoformat()
    elif args.preset == "this_month":
        start = today.replace(day=1).isoformat()
        end   = today.isoformat()
    elif args.preset == "last_7d":
        start = (today - timedelta(days=7)).isoformat()
        end   = today.isoformat()
    else:
        start = (today - timedelta(days=30)).isoformat()
        end   = today.isoformat()

    print(f"\n📅 Período: {start} → {end}\n")

    token = get_access_token()
    location_name = discover_location(token)

    print("📍 Buscando métricas de performance...")
    perf = fetch_performance(location_name, start, end, token)

    print("⭐ Buscando avaliações...")
    reviews = fetch_reviews(location_name, start, end, token)

    result = {
        "periodo": {"start": start, "end": end},
        "visitas":        perf["impressions_total"],
        "rotas":          perf["directions"],
        "cliques_site":   perf["website_clicks"],
        "ligacoes":       perf["call_clicks"],
        "nota":           reviews["avg_rating"],
        "total_avaliacoes_acumulado": reviews["total_accumulated"],
        "avaliacoes_mes": reviews["month_count"],
        "avaliacoes":     reviews["reviews"],
        "breakdown": {
            "impressoes_maps_desktop":   perf["impressions_maps_desktop"],
            "impressoes_search_desktop": perf["impressions_search_desktop"],
            "impressoes_maps_mobile":    perf["impressions_maps_mobile"],
            "impressoes_search_mobile":  perf["impressions_search_mobile"],
        }
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))

    print(f"\n✅ GMB coletado:")
    print(f"   Visitas: {perf['impressions_total']:,}")
    print(f"   Rotas: {perf['directions']:,}")
    print(f"   Cliques site: {perf['website_clicks']:,}")
    print(f"   Avaliações no mês: {reviews['month_count']}")
    print(f"   Nota: {reviews['avg_rating']} ★")

    return result

if __name__ == "__main__":
    main()
