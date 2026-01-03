#!/usr/bin/env bash
# Exemplos de chamadas para o endpoint /detect (assegure-se que o servidor esteja rodando)

set -euo pipefail

echo "Exemplo: Visa (válido)"
curl -s -X POST http://127.0.0.1:8000/detect -H 'Content-Type: application/json' -d '{"number":"4111111111111111","require_luhn":false}' | jq || true

echo "\nExemplo: Luhn inválido (retorna brand: null quando require_luhn=true)"
curl -s -X POST http://127.0.0.1:8000/detect -H 'Content-Type: application/json' -d '{"number":"411111111111112","require_luhn":true}' | jq || true
