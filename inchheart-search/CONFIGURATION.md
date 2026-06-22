# SearXNG 配置优化与个性化

## 本机配置概要

- **地址：** `http://127.0.0.1:8888`
- **配置文件：** `/Users/mac/Repository/Services/Local/Tools/SearXNG/settings.yml`
- **源码：** `/Users/mac/Repository/Services/Local/Tools/SearXNG/searxng-source/`
- **日志：** `/Users/mac/Repository/Services/Local/Tools/SearXNG/searxng.log`
- **启动：** `/Users/mac/Repository/Services/Local/Tools/SearXNG/start-searxng.sh`
- **停止：** `/Users/mac/Repository/Services/Local/Tools/SearXNG/stop-searxng.sh`
- **服务管理：** launchctl（`local.searxng.plist`），非 Docker

### 当前 7 个 Tab 分类

| Tab 分类 | 标签名 | 引擎 |
|----------|--------|------|
| general | 综合 | Google, Bing |
| dev | 编程 | GitHub, GitLab, npm, PyPI, HackerNews, Ollama, HuggingFace, StackOverflow |
| music | 音乐 | SoundCloud, Freesound, Bandcamp, Genius, Deezer, Mixcloud |
| images | 搜图 | Pinterest, DeviantArt, Imgur, Wallhaven, 500px, ArtStation, Openverse, Pixiv |
| academic | 学术 | arXiv, Wikipedia, PubMed, Crossref, OpenAlex, Google Scholar |
| videos | 视频 | YouTube, Dailymotion |
| downloads | 下载 | PirateBay, SolidTorrents, BT4G |

## 核心原则

**目标：** 根据用户兴趣领域定制搜索引擎，提升搜索结果的相关性和覆盖范围。

**工作方法：**
1. 分析用户兴趣领域确定需要的引擎
2. 用 `use_default_settings.engines.keep_only` 精简引擎列表
3. 调整引擎权重（高权重 = 更可靠的结果来源）
4. 用 `categories_as_tabs` 设置中文标签
5. 验证引擎是否真实存在（部分引擎名带下划线会失败）

## JSON API 使用

```bash
# 综合搜索
curl "http://127.0.0.1:8888/search?q=test&format=json" | jq '.results[:3]'

# 按分类搜索
curl "http://127.0.0.1:8888/search?q=FastAPI&categories=dev&format=json" | jq '.results[:3]'

# POST 方式
curl -X POST -d "q=Python&format=json" "http://127.0.0.1:8888/search"
```

Python 提取：

```python
import requests

def search_json(query, categories='general', max_results=10):
    resp = requests.get(
        'http://127.0.0.1:8888/search',
        params={'q': query, 'categories': categories, 'format': 'json'},
        timeout=15
    )
    return resp.json().get('results', [])[:max_results]
```

若需要 JS 渲染或绕过反爬，备选 Camoufox 渲染搜索结果页：

```python
from camoufox.sync_api import Camoufox

def search_camoufox(query, categories='general', max_results=10):
    url = f"http://127.0.0.1:8888/?q={query}&categories={categories}"
    with Camoufox(headless=True) as browser:
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')
        page.wait_for_selector('article', timeout=10000)
        items = page.evaluate('''() =>
            [...document.querySelectorAll('article')].map(a => ({
                title: a.querySelector('h3')?.innerText?.trim() || '',
                url: a.querySelector('a[href^="http"]')?.href || '',
                description: a.querySelector('.content')?.innerText?.trim()?.slice(0,200) || ''
            }))
        ''')
        page.close()
    return items[:max_results]
```

## settings.yml 配置模板

### 核心结构

```yaml
use_default_settings:
  engines:
    keep_only:
      - google
      - bing
      - github

general:
  instance_name: "SearXNG 本机"
  default_lang: "zh-CN"
  default_theme: simple
  default_number_of_results: 15

search:
  safe_search: 0
  autocomplete: "google"
  formats: [html, csv, json, rss]

server:
  port: 8888
  bind_address: "127.0.0.1"
  limiter: false
  image_proxy: true

categories_as_tabs:
  general: 综合
  dev: 编程
  music: 音乐
  images: 搜图
  academic: 学术
  videos: 视频
  downloads: 下载
```

### 引擎权重配置

```yaml
engines:
  - name: google
    categories: general
    disabled: false
    weight: 3.0

  - name: github
    categories: dev
    disabled: false
    weight: 3.0

  - name: stackoverflow
    categories: dev
    disabled: false
    weight: 2.5
```

## YAML 配置陷阱

### 陷阱 1：引擎名含下划线失败

**错误表现：** `google_images`、`semantic_scholar`、`stackexchange` 加载失败。

