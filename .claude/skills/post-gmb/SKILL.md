---
name: post-gmb
description: >
  Cria legendas de posts para o Google Meu Negócio com copy ultra persuasiva e SEO local.
  Aplica as metodologias de Schwartz (consciência), Halbert (gancho emocional) e Ogilvy
  (especificidade e headline). Para clientes com múltiplas unidades, menciona as unidades
  no post. Porks são franqueados independentes e não fazem posts de GMB.
  Use quando o usuário disser "cria post pro GMB de [cliente]", "legenda Google Meu Negócio",
  "faz post de SEO local para [cliente]".
---

# /post-gmb — Legenda de Post para Google Meu Negócio

## Base metodológica

As mesmas três referências da skill `/copy-anuncio`:

**Eugene Schwartz** — o post fala com quem já está procurando (nível 3-5 de consciência).
Não precisa educar — precisa confirmar que encontrou o lugar certo e induzir a ação.

**Gary Halbert** — encontre quem já quer o que o cliente oferece e dê o empurrão.
A primeira linha precisa parar quem está navegando. Se não parar, o post não existe.

**David Ogilvy** — especificidade converte. Não "ótimos petiscos" — "costela defumada servida ao peso, direto do balcão".
Cada detalhe concreto vale mais que dez adjetivos.

---

## Dependências

- **Lista de clientes e palavras-chave:** `clientes/lista-clientes.md`
- **Tom de voz do cliente:** `clientes/[nome-cliente]/tom-de-voz.md` (se existir)
- **Preferências gerais:** `_contexto/preferencias.md`

---

## Regra de unidades

**Clientes com múltiplas unidades — mencionar as unidades no post:**

Ao gerar post para clientes com mais de uma unidade, incluir referência às unidades
no corpo do texto ou no CTA. Não fazer post genérico que não diz onde o cliente está.

Clientes com múltiplas unidades ativas no GMB:
- Bar do Açougueiro: Água Verde, Bacacheri e Batel (Curitiba)
- Quermesse Bar: Bom Retiro e Ecoville (Curitiba)
- Bebedouro Bar e Fogo: unidade 356 (rooftop, Olhos D'Água) e Pampulha (BH)
- Bsbichos: Asa Sul e Asa Norte (Brasília)

Se o post for para uma unidade específica, usar apenas o bairro daquela unidade.
Se o post for geral (para todas as unidades do cliente), mencionar os bairros.

**Porks — não fazem posts de GMB:**
Todas as unidades Porks (Asa Sul, Asa Norte, Samambaia, Ceilândia, Guará, Casarão, Castelo, Pirenópolis, Três Lagoas) são franqueados independentes entre si.
Nenhuma delas faz posts de Google Meu Negócio no contexto desse trabalho.
Se o usuário pedir post de GMB para qualquer unidade Porks, avisar:
"As unidades Porks são franqueados independentes e não fazem posts de GMB. Quer criar algo diferente para eles?"

---

## Workflow

### Passo 1 — Identificar o cliente e a unidade

Perguntar: "Post pra qual cliente?"

Ler `clientes/lista-clientes.md` e verificar:
- O cliente tem GMB ativo?
- Tem mais de uma unidade? Se sim, o post é para qual unidade ou para todas?
- É um cliente Porks? Se sim, aplicar a regra acima.

### Passo 2 — Definir o tema e o tipo de post

Perguntar: "Qual o tema do post?"

Tipos comuns:
- **Evento:** show, data comemorativa, noite especial
- **Promoção:** happy hour, desconto, combo
- **Produto/serviço em destaque:** item do cardápio, serviço novo
- **Institucional de rankeamento:** post sem evento específico, objetivo é SEO

Para posts institucionais de rankeamento, o foco é distribuir palavras-chave locais de forma natural. Usar a lista de keywords do cliente em `lista-clientes.md`.

### Passo 3 — Verificar tom de voz

Verificar `clientes/[nome-cliente]/tom-de-voz.md`.
- Se existir: usar o tom registrado
- Se não existir: usar o segmento como referência. Bar de boteco fala diferente de café sofisticado. Hamburgueria artesanal fala diferente de churrascaria familiar.

### Passo 4 — Encontrar o gancho (Halbert)

Antes de escrever, identificar:
- Quem vai ver esse post? Quem já está procurando esse tipo de lugar?
- O que essa pessoa quer sentir ou viver naquele momento?
- Qual é o detalhe específico que vai parar o scroll?

Usar esse insight para definir a primeira linha de cada variação.

### Passo 5 — Gerar as variações

**Limite:** 1.500 caracteres (GMB aceita até 1.500 — manter entre 800-1.200 para leitura confortável)

**Variação 1 — SEO e rankeamento (Ogilvy: específico e informativo)**
- Foco em distribuir palavras-chave locais naturalmente
- Estrutura: o que é + onde fica (bairro + cidade) + o que serve + CTA
- Tom direto, sem adjetivos vazios
- 2-4 palavras-chave da lista do cliente incorporadas naturalmente

**Variação 2 — Persuasão e conversão (Halbert + Schwartz)**
- Foco em amplificar o desejo de quem já está procurando
- Estrutura: gancho emocional + especificidade do produto/experiência + CTA
- Tom do cliente: fala como ele fala com o público
- A primeira linha precisa parar quem está navegando

**Ao final de cada variação, indicar:**
```
[Botão sugerido: Fazer reserva / Ligar agora / Ver mais / Fazer pedido]
[Palavras-chave usadas: ...]
[Unidades mencionadas: ... ] (se aplicável)
[Caracteres: XX/1500]
```

### Passo 6 — CTA e botão

Indicar o botão de ação mais adequado ao objetivo:
- "Fazer reserva" — bares e restaurantes com reserva
- "Ligar agora" — serviços e comércios
- "Ver mais" — posts informativos ou institucionais
- "Fazer pedido" — delivery
- "Comprar" — e-commerce ou produtos

### Passo 7 — Sugestão de imagem (opcional)

Após gerar o texto, perguntar: "Quer sugestão de imagem para esse post?"

Se sim, descrever o tipo de imagem que reforça o rankeamento local:
- Foto do produto em destaque com o ambiente visível ao fundo
- Fachada com nome do lugar legível
- Equipe ou bastidores (humaniza e aumenta engajamento)
- Foto com geolocalização ativada no celular (sinal de entidade para o Google)

---

## Regras de escrita

- Usar o nome exato do bairro e cidade — "bar no Batel, Curitiba" é mais forte que "bar em Curitiba"
- Categorização precisa: nunca chamar boteco de "espaço gastronômico" ou bar de "restaurante premium"
- Sem construções de IA: sem travessão estilístico, "mergulhe em", "descubra", "venha viver experiências únicas"
- Sem adjetivos vazios: "incrível", "único", "imperdível", "especial" não dizem nada
- Palavras-chave incorporadas de forma natural — o texto precisa soar humano, não spam de SEO
- A primeira linha de cada variação precisa parar o scroll — se não parar, reescrever
- Fundo de funil: o leitor já sabe o que quer, o post confirma e converte
