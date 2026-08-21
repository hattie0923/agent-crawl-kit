from __future__ import annotations

import json
import shutil
import subprocess

from agent_crawl.models import error, ok, unavailable


def search_web(query: str, limit: int = 5) -> object:
    if not shutil.which("mcporter"):
        return unavailable(None, "`mcporter` is not installed; configure a supported search backend first")
    expression = f'exa.web_search_exa(query: "{_escape(query)}", numResults: {limit})'
    command = ["mcporter", "call", expression]
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=60)
    except Exception as exc:  # noqa: BLE001 - CLI should return structured failures.
        return error(None, str(exc))
    if completed.returncode != 0:
        return error(None, completed.stderr.strip() or completed.stdout.strip())
    return ok(None, {"query": query, "raw": _maybe_json(completed.stdout)})


def _escape(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _maybe_json(value: str) -> object:
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value.strip()

