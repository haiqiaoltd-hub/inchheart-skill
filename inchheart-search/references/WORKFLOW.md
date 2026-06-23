# 网页研究与爬取工作流

**核心策略：** Firecrawl 默认处理公网搜索/抓取/爬站；本机工具只在私有、本地、交互或轻量专用场景补位。更多 Firecrawl 命令与鉴权细节见 `FIRECRAWL.md`。

```
Firecrawl 综合联网                 本机补位工具
      ↓                              ↓
 search / scrape / crawl / map     SearXNG / defuddle / curl / obscura / agent-browser
 适合公网和综合研究                适合本地、私有、交互、低成本或专用任务
```

## 工具选择

| 任务 | 首选工具 | 兜底 | 示例 |
|---|---|---|---|
| 最新事实、新闻、价格、政策、需要引用 | OpenAI built-in web search | `firecrawl search` | 非本机命令 |
| 综合搜索、单页抓取、爬站、站点地图 | `firecrawl` | SearXNG + local fetch tools | `firecrawl search "query"` / `firecrawl scrape URL` |
| 找资料入口、GitHub/文档/包发现 | `scripts/inchheart-search` / SearXNG | `firecrawl search` | `scripts/inchheart-search "site:docs.rs tokio"` |
| 普通文章、博客、文档正文清洗 | `defuddle` | `firecrawl scrape` | `defuddle parse "https://example.com"` |
| 原始 HTML、HTTP 头、API 检查 | `curl` | Obscura `--dump original` | `curl -I "https://example.com"` |
| JS 渲染网页、批量渲染文本/HTML/Markdown | `firecrawl scrape` | `obscura` | `firecrawl scrape URL --format markdown` |
| 点击、填表、截图、Cookie、网络拦截 | `agent-browser` | Camoufox/Playwright | `agent-browser open "https://example.com"` |
| 反指纹、复杂登录态、长 Python 浏览器脚本 | Camoufox/Playwright | `agent-browser` | `from camoufox.sync_api import Camoufox` |
| GitHub release、issue、repo、API | `gh` | SearXNG/GitHub web | `gh api repos/owner/repo/releases/latest` |

浏览器三件套边界：

| 工具 | 默认角色 | 使用条件 | 避免 |
|---|---|---|---|
| `obscura` | 本机/private 只读渲染抓取 | 公网 Firecrawl 效果差、需要抓本地服务、内网/private 页面，或不想走云端 API | 常规公网页面、登录、连续点击、复杂表单 |
| `agent-browser` | 真实页面交互 | 用户说“去网站完成一件事”、需要点击/填表/截图/Cookie/网络拦截 | 大批量只读抓取 |
| Camoufox/Playwright | 高级浏览器兜底 | 需要反指纹、复杂登录态、长脚本、Firefox 行为或 agent-browser 不够 | 普通文章、简单搜索、一次性截图 |

本机实测：Camoufox 首次使用可能先下载约 304MB 浏览器运行时；因此不要把它作为常规浏览器默认项。需要反指纹/复杂登录态时再接受这笔启动成本。

如果用户要求“去网站完成一件事”（跨页面导航、登录、填表、下单、保留 Cookie、网络拦截），优先现场检查 `agent-browser`。不存在或不够用时，才使用 Camoufox/Playwright 脚本完成。

对 Pi、Hermes、OpenCode 这类没有 OpenAI 原生联网工具的 CLI：

1. 综合联网研究和大多数公网页面抓取默认优先 `firecrawl`，因为它同时支持 `search`、`scrape`、`crawl`、`map` 和 `agent`。
2. 需要本机私有搜索或避免云端 API 时，用 SearXNG：`scripts/inchheart-search "query"`。
3. 已知 URL 且是普通文章，用 `defuddle`。
4. 已知公网 URL 且需要 JS 渲染或批量抓取，先用 `firecrawl scrape`；如果是本地/private 页面或 Firecrawl 效果差，再用 `obscura`。
5. 需要真实页面交互，用 `agent-browser`；只有反指纹、复杂登录态或长脚本需求时才用 Camoufox/Playwright。
6. GitHub 相关事实优先 `gh api`，少走网页搜索。

## 标准工作流

### 阶段 1：Firecrawl 综合研究

```bash
# 搜索并返回结果
firecrawl search "目标主题"

# 已知公网 URL，提取 Markdown
firecrawl scrape "https://example.com" --format markdown --only-main-content

# 站点级 URL 发现
firecrawl map "https://example.com"

# 小型站点爬取
firecrawl crawl "https://example.com"
```

### 阶段 2：本机补位

只在以下情况进入本机补位：

