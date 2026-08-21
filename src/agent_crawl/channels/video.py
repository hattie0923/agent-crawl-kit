from __future__ import annotations

import json
import shutil
import subprocess

from agent_crawl.models import error, ok, unavailable


def inspect_video(url: str) -> object:
    if not shutil.which("yt-dlp"):
        return unavailable(url, "`yt-dlp` is not installed")
    command = ["yt-dlp", "--dump-json", "--skip-download", url]
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=60)
    except Exception as exc:  # noqa: BLE001 - CLI should return structured failures.
        return error(url, str(exc))
    if completed.returncode != 0:
        return error(url, completed.stderr.strip() or completed.stdout.strip())
    payload = json.loads(completed.stdout.splitlines()[0])
    return ok(
        url,
        {
            "title": payload.get("title"),
            "channel": payload.get("channel") or payload.get("uploader"),
            "duration": payload.get("duration"),
            "webpage_url": payload.get("webpage_url"),
            "subtitles": sorted((payload.get("subtitles") or {}).keys()),
            "automatic_captions": sorted((payload.get("automatic_captions") or {}).keys()),
        },
    )

