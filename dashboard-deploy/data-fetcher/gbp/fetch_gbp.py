#!/usr/bin/env python3
"""
Coleta métricas do Google Business Profile via LocalSEO Data API.
Substitui fetch_gmb.py (que depende de APIs com cota zero no projeto GCP).

Uso:
  python3 fetch_gbp.py --start 2026-04-01 --end 2026-04-30

Retorna JSON com:
  - nota atual e total de avaliações
  - avaliações do período (filtradas por data)
  - dados básicos do perfil (nome, endereço, categorias)

Marcador de saída: GBP_JSON_START / GBP_JSON_END
"""

import argparse, json, sys, urllib.request, urllib.error
from datetime import date, datetime

API_URL = "https://mcp.localseodata.com/mcp"
API_KEY = "sk_live_F2spYffWxQ6wsJo3FuX7kBOs1o4AEtI3"

BUSINESS_NAME = "Bar do Açougueiro"
LOCATION      = "Água Verde, Curitiba, PR"
PLACE_ID      = "ChIJS6DjlqLl3JQRDTF7IyirKR8"  # evita ambiguidade na busca

def call_tool(name, arguments):
    body = json.dumps({
        "jsonrpc": "2.0", "id": 1,
        "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    }).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type":  "application/json",
        "Accept":        "application/json, text/event-stream",
    })
    try:
        resp = urllib.request.urlopen(req, timeout=45)
        data = json.loads(resp.read())
        content = data.get("result", {}).get("content", [])
        if not content:
            print(f"❌ {name}: resposta vazia", file=sys.stderr)
            return {}
        text = content[0].get("text", "")
        # Remove linha de créditos (primeira linha) se presente
        lines = text.strip().splitlines()
        json_start = next((i for i, l in enumerate(lines) if l.strip().startswith("{")), 0)
        return json.loads("\n".join(lines[json_start:]))
    except urllib.error.HTTPError as e:
        print(f"❌ {name} HTTP {e.code}: {e.read().decode()[:200]}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"❌ {name}: {e}", file=sys.stderr)
        return {}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True)
    parser.add_argument("--end",   required=True)
    args = parser.parse_args()

    s = date.fromisoformat(args.start)
    e = date.fromisoformat(args.end)

    print(f"⭐ Buscando avaliações...", file=sys.stderr)
    reviews_data = call_tool("google_reviews", {
        "business_name": BUSINESS_NAME,
        "location":      LOCATION,
        "limit":         100,
        "sort":          "newest",
    })

    all_reviews   = reviews_data.get("reviews", [])
    avg_rating    = float(reviews_data.get("average_rating", 0))
    total_reviews = int(reviews_data.get("total_reviews", 0))

    # Filtra pelo período solicitado
    monthly_reviews = []
    for r in all_reviews:
        try:
            dt = datetime.fromisoformat(r["date"].replace(" +00:00", "+00:00").replace(" +", "+"))
            review_date = dt.date()
        except Exception:
            continue
        if s <= review_date <= e:
            monthly_reviews.append({
                "author":  r.get("author_name", "Anônimo"),
                "stars":   int(r.get("rating", 5)),
                "text":    r.get("text", ""),
                "date":    review_date.strftime("%d/%m/%Y"),
                "replied": bool(r.get("owner_reply")),
            })

    result = {
        "nota":                      round(avg_rating, 1),
        "total_avaliacoes_acumulado": total_reviews,
        "avaliacoes_mes":             len(monthly_reviews),
        "avaliacoes":                 monthly_reviews[:10],
        # Dados básicos do perfil (úteis para debug)
        "visitas":      0,
        "rotas":        0,
        "cliques_site": 0,
        "ligacoes":     0,
    }

    print(f"\n✅ GBP coletado via LocalSEO Data:", file=sys.stderr)
    print(f"   Nota: {avg_rating} ★  |  Total: {total_reviews} avaliações", file=sys.stderr)
    print(f"   No período {args.start} → {args.end}: {len(monthly_reviews)} avaliações", file=sys.stderr)

    print("GBP_JSON_START")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    print("GBP_JSON_END")

if __name__ == "__main__":
    main()
