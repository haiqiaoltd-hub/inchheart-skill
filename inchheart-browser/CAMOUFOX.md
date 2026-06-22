# Camoufox 使用参考

Camoufox 是基于 Playwright Firefox 的反指纹浏览器。适用于需要页面交互、登录态、反爬绕过或截图的**深度爬取**。

## 安装

```bash
uv tool install camoufox
camoufox install   # 安装 Playwright 浏览器内核（Firefox）

# 验证
camoufox version
python3 -c "from camoufox.sync_api import Camoufox; print('✓ 安装成功')"
```

## 基本用法

### 同步 API

```python
from camoufox.sync_api import Camoufox

with Camoufox(headless=True) as browser:
    page = browser.new_page()
    page.goto('https://example.com')

    title = page.title()
    content = page.content()

    page.close()
```

### 异步 API

```python
from camoufox.async_api import AsyncCamoufox

async with AsyncCamoufox(headless=True) as browser:
    page = await browser.new_page()
    await page.goto('https://example.com')

    title = await page.title()
    content = await page.content()

    await page.close()
```

## 核心功能

### 获取页面信息

```python
with Camoufox(headless=True) as browser:
    page = browser.new_page()
    page.goto('https://example.com')
    page.wait_for_load_state('networkidle')

    title = page.title()
    url = page.url
    html = page.content()
    text = page.eval_on_selector('body', 'el => el.innerText')

    page.close()
```

### 执行 JavaScript

```python
with Camoufox(headless=True) as browser:
    page = browser.new_page()
    page.goto('https://example.com')

    info = page.evaluate('''() => ({
        userAgent: navigator.userAgent,
        webdriver: navigator.webdriver,  # Camoufox 返回 false
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    })''')

    print(info)
    page.close()
```

### 截图

```python
with Camoufox(headless=True) as browser:
    page = browser.new_page()
    page.goto('https://example.com')

    # 全屏截图
    page.screenshot(path='/tmp/screenshot.png')

    # 元素截图
    el = page.query_selector('.main-content')
    if el:
        el.screenshot(path='/tmp/element.png')

    page.close()
```

### 页面交互

```python
with Camoufox(headless=True) as browser:
    page = browser.new_page()
    page.goto('https://example.com')

    page.click('button#submit')
    page.fill('input#search', '关键词')
    page.press('input#search', 'Enter')
    page.evaluate('window.scrollBy(0, 500)')
    page.wait_for_selector('.result-item')

    page.close()
```

## 高级用法

### 会话持久化（Cookie）

```python
import json

# 登录并保存
with Camoufox(headless=True) as browser:
    page = browser.new_page()
    page.goto('https://example.com/login')
    page.fill('#username', 'user')
    page.fill('#password', 'pass')
    page.click('button[type="submit"]')

    cookies = page.context.cookies()
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f)
    page.close()

# 复用会话
with Camoufox(headless=True) as browser:
    page = browser.new_page()
    with open('cookies.json', 'r') as f:
        page.context.add_cookies(json.load(f))
    page.goto('https://example.com/protected')
    page.close()
```

### 资源拦截（加速）

```python
def route_handler(route, request):
    if request.resource_type in ['image', 'font', 'stylesheet']:
        route.abort()
    else:
        route.continue_()

with Camoufox(headless=True) as browser:
    page = browser.new_page()
    page.route('**', route_handler)
    page.goto('https://example.com')
```

## 故障排查

### ModuleNotFoundError

```bash
uv tool install camoufox
camoufox install
python3 -c "from camoufox.sync_api import Camoufox; print('✓ OK')"
```

### 'Browser' object has no attribute 'page'

**原因：** 使用了错误的导入方式。

```python
# ✅ 正确
from camoufox.sync_api import Camoufox
with Camoufox(headless=True) as browser:
    page = browser.new_page()

# ❌ 错误
from camoufox import Camoufox
```

### TypeError: NewBrowser() missing ...

**解决：** 使用 `from camoufox.sync_api import Camoufox`，不要用 `NewBrowser`。

### 页面加载超时

```python
page.goto('https://example.com', timeout=60000)
page.wait_for_load_state('networkidle', timeout=30000)
```

## 性能优化

1. **复用浏览器实例**：在循环外创建 `with Camoufox()` 块
2. **无头模式**：始终 `headless=True`
3. **资源拦截**：阻止图片/字体/CSS 加载
4. **并发控制**：限制同时打开的页面数量

## 参考资料

- 官网: https://camoufox.com/
- GitHub: https://github.com/daijro/camoufox
- 指纹: https://camoufox.com/fingerprint/
- Stealth: https://camoufox.com/stealth/

*最后更新：2026-06-01*
