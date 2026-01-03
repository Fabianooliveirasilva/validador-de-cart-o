# Examples

Scripts úteis para demonstrar o uso do projeto:

- `examples/scripts/demo_lib.py` — demonstra uso das funções `detect_brand` e `is_luhn_valid`.

  - Exemplo: `python examples/scripts/demo_lib.py`
  - Testar um cartão específico: `python examples/scripts/demo_lib.py 4111111111111111`

- `examples/scripts/run_fastapi.sh` — script para iniciar o servidor FastAPI de exemplo (requer `uvicorn`).

  - Exemplo: `bash examples/scripts/run_fastapi.sh`

- `examples/scripts/curl_examples.sh` — exemplos de chamadas `curl` ao endpoint `/detect` (requer servidor rodando e `jq` para saída formatada).
  - Exemplo: `bash examples/scripts/curl_examples.sh`
