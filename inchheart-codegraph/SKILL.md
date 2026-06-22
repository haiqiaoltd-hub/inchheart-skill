---
name: inchheart-codegraph
description: Use CodeGraph MCP for InchHeart's locally indexed source archive. Trigger when the user asks to inspect, understand, compare, review, or trace code in known source projects such as Hermes, Claude Code, Codex, OpenCode, Gemini CLI, CC Switch, Cherry Studio, LiteLLM, or asks about CodeGraph projectPath usage and indexed source directories.
---

# InchHeart CodeGraph

## Overview

Use this skill to query InchHeart's pre-indexed CLI source repositories with `CodeGraph MCP`. The important rule is simple: do not rely on CodeGraph to discover these repositories from `/Users/mac`; resolve the repository through this skill and explicitly pass the resulting `projectPath`.

## Workflow

1. Identify which CLI source repository the user means.
2. Resolve the repository through `references/registry.json` or `scripts/resolve_project.py`.
3. Call CodeGraph MCP with the selected `projectPath` on every query.
4. Prefer `codegraph_explore` first for architecture, behavior, bug, symbol, or code-area questions. Use `codegraph_node`, `codegraph_callers`, `codegraph_callees`, `codegraph_impact`, or `codegraph_files` only for narrower follow-ups.
5. If the repository is not listed, run `scripts/refresh_registry.py --write` to rescan `/Users/mac/Repository/Sources`, then resolve again.

## CodeGraph Rules

- Always pass `projectPath` for the mapped repositories.
- Do not use `/Users/mac/Repository/Sources/<source-collection>` as `projectPath` unless that directory itself contains `.codegraph/codegraph.db`.
- The real project root is the directory immediately above `.codegraph/`.
- If `CodeGraph MCP` says no project is loaded, retry with the explicit `projectPath` from `references/registry.json`.
- If the source was just updated, verify freshness before relying on CodeGraph results.
- If `codegraph_status` fails for a listed path, verify with:

```bash
codegraph status /absolute/project/path
```

## Freshness

Handle CodeGraph and source updates by case:

| Case | Action |
| --- | --- |
| A new source repository now has `.codegraph/` | Run `python3 scripts/refresh_registry.py --write` so the skill learns it. |
| A listed `.codegraph/` database changed | Run `python3 scripts/refresh_registry.py --write` to refresh stats and status. |
| Source files changed but CodeGraph may be stale | Run `codegraph status --json <projectPath>` and inspect `pendingChanges`. |
| `pendingChanges` shows added, modified, or removed files | Run `codegraph sync <projectPath>`, then refresh the registry. |
| The index looks corrupted or badly out of date | Run `codegraph index <projectPath>`, then refresh the registry. |
| `worktreeMismatch` is not null | Treat results as suspect; re-index or rebuild the correct project root. |
| A source directory was renamed or replaced (version bump) | Run `python3 scripts/refresh_registry.py --write`, then regenerate `source-repos.md` from `registry.json` — see "Regenerating source-repos.md" below. |

Before answering code questions after a recent `git pull`, source replacement, unzip, branch change, or manual file edit, prefer:

```bash
codegraph status --json "$(python3 scripts/resolve_project.py codex --field projectPath)"
```

If pending changes are non-zero:

```bash
projectPath="$(python3 scripts/resolve_project.py codex --field projectPath)"
codegraph sync "$projectPath"
python3 scripts/refresh_registry.py --write
```

### Regenerating source-repos.md

`source-repos.md` is a **derived file** generated from `registry.json`. When directory names change (e.g., `litellm-1.83.13-nightly` → `litellm-1.89.0`), the registry updates but `source-repos.md` stays stale. After running `refresh_registry.py --write`, regenerate `source-repos.md` to keep it in sync. The key rule: **never hard-code version numbers or commit hashes in `source-repos.md`** — the `projectPath` column must always come from `registry.json` (the single source of truth).

