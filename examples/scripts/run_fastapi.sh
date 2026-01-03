#!/usr/bin/env bash
# Inicie o servidor FastAPI de exemplo:
# uvicorn examples.fastapi_app:app --reload --host 127.0.0.1 --port 8000

if ! command -v uvicorn >/dev/null 2>&1; then
  echo "uvicorn não encontrado. Instale com: python -m pip install uvicorn"
  exit 1
fi

echo "Iniciando uvicorn em http://127.0.0.1:8000 (CTRL+C para parar)"
exec uvicorn examples.fastapi_app:app --reload --host 127.0.0.1 --port 8000
