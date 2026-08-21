# Login State And Tokens

Some platform backends need login state or service tokens. Agent Crawl Kit provides local configuration commands for those values.

## Cookie Editor

Cookie Editor can be used to manually export cookies from a browser session that is already logged in.

Typical flow:

1. Open the target website in the browser.
2. Confirm the site is already logged in.
3. Use Cookie Editor to export cookies for that site.
4. Save the exported value to a local file.
5. Store it with `agent-crawl configure cookie`.

Example:

```bash
agent-crawl configure cookie xiaohongshu --from-file ~/Downloads/xiaohongshu-cookie.txt
agent-crawl configure cookie twitter --from-stdin
agent-crawl configure list --format markdown
agent-crawl doctor --format markdown
```

Supported cookie names:

- `twitter`
- `reddit`
- `xiaohongshu`
- `facebook`
- `instagram`

## Tokens

Service tokens can be stored from environment variables:

```bash
export OPENROUTER_API_KEY="..."
agent-crawl configure openrouter --from-env OPENROUTER_API_KEY
agent-crawl openrouter models --limit 5 --format json
```

Generic tokens can also be stored:

```bash
agent-crawl configure token service-name --from-stdin
agent-crawl configure token service-name --from-file ~/Downloads/token.txt
agent-crawl configure token service-name --from-env SERVICE_TOKEN
```

## Storage

Configuration is stored under:

```text
~/.agent-crawl/config
```

Secret files are written with user-only permissions. Listing commands report only names and paths, not secret values.

