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
  bash -s -- --agent auto --ref v0.1.0
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

## Install The Skill Only

If the CLI is already installed but the skill is missing:

```bash
cp ~/.agent-crawl-kit/skills/agent-crawl/SKILL.md ~/.agents/skills/agent-crawl/SKILL.md
```

Replace `~/.agents/skills` with the target agent's skill directory when needed.
