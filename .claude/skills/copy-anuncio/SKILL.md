---
name: copy-anuncio
description: >
  Gera copies de anúncio ultra persuasivas para Google Ads e Meta Ads.
  Baseia cada copy no nível de consciência do público (Schwartz), no gancho emocional
  e na multidão faminta (Halbert) e no poder da headline específica (Ogilvy).
  Respeita o tom de voz de cada cliente.
  Use quando o usuário disser "cria a copy do evento X", "faz o texto do anúncio",
  "copy para a campanha de [cliente]", "cria o anúncio de [produto/serviço]".
---

# /copy-anuncio — Copy de Anúncio Ultra Persuasiva

## Base metodológica

Três copywriters fundamentam cada copy gerada por essa skill:

**Eugene Schwartz — Breakthrough Advertising**
Nenhuma copy funciona sem primeiro diagnosticar o nível de consciência do público.
A mensagem muda radicalmente dependendo de onde o prospect está na jornada.
5 níveis: Inconsciente / Consciente do problema / Consciente da solução / Consciente do produto / Mais consciente (pronto pra comprar)

**Gary Halbert — The Boron Letters**
Antes de escrever uma linha, encontre a "multidão faminta": quem já quer o que você oferece e só precisa de uma razão pra agir agora?
A copy não convence — ela amplifica um desejo que já existe.
O gancho emocional precisa aparecer nos primeiros 3 segundos. Se não parar o scroll, o resto não importa.

**David Ogilvy — Confessions of an Advertising Man**
A headline é responsável por 80% do resultado do anúncio.
Especificidade vende. Não "chopp gelado" — "chopp tirado na temperatura certa, em copo de 600ml".
A primeira frase precisa tornar impossível não ler a segunda.

---

## Dependências

- **Tom de voz do cliente:** `clientes/[nome-cliente]/tom-de-voz.md`
- **Contexto geral:** `_contexto/preferencias.md`

---

## Workflow

### Passo 1 — Identificar o cliente e o tom de voz

Perguntar: "Qual é o cliente?"

Buscar `clientes/[nome-cliente]/tom-de-voz.md`.
- Se existir: ler e usar como base de tom e linguagem
- Se não existir: avisar — "Ainda não tenho o tom de voz de [cliente]. Me descreve em 2-3 linhas como ele fala com o público." Após a resposta, salvar em `clientes/[nome-cliente]/tom-de-voz.md`.

### Passo 2 — Coletar os dados do anúncio

Perguntar: "Me passa os dados do que vai ser anunciado — evento, promoção, serviço, produto."

Extrair:
- O que está sendo anunciado (evento, promoção, lançamento, serviço recorrente)
- Data, horário e local (se aplicável)
- Destaque principal: o que é irresistível nisso? (preço, exclusividade, experiência, artista, etc.)
- Link de destino (se houver)
- Plataformas: Meta Ads, Google Ads ou ambas

Se o usuário mandar imagem ou arte, extrair os dados diretamente dela.

### Passo 3 — Diagnosticar o nível de consciência (Schwartz)

Antes de escrever, definir em qual nível de consciência está o público-alvo desse anúncio:

**Nível 1 — Inconsciente:** não sabe que tem o problema ou desejo
*Abordagem: conte uma história, desperte o desejo sem citar o produto*

**Nível 2 — Consciente do problema:** sabe que quer sair, se divertir, comer bem — mas não sabe onde
*Abordagem: reflita o problema/desejo de volta pra ele, mostre que você entende*

**Nível 3 — Consciente da solução:** já sabe que quer um bar, já está pesquisando opções
*Abordagem: apresente o diferencial que te separa das outras opções*

**Nível 4 — Consciente do produto:** já conhece o negócio, só precisa de um motivo pra ir agora
*Abordagem: foco em urgência, novidade, evento específico, oferta*

**Nível 5 — Mais consciente (pronto pra comprar/visitar):** já quer ir, só precisa de um empurrão
*Abordagem: CTA direto, remova fricção, facilite a ação*

Para cada anúncio, identificar o nível predominante do público segmentado e deixar isso explícito antes de gerar as copies.

### Passo 4 — Encontrar a multidão faminta (Halbert)

