# Privacy And Safety

Agent Crawl Kit is designed for public information collection and evidence-preserving extraction.

## Rules

- Do not bypass authentication or paywalls.
- Do not automate login without explicit user approval.
- Do not collect private, sensitive, or unnecessary personal data.
- Do not upload cookies, tokens, or browser sessions to external services.
- Do not fabricate missing fields.
- Respect platform terms, rate limits, and robots guidance where applicable.

## Credentials

Credentials must stay on the user's machine. Commands should read credentials from the local environment or official local tooling only.

## Output

Every output should include:

- `source_url`
- `retrieved_at`
- extraction status
- evidence excerpts when fields are extracted

When extraction fails, return a clear error or partial result instead of guessing.

