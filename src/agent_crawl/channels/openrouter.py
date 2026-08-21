from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from agent_crawl.config import read_secret
from agent_crawl.models import error, ok, unavailable


def list_models(limit: int = 20) -> object:
    api_key = os.environ.get("OPENROUTER_API_KEY") or read_secret("token", "openrouter")
    headers = {"User-Agent": "agent-crawl-kit/0.1"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    request = Request("https://openrouter.ai/api/v1/models", headers=headers)
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (HTTPError, URLError, TimeoutError) as exc:
        return error("https://openrouter.ai/api/v1/models", str(exc))
    except json.JSONDecodeError as exc:
        return error("https://openrouter.ai/api/v1/models", f"invalid JSON response: {exc}")

    models = payload.get("data")
    if not isinstance(models, list):
        return unavailable("https://openrouter.ai/api/v1/models", "OpenRouter models response did not contain a data list")
    return ok(
        "https://openrouter.ai/api/v1/models",
        {
            "configured": bool(api_key),
            "items": models[:limit],
            "count": min(len(models), limit),
        },
    )

