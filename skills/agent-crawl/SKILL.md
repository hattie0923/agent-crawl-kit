---
name: "agent-crawl"
description: "Collects and extracts public web information with evidence. Invoke when users ask agents to search, crawl, read URLs, parse RSS, inspect GitHub, or extract tables/articles."
---

# Agent Crawl

Use this skill when the user needs public information collection, web reading, crawling, or structured extraction.

## Use Cases

- Search the web or code hosting sites for public information.
- Read a URL and extract title, text, links, and metadata.
- Parse RSS or Atom feeds.
- Inspect public GitHub repositories through local official tooling.
- Extract public video metadata or transcripts when local tooling supports it.
- Extract article fields, tables, lists, links, dates, prices, or contacts from fetched content.
- Convert crawl results to JSON, JSONL, CSV, or Markdown.

## Boundaries

- Do not make business judgments.
- Do not score leads or classify competitors.
- Do not bypass authentication, paywalls, or platform controls.
- Do not collect private or sensitive data unless the user explicitly owns and authorizes access.
- Do not fabricate missing data.

## Standard Workflow

1. Run `agent-crawl doctor` before broad or multi-platform collection tasks.
2. Choose the available channel for the requested source.
3. Fetch or search the source.
4. Extract structured fields only when evidence is available.
5. Return `source_url`, `retrieved_at`, status, data, and evidence.
6. Explain unavailable channels and suggest configuration steps.

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

## Output Rules

Always prefer structured output with provenance:

```json
{
  "status": "ok",
  "source_url": "https://example.com",
  "retrieved_at": "2026-08-20T10:00:00Z",
  "data": {},
  "evidence": []
}
```

If the result is incomplete, mark it as `partial`. If a channel is missing, mark it as `unavailable`.

