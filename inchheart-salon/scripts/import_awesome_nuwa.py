#!/usr/bin/env python3
"""Import Panmax/awesome-nuwa perspectives into inchheart-salon."""

from __future__ import annotations

import argparse
import concurrent.futures
import json
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any


GITHUB_RE = re.compile(r"\[([^\]]+)\]\(https://github\.com/([^/]+)/([^)]+)\)")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)

CATEGORY_MAP = {
    "中国哲学家": "哲学、理论与宗教",
    "西方哲学家": "哲学、理论与宗教",
    "精神与智慧": "哲学、理论与宗教",
    "当代思想者": "哲学、理论与宗教",
    "科学家": "科学、技术与工程",
    "科技与创新": "AI 与科技创业",
    "商业领袖": "商业、投资与增长",
    "当代中国企业家": "商业、投资与增长",
    "投资大师": "商业、投资与增长",
    "经济学家": "商业、投资与增长",
    "中国文学家": "文学、艺术与电影",
    "西方作家": "文学、艺术与电影",
    "艺术与设计": "文学、艺术与电影",
    "体育": "人物、教育与行动",
    "教育": "人物、教育与行动",
    "心理学家": "心理、生命与陪伴",
    "政治领袖": "政治、战略与历史",
    "军事与战略": "政治、战略与历史",
}

MANUAL_DUPLICATE_BY_REPO = {
    "nietzsche-skill": "nietzsche-perspective",
    "foucault-skill": "foucault-perspective",
    "arendt-skill": "hannah-arendt-perspective",
    "feynman-skill": "feynman-perspective",
    "einstein-skill": "einstein-perspective",
    "darwin-skill": "darwin-perspective",
    "bezos-skill": "jeff-bezos-perspective",
    "zhangyiming-skill": "zhang-yiming-perspective",
    "duanyongping-skill": "duan-yongping-perspective",
    "zhangxiaolong-skill": "zhang-xiaolong-perspective",
    "buffett-skill": "warren-buffett-perspective",
    "munger-skill": "munger-perspective",
    "pggraham-skill": "paul-graham-perspective",
    "steve-jobs-skill": "steve-jobs-perspective",
    "elon-musk-skill": "elon-musk-perspective",
    "altman-skill": "sam-altman-perspective",
    "luxun-skill": "lu-xun-perspective",
    "kafka-skill": "kafka-perspective",
    "borges-skill": "borges-perspective",
    "jung-skill": "carl-jung-perspective",
    "mao-skill": "mao-zedong-perspective",
    "dalailama-skill": "dalai-lama-perspective",
}


@dataclass(frozen=True)
class AwesomeEntry:
    display_name: str
    category: str
    owner: str
    repo: str
    field: str

    @property
    def url(self) -> str:
        return f"https://github.com/{self.owner}/{self.repo}"

    @property
    def cache_dir_name(self) -> str:
        return f"{self.owner}__{self.repo}"


def normalize_name(value: str) -> str:
    return re.sub(r"[\s·・,，.。:：/／()（）《》“”\"'’‘\-–—_]+", "", value).lower()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"-skill$", "", value)
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    if not value:
        return ""
    return f"{value}-perspective"


