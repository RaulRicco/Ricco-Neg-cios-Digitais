/**
 * Cloudflare Worker — Basic Auth para dashboards de clientes
 * Domínio: dash.raulricco.com.br
 *
 * Cada rota /slug-do-cliente exige uma senha configurada em CLIENTES abaixo.
 * Adicionar novo cliente = adicionar uma linha no objeto CLIENTES.
 *
 * Rotas em PUBLIC_PASSTHROUGH não passam pelo Basic Auth do browser —
 * usadas quando a própria página já tem sua tela de senha (ex: aditivos/propostas).
 */

const PUBLIC_PASSTHROUGH = new Set([
  'aditivo-seu-barbudo',
]);

const CLIENTES = {
  'acougueiro-agua-verde':  'aguaverde2026',
  'acougueiro-bacacheri':   'bacacheri2026',
  'acougueiro-batel':       'batel2026',
  'quermesse-bom-retiro':   'bomretiro2026',
  'quermesse-ecoville':     'ecoville2026',
  'floreria':               'floreria2026',
  'boi-dourado':            'boidourado2026',
  'bebedouro':              'bebedouro2026',
  'bebedouro-356':          'bebedouro356@2026',
  'balcao-savassi':         'balcaosavassi2026',
  'ameriparts':             'ameriparts2026',
  'comodoro-burguer':       'comodoro2026',
  'bsbichos':               'bsbichos2026',
  'bistecao':               'bistecao2026',
  'garage-burger':          'garageburger2026',
  'dona-cleide':            'donacleide2026',
  'seu-barbudo':            'barbudo2026',
  'horus':                  'horus2026',
  'sol-e-lar':              'solelar2026',
  'solar-e-cia':            'solarecia2026',
  'fish-me':                'fishme2026',
  'porks-asa-sul':          'porksasasul2026',
  'porks-asa-norte':        'porksasanorte2026',
  'porks-samambaia':        'porkssam2026',
  'porks-guara':            'porksguara2026',
  'porks-tres-lagoas':      'porkstl2026',
  'porks-casarao':          'porkscasarao2026',
  'porks-castelo':          'porkscastelo2026',
  'porks-pirenopolis':      'porkspiri2026',
  'boteco-do-quintal':      'botecodomquintal2026',
  'quintal-piri':           'quintalpiri2026',
};

const REALM = 'Dashboard Ricco';

export default {
  async fetch(request) {
    const url  = new URL(request.url);
    // Extrai o slug da rota: /acougueiro-agua-verde → 'acougueiro-agua-verde'
    const slug = url.pathname.replace(/^\//, '').split('/')[0];

    // Rota raiz — sem autenticação, retorna 404 simples
    if (!slug) return new Response('Not found', { status: 404 });

    // Rotas com senha própria na página — passa direto pro Pages
    if (PUBLIC_PASSTHROUGH.has(slug)) {
      return fetch(request);
    }

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
