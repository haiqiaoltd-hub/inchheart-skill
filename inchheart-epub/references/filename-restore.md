---
name: inchheart-epub-filename-restore
description: 还原 EPUB 内被多看/掌阅加扰的怪名字为正常文件名（次要附录）
tags: [epub, filename, duokan, ireader, restore]
---

# 还原混淆文件名（次要附录）

> 适用场景：EPUB 内文件名是 `\|:_*_:**_***:*\|.xhtml` 这种怪字符，OPF 里 `id` 是真名但 `href` 是 URL 编码后的加扰名。
>
> 通常是 `inchheart-epub` 元数据优化的**前置步骤**——先还原文件名，再做元数据清理。

## 触发判断

EPUB 内出现以下任一信号：

```
- OEBPS/Text/ 下文件名是 _:*_*_*|:*|*:*_.xhtml 这类含 *|:_ 符号的怪名
- OEBPS/Fonts/ 下文件名同样加扰
- OEBPS/content.opf 中 <item id="Author.xhtml" href="Text/%2A%3A%2A...xhtml">
   ↑ id 是真名，href 是 URL 编码后的加扰名
- 标题中文件名显示为 %2A%3A%2A...（URL 编码形式）
```

满足任一 → 走 6 步流程。

## 6 步流程

**永远不覆盖原文件**，输出 `<原名>_restored.epub`。

```bash
SRC="<path>/<name>.epub"
DIR="$(dirname "$SRC")"
BASE="$(basename "$SRC" .epub)"
OUT="${DIR}/${BASE}_restored.epub"
WORK="$(mktemp -d)"

# === 步骤 1：解包 ===
unzip -q "$SRC" -d "$WORK"

# === 步骤 2：从 OPF 构建 id → 真实文件名 映射表 ===
python3 - <<PY
import json, pathlib, urllib.parse
from xml.etree import ElementTree as ET

work = pathlib.Path("$WORK")
opf = work / "OEBPS" / "content.opf"
ns = {"opf": "http://www.idpf.org/2007/opf"}
tree = ET.parse(opf)
root = tree.getroot()

# id → 加扰文件名（href 解码后）
id_to_obfuscated = {}
for item in root.findall(".//opf:manifest/opf:item", ns):
    item_id = item.get("id")
    href = item.get("href")
    if item_id and href:
        decoded = urllib.parse.unquote(href)
        id_to_obfuscated[item_id] = decoded.split("/")[-1]

pathlib.Path("$WORK/_rename_map.json").write_text(
    json.dumps(id_to_obfuscated, ensure_ascii=False, indent=2)
)
print(f"映射条目数: {len(id_to_obfuscated)}")
PY

# === 步骤 3：批量重命名文件 ===
python3 - <<PY
import json, pathlib

work = pathlib.Path("$WORK")
mapping = json.loads((work / "_rename_map.json").read_text())

for item_id, old_name in mapping.items():
    for sub in ("Text", "Fonts", "Images", "Styles"):
        old_path = work / "OEBPS" / sub / old_name
        if old_path.exists():
            new_path = work / "OEBPS" / sub / item_id
            if new_path.exists():
                print(f"⚠️ 目标已存在，跳过: {new_path}")
                continue
            old_path.rename(new_path)
            print(f"✓ {sub}/{old_name} → {item_id}")
            break
PY

# === 步骤 4：重写 OPF 内的 href ===
python3 - <<PY
import json, pathlib, urllib.parse
work = pathlib.Path("$WORK")
mapping = json.loads((work / "_rename_map.json").read_text())

opf_path = work / "OEBPS" / "content.opf"
text = opf_path.read_text(encoding="utf-8")

for item_id, old_name in mapping.items():
    encoded = urllib.parse.quote(old_name)
    for sub in ("Text", "Fonts", "Images", "Styles"):
        text = text.replace(f'href="{sub}/{old_name}"', f'href="{sub}/{item_id}"')
        text = text.replace(f'href="{sub}/{encoded}"', f'href="{sub}/{item_id}"')

opf_path.write_text(text, encoding="utf-8")
print("✓ OPF href 已更新")
PY

# === 步骤 5：重写 CSS 和 xhtml 内的 url() / src= / href= 引用 ===
python3 - <<PY
import json, pathlib, urllib.parse
work = pathlib.Path("$WORK")
mapping = json.loads((work / "_rename_map.json").read_text())
rename_pairs = [(old, new) for new, old in mapping.items()]

for sub in ("Text", "Styles"):
    base = work / "OEBPS" / sub
    if not base.exists():
        continue
    for f in base.rglob("*"):
        if f.is_file() and f.suffix in (".css", ".xhtml", ".html"):
            text = f.read_text(encoding="utf-8", errors="ignore")
            original = text
            for old_name, new_name in rename_pairs:
                encoded = urllib.parse.quote(old_name)
                for d in ("Fonts", "Images", "Styles", "Text"):
                    text = text.replace(f'"{d}/{old_name}"', f'"{d}/{new_name}"')
                    text = text.replace(f'"{d}/{encoded}"', f'"{d}/{new_name}"')
                    text = text.replace(f"'../{d}/{old_name}'", f"'../{d}/{new_name}'")
                    text = text.replace(f"'../{d}/{encoded}'", f"'../{d}/{new_name}'")
            if text != original:
                f.write_text(text, encoding="utf-8")
                print(f"✓ 引用已更新: {f.relative_to(work)}")
PY

# === 步骤 6：清理 + 重打包 ===
rm -f "$WORK/_rename_map.json"
cd "$WORK"
zip -X0q "$OUT" mimetype
zip -Xrq9DX "$OUT" META-INF OEBPS -x "*.DS_Store" "_rename_map.json"
rm -rf "$WORK"
echo "✅ 还原完成: $OUT"
```

## 验证清单

```bash
# A. 文件名已正常
unzip -l "$OUT" | grep -E "\.xhtml" | head -5

# B. OPF 引用对齐
unzip -p "$OUT" OEBPS/content.opf | grep -E 'href=' | head -5

# C. xhtml 内引用可解析
unzip -p "$OUT" OEBPS/Text/chapter-01.xhtml 2>/dev/null | head -5

# D. epubcheck（推荐）
epubcheck "$OUT"
```

## Pitfalls

- ❌ **不要**用 `sed` 替换文件名 — OPF 是 XML，需保留属性顺序、字符转义
- ❌ **不要**只改磁盘文件不改 OPF — 引用全断
- ❌ **不要**忘记改 CSS 内的 `url()` — 字体/背景图会全失效
- ❌ **不要**覆盖原文件 — 改错了就回不去了
- ❌ **不要**处理真实加密的 EPUB — 本附录不解决 DRM

## 适用范围

- ✅ 多看(Duokan)、掌阅(iReader)、京东读书、书生的加扰 EPUB
- ✅ Sigil 自制但被多看导入加扰的版本
- ❌ Kindle 格式（.azw/.mobi）
- ❌ 真实加密（Adobe Adept / FairPlay / LCP）

## 典型工作流

```
1. filename-restore（本附录）→ 文件名干净
2. inchheart-epub 主线 → 元数据优化
3. inchheart-assets → 入库分类
```

## 相关

- 元数据优化（主线）→ `../SKILL.md`
- 移除 DRM 锁 → `drm-unlock.md`
- 电子书入库分类 → `inchheart-assets`
