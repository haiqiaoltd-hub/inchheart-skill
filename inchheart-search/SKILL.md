---
name: inchheart-search
description: "InchHeart 搜索、网页研究与无头浏览器技能：用于通过本机 SearXNG 搜索资料、查询文档和 GitHub 项目，排查 SearXNG 配置/YAML 问题，并使用 Obscura、Camoufox 完成网页抓取、JS 渲染、截图、登录交互、CDP/MCP 和反指纹浏览任务。"
---

# inchheart-search

InchHeart's integrated web research hub. Five parts:

| File | What | When to read |
|------|------|-------------|
| `scripts/inchheart-search` | CLI search tool (Bash + Python) | User asks to search the web through local SearXNG |
| `CONFIGURATION.md` | SearXNG setup, YAML traps, engine mgmt, health check | User asks about SearXNG config, engines, YAML pitfalls, or troubleshooting |
| `WORKFLOW.md` | Search → Obscura/Camoufox scraping pipeline | User wants full search-then-scrape workflow, batch fetch, or page monitoring |
| `OBSCURA.md` | Obscura commands, `--dump` modes, CDP/MCP, scrape, V8 bug, source build | User needs fast batch fetch, rendered text/HTML/Markdown, links/assets, CDP, MCP, or internal-service fetch |
| `CAMOUFOX.md` | Camoufox Python API, screenshots, click/input, cookie persistence, resource blocking | User needs page interaction, login, screenshots, anti-fingerprinting, or JS-heavy pages |

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
- User wants fast batch page fetch, rendered text/HTML/Markdown, or CDP/MCP → read OBSCURA.md
- User needs login, click, form fill, screenshots, anti-fingerprinting, or JS-heavy interaction → read CAMOUFOX.md
- User asks about search formats, JSON API, or category-based search
- User asks about YAML pitfalls, engine failures, or SearXNG fault-finding

Do NOT use for:
- High-stakes facts requiring cited sources (use built-in web search)
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
