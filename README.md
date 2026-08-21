# Agent Crawl Kit

Agent Crawl Kit is an installable capability pack that gives coding agents a practical way to search, read, crawl, and extract public information from the internet.

It focuses on information access and data extraction only. It does not make business judgments, score leads, classify competitors, or generate strategy.

## What It Provides

- Web page reading with source URL and retrieval time.
- Search routing through available local tools.
- RSS and Atom reading for public feeds.
- GitHub repository inspection through the official GitHub CLI.
- Video transcript extraction through available local tooling.
- Article and table extraction from fetched content.
- JSON, JSONL, CSV, and Markdown-friendly output contracts.
- Environment diagnosis so an agent can explain which channels are available.

## Intended Users

This project is built for agents used by teammates. After installation, users can ask their agent to:

- Search the web and read the most relevant sources.
- Read a URL and extract the title, text, links, and metadata.
- Parse a pricing page into structured rows.
- Read RSS updates from a source.
- Inspect a GitHub repository, releases, issues, or README.
- Extract video transcripts when local tooling supports it.
- Return structured data with source evidence instead of untraceable summaries.

## Non-Goals

- No business-specific scoring or classification.
- No private-data scraping.
- No credential bypassing or automated login.
- No platform terms circumvention.
- No hidden fallback to fabricated data.

## Quick Start

```bash
cd agent-crawl-kit
python -m venv .venv
source .venv/bin/activate
pip install -e .
agent-crawl doctor
```

Read a page:

```bash
agent-crawl read-url https://example.com --format json
```

Extract an article:

```bash
agent-crawl extract article https://example.com/article --format json
```

Read RSS:

```bash
agent-crawl rss https://example.com/feed.xml --limit 10 --format jsonl
```

## Output Contract

Every command should preserve provenance:

```json
{
  "status": "ok",
  "retrieved_at": "2026-08-20T10:00:00Z",
  "source_url": "https://example.com",
  "data": {},
  "evidence": []
}
```

When a channel is unavailable, commands return explicit unavailable or error states instead of inventing results.

## Skill

The agent-facing skill lives at:

```text
skills/agent-crawl/SKILL.md
```

Install that skill into the target agent environment so the agent knows when to call this toolkit and how to report crawl results.

