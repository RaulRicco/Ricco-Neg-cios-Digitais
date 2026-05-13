// Cloudflare Pages Function — middleware de autenticação por senha
// Intercepta todas as rotas de dashboard e exige senha antes de servir o conteúdo.

const SENHAS = {
  "acougueiro-agua-verde": "acougueiro24",
  "acougueiro-bacacheri":  "acougueiro24",
  "acougueiro-batel":      "acougueiro24",
  "quermesse-bom-retiro":  "quermesse24",
  "quermesse-ecoville":    "quermesse24",
  "floreria":              "floreria24",
  "boi-dourado":           "boidourado24",
  "bebedouro":             "bebedouro24",
  "balcao-savassi":        "balcao24",
  "ameriparts":            "ameriparts24",
  "comodoro-burguer":      "comodoro24",
  "bsbichos":              "bsbichos24",
  "bistecao":              "bistecao24",
  "garage-burger":         "garage24",
  "dona-cleide":           "cleide24",
  "seu-barbudo":           "barbudo24",
  "horus":                 "horus24",
  "sol-e-lar":             "solelar24",
  "solar-e-cia":           "solar24",
  "fish-me":               "fishme24",
  "porks-asa-sul":         "porks24",
  "porks-asa-norte":       "porks24",
  "porks-samambaia":       "porks24",
  "porks-guara":           "porks24",
  "porks-tres-lagoas":     "porks24",
  "porks-casarao":         "porks24",
  "porks-castelo":         "porks24",
  "porks-pirenopolis":     "porks24",
  "boteco-do-quintal":     "quintal24",
  "quintal-piri":          "quintal24",
};

const COOKIE_NAME = "ricco_dash_auth";
const COOKIE_MAX_AGE = 60 * 60 * 24 * 7; // 7 dias

