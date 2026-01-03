import subprocess
import time

import pytest
import requests

try:
    from playwright.sync_api import sync_playwright
except Exception:  # pragma: no cover - skip if playwright not installed
    pytest.skip("Playwright not installed; skipping E2E tests", allow_module_level=True)

import os
from pathlib import Path

SERVER_URL = "http://127.0.0.1:8002"


def wait_for_server(url: str, timeout: int = 10.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            r = requests.get(f"{url}/openapi.json", timeout=1)
            if r.status_code == 200:
                return True
        except Exception:
            pass
        time.sleep(0.2)
    return False


def test_web_ui_detects_brand_and_luhn():
    # Start uvicorn server on port 8002
    proc = subprocess.Popen(
        [
            "./.venv/bin/python",
            "-m",
            "uvicorn",
            "examples.fastapi_app:app",
            "--port",
            "8002",
        ]
    )
    try:
        assert wait_for_server(SERVER_URL, timeout=15), "Server did not start in time"

        with sync_playwright() as p:
            # Choose browser from env or default to chromium
            browser_name = os.environ.get("PLAYWRIGHT_BROWSER", "chromium")
            browser_launcher = getattr(p, browser_name)

            art_dir = Path("tests/e2e/artifacts")
            art_dir.mkdir(parents=True, exist_ok=True)

            browser = browser_launcher.launch(headless=True)
            context = browser.new_context()
            # Start tracing to capture snapshots and sources
            try:
                context.tracing.start(screenshots=True, snapshots=True, sources=True)
            except Exception:
                pass
            page = context.new_page()
            page.goto(SERVER_URL + "/")

            try:
                # Type a known Visa number and wait for Luhn indicator
                page.fill("#number", "4111111111111111")
                page.wait_for_selector("#luhn-status.text-success", timeout=3000)
                # Brand hint should update
                hint = page.text_content("#brand-hint")
                assert "Visa" in hint

                # Click detect and check output
                page.click("#go")
                page.wait_for_selector("#output", timeout=3000)
                assert "Visa" in page.text_content("#brand")
                assert "Sim" in page.text_content("#luhn")

            except Exception:  # pragma: no cover - capture artifacts on failure
                screenshot = art_dir / f"failure-{browser_name}.png"
                trace = art_dir / f"trace-{browser_name}.zip"
                try:
                    page.screenshot(path=str(screenshot))
                except Exception:
                    pass
                try:
                    context.tracing.stop(path=str(trace))
                except Exception:
                    pass
                raise
            finally:
                try:
                    context.close()
                except Exception:
                    pass
                try:
                    browser.close()
                except Exception:
                    pass
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=3)
        except Exception:
            proc.kill()
