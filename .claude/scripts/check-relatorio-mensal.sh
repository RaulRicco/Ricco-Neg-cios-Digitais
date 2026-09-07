#!/bin/bash
# SessionStart hook: lembra de gerar os relatórios mensais de todos os clientes
# assim que virar o dia 1º (ou depois) e ainda não tiver rodado no mês corrente.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
STATE_FILE="$REPO_DIR/.claude/.ultimo-relatorio-mensal"

DIA_ATUAL="$(date +%-d)"
MES_ANO_ATUAL="$(date +%Y-%m)"

# Só considera a partir do dia 1 (sempre verdadeiro, mas deixa explícito a intenção)
if [ "$DIA_ATUAL" -lt 1 ]; then
  exit 0
fi

ULTIMO_MES_RODADO=""
if [ -f "$STATE_FILE" ]; then
  ULTIMO_MES_RODADO="$(cat "$STATE_FILE" 2>/dev/null || true)"
fi

if [ "$ULTIMO_MES_RODADO" = "$MES_ANO_ATUAL" ]; then
  # Já rodou (ou foi marcado) este mês, não repetir o lembrete.
  exit 0
fi

MES_FECHADO="$(date -v-1m +%m 2>/dev/null || date -d 'last month' +%m)"
ANO_MES_FECHADO="$(date -v-1m +%Y 2>/dev/null || date -d 'last month' +%Y)"

MESES_PT=(Janeiro Fevereiro Março Abril Maio Junho Julho Agosto Setembro Outubro Novembro Dezembro)
NOME_MES_FECHADO="${MESES_PT[$((10#$MES_FECHADO - 1))]}"

CONTEXT_MSG="LEMBRETE AUTOMÁTICO (SessionStart): hoje é dia $DIA_ATUAL do mês, e o fechamento mensal de todos os clientes referente ao mês fechado anterior ($NOME_MES_FECHADO/$ANO_MES_FECHADO, período $ANO_MES_FECHADO-$MES_FECHADO-01 a fim do mês) ainda não foi feito neste ciclo. 'Relatório do mês anterior' ou 'atualizar relatórios' cobre DUAS partes distintas — sempre ofereça as duas: (1) Relatórios HTML estáticos em clientes/[cliente]/relatorios/relatorio-[mes]-$ANO_MES_FECHADO.html, puxando dados via API das skills google-ads-ratos e meta-ads-ratos (mês fechado); (2) Dashboards interativos em dashboard-deploy/ — rodar cada script dashboard-deploy/data-fetcher/fetch_*.py com --start $ANO_MES_FECHADO-$MES_FECHADO-01 --end <último dia do mês fechado> (usa ~/.claude/skills/.venv-ads/bin/python3; se der ModuleNotFoundError google.analytics, rodar pip install google-analytics-data nessa venv; se der invalid_grant no GA4, o usuário precisa reautorizar rodando ~/.claude/skills/ga4-ratos/scripts/auth.py interativamente), depois publicar com 'npx wrangler pages deploy ../pages --project-name ricco-dashboards --commit-message \"auto-update $ANO_MES_FECHADO-$MES_FECHADO\" --branch main' dentro de dashboard-deploy/worker. ATENÇÃO: o crontab do sistema (dashboard-deploy/auto-update.sh, dia 1 às 06h) está cadastrado mas nunca gerou log em /tmp/dashboard-update.log — não confiar nele, tratar a atualização como manual nesta sessão. Ao adicionar um cliente novo, também criar o fetch_*.py correspondente e cadastrar em dashboard-deploy/clientes.yaml. Depois de concluir as duas partes (ou se o usuário disser para pular desta vez), rode: echo \"$MES_ANO_ATUAL\" > \"$STATE_FILE\" para não repetir este lembrete no mesmo mês."

jq -n --arg ctx "$CONTEXT_MSG" '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $ctx}}'
