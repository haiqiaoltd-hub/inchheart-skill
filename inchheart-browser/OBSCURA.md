# Obscura 使用参考

Obscura 是 Go 实现的轻量无头浏览器（基于 Chromium CDP 协议），也支持纯 HTTP 抓取。**批量快速抓取首选。**

> ⚠️ 官方 `v0.1.0-v0.1.6` 二进制有 V8 清理 bug（`--dump text/html/markdown/links` 卡死）。**已从源码自编译修复，所有 `--dump` 模式正常。** 升级见"从源码构建"节。

## 安装路径

| 文件 | 路径 |
|------|------|
| 二进制 | `/Users/mac/.local/bin/obscura` |
| worker | `/Users/mac/.local/bin/obscura-worker` |
| 代理包装 | `/Users/mac/.local/bin/obscura-proxy` |

验证：`obscura --version`

## `fetch --dump` 模式

> 注意 `--dump` 是 `obscura fetch` 的子选项，不是顶层选项。

| 模式 | 说明 | 稳定性 |
|------|------|--------|
| `original` | 原始 HTTP 响应（不经过浏览器，最快） | ✅ 通用稳定 |
| `text` | 渲染后纯文本（去干扰） | ✅ 自编译版 |
| `html` | 渲染后 HTML | ✅ 自编译版 |
| `markdown` | 渲染后 Markdown | ✅ 自编译版 |
| `links` | 页面链接列表 | ✅ 自编译版 |
| `assets` | 页面资源清单 | ✅ 自编译版 |

```bash
# 原始 HTTP（日常抓取首选）
obscura fetch --dump original "https://example.com"
obscura fetch --dump original --timeout 30 "https://example.com" -o page.html

# 渲染后文本（去干扰）
obscura fetch --dump text --timeout 15 "https://example.com"

# 渲染后 HTML / Markdown
obscura fetch --dump html --timeout 15 "https://example.com"
obscura fetch --dump markdown --timeout 15 "https://example.com"

# 链接 / 资源清单
obscura fetch --dump links --timeout 15 "https://example.com"
obscura fetch --dump assets --timeout 15 "https://example.com"
```

## 代理

```bash
# HTTP 代理（Clash 翻墙）
obscura fetch --dump original --proxy http://127.0.0.1:7897 "https://example.com"

# SOCKS5
obscura fetch --dump original --proxy socks5://127.0.0.1:7897 "https://example.com"

# 内网直连（必须有 --allow-private-network）
obscura fetch --dump original --allow-private-network "http://127.0.0.1:3000/page"
```

代理包装脚本：

```bash
obscura-proxy fetch --dump original "https://example.com"
# 等价于 obscura --proxy http://127.0.0.1:7897 fetch ...
```

## CDP 模式

```bash
obscura serve --port 9333 --workers 4
# WebSocket: ws://127.0.0.1:9333/devtools/browser
```

## MCP 模式（AI Agent 集成）

```bash
# stdio
obscura mcp

# HTTP
obscura mcp --http --port 8080
```

## `scrape` 批量

```bash
obscura scrape --timeout 30 --concurrency 5 "https://a.com" "https://b.com"
obscura scrape --quiet --timeout 30 --concurrency 10 urls.txt
obscura scrape --eval "document.title" "https://example.com"
```

> 旧版 `obscura-worker` 导致 "Read failed"，升级后已修复。

## 并发抓取（Python）

```python
import subprocess
import concurrent.futures

def fetch_page(url):
    try:
        result = subprocess.run(
            ['obscura', 'fetch', '--dump', 'original', '--timeout', '30', url],
            capture_output=True, text=True, timeout=35
        )
        return {'url': url, 'content': result.stdout, 'success': True}
    except subprocess.TimeoutExpired:
        return {'url': url, 'error': 'timeout', 'success': False}
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

## Shell 批量脚本

```bash
#!/usr/bin/env bash
URLS=("https://example.com" "https://example.org")
OUTPUT_DIR="/tmp/obscura-output"
mkdir -p "$OUTPUT_DIR"

for url in "${URLS[@]}"; do
    filename=$(echo "$url" | sed 's|https\?://||; s|/|_|g; s|[^a-zA-Z0-9_.-]|_|g')
    echo "抓取: $url"
    obscura fetch --dump original --timeout 15 "$url" > "$OUTPUT_DIR/$filename.html" 2>/dev/null
    if [ $? -eq 0 ] && [ -s "$OUTPUT_DIR/$filename.html" ]; then
        echo "  ✓ 保存到 $OUTPUT_DIR/$filename.html"
    else
        echo "  ✗ 失败"
    fi
done
```

## 故障排查

### fetch 卡死/无输出

**原因：** `--dump text/html/markdown/links/assets` 因 V8 bug 卡死。

**解决：** 使用 `--dump original`，或从源码重新编译。

```bash
obscura fetch --dump original "https://example.com" > page.html
timeout 20 obscura fetch --dump original --timeout 15 "https://example.com"
```

### "Read failed" 错误

**原因：** 旧版 `obscura-worker` V8 bug。

**解决：** 从源码重编译 `obscura-worker`。

### 无法连接内部服务

**原因：** SSRF 防护默认阻止内网。

**解决：** 加 `--allow-private-network`。

### 找不到命令

```bash
ls -la /Users/mac/.local/bin/obscura
export PATH="$HOME/.local/bin:$PATH"
```

## 从源码构建

```bash
# 前置：安装 Rust
# curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

gh repo clone h4ckf0r0day/obscura /tmp/obscura-src
cd /tmp/obscura-src
cargo build --release

cp target/release/obscura /Users/mac/.local/bin/obscura
cp target/release/obscura-worker /Users/mac/.local/bin/obscura-worker

# 验证
obscura fetch --dump text "https://example.com"
```

## 参考资料

- GitHub: https://github.com/nicholasgasior/obscura
- 本机帮助: `obscura --help`

*最后更新：2026-06-01*
