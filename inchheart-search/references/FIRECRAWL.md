# Firecrawl

## What It Is

Firecrawl is the default cloud-backed web research layer for public web search, scraping, mapping, crawling, and live-page interaction.

## When to Use

- No exact URL yet: use `search`
- Exact URL: use `scrape`
- Need URLs inside a site: use `map`
- Need bulk extraction: use `crawl`
- Need structured extraction or browser-style actions: use `agent` / `interact`
- Need setup, auth, or integrations: use `config`, `login`, `setup`, or `env`

## CLI Surface

- `firecrawl search` for search-first research
- `firecrawl scrape` for page extraction
- `firecrawl map` for site URL discovery
- `firecrawl crawl` for multi-page extraction
- `firecrawl agent` for structured extraction
- `firecrawl interact` for live browser actions after a scrape
- `firecrawl init` / `firecrawl setup` for installation and integrations
- `firecrawl config` / `firecrawl view-config` / `firecrawl login` for auth
- `firecrawl --status` for health, credits, and concurrency

## Local Reality on This Machine

- Firecrawl is used through the `firecrawl` CLI.
- It authenticates with stored credentials / API key state.
- It is cloud-backed, not a local daemon.
- It is the default broad public-web tool for `inchheart-search`.

## Rules

- Prefer `search` when you don't know the URL.
- Prefer `scrape` when you already know the URL.
- Do not re-scrape URLs already returned by `search --scrape`.
- Keep `.firecrawl/` ignored when saving outputs.
- Do not print API keys.