Antes de escrever, responder mentalmente:
- Quem já quer exatamente o que esse cliente oferece?
- Qual é o desejo que já existe e precisa apenas ser amplificado?
- O que essa pessoa está sentindo no momento em que vai ver esse anúncio?

Exemplo: para um bar na Savassi em uma quinta-feira: a pessoa está no trabalho, já pensando no fim de tarde, querendo uma justificativa para sair mais cedo. A copy não precisa convencer — precisa dar o empurrão.

Usar esse insight para calibrar o gancho emocional de cada variação.

### Passo 5 — Gerar as copies

Com nível de consciência definido, multidão faminta identificada e tom de voz do cliente carregado, gerar:

---

#### META ADS (Facebook / Instagram)

**Texto principal — 3 variações com estruturas diferentes:**

**Variação 1 — Estrutura PAS (Problem / Agitation / Solution)**
- Linha 1: espelha o problema ou desejo que o público já sente
- Linha 2: amplifica a dor ou o desejo (faz ele sentir mais)
- Linha 3: apresenta a solução como inevitável
- Linha 4: CTA direto

**Variação 2 — Estrutura de Gancho + Prova + CTA (Halbert)**
- Linha 1: gancho que para o scroll nos primeiros 3 segundos (pergunta, dado específico, provocação ou promessa ousada)
- Linha 2-3: prova ou especificidade que sustenta o gancho (Ogilvy: seja concreto, não vago)
- Linha 4: CTA

**Variação 3 — Estrutura AIDA (Attention / Interest / Desire / Action)**
- Atenção: headline que interrompe o feed
- Interesse: detalhe específico que mantém lendo
- Desejo: o que a pessoa vai sentir ou ganhar
- Ação: CTA com urgência ou benefício imediato

Cada variação: máximo 5 linhas, tom do cliente, sem frases genéricas de IA.

**Headlines — 4 opções (Ogilvy: a headline vale 80%):**
- Opção 1: específica e informativa (data + evento + destaque)
- Opção 2: orientada ao benefício emocional
- Opção 3: curiosidade ou provocação
- Opção 4: urgência ou escassez (se aplicável)

Limite: até 40 caracteres por headline.

**Descrição — 2 opções:**
- Complemento da headline, até 30 caracteres
- Uma reforça benefício, outra reforça CTA

---

#### GOOGLE ADS

**Headlines — 6 opções (até 30 caracteres cada):**
- Nome do negócio + localização
- Evento ou oferta principal
- Destaque específico (Ogilvy: seja concreto)
- Benefício emocional em 4-5 palavras
- CTA direto
- Urgência ou escassez (se aplicável)

**Descrições — 3 opções (até 90 caracteres cada):**
- Opção 1: o que é + diferencial específico + CTA
- Opção 2: dor/desejo do público + solução + CTA (estrutura PAS comprimida)
- Opção 3: evento/oferta específica + urgência + CTA

---

### Passo 6 — Apresentar o resultado

Apresentar organizado por plataforma, com o nível de consciência identificado no topo para referência.

Formato de saída:

```
NIVEL DE CONSCIENCIA IDENTIFICADO: [nível + justificativa em 1 frase]
MULTIDAO FAMINTA: [quem é + o que já quer]

--- META ADS ---
[copies organizadas por variação + headlines + descrições]

--- GOOGLE ADS ---
[headlines + descrições]
```

Ao final perguntar: "Quer ajustar alguma variação, mudar a estrutura ou gerar mais opções?"

---

## Regras de escrita

- Usar sempre o tom de voz do cliente — não tom genérico
- Especificidade vende: "chopp de 600ml tirado na temperatura certa" bate "chopp gelado"
- Sem construções de IA: sem travessão estilístico, "mergulhe em", "descubra", "venha viver experiências únicas"
- Sem adjetivos vazios: "incrível", "único", "imperdível", "especial" não dizem nada
- Categorização precisa: bar não é "espaço gastronômico", boteco não é "restaurante premium"
- Headlines do Google: contar os caracteres — nunca ultrapassar o limite
- A primeira linha de cada variação precisa parar o scroll — se não parar, reescrever
- Se faltar dado importante, perguntar antes de gerar — nunca inventar informação do cliente
