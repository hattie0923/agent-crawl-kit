# Teammate Install Guide

Give this page to teammates when they want their agent to gain public information crawling and extraction capability.

## Copy This To Your Agent

```text
Please install the company information crawling capability pack from:
https://github.com/hattie0923/agent-crawl-kit

Follow docs/install.md. After installation, run agent-crawl doctor --format markdown and tell me which channels are available.
Do not bypass login, paywalls, or platform restrictions. Only collect public or explicitly authorized information.
```

## One-Line Install

For macOS or Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/hattie0923/agent-crawl-kit/main/scripts/install.sh | bash
```

Default install location:

```text
~/.agent-crawl-kit
```

## Install With Skill Copy

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

## Daily Usage

```bash
source ~/.agent-crawl-kit/.venv/bin/activate
agent-crawl doctor --format markdown
agent-crawl read-url https://example.com --format json
agent-crawl extract article https://example.com --format json
agent-crawl extract table https://example.com/pricing --format csv
agent-crawl rss https://example.com/feed.xml --limit 10 --format jsonl
agent-crawl github owner/repo --format json
```

## What To Expect

The toolkit returns structured data with provenance:

- `status`
- `source_url`
- `retrieved_at`
- `data`
- `evidence`

Unavailable channels are reported explicitly. The agent should explain what is missing instead of guessing.

## Update

```bash
curl -fsSL https://raw.githubusercontent.com/hattie0923/agent-crawl-kit/main/scripts/install.sh | bash
```

Or manually:

```bash
cd ~/.agent-crawl-kit
git pull --ff-only
source .venv/bin/activate
pip install -e .
agent-crawl doctor --format markdown
```

