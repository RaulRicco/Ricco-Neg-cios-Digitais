# Ricco Negócios Digitais — Claude Code OS

## O que é esse workspace

Workspace principal de Raul (Ricco Negócios Digitais) — gestão de tráfego pago e marketing digital com foco em comércio local. Usado para agilizar entregas de campanhas, propostas, conteúdo e automações para múltiplos clientes.

**Estrutura de pastas:**
- `clientes/` — uma pasta por cliente com briefing e proposta
- `clientes/_modelo-cliente/` — template base para novos clientes
- `conteudo/` — peças de conteúdo avulsas ou em série
- `dados/` — drop zone para arquivos a analisar (CSV, XLSX, PDF, TXT)
- `tarefas.md` — lista de tarefas e pendências
- `templates/skills/` — templates de skills prontos para personalizar com /mapear
- `templates/ferramentas/catalogo.md` — APIs e ferramentas disponíveis para usar em skills

## Sobre o negócio

Raul é estrategista de tráfego pago e SEO local, atendendo múltiplos clientes externos nos segmentos de bares, restaurantes, pet shops e portais de notícias. Foco geográfico em Belo Horizonte e Curitiba. Coordena devs e parceiros de execução a partir de briefings técnicos.

## O que mais fazemos aqui

- Planejamento e gestão de campanhas Google Ads e Meta Ads
- Otimização de SEO local (Google Business Profile)
- Automação de fluxos de leads (Make, RD Station, Webhooks)
- Copywriting focado em conversão e reputação
- Propostas comerciais e briefings técnicos para clientes

## Clientes e contexto

Atende clientes externos com forte presença em gastronomia e serviços locais. Foco em ROI consistente e previsível. Cada cliente tem pasta própria em `clientes/`.

## Tom de voz

Profissional, analítico e tecnicamente preciso. Preferência por categorização exata de nicho — usar "comida de boteco" em vez de termos genéricos, por exemplo. Sem descrições vagas. Não incluir nomes de parceiros não autorizados em materiais.

## Ferramentas conectadas

- Google Ads
- Meta Ads
- Make (automação)
- RD Station
- Webhooks

---

## Contexto do negócio

No início de toda conversa, ler os seguintes arquivos (se existirem e estiverem configurados):

1. `_contexto/empresa.md` — quem é o usuário, o que faz, como funciona o negócio
2. `_contexto/preferencias.md` — tom de voz, estilo de escrita, o que evitar
3. `_contexto/estrategia.md` — foco atual, prioridades, o que pode esperar

Usar essas informações como base pra qualquer resposta ou decisão. Ao sugerir prioridades, formatos ou abordagens, considerar o foco atual descrito em `estrategia.md`.

Para qualquer tarefa visual (carrossel, proposta, slide, landing page), consultar `marca/design-guide.md` como referência de estilo.

Não é necessário listar o que foi lido nem confirmar a leitura. Apenas usar o contexto naturalmente.

---

## Fluxo de trabalho

Antes de executar qualquer tarefa, verificar se existe uma skill relevante em `.claude/skills/` ou `.claude/commands/`.
Se encontrar, seguir as instruções da skill.
Se não encontrar, executar a tarefa normalmente.

Ao concluir uma tarefa que não tinha skill mas parece repetível (o usuário provavelmente vai pedir de novo no futuro), perguntar:

> "Isso pode virar uma skill pra próxima vez. Quer que eu crie?"

Não perguntar pra tarefas pontuais ou perguntas simples. Só quando o padrão de repetição for claro.

---

## Aprender com correções

Quando o usuário corrigir algo, melhorar uma resposta ou dar uma instrução que parece permanente (frases como "na verdade é assim", "não faça mais isso", "prefiro assim", "sempre que...", "evita...", "da próxima vez..."), perguntar:

> "Quer que eu salve isso pra não precisar repetir?"

Se sim, identificar onde faz mais sentido salvar:

- **Sobre o negócio** (quem são os clientes, como funciona a empresa, serviços, mercado) → adicionar em `_contexto/empresa.md`
- **Sobre preferências e estilo** (tom de voz, formato de resposta, o que evitar, como estruturar textos) → adicionar em `_contexto/preferencias.md`
- **Sobre prioridades e foco atual** (projetos em andamento, metas do momento, prazos importantes, o que é prioridade agora) → adicionar em `_contexto/estrategia.md`
- **Regra de comportamento nessa pasta** (onde salvar arquivos, como nomear, fluxos específicos) → adicionar no próprio `CLAUDE.md`

Salvar com uma linha nova clara, sem reformatar o arquivo inteiro. Confirmar o que foi salvo mostrando a linha adicionada.

Não perguntar se a correção for óbvia de contexto imediato (ex: "na verdade o arquivo se chama X"). Só perguntar quando a informação tiver valor duradouro.

---

## Manter contexto atualizado

Ao terminar uma tarefa que mudou algo relevante no projeto (novo cliente, nova skill, mudança de foco, novo processo, ferramenta instalada, estrutura de pastas alterada), perguntar:

> "Isso mudou algo no teu contexto. Quer que eu atualize os arquivos de memória?"

Se sim, identificar o que precisa atualizar:

