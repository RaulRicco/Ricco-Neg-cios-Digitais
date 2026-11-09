#!/usr/bin/env python3
"""
Gera pages/<slug>/index.html (dashboard v2) a partir de template/dashboard.html + clientes.yaml.
Os dados ficam em pages/<slug>/data.json (gerado por data-fetcher/coletar_v2.py).

Uso:  python3 gerar_paginas.py              # todos
      python3 gerar_paginas.py --slug boi-dourado
"""
import argparse, hashlib, html
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parent
TPL = (ROOT / "template/dashboard.html").read_text(encoding="utf-8")


def render(c):
    senha = c.get("senha", "ricco2024")
    return (TPL.replace("{{SLUG}}", c["slug"])
               .replace("{{SENHA_HASH}}", hashlib.sha256(senha.encode()).hexdigest())
               .replace("{{NOME}}", html.escape(c["nome"]).replace("'", "&#39;")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", action="append", default=[])
    a = ap.parse_args()
    clientes = yaml.safe_load((ROOT / "clientes.yaml").read_text())["clientes"]
    for c in clientes:
        if a.slug and c["slug"] not in a.slug:
            continue
        d = ROOT / "pages" / c["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(render(c), encoding="utf-8")
        print("✅", c["slug"])


if __name__ == "__main__":
    main()