- 目标是 `localhost`、内网、私有服务或不希望走云端 API。
- Firecrawl 抓取结果噪声过多、缺字段或无法访问。
- 用户要实际操作页面，而不是只读内容。
- 用户明确要求使用本机 SearXNG、Obscura、agent-browser 或 Camoufox。

#### SearXNG 搜索定位

```bash
scripts/inchheart-search "目标主题" --limit 8
scripts/inchheart-search "site:docs.rs tokio" --engines brave,bing
```

#### Defuddle 文章清洗

```bash
defuddle parse "https://example.com/article"
```

#### Obscura 本机只读渲染抓取

```bash
# 渲染后文本（推荐）
obscura fetch --dump text --timeout 15 "https://example.com"

# 渲染后 HTML
obscura fetch --dump html --timeout 15 "https://example.com" -o page.html

# 原始 HTTP 响应（最快，不经过浏览器）
obscura fetch --dump original --timeout 15 "https://example.com"

# 带代理（翻墙）
obscura fetch --dump text --proxy http://127.0.0.1:7897 "https://example.com"

# 内网地址需加 --allow-private-network
obscura fetch --dump text --allow-private-network "http://127.0.0.1:3000/page"
```

#### Agent-browser 真实交互

```bash
agent-browser open "https://example.com"
agent-browser snapshot
agent-browser click "@ref"
agent-browser screenshot /tmp/page.png
agent-browser close --all
```

#### Camoufox 高级兜底

Camoufox 只在需要反指纹、复杂登录态、Firefox 行为或长 Python 浏览器脚本时使用。普通抓取、一次性截图、简单点击优先 Firecrawl/Obscura/agent-browser。

## 进阶工作流

### Obscura 批量并发抓取

```python
import subprocess
import concurrent.futures

def fetch_page(url):
    try:
        result = subprocess.run(
            ['obscura', 'fetch', '--dump', 'original', '--timeout', '15', url],
            capture_output=True, text=True, timeout=20
        )
        return {'url': url, 'content': result.stdout, 'success': True}
    except Exception as e:
        return {'url': url, 'error': str(e), 'success': False}

urls = ['https://example.com', 'https://example.org', 'https://example.net']
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(fetch_page, urls))

for r in results:
    if r['success']:
        print(f"✓ {r['url']}: {len(r['content'])} 字符")
    else:
        print(f"✗ {r['url']}: {r['error']}")
```

### 递归爬取（优先 Firecrawl）

```bash
firecrawl crawl "https://example.com"
firecrawl map "https://example.com"
```

### 监控页面变化

```python
import hashlib
import json
import subprocess
from pathlib import Path

CACHE_FILE = '/tmp/page_cache.json'

def monitor_pages(urls):
    cache = json.loads(Path(CACHE_FILE).read_text()) if Path(CACHE_FILE).exists() else {}
    changes = []

    for url in urls:
        result = subprocess.run(
            ['firecrawl', 'scrape', url, '--format', 'markdown', '--only-main-content'],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            content = result.stdout
            content_hash = hashlib.md5(content.encode()).hexdigest()

            if url in cache:
                if cache[url] != content_hash:
                    changes.append({'url': url, 'status': 'changed'})
                else:
                    print(f"✓ 无变化：{url}")
            else:
                changes.append({'url': url, 'status': 'new'})

            cache[url] = content_hash
        else:
            changes.append({'url': url, 'status': 'error', 'error': result.stderr})

    Path(CACHE_FILE).write_text(json.dumps(cache, indent=2))
    return changes
```

## 常见陷阱

| 问题 | 原因 | 解决 |
|------|------|------|
| 被封 IP | 请求太频繁 | 加延迟、用代理、轮换 UA |
| JS 内容获取不到 | 工具未渲染或等待不足 | 先用 `firecrawl scrape`，本机兜底用 Obscura |
| Obscura scrape 报 Read failed | 旧版 worker 崩溃 | 重新编译 `obscura-worker` |
| Obscura 连不上内网 | SSRF 防护 | 加 `--allow-private-network` |
| 内存占用高 | 浏览器实例过多 | 复用实例、及时关闭页面 |

## 工具对比

| 工具 | 速度 | 深度 | 场景 |
|------|------|------|------|
| **Firecrawl** | ⚡⚡ | 深 | 默认公网搜索、抓取、爬站、站点地图 |
| **SearXNG** | ⚡⚡⚡ | 浅 | 本机私有搜索、URL 发现 |
| **Defuddle** | ⚡⚡⚡ | 中 | 普通文章/文档正文清洗 |
| **Obscura** | ⚡⚡ | 中 | 本机/private 渲染抓取、CDP/MCP |
| **agent-browser** | ⚡⚡ | 深 | 页面交互、截图、Cookie、网络拦截 |
| **Camoufox** | ⚡ | 深 | 反指纹、复杂登录态、高级兜底 |

*最后更新：2026-06-23*
