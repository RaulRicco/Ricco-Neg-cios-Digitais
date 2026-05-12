/**
 * Cloudflare Worker — Basic Auth para dashboards de clientes
 * Domínio: dash.raulricco.com.br
 *
 * Cada rota /slug-do-cliente exige uma senha configurada em CLIENTES abaixo.
 * Adicionar novo cliente = adicionar uma linha no objeto CLIENTES.
 */

const CLIENTES = {
  'acougueiro-agua-verde': 'acougueiro2026',
  // Próximos clientes — adicionar aqui:
  // 'bebedouro-pampulha':    'bebedouro2026',
  // 'boi-dourado':           'boidourado2026',
  // 'quermesse-bar':         'quermesse2026',
};

const REALM = 'Dashboard Ricco';

export default {
  async fetch(request) {
    const url  = new URL(request.url);
    // Extrai o slug da rota: /acougueiro-agua-verde → 'acougueiro-agua-verde'
    const slug = url.pathname.replace(/^\//, '').split('/')[0];

    // Rota raiz — sem autenticação, retorna 404 simples
    if (!slug) return new Response('Not found', { status: 404 });

    const senhaCorreta = CLIENTES[slug];

    // Slug não cadastrado
    if (!senhaCorreta) {
      return new Response('Not found', { status: 404 });
    }

    // Verifica Authorization header
    const authHeader = request.headers.get('Authorization') ?? '';
    if (authHeader.startsWith('Basic ')) {
      const decoded   = atob(authHeader.slice(6));
      const [, senha] = decoded.split(':');
      if (senha === senhaCorreta) {
        // Autenticado — faz proxy para o Cloudflare Pages
        return fetch(request);
      }
    }

    // Solicita credenciais
    return new Response('Acesso restrito. Informe a senha fornecida pela Ricco Negócios.', {
      status: 401,
      headers: {
        'WWW-Authenticate': `Basic realm="${REALM}"`,
        'Content-Type': 'text/plain; charset=utf-8',
      },
    });
  },
};
