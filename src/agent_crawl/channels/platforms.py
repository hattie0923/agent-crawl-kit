from __future__ import annotations

import shutil
import subprocess

from agent_crawl.models import error, ok, unavailable


def search_platform(platform: str, query: str, limit: int = 10) -> object:
    platform_key = platform.lower()
    routes = {
        "bilibili": [["bili", "search", query, "--type", "video", "-n", str(limit)]],
        "twitter": [["twitter", "search", query, "-n", str(limit)], ["opencli", "twitter", "search", query, "-f", "yaml"]],
        "x": [["twitter", "search", query, "-n", str(limit)], ["opencli", "twitter", "search", query, "-f", "yaml"]],
        "reddit": [["opencli", "reddit", "search", query, "-f", "yaml"], ["rdt", "search", query, "--limit", str(limit)]],
        "xiaohongshu": [["opencli", "xiaohongshu", "search", query, "-f", "yaml"]],
        "xhs": [["opencli", "xiaohongshu", "search", query, "-f", "yaml"]],
        "facebook": [["opencli", "facebook", "search", query, "-f", "yaml"]],
        "instagram": [["opencli", "instagram", "search", query, "-f", "yaml"]],
        "linkedin": [["opencli", "linkedin", "search", query, "-f", "yaml"]],
    }
    commands = routes.get(platform_key)
    if not commands:
        return unavailable(None, f"unsupported platform: {platform}")

    skipped: list[str] = []
    for command in commands:
        binary = command[0]
        if not shutil.which(binary):
            skipped.append(binary)
            continue
        try:
            completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=90)
        except Exception as exc:  # noqa: BLE001 - CLI should return structured failures.
            return error(None, str(exc))
        if completed.returncode == 0:
            return ok(
                None,
                {
                    "platform": platform_key,
                    "query": query,
                    "backend": binary,
                    "raw": completed.stdout.strip(),
                },
            )
        last_error = completed.stderr.strip() or completed.stdout.strip()
        return error(None, f"{binary} failed: {last_error}")

    return unavailable(None, f"no backend installed for {platform}; missing: {', '.join(skipped)}")

