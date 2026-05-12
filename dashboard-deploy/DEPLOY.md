# Deploy — dash.raulricco.com.br

## Pré-requisitos

```bash
npm install -g wrangler
wrangler login   # abre o browser para autenticar na sua conta Cloudflare
```

---

## Parte 1 — Cloudflare Pages (hospeda os HTMLs)

### 1.1 Criar o projeto Pages

No dashboard da Cloudflare:
1. Acesse **Workers & Pages → Create → Pages → Upload assets**
2. Nome do projeto: `ricco-dashboards`
3. Faça upload da pasta `pages/` inteira (arraste a pasta ou compacte em ZIP)
4. Clique em **Deploy site**

### 1.2 Vincular o subdomínio ao Pages

1. No projeto `ricco-dashboards` → **Custom Domains**
2. Adicionar: `dash.raulricco.com.br`
3. Cloudflare configura o DNS automaticamente (seu domínio já está na Cloudflare ✓)

---

## Parte 2 — Cloudflare Worker (autenticação Basic Auth)

### 2.1 Deploy do Worker

```bash
cd dashboard-deploy/worker
wrangler deploy
```

Saída esperada:
```
✅  Successfully deployed ricco-dash-auth
    https://ricco-dash-auth.<seu-subdominio>.workers.dev
```

### 2.2 Vincular o Worker ao subdomínio

No dashboard da Cloudflare:
1. **Workers & Pages → ricco-dash-auth → Settings → Triggers**
2. **Custom Domains → Add Custom Domain**
3. Adicionar: `dash.raulricco.com.br`

> Isso faz o Worker interceptar todas as requisições ao subdomínio ANTES de chegar ao Pages — é onde a senha é verificada.

---

## Parte 3 — Testar

```bash
# Deve retornar 401 (sem senha)
curl -I https://dash.raulricco.com.br/acougueiro-agua-verde

# Deve retornar 200 (com senha correta)
curl -I -u "ricco:acougueiro2026" https://dash.raulricco.com.br/acougueiro-agua-verde
```

Ou simplesmente acesse no browser:
**dash.raulricco.com.br/acougueiro-agua-verde** → digitar a senha quando solicitado.

---

## Adicionar novo cliente

```bash
# 1. Copiar template
cp -r pages/acougueiro-agua-verde pages/novo-slug

# 2. Editar o HTML com os dados do cliente
# (nome, métricas, plataformas)

# 3. Adicionar a senha no Worker
# Editar worker/index.js → objeto CLIENTES

# 4. Adicionar rota
# Editar pages/_redirects

# 5. Redesployar Pages (upload da pasta pages/ atualizada)
# 6. Redesployar Worker
wrangler deploy
```

---

## Atualizar dashboard de um cliente

1. Editar o `index.html` correspondente em `pages/slug-do-cliente/`
2. Fazer novo upload da pasta `pages/` no Cloudflare Pages
   - Workers & Pages → ricco-dashboards → Deployments → Upload assets

---

## Estrutura de arquivos

```
dashboard-deploy/
├── worker/
│   ├── index.js          ← lógica de autenticação
│   └── wrangler.toml     ← config do Worker
├── pages/
│   ├── _redirects        ← rotas por cliente
│   ├── _headers          ← cache
│   └── acougueiro-agua-verde/
│       └── index.html    ← dashboard do cliente
├── CLIENTES.md           ← tabela de senhas e URLs
└── DEPLOY.md             ← este arquivo
```
