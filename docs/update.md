# Update

Use this guide when a user asks to update the information crawling capability pack.

```bash
cd agent-crawl-kit
git pull --ff-only
source .venv/bin/activate
pip install -e .
agent-crawl doctor
```

If the update changes skill instructions, reinstall:

```bash
cp skills/agent-crawl/SKILL.md <target-agent-skill-dir>/agent-crawl/SKILL.md
```

Always run `agent-crawl doctor` after updating and tell the user which channels changed.

