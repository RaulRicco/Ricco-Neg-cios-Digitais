#!/usr/bin/env python3
"""
Coletor do dashboard v2 — gera pages/<slug>/data.json com:
  - mês do relatório (Meta, Google Ads, GA4) — reaproveita as funções de fetch_<slug>.py
  - mês anterior (para as comparações ↑↓)
  - série diária REAL (investimento, cliques, resultados, sessões)
  - config do cliente (dashboard-deploy/config/<slug>.json, opcional)

Uso:
  python3 coletar_v2.py --slug boi-dourado                 # mês fechado anterior
  python3 coletar_v2.py --slug boi-dourado --start 2026-10-01 --end 2026-10-31
  python3 coletar_v2.py --todos                            # todos os clientes de clientes.yaml
  --allow-partial  grava mesmo se alguma API falhar (padrão: não grava)

Rodar com ~/.claude/skills/.venv-ads/bin/python3
"""
import argparse, importlib.util, json, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
FETCH_DIR = ROOT / "data-fetcher"
PAGES = ROOT / "pages"
CFG_DIR = ROOT / "config"
SK = Path.home() / ".claude/skills"
PY = sys.executable
ESPECIAIS = {"acougueiro-agua-verde": "fetch_acougueiro.py"}
# Tipos de resultado da Meta que contam como resultado de negócio (igual ao KIND do template)
RESULTADOS_META = {"Leads", "Mensagens", "Reservas", "Vendas"}


def mes_fechado(ref=None):
    ref = ref or date.today()
    fim = ref.replace(day=1) - timedelta(days=1)
    return fim.replace(day=1), fim


def mes_anterior(start):
    fim = start - timedelta(days=1)
    return fim.replace(day=1), fim


def run_json(args):
    r = subprocess.run([PY] + args, capture_output=True, text=True, timeout=240)
    out = r.stdout
    idx = [p for p in (out.find("["), out.find("{")) if p >= 0]
    if r.returncode != 0 or not idx:
        return None
    try:
        data = json.loads(out[min(idx):])
    except Exception:
        return None
    if isinstance(data, dict) and data.get("error"):
        return None
    return data