function slugFromPath(pathname) {
  const parts = pathname.replace(/^\//, "").split("/");
  return parts[0] || "";
}

function isAuthenticated(request, slug) {
  const cookieHeader = request.headers.get("Cookie") || "";
  const cookies = Object.fromEntries(
    cookieHeader.split(";").map(c => {
      const [k, ...v] = c.trim().split("=");
      return [k, v.join("=")];
    })
  );
  const token = cookies[COOKIE_NAME];
  if (!token) return false;
  try {
    const payload = JSON.parse(atob(token));
    return payload.slug === slug && payload.pwd === SENHAS[slug];
  } catch {
    return false;
  }
}

function loginPage(slug, nome, error = false) {
  return `<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Acesso — ${nome}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box;}
  body{font-family:'Inter',sans-serif;background:#0a0a0a;color:#fff;min-height:100vh;display:flex;align-items:center;justify-content:center;}
  .box{background:#141414;border:1px solid #222;border-radius:16px;padding:40px;width:100%;max-width:380px;}
  .badge{display:inline-block;background:#a3e635;color:#000;font-size:10px;font-weight:800;padding:4px 10px;border-radius:6px;letter-spacing:0.06em;text-transform:uppercase;margin-bottom:20px;}
  h1{font-size:20px;font-weight:800;margin-bottom:6px;}
  .sub{font-size:13px;color:#666;margin-bottom:28px;}
  label{display:block;font-size:11px;font-weight:600;color:#888;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;}
  input{width:100%;background:#1a1a1a;border:1px solid #333;border-radius:8px;color:#fff;font-family:'Inter',sans-serif;font-size:14px;font-weight:600;padding:12px 14px;outline:none;transition:border-color .15s;}
  input:focus{border-color:#a3e635;}
  button{width:100%;background:#a3e635;color:#000;font-family:'Inter',sans-serif;font-size:14px;font-weight:800;padding:12px;border:none;border-radius:8px;cursor:pointer;margin-top:14px;transition:opacity .15s;}
  button:hover{opacity:0.9;}
  .error{background:#2a0a0a;border:1px solid #5a1a1a;border-radius:8px;padding:10px 14px;font-size:13px;color:#ff6b6b;margin-bottom:16px;}
  .footer{text-align:center;font-size:11px;color:#444;margin-top:24px;}
</style>
</head>
<body>
<div class="box">
  <div class="badge">Ricco</div>
  <h1>${nome}</h1>
  <p class="sub">Dashboard de Performance</p>
  ${error ? '<div class="error">Senha incorreta. Tente novamente.</div>' : ''}
  <form method="POST">
    <label>Senha de acesso</label>
    <input type="password" name="pwd" placeholder="••••••••••" autofocus required>
    <button type="submit">Entrar</button>
  </form>
  <p class="footer">Ricco Negócios Digitais</p>
</div>
</body>
</html>`;
}

const NOMES = {
  "acougueiro-agua-verde": "Bar do Açougueiro — Água Verde",
  "acougueiro-bacacheri":  "Bar do Açougueiro — Bacacheri",
  "acougueiro-batel":      "Bar do Açougueiro — Batel",
  "quermesse-bom-retiro":  "Quermesse Bar — Bom Retiro",
  "quermesse-ecoville":    "Quermesse Bar — Ecoville",
  "floreria":              "Floreria Café.Bar",
  "boi-dourado":           "Churrascaria Boi Dourado",
  "bebedouro":             "Bebedouro Bar e Fogo",
  "balcao-savassi":        "Balcão Savassi",
  "ameriparts":            "Ameriparts Três Lagoas",
  "comodoro-burguer":      "Comodoro Burguer",
  "bsbichos":              "BsBichos PetShop",
  "bistecao":              "Supermercado Bistecão",
  "garage-burger":         "Burger Garage",
  "dona-cleide":           "Dona Cleide — Sabor Caseiro",
  "seu-barbudo":           "Seu Barbudo Barbearia",
  "horus":                 "Hórus Treinamento Físico",
  "sol-e-lar":             "Casas Sol e Lar",
  "solar-e-cia":           "Solar e Cia",
  "fish-me":               "FishMe Bar e Cozinha",
  "porks-asa-sul":         "Porks Asa Sul",
  "porks-asa-norte":       "Porks Asa Norte",
  "porks-samambaia":       "Porks Samambaia",
  "porks-guara":           "Porks Guará",
  "porks-tres-lagoas":     "Porks Três Lagoas",
  "porks-casarao":         "Porks Casarão",
  "porks-castelo":         "Porks Castelo",
  "porks-pirenopolis":     "Porks Pirenópolis",
  "boteco-do-quintal":     "Boteco do Quintal",
  "quintal-piri":          "O Quintal Piri",
};

export async function onRequest(context) {
  const { request, next } = context;
  const url = new URL(request.url);
  const slug = slugFromPath(url.pathname);

  // Só protege rotas que têm senha configurada
  if (!SENHAS[slug]) return next();

  // Recurso estático (data.json, etc.) — valida cookie mas não exibe login
  const isAsset = url.pathname.endsWith(".json") || url.pathname.endsWith(".js") || url.pathname.endsWith(".css");

  if (isAuthenticated(request, slug)) return next();

  // POST — tentativa de login
  if (request.method === "POST") {
    const formData = await request.formData();
    const pwd = formData.get("pwd") || "";
    if (pwd === SENHAS[slug]) {
      const token = btoa(JSON.stringify({ slug, pwd }));
      const response = new Response(null, {
        status: 302,
        headers: {
          "Location": url.pathname,
          "Set-Cookie": `${COOKIE_NAME}=${token}; Path=/; Max-Age=${COOKIE_MAX_AGE}; HttpOnly; SameSite=Lax`,
        },
      });
      return response;
    }
    // Senha errada
    const nome = NOMES[slug] || slug;
    return new Response(loginPage(slug, nome, true), {
      status: 401,
      headers: { "Content-Type": "text/html; charset=utf-8" },
    });
  }

  // GET sem autenticação — exibe tela de login
  if (isAsset) {
    return new Response("Unauthorized", { status: 401 });
  }

  const nome = NOMES[slug] || slug;
  return new Response(loginPage(slug, nome, false), {
    status: 200,
    headers: { "Content-Type": "text/html; charset=utf-8" },
  });
}
