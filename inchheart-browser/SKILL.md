---
name: inchheart-browser
description: Headless browser toolkit — Obscura (Go, fast, lightweight) for batch scraping & CDP/MCP, Camoufox (Python, Playwright) for interaction, screenshots, login, and anti-fingerprinting. Read OBSCURA.md or CAMOUFOX.md for detailed usage.
tags: [browser, scraping, obscura, camoufox, headless]
---

# inchheart-browser

Two headless browsers for different needs:

| Tool | Language | Speed | Memory | Best for |
|------|----------|-------|--------|----------|
| **Obscura** | Go | ⚡⚡⚡ | Low | Batch fetch rendered text/HTML/MD, CDP service, MCP agent |
| **Camoufox** | Python | ⚡ | High | Page interaction, login, screenshots, anti-fingerprinting |

When to read each file:

| File | Read when user asks about |
|------|--------------------------|
| `OBSCURA.md` | `obscura fetch` commands, `--dump` modes, CDP/MCP, scrape, V8 bug, build from source |
| `CAMOUFOX.md` | Camoufox Python API, screenshots, click/input, cookie persistence, resource blocking |

## Quick Reference

### Obscura — batch fetch

```bash
# Original HTTP (fastest, no browser)
obscura fetch --dump original --timeout 15 "https://example.com"

# Rendered text (cleaned)
obscura fetch --dump text --timeout 15 "https://example.com"

# Rendered Markdown
obscura fetch --dump markdown --timeout 15 "https://example.com"

# With proxy (Clash)
obscura fetch --dump original --proxy http://127.0.0.1:7897 "https://example.com"

# Internal service
obscura fetch --dump original --allow-private-network "http://127.0.0.1:3000"

# CDP server
obscura serve --port 9333 --workers 4

# MCP mode (for AI agents)
obscura mcp
```

### Camoufox — interaction & screenshots

```python
from camoufox.sync_api import Camoufox

with Camoufox(headless=True) as browser:
    page = browser.new_page()
    page.goto('https://example.com')

    title = page.title()
    page.screenshot(path='/tmp/screenshot.png')
    page.click('button#submit')
    page.fill('input#search', 'query')

    page.close()
```

### Concurrency (Obscura)

```python
import subprocess, concurrent.futures

def fetch(url):
    r = subprocess.run(['obscura', 'fetch', '--dump', 'original', '--timeout', '15', url],
                       capture_output=True, text=True, timeout=20)
    return r.stdout

with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    results = list(ex.map(fetch, ['https://a.com', 'https://b.com', 'https://c.com']))
```

### SearXNG integration

Use the JSON API (`?format=json`) from `inchheart-search`. Camoufox rendering of search result pages is an alternative when JS execution is needed.

## When To Use

- **Small batch, fast → Obscura** (startup ms, low memory, no overhead)
- **Large batch pages → Obscura** (multiprocess, concurrency flag)
- **Need click/form/login → Camoufox**
- **Need screenshot → Camoufox** (`page.screenshot()`)
- **Need CDP protocol → Obscura** (`obscura serve`)
- **Need MCP AI agent → Obscura** (`obscura mcp`)
- **Need anti-fingerprinting → Camoufox**

## Notes

- Obscura v0.1.0 binary has V8 bug. **Fix:** build from source (`cargo build --release`). See `OBSCURA.md` for details.
- Camoufox uses Playwright Firefox under the hood. Install via `uv tool install camoufox && camoufox install`.
