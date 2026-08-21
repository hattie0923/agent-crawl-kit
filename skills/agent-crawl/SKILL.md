---
name: "agent-crawl"
description: "Collects and extracts web information. Invoke when users ask agents to search, crawl, read URLs, parse RSS, inspect GitHub, or extract tables/articles."
---

# Agent Crawl

Use this skill when the user needs internet information access, crawling, or structured extraction.

## Capabilities

- Check available local crawl channels.
- Search the web through configured local search tooling.
- Read a URL and extract title, text, links, and metadata.
- Parse RSS or Atom feeds.
- Inspect GitHub repositories through local tooling.
- Extract video metadata or transcripts when local tooling supports it.
- Extract article fields, tables, lists, links, dates, prices, or contacts from fetched content.
- Convert crawl results to JSON, JSONL, CSV, or Markdown.

## Commands

```bash
agent-crawl doctor --format markdown
agent-crawl read-url https://example.com --format json
agent-crawl extract article https://example.com/article --format json
agent-crawl extract table https://example.com/pricing --format csv
agent-crawl rss https://example.com/feed.xml --limit 10 --format jsonl
agent-crawl github owner/repo --format json
agent-crawl video https://www.youtube.com/watch?v=example --format json
```

## Flexible Structured Output

Commands can return a small response envelope when a structured format is requested. The envelope is stable, while the `data` object stays flexible for the user's requested content.

```json
{
  "status": "ok",
  "source_url": "https://example.com",
  "retrieved_at": "2026-08-20T10:00:00Z",
  "data": {
    "any_requested_fields": "..."
  },
  "evidence": []
}
```

Status values include `ok`, `partial`, `unavailable`, `skipped`, and `error`. The `data` object can contain article fields, table rows, feed items, repository metadata, video metadata, links, or future extractor-specific fields.
