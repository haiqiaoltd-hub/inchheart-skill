#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = SKILL_DIR / "references" / "registry.json"


def norm(value):
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def load_registry(path):
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def project_terms(project):
    values = [
        project.get("alias", ""),
        project.get("name", ""),
        project.get("projectPath", ""),
        Path(project.get("projectPath", "")).name,
        Path(project.get("projectPath", "")).parent.name,
    ]
    values.extend(project.get("aliases", []))
    return [v for v in values if v]


def resolve(registry, query):
    target = norm(query)
    exact = []
    partial = []
    for project in registry.get("projects", []):
        terms = project_terms(project)
        normalized = [norm(term) for term in terms]
        if target in normalized:
            exact.append(project)
        elif any(target and target in term for term in normalized):
            partial.append(project)

    matches = exact or partial
    if not matches:
        raise SystemExit(f"No CodeGraph project matched: {query}")
    if len(matches) > 1:
        options = ", ".join(f"{p.get('alias')}={p.get('projectPath')}" for p in matches)
        raise SystemExit(f"Ambiguous CodeGraph project '{query}'. Matches: {options}")
    return matches[0]


def main():
    parser = argparse.ArgumentParser(description="Resolve an InchHeart CodeGraph project alias.")
    parser.add_argument("query", help="Project alias, name, source directory, or path fragment")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY), help="Path to registry.json")
    parser.add_argument("--field", choices=["alias", "name", "projectPath"], help="Print only one field")
    args = parser.parse_args()

    project = resolve(load_registry(args.registry), args.query)
    if args.field:
        print(project[args.field])
    else:
        print(json.dumps(project, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130)
