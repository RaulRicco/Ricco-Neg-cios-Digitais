# Clientes com Dashboard

| Cliente | URL | Senha | Plataformas |
|---|---|---|---|
| Bar do Açougueiro — Água Verde | dash.raulricco.com.br/acougueiro-agua-verde | acougueiro2026 | Meta · Google · GA4 · GMB |

## Adicionar novo cliente

1. Copiar `pages/acougueiro-agua-verde/` → `pages/novo-slug/`
2. Editar `index.html` com nome e dados do cliente
3. Adicionar senha em `worker/index.js` (objeto `CLIENTES`)
4. Adicionar rota em `pages/_redirects`
5. Fazer deploy (ver DEPLOY.md)
