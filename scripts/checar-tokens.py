#!/usr/bin/env python3
"""
Vigia diário das credenciais de API (Google Ads, GA4, Meta Ads).

Testa cada credencial sem gastar cota, grava log e manda notificação no macOS
quando algo quebrou ou está perto de expirar.

Uso:  python3 checar-tokens.py            # checa e notifica só se tiver problema
      python3 checar-tokens.py --sempre   # notifica mesmo se tudo OK
Log:  ~/Library/Logs/ricco-tokens.log
"""
import json, os, subprocess, sys, urllib.parse, urllib.request, urllib.error
from datetime import datetime
from pathlib import Path

SKILLS = Path.home() / ".claude/skills"
LOG = Path.home() / "Library/Logs/ricco-tokens.log"
AVISO_DIAS = 10  # avisa quando faltar menos que isso para expirar


def ler_env(path):
    env = {}
    if not path.is_file():
        return env
    for linha in path.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        k, v = linha.split("=", 1)
        env[k.strip()] = v.strip().strip('"').strip("'")
    return env


def http(url, data=None):
    body = urllib.parse.urlencode(data).encode() if data else None
    try:
        with urllib.request.urlopen(url, data=body, timeout=30) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read())
        except Exception:
            return e.code, {}


def testar_refresh(client_id, secret, refresh):
    status, resp = http("https://oauth2.googleapis.com/token", {
        "client_id": client_id, "client_secret": secret,
        "refresh_token": refresh, "grant_type": "refresh_token",
    })
    if status == 200 and "access_token" in resp:
        return True, "refresh token OK"
    return False, f"{resp.get('error', status)}: {resp.get('error_description', '')}".strip()


def checar_google_ads():
    env = ler_env(SKILLS / "google-ads-ratos/.env")
    faltando = [k for k in ("GOOGLE_ADS_CLIENT_ID", "GOOGLE_ADS_CLIENT_SECRET",
                            "GOOGLE_ADS_REFRESH_TOKEN", "GOOGLE_ADS_DEVELOPER_TOKEN") if not env.get(k)]
    if faltando:
        return "ERRO", f"faltando no .env: {', '.join(faltando)}"
    ok, msg = testar_refresh(env["GOOGLE_ADS_CLIENT_ID"], env["GOOGLE_ADS_CLIENT_SECRET"],
                             env["GOOGLE_ADS_REFRESH_TOKEN"])
    if ok:
        return "OK", msg
    return "ERRO", msg + " → rodar setup.py oauth (google-ads-ratos)"


def checar_ga4():
    env = ler_env(SKILLS / "ga4-ratos/.env")
    gads = ler_env(SKILLS / "google-ads-ratos/.env")
    sa = env.get("GA4_CREDENTIALS_PATH")
    if sa:
        p = Path(os.path.expanduser(sa))
        if not p.is_file():
            return "ERRO", f"Service Account não encontrada em {p}"
        try:
            info = json.loads(p.read_text())
            return "OK", f"Service Account {info.get('client_email', '?')} (não expira)"
        except Exception as e:
            return "ERRO", f"JSON da Service Account inválido: {e}"
    refresh = env.get("GA4_REFRESH_TOKEN") or gads.get("GOOGLE_ADS_REFRESH_TOKEN")
    cid = env.get("GA4_CLIENT_ID") or gads.get("GOOGLE_ADS_CLIENT_ID")
    sec = env.get("GA4_CLIENT_SECRET") or gads.get("GOOGLE_ADS_CLIENT_SECRET")
    if not (refresh and cid and sec):
        return "ERRO", "sem credencial configurada"
    ok, msg = testar_refresh(cid, sec, refresh)
    if ok:
        return "AVISO", "OAuth OK, mas ainda sem Service Account (pode expirar)"
    return "ERRO", msg + " → rodar ga4-ratos/scripts/auth.py ou migrar p/ Service Account"


def checar_meta():
    env = ler_env(SKILLS / "meta-ads-ratos/.env")
    token = env.get("META_ADS_TOKEN")
    if not token:
        return "ERRO", "META_ADS_TOKEN ausente"
    status, resp = http("https://graph.facebook.com/v21.0/debug_token?" +
                        urllib.parse.urlencode({"input_token": token, "access_token": token}))
    if "error" in resp:
        return "ERRO", resp["error"].get("message", "token inválido")[:160]
    d = resp.get("data", {})
    if not d.get("is_valid"):
        return "ERRO", (d.get("error") or {}).get("message", "token inválido")[:160]
    tipo = d.get("type", "?")
    exp = d.get("expires_at", 0)
    if not exp:
        return "OK", f"token {tipo}, não expira"
    dias = (datetime.fromtimestamp(exp) - datetime.now()).days
    nivel = "AVISO" if dias < AVISO_DIAS else "OK"
    sufixo = " → trocar por token de Usuário do Sistema" if tipo != "SYSTEM_USER" else ""
    return nivel, f"token {tipo} expira em {dias} dias ({datetime.fromtimestamp(exp):%d/%m/%Y}){sufixo}"


def notificar(titulo, texto):
    texto = texto.replace('"', "'")
    subprocess.run(["osascript", "-e",
                    f'display notification "{texto}" with title "{titulo}" sound name "Basso"'],
                   check=False, capture_output=True)


def main():
    checks = {"Google Ads": checar_google_ads, "GA4": checar_ga4, "Meta Ads": checar_meta}
    resultados = {}
    for nome, fn in checks.items():
        try:
            resultados[nome] = fn()
        except Exception as e:
            resultados[nome] = ("ERRO", f"falha no teste: {e}")

    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    linhas = [f"[{agora}] {nome:<10} {nivel:<5} {msg}" for nome, (nivel, msg) in resultados.items()]
    print("\n".join(linhas))
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")

    erros = [n for n, (lvl, _) in resultados.items() if lvl == "ERRO"]
    avisos = [n for n, (lvl, _) in resultados.items() if lvl == "AVISO"]
    if erros:
        notificar("⚠️ Token quebrado", f"{', '.join(erros)} parou de funcionar. Ver ~/Library/Logs/ricco-tokens.log")
    elif avisos:
        notificar("Tokens: atenção", f"{', '.join(avisos)}: ver ~/Library/Logs/ricco-tokens.log")
    elif "--sempre" in sys.argv:
        notificar("Tokens OK", "Google Ads, GA4 e Meta funcionando")
    sys.exit(1 if erros else 0)


if __name__ == "__main__":
    main()
