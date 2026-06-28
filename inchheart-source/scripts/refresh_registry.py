#!/usr/bin/env python3
import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = SKILL_DIR / "references" / "registry.json"


def load_registry(path):
    path = Path(path)
    if not path.exists():
        return {"schemaVersion": 1, "scanRoots": ["/Users/mac/Repository/Sources"], "projects": []}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def find_project_roots(scan_roots):
    roots = []
    for scan_root in scan_roots:
        base = Path(scan_root).expanduser()
        if not base.exists():
            continue
        for codegraph_dir in sorted(base.rglob(".codegraph")):
            db = codegraph_dir / "codegraph.db"
            if db.exists():
                project_path = codegraph_dir.parent
                # Only index under tracked source directories
                rel = str(project_path)
                tracked_prefixes = ("/agent-cli/", "/agent-gateway/", "/no-update/", "/plugin/")
                if not any(prefix in rel for prefix in tracked_prefixes):
                    continue
                roots.append(project_path)
    return roots


def status_for(path):
    result = subprocess.run(
        ["codegraph", "status", "--json", str(path)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode != 0:
        return {}
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError:
        return {}


def inferred_alias(path):
    parent = path.parent.name
    if parent.endswith("-source"):
        parent = parent[:-7]
    if parent.endswith("-cli"):
        return parent
    return parent


def merge_project(existing_by_path, path):
    current = existing_by_path.get(str(path), {})
    info = status_for(path)
    return {
        "alias": current.get("alias") or inferred_alias(path),
        "name": current.get("name") or Path(path).name,
        "aliases": current.get("aliases", []),
        "projectPath": str(path),
        "initialized": info.get("initialized", current.get("initialized")),
        "files": info.get("fileCount", current.get("files")),
        "nodes": info.get("nodeCount", current.get("nodes")),
        "dbSizeBytes": info.get("dbSizeBytes", current.get("dbSizeBytes")),
        "pendingChanges": info.get("pendingChanges", current.get("pendingChanges")),
        "worktreeMismatch": info.get("worktreeMismatch", current.get("worktreeMismatch")),
    }


def refresh(registry):
    existing_by_path = {project["projectPath"]: project for project in registry.get("projects", [])}
    scan_roots = registry.get("scanRoots") or ["/Users/mac/Repository/Sources"]
    projects = [merge_project(existing_by_path, path) for path in find_project_roots(scan_roots)]
    projects.sort(key=lambda item: item["alias"])
    return {
        "schemaVersion": registry.get("schemaVersion", 1),
        "lastVerified": datetime.now().astimezone().isoformat(timespec="seconds"),
        "scanRoots": scan_roots,
        "projects": projects,
    }


def regenerate_source_repos_md(registry, registry_path):
    """Regenerate source-repos.md from registry.json to keep them in sync."""
    md_path = registry_path.parent / "source-repos.md"
    projects = registry.get("projects", [])
    last_verified = registry.get("lastVerified", "unknown")

    lines = [
        "# Sources CodeGraph Indexes",
        "",
        f"Last verified: {last_verified}.",
        "",
        "Use the directory shown in `projectPath` as the CodeGraph MCP `projectPath`. The parent collection directory is usually not initialized; the concrete extracted repository directory is initialized.",
        "",
        "Release versions and commit hashes embedded in directory names change with every update — **do not hard-code them here**. The `projectPath` column comes from `registry.json` (auto-refreshed); the `Alias` column is the stable identifier.",
        "",
        "| Alias | Also Match | `projectPath` | Files | Nodes | DB |",
        "| --- | --- | --- | ---: | ---: | ---: |",
    ]

    for p in projects:
        alias = p.get("alias", "")
        also = ", ".join(p.get("aliases", [])) or ""
        path = p.get("projectPath", "")
        files = p.get("files", "?") or "?"
        nodes = p.get("nodes", "?") or "?"
        db_bytes = p.get("dbSizeBytes", 0) or 0
        db_mb = f"{db_bytes / (1024*1024):.2f} MB" if db_bytes else "?"
        lines.append(f"| {alias} | {also} | `{path}` | {files} | {nodes} | {db_mb} |")

    lines.extend([
        "",
        "## Quick Checks",
        "",
        "Check one repository:",
        "",
        "```bash",
        'codegraph status "$(python3 scripts/resolve_project.py codex --field projectPath)"',
        "```",
        "",
        "Find all CodeGraph indexes:",
        "",
        "```bash",
        "find /Users/mac/Repository/Sources -name .codegraph -type d -prune -print 2>/dev/null | sort",
        "```",
        "",
        "Use a mapped repository with MCP:",
        "",
        "```bash",
        'projectPath="$(python3 scripts/resolve_project.py litellm --field projectPath)"',
        "```",
        "",
        "Refresh the registry after re-indexing or adding new source repositories:",
        "",
        "```bash",
        "python3 scripts/refresh_registry.py --write",
        "```",
    ])

    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Refresh InchHeart CodeGraph registry.")
    parser.add_argument("--registry", default=str(DEFAULT_REGISTRY), help="Path to registry.json")
    parser.add_argument("--write", action="store_true", help="Write refreshed registry back to disk")
    args = parser.parse_args()

    registry_path = Path(args.registry)
    refreshed = refresh(load_registry(registry_path))
    text = json.dumps(refreshed, ensure_ascii=False, indent=2) + "\n"
    if args.write:
        registry_path.write_text(text, encoding="utf-8")
        regenerate_source_repos_md(refreshed, registry_path)
    else:
        print(text, end="")


if __name__ == "__main__":
    main()