def parse_awesome_readme(path: Path) -> list[AwesomeEntry]:
    text = path.read_text(encoding="utf-8")
    entries: list[AwesomeEntry] = []
    category = ""
    for line in text.splitlines():
        heading = re.match(r"^##\s+(.+?)\s*$", line)
        if heading and heading.group(1) not in {"安装方式", "目录", "使用方法", "贡献", "致谢"}:
            category = heading.group(1).strip()
            continue
        if not line.startswith("| ["):
            continue
        match = GITHUB_RE.search(line)
        if not match:
            continue
        display_name, owner, repo = match.groups()
        if repo == "nuwa-skill" or not repo.endswith("-skill"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        field = cells[1] if len(cells) > 1 else ""
        entries.append(AwesomeEntry(display_name, category, owner, repo, field))

    deduped: list[AwesomeEntry] = []
    seen: set[tuple[str, str]] = set()
    for entry in entries:
        key = (entry.owner, entry.repo)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(entry)
    return deduped


def run(cmd: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def clone_or_update(entry: AwesomeEntry, cache_root: Path) -> tuple[AwesomeEntry, bool, str]:
    target = cache_root / entry.cache_dir_name
    if (target / ".git").exists():
        result = run(["git", "-C", str(target), "pull", "--ff-only"])
        return entry, result.returncode == 0, result.stderr.strip() or result.stdout.strip()
    result = run(["git", "clone", "--depth=1", entry.url, str(target)])
    return entry, result.returncode == 0, result.stderr.strip() or result.stdout.strip()


def parse_frontmatter_name(skill_text: str, fallback: str) -> tuple[str, str]:
    match = FRONTMATTER_RE.match(skill_text)
    if not match:
        return slugify(fallback), skill_text
    frontmatter = match.group(1)
    body = skill_text[match.end() :]
    name_match = re.search(r"^name:\s*(.+?)\s*$", frontmatter, re.M)
    if not name_match:
        return slugify(fallback), body
    name = name_match.group(1).strip().strip("\"'")
    return name, body


def build_existing_maps(routing_path: Path) -> tuple[dict[str, Any], dict[str, str]]:
    data = json.loads(routing_path.read_text(encoding="utf-8"))
    by_id: dict[str, Any] = {}
    by_name: dict[str, str] = {}
    for group in data.get("groups", []):
        for item in group.get("perspectives", []):
            item_id = item.get("id", "")
            by_id[item_id] = item
            names = [item.get("zh_name", ""), item.get("description", "")]
            names.extend(item.get("positive_triggers", []))
            for name in names:
                normalized = normalize_name(str(name))
                if normalized:
                    by_name[normalized] = item_id
    return by_id, by_name


def find_duplicate(entry: AwesomeEntry, imported_id: str, by_id: dict[str, Any], by_name: dict[str, str]) -> str | None:
    if entry.repo in MANUAL_DUPLICATE_BY_REPO:
        return MANUAL_DUPLICATE_BY_REPO[entry.repo]
    if imported_id in by_id:
        return imported_id
    display_norm = normalize_name(entry.display_name)
    if display_norm in by_name:
        return by_name[display_norm]
    return None


def quality_score(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8", errors="ignore")
    sections = [
        "## 角色扮演规则",
        "## 回答工作流",
        "## 身份卡",
        "## 灵魂内核",
        "## 核心心智模型",
        "## 决策启发式",
        "## 表达DNA",
        "## 诚实边界",
        "## Correction Log",
    ]
    score = sum(10 for section in sections if section in text)
    score += min(len(text) // 1500, 30)
    if "直接以" in text and "身份回应" in text:
        score += 8
    if "不是本人" in text or "不宣称自己就是本人" in text or "视角模拟" in text:
        score += 10
    return score


def convert_skill_to_perspective(entry: AwesomeEntry, imported_id: str, skill_text: str) -> str:
    _, body = parse_frontmatter_name(skill_text, entry.repo)
    body = body.replace("此Skill", "此 perspective")

    description = (
        f"{entry.display_name}的公开思维框架。来源：Panmax/awesome-nuwa 索引中的 {entry.owner}/{entry.repo}；"
        f"领域：{entry.field}。已转换为 InchHeart Support 内部 perspective。"
    )
    frontmatter = f"---\nname: {imported_id}\ndescription: |\n  {description}\n---\n\n"
    boundary = (
        "## InchHeart 沉浸规则\n\n"
        "- 优先保留这个人物最本真的说话方式、判断节奏、偏见、执念和盲区。\n"
        "- 可以直接使用第一人称和“直接以某人物身份回应”的写法；不要把人物磨平成中性助手。\n"
        "- 不需要反复免责声明。只有当用户询问现实事实、专业处置或可能把视角当作现实本人时，才简短澄清来源和现实限制。\n"
        "- 下文若出现“不是本人”“不得冒充”“视角模拟”等句子，只作为资料来源提醒，不削弱沉浸式表达优先级。\n\n"
    )
    if "## Correction Log" not in body:
        body = body.rstrip() + "\n\n## Correction Log\n\n- 2026-06-08：从 Panmax/awesome-nuwa 外部 Nuwa skill 转换导入。\n"
    return frontmatter + boundary + body.lstrip()


def copy_duplicate_reference(root: Path, cache_dir: Path, entry: AwesomeEntry, target_id: str, external_score: int, local_score: int) -> None:
    target = root / "references" / "perspectives" / target_id / "references"
    target.mkdir(parents=True, exist_ok=True)
    skill_path = cache_dir / "SKILL.md"
    research_path = cache_dir / "references" / "research.md"
    if skill_path.exists():
        text = skill_path.read_text(encoding="utf-8", errors="ignore")
        header = (
            f"# Awesome Nuwa 外部版本：{entry.display_name}\n\n"
            f"- 来源仓库：{entry.url}\n"
            f"- 外部领域：{entry.field}\n"
            f"- 外部质量分：{external_score}\n"
            f"- 本地主卡质量分：{local_score}\n"
            f"- 处理决策：保留本地 `PERSPECTIVE.md` 作为主卡；本文件仅作为参考材料。\n\n"
            "## 外部 SKILL 原文\n\n"
        )
        (target / "awesome-nuwa.md").write_text(header + text, encoding="utf-8")
    if research_path.exists():
        text = research_path.read_text(encoding="utf-8", errors="ignore")
        header = (
            f"# Awesome Nuwa 外部调研：{entry.display_name}\n\n"
            f"- 来源仓库：{entry.url}\n"
            "- 用途：作为本地人物 perspective 的补充研究材料，不替代主卡。\n\n"
        )
        (target / "awesome-nuwa-research.md").write_text(header + text, encoding="utf-8")


def update_routing(root: Path, new_items: list[dict[str, Any]]) -> None:
    routing_path = root / "references" / "routing" / "perspective-routing.json"
    data = json.loads(routing_path.read_text(encoding="utf-8"))
    groups = {group.get("name"): group for group in data.get("groups", [])}
    existing_ids = {
        item.get("id")
        for group in data.get("groups", [])
        for item in group.get("perspectives", [])
    }
    for item in new_items:
        if item["id"] in existing_ids:
            continue
        group_name = item["group"]
        group = groups.get(group_name)
        if group is None:
            group = {"name": group_name, "perspectives": []}
            data.setdefault("groups", []).append(group)
            groups[group_name] = group
        group["perspectives"].append(item)
        existing_ids.add(item["id"])
    data["count"] = sum(len(group.get("perspectives", [])) for group in data.get("groups", []))
    routing_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_index(root: Path, imported: list[dict[str, Any]], duplicates: list[dict[str, Any]]) -> None:
    index_path = root / "references" / "routing" / "perspective-index.md"
    routing_path = root / "references" / "routing" / "perspective-routing.json"
    data = json.loads(routing_path.read_text(encoding="utf-8"))
    lines = [
        "# Perspective Index",
        "",
        f"这是 `inchheart-salon` 的人物视角索引。当前共 {data['count']} 个 perspective（视角）。",
        "",
        "## 使用规则",
        "",
        "- 默认从 `inchheart-salon` 主入口路由。",
        "- 只有用户点名人物/主题，或需求明显匹配某个思维框架时，才读取对应卡片。",
        "- 普通人物读取路径：`references/perspectives/<id>/PERSPECTIVE.md`。",
        "- 酒馆人物读取路径：`references/tavern/<id>/PERSPECTIVE.md`。",
        "- 点名人物时，读取该人物目录下 `references/**/*.md` 的全部 Markdown 研究材料；不读取脚本、缓存、图片或非 Markdown 文件。",
        "- 触发“闲聊酒馆”时，先读 `tavern-routing.md/json`，只从酒馆成员中随机 1 位主聊人物。",
        "- 人物视角优先沉浸；只在现实事实、专业处置或身份混淆时简短澄清来源。",
        "",
    ]
    for group in data.get("groups", []):
        lines.append(f"## {group.get('name')}")
        lines.append("")
        lines.append("| 中文/英文名 | Perspective | 何时调用 |")
        lines.append("|---|---|---|")
        for item in group.get("perspectives", []):
            description = str(item.get("description", "")).replace("\n", " ").strip()
            if len(description) > 110:
                description = description[:107] + "..."
            lines.append(f"| {item.get('zh_name', '')} | `{item.get('id', '')}` | {description} |")
        lines.append("")
    if imported or duplicates:
        lines.append("## Awesome Nuwa 导入记录")
        lines.append("")
        lines.append(f"- 新增人物：{len(imported)}。")
        lines.append(f"- 重叠人物：{len(duplicates)}，保留本地主卡，外部版本写入对应人物 `references/`。")
        lines.append("- 导入来源：`Panmax/awesome-nuwa` 及其索引仓库。")
        lines.append("")
    index_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--awesome", default="/Users/mac/Repository/Sources/no-update/awesome-nuwa")
    parser.add_argument("--cache", default="/Users/mac/Repository/Sources/no-update/awesome-nuwa-skills")
    parser.add_argument("--jobs", type=int, default=16)
    args = parser.parse_args()

    root = Path(args.root).expanduser()
    awesome = Path(args.awesome).expanduser()
    cache = Path(args.cache).expanduser()
    cache.mkdir(parents=True, exist_ok=True)

    entries = parse_awesome_readme(awesome / "README.md")
    print(f"entries={len(entries)}")

    failures: list[tuple[str, str]] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(clone_or_update, entry, cache) for entry in entries]
        for future in concurrent.futures.as_completed(futures):
            entry, ok, message = future.result()
            if not ok:
                failures.append((entry.repo, message))
    if failures:
        for repo, message in failures:
            print(f"CLONE_FAIL {repo}: {message}")

    by_id, by_name = build_existing_maps(root / "references" / "routing" / "perspective-routing.json")
    new_items: list[dict[str, Any]] = []
    imported: list[dict[str, Any]] = []
    duplicates: list[dict[str, Any]] = []
    skipped: list[str] = []

    for entry in entries:
        cache_dir = cache / entry.cache_dir_name
        skill_path = cache_dir / "SKILL.md"
        if not skill_path.exists():
            skipped.append(entry.repo)
            continue
        skill_text = skill_path.read_text(encoding="utf-8", errors="ignore")
        imported_id, _ = parse_frontmatter_name(skill_text, entry.repo)
        if not imported_id.endswith("-perspective") or imported_id == "-perspective":
            imported_id = slugify(imported_id) or slugify(entry.repo)
        if not imported_id or imported_id == "-perspective":
            skipped.append(entry.repo)
            continue
        duplicate_id = find_duplicate(entry, imported_id, by_id, by_name)
        external_score = quality_score(skill_path)

        if duplicate_id:
            local_path = root / "references" / "perspectives" / duplicate_id / "PERSPECTIVE.md"
            local_score = quality_score(local_path)
            copy_duplicate_reference(root, cache_dir, entry, duplicate_id, external_score, local_score)
            duplicates.append(
                {
                    "display_name": entry.display_name,
                    "repo": entry.repo,
                    "target_id": duplicate_id,
                    "external_score": external_score,
                    "local_score": local_score,
                }
            )
            continue

        target_dir = root / "references" / "perspectives" / imported_id
        target_dir.mkdir(parents=True, exist_ok=True)
        (target_dir / "PERSPECTIVE.md").write_text(convert_skill_to_perspective(entry, imported_id, skill_text), encoding="utf-8")
        refs_dir = target_dir / "references"
        refs_dir.mkdir(parents=True, exist_ok=True)
        research_path = cache_dir / "references" / "research.md"
        if research_path.exists():
            shutil.copy2(research_path, refs_dir / "awesome-nuwa-research.md")
        else:
            (refs_dir / "awesome-nuwa-research.md").write_text(
                f"# Awesome Nuwa 调研材料\n\n- 来源仓库：{entry.url}\n- 状态：该仓库没有 `references/research.md`。\n",
                encoding="utf-8",
            )
        group = CATEGORY_MAP.get(entry.category, "Awesome Nuwa 导入")
        description = (
            f"{entry.display_name}的公开思维框架。外部领域：{entry.field}。"
            f"从 Panmax/awesome-nuwa 的 {entry.owner}/{entry.repo} 转换导入。"
        )
        item = {
            "id": imported_id,
            "zh_name": entry.display_name,
            "group": group,
            "source_path": f"references/perspectives/{imported_id}/PERSPECTIVE.md",
            "card_path": f"references/perspectives/{imported_id}/PERSPECTIVE.md",
            "positive_triggers": [entry.display_name, imported_id.replace("-perspective", ""), entry.field],
            "negative_triggers": ["用户明确拒绝该人物视角", "任务只需要客观工具执行且不需要人物判断", "现实高风险处置需要专业路径"],
            "description": description,
        }
        if imported_id not in {row["id"] for row in imported}:
            new_items.append(item)
            imported.append({"display_name": entry.display_name, "repo": entry.repo, "id": imported_id, "group": group})
        else:
            skipped.append(f"duplicate-import-id:{entry.repo}:{imported_id}")

    update_routing(root, new_items)
    update_index(root, imported, duplicates)

    report = {
        "entries": len(entries),
        "imported": len(imported),
        "duplicates": len(duplicates),
        "skipped": skipped,
        "clone_failures": failures,
        "duplicate_items": duplicates,
        "imported_items": imported,
    }
    report_path = root / "references" / "routing" / "awesome-nuwa-import-report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"imported={len(imported)} duplicates={len(duplicates)} skipped={len(skipped)} failures={len(failures)}")
    print(f"report={report_path}")
    return 0 if not failures else 1


if __name__ == "__main__":
    raise SystemExit(main())
