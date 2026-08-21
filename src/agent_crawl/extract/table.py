from __future__ import annotations

from html.parser import HTMLParser
from urllib.request import Request, urlopen

from agent_crawl.models import CrawlResult, error, ok


class _TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tables: list[list[list[str]]] = []
        self._table: list[list[str]] | None = None
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "table":
            self._table = []
        elif tag == "tr" and self._table is not None:
            self._row = []
        elif tag in {"td", "th"} and self._row is not None:
            self._cell = []

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self._cell is not None and self._row is not None:
            self._row.append(" ".join(self._cell).strip())
            self._cell = None
        elif tag == "tr" and self._row is not None and self._table is not None:
            if any(self._row):
                self._table.append(self._row)
            self._row = None
        elif tag == "table" and self._table is not None:
            if self._table:
                self.tables.append(self._table)
            self._table = None

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            text = data.strip()
            if text:
                self._cell.append(text)


def extract_tables(url: str) -> CrawlResult:
    try:
        request = Request(url, headers={"User-Agent": "agent-crawl-kit/0.1"})
        with urlopen(request, timeout=20) as response:
            html = response.read(2_000_000).decode("utf-8", errors="replace")
    except Exception as exc:  # noqa: BLE001 - CLI should return structured failures.
        return error(url, str(exc))

    parser = _TableParser()
    parser.feed(html)
    return ok(
        url,
        {
            "record_type": "tables",
            "count": len(parser.tables),
            "tables": parser.tables,
            "items": _tables_as_items(parser.tables),
        },
    )


def _tables_as_items(tables: list[list[list[str]]]) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for table_index, table in enumerate(tables):
        if not table:
            continue
        headers = table[0]
        for row in table[1:]:
            items.append(
                {
                    "table": str(table_index),
                    **{headers[index] if index < len(headers) else f"column_{index}": value for index, value in enumerate(row)},
                },
            )
    return items

