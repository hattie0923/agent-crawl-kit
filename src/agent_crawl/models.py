from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


@dataclass
class Evidence:
    field: str
    source_url: str
    excerpt: str
    retrieved_at: str
    selector: str | None = None
    confidence: float | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class CrawlResult:
    status: str
    source_url: str | None
    retrieved_at: str
    data: dict[str, Any] = field(default_factory=dict)
    evidence: list[Evidence] = field(default_factory=list)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["evidence"] = [item.to_dict() for item in self.evidence]
        return payload


def ok(source_url: str | None, data: dict[str, Any], evidence: list[Evidence] | None = None) -> CrawlResult:
    return CrawlResult(
        status="ok",
        source_url=source_url,
        retrieved_at=utc_now(),
        data=data,
        evidence=evidence or [],
    )


def unavailable(source_url: str | None, message: str) -> CrawlResult:
    return CrawlResult(
        status="unavailable",
        source_url=source_url,
        retrieved_at=utc_now(),
        error=message,
    )


def error(source_url: str | None, message: str) -> CrawlResult:
    return CrawlResult(
        status="error",
        source_url=source_url,
        retrieved_at=utc_now(),
        error=message,
    )

