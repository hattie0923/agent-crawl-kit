# Platform Support

Agent Crawl Kit uses local tools and explicit user configuration. Availability depends on the target machine.

## Zero Or Low Configuration

| Channel | Purpose | Typical Backend |
|---|---|---|
| Web | Read pages | Python HTTP, `curl`, readable text endpoints |
| RSS | Read feeds | Python stdlib XML parsing |
| GitHub | Inspect repositories | `gh` CLI |
| Video | Extract metadata or subtitles | `yt-dlp` when available |
| Search | Search web or code | configured local search tools |

## Manual Configuration

Some channels can be connected to local sessions, tokens, cookies, or additional command-line tools depending on the agent environment.

## Status Values

- `ok`: the channel is available and the command completed.
- `partial`: the channel returned incomplete but usable data.
- `unavailable`: required local tooling or configuration is missing.
- `skipped`: the command intentionally did not run.
- `error`: the command failed after attempting the supported route.

Use `agent-crawl doctor` to inspect the current machine.
