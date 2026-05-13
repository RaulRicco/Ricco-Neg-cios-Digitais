#!/usr/bin/env python3
"""
Gera refresh token OAuth2 com escopo Google Business Profile.
Roda uma vez — salva o token em gmb_token.txt para uso pelo fetch_gmb.py.

Uso:
  python3 auth_gmb.py
"""

import hashlib, json, os, re, secrets, socket, sys, webbrowser
import urllib.parse, urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GADS_ENV   = os.path.expanduser("~/.claude/skills/google-ads-ratos/.env")
TOKEN_FILE = os.path.join(SCRIPT_DIR, "gmb_token.txt")

SCOPES = " ".join([
    "https://www.googleapis.com/auth/business.manage",
])

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

def find_free_port(start=8080, end=8090):
    for port in range(start, end + 1):
        try:
            s = socket.socket()
            s.bind(("127.0.0.1", port))
            s.close()
            return port
        except OSError:
            continue
    return None

def main():
    env = load_env(GADS_ENV)
    client_id     = env.get("GOOGLE_ADS_CLIENT_ID", "")
    client_secret = env.get("GOOGLE_ADS_CLIENT_SECRET", "")

    if not client_id or not client_secret:
        print("❌ GOOGLE_ADS_CLIENT_ID / GOOGLE_ADS_CLIENT_SECRET não encontrados.")
        sys.exit(1)

    port = find_free_port()
    if not port:
        print("❌ Nenhuma porta disponível entre 8080-8090.")
        sys.exit(1)

    redirect_uri  = f"http://127.0.0.1:{port}/callback"
    state         = secrets.token_hex(16)
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()
    import base64
    code_challenge_b64 = base64.urlsafe_b64encode(code_challenge).rstrip(b"=").decode()

    auth_url = (
        "https://accounts.google.com/o/oauth2/v2/auth?"
        + urllib.parse.urlencode({
            "client_id":             client_id,
            "redirect_uri":          redirect_uri,
            "response_type":         "code",
            "scope":                 SCOPES,
            "state":                 state,
            "access_type":           "offline",
            "prompt":                "consent",
            "code_challenge":        code_challenge_b64,
            "code_challenge_method": "S256",
        })
    )

    print(f"\n🔐 Abrindo autenticação Google no browser...")
    print(f"   Escopo: business.manage (Google Business Profile)\n")
    webbrowser.open(auth_url)

    # Servidor local para capturar o callback
    import http.server
    auth_code = {}

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            params = dict(urllib.parse.parse_qsl(urllib.parse.urlparse(self.path).query))
            auth_code["code"]  = params.get("code", "")
            auth_code["state"] = params.get("state", "")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h2 style='font-family:sans-serif;color:green'>Autenticado! Pode fechar esta aba.</h2>")
        def log_message(self, *a): pass

    server = http.server.HTTPServer(("127.0.0.1", port), Handler)
    server.handle_request()

    if not auth_code.get("code"):
        print("❌ Código de autorização não recebido.")
        sys.exit(1)
    if auth_code.get("state") != state:
        print("❌ State inválido — possível CSRF.")
        sys.exit(1)

    # Troca code por tokens
    token_data = urllib.parse.urlencode({
        "client_id":     client_id,
        "client_secret": client_secret,
        "code":          auth_code["code"],
        "code_verifier": code_verifier,
        "redirect_uri":  redirect_uri,
        "grant_type":    "authorization_code",
    }).encode()

    req = urllib.request.Request(
        "https://oauth2.googleapis.com/token",
        data=token_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    resp = urllib.request.urlopen(req)
    tokens = json.loads(resp.read())

    refresh_token = tokens.get("refresh_token", "")
    if not refresh_token:
        print("❌ Refresh token não retornado. Tente novamente.")
        sys.exit(1)

    with open(TOKEN_FILE, "w") as f:
        f.write(refresh_token)

    print(f"✅ Refresh token salvo em: {TOKEN_FILE}")
    print(f"   Token: {refresh_token[:20]}...")

if __name__ == "__main__":
    main()
