---
name: inchheart-search
description: Combined InchHeart web search & research skill — SearXNG search tool, server configuration reference, and web scraping workflow. Run `scripts/inchheart-search "query"` to search, read CONFIGURATION.md for SearXNG YAML/fault-finding, read WORKFLOW.md for search-to-scrape pipelines.
---

# inchheart-search

InchHeart's integrated web research hub. Three parts:

| File | What | When to read |
|------|------|-------------|
| `scripts/inchheart-search` | CLI search tool (Bash + Python) | User asks to search the web through local SearXNG |
| `CONFIGURATION.md` | SearXNG setup, YAML traps, engine mgmt, health check | User asks about SearXNG config, engines, YAML pitfalls, or troubleshooting |
| `WORKFLOW.md` | Search → Obscura/Camoufox scraping pipeline | User wants full search-then-scrape workflow, batch fetch, or page monitoring |

## Quick Start — Search

```bash
scripts/inchheart-search "query"
scripts/inchheart-search "query" --category it --limit 5
scripts/inchheart-search "!github opencode"
scripts/inchheart-search "site:docs.rs tokio" --engines brave,bing
scripts/inchheart-search "query" --json
```

The script auto-starts SearXNG via launchctl if it is not running.

## When To Use

- User asks for web search, private search, 本机搜索, mentions SearXNG
- User asks for SearXNG configuration or engine tuning → read CONFIGURATION.md
- User wants to scrape pages after searching → read WORKFLOW.md
- User asks about search formats, JSON API, or category-based search
- User asks about YAML pitfalls, engine failures, or SearXNG fault-finding

Do NOT use for:
- High-stakes facts requiring cited sources (use built-in web search)
- Pages needing login, click, form fill (needs Camoufox, see `inchheart-browser` → `CAMOUFOX.md`)
- Searching private notes or secrets

## Service

```text
http://127.0.0.1:8888
/Users/mac/Repository/Services/Local/Tools/SearXNG
```

Manual: `cd /Users/mac/Repository/Services/Local/Tools/SearXNG && ./start-searxng.sh`

## Notes

SearXNG is a metasearch engine — individual upstream engines may CAPTCHA or rate-limit. If results are weak, try:
- More specific query or bang (`!github`, `!stackoverflow`, `!mdn`, `!npm`, `!pypi`)
- `--engines brave,bing` for general web fallback
- `--category it` for coding-focused search
- Avoid forcing Google/DuckDuckGo/Startpage (CAPTCHA-prone)
