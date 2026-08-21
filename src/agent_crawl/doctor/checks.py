from __future__ import annotations

import shutil
import sys
from dataclasses import asdict, dataclass


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
        _tool("mcporter", "search", "optional semantic web search", "Install and configure the local search backend used by your agent environment."),
    ]


def _tool(binary: str, channel: str, purpose: str, install_hint: str) -> ChannelCheck:
    path = shutil.which(binary)
    if path:
        return ChannelCheck(channel, "ok", binary, f"{purpose}; found at {path}")
    return ChannelCheck(channel, "unavailable", binary, f"{purpose}; `{binary}` is not installed", install_hint)
