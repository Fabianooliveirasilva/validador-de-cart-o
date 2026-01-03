# Validador de Bandeiras de Cartão ✅

[![CI](https://github.com/OWNER/REPO/actions/workflows/python-package.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/python-package.yml) [![Lint](https://github.com/OWNER/REPO/actions/workflows/lint.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/lint.yml) [![E2E](https://github.com/OWNER/REPO/actions/workflows/e2e.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/e2e.yml) [![Release Drafter](https://github.com/OWNER/REPO/actions/workflows/release-drafter.yml/badge.svg)](https://github.com/OWNER/REPO/actions/workflows/release-drafter.yml) [![PyPI](https://img.shields.io/pypi/v/validador-bandeiras?label=PyPI&color=blue)](https://pypi.org/project/validador-bandeiras/) [![Cheat Sheet](https://img.shields.io/badge/CHEAT-SHEET-blue?style=flat)](CHEATSHEET.md)

**Detecte bandeiras de cartão (Visa, MasterCard, Amex, Discover, JCB, Diners) e valide o dígito verificador (Luhn) — leve e testado.**

> Substitua `OWNER/REPO` nas URLs dos badges pelos valores do seu repositório GitHub para ativar os badges.

---

## 🚀 Visão geral

Validador de Bandeiras é uma pequena biblioteca em Python que fornece:

- Detecção de bandeira a partir do número do cartão (`detect_brand`)📇
- Validação do dígito verificador (algoritmo Luhn) (`is_luhn_valid`) ✔️
- CLI simples para uso em linha de comando 🖥️
- Exemplo de API com FastAPI para integração via HTTP 🌐
- Testes, linting e workflows de CI configurados ✅

---

## 📁 Estrutura do projeto

- `src/validador_bandeiras/` - package principal
  - `detector.py` - limpeza de input, Luhn e `detect_brand`
  - `patterns.py` - regex/ranges por bandeira
  - `cli.py` - entrypoint CLI
- `tests/` - casos de teste com `pytest`
- `examples/` - exemplos e scripts (FastAPI + demos)
- `docs/` - documentação técnica e exemplos
- `.github/workflows/` - CI: testes, lint e E2E

---

## 📦 Instalação (desenvolvimento)

Recomenda-se usar um virtualenv:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -U pytest black ruff
```

Instale dependências opcionais para a API/example:

```bash
python -m pip install fastapi uvicorn httpx jq
```

---

## ▶️ Uso

### CLI

```bash
python -m validador_bandeiras.cli "4111 1111 1111 1111"
# Com Luhn obrigatório (retorna Unknown/None quando inválido)
python -m validador_bandeiras.cli --require-luhn "4111 1111 1111 1111"
```

### Biblioteca (Python)

```python
from validador_bandeiras import detect_brand, is_luhn_valid

num = "378282246310005"
print(detect_brand(num))     # -> 'American Express'
print(is_luhn_valid(num))    # -> True
```

### Exemplo FastAPI (local)

Rode o servidor:

```bash
python -m uvicorn examples.fastapi_app:app --reload
```

POST /detect (JSON):

```json
{ "number": "4111111111111111", "require_luhn": false }
```

Resposta:

```json
{ "brand": "Visa", "luhn_valid": true }
```

> Nota: se `require_luhn=true` e o Luhn falhar, a API retorna `brand: null`.

---

## � Cheat sheet rápido

Para comandos práticos, exemplos de uso e passos de instalação, veja `CHEATSHEET.md`.

---

## �🧪 Testes & Lint

Execute:

```bash
# Testes
python -m pytest -q

# Lint
ruff check .

# Formatação
black .
```

Também há um alvo `Makefile` para facilitar:

```bash
make test
make lint
make format
```

---

## 🔬 Testes end-to-end

Há um workflow de E2E (`.github/workflows/e2e.yml`) que inicia o servidor FastAPI, executa dois smoke tests e finaliza o servidor. Localmente você pode executar:

```bash
make e2e
```

---

## 🛠️ Contribuição

Veja `CONTRIBUTING.md` para guias de estilo, como rodar os testes e usar `pre-commit` (Black + Ruff). Use as labels (`feature`, `bug`, `documentation`, `tests`) ao abrir PRs para ajudar a gerar changelogs automáticos.

---

## 📣 Publicação

Para construir e publicar no PyPI:

```bash
python -m pip install -U build twine
python -m build
python -m twine upload dist/*
```

Há um workflow de release que publica quando uma tag `vX.Y.Z` é criada (requer `PYPI_API_TOKEN` configurado no repositório).

---

## 📄 Segurança

Veja `SECURITY.md` para instruções de reporte responsável (atualmente com um placeholder de e-mail — substitua antes de publicar o repositório).

---

## 🧾 Changelog

Ver `CHANGELOG.md` para histórico de alterações.

---

## ✨ Observações finais

- Números de cartão usados nos exemplos são apenas números de teste amplamente divulgados (não reais).
- A detecção cobre Visa, MasterCard, American Express, Discover, JCB e Diners Club por padrão; contribuições para adicionar outras bandeiras são bem-vindas.

---

Se quiser, eu também:

- adiciono badges de CI/coverage/packaging na parte superior; ou
- gero um `README.md` pronto para o GitHub com imagens/badges e um resumo curto para o cabeçalho.

Diga se prefere que eu já inclua badges e um resumo visual (Sim/Não).
