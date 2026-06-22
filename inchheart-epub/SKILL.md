---
name: inchheart-epub
description: EPUB 元数据优化 — 清理多看/掌阅残留脏数据、补全缺失字段、修正 OPF 结构、按元数据重命名文件、生成 Calibre 兼容 metadata.opf
tags: [epub, ebook, metadata, calibre, duokan, ireader, optimization]
---

# EPUB 元数据优化

EPUB 文件的"清理 + 标准化"工具集。**主线**是把杂乱的 OPF 元数据（多看/掌阅残留、缺失字段、结构错误）整理成规范、可被 Calibre/Apple Books/微信读书等任意阅读器正确识别的标准 EPUB。

## 主线 / 次要 / 附录

| 用途 | 章节 | 何时调用 |
|---|---|---|
| **元数据优化**（主线） | 见本文 | EPUB 元数据脏/缺失/不一致，想标准化 |
| 还原混淆文件名 | `references/filename-restore.md` | 文件名被加扰成怪字符 |
| 移除声明性 DRM 锁 | `references/drm-unlock.md` | EPUB 锁了，无法在常规阅读器打开 |

## 适用场景

- 用户从多看/掌阅/京东读书导入 EPUB，OPF 内是 `duokan-book-id` 等脏 identifier
- 书名/作者/出版社/ISBN 等字段缺失或错误
- Calibre 识别不出书名（导入后显示 "Unknown"）
- 文件名是 `【F-032】哲学的历程_v1_0.epub` 这种下载站命名
- 想统一书库命名规范
- 多个 EPUB 想批量标准化

## 不适用场景

- **真实加密**（Adobe Adept / Apple FairPlay / Readium LCP）— 字节不可读
- **PDF/EPUB 转换**（pdf→epub）— 不是元数据问题
- **DRM 锁移除** — 见 `references/drm-unlock.md`
- **内容修改**（加批注/换字体/合并章节）— 是另一个 skill 的事

---

## 工作流概览

```
1. 解包
2. 解析 OPF → 提取元数据（用 ElementTree）
3. 清理脏数据（多看/掌阅残留）
4. 补全/修正元数据（缺什么补什么）
5. 修正 OPF 结构（spine / manifest / cover）
6. 清理 toc.ncx（移除死链、规范 ID）
7. 按元数据重命名文件
8. 写 Calibre 兼容 metadata.opf
9. 重打包
```

---

## 8 步流程

**永远不覆盖原文件**，输出 `<新书名>_<作者>.epub` 或保留 `<原名>_optimized.epub`（用户选）。

```bash
SRC="<path>/<name>.epub"
DIR="$(dirname "$SRC")"
WORK="$(mktemp -d)"

# === 步骤 1：解包 ===
unzip -q "$SRC" -d "$WORK"
ls "$WORK/OEBPS/"  # 快速检查结构
```

```bash
# === 步骤 2：解析 OPF → 提取元数据 ===
python3 - <<PY
import json, pathlib
from xml.etree import ElementTree as ET

work = pathlib.Path("$WORK")
opf = work / "OEBPS" / "content.opf"
ns = {
    "opf": "http://www.idpf.org/2007/opf",
    "dc":  "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
}

tree = ET.parse(opf)
root = tree.getroot()
metadata = root.find("opf:metadata", ns)

# 提取常见字段
fields = {}
for tag in ("title", "creator", "language", "publisher",
            "date", "identifier", "description", "subject", "rights", "coverage"):
    el = metadata.find(f"dc:{tag}", ns)
    if el is not None:
        fields[tag] = {"text": el.text, "id": el.get("id"), "opf_attrs": dict(el.attrib)}

# meta 标签（EPUB 3 refined）
fields["meta"] = []
for m in metadata.findall("opf:meta", ns):
    fields["meta"].append(dict(m.attrib) | {"text": m.text})

pathlib.Path("$WORK/_metadata.json").write_text(
    json.dumps(fields, ensure_ascii=False, indent=2)
)
print(json.dumps(fields, ensure_ascii=False, indent=2))
PY
```

读 `_metadata.json` 后，识别脏数据并准备修复方案。常见脏数据见末尾字典。

