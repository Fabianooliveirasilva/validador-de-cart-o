PYTHON := $(shell [ -x .venv/bin/python ] && echo .venv/bin/python || echo python3)
.PHONY: test lint format build publish clean e2e e2e-ci

test:
	$(PYTHON) -m pytest -q

lint:
	ruff check .

format:
	black .

build:
	$(PYTHON) -m pip install -U build
	$(PYTHON) -m build

publish:
	$(PYTHON) -m pip install -U twine
	twine upload dist/*

# End-to-end smoke test (local)
e2e:
	$(PYTHON) -m pip install -U uvicorn jq || true
	@echo "Starting uvicorn in background..."
	$(PYTHON) -m uvicorn examples.fastapi_app:app --host 127.0.0.1 --port 8000 > /tmp/uvicorn_e2e_local.log 2>&1 & echo $$! > /tmp/uvicorn_e2e.pid || true
	@PID=$$(cat /tmp/uvicorn_e2e.pid 2>/dev/null || echo); \
	if [ -n "$$PID" ] && kill -0 $$PID 2>/dev/null; then \
		echo "uvicorn started (pid $$PID)"; \
	else \
		echo "uvicorn failed to start, output:"; tail -n 200 /tmp/uvicorn_e2e_local.log; exit 1; \
	fi
	@for i in 1 2 3 4 5 6 7 8 9 10; do \
		if curl -sSf http://127.0.0.1:8000/openapi.json >/dev/null 2>&1; then \
			echo "server ready" && break; \
		fi; \
		sleep 1; \
	done
	@echo "Running smoke tests..."
	@curl -s -X POST http://127.0.0.1:8000/detect -H 'Content-Type: application/json' -d '{"number":"4111111111111111","require_luhn":false}' | jq -e '.brand == "Visa" and .luhn_valid == true'
	@curl -s -X POST http://127.0.0.1:8000/detect -H 'Content-Type: application/json' -d '{"number":"411111111111112","require_luhn":true}' | jq -e '.brand == null and .luhn_valid == false'
	@echo "Stopping uvicorn..."
	@if [ -f /tmp/uvicorn_e2e.pid ]; then \
		PID=$$(cat /tmp/uvicorn_e2e.pid); \
		if kill -0 $$PID 2>/dev/null; then \
			kill $$PID || true; \
		fi; \
		rm -f /tmp/uvicorn_e2e.pid; \
	else \
		echo "No pid file found, skipping kill"; \
	fi

# Playwright end-to-end test (local)
e2e-playwright:
	$(PYTHON) -m pip install -U playwright requests pytest || true
	$(PYTHON) -m playwright install chromium
	@echo "Starting uvicorn in background (port 8002)..."
	$(PYTHON) -m uvicorn examples.fastapi_app:app --host 127.0.0.1 --port 8002 > /tmp/uvicorn_e2e_playwright.log 2>&1 & echo $$! > /tmp/uvicorn_e2e_playwright.pid || true
	@for i in 1 2 3 4 5 6 7 8 9 10; do \
		if curl -sSf http://127.0.0.1:8002/openapi.json >/dev/null 2>&1; then \
			echo "server ready" && break; \
		fi; \
		sleep 1; \
	done
	$(PYTHON) -m pytest tests/e2e/test_web_ui.py -q
	@echo "Stopping uvicorn..."
	@if [ -f /tmp/uvicorn_e2e_playwright.pid ]; then \
		PID=$$(cat /tmp/uvicorn_e2e_playwright.pid); \
		if kill-0 $$PID 2>/dev/null; then \
			kill $$PID || true; \
		fi; \
		rm -f /tmp/uvicorn_e2e_playwright.pid; \
	else \
		echo "No pid file found, skipping kill"; \
	fi

# End-to-end smoke test for CI (non-interactive, fails on errors)
e2e-ci:
	$(PYTHON) -m pip install -U uvicorn jq
	$(PYTHON) -m uvicorn examples.fastapi_app:app --host 127.0.0.1 --port 8000 > uvicorn.log 2>&1 & echo $$! > uvicorn.pid
	@for i in 1 2 3 4 5 6 7 8 9 10; do \
		if curl -sSf http://127.0.0.1:8000/openapi.json >/dev/null 2>&1; then \
			echo "server ready" && break; \
		fi; \
		sleep 1; \
	done
	curl -s -X POST http://127.0.0.1:8000/detect -H 'Content-Type: application/json' -d '{"number":"4111111111111111","require_luhn":false}' | jq -e '.brand == "Visa" and .luhn_valid == true'
	curl -s -X POST http://127.0.0.1:8000/detect -H 'Content-Type: application/json' -d '{"number":"411111111111112","require_luhn":true}' | jq -e '.brand == null and .luhn_valid == false'
	@if [ -f uvicorn.pid ]; then \
		kill "$(cat uvicorn.pid)" || true; \
		rm -f uvicorn.pid; \
	else \
		echo "No pid file found, skipping kill"; \
	fi

clean:
	rm -rf build dist *.egg-info
