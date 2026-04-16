---
name: analisar-seo
description: >
  Analisa o SEO de um site de cliente e entrega recomendações priorizadas de otimização.
  Cruza o conteúdo do site com as palavras-chave mapeadas e identifica gaps técnicos e de conteúdo.
  Use quando o usuário disser "analisa o SEO de [cliente]", "o que preciso melhorar no site de [cliente]",
  "auditoria de SEO [cliente]".
---

# /analisar-seo — Análise de SEO

## Dependências

- **Lista de clientes e palavras-chave:** `clientes/lista-clientes.md`
- **Tom de voz do cliente:** `clientes/[nome-cliente]/tom-de-voz.md`

---

## Workflow

### Passo 1 — Identificar o cliente

Perguntar: "SEO de qual cliente?"

Ler `clientes/lista-clientes.md` e localizar:
- URL do site (se cadastrada)
- Palavras-chave mapeadas
- Serviços ativos — confirmar que o cliente tem SEO ativo

Clientes com SEO ativo:
- Bar do Açougueiro
- Quermesse Bar
- Floreria Café.Bar
- Churrascaria Boi Dourado
- Bsbichos
- Ameriparts Três Lagoas
- Comodoro Burguer

Se o site não estiver cadastrado em `lista-clientes.md`, perguntar: "Qual é a URL do site?"

### Passo 2 — Acessar o site

Usar WebFetch para ler o conteúdo da URL principal do cliente.

Se o site tiver páginas internas relevantes (serviços, sobre, contato), fazer WebFetch nas principais também para análise mais completa.

Se o site retornar erro, informar: "Não consegui acessar o site. Verifique se a URL está correta ou se o site está no ar."

### Passo 3 — Analisar o site

Com o conteúdo do site e as palavras-chave do cliente, analisar:

#### SEO On-Page

**Title tag:**
- Está presente?
- Contém a palavra-chave principal?
- Tem entre 50-60 caracteres?
- É único por página?

**Meta description:**
- Está presente?
- Contém palavra-chave e CTA?
- Tem entre 150-160 caracteres?

**Headings (H1, H2, H3):**
- Existe H1 único e claro?
- H1 contém palavra-chave principal?
- H2s organizam o conteúdo com palavras-chave secundárias?

**Conteúdo:**
- As palavras-chave do cliente aparecem naturalmente no texto?
- Há palavras-chave importantes faltando?
- O conteúdo responde a intenção de busca do público?
- Existe conteúdo suficiente (páginas rasas penalizam no Google)?

**URLs:**
- São amigáveis e descritivas?
- Contêm palavras-chave relevantes?

**Links internos:**
- Existem links entre as páginas do site?
- As âncoras são descritivas?

**Google Meu Negócio:**
- O NAP (Nome, Endereço, Telefone) do site é consistente com o GMB?

#### SEO Local (para clientes com foco geográfico)

- Cidade e bairro aparecem no conteúdo?
- Palavras-chave locais estão sendo usadas (ex: "bar em Curitiba")?
- Existe página específica por unidade (quando o cliente tem múltiplas unidades)?

### Passo 4 — Entregar a análise

Apresentar em formato de lista priorizada:

```
## Análise de SEO — [Nome do Cliente]
Site analisado: [URL]

### 🔴 Crítico — resolver primeiro
[itens que mais impactam o rankeamento]

### 🟡 Importante — resolver em seguida
[itens que melhoram mas não são bloqueantes]

### 🟢 Oportunidade — quando tiver tempo
[melhorias de longo prazo]

### ✅ Já está bem
[o que está funcionando — não mexa]

---
### Palavras-chave com oportunidade
[palavras do cliente que não aparecem no site ou aparecem pouco]

### Sugestão de próximo passo
[a ação mais impactante pra fazer agora]
```

### Passo 5 — Aprofundar se necessário

Após apresentar a análise, perguntar: "Quer que eu aprofunde algum ponto ou gere sugestões de texto pra alguma seção?"

Se sim:
- Gerar sugestão de title tag e meta description otimizados
- Reescrever trechos de conteúdo com as palavras-chave incorporadas
- Sugerir estrutura de H1/H2 para a página

---

## Regras

- Usar sempre as palavras-chave específicas do cliente — nunca genéricas
- Categorização precisa: "bar em Curitiba" não é a mesma coisa que "restaurante em Curitiba"
- Priorizar o que mais impacta rankeamento local (Google Meu Negócio + SEO local)
- Não sugerir mudanças que fujam do tom de voz do cliente
- Se o site tiver problema técnico grave (sem HTTPS, lentidão visível, sem mobile), mencionar mesmo que não dê pra verificar via WebFetch
