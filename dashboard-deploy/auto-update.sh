#!/usr/bin/env bash
# Atualização mensal automática — roda no dia 01 de cada mês via crontab
# Coleta dados do mês anterior e publica no Cloudflare Pages
#
# Crontab recomendado (dia 01 às 06:00):
#   0 6 1 * * /Users/raulricco/ricco-negocios/dashboard-deploy/auto-update.sh >> /tmp/dashboard-update.log 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DATA_FETCHER="$SCRIPT_DIR/data-fetcher"
PAGES_DIR="$SCRIPT_DIR/pages"
WORKER_DIR="$SCRIPT_DIR/worker"
LOG="[$(date '+%Y-%m-%d %H:%M:%S')]"

echo "$LOG ─── Iniciando atualização mensal do dashboard ───"

# ── 1. Coleta dados (usa last_month por padrão) ──────────────────────────────
echo "$LOG Coletando Meta Ads, Google Ads, GA4..."
python3 "$DATA_FETCHER/fetch_acougueiro.py" --preset last_month

echo "$LOG Dados coletados. JSON salvo em pages/acougueiro-agua-verde/data.json"

# ── 2. Deploy no Cloudflare Pages ────────────────────────────────────────────
echo "$LOG Publicando no Cloudflare Pages..."

cd "$WORKER_DIR"
npx wrangler pages deploy "$PAGES_DIR" \
  --project-name ricco-dashboards \
  --commit-message "auto-update $(date '+%Y-%m')" \
  --branch main

echo "$LOG Deploy concluído."

# ── 3. Deploy do Worker (caso tenha mudado) ──────────────────────────────────
# Descomente se quiser redesployar o worker também:
# npx wrangler deploy

echo "$LOG ─── Atualização concluída com sucesso ───"
