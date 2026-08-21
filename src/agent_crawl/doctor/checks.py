from __future__ import annotations

import shutil
import sys
from dataclasses import asdict, dataclass

from agent_crawl.config import has_secret


@dataclass
class ChannelCheck:
    channel: str
    status: str
    backend: str | None
    message: str
    install_hint: str | None = None

    def to_dict(self) -> dict[str, str | None]:
        return asdict(self)


def run_checks() -> list[ChannelCheck]:
    return [
        ChannelCheck("python", "ok", sys.executable, f"Python {sys.version.split()[0]}"),
        _tool("curl", "web", "optional HTTP fallback", "Install curl with your system package manager."),
        _tool("gh", "github", "GitHub repository access", "Install GitHub CLI: brew install gh, then run gh auth login if needed."),
        _tool("yt-dlp", "video", "video metadata and subtitle extraction", "Install yt-dlp: python -m pip install yt-dlp."),
        _tool("bili", "bilibili", "Bilibili search and video access", "Install the configured Bilibili CLI backend."),
        _tool("opencli", "browser-platforms", "browser-session platform backend", "Install the configured browser-session backend."),
        _tool("mcporter", "search", "optional semantic web search", "Install and configure the local search backend used by your agent environment."),
        _tool("twitter", "twitter", "Twitter/X CLI backend", "Install the configured Twitter/X CLI backend."),
        _tool("rdt", "reddit", "Reddit CLI backend", "Install the configured Reddit CLI backend."),
        _configured("cookie", "twitter", "Twitter/X cookie configuration"),
        _configured("cookie", "reddit", "Reddit cookie configuration"),
        _configured("cookie", "xiaohongshu", "Xiaohongshu cookie configuration"),
        _configured("cookie", "facebook", "Facebook cookie configuration"),
        _configured("cookie", "instagram", "Instagram cookie configuration"),
        _configured("token", "openrouter", "OpenRouter API key"),
    ]


def _tool(binary: str, channel: str, purpose: str, install_hint: str) -> ChannelCheck:
    path = shutil.which(binary)
    if path:
        return ChannelCheck(channel, "ok", binary, f"{purpose}; found at {path}")
    return ChannelCheck(channel, "unavailable", binary, f"{purpose}; `{binary}` is not installed", install_hint)


def _configured(kind: str, name: str, purpose: str) -> ChannelCheck:
    if has_secret(kind, name):
        return ChannelCheck(name, "ok", kind, f"{purpose}; configured locally")
    return ChannelCheck(
        name,
        "unavailable",
        kind,
        f"{purpose}; not configured",
        f"Configure with: agent-crawl configure {kind} {name} --from-stdin",
    )
