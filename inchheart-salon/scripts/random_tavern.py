#!/usr/bin/env python3
"""Pick one InchHeart Tavern member and print its read paths."""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Randomly choose one Tavern perspective.")
    parser.add_argument(
        "root",
        nargs="?",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Skill root. Defaults to this script's parent skill directory.",
    )
    parser.add_argument("--seed", type=str, help="Optional deterministic seed for tests.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    routing_path = root / "references" / "routing" / "tavern-routing.json"
    routing: dict[str, Any] = json.loads(routing_path.read_text(encoding="utf-8"))
    members = routing.get("members", [])
    if not members:
        raise SystemExit(f"No Tavern members in {routing_path}")

    rng = random.Random(args.seed) if args.seed is not None else random.SystemRandom()
    member = rng.choice(members)
    output = {
        "id": member["id"],
        "zh_name": member["zh_name"],
        "card_path": member["path"],
        "references_glob": member["references_glob"],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
