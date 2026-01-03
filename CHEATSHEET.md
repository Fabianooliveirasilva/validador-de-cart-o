# CHEATSHEET — Validador de Bandeiras de Cartão

Guia rápido com comandos práticos para rodar o projeto localmente.

---

## 1) Preparar ambiente

Linux / macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

---

## 2) Instalar dependências

Dependências de desenvolvimento:

```bash
python -m pip install -U pytest black ruff
```

Dependências para exemplos / API (opcional):

```bash
python -m pip install fastapi uvicorn httpx jq
```

---

## 3) Testes, lint e formatação

```bash
# Testes
python -m pytest -q

# Lint
ruff check .

# Formatar
black .

# Alternativa com Makefile
make test
make lint
make format
```

---

## 4) CLI

```bash
# Detecta bandeira
python -m validador_bandeiras.cli "4111 1111 1111 1111"

# Exige Luhn válido
python -m validador_bandeiras.cli --require-luhn "4111 1111 1111 1111"
```

---

## 5) Scripts de demonstração

```bash
# Demo da biblioteca
python examples/scripts/demo_lib.py
python examples/scripts/demo_lib.py 4111111111111111

# Iniciar FastAPI (local)
python -m uvicorn examples.fastapi_app:app --reload

# Exemplos curl (requer servidor rodando e jq)
bash examples/scripts/curl_examples.sh
```

---

## 6) Teste rápido da API (curl)

```bash
# Valido
curl -s -X POST http://127.0.0.1:8000/detect -H 'Content-Type: application/json' -d '{"number":"4111111111111111","require_luhn":false}'

# Luhn inválido
curl -s -X POST http://127.0.0.1:8000/detect -H 'Content-Type: application/json' -d '{"number":"411111111111112","require_luhn":true}'
```

---

## 7) Testes end-to-end (smoke)

Local:

```bash
make e2e
```

O workflow de CI E2E está em `.github/workflows/e2e.yml`.

---

## 8) Build & publish

```bash
python -m pip install -U build twine
python -m build
python -m twine upload dist/*
```

> Configure `PYPI_API_TOKEN` no repositório para publicação automática via GitHub Actions.

---

## 9) Comandos úteis

```bash
# Sanity: formata + lint + testes
make format && make lint && make test

# Rodar uvicorn sem ativar venv (quando existir .venv)
.venv/bin/python -m uvicorn examples.fastapi_app:app --reload
```

---

## 10) Problemas comuns

- `uvicorn not found` → `python -m pip install -U uvicorn`
- `python: not found` em Make → ative `.venv` ou use `make` após ativar o venv
- `jq` não instalado → `sudo apt install jq` / `brew install jq`

---

## 11) Observações finais

- `SECURITY.md` contém placeholder de e-mail — substitua antes de publicar.
- A API retorna `{"brand": null}` quando `require_luhn=true` e o Luhn é inválido (comportamento intencional).

---

Se quiser, eu adiciono este `CHEATSHEET.md` ao `README` ou crio uma versão reduzida para um `QuickStart` na página do GitHub. Quer que eu insira um link no `README` para este cheat-sheet? (Sim/Não)
