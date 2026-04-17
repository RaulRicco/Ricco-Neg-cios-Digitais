---
name: auditoria-gmb
description: >
  Analisa o perfil do Google Meu Negócio de um cliente, mapeia os principais concorrentes
  e gera um plano de ação priorizado para rankear entre os primeiros no Map Pack e nas
  buscas com IA. Baseado na metodologia do Sterling Sky.
  Use quando o usuário disser "analisa o GMB de [cliente]", "auditoria Google Meu Negócio",
  "plano de ação GMB [cliente]", "como rankeamos melhor no Google Maps".
---

# /auditoria-gmb — Auditoria e Plano de Ação para Google Meu Negócio

## Base metodológica

Baseado na metodologia de SEO local do Sterling Sky (sterlingsky.ca), referência em testes
de fatores de ranking do Google Business Profile.

Fatores de ranking confirmados por testes:
- Completude e precisão do perfil (nome, categoria, endereço, horários, serviços)
- Serviços listados com granularidade impactam ranking direto em 24-72h
- Reviews: volume, frequência, rating e palavras-chave nas avaliações
- Fotos e conteúdo visual ativo
- Consistência de NAP entre GBP, site e diretórios (essencial para IA)
- Autoridade de entidade: Google e IAs privilegiam dados verificados e consistentes

---

## Dependências

- **Lista de clientes:** `clientes/lista-clientes.md`
- **Pasta do cliente:** `clientes/[nome-cliente]/`
- **Preferências:** `_contexto/preferencias.md`
- **Ferramentas:** WebSearch e WebFetch para buscar perfil e concorrentes

---

## Workflow

### Passo 1 — Identificar o cliente e a unidade

Perguntar: "Auditoria pra qual cliente? Se tiver mais de uma unidade, qual delas?"

Ler `clientes/lista-clientes.md` e coletar:
- Segmento exato
- Bairro e cidade
- Palavras-chave já mapeadas
- URL do site (se existir)

Se o cliente não tiver Google Meu Negócio listado, avisar e perguntar se quer continuar mesmo assim.

### Passo 2 — Localizar o perfil do cliente

Usar WebSearch para encontrar o perfil GBP do cliente:
- Buscar: `"[nome do cliente]" "[cidade]" site:google.com/maps OR "google.com/maps"`
- Ou buscar diretamente: `"[nome do cliente]" "[bairro]" "[cidade]"`

Se o usuário souber a URL do perfil, pedir pra fornecer para ir mais rápido.

Usar WebFetch no perfil encontrado para coletar dados visíveis:
- Categoria principal
- Categorias secundárias (se visíveis)
- Serviços listados
- Quantidade de fotos
- Quantidade e nota média de reviews
- Se tem posts recentes
- Se tem Q&A respondida
- Horários de funcionamento
- Se o perfil está verificado

### Passo 3 — Mapear os concorrentes

Usar WebSearch com as palavras-chave principais do cliente:
- Buscar: `"[palavra-chave principal]" "[bairro]" "[cidade]"` — ex: "bar na Savassi Belo Horizonte"
- Buscar também: `"[categoria]" "[cidade]"` — ex: "bar Belo Horizonte"

Identificar os top 3 a 5 concorrentes que aparecem no Map Pack para essas buscas.

Para cada concorrente, usar WebFetch ou WebSearch para coletar:
- Categoria principal
- Quantidade de reviews e nota
- Se tem site linkado
- Quantidade de fotos (aproximada)
- Se tem posts ativos
- Serviços listados (se visíveis)

Montar uma tabela comparativa simples:

```
| Critério            | [Cliente] | Concorrente 1 | Concorrente 2 | Concorrente 3 |
|---------------------|-----------|---------------|---------------|---------------|
| Categoria principal | ...       | ...           | ...           | ...           |
| Reviews (qtd)       | ...       | ...           | ...           | ...           |
| Nota média          | ...       | ...           | ...           | ...           |
| Fotos (aprox)       | ...       | ...           | ...           | ...           |
| Posts ativos        | sim/não   | sim/não       | sim/não       | sim/não       |
| Site linkado        | sim/não   | sim/não       | sim/não       | sim/não       |
| Serviços listados   | sim/não   | sim/não       | sim/não       | sim/não       |
```

### Passo 4 — Auditoria completa do perfil do cliente

Verificar cada item do checklist. Marcar como OK, Incompleto ou Ausente.

**Bloco 1 — Informações básicas (NAP + identidade)**
- [ ] Nome do negócio está correto e sem keyword stuffing artificial
- [ ] Categoria primária reflete o core do negócio com precisão
- [ ] Categorias secundárias adicionadas (ex: bar + restaurante + happy hour)
- [ ] Endereço completo e correto
- [ ] Telefone atualizado
- [ ] Site linkado e funcionando
- [ ] Horários de funcionamento completos e atualizados (incluindo feriados)
- [ ] Atributos relevantes preenchidos (aceita cartão, wifi, acessível, etc.)

