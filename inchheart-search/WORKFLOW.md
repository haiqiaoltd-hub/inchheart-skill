# 网页研究与爬取工作流

**核心策略：** SearXNG 搜索定位 → 无头浏览器深度抓取

```
SearXNG 搜索引擎                   无头浏览器
      ↓                              ↓
 标题 + URL + 摘要              完整 HTML / 渲染文本
 5-10 条结果/秒                 Obscura: 1-3 页/秒
 浅层信息                       Camoufox: 1-2 页/30 秒（含交互）
```

## 工具选择

| 场景 | 推荐工具 |
|------|----------|
| 渲染后文本/HTML/Markdown | Obscura `--dump text/html/markdown` |
| 原始 HTML（免渲染） | Obscura `--dump original` |
| 截图 | Camoufox `page.screenshot()` |
| 页面交互（点击/输入） | Camoufox |
| 登录态（Cookie 持久化） | Camoufox |
| 反指纹欺骗 | Camoufox |
| 批量抓取 10+ 页 | Obscura 多进程并发 |

## 标准工作流

### 阶段 1：搜索定位

```python
import requests

def search_searxng(query, categories='general', max_results=10):
    resp = requests.get(
        f"http://127.0.0.1:8888/search?q={query}&categories={categories}&format=json",
        timeout=15
    )
    return resp.json().get('results', [])[:max_results]

results = search_searxng('目标主题', categories='dev')

# 筛选高质量来源
urls_to_visit = []
for item in results:
    print(f"找到：{item['title']}")
    print(f"URL: {item['url']}")
    print(f"摘要：{item['description'][:100]}...")

    if any(domain in item['url'] for domain in [
        'github.com', 'medium.com', 'dev.to', 'arxiv.org'
    ]):
        urls_to_visit.append(item['url'])

print(f"\n准备深度访问 {len(urls_to_visit)} 个页面")
```

### 阶段 2a：Obscura 快速获取

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

### 阶段 2b：Camoufox 深度获取

```python
from camoufox.sync_api import Camoufox
import time

collected_data = []

with Camoufox(headless=True) as browser:
    for url in urls_to_visit[:5]:
        try:
            page = browser.new_page()
            print(f"\n访问：{url}")
            page.goto(url, wait_until='networkidle')
            page.wait_for_load_state('networkidle')

            data = {
                'url': page.url,
                'title': page.title(),
                'content': page.eval_on_selector('body', 'el => el.innerText'),
                'html': page.content(),
                'screenshot_path': f'/tmp/screenshot_{hash(url)}.png'
            }

            page.screenshot(path=data['screenshot_path'])
            collected_data.append(data)

            print(f"✓ 获取成功：{data['title']}")
            print(f"  内容长度：{len(data['content'])} 字符")

            page.close()
            time.sleep(2)

        except Exception as e:
            print(f"✗ 访问失败：{e}")
            continue

print(f"\n共成功获取 {len(collected_data)} 个页面")
```

### 阶段 3：数据处理

```python
for item in collected_data:
    print(f"\n{'='*60}")
    print(f"标题：{item['title']}")
    print(f"URL: {item['url']}")
    print(f"内容预览：{item['content'][:500]}...")
```

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

### 递归爬取（控制深度）

```python
def crawl_with_depth(seed_url, max_depth=2, visited=None):
    if visited is None:
        visited = set()
    if max_depth <= 0 or seed_url in visited:
        return []

    visited.add(seed_url)
    results = []

    with Camoufox(headless=True) as browser:
        page = browser.new_page()
        page.goto(seed_url, wait_until='networkidle')

        content = page.eval_on_selector('body', 'el => el.innerText')
        results.append({'url': seed_url, 'content': content, 'depth': max_depth})

        links = page.evaluate('''(baseUrl) => {
            return [...document.querySelectorAll('a')]
                .map(a => a.href)
                .filter(href => href.startsWith(baseUrl))
                .slice(0, 10)
        }''', seed_url.split('/')[2])

        page.close()

    for link in links[:3]:
        results.extend(crawl_with_depth(link, max_depth - 1, visited))

    return results
```

### 监控页面变化

```python
import hashlib
import json
from pathlib import Path

CACHE_FILE = '/tmp/page_cache.json'

def monitor_pages(urls):
    cache = json.loads(Path(CACHE_FILE).read_text()) if Path(CACHE_FILE).exists() else {}
    changes = []

    with Camoufox(headless=True) as browser:
        for url in urls:
            page = browser.new_page()
            page.goto(url, wait_until='networkidle')

            content = page.eval_on_selector('body', 'el => el.innerText')
            content_hash = hashlib.md5(content.encode()).hexdigest()

            if url in cache:
                if cache[url] != content_hash:
                    changes.append({'url': url, 'status': 'changed'})
                else:
                    print(f"✓ 无变化：{url}")
            else:
                changes.append({'url': url, 'status': 'new'})

            cache[url] = content_hash
            page.close()

    Path(CACHE_FILE).write_text(json.dumps(cache, indent=2))
    return changes
```

## 常见陷阱

| 问题 | 原因 | 解决 |
|------|------|------|
| 被封 IP | 请求太频繁 | 加延迟、用代理、轮换 UA |
| JS 内容获取不到 | 没等加载完成 | `wait_for_load_state('networkidle')` |
| Obscura scrape 报 Read failed | 旧版 worker 崩溃 | 重新编译 `obscura-worker` |
| Obscura 连不上内网 | SSRF 防护 | 加 `--allow-private-network` |
| 内存占用高 | 浏览器实例过多 | 复用实例、及时关闭页面 |

## 工具对比

| 工具 | 速度 | 深度 | 场景 |
|------|------|------|------|
| **SearXNG** | ⚡⚡⚡ | 浅 | 搜索、URL 发现 |
| **Obscura** | ⚡⚡ | 中 | 批量渲染抓取、CDP/MCP |
| **Camoufox** | ⚡ | 深 | 页面交互、登录、反指纹、截图 |
| **SearXNG + Obscura** | ⚡⚡⚡ + ⚡⚡ | 浅+中 | 推荐日常组合 |
| **SearXNG + Camoufox** | ⚡⚡⚡ + ⚡ | 浅+深 | 需要交互时的完整方案 |

*最后更新：2026-06-01*
