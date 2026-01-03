# Exemplos de Inputs / Outputs

Casos de teste e exemplos reais:

| Número              | Bandeira esperada | Luhn |
| ------------------- | ----------------- | ---- |
| 4111 1111 1111 1111 | Visa              | True |
| 5555 5555 5555 4444 | MasterCard        | True |
| 3782 822463 10005   | American Express  | True |
| 6011 1111 1111 1117 | Discover          | True |
| 3530 1113 3330 0000 | JCB               | True |
| 3056 9309 0259 04   | Diners Club       | True |

Observações:

- Números de exemplo são números de teste amplamente divulgados para fins de validação e não representam cartões reais.
- A função `detect_brand` retorna `"Unknown"` quando nenhum padrão é reconhecido; se `validate_luhn=True` e o Luhn falhar, retorna `None`.

Scripts de demonstração:

- `examples/scripts/demo_lib.py` — demonstra uso das funções `detect_brand` e `is_luhn_valid`.
- `examples/scripts/run_fastapi.sh` — inicia o servidor FastAPI de exemplo (requer `uvicorn`).
- `examples/scripts/curl_examples.sh` — exemplos de chamadas `curl` ao endpoint `/detect` (requer servidor rodando e `jq` para saída formatada).
