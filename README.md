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
- Local cookie and token configuration for login-required backends.
- OpenRouter key configuration and model listing.
- Platform search through configured local backends.
- JSON, JSONL, CSV, and Markdown-friendly output contracts.
- Environment diagnosis so an agent can explain which channels are available.

## Capability Levels

### Built In

- `doctor`: inspect available channels and local configuration.
- `read-url`: read a URL and return title, text, links, and metadata.
- `rss`: parse RSS or Atom feeds.
- `extract article`: extract article-like fields from a page.
- `extract table`: extract HTML tables from a page.
- `configure`: store local cookies and tokens without printing secret values.
- `platform search`: use configured local platform backends.

### Requires Local Tools

- `github`: requires `gh`.
- `video`: requires `yt-dlp`.
- `search`: requires a configured local search backend such as `mcporter`.
- `bilibili`: requires a configured Bilibili CLI backend.
- Browser-session platforms: require a configured browser automation backend such as `opencli`.
- Twitter/X and Reddit CLI paths: require their configured local CLI backends.

### Requires Login State Or Tokens

- Private GitHub access uses `gh auth login`.
- Twitter/X, Reddit, Xiaohongshu, Facebook, and Instagram can use locally stored cookies or browser-session backends.
- Cookie values can be exported manually with Cookie Editor and stored locally with `agent-crawl configure cookie`.
- OpenRouter uses `agent-crawl configure openrouter` or the `OPENROUTER_API_KEY` environment variable.

Secrets are stored under `~/.agent-crawl/config` with user-only file permissions. Commands do not print stored secret values.

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

Install a released version:

```bash
curl -fsSL https://raw.githubusercontent.com/hattie0923/agent-crawl-kit/main/scripts/install.sh | \
  bash -s -- --agent auto --ref v0.2.0
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

Configure a cookie exported with Cookie Editor:

```bash
agent-crawl configure cookie xiaohongshu --from-file ~/Downloads/xiaohongshu-cookie.txt
```

Configure OpenRouter:

```bash
export OPENROUTER_API_KEY="..."
agent-crawl configure openrouter --from-env OPENROUTER_API_KEY
agent-crawl openrouter models --limit 5 --format json
```

Search a configured platform backend:

```bash
agent-crawl platform search bilibili "AI tutorial" --limit 5 --format json
agent-crawl platform search xiaohongshu "AI camera" --limit 5 --format json
agent-crawl platform search twitter "new model release" --limit 5 --format json
```

## Flexible Structured Output

Commands use a small response envelope so agents can read status and provenance consistently. The `data` object is intentionally flexible and should match the user's request.

```json
{
  "status": "ok",
  "retrieved_at": "2026-08-20T10:00:00Z",
  "source_url": "https://example.com",
  "data": {
    "any_requested_fields": "..."
  },
  "evidence": []
}
```

For example, `data` can contain article text, table rows, RSS items, repository metadata, transcript metadata, extracted links, or any future extractor output.

## Skill

The agent-facing skill lives at:

```text
skills/agent-crawl/SKILL.md
```

Install that skill into the target agent environment so the agent knows when to call this toolkit and how to report crawl results.

For teammate onboarding, see [docs/teammate-install.md](docs/teammate-install.md).

For login-state and token setup, see [docs/login-state.md](docs/login-state.md).
