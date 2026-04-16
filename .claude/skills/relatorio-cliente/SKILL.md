---
name: relatorio-cliente
description: >
  Gera relatório mensal de performance em PDF a partir de CSVs exportados das plataformas.
  Lê os dados de Meta Ads, Google Ads, Google Meu Negócio e Analytics e monta relatório visual por cliente.
  Use quando o usuário disser "gera relatório de [cliente]", "relatório mensal [cliente]",
  "faz o relatório com os CSVs de [cliente]".
---

# /relatorio-cliente — Relatório Mensal de Performance

## Dependências

- **Lista de clientes:** `clientes/lista-clientes.md`
- **Design guide:** `marca/design-guide.md`
- **CSVs exportados:** `dados/` (o usuário deve jogar os arquivos aqui antes de rodar)
- **Saída:** `clientes/[nome-cliente]/relatorios/relatorio-[mes-ano].pdf`

---

## Workflow

### Passo 1 — Identificar o cliente e os arquivos

Perguntar: "Relatório de qual cliente e de qual mês?"

Verificar os arquivos disponíveis em `dados/`:
- Listar os CSVs encontrados
- Identificar de qual plataforma cada um é (Meta Ads, Google Ads, GMB, Analytics)
- Confirmar com o usuário: "Encontrei esses arquivos: [lista]. São esses mesmos?"

Se faltar algum arquivo esperado, avisar: "Não encontrei CSV do [plataforma]. Quer gerar o relatório sem esses dados ou vai jogar o arquivo na pasta dados/ antes?"

### Passo 2 — Ler e processar os dados

Ler cada CSV e extrair as métricas relevantes por plataforma:

**Meta Ads:**
- Alcance
- Impressões
- Cliques no link
- CTR
- CPM
- CPC
- Valor gasto
- Resultados (leads, mensagens, compras — conforme objetivo da campanha)
- Custo por resultado
- Campanhas com melhor performance

**Google Ads:**
- Impressões
- Cliques
- CTR
- CPC médio
- Conversões
- Custo por conversão
- Valor gasto total
- Campanhas com melhor performance

**Google Meu Negócio:**
- Visualizações do perfil
- Buscas (diretas e por descoberta)
- Cliques para ligar
- Cliques para site
- Solicitações de rota
- Avaliações (média e total)

**Google Analytics:**
- Sessões
- Usuários
- Taxa de rejeição
- Páginas mais visitadas
- Origem do tráfego (orgânico, pago, direto, referência)
- Conversões (se configurado)

Calcular variações em relação ao mês anterior, se o usuário tiver o CSV do período anterior disponível.

### Passo 3 — Montar o relatório HTML

Gerar um arquivo HTML com visual profissional baseado em `marca/design-guide.md` (dark, verde neon, tipografia bold).

**Estrutura do relatório:**

```
[Capa]
- Logo do cliente (se disponível em clientes/[nome]/logo.*)
- Nome do cliente
- Período: Mês / Ano
- Elaborado por: Ricco Negócios Digitais

[Resumo Executivo]
- Principais números do mês em cards destacados
- 2-3 frases com os destaques e pontos de atenção

[Seção por plataforma]
(uma seção para cada plataforma com dados disponíveis)
- Métricas principais em cards
- Variação em relação ao mês anterior (se disponível)
- Campanha destaque do período

[Conclusão e próximos passos]
- O que funcionou bem
- O que será ajustado no próximo mês
- Ações planejadas

[Rodapé]
- Ricco Negócios Digitais — raulricco.com.br
- Mês/Ano do relatório
```

Salvar o HTML em `clientes/[nome-cliente]/relatorios/relatorio-[mes-ano].html`

### Passo 4 — Gerar o PDF

Usar a skill nativa `/pdf` para converter o HTML em PDF.

Salvar em `clientes/[nome-cliente]/relatorios/relatorio-[mes-ano].pdf`

Confirmar: "Relatório gerado em clientes/[nome-cliente]/relatorios/relatorio-[mes-ano].pdf"

### Passo 5 — Limpar a pasta dados/

Perguntar: "Quer que eu mova os CSVs usados pra dentro da pasta do cliente ou pode apagar da dados/?"

- Se mover: salvar em `clientes/[nome-cliente]/relatorios/dados-[mes-ano]/`
- Se apagar: remover os arquivos de `dados/`

---

## Regras

- Nunca inventar métricas — se o dado não estiver no CSV, deixar em branco com nota "dado não disponível"
- Variações percentuais: só calcular se tiver o período anterior para comparar
- Visual do relatório deve ser limpo e fácil de ler — o cliente não é técnico
- Métricas negativas (ex: CPC subiu) devem aparecer com contexto, não só o número
- O relatório é da Ricco Negócios Digitais para o cliente — manter profissionalismo
- Cada cliente tem serviços diferentes — só incluir seções das plataformas que o cliente usa (consultar lista-clientes.md)
