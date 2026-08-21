from __future__ import annotations

import json
import shutil
import subprocess

from agent_crawl.models import CrawlResult, error, ok, unavailable


def inspect_repo(repo: str) -> CrawlResult:
    if not shutil.which("gh"):
        return unavailable(f"https://github.com/{repo}", "GitHub CLI `gh` is not installed")
    command = [
        "gh",
        "repo",
        "view",
        repo,
        "--json",
        "nameWithOwner,description,url,stargazerCount,forkCount,licenseInfo,latestRelease,updatedAt",
    ]
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True, timeout=30)
    except Exception as exc:  # noqa: BLE001 - CLI should return structured failures.
        return error(f"https://github.com/{repo}", str(exc))
    if completed.returncode != 0:
        return error(f"https://github.com/{repo}", completed.stderr.strip() or completed.stdout.strip())
    return ok(f"https://github.com/{repo}", json.loads(completed.stdout))

