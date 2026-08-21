from __future__ import annotations

from agent_crawl.channels.web import read_url
from agent_crawl.models import Evidence, CrawlResult


def extract_article(url: str) -> CrawlResult:
    result = read_url(url)
    if result.status != "ok":
        return result

    text = str(result.data.get("text") or "")
    title = result.data.get("title")
    summary = text[:800]
    result.data = {
        "record_type": "article",
        "title": title,
        "body": text,
        "summary": summary,
        "word_count": len(text.split()),
        "links": result.data.get("links", []),
    }
    result.evidence = []
    if title:
        result.evidence.append(
            Evidence(
                field="title",
                source_url=url,
                excerpt=str(title),
                retrieved_at=result.retrieved_at,
                selector="title",
                confidence=0.9,
            ),
        )
    if summary:
        result.evidence.append(
            Evidence(
                field="body",
                source_url=url,
                excerpt=summary,
                retrieved_at=result.retrieved_at,
                confidence=0.6,
            ),
        )
    return result

