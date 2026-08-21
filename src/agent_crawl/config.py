from __future__ import annotations

import json
import os
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


CONFIG_HOME = Path(os.environ.get("AGENT_CRAWL_HOME", "~/.agent-crawl")).expanduser()
CONFIG_DIR = CONFIG_HOME / "config"


@dataclass
class ConfigEntry:
    kind: str
    name: str
    path: str
    configured: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "name": self.name,
            "path": self.path,
            "configured": self.configured,
        }


def config_path(kind: str, name: str) -> Path:
    safe_name = name.lower().replace("/", "_").replace(" ", "_")
    return CONFIG_DIR / kind / f"{safe_name}.json"


def write_secret(kind: str, name: str, value: str, metadata: dict[str, Any] | None = None) -> ConfigEntry:
    path = config_path(kind, name)
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "kind": kind,
        "name": name,
        "value": value,
        "metadata": metadata or {},
    }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    return ConfigEntry(kind=kind, name=name, path=str(path), configured=True)


def read_secret(kind: str, name: str) -> str | None:
    path = config_path(kind, name)
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    value = payload.get("value")
    return value if isinstance(value, str) and value else None


def has_secret(kind: str, name: str) -> bool:
    return read_secret(kind, name) is not None


def list_entries() -> list[ConfigEntry]:
    entries: list[ConfigEntry] = []
    if not CONFIG_DIR.exists():
        return entries
    for path in sorted(CONFIG_DIR.glob("*/*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        kind = str(payload.get("kind") or path.parent.name)
        name = str(payload.get("name") or path.stem)
        entries.append(ConfigEntry(kind=kind, name=name, path=str(path), configured=bool(payload.get("value"))))
    return entries


def read_stdin_secret() -> str:
    value = sys.stdin.read().strip()
    if not value:
        raise ValueError("empty secret from stdin")
    return value


def read_file_secret(path: str) -> str:
    value = Path(path).expanduser().read_text(encoding="utf-8").strip()
    if not value:
        raise ValueError(f"empty secret file: {path}")
    return value


def read_env_secret(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"environment variable is empty or missing: {name}")
    return value