```bash
# === 步骤 3：清理脏元数据 ===
python3 - <<PY
import json, pathlib
from xml.etree import ElementTree as ET

work = pathlib.Path("$WORK")
fields = json.loads((work / "_metadata.json").read_text())
opf = work / "OEBPS" / "content.opf"
ns = {
    "opf": "http://www.idpf.org/2007/opf",
    "dc":  "http://purl.org/dc/elements/1.1/",
}
tree = ET.parse(opf)
root = tree.getroot()
metadata = root.find("opf:metadata", ns)

# 3a. 移除多看/掌阅/京东/书生的脏 identifier
DIRTY_KEYS = ("duokan", "ireader", "jdreader", "sursen", "tx-reader")
to_remove = []
for ident in metadata.findall("dc:identifier", ns):
    ident_id = (ident.get("id") or "").lower()
    ident_text = (ident.text or "").lower()
    if any(k in ident_id for k in DIRTY_KEYS) or \
       any(k in ident_text for k in DIRTY_KEYS):
        to_remove.append(ident)
for el in to_remove:
    metadata.remove(el)
    print(f"✗ 移除脏 identifier: id={el.get('id')} text={el.text}")

# 3b. 移除 <meta name="..."> 中的脏属性
DIRTY_META_NAMES = ("duokan-book-id", "ireader-book-id", "cover")
to_remove = []
for m in metadata.findall("opf:meta", ns):
    name = (m.get("name") or "").lower()
    if any(k in name for k in DIRTY_KEYS):
        to_remove.append(m)
for el in to_remove:
    metadata.remove(el)
    print(f"✗ 移除脏 meta: name={el.get('name')}")

# 3c. 修正编码（多看有时把字段写成 URL 编码）
import urllib.parse
for el in metadata.iter():
    if el.text and "%" in el.text and el.text.count("%") >= 2:
        try:
            decoded = urllib.parse.unquote(el.text)
            if decoded != el.text:
                print(f"~ 解码: {el.text!r} → {decoded!r}")
                el.text = decoded
        except Exception:
            pass

tree.write(opf, encoding="utf-8", xml_declaration=True)
print("✓ OPF 脏数据已清理")
PY
```

```bash
# === 步骤 4：补全 / 修正元数据（用户确认后手动改） ===
python3 - <<'PY'
"""
在这里编辑 fields 字典：
- 缺失的字段补全
- 错误的字段修正（如作者名写错、ISBN 多一位）
- 标准化的字段（如日期统一为 YYYY-MM-DD）
然后写回 OPF。
"""
import json, pathlib
from xml.etree import ElementTree as ET

work = pathlib.Path("$WORK")
fields = json.loads((work / "_metadata.json").read_text())
opf = work / "OEBPS" / "content.opf"
ns = {
    "opf": "http://www.idpf.org/2007/opf",
    "dc":  "http://purl.org/dc/elements/1.1/",
}
tree = ET.parse(opf)
root = tree.getroot()
metadata = root.find("opf:metadata", ns)

# ==== 在这里填入正确的元数据 ====
CORRECTED = {
    "title":       "",   # 例如 "哲学的历程：西方哲学历史导论（第4版）"
    "creator":     "",   # 例如 "威廉·魏施德"
    "language":    "zh", # ISO 639-1
    "publisher":   "",   # 例如 "中国轻工业出版社"
    "date":        "",   # YYYY-MM-DD
    "identifier":  "",   # ISBN-13: 978-7-5019-XXXX-X
    "description": "",
    "subject":     [],   # ["哲学", "西方哲学", "导论"]
    "rights":      "",
}
# ==== 修正结束 ====

# 删旧 → 写新
for tag, value in CORRECTED.items():
    for el in metadata.findall(f"dc:{tag}", ns):
        metadata.remove(el)
    if not value:
        continue
    if isinstance(value, list):
        for v in value:
            el = ET.SubElement(metadata, f"{{http://purl.org/dc/elements/1.1/}}{tag}")
            el.text = v
    else:
        el = ET.SubElement(metadata, f"{{http://purl.org/dc/elements/1.1/}}{tag}")
        el.text = value
        # identifier 需要 id 属性
        if tag == "identifier":
            el.set("id", "BookId")

tree.write(opf, encoding="utf-8", xml_declaration=True)
print("✓ 元数据已补全/修正")
PY
```

