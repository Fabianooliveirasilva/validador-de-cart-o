# Uso

Este documento mostra como utilizar o validador de bandeiras.

## CLI

Exemplos:

```bash
# Detectar sem exigir Luhn
python -m validador_bandeiras.cli "4111 1111 1111 1111"

# Detectar e exigir Luhn válido
python -m validador_bandeiras.cli --require-luhn "4111 1111 1111 1111"
```

Saída esperada:

```
Brand: Visa
Luhn válido: True
```

## API FastAPI (exemplo)

Enviar POST para `/detect` com JSON:

```json
{ "number": "4111111111111111", "require_luhn": false }
```

Resposta:

```json
{ "brand": "Visa", "luhn_valid": true }
```
