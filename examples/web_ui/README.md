# Web UI Example

Roda uma página simples para inserir número do cartão e ver a bandeira e Luhn.

Recursos adicionados:

- Estilização com **Bootstrap (CDN)** para um layout mais agradável.
- Máscara/formatação automática (grupos de 4 dígitos) enquanto digita.
- Validação _Luhn_ em tempo real no cliente (mostra visualmente `Sim` / `Não`).
- Se `Exigir Luhn válido` estiver marcado, o botão **Detectar** é desabilitado até o Luhn ser válido.

Como usar:

1. Ative o venv (recomendado):

```bash
source .venv/bin/activate
```

2. Instale dependências (opcionais):

```bash
python -m pip install fastapi uvicorn
```

3. Rode o app:

```bash
python -m uvicorn examples.fastapi_app:app --reload
```

4. Abra no navegador: `http://127.0.0.1:8000/`

Observação: este é um exemplo para demonstração — para produção, acrescente validações de segurança, proteja endpoints e não confie apenas em validações no cliente.

Recursos visuais adicionais

- Ícones SVG das bandeiras (ex: `examples/static/icons/*.svg`) são usados para um feedback visual mais claro.
- O título possui animação sutil e gradiente em roxo.

Testes E2E com Playwright (opcional)

1. Instale as dependências de teste:

```bash
source .venv/bin/activate
python -m pip install playwright requests pytest
python -m playwright install chromium
```

2. Execute os testes E2E:

```bash
pytest tests/e2e/test_web_ui.py -q
```

Nota: os testes usam o Playwright (Chromium). Se preferir executar no CI, adicione um workflow que instale os navegadores (ex.: `playwright install`) e tenha suporte a navegadores headless.
