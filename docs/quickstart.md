# Quickstart

This page helps a teammate verify that the information crawling capability pack is installed and available to their agent.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/hattie0923/agent-crawl-kit/main/scripts/install.sh | \
  bash -s -- --agent auto
```

For a released version:

```bash
curl -fsSL https://raw.githubusercontent.com/hattie0923/agent-crawl-kit/main/scripts/install.sh | \
  bash -s -- --agent auto --ref v0.2.0
```

## Verify

```bash
source ~/.agent-crawl-kit/.venv/bin/activate
agent-crawl doctor --format markdown
```

The command prints available channels and install hints for missing optional tools.

## Try A URL

```bash
agent-crawl read-url https://example.com --format json
```

## Try An Extractor

```bash
agent-crawl extract article https://example.com --format json
```

## Try GitHub

```bash
agent-crawl github owner/repo --format json
```

If `github` is unavailable, install `gh` and run the doctor command again.

## Try Video

```bash
agent-crawl video https://example.com/video --format json
```

If `video` is unavailable, install `yt-dlp` and run the doctor command again.

## Configure Login-State Channels

For platforms that need cookies, export cookies manually with Cookie Editor and store them locally:

```bash
agent-crawl configure cookie twitter --from-stdin
agent-crawl configure cookie xiaohongshu --from-file ~/Downloads/xiaohongshu-cookie.txt
agent-crawl configure list --format markdown
agent-crawl doctor --format markdown
```

## Configure OpenRouter

```bash
export OPENROUTER_API_KEY="..."
agent-crawl configure openrouter --from-env OPENROUTER_API_KEY
agent-crawl openrouter models --limit 5 --format json
```

## Try A Platform Backend

```bash
agent-crawl platform search bilibili "AI tutorial" --limit 5 --format json
agent-crawl platform search xiaohongshu "AI camera" --limit 5 --format json
```

## Install The Skill Only

If the CLI is already installed but the skill is missing:

```bash
cp ~/.agent-crawl-kit/skills/agent-crawl/SKILL.md ~/.agents/skills/agent-crawl/SKILL.md
```

Replace `~/.agents/skills` with the target agent's skill directory when needed.
