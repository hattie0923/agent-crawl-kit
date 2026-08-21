# Install

This guide is written for agents. Follow it when a user asks to install the information crawling capability pack.

## Safe Install

```bash
git clone <repo-url> agent-crawl-kit
cd agent-crawl-kit
python -m venv .venv
source .venv/bin/activate
pip install -e .
agent-crawl doctor
```

## Optional Tools

Install optional tools only when the user approves them:

- `gh` for GitHub repository and code access.
- `yt-dlp` for public video metadata and subtitles.
- `curl` for HTTP fallback.
- Browser automation tools when JavaScript-rendered pages must be read.

## Skill Install

Copy `skills/agent-crawl/SKILL.md` into the target agent's skill directory.

After installation, run:

```bash
agent-crawl doctor --format markdown
```

Report which channels are available and which need manual configuration.