## Directory Naming Convention (Critical)

Source archive directories **MUST NOT** embed version numbers, commit hashes, or org prefixes in their final directory name. Use stable, short names so that future updates can overwrite files in-place and run `codegraph sync` instead of a full `codegraph index`.

| Do | Don't | Why |
| --- | --- | --- |
| `codex-cli` | `openai-codex-cfa0e4c` | Overwrite → `sync` (seconds) |
| `hermes-cli` | `NousResearch-hermes-agent-66a6b9c` | Overwrite → `sync` (seconds) |
| `litellm` | `litellm-1.83.13-nightly` | Overwrite → `sync` (seconds) |
| `opencode-cli` | `anomalyco-opencode-76c631d` | Overwrite → `sync` (seconds) |
| `gemini-cli` | `google-gemini-gemini-cli-dfa8394` | Overwrite → `sync` (seconds) |
| `claude-code-source-cli` | `claude-code-source-main` | Overwrite → `sync` (seconds) |
| `cherry-studio` | `CherryHQ-cherry-studio-b574570` | Overwrite → `sync` (seconds) |
| `cc-switch` | `farion1231-cc-switch-25951d8` | Overwrite → `sync` (seconds) |
| `cc-switch-cli` | `SaladDay-cc-switch-cli-8189886` | Overwrite → `sync` (seconds) |

**CLI suffix rule:** Projects under `agent-cli/` (CLI tools) get a `-cli` suffix in their stable name (e.g., `codex-cli`, `hermes-cli`). Projects under `agent-gateway/` or other categories (desktop apps, libraries, gateways) do **not** get the `-cli` suffix (e.g., `litellm`, `cherry-studio`, `cc-switch`).

When a new zip arrives:

1. Extract it to a **temporary** location.
2. Delete all files in the existing stable-name directory (but keep `.codegraph/`).
3. Copy the new files into the stable-name directory.
4. Run `codegraph sync <projectPath>` — incremental, fast.
5. Run `python3 scripts/refresh_registry.py --write`.
6. Regenerate `source-repos.md` from `registry.json` (see "Regenerating source-repos.md").

If the directory still has a versioned name, the first time you must:

1. Rename it to the stable name (`mv old-name new-name`).
2. Verify with `codegraph status <projectPath>` — the DB uses relative paths and survives renames.
3. Run `python3 scripts/refresh_registry.py --write` to update `registry.json` and `source-repos.md`.

### Implementation (Python preferred)

**Pitfall: macOS rsync bug** — `rsync --delete` fails with `error: poll: bad fd / unexpected end of file` when multiple rsync processes run concurrently on macOS. Do NOT use rsync for the overwrite step. Use Python `shutil` instead:

```python
import shutil, os, zipfile, tempfile
from pathlib import Path

# Step 1: Extract to temp
tmp_dir = tempfile.mkdtemp(prefix="codegraph_update_")
with zipfile.ZipFile(zip_path, 'r') as zf:
    zf.extractall(tmp_dir)

# Find the extracted root (GitHub zips have one top-level dir)
items = os.listdir(tmp_dir)
new_src = Path(tmp_dir) / items[0] if len(items) == 1 and os.path.isdir(os.path.join(tmp_dir, items[0])) else Path(tmp_dir)

# Step 2: Backup .codegraph, clear old files, copy new, restore .codegraph
cg_bak = Path(tempfile.mkdtemp(prefix="cg_bak_"))
if (src_dir / ".codegraph").exists():
    shutil.copytree(src_dir / ".codegraph", cg_bak, symlinks=True)

for item in src_dir.iterdir():
    if item.name == ".codegraph":
        continue
    if item.is_dir():
        shutil.rmtree(item, ignore_errors=True)
    else:
        item.unlink()

for item in new_src.iterdir():
    dst = src_dir / item.name
    if item.is_dir():
        shutil.copytree(item, dst, symlinks=True)
    else:
        shutil.copy2(item, dst)

if cg_bak.exists() and not (src_dir / ".codegraph").exists():
    shutil.copytree(cg_bak, src_dir / ".codegraph", symlinks=True)

# Step 3: sync + refresh
subprocess.run(["codegraph", "sync", str(src_dir)], ...)
subprocess.run(["python3", scripts_dir / "refresh_registry.py", "--write"], ...)

# Cleanup
shutil.rmtree(tmp_dir, ignore_errors=True)
shutil.rmtree(cg_bak, ignore_errors=True)
```

