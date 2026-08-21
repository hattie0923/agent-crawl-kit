# Platform Support

Agent Crawl Kit uses local tools and explicit user configuration. Availability depends on the target machine.

## Built In Or Low Configuration

| Channel | Purpose | Typical Backend |
|---|---|---|
| Web | Read pages | Python HTTP, `curl`, readable text endpoints |
| RSS | Read feeds | Python stdlib XML parsing |
| Article extraction | Extract title/body/links | built-in HTML parser |
| Table extraction | Extract HTML tables | built-in HTML parser |

## Local Tool Backends

| Channel | Purpose | Typical Backend | Check |
|---|---|---|---|
| Search | Search web or code | `mcporter` or another configured search backend | `agent-crawl doctor` |
| GitHub | Inspect repositories | `gh` CLI | `gh auth status` |
| Video | Extract metadata or subtitles | `yt-dlp` | `yt-dlp --version` |
| Bilibili | Search or read Bilibili content | `bili` CLI or browser backend | `agent-crawl doctor` |
| Browser platforms | Read session-backed sites | `opencli` or another browser-session backend | `agent-crawl doctor` |
| Twitter/X | Search or read content | local CLI, cookie-backed CLI, or browser backend | `agent-crawl doctor` |
| Reddit | Search or read posts | local CLI, cookie-backed CLI, or browser backend | `agent-crawl doctor` |

Generic platform search command:

```bash
agent-crawl platform search bilibili "AI tutorial" --limit 5 --format json
agent-crawl platform search twitter "new model release" --limit 5 --format json
agent-crawl platform search xiaohongshu "AI camera" --limit 5 --format json
agent-crawl platform search reddit "agent crawling" --limit 5 --format json
```

## Login State And Cookies

Some platforms need login state. The toolkit stores user-provided cookies locally, then `doctor` reports whether the configuration exists.

Supported cookie names:

- `twitter`
- `reddit`
- `xiaohongshu`
- `facebook`
- `instagram`

Examples:

```bash
agent-crawl configure cookie twitter --from-stdin
agent-crawl configure cookie xiaohongshu --from-file ~/Downloads/xiaohongshu-cookie.txt
agent-crawl configure list --format markdown
agent-crawl doctor --format markdown
```

Cookie Editor can be used to manually export cookies from a logged-in browser session. Store exported cookies locally with `agent-crawl configure cookie ...`; secret values are not printed by `configure list` or `doctor`.

## OpenRouter

OpenRouter is an optional LLM backend for future extraction and transformation features. The current toolkit can store the key and list models.

```bash
export OPENROUTER_API_KEY="..."
agent-crawl configure openrouter --from-env OPENROUTER_API_KEY
agent-crawl openrouter models --limit 5 --format json
```

## Status Values

- `ok`: the channel is available and the command completed.
- `partial`: the channel returned incomplete but usable data.
- `unavailable`: required local tooling or configuration is missing.
- `skipped`: the command intentionally did not run.
- `error`: the command failed after attempting the supported route.

Use `agent-crawl doctor` to inspect the current machine.