**Bloco 2 — Conteúdo e otimização**
- [ ] Descrição do perfil criada e otimizada (usar `/descricao-gmb` se não tiver)
- [ ] Serviços listados com especificidade (não apenas "bar", mas "chopp", "petiscos", "happy hour", "drinques")
- [ ] Produtos adicionados (se aplicável)
- [ ] Fotos de qualidade (mínimo recomendado: 10 fotos — ambiente, produtos, fachada)
- [ ] Vídeo no perfil (diferencial crescente em 2025-2026)
- [ ] Posts publicados nos últimos 30 dias

**Bloco 3 — Reputação e engajamento**
- [ ] Quantidade de reviews (comparar com concorrentes)
- [ ] Nota média (meta: acima de 4.3)
- [ ] Reviews recentes (últimos 30 dias)
- [ ] Todas as reviews respondidas (ou pelo menos as negativas)
- [ ] Palavras-chave aparecem naturalmente nas reviews
- [ ] Seção de Q&A: perguntas frequentes respondidas

**Bloco 4 — Consistência e autoridade de entidade**
- [ ] NAP no site é idêntico ao do GBP (nome, endereço, telefone exatos)
- [ ] Schema markup LocalBusiness no site
- [ ] Negócio listado nos principais diretórios (Google, Yelp, TripAdvisor, Foursquare, iFood se aplicável)
- [ ] Informações consistentes entre todas as plataformas
- [ ] Sem perfis duplicados no Google Maps

**Bloco 5 — Sinais para IA (AI Overviews e Ask Maps)**
- [ ] Dados estruturados e consistentes em todas as fontes públicas
- [ ] Site com conteúdo que confirma e expande o que está no GBP
- [ ] Reviews mencionam serviços específicos e localização (sinais de entidade)

### Passo 5 — Gerar o plano de ação

Com base na auditoria e na comparação com concorrentes, montar o plano de ação em 3 níveis.

**Nível 1 — Quick Wins (fazer esta semana)**
Itens ausentes ou incompletos que têm impacto imediato e são fáceis de executar.
Exemplos típicos:
- Completar categorias secundárias
- Adicionar serviços específicos (impacto em 24-72h confirmado por testes)
- Atualizar horários
- Adicionar atributos
- Criar ou otimizar a descrição com `/descricao-gmb`

**Nível 2 — Médio prazo (próximas 4 semanas)**
Ações que exigem consistência ou conteúdo.
Exemplos típicos:
- Campanha de coleta de reviews (pedir pra clientes satisfeitos avaliarem)
- Publicar posts semanais no GMB com `/post-gmb`
- Adicionar pelo menos 10 fotos de qualidade
- Responder todas as reviews em aberto
- Criar Q&A com perguntas frequentes

**Nível 3 — Longo prazo (próximos 3 meses)**
Ações estruturais que constroem autoridade.
Exemplos típicos:
- Corrigir e padronizar NAP em todos os diretórios
- Implementar schema markup LocalBusiness no site
- Estratégia contínua de reviews (meta mensal)
- Monitorar e responder ao Ask Maps (quando disponível no BR)
- Adicionar vídeo ao perfil

### Passo 6 — Resumo executivo

Entregar no final:

```
RESUMO — AUDITORIA GMB [Nome do Cliente] ([Unidade])
Data: [data]

SITUACAO ATUAL
Posicao estimada para "[palavra-chave principal]": [aparece / nao aparece / posicao X]
Maior gap vs. concorrentes: [o que os concorrentes tem que o cliente nao tem]

PONTUACAO DO PERFIL
Informacoes basicas:  [X/8 itens OK]
Conteudo:             [X/7 itens OK]
Reputacao:            [X/6 itens OK]
Consistencia/IA:      [X/5 itens OK]

PRIORIDADE MAXIMA
[Top 3 acoes com maior impacto esperado]

PROXIMO PASSO
[Acao mais urgente e como executar]
```

---

## Regras

- Nunca inventar dados do perfil — só reportar o que foi encontrado via busca
- Se não conseguir acessar o perfil do cliente, pedir que o usuário forneça as informações manualmente
- Categorização precisa: usar o segmento exato do cliente, não termos genéricos
- Comparação de concorrentes deve ser factual, sem julgamento de qualidade subjetivo
- Plano de ação deve ser acionável: cada item tem um responsável implícito e uma ação concreta, não uma sugestão vaga
- Se o cliente tiver múltiplas unidades, gerar auditoria separada por unidade
- Ao identificar que o cliente precisa de descrição otimizada, indicar: "rodar `/descricao-gmb` para esse cliente"
- Ao identificar que o cliente precisa de posts, indicar: "rodar `/post-gmb` para esse cliente"
