---
name: copy-anuncio
description: >
  Gera copies de anúncio prontos para colar no Google Ads e Meta Ads a partir dos dados de um evento.
  Consulta o tom de voz específico do cliente antes de gerar.
  Use quando o usuário disser "cria a copy do evento X", "faz o texto do anúncio", "copy para a campanha de [cliente]".
---

# /copy-anuncio — Copy de Anúncio para Eventos

## Dependências

- **Tom de voz do cliente:** `clientes/[nome-cliente]/tom-de-voz.md`
- **Contexto geral:** `_contexto/preferencias.md`

---

## Workflow

### Passo 1 — Identificar o cliente

Perguntar: "Qual é o cliente? Vou checar o tom de voz dele."

Buscar o arquivo `clientes/[nome-cliente]/tom-de-voz.md`.

- Se existir: ler e usar como base para o tom
- Se não existir: avisar — "Ainda não tenho o tom de voz de [cliente] cadastrado. Me descreve em 2-3 linhas como ele se comunica com o público e eu já uso nisso." Após a resposta, criar o arquivo em `clientes/[nome-cliente]/tom-de-voz.md` com o que foi descrito.

### Passo 2 — Coletar os dados do evento

Perguntar: "Me passa os dados do evento — pode ser uma descrição ou os dados que estão na arte."

Extrair:
- **Nome do evento / atração**
- **Data e horário**
- **Local** (se aplicável)
- **Destaque principal** (o que vende o evento — preço, artista, experiência, etc.)
- **Link de destino** (se houver)

Se o usuário mandar imagem da arte, extrair os dados diretamente.

### Passo 3 — Identificar o objetivo da campanha

Perguntar: "Qual o objetivo dessa campanha?"

Opções comuns:
- Alcance / reconhecimento de marca
- Engajamento (curtidas, comentários, compartilhamentos)
- Tráfego para site ou link
- Conversão (reserva, compra, cadastro)

O objetivo define o estilo da copy (mais informativa vs. mais persuasiva/urgência).

### Passo 4 — Gerar as copies

Com os dados do evento, o tom de voz do cliente e o objetivo da campanha, gerar:

#### Meta Ads (Facebook / Instagram)

**Texto principal (3 variações):**
- Variação 1: foco no evento em si (o que é, quando, onde)
- Variação 2: foco na experiência / emoção
- Variação 3: foco em urgência ou escassez (se aplicável)

Cada variação: 2-4 linhas, linguagem do cliente, CTA no final.

**Headlines (3 opções):**
- Diretas, até 40 caracteres
- Uma com nome do evento, uma com data/local, uma com CTA

**Descrição (1-2 opções):**
- Complemento da headline, até 30 caracteres

---

#### Google Ads

**Headlines (5 opções — até 30 caracteres cada):**
- Nome do evento
- Data + local
- Destaque principal
- CTA
- Variação de benefício

**Descrições (2 opções — até 90 caracteres cada):**
- Linha 1: o que é o evento + diferencial
- Linha 2: CTA + urgência ou benefício adicional

---

### Passo 5 — Apresentar o resultado

Apresentar tudo organizado por plataforma, pronto para copiar e colar.

Ao final, perguntar: "Quer ajustar alguma variação ou gerar mais opções?"

---

## Regras

- Usar sempre o tom de voz do cliente — não o tom genérico de Raul
- Categorização precisa de nicho: não chamar bar de "restaurante", não chamar boteco de "espaço gastronômico"
- Sem frases de efeito vazias ("venha viver experiências únicas", "não perca essa oportunidade incrível")
- Headlines do Google: contar os caracteres — nunca ultrapassar o limite
- Se faltar dado importante (ex: link de destino), perguntar antes de gerar
