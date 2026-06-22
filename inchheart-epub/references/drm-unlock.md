---
name: inchheart-epub-drm-unlock
description: 移除 EPUB 声明性 DRM（多看/掌阅/京东等）— 检测 encryption.xml，验证内容未加密，剥离 DRM 声明，按 EPUB 规范重打包
tags: [epub, drm, duokan, ireader, ebook]
---

# 声明性 DRM 解锁（次要附录）

> 适用场景：EPUB 锁了、只能在多看/掌阅/京东读书打开，Calibre/Apple Books/Koodo/Thorium 打不开。
>
> **如果 EPUB 已经被 `inchheart-epub` 处理过（混淆文件名已还原），本附录依然适用**——两者是独立的清理步骤。

## 适用场景

触发条件（满足任一）：

- 用户说 EPUB "锁了" / "打不开" / "要登录"
- EPUB 只能在多看/掌阅打开，Calibre/Apple Books 失败
- `unzip -l` 显示 `META-INF/encryption.xml`
- OPF 包含 `<dc:identifier id="duokan-book-id">`

## 不适用场景

- **Adobe Adept** — 真实加密
- **Apple FairPlay** — 真实加密
- **Readium LCP** — `license.lcpl` + 真实 AES
- **Kindle** — 非 EPUB 格式
- 字节实际不可读（真实加密）

## 决策流程

```
1. unzip -l <file>.epub → 查 META-INF/encryption.xml
   ├─ 不存在 → 非声明性 DRM，停止
   └─ 存在 → 继续

2. unzip -p <file>.epub META-INF/encryption.xml
   检查 CipherReference：
   ├─ 仅 stylesheet → 99% 安全可移除
   ├─ 所有 xhtml/opf → 真实加密，停止
   └─ 不确定 → 抽查 xhtml：unzip -p ... | head
                UTF-8 中文 → 明文

3. 抽查字体：
   unzip -p <file>.epub "OEBPS/Fonts/*.ttf" | head -c 4
   → 00 01 00 00 (TTF) = 未加密

4. 判断：
   ├─ 声明性 DRM → 执行解锁
   └─ 真实加密 → 停止，告知用户
```

## 解锁步骤

**永远不覆盖原文件**，输出 `<原名>_unlocked.epub`。

```bash
SRC="<path>/<name>.epub"
DIR="$(dirname "$SRC")"
BASE="$(basename "$SRC" .epub)"
OUT="${DIR}/${BASE}_unlocked.epub"
WORK="$(mktemp -d)"

# 1. 解包
unzip -q "$SRC" -d "$WORK"

# 2. 移除 DRM 声明
rm -v "$WORK/META-INF/encryption.xml"

# 3. 重打包（EPUB 规范）
cd "$WORK"
zip -X0q "$OUT" mimetype
zip -Xrq9DX "$OUT" META-INF OEBPS -x "*.DS_Store"

# 4. 清理
rm -rf "$WORK"
```

## 验证清单（必须全部通过）

```bash
# A. mimetype 正确且未压缩
unzip -p "$OUT" mimetype                # 必须：application/epub+zip
unzip -v "$OUT" | head -3               # Method = "Stored"

# B. 无 DRM 残留
unzip -l "$OUT" | grep -iE "(encrypt|right)" || echo "OK"

# C. 内容可解析
unzip -p "$OUT" OEBPS/content.opf | head -5
unzip -p "$OUT" OEBPS/Text/*.xhtml | head -5
```

## 多平台识别

| 信号 | 平台 |
|------|------|
| `DuoKan.Inc` / `duokan-book-id` | 多看 |
| `iReader.Inc` / `ireader-` | 掌阅 |
| `JDReader.Inc` / `jdreader-` | 京东 |
| `Sursen.Inc` / `sursen-` | 书生 |
| `aes128-ctr` | 多看系 |
| `aes128-cbc` | 掌阅系 |

## Pitfalls

- ❌ **不要**用 `zip -r` — 添加 `__MACOSX/` 垃圾，用 `-X`
- ❌ **不要**压缩 mimetype — epubcheck 会拒绝
- ❌ **不要**假设 encryption.xml 是假的 — 先抽查
- ❌ **不要**覆盖原文件 — macOS Finder 会混淆

## 汇报模板

1. **发现**：哪个 DRM，什么被声明加密
2. **验证**：xhtml 抽查确认明文
3. **改动**：仅移除 `encryption.xml`
4. **位置**：完整路径
5. **可选**：是否恢复混淆文件名（见主 SKILL.md 的 6 步流程）

## 相关

- 还原混淆文件名（优化主线）→ `../SKILL.md`
- 电子书入库分类 → `inchheart-assets`
