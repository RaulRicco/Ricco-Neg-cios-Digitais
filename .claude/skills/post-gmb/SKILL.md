---
name: post-gmb
description: >
  Cria posts otimizados para o Google Meu Negócio com foco em rankeamento local.
  Usa as palavras-chave do cliente e gera textos de fundo de funil com CTA.
  Use quando o usuário disser "cria post pro GMB de [cliente]", "post Google Meu Negócio",
  "faz post de SEO local para [cliente]".
---

# /post-gmb — Post para Google Meu Negócio

## Dependências

- **Lista de clientes e palavras-chave:** `clientes/lista-clientes.md`
- **Tom de voz do cliente:** `clientes/[nome-cliente]/tom-de-voz.md` (se existir)
- **Preferências gerais:** `_contexto/preferencias.md`

---

## Workflow

### Passo 1 — Identificar o cliente e a unidade

Perguntar: "Post pra qual cliente? Se tiver mais de uma unidade, qual delas?"

Ler `clientes/lista-clientes.md` e localizar:
- Segmento exato do cliente
- Palavras-chave já mapeadas
- Serviços ativos (confirmar que o cliente tem GMB)

Se o cliente não tiver GMB na lista, avisar: "[Cliente] não tem Google Meu Negócio na estrutura atual. Quer criar o post mesmo assim?"

### Passo 2 — Definir o tema do post

Perguntar: "Qual o tema do post? Pode ser um evento, promoção, serviço específico, data comemorativa, ou post institucional de rankeamento."

Identificar:
- **Tipo:** evento / promoção / serviço / institucional
- **Assunto principal:** o que o post vai comunicar
- **Data relevante** (se aplicável): dia do evento, validade da promoção

Se for post institucional de rankeamento (sem evento específico), usar as palavras-chave do cliente de forma natural no texto.

### Passo 3 — Verificar tom de voz

Verificar se existe `clientes/[nome-cliente]/tom-de-voz.md`.
- Se existir: usar o tom registrado
- Se não existir: usar o segmento como referência (bar de boteco ≠ café sofisticado ≠ hamburgueria artesanal) e manter tom profissional mas próximo ao público

### Passo 4 — Gerar o post

**Estrutura do post GMB (fundo de funil):**

- **Limite:** até 1.500 caracteres (GMB aceita até 1.500 — manter entre 800-1.200 para leitura confortável)
- **Tom:** direto, com intenção de conversão — o leitor já está procurando, o post precisa confirmar a escolha
- **Palavras-chave:** incorporar naturalmente 2-4 palavras-chave do cliente no texto (sem repetição forçada)
- **CTA obrigatório:** indicar o botão de ação mais adequado ao objetivo:
  - "Fazer reserva" — para bares e restaurantes com reserva
  - "Ligar agora" — para serviços e comércios
  - "Ver mais" — para posts informativos
  - "Comprar" — para e-commerce ou produtos
  - "Fazer pedido" — para delivery

**Gerar 2 variações do post:**
- Variação 1: foco no serviço/produto (mais informativo, rankeamento)
- Variação 2: foco na experiência/benefício (mais persuasivo)

**Ao final de cada variação, indicar:**
```
[Botão sugerido: Fazer reserva / Ligar agora / etc.]
[Palavras-chave usadas: ...]
```

### Passo 5 — Sugerir imagem (opcional)

Após gerar o texto, perguntar: "Quer sugestão de imagem ou legenda pra foto que vai junto com esse post?"

Se sim, descrever o tipo de imagem que reforça o rankeamento local: foto do ambiente, do produto em destaque, ou da fachada com localização visível.

---

## Regras

- Usar o nome exato do bairro ou cidade nas palavras-chave quando relevante (ex: "bar no Batel", "rooftop em BH")
- Categorização precisa: nunca chamar boteco de "espaço gastronômico", bar de "restaurante premium"
- Não usar linguagem genérica de marketing ("venha nos visitar", "temos o melhor da cidade")
- Palavras-chave incorporadas de forma natural — o texto precisa soar humano, não spam de SEO
- Fundo de funil: o leitor já sabe o que quer, o post confirma e converte
- Sempre indicar o botão de CTA mais adequado ao objetivo do post
