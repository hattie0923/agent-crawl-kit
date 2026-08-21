# Recipes

Recipes are agent-facing patterns for common information collection tasks.

## Web Research

1. Run `agent-crawl doctor`.
2. Run `agent-crawl search "<query>" --limit 10 --format json`.
3. Read the most relevant URLs with `agent-crawl read-url`.
4. Extract article fields with `agent-crawl extract article`.
5. Return a table with source URL, title, retrieved time, and key excerpts.

## URL Read

```bash
agent-crawl read-url https://example.com --format json
```

Use this when the user provides a URL and asks what it says.

## Pricing Page

```bash
agent-crawl extract table https://example.com/pricing --format csv
```

Use this when the user asks for plans, prices, quotas, or comparison tables.

## RSS Monitor

```bash
agent-crawl rss https://example.com/feed.xml --limit 20 --format jsonl
```

Use this when the user asks for latest updates from a site or publisher.

## GitHub Repo

```bash
agent-crawl github owner/repo --format json
```

Use this when the user asks what a public repository is, when it was updated, or what license/release it has.

## Video Metadata

```bash
agent-crawl video https://www.youtube.com/watch?v=example --format json
```

Use this when the user asks for public video metadata or available subtitles.

