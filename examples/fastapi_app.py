"""Exemplo opcional: app FastAPI para detecção (instalar fastapi + uvicorn)"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from validador_bandeiras import detect_brand, is_luhn_valid

app = FastAPI(title="Validador de Bandeiras")

# Serve example static assets (icons used by the demo UI)
app.mount("/static", StaticFiles(directory="examples/static"), name="static")


class CardIn(BaseModel):
    number: str
    require_luhn: bool = False


@app.post("/detect")
def detect(card: CardIn):
    brand = detect_brand(card.number, validate_luhn=card.require_luhn)
    return {"brand": brand, "luhn_valid": is_luhn_valid(card.number)}


@app.get("/", response_class=HTMLResponse)
def ui():
    """Página HTML simples para inserir número e mostrar resultado"""
    return r"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Validador de Bandeiras</title>
    <!-- Bootstrap CSS CDN -->
    <link
      href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css"
      rel="stylesheet"
      integrity="sha384-..."
      crossorigin="anonymous"
    >
    <style>
      /* Full-page gradient with centered card */
      body {
        font-family: system-ui, -apple-system, 'Segoe UI', Roboto,
          'Helvetica Neue', Arial;
        min-height: 100vh;
        margin: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2rem;
        background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #4ca1af 100%);
      }

      /* Card that holds the UI */
      .ui-card {
        width: 100%;
        max-width: 880px;
        background: rgba(255, 255, 255, 0.98);
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
        padding: 1.5rem 1.25rem;
      }

      .result {
        margin-top: 1rem;
        padding: 1rem;
        border-radius: 6px;
        background: #f7f7f8;
      }

      /* Title with eye-catching gradient text */
      .brand-title {
        font-weight: 800;
        font-size: 1.5rem;
        line-height: 1.1;
        background: linear-gradient(45deg, #9b5de5, #7b2cbf);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: titlePulse 3s ease-in-out infinite;
      }

      @keyframes titlePulse {
        0%, 100% { transform: scale(1); filter: brightness(1); }
        50% { transform: scale(1.03); filter: brightness(1.08); }
      }

      /* Brand icon styles */
      .brand-icon {
        width: 48px;
        height: auto;
        border-radius: 6px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.08);
      }
      .brand-icon-sm {
        width: 36px;
        height: auto;
        border-radius: 6px;
        box-shadow: 0 3px 6px rgba(0,0,0,0.06);
      }
      .muted { color: #666; font-size: 0.9rem }
      #luhn-status { font-weight: 600 }

      /* Small brand-like badges */
      #brand-hint { font-weight: 700 }
      .brand-visa { background: #1a1f71 !important; color: #fff }
      .brand-mastercard {
        background: linear-gradient(90deg,#ff5f00,#eb001b) !important;
        color: #fff
      }
      .brand-american { background: #2e77bb !important; color: #fff }
      .brand-discover { background: #f76b1c !important; color: #fff }
      .brand-jcb { background: #2b2e83 !important; color: #fff }
      .brand-diners { background: #006064 !important; color: #fff }
    </style>
  </head>
  <body>
    <div class="ui-card container">
      <header class="mb-4">
        <h1 class="h3 brand-title">Validador de Bandeiras</h1>
        <p class="muted">
          Insira o número do cartão (pode conter espaços ou hífens).
          Você terá feedback imediato do Luhn e pode <strong>Detectar</strong>
          para ver a bandeira.
        </p>
      </header>

      <div class="mb-3">
        <label for="number" class="form-label">Número do cartão</label>
        <input
          id="number"
          class="form-control form-control-lg"
          type="text"
          placeholder="4111 1111 1111 1111"
          inputmode="numeric"
          autocomplete="cc-number"
        />
        <div class="form-text">
          Formatação automática em grupos de 4 dígitos.
          Apenas dígitos são considerados.
        </div>
      </div>

      <div class="d-flex align-items-center gap-3 mb-3">
        <div class="form-check">
          <input id="require" class="form-check-input" type="checkbox" />
          <label class="form-check-label" for="require">Exigir Luhn válido</label>
        </div>
        <button id="go" class="btn btn-primary btn-lg">Detectar</button>
        <div id="live-luhn" class="ms-3 text-muted">
          Luhn: <span id="luhn-status">—</span>
        </div>
        <div class="ms-3 d-flex align-items-center gap-2 ms-auto">
          <img id="brand-icon" src="" alt="" class="brand-icon" hidden />
          <span id="brand-hint" class="badge bg-secondary">—</span>
        </div>
      </div>

      <div id="output" class="result" aria-live="polite" hidden>
        <div class="mb-2 d-flex align-items-center gap-2"><strong>Bandeira:</strong>
          <img id="output-icon" src="" alt="" class="brand-icon-sm" hidden />
          <span id="brand">-</span>
        </div>
        <div><strong>Luhn válido:</strong> <span id="luhn">-</span></div>
      </div>

      <footer class="mt-4 text-muted small">
        Exemplo simples — para produção, realize validações adicionais e
        proteja endpoints.
      </footer>
    </div>

    <script>
      const numberInput = document.getElementById('number');
      const requireBox = document.getElementById('require');
      const go = document.getElementById('go');
      const output = document.getElementById('output');
      const brandEl = document.getElementById('brand');
      const luhnEl = document.getElementById('luhn');
      const luhnStatus = document.getElementById('luhn-status');
      const brandHint = document.getElementById('brand-hint');

      function onlyDigits(s) {
        return s.replace(/\D/g, '');
      }

      function formatCardNumber(s) {
        const d = onlyDigits(s);
        return d.replace(/(\d{4})(?=\d)/g, '$1 ').trim();
      }

      function luhnCheck(num) {
        const s = onlyDigits(num);
        let sum = 0;
        let alt = false;
        for (let i = s.length - 1; i >= 0; i--) {
          let n = parseInt(s.charAt(i), 10);
          if (alt) {
            n *= 2;
            if (n > 9) n -= 9;
          }
          sum += n;
          alt = !alt;
        }
        return s.length >= 12 && sum % 10 === 0;
      }

      function detectBrandJS(num) {
        const s = onlyDigits(num);
        if (!s) return null;
        const patterns = {
          Visa: /^4\d{12}(?:\d{3}){0,2}$/, // 13,16,19
          'American Express': /^3[47]\d{13}$/, // 15
          'Diners Club': /^3(?:0[0-5]|[68]\d)\d{11}$/, // 14/16ish
          JCB: /^35(?:2[89]|[3-8]\d)\d{12}$/,
        };
        for (const [name, rx] of Object.entries(patterns)) {
          if (rx.test(s)) return name;
        }
        function isMastercard(n) {
          if (n.length !== 16) return false;
          const firstTwo = parseInt(n.slice(0, 2) || '0', 10);
          const firstSix = parseInt(n.slice(0, 6) || '0', 10);
          if (51 <= firstTwo && firstTwo <= 55) return true;
          if (222100 <= firstSix && firstSix <= 272099) return true;
          return false;
        }
        function isDiscover(n) {
          if (![16, 19].includes(n.length)) return false;
          if (n.startsWith('6011') || n.startsWith('65')) return true;
          const firstThree = parseInt(n.slice(0, 3) || '0', 10);
          if (644 <= firstThree && firstThree <= 649) return true;
          const firstSix = parseInt(n.slice(0, 6) || '0', 10);
          if (622126 <= firstSix && firstSix <= 622925) return true;
          return false;
        }
        if (isMastercard(s)) return 'MasterCard';
        if (isDiscover(s)) return 'Discover';
        return 'Unknown';
      }

      function updateLive() {
        const val = numberInput.value;
        const digits = onlyDigits(val);
        numberInput.value = formatCardNumber(val);
        if (digits.length === 0) {
          luhnStatus.textContent = '—';
          luhnStatus.className = '';
          brandHint.textContent = '—';
          brandHint.className = 'badge bg-secondary';
          go.disabled = false;
          return;
        }
        const ok = luhnCheck(digits);
        luhnStatus.textContent = ok ? 'Sim' : 'Não';
        luhnStatus.className = ok ? 'text-success' : 'text-danger';
        // Se exigir Luhn e inválido, desabilita botão
        if (requireBox.checked && !ok) {
          go.disabled = true;
        } else {
          go.disabled = false;
        }
        // Atualiza hint de bandeira (rápido, sem Luhn)
        const b = detectBrandJS(digits);
        let className = 'badge';
        if (b === 'Visa') className += ' brand-visa';
        else if (b === 'MasterCard') className += ' brand-mastercard';
        else if (b === 'American Express') className += ' brand-american';
        else if (b === 'Discover') className += ' brand-discover';
        else if (b === 'JCB') className += ' brand-jcb';
        else if (b === 'Diners Club') className += ' brand-diners';
        else className += ' bg-secondary';
        brandHint.textContent = b || '—';
        brandHint.className = className;

        // Atualiza ícone (se disponível)
        const iconMap = {
          Visa: '/static/icons/visa.svg',
          'MasterCard': '/static/icons/mastercard.svg',
          'American Express': '/static/icons/american_express.svg',
          Discover: '/static/icons/discover.svg',
          JCB: '/static/icons/jcb.svg',
          'Diners Club': '/static/icons/diners.svg',
        };
        const icon = iconMap[b];
        if (icon) {
          brandIcon.src = icon;
          brandIcon.alt = b;
          brandIcon.hidden = false;
        } else {
          brandIcon.hidden = true;
          brandIcon.src = '';
          brandIcon.alt = '';
        }
      }

      async function detect() {
        const num = numberInput.value.trim();
        if (!onlyDigits(num)) {
          alert('Insira um número de cartão válido.');
          return;
        }
        // Se exigir Luhn, verifique localmente antes de enviar
        if (requireBox.checked && !luhnCheck(num)) {
          alert('Luhn inválido. Marque um número válido ou desmarque "Exigir Luhn".');
          return;
        }
        go.disabled = true;
        go.textContent = 'Detectando...';
        try {
          const resp = await fetch('/detect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ number: num, require_luhn: requireBox.checked })
          });
          const data = await resp.json();
          brandEl.textContent = data.brand === null
            ? 'Nenhuma (Luhn inválido)'
            : (data.brand || 'Unknown');
          luhnEl.textContent = data.luhn_valid ? 'Sim' : 'Não';
          // Atualiza ícone de saída
          const outIconMap = {
            Visa: '/static/icons/visa.svg',
            'MasterCard': '/static/icons/mastercard.svg',
            'American Express': '/static/icons/american_express.svg',
            Discover: '/static/icons/discover.svg',
            JCB: '/static/icons/jcb.svg',
            'Diners Club': '/static/icons/diners.svg',
          };
          const outIcon = outIconMap[data.brand];
          if (outIcon) {
            const oi = document.getElementById('output-icon');
            oi.src = outIcon;
            oi.alt = data.brand || '';
            oi.hidden = false;
          }
          output.hidden = false;
        } catch (err) {
          alert('Erro: ' + err.message);
        } finally {
          go.disabled = false;
          go.textContent = 'Detectar';
        }
      }

      numberInput.addEventListener('input', updateLive);
      requireBox.addEventListener('change', updateLive);
      go.addEventListener('click', detect);
      numberInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') detect();
      });
    </script>

    <!-- Bootstrap JS bundle (optional) -->
    <script
      src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
      integrity="sha384-..."
      crossorigin="anonymous"
    ></script>
  </body>
</html>"""
