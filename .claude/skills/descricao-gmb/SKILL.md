---
name: descricao-gmb
description: >
  Cria descrição otimizada para o Google Meu Negócio seguindo a fórmula de SEO local:
  localizações primeiro, serviços depois. Limite de 750 caracteres, sem keyword stuffing.
  Use quando o usuário disser "cria descrição do GMB de [cliente]", "descrição Google Meu Negócio",
  "otimiza a descrição do perfil de [cliente]".
---

# /descricao-gmb — Descrição Otimizada para Google Meu Negócio

## Referência metodológica

Baseada na fórmula de SEO local validada:
**Localizações primeiro → Serviços depois**

Evitar:
- Keyword stuffing (repetição forçada de termos)
- Texto vago ou genérico ("venha nos visitar", "somos os melhores")
- Descrições que não dizem claramente o que o negócio faz e onde

O objetivo é que o Google entenda com precisão **o que** o negócio oferece e **onde** atua — isso impacta diretamente a visibilidade no Map Pack.

---

## Dependências

- **Lista de clientes e palavras-chave:** `clientes/lista-clientes.md`
- **Tom de voz do cliente:** `clientes/[nome-cliente]/tom-de-voz.md` (se existir)
- **Preferências gerais:** `_contexto/preferencias.md`

---

## Workflow

### Passo 1 — Identificar o cliente e a unidade

Perguntar: "Descrição pra qual cliente? Se tiver mais de uma unidade, qual delas?"

Ler `clientes/lista-clientes.md` e localizar:
- Segmento exato do cliente (usar a categorização precisa — "bar de boteco", não "espaço gastronômico")
- Endereço(s) e bairro(s)
- Cidade(s) de atuação
- Palavras-chave já mapeadas

Se o cliente não tiver Google Meu Negócio na lista, avisar: "[Cliente] não tem GMB na estrutura atual. Quer criar a descrição mesmo assim?"

### Passo 2 — Verificar tom de voz

Verificar se existe `clientes/[nome-cliente]/tom-de-voz.md`.
- Se existir: usar o tom registrado
- Se não existir: usar o segmento como referência e manter tom direto e profissional

### Passo 3 — Aplicar a fórmula

**Estrutura obrigatória:**

```
[Localizações] + [O que o negócio é/faz] + [Serviços ou diferenciais específicos]
```

**Regras da fórmula:**

1. **Localizações primeiro:** abrir com a cidade e bairro(s) onde o negócio atua. Se tiver múltiplas unidades, citar as principais. Ex: "No Batel e no Água Verde, em Curitiba..."
2. **Serviços depois:** descrever o que o negócio oferece de forma específica. Evitar generalidades — citar pratos, tipos de atendimento, diferenciais reais.
3. **Densidade de palavras-chave:** incorporar 3-5 palavras-chave da lista do cliente de forma natural. Não repetir o mesmo termo mais de uma vez.
4. **Limite rígido:** máximo 750 caracteres (o GMB corta o restante).
5. **Sem CTA:** descrição do perfil não é post — não usar "ligue agora", "faça sua reserva aqui".

### Passo 4 — Gerar as variações

Gerar **2 variações** da descrição:

- **Variação 1 — Rankeamento:** prioriza a cobertura de palavras-chave e localizações. Mais informativa, direta.
- **Variação 2 — Conversão:** prioriza o diferencial e a proposta de valor. Mais persuasiva, sem perder a precisão.

Ao final de cada variação, indicar:
```
[Caracteres: XX/750]
[Palavras-chave usadas: ...]
[Localizações mencionadas: ...]
```

### Passo 5 — Revisão rápida

Após gerar, verificar mentalmente:
- A descrição deixa claro o que o negócio faz e onde fica? ✓
- Tem keyword stuffing (mesma palavra repetida)? ✗
- Está dentro de 750 caracteres? ✓
- A categorização do segmento está precisa? ✓

---

## Regras

- Usar o nome exato do bairro e cidade — "bar no Batel, Curitiba" é melhor que "bar em Curitiba"
- Categorização precisa: nunca chamar boteco de "restaurante premium" ou bar de "espaço gourmet"
- Localizações sempre antes dos serviços — é a fórmula que ajuda no Map Pack
- Sem frases genéricas de marketing ("somos referência", "atendimento de qualidade")
- Se o cliente tiver múltiplas unidades com perfis separados, gerar uma descrição por unidade (com o bairro específico de cada uma)
- Tom segue `_contexto/preferencias.md`: direto, preciso, sem entusiasmo vazio
