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

CONTEXT_MSG="LEMBRETE AUTOMÁTICO (SessionStart): hoje é dia $DIA_ATUAL do mês, e os relatórios mensais de todos os clientes referentes ao mês fechado anterior ($NOME_MES_FECHADO/$ANO_MES_FECHADO, período $ANO_MES_FECHADO-$MES_FECHADO-01 a fim do mês) ainda não foram gerados neste ciclo. Assim que fizer sentido nesta sessão, pergunte ao usuário se pode gerar/atualizar os relatórios de todos os clientes agora (puxando dados via API das skills google-ads-ratos e meta-ads-ratos, mês fechado, seguindo o padrão de clientes/[cliente]/relatorios/relatorio-[mes]-$ANO_MES_FECHADO.html). Depois de gerar (ou se o usuário disser para pular desta vez), rode: echo \"$MES_ANO_ATUAL\" > \"$STATE_FILE\" para não repetir este lembrete no mesmo mês."

jq -n --arg ctx "$CONTEXT_MSG" '{hookSpecificOutput: {hookEventName: "SessionStart", additionalContext: $ctx}}'
