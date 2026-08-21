# Teammate Install Guide

Give this page to teammates when they want their agent to gain information crawling and extraction capability.

## Copy This To Your Agent

```text
Please install the company information crawling capability pack from:
https://github.com/hattie0923/agent-crawl-kit

Follow docs/install.md. After installation, run agent-crawl doctor --format markdown and tell me which channels are available.
```

## Recommended One-Line Install

For macOS or Linux, install the toolkit and auto-detect the local agent skill directory:

```bash
curl -fsSL https://raw.githubusercontent.com/hattie0923/agent-crawl-kit/main/scripts/install.sh | \
  bash -s -- --agent auto
```

For a released version:

```bash
curl -fsSL https://raw.githubusercontent.com/hattie0923/agent-crawl-kit/main/scripts/install.sh | \
  bash -s -- --agent auto --ref v0.2.0
```

Default install location:

```text
~/.agent-crawl-kit
```

## Agent Targets

Use an explicit target when auto-detection is not desired:

```bash
curl -fsSL https://raw.githubusercontent.com/hattie0923/agent-crawl-kit/main/scripts/install.sh | \
  bash -s -- --agent trae
```

Supported targets:

- `auto`: detect an existing skill directory, then fall back to `~/.agents/skills`.
- `trae`: install to `~/.trae/skills`.
- `claude`: install to `~/.claude/skills`.
- `cursor`: install to `~/.cursor/skills`.
- `generic`: install to `~/.agents/skills`.
- `none`: install CLI only.

## Manual Skill Directory

If the agent has a known local skill directory, pass it explicitly:

```bash
curl -fsSL https://raw.githubusercontent.com/hattie0923/agent-crawl-kit/main/scripts/install.sh | \
  bash -s -- --skill-dir "$HOME/.trae/skills"
```

The installer copies:

```text
skills/agent-crawl/SKILL.md
```

to:

```text
<skill-dir>/agent-crawl/SKILL.md
```

## Manual Install

```bash
git clone https://github.com/hattie0923/agent-crawl-kit.git ~/.agent-crawl-kit
cd ~/.agent-crawl-kit
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
agent-crawl doctor --format markdown
```

## Command Reference

```bash
source ~/.agent-crawl-kit/.venv/bin/activate
agent-crawl doctor --format markdown
agent-crawl read-url https://example.com --format json
agent-crawl extract article https://example.com --format json
agent-crawl extract table https://example.com/pricing --format csv
agent-crawl rss https://example.com/feed.xml --limit 10 --format jsonl
agent-crawl github owner/repo --format json
agent-crawl video https://example.com/video --format json
agent-crawl search "your query" --limit 5 --format json
agent-crawl platform search bilibili "AI tutorial" --limit 5 --format json
agent-crawl platform search xiaohongshu "AI camera" --limit 5 --format json
agent-crawl openrouter models --limit 5 --format json
```

## Built-In And Optional Capabilities

Built in:

- `doctor`
- `read-url`
- `rss`
- `extract article`
- `extract table`
- `configure`
- `platform search`

Requires local tools:

- `github`: requires `gh`.
- `video`: requires `yt-dlp`.
- `search`: requires a configured search backend such as `mcporter`.
- `bilibili`: requires a configured Bilibili backend.
- Browser-session platforms: require a configured browser backend such as `opencli`.

Login state and tokens:

- GitHub private access uses `gh auth login`.
- Twitter/X, Reddit, Xiaohongshu, Facebook, and Instagram can use locally stored cookies or browser-session backends.
- Cookie Editor can be used to manually export cookies from an existing browser session.
- OpenRouter can be configured as a token-backed LLM backend.

## Cookie And Token Configuration

```bash
agent-crawl configure cookie twitter --from-stdin
agent-crawl configure cookie xiaohongshu --from-file ~/Downloads/xiaohongshu-cookie.txt
agent-crawl configure openrouter --from-env OPENROUTER_API_KEY
agent-crawl configure list --format markdown
agent-crawl doctor --format markdown
```

## Flexible Structured Output

Structured formats use a small response envelope:

- `status`
- `source_url`
- `retrieved_at`
- `data`: flexible content requested by the user, such as article text, table rows, feed items, repository metadata, or video metadata.
- `evidence`: optional source snippets or anchors.

Commands may also return `error` when a channel is unavailable or a request fails.

## Update

```bash
curl -fsSL https://raw.githubusercontent.com/hattie0923/agent-crawl-kit/main/scripts/install.sh | \
  bash -s -- --agent auto
```

Or manually:

```bash
cd ~/.agent-crawl-kit
git pull --ff-only
source .venv/bin/activate
pip install -e .
agent-crawl doctor --format markdown
```
