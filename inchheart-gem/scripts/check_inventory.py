#!/usr/bin/env python3
"""Check inchheart-gem inventory and routing consistency."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


def load_json(path: Path, report: list[str]) -> dict[str, Any]:
    if not path.exists():
        report.append(f"FAIL missing {path}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        report.append(f"FAIL invalid JSON {path}: {exc}")
        return {}


def duplicate_items(items: list[str]) -> list[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return sorted(duplicates)


def rel(root: Path, path: Path) -> str:
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def check_perspectives(root: Path, report: list[str]) -> tuple[int, int, int]:
    perspectives_dir = root / "references" / "perspectives"
    tavern_dir = root / "references" / "tavern"
    routing_path = root / "references" / "routing" / "perspective-routing.json"
    tavern_path = root / "references" / "routing" / "tavern-routing.json"

    flat_cards = sorted(perspectives_dir.glob("*.md"))
    if flat_cards:
        report.append("FAIL flat perspective cards remain: " + ", ".join(rel(root, p) for p in flat_cards))

    perspective_card_paths = sorted(perspectives_dir.glob("*/PERSPECTIVE.md"))
    tavern_card_paths = sorted(tavern_dir.glob("*/PERSPECTIVE.md")) if tavern_dir.exists() else []
    card_paths = perspective_card_paths + tavern_card_paths
    card_ids = sorted(p.parent.name for p in card_paths)

    missing_reference_ids: list[str] = []
    for card_path in card_paths:
        reference_dir = card_path.parent / "references"
        reference_files = sorted(reference_dir.rglob("*.md")) if reference_dir.exists() else []
        if not reference_files:
            missing_reference_ids.append(card_path.parent.name)
    if missing_reference_ids:
        report.append("FAIL perspective directories without Markdown references: " + ", ".join(missing_reference_ids))

    routing = load_json(routing_path, report)
    tavern = load_json(tavern_path, report)
    tavern_ids = {str(item.get("id", "")) for item in tavern.get("members", [])}
    items = [item for group in routing.get("groups", []) for item in group.get("perspectives", [])]
    routing_ids = sorted(str(item.get("id", "")) for item in items)
    declared_count = routing.get("count")

    duplicates = duplicate_items(routing_ids)
    if duplicates:
        report.append("FAIL duplicate perspective routing ids: " + ", ".join(duplicates))
    if declared_count != len(routing_ids):
        report.append(f"FAIL perspective routing count {declared_count} != actual {len(routing_ids)}")

    missing_in_dirs = sorted(set(routing_ids) - set(card_ids))
    missing_in_routing = sorted(set(card_ids) - set(routing_ids))
    if missing_in_dirs:
        report.append("FAIL perspectives missing directories: " + ", ".join(missing_in_dirs))
    if missing_in_routing:
        report.append("FAIL perspective directories missing routing: " + ", ".join(missing_in_routing))

    for item in items:
        item_id = str(item.get("id", ""))
        base_dir = "tavern" if item_id in tavern_ids else "perspectives"
        expected = Path("references") / base_dir / item_id / "PERSPECTIVE.md"
        for key in ("source_path", "card_path"):
            value = str(item.get(key, ""))
            if value != str(expected):
                report.append(f"FAIL {item_id} {key} {value!r} != {str(expected)!r}")
            if value and not (root / value).exists():
                report.append(f"FAIL missing {key} for {item_id}: {value}")

    group_map = {str(group.get("name", "")): group.get("perspectives", []) for group in routing.get("groups", [])}
    tavern_group = group_map.get("闲聊酒馆")
    if tavern_group is None:
        report.append("FAIL missing perspective group: 闲聊酒馆")
    else:
        actual_tavern_ids = {str(item.get("id", "")) for item in tavern_group}
        if actual_tavern_ids != tavern_ids:
            report.append("FAIL tavern perspective ids " f"{sorted(actual_tavern_ids)} != {sorted(tavern_ids)}")
        for item in tavern_group:
            if str(item.get("group", "")) != "闲聊酒馆":
                report.append(f"FAIL tavern item group mismatch: {item.get('id')}")

    tavern_dirs = {p.parent.name for p in tavern_card_paths}
    if tavern_dirs != tavern_ids:
        report.append(f"FAIL tavern directories {sorted(tavern_dirs)} != {sorted(tavern_ids)}")

    leaked_tavern_in_perspectives = sorted(tavern_ids & {p.parent.name for p in perspective_card_paths})
    if leaked_tavern_in_perspectives:
        report.append("FAIL tavern directories still under references/perspectives: " + ", ".join(leaked_tavern_in_perspectives))

    for item in tavern.get("members", []):
        member_id = str(item.get("id", ""))
        path = str(item.get("path", ""))
        expected_path = str(Path("references") / "tavern" / member_id / "PERSPECTIVE.md")
        if path != expected_path:
            report.append(f"FAIL tavern member {member_id} path {path!r} != {expected_path!r}")
        if path and not (root / path).exists():
            report.append(f"FAIL missing tavern member path for {member_id}: {path}")

    return len(card_ids), len(perspective_card_paths), len(tavern_card_paths)


def check_cleanliness(root: Path, report: list[str]) -> None:
    forbidden_dirs = [root / "references" / "professors"]
    for directory in forbidden_dirs:
        if directory.exists():
            report.append(f"FAIL professor resource remains: {rel(root, directory)}")

    pycache = sorted(root.rglob("__pycache__"))
    if pycache:
        report.append("FAIL __pycache__ directories: " + ", ".join(rel(root, p) for p in pycache))

    skill_files = sorted(root.rglob("SKILL.md"))
    expected_skill = root / "SKILL.md"
    if len(skill_files) != 1 or skill_files[0] != expected_skill:
        report.append("FAIL expected only root SKILL.md, found: " + ", ".join(rel(root, p) for p in skill_files))


def main() -> int:
    root = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    report: list[str] = []

    total_count, ordinary_count, tavern_count = check_perspectives(root, report)
    check_cleanliness(root, report)

    if report:
        print("\n".join(report))
        return 1

    print(f"GEM_INVENTORY_OK perspectives={total_count} ordinary={ordinary_count} tavern={tavern_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
