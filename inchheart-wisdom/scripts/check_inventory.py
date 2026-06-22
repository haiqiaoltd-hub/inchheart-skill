#!/usr/bin/env python3
"""Check inchheart-wisdom inventory and routing consistency."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ANALYSIS_ROOT = Path("/Users/mac/Repository/Projects/InchHeart Skill/inchheart-analysis")

EXPECTED_IDS = [
    "postmodern-philosophy-professor",
    "literature-professor",
    "music-professor",
    "film-professor",
    "psychology-professor",
    "art-professor",
    "economics-professor",
    "law-professor",
    "sociology-professor",
    "kinesiology-professor",
    "physics-professor",
    "modern-computing-professor",
    "political-science-professor",
    "medicine-professor",
    "biology-professor",
]


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def load_json(path: Path, report: list[str]) -> dict[str, Any]:
    if not path.exists():
        report.append(f"FAIL missing {rel(path.parents[3], path)}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.append(f"FAIL invalid JSON {path}: {exc}")
        return {}


def duplicates(items: list[str]) -> list[str]:
    seen: set[str] = set()
    dupes: set[str] = set()
    for item in items:
        if item in seen:
            dupes.add(item)
        seen.add(item)
    return sorted(dupes)


def check_current_professors(root: Path, report: list[str]) -> int:
    professors_dir = root / "references" / "professors"
    routing_path = root / "references" / "routing" / "professor-routing.json"
    routing = load_json(routing_path, report)

    card_paths = sorted(professors_dir.glob("*/PROFESSOR.md"))
    dir_ids = sorted(path.parent.name for path in card_paths)
    routing_items = routing.get("core_professors", [])
    routing_ids = [str(item.get("id", "")) for item in routing_items]

    if sorted(EXPECTED_IDS) != dir_ids:
        report.append(f"FAIL current professor dirs {dir_ids} != expected {sorted(EXPECTED_IDS)}")
    if sorted(EXPECTED_IDS) != sorted(routing_ids):
        report.append(f"FAIL routing professor ids {sorted(routing_ids)} != expected {sorted(EXPECTED_IDS)}")

    dupes = duplicates(routing_ids)
    if dupes:
        report.append("FAIL duplicate routing ids: " + ", ".join(dupes))

    if routing.get("core_professor_count") != len(EXPECTED_IDS):
        report.append(
            f"FAIL core_professor_count {routing.get('core_professor_count')} != {len(EXPECTED_IDS)}"
        )

    for item in routing_items:
        professor_id = str(item.get("id", ""))
        path = str(item.get("path", ""))
        expected_path = str(Path("references") / "professors" / professor_id / "PROFESSOR.md")
        if path != expected_path:
            report.append(f"FAIL {professor_id} path {path!r} != {expected_path!r}")
        if path and not (root / path).exists():
            report.append(f"FAIL missing professor path for {professor_id}: {path}")

    nested_references = sorted(professors_dir.glob("*/references/**/*.md"))
    if nested_references:
        report.append(
            "FAIL current professors must not carry nested references: "
            + ", ".join(rel(root, path) for path in nested_references)
        )

    return len(card_paths)


def check_boundaries(root: Path, report: list[str]) -> None:
    forbidden_dirs = [
        root / "references" / "legacy",
        root / "references" / "perspectives",
        root / "references" / "tavern",
        root / "prompts",
    ]
    for path in forbidden_dirs:
        if path.exists():
            report.append(f"FAIL non-professor resource remains: {rel(root, path)}")

    pycache = sorted(root.rglob("__pycache__"))
    if pycache:
        report.append("FAIL __pycache__ directories: " + ", ".join(rel(root, path) for path in pycache))

    skill_files = sorted(root.rglob("SKILL.md"))
    expected_skill = root / "SKILL.md"
    if len(skill_files) != 1 or skill_files[0] != expected_skill:
        report.append("FAIL expected only root SKILL.md, found: " + ", ".join(rel(root, path) for path in skill_files))


def check_methods(root: Path, report: list[str]) -> None:
    expected_resources = [
        (
            "references/methods/audit-response-protocol.md",
            ANALYSIS_ROOT / "SKILL.md",
        ),
        (
            "references/methods/dimensional-audit.md",
            ANALYSIS_ROOT / "references" / "audit-model.md",
        ),
    ]
    for expected_path, source_path in expected_resources:
        method_path = root / expected_path
        if not method_path.exists():
            report.append(f"FAIL missing method resource: {rel(root, method_path)}")
        if not source_path.exists():
            report.append(f"FAIL missing analysis source: {source_path}")
        if method_path.exists() and source_path.exists():
            if method_path.read_bytes() != source_path.read_bytes():
                report.append(
                    f"FAIL method mirror drift: {rel(root, method_path)} != {source_path}"
                )

    routing = load_json(root / "references" / "routing" / "professor-routing.json", report)
    method_resources = routing.get("method_resources", [])
    paths = [str(item.get("path", "")) for item in method_resources]
    source_paths = [str(item.get("source_path", "")) for item in method_resources]
    for expected_path, source_path in expected_resources:
        if expected_path not in paths:
            report.append(f"FAIL routing missing method resource: {expected_path}")
        if str(source_path) not in source_paths:
            report.append(f"FAIL routing missing method source: {source_path}")


def main() -> int:
    root = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    report: list[str] = []

    current_count = check_current_professors(root, report)
    check_boundaries(root, report)
    check_methods(root, report)

    if report:
        print("\n".join(report))
        return 1

    print(f"PROFESSOR_INVENTORY_OK current_professors={current_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