- **Novo cliente, serviço, ferramenta, equipe** → `_contexto/empresa.md`
- **Mudança de prioridade ou foco** → `_contexto/estrategia.md`
- **Correção de tom ou estilo** → `_contexto/preferencias.md`
- **Nova pasta, regra de organização, skill criada** → `CLAUDE.md`
- **Mudança visual (cores, fontes, logo)** → `marca/design-guide.md`

Mostrar o que vai mudar antes de salvar. Não reformatar o arquivo inteiro, só adicionar ou editar a linha relevante.

**Quando NÃO perguntar:**
- Tarefas pontuais que não mudam o contexto (ex: escrever um email, criar um post avulso)
- Perguntas simples ou conversas sem ação
- Mudanças que já foram salvas pelo bloco "Aprender com correções"

**Dica:** se não sabe se algo mudou, rode `/atualizar` pra uma varredura completa.

---

## Criação de skills

Quando o usuário pedir pra criar uma nova skill:

1. Verificar se existe um template relevante em `templates/skills/`. Se existir, usar como base e adaptar pro contexto do usuário
2. Perguntar: "Essa skill é específica pra esse projeto ou vai ser útil em qualquer projeto?"
   - Específica desse negócio → salvar em `.claude/skills/nome-da-skill/SKILL.md` (local)
   - Útil em qualquer projeto → salvar em `~/.claude/skills/nome-da-skill/SKILL.md` (global)
3. Ler `_contexto/empresa.md` e `_contexto/preferencias.md` pra calibrar o conteúdo da skill ao contexto do negócio
4. Se a skill precisar de arquivos de apoio (templates, referências, exemplos), criar dentro da pasta da skill
5. Seguir o fluxo da skill-creator nativa do Claude Code

---

## Estrutura de templates

A pasta `templates/` contém modelos prontos pra reutilizar — nunca editar diretamente, sempre copiar:

- `templates/skills/` — templates de skills prontas (carrossel, proposta, slide, etc.). Usar como base ao criar novas skills similares
- `templates/ferramentas/catalogo.md` — catálogo de APIs, CLIs e MCPs disponíveis (Playwright, Cloudflare Pages, etc.). Consultar antes de criar skills que precisem de ferramentas externas
- `templates/perfis/` — exemplos de CLAUDE.md por perfil de negócio (agência, empresa, freelancer, solopreneur). Usar como referência ao customizar este arquivo
- `templates/marca/` — estrutura do design guide. Usar se o usuário precisar resetar ou recriar `marca/design-guide.md`

---

## Pasta dados/

`dados/` é uma drop zone para arquivos que o usuário quer analisar (CSV, XLSX, TXT, PDF). Usar com `/analisar-dados dados/nome-do-arquivo`. Útil quando não há MCP de Google Drive configurado.

---

## Relatório de tráfego de todos os clientes (via API, sem CSV)

Para atualizar o relatório mensal de performance de vários/todos os clientes de uma vez, preferir puxar os dados direto via API (skills `google-ads-ratos` e `meta-ads-ratos`) em vez de pedir CSV manual — é mais rápido para o volume de 20+ clientes.

**Ambiente Python:** o Python do sistema (Homebrew) bloqueia `pip install` (PEP 668). Existe uma venv dedicada em `~/.claude/skills/.venv-ads` com `google-ads`, `facebook-business`, `protobuf` e `google-auth-oauthlib` instalados — sempre rodar os scripts dessas skills com `~/.claude/skills/.venv-ads/bin/python3` em vez do `python3` do sistema.

**Contas cadastradas:** `~/.claude/skills/google-ads-ratos/contas.yaml` (15 contas) e `~/.claude/skills/meta-ads-ratos/contas.yaml` (29 contas) já têm o mapeamento cliente → customer_id / conta de anúncio.

**Período do relatório:** usar mês fechado (ex: `--since 2026-08-01 --until 2026-08-31`), não `LAST_30_DAYS` — o relatório é sempre do mês calendário completo, não dos últimos 30 dias corridos.

**Quebra por campanha na Meta:** `insights.py campaign --id <id>` espera o ID de UMA campanha específica. Para listar todas as campanhas de uma conta com métricas, usar `insights.py account --id act_XXX --level campaign --fields campaign_name,spend,...`.

**Google Ads token expira periodicamente** — se der `invalid_grant`, rodar `~/.claude/skills/.venv-ads/bin/python3 setup.py oauth` dentro de `~/.claude/skills/google-ads-ratos/scripts/` para gerar um novo refresh token (abre o browser).

**Padrão de nomenclatura de pastas de cliente:** alguns clientes agrupam múltiplas unidades numa pasta só (ex: `porks-asas` = Asa Norte + Asa Sul; `porks-bdf` = Samambaia + Guará + Pirenópolis) — somar as métricas das contas de anúncio correspondentes antes de gerar o relatório único.

**Formato do relatório:** seguir o HTML dark/verde neon já usado em `clientes/[cliente]/relatorios/relatorio-[mes]-2026.html` (ver qualquer relatório existente como referência de estrutura/CSS).

---

## Auto-sync

Este projeto tem um hook configurado em `.claude/settings.json` que faz commit e push automático ao final de cada sessão (quando o Claude para). O comportamento é silencioso — não precisa avisar o usuário. Se o repositório remoto ainda não estiver configurado, o hook simplesmente não faz nada.
