#!/usr/bin/env python3
"""
Compartilha em lote as contas de anúncio dos clientes com o BM raulriccopro (parceiro).

Usa um token de USUÁRIO temporário (do perfil do Raul, admin dos BMs dos clientes),
lido de ~/.claude/skills/meta-ads-ratos/.user-token e APAGADO ao final.

Uso:
  python3 compartilhar-contas-meta.py           # simula (não altera nada)
  python3 compartilhar-contas-meta.py --executar
"""
import json, os, re, sys, urllib.parse, urllib.request, urllib.error
from pathlib import Path

BM_AGENCIA = "2228834844139201"  # raulriccopro
API = "https://graph.facebook.com/v21.0"
TOKEN_FILE = Path.home() / ".claude/skills/meta-ads-ratos/.user-token"
LISTA = Path(__file__).with_name("contas-meta-compartilhar.md")
TAREFAS = ["MANAGE", "ADVERTISE", "ANALYZE"]


def chamar(metodo, caminho, params):
    data = urllib.parse.urlencode(params).encode()
    url = f"{API}/{caminho}"
    if metodo == "GET":
        url, data = f"{url}?{data.decode()}", None
    try:
        with urllib.request.urlopen(urllib.request.Request(url, data=data, method=metodo), timeout=30) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}")


def main():
    executar = "--executar" in sys.argv
    if not TOKEN_FILE.is_file():
        sys.exit(f"Token de usuário não encontrado em {TOKEN_FILE}")
    token = TOKEN_FILE.read_text().strip()

    contas = re.findall(r"\| \[ \] \| (.+?) \| (\d+) \|", LISTA.read_text(encoding="utf-8"))
    print(f"{len(contas)} contas pendentes — modo {'EXECUTAR' if executar else 'SIMULAÇÃO'}\n")

    ok, falhas = [], []
    for nome, cid in contas:
        info = chamar("GET", f"act_{cid}", {"fields": "name,business{id,name}", "access_token": token})
        if "error" in info:
            falhas.append((nome, cid, "sem acesso: " + info["error"].get("message", "")[:90]))
            print(f"  ✗ {nome}: sem acesso à conta")
            continue
        dono = (info.get("business") or {}).get("name", "sem BM (perfil pessoal)")
        if not executar:
            print(f"  · {nome} — dono: {dono}")
            continue
        r = chamar("POST", f"act_{cid}/agencies", {
            "business": BM_AGENCIA,
            "permitted_tasks": json.dumps(TAREFAS),
            "access_token": token,
        })
        if r.get("success") or ("error" not in r and r):
            ok.append((nome, cid))
            print(f"  ✓ {nome}")
        else:
            msg = r.get("error", {}).get("error_user_msg") or r.get("error", {}).get("message", "erro")
            falhas.append((nome, cid, msg[:120]))
            print(f"  ✗ {nome}: {msg[:120]}")

    if executar:
        txt = LISTA.read_text(encoding="utf-8")
        for nome, cid in ok:
            txt = txt.replace(f"| [ ] | {nome} | {cid} |", f"| [x] | {nome} | {cid} |")
        LISTA.write_text(txt, encoding="utf-8")
        TOKEN_FILE.unlink()
        print(f"\n{len(ok)} compartilhadas, {len(falhas)} com falha. Token temporário apagado.")
    if falhas:
        print("\nFalhas:")
        for nome, cid, msg in falhas:
            print(f"  - {nome} ({cid}): {msg}")


if __name__ == "__main__":
    main()
