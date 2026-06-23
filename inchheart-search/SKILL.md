---
name: inchheart-search
description: "InchHeart 搜索、联网研究与网页抓取技能：用于通过本机 SearXNG 搜索资料、查询文档和 GitHub 项目，选择 defuddle/curl/firecrawl/Obscura/Camoufox 等抓取工具，排查 SearXNG 配置/YAML 问题，并完成网页抓取、JS 渲染、截图、登录交互、CDP/MCP 和反指纹浏览任务。"
---

# inchheart-search

InchHeart's integrated web research hub. It covers search, page extraction, rendered scraping, and browser interaction.

| File | What | When to read |
|------|------|-------------|
| `scripts/inchheart-search` | CLI search tool (Bash + Python) | User asks to search the web through local SearXNG |
| `references/CONFIGURATION.md` | SearXNG setup, YAML traps, engine mgmt, health check | User asks about SearXNG config, engines, YAML pitfalls, or troubleshooting |
| `references/WORKFLOW.md` | Firecrawl-first research pipeline plus local fallback selection | User wants full search-then-scrape workflow, batch fetch, or page monitoring |
| `references/FIRECRAWL.md` | Firecrawl CLI, auth, command split, and local usage | User asks how Firecrawl works, what commands it exposes, or how this machine uses it |
| `references/OBSCURA.md` | Obscura commands, `--dump` modes, CDP/MCP, scrape, V8 bug, source build | User needs local/private rendered fetch, text/HTML/Markdown, links/assets, CDP, MCP, or internal-service fetch |
| `references/CAMOUFOX.md` | Camoufox Python API, screenshots, click/input, cookie persistence, resource blocking | User needs anti-fingerprinting, complex login state, or Python browser scripts |

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
- User asks which networking/search/scraping/browser tool to use
- User asks for SearXNG configuration or engine tuning → read `references/CONFIGURATION.md`
- User wants to scrape pages after searching → read `references/WORKFLOW.md`
- User asks how Firecrawl CLI/auth/command split works → read `references/FIRECRAWL.md`
- User wants fast batch page fetch, rendered text/HTML/Markdown, or CDP/MCP → read `references/OBSCURA.md`
- User needs click, form fill, screenshots, Cookie, or network interception → prefer `agent-browser`
- User needs anti-fingerprinting, complex login state, or Python browser scripts → read `references/CAMOUFOX.md`
- User asks about search formats, JSON API, or category-based search
- User asks about YAML pitfalls, engine failures, or SearXNG fault-finding

Do NOT use for:
- High-stakes facts requiring cited sources (use built-in web search)
- Searching private notes or secrets

## Tool Selection

Check live availability with `command -v <tool>` before relying on a tool. Current preferred order:

| 任务 | 首选 | 兜底 | 说明 |
|---|---|---|---|
| 最新事实、新闻、价格、政策、需要引用 | OpenAI built-in web search when available | `firecrawl search` | OpenAI 工具只有 Codex/OpenAI 环境可能有；Pi/Hermes/OpenCode 通常不能直接用 |
| 综合搜索、单页抓取、爬站、站点地图 | `firecrawl` | SearXNG + local fetch tools | 一站式、额度充足时作为非 Codex CLI 的默认联网工具；较慢且 API-backed |
| 找资料入口、GitHub/文档/包发现 | `scripts/inchheart-search` / local SearXNG | `firecrawl search` | 本机私有元搜索；适合先定位 URL |
| 普通文章、博客、文档正文清洗 | `defuddle parse URL` | `firecrawl scrape` | 最快得到干净 Markdown |
| 原始 HTML、HTTP 头、API 检查 | `curl` | Obscura `--dump original` | 不需要浏览器渲染时优先 |
| JS 渲染页面、批量渲染文本/HTML/Markdown | `firecrawl scrape` | `obscura` | Firecrawl 已能覆盖大多数 JS-heavy 页面；本机/private 页面再用 Obscura |
| 点击、填表、截图、Cookie、网络拦截 | `agent-browser` | Camoufox/Playwright | 交互式网页任务首选 |
| 反指纹、复杂登录态、长 Python 浏览器脚本 | Camoufox/Playwright | `agent-browser` | 高级兜底，不作为普通交互默认工具 |
| GitHub release/issue/repo/API | `gh api` / `gh search` | SearXNG/GitHub web | GitHub 专用，比普通网页搜索更准 |

Browser tool boundary:

| 工具 | 默认角色 | 不要用于 |
|---|---|---|
| `obscura` | 本机/private 只读渲染抓取、批量读取页面文本/HTML/Markdown | 常规公网页面、登录、连续点击、复杂表单 |
| `agent-browser` | 真实页面交互、截图、Cookie、网络拦截 | 大批量只读抓取 |
| Camoufox/Playwright | 反指纹、复杂登录态、长期脚本化浏览器流程 | 普通文章和简单搜索 |

On this machine, Camoufox may trigger a large browser runtime download before first use. Do not use it for routine page reads or simple interaction tests.

For Pi, Hermes, OpenCode, or other CLIs without OpenAI's built-in web tool, prefer `firecrawl` for broad web research and most public-page scraping. Use SearXNG + `defuddle`/`obscura`/`agent-browser` only when the task is narrower, private/local, cheaper to do locally, or needs local browser control.

Do not print Firecrawl API keys. If using Firecrawl inside a repository, keep `.firecrawl/` cache ignored.

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
