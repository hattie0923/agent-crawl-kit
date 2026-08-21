from __future__ import annotations

import xml.etree.ElementTree as ET

from agent_crawl.channels.web import read_url
from agent_crawl.models import CrawlResult, error, ok


def read_feed(url: str, limit: int = 20) -> CrawlResult:
    fetched = read_url(url)
    if fetched.status != "ok":
        return fetched

    text = fetched.data.get("text") or ""
    # Fetch again to parse XML because read_url stores readable text, not raw XML.
    try:
        import urllib.request

        request = urllib.request.Request(url, headers={"User-Agent": "agent-crawl-kit/0.1"})
        with urllib.request.urlopen(request, timeout=20) as response:
            xml_body = response.read(2_000_000)
    except Exception as exc:  # noqa: BLE001 - CLI should return structured failures.
        return error(url, str(exc))

    try:
        root = ET.fromstring(xml_body)
    except ET.ParseError as exc:
        return error(url, f"invalid feed XML: {exc}; preview={text[:120]}")

    items = _rss_items(root) or _atom_items(root)
    return ok(url, {"items": items[:limit], "count": min(len(items), limit)})


def _rss_items(root: ET.Element) -> list[dict[str, str | None]]:
    rows: list[dict[str, str | None]] = []
    for item in root.findall(".//item"):
        rows.append(
            {
                "title": _child_text(item, "title"),
                "url": _child_text(item, "link"),
                "published_at": _child_text(item, "pubDate"),
                "summary": _child_text(item, "description"),
            },
        )
    return rows


def _atom_items(root: ET.Element) -> list[dict[str, str | None]]:
    rows: list[dict[str, str | None]] = []
    for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
        link = entry.find("{http://www.w3.org/2005/Atom}link")
        rows.append(
            {
                "title": _child_text(entry, "{http://www.w3.org/2005/Atom}title"),
                "url": link.attrib.get("href") if link is not None else None,
                "published_at": _child_text(entry, "{http://www.w3.org/2005/Atom}updated"),
                "summary": _child_text(entry, "{http://www.w3.org/2005/Atom}summary"),
            },
        )
    return rows


def _child_text(parent: ET.Element, name: str) -> str | None:
    child = parent.find(name)
    return child.text.strip() if child is not None and child.text else None

