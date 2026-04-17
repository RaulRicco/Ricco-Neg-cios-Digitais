---
name: descricao-gmb
description: >
  Cria descrição otimizada para o Google Meu Negócio seguindo a fórmula de SEO local:
  palavra-chave principal + bairro + cidade, o que serve, diferenciais e CTA de visita.
  Limite de 750 caracteres, tom de fundo de funil, sem marcas de escrita de IA.
  Use quando o usuário disser "cria descrição do GMB de [cliente]", "descrição Google Meu Negócio",
  "otimiza a descrição do perfil de [cliente]".
---

# /descricao-gmb — Descrição Otimizada para Google Meu Negócio

## Referência metodológica

Fórmula de SEO local para Map Pack:

1. Palavra-chave principal + bairro + cidade
2. O que serve (produtos, pratos, bebidas, serviços)
3. Diferenciais do negócio
4. CTA para visita (fundo de funil)

O objetivo é capturar quem já está procurando ativamente. A descrição precisa confirmar que encontrou o lugar certo e induzir a visita.

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
- Segmento exato do cliente (usar categorização precisa: "bar de boteco", não "espaço gastronômico")
- Bairro e cidade de cada unidade
- Palavras-chave já mapeadas

Se o cliente não tiver Google Meu Negócio na lista, avisar: "[Cliente] não tem GMB na estrutura atual. Quer criar a descrição mesmo assim?"

### Passo 2 — Verificar tom de voz

Verificar se existe `clientes/[nome-cliente]/tom-de-voz.md`.
- Se existir: usar o tom registrado
- Se não existir: usar o segmento como referência e manter tom direto, de bairro, sem formalidade excessiva

### Passo 3 — Aplicar a estrutura

**Bloco 1 — Abertura com palavra-chave + localização:**
Abrir com uma frase que contenha a palavra-chave principal, o bairro e a cidade. O formato deve soar natural, como alguém descrevendo o lugar, não como tag de SEO.
Exemplo: "Se você está procurando um bar na Savassi, em Belo Horizonte..."
Ou: "O Balcão Savassi é um bar no coração da Savassi, em Belo Horizonte..."

**Bloco 2 — O que serve:**
Listar de forma direta o que o cliente oferece: bebidas, pratos, petiscos, serviços. Ser específico. Citar itens reais quando souber (chopp, drinques, petiscos, rodízio, etc.). Evitar "cardápio variado" ou "opções para todos os gostos".

**Bloco 3 — Diferenciais:**
Citar o que diferencia esse bar dos outros na mesma região. Pode ser o ambiente, localização privilegiada, happy hour, música ao vivo, espaço, história do bairro, etc. Usar as informações do tom de voz do cliente.

**Bloco 4 — CTA de visita:**
Fechar com uma frase que convide à visita física. Tom de fundo de funil: a pessoa já sabe o que quer, só precisa confirmar que vai ao lugar certo. Exemplos: "Venha conferir pessoalmente.", "Estamos te esperando na [rua/bairro].", "A melhor forma de conhecer é vindo."

### Passo 4 — Regras de escrita

- **Sem travessões** (—) em nenhuma circunstância
- **Sem reticências** (...) como recurso estilístico
- **Sem construções de IA** como "mergulhe em", "descubra um universo de", "eleve sua experiência", "onde cada detalhe importa"
- **Sem adjetivos vazios** como "incrível", "único", "especial", "imperdível"
- **Sem keyword stuffing:** incorporar 3 a 5 palavras-chave da lista do cliente, sem repetir o mesmo termo mais de uma vez
- **Limite rígido:** máximo 750 caracteres (o GMB corta o restante)
- Escrever como um humano descreveria o lugar para um amigo que está pesquisando onde ir

### Passo 5 — Gerar as variações

Gerar **2 variações** da descrição seguindo a mesma estrutura dos 4 blocos:

- **Variação 1:** abertura mais direta com a palavra-chave ("Bar na Savassi...")
- **Variação 2:** abertura mais contextual, pelo nome do lugar ou pelo diferencial

Ao final de cada variação, indicar:
```
[Caracteres: XX/750]
[Palavras-chave usadas: ...]
[Localizações mencionadas: ...]
```

### Passo 6 — Revisão rápida

Antes de entregar, verificar:
- Tem travessão, reticências ou construção típica de IA? Reescrever.
- A abertura contém palavra-chave + bairro + cidade? Confirmar.
- Os 4 blocos estão presentes (abertura, o que serve, diferenciais, CTA)? Confirmar.
- Está dentro de 750 caracteres? Confirmar.
- A categorização do segmento está precisa? Confirmar.

---

## Regras gerais

- Categorização precisa: nunca chamar boteco de "restaurante premium" ou bar de "espaço gourmet"
- Se o cliente tiver múltiplas unidades com perfis separados, gerar uma descrição por unidade com o bairro específico de cada uma
- Tom segue `_contexto/preferencias.md` e o tom de voz do cliente: direto, sem entusiasmo vazio
- A descrição é fundo de funil: quem lê já está procurando, não precisa ser convencido de que quer um bar, precisa ser convencido de que esse é o certo