**原因：** SearXNG 引擎名使用空格而非下划线。

**正确名称：**
- `google`（不是 `google_images`）
- `google scholar`（不是 `semantic_scholar`）
- `stackoverflow`（不是 `stackexchange`）

### 陷阱 2：categories_as_tabs 格式错误

```yaml
# ✅ 正确
categories_as_tabs:
  general: 综合搜索

# ❌ 错误：缺少空格
categories_as_tabs:
  dev:编程开发

# ❌ 错误：中文冒号
categories_as_tabs:
  dev：编程开发
```

### 陷阱 3：自定义分类不生效

SearXNG 引擎的分类硬编码在 Python 引擎文件中，配置的 `categories` 字段不会覆盖引擎代码。使用内置分类名，在 `categories_as_tabs` 中映射到中文显示名。

常用内置分类：`general`, `images`, `videos`, `music`, `dev`, `academic`, `downloads`。

### 陷阱 4：被移除的引擎（中国网络环境不可用）

| 引擎 | 原因 |
|------|------|
| DuckDuckGo | CAPTCHA |
| Startpage | CAPTCHA |
| Vimeo | 访问拒绝 |
| Unsplash | 访问拒绝 |
| Pexels | 访问拒绝 |
| Bilibili | 解析错误 |
| Brave | 已移除 |
| Reddit | 已移除 |
| Google Images | 已移除（改用 image 分类下 `google`） |
| Semantic Scholar | 引擎名含下划线 |

## 性能优化

```yaml
server:
  cache:
    enabled: true
    max_age: 300
    method: memory

outgoing:
  request_timeout: 5.0
  max_request_timeout: 10.0
  pool_connections: 15
  pool_maxsize: 25
  enable_http2: true
```

## 部署与验证

### 启动脚本

```bash
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_FILE="$ROOT_DIR/local.searxng.plist"
PORT=8888

if lsof -i :$PORT -nP | grep -q LISTEN; then
    echo "端口 $PORT 已被占用"
    exit 1
fi

launchctl bootstrap "gui/$(id -u)" "$PLIST_FILE"

for _ in {1..20}; do
    if curl -fsS -I http://127.0.0.1:$PORT/ >/dev/null 2>&1; then
        echo "✓ SearXNG 已启动：http://127.0.0.1:$PORT"
        exit 0
    fi
    sleep 1
done

echo "✗ 启动超时"
exit 1
```

### 健康检查

```bash
echo "=== SearXNG 健康检查 ==="

# 1. 检查进程
launchctl print "gui/$(id -u)/local.searxng" 2>/dev/null && echo "✓ 服务已注册" || echo "✗ 服务未注册"

# 2. 检查端口
lsof -i :8888 -nP | grep -q LISTEN && echo "✓ 端口监听正常" || echo "✗ 端口未监听"

# 3. JSON API 搜索测试
response_time=$(curl -s -o /dev/null -w "%{time_total}" "http://127.0.0.1:8888/search?q=test&format=json")
if [[ ${response_time%.*} -lt 15 ]]; then
    echo "✓ JSON API 响应时间：${response_time}s"
else
    echo "⚠ JSON API 响应慢：${response_time}s"
fi

echo "=== 健康检查完成 ==="
```

### 停止

```bash
launchctl bootout "gui/$(id -u)/local.searxng"
```

## 故障排查

### 服务启动失败

```bash
tail -50 /Users/mac/Repository/Services/Local/Tools/SearXNG/searxng.log
python3 -c "import yaml; yaml.safe_load(open('/Users/mac/Repository/Services/Local/Tools/SearXNG/settings.yml'))"
lsof -i :8888
```

### 引擎加载失败

```bash
grep "ERROR" /Users/mac/Repository/Services/Local/Tools/SearXNG/searxng.log | tail -20
ls /Users/mac/Repository/Services/Local/Tools/SearXNG/searxng-source/searx/engines/*.py | grep -E "pinterest|soundcloud"
```

## 已知问题

- ~~**JSON API 403**：已修复（2026-06-01），原因为默认 `searx/settings.yml` 中 `formats` 只含 `html`，已在用户配置中覆盖为 `[html, csv, json, rss]`。~~
- **引擎超时：** `bt4g` 和 `piratebay` 经常超时，`solidtorrents` 解析错误——下载分类在 CN 网络环境不稳定。
- **`limiter.toml` 缺失：** 日志警告 botdetection 配置文件缺失。不影响功能。

## 参考资料

- SearXNG 官方文档：https://docs.searxng.org/
- 引擎列表：https://docs.searxng.org/admin/settings/settings.html#engines
- 本项目配置：`/Users/mac/Repository/Services/Local/Tools/SearXNG/settings.yml`

*最后更新：2026-06-01*