def carregar_fetch(slug):
    path = FETCH_DIR / ESPECIAIS.get(slug, f"fetch_{slug.replace('-', '_')}.py")
    spec = importlib.util.spec_from_file_location(f"f_{slug.replace('-', '_')}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    if not hasattr(mod, "FALHAS"):  # scripts antigos: registra falhas envolvendo run()
        mod.FALHAS = []
        orig = mod.run

        def run_registrando(cmd, label="", _orig=orig, _mod=mod):
            d = _orig(cmd, label)
            if d is None or (isinstance(d, dict) and d.get("error")):
                _mod.FALHAS.append(label)
            return d
        mod.run = run_registrando
    return mod


def periodo(mod, servicos, s, e):
    mod.FALHAS.clear()
    tem = lambda svc, const, fn: svc in servicos and getattr(mod, const, "") and hasattr(mod, fn)
    out = {
        "meta": mod.fetch_meta(s, e) if tem("meta", "META_ACCOUNT", "fetch_meta") else None,
        "google": mod.fetch_google_ads(s, e) if tem("google", "GADS_CUSTOMER", "fetch_google_ads") else None,
        "ga4": mod.fetch_ga4(s, e) if tem("ga4", "GA4_PROPERTY", "fetch_ga4") else None,
    }
    return out, list(mod.FALHAS)


def diario(mod, servicos, s, e):
    dias, falhas = {}, []
    cur = datetime.fromisoformat(s).date()
    while cur <= datetime.fromisoformat(e).date():
        k = cur.isoformat()
        dias[k] = {"date": k, "meta_spend": 0.0, "google_spend": 0.0, "clicks": 0, "results": 0.0, "sessions": 0}
        cur += timedelta(days=1)

    if "meta" in servicos and getattr(mod, "META_ACCOUNT", ""):
        # Por campanha e por dia, com a MESMA regra de resultado do total do mês (extract_result do fetch)
        meta = run_json([str(SK / "meta-ads-ratos/scripts/insights.py"), "account", "--account", mod.META_ACCOUNT,
                         "--level", "campaign", "--fields", "spend,clicks,actions,objective,optimization_goal",
                         "--time-increment", "1", "--time-range", json.dumps({"since": s, "until": e}),
                         "--limit", "5000"])
        if meta is None:
            falhas.append("Meta diário")
        for r in meta or []:
            x = dias.get(r.get("date_start"))
            if not x:
                continue
            spend = float(r.get("spend", 0))
            x["meta_spend"] += spend
            x["clicks"] += int(r.get("clicks", 0))
            label, qty, _ = mod.extract_result(r.get("objective", ""), r.get("optimization_goal", ""),
                                               r.get("actions", []), spend)
            if label in RESULTADOS_META:
                x["results"] += qty

    if "google" in servicos and getattr(mod, "GADS_CUSTOMER", ""):
        g = run_json([str(SK / "google-ads-ratos/scripts/insights.py"), "daily", "--customer-id", mod.GADS_CUSTOMER,
                      "--since", s, "--until", e])
        if g is None:
            falhas.append("Google diário")
        for r in g or []:
            x = dias.get((r.get("segments") or {}).get("date"))
            if not x:
                continue
            m = r.get("metrics", {})
            x["google_spend"] += float(m.get("cost", 0) or 0)
            x["clicks"] += int(m.get("clicks", 0) or 0)
            x["results"] += float(m.get("conversions", 0) or 0)

    if "ga4" in servicos and getattr(mod, "GA4_PROPERTY", ""):
        ga = run_json([str(SK / "ga4-ratos/scripts/reports.py"), "daily", "--property", mod.GA4_PROPERTY,
                       "--start-date", s, "--end-date", e])
        if ga is None:
            falhas.append("GA4 diário")
        for r in (ga or {}).get("rows", []):
            k = r["date"]
            x = dias.get(f"{k[:4]}-{k[4:6]}-{k[6:]}")
            if x:
                x["sessions"] += int(r.get("sessions", 0))

    for x in dias.values():
        x["meta_spend"] = round(x["meta_spend"], 2)
        x["google_spend"] = round(x["google_spend"], 2)
        x["results"] = round(x["results"])
    return sorted(dias.values(), key=lambda x: x["date"]), falhas


def coletar(c, start, end, allow_partial=False):
    slug = c["slug"]
    servicos = set(c.get("servicos", []))
    try:
        mod = carregar_fetch(slug)
    except Exception as ex:
        return slug, "ERRO", f"fetch script: {ex}"
    ps, pe = mes_anterior(start)
    s, e = start.isoformat(), end.isoformat()
    atual, f1 = periodo(mod, servicos, s, e)
    anterior, f2 = periodo(mod, servicos, ps.isoformat(), pe.isoformat())
    dia, f3 = diario(mod, servicos, s, e)
    falhas = f1 + f3  # falha no mês anterior só desliga a comparação
    if falhas and not allow_partial:
        return slug, "PULADO", "falhou: " + ", ".join(sorted(set(falhas)))
    cfg_path = CFG_DIR / f"{slug}.json"
    config = json.loads(cfg_path.read_text(encoding="utf-8")) if cfg_path.is_file() else {}
    config.setdefault("nome", c.get("nome", slug))
    out = {
        "versao": 2,
        "cliente": c.get("nome", slug),
        "periodo": {"start": s, "end": e},
        "periodo_anterior": None if f2 else {"start": ps.isoformat(), "end": pe.isoformat()},
        "gerado_em": datetime.now().isoformat(timespec="seconds"),
        **atual,
        "anterior": None if f2 else anterior,
        "diario": dia,
        "config": config,
    }
    (PAGES / slug).mkdir(parents=True, exist_ok=True)
    (PAGES / slug / "data.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    gasto = sum(float((out.get(p) or {}).get("spend", 0) or 0) for p in ("meta", "google"))
    aviso = f" (sem comparação: {', '.join(f2)})" if f2 else ""
    return slug, "OK", f"R$ {gasto:,.2f}{aviso}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", action="append", default=[])
    ap.add_argument("--todos", action="store_true")
    ap.add_argument("--start")
    ap.add_argument("--end")
    ap.add_argument("--allow-partial", action="store_true")
    ap.add_argument("--workers", type=int, default=5)
    a = ap.parse_args()
    if a.start and a.end:
        start, end = date.fromisoformat(a.start), date.fromisoformat(a.end)
    else:
        start, end = mes_fechado()
    clientes = yaml.safe_load((ROOT / "clientes.yaml").read_text())["clientes"]
    if not a.todos:
        clientes = [c for c in clientes if c["slug"] in a.slug]
    if not clientes:
        sys.exit("Nenhum cliente selecionado (use --slug ou --todos)")
    print(f"Período {start} → {end} · {len(clientes)} clientes\n", flush=True)
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        res = list(ex.map(lambda c: coletar(c, start, end, a.allow_partial), clientes))
    for slug, st, msg in sorted(res, key=lambda r: (r[1], r[0])):
        print(f"{st:7} {slug:24} {msg}")
    sys.exit(0 if all(r[1] == "OK" for r in res) else 1)


if __name__ == "__main__":
    main()