```bash
# === 步骤 5：修正 OPF 结构（spine / manifest / cover） ===
python3 - <<PY
import pathlib
from xml.etree import ElementTree as ET

work = pathlib.Path("$WORK")
opf = work / "OEBPS" / "content.opf"
ns = {"opf": "http://www.idpf.org/2007/opf"}
tree = ET.parse(opf)
root = tree.getroot()

# 5a. 清理 manifest 中的死链
manifest = root.find("opf:manifest", ns)
spine    = root.find("opf:spine", ns)
spine_ids = {ir.get("idref") for ir in spine.findall("opf:itemref", ns)} if spine is not None else set()

to_remove = []
for item in manifest.findall("opf:item", ns):
    item_id = item.get("id")
    href = item.get("href")
    fp = work / "OEBPS" / href
    if not fp.exists():
        print(f"✗ manifest 死链: id={item_id} href={href}")
        to_remove.append(item)
    elif item_id not in spine_ids and item.get("media-type") != "application/x-dtbncx+xml":
        # manifest 有但 spine 没用上 → 可能是垃圾资源
        print(f"? manifest 未引用: id={item_id} href={href}")
        # 保守策略：保留，由用户决定
for el in to_remove:
    manifest.remove(el)

# 5b. 修正 cover 标识（epub 2 用 <meta name="cover" content="...">，epub 3 用 <meta property="cover-image">）
cover_id = None
for item in manifest.findall("opf:item", ns):
    if (item.get("properties") or "").lower() == "cover-image":
        cover_id = item.get("id")
        break

metadata = root.find("opf:metadata", ns)
# 移除旧的 cover meta
for m in metadata.findall("opf:meta", ns):
    if (m.get("name") or "").lower() == "cover":
        metadata.remove(m)

if cover_id:
    # EPUB 2 兼容
    m = ET.SubElement(metadata, "{http://www.idpf.org/2007/opf}meta")
    m.set("name", "cover")
    m.set("content", cover_id)
    print(f"✓ 设置 cover → {cover_id}")

tree.write(opf, encoding="utf-8", xml_declaration=True)
print("✓ OPF 结构已修正")
PY
```

```bash
# === 步骤 6：清理 toc.ncx ===
python3 - <<PY
import pathlib
from xml.etree import ElementTree as ET

work = pathlib.Path("$WORK")
ncx_path = work / "OEBPS" / "toc.ncx"
if not ncx_path.exists():
    print("(无 toc.ncx，跳过)")
else:
    ns = {"ncx": "http://www.daisy.org/z3986/2005/ncx/"}
    tree = ET.parse(ncx_path)
    root = tree.getroot()

    # 移除 navPoint 指向不存在的 xhtml 的死链
    to_remove = []
    for np in root.iter("{http://www.daisy.org/z3986/2005/ncx/}navPoint"):
        content = np.find("ncx:content", ns)
        if content is not None:
            src = content.get("src", "").split("#")[0]
            if src and not (work / "OEBPS" / src).exists():
                print(f"✗ navPoint 死链: {src}")
                to_remove.append(np)
    for el in to_remove:
        # 找到父节点移除（ET 的 remove 不会自动处理嵌套）
        for parent in root.iter():
            for child in list(parent):
                if child is el:
                    parent.remove(child)
    tree.write(ncx_path, encoding="utf-8", xml_declaration=True)
    print("✓ toc.ncx 已清理")
PY
```

```bash
# === 步骤 7：按元数据重命名文件 ===
python3 - <<PY
"""
重命名策略（用户可选）：
A. 用书名+作者：<书名>_<作者>.epub
B. 用 ISBN：<ISBN>.epub
C. 保留原名 + _optimized 后缀
"""
import json, pathlib, shutil, re
work = pathlib.Path("$WORK")
fields = json.loads((work / "_metadata.json").read_text())

SRC = "$SRC"
DIR = "$DIR"
WORK_DIR = pathlib.Path(SRC).parent

# ==== 选择重命名策略 ====
STRATEGY = "A"  # A / B / C

title = fields.get("title", {}).get("text", "").strip()
creator = fields.get("creator", {}).get("text", "").strip()

def safe(s):
    """清理文件名非法字符"""
    return re.sub(r'[\\/:*?"<>|]', "", s).strip()

if STRATEGY == "A" and title and creator:
    new_name = f"{safe(title)}_{safe(creator)}.epub"
elif STRATEGY == "B":
    isbn = fields.get("identifier", {}).get("text", "").strip()
    new_name = f"{safe(isbn)}.epub" if isbn else None
else:
    base = pathlib.Path(SRC).stem
    new_name = f"{base}_optimized.epub"

print(f"建议新文件名: {new_name}")
# 用户确认后再执行 mv
PY
```