### Registry filtering

`registry.json` only contains projects under `agent-cli/` and `agent-gateway/`. The `refresh_registry.py` script automatically:
- **Excludes** any project whose `projectPath` contains `/no-update/`
- **Excludes** any project not under `agent-cli/` or `agent-gateway/`

**Pitfall:** When a project directory is moved to `no-update/` *before* running `refresh_registry.py`, the old path entry may persist in `registry.json` (the script scans for `.codegraph/` directories that currently exist — if the directory was already moved away, the stale entry remains). After moving projects to `no-update/`, verify `registry.json` and manually remove any entries with `/no-update/` in the path. Then re-run `refresh_registry.py --write` to rewrite the file cleanly.

## `source-repos.md` Maintenance

`references/source-repos.md` is **auto-generated** from `registry.json` by the refresh script. Do NOT hand-edit version-specific paths into it. Running `refresh_registry.py --write` regenerates both `registry.json` and (via post-write hook) `source-repos.md`. The markdown table's `projectPath` column always reflects the current `registry.json` data.

## References & Scripts

- `references/registry.json` — **single source of truth** for all known CodeGraph indexes. Auto-refreshed by `refresh_registry.py --write`.
- `references/source-repos.md` — human-readable table derived from `registry.json`. Do NOT hand-edit version-specific paths.
- `scripts/resolve_project.py` — resolve a project alias to its `projectPath`.
- `scripts/refresh_registry.py` — rescan `/Users/mac/Repository/Sources` for `.codegraph/` directories, update `registry.json`, then regenerate `source-repos.md`.

## Overwrite-then-Sync Update Procedure

When a new version zip arrives for an already-indexed project:

**Do NOT use rsync** — macOS `rsync --delete` has a concurrency bug (`poll: bad fd / unexpected end of file`) that causes silent failures when multiple rsync processes run in the same session. Use Python `shutil` instead (see "Implementation (Python preferred)" above).

Shell-based alternative (single project only, no concurrency):

```bash
# 1. Extract new version to temp
cd /Users/mac/Repository/Sources/<category>/<project>/
unzip -q <new-version>.zip -d /tmp/<project>-new

# 2. Remove old source files (keep .codegraph/ and .zip files)
# CAUTION: This find-based approach may miss directories. Prefer Python shutil.
find <stable-dir-name> -mindepth 1 \
  -not -path '<stable-dir-name>/.codegraph*' \
  -not -name '*.zip' \
  -not -name '.DS_Store' \
  -delete

# 3. Copy new files in (avoid rsync; use cp -a or Python shutil)
cp -a /tmp/<project>-new/<extracted-dir>/. <stable-dir-name>/

# 4. Incremental sync (fast!)
codegraph sync "/Users/mac/Repository/Sources/<category>/<project>/<stable-dir-name>"

# 5. Refresh registry + regenerate source-repos.md
python3 scripts/refresh_registry.py --write

# 6. Cleanup
rm -rf /tmp/<project>-new
```

Key points:
- **Never delete `.codegraph/`** — that is the index database.
- Keep `.zip` files alongside the directory for archival; they do not interfere.
- **Avoid rsync on macOS** — use `cp -a` or Python `shutil.copytree` instead.
- If `codegraph sync` reports `worktreeMismatch`, fall back to `codegraph index`.
