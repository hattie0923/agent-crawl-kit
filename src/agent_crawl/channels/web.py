from __future__ import annotations

import re
from html import unescape
from html.parser import HTMLParser
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from agent_crawl.models import Evidence, CrawlResult, error, ok


class _TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title: str | None = None
        self.links: list[str] = []
        self._in_title = False
        self._skip_depth = 0
        self._chunks: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip_depth += 1
        if tag == "title":
            self._in_title = True
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self._skip_depth:
            self._skip_depth -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if not text:
            return
        if self._in_title:
            self.title = text
        if self._skip_depth == 0:
            self._chunks.append(text)

    @property
    def text(self) -> str:
        return re.sub(r"\s+", " ", unescape(" ".join(self._chunks))).strip()


def read_url(url: str, timeout: int = 20) -> CrawlResult:
    request = Request(url, headers={"User-Agent": "agent-crawl-kit/0.1"})
    try:
        with urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get("content-type", "")
            raw = response.read(2_000_000)
            body = raw.decode(_encoding_from_content_type(content_type), errors="replace")
    except (HTTPError, URLError, TimeoutError) as exc:
        return error(url, str(exc))

    parser = _TextExtractor()
    parser.feed(body)
    text = parser.text
    result = ok(
        url,
        {
            "title": parser.title,
            "text": text,
            "links": parser.links[:200],
            "content_type": content_type,
            "bytes_read": len(raw),
        },
    )
    if parser.title:
        result.evidence.append(
            Evidence(
                field="title",
                source_url=url,
                excerpt=parser.title,
                retrieved_at=result.retrieved_at,
                selector="title",
                confidence=0.9,
            ),
        )
    if text:
        result.evidence.append(
            Evidence(
                field="text",
                source_url=url,
                excerpt=text[:500],
                retrieved_at=result.retrieved_at,
                confidence=0.6,
            ),
        )
    return result


def _encoding_from_content_type(content_type: str) -> str:
    match = re.search(r"charset=([^;\s]+)", content_type, re.I)
    return match.group(1) if match else "utf-8"