```bash
# === 步骤 8：写 Calibre 兼容 metadata.opf ===
python3 - <<PY
"""
Calibre 读取 EPUB 时，会合并 OPF metadata + 它自己的 metadata.db。
为了 Calibre 友好：
- dc:identifier id="BookId"  → ISBN 或 UUID
- dc:title 必填
- dc:creator 必填
- dc:language 必填
- 添加 <meta property="dcterms:modified"> 时间戳
- 添加 <meta name="calibre:series">（如果有丛书）
"""
import pathlib
from xml.etree import ElementTree as ET
import datetime

work = pathlib.Path("$WORK")
opf = work / "OEBPS" / "content.opf"
ns = {"opf": "http://www.idpf.org/2007/opf", "dc": "http://purl.org/dc/elements/1.1/"}
tree = ET.parse(opf)
root = tree.getroot()
metadata = root.find("opf:metadata", ns)

# 添加 dcterms:modified（Calibre 用来检测更新）
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
for m in metadata.findall("opf:meta", ns):
    if m.get("property") == "dcterms:modified":
        metadata.remove(m)
m = ET.SubElement(metadata, "{http://www.idpf.org/2007/opf}meta")
m.set("property", "dcterms:modified")
m.text = now

tree.write(opf, encoding="utf-8", xml_declaration=True)
print("✓ Calibre 兼容字段已添加")
PY
```

```bash
# === 步骤 9：重打包 ===
NEW_NAME="<按步骤 7 确认的名字>"
OUT="${DIR}/${NEW_NAME}"

cd "$WORK"
zip -X0q "$OUT" mimetype
zip -Xrq9DX "$OUT" META-INF OEBPS -x "*.DS_Store" "_metadata.json"
rm -rf "$WORK"
echo "✅ 优化完成: $OUT"
```

---

## 验证清单

```bash
# A. 元数据可读
unzip -p "$OUT" OEBPS/content.opf | python3 -c "
import sys
from xml.etree import ElementTree as ET
ns = {'opf': 'http://www.idpf.org/2007/opf', 'dc': 'http://purl.org/dc/elements/1.1/'}
root = ET.fromstring(sys.stdin.read())
m = root.find('opf:metadata', ns)
for tag in ('title', 'creator', 'language', 'publisher', 'date', 'identifier'):
    el = m.find(f'dc:{tag}', ns)
    print(f'{tag}: {el.text if el is not None else \"(缺失)\"}')
"

# B. 无脏数据
unzip -p "$OUT" OEBPS/content.opf | grep -iE "(duokan|ireader|jdreader|sursen)" || echo "OK: 无国产 DRM 残留"

# C. 用 epubcheck 验证
epubcheck "$OUT"  # brew install epubcheck

# D. Calibre 导入测试
calibredb add "$OUT" --library-path /tmp/test-library
```

## 常见脏元数据字典

| 字段 | 脏数据示例 | 原因 | 处理 |
|---|---|---|---|
| `<dc:identifier id="duokan-book-id">` | `duokan-book-id-12345` | 多看导入 | 移除整个元素 |
| `<meta name="cover" content="...">` | 指向不存在的 jpg | 多看残留 | 修正或移除 |
| `<dc:title>` URL 编码 | `%E5%93%B2%E5%AD%A6...` | 多看写入错误 | URL 解码 |
| `<dc:creator>` 空 | `<dc:creator/>` | 缺失 | 补全 |
| `<dc:date>` 格式混乱 | `2009.06` / `2009/6` | 来源不一 | 标准化为 `YYYY-MM-DD` |
| `<dc:language>` 错误 | `cn` / `chi` | 不规范 | 改为 `zh` |
| `<dc:identifier>` 不是 ISBN | UUID / 内部 ID | 缺失 ISBN | 补 ISBN-13 |

## Pitfalls

- ❌ **不要**直接编辑原始 OPF 字符串 — 用 ElementTree，避免破坏 XML 结构
- ❌ **不要**丢失 `xml:lang` 属性（多语言 EPUB 需要）
- ❌ **不要**把 `<dc:identifier>` 改成 `id="uuid"` — Calibre 会去重
- ❌ **不要**把 `<dc:date>` 写成 `<dc:date opf:event="original-publication">2009</dc:date>` 后又改文本 — event 标签和文本必须一致
- ❌ **不要**忽略 `<meta property="belongs-to-collection">` — 影响丛书显示
- ❌ **不要**在优化前没备份 — 步骤多，错误可能累积

## 汇报模板

1. **原状**：识别出哪些脏数据、哪些缺失字段
2. **修复**：补全/修正了哪些字段
3. **结构调整**：spine/manifest 死链数、cover 设置状态
4. **重命名**：采用策略 A/B/C、新文件名
5. **验证**：epubcheck + Calibre 导入测试结果
6. **位置**：输出文件完整路径

## 相关附录

- 还原混淆文件名 → `references/filename-restore.md`
- 移除声明性 DRM 锁 → `references/drm-unlock.md`
- 电子书入库分类 → `inchheart-assets`
