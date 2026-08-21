# Platform Support

Agent Crawl Kit uses local tools and explicit user configuration. Availability depends on the target machine.

## Zero Or Low Configuration

| Channel | Purpose | Typical Backend |
|---|---|---|
| Web | Read public pages | Python HTTP, `curl`, readable text endpoints |
| RSS | Read public feeds | Python stdlib XML parsing |
| GitHub | Inspect repositories | `gh` CLI |
| Video | Extract metadata or subtitles | `yt-dlp` when available |
| Search | Search web or code | configured local search tools |

## Login Or Manual Configuration

Some platforms require a user-controlled browser session, cookies, or approved tools. The toolkit must not log in on behalf of the user.

## Status Values

- `ok`: the channel is available and the command completed.
- `partial`: the channel returned incomplete but usable data.
- `unavailable`: required local tooling or configuration is missing.
- `skipped`: the command intentionally did not run.
- `error`: the command failed after attempting the supported route.

## Agent Behavior

Agents should run `agent-crawl doctor` before complex collection tasks and explain unavailable channels before continuing.

