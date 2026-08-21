# Agent Crawl Kit

Agent Crawl Kit is an installable capability pack that gives coding agents a practical way to search, read, crawl, and extract information from the internet.

It provides reusable commands and a skill description. Each team can decide its own workflows, prompts, and downstream business logic.

## What It Provides

- Web page reading with source URL and retrieval time.
- Search routing through available local tools.
- RSS and Atom reading for public feeds.
- GitHub repository inspection through the official GitHub CLI.
- Video transcript extraction through available local tooling.
- Article and table extraction from fetched content.
- JSON, JSONL, CSV, and Markdown-friendly output contracts.
- Environment diagnosis so an agent can explain which channels are available.

## Design

- Capability-first: commands expose reusable access and extraction functions.
- Workflow-neutral: teams decide when and how to combine commands.
- Agent-friendly: the included skill tells agents which commands exist.
- Structured: commands can return JSON, JSONL, CSV, or Markdown.

## Quick Start

One-line install with auto skill setup:

```bash
curl -fsSL https://raw.githubusercontent.com/hattie0923/agent-crawl-kit/main/scripts/install.sh | \
  bash -s -- --agent auto
```

Install to a known skill directory:

```bash
curl -fsSL https://raw.githubusercontent.com/hattie0923/agent-crawl-kit/main/scripts/install.sh | \
  bash -s -- --skill-dir "$HOME/.trae/skills"
```

Manual local install:

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

For teammate onboarding, see [docs/teammate-install.md](docs/teammate-install.md).
