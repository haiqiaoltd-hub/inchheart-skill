---
name: inchheart-source
description: "本机源码归档与 CodeGraph 索引维护技能：用于检查、审阅、更新、刷新或下载 /Users/mac/Repository/Sources 中的源码归档，维护 Source说明.md，执行 zip 下载校验、解压替换、codegraph sync、registry 刷新，并通过 resolve_project.py 为 CodeGraph MCP 提供 projectPath。"
---

# InchHeart Source

## Scope

Use this skill to maintain `/Users/mac/Repository/Sources` and its index file:

`/Users/mac/Repository/Sources/Source说明.md`

This is a source archive, not a working project area and not a deployment area.

| Directory | Meaning |
|---|---|
| `/Users/mac/Repository/Sources` | Read, study, compare, back up, and track source code |
| `/Users/mac/Repository/Projects` | User-owned projects under active development |
| `/Users/mac/Repository/Services` | Running local services and deployable service copies |

## Directory Naming Convention

Source archive directories that are CodeGraph-indexed **MUST** use stable names without version numbers or commit hashes. This enables `codegraph sync` (incremental, seconds) instead of `codegraph index` (full rebuild, minutes) when updating to newer versions.

- **CLI projects** (under `agent-cli/`): stable name + `-cli` suffix → e.g., `codex-cli`, `hermes-cli`, `opencode-cli`
- **Non-CLI projects** (under `agent-gateway/`, etc.): stable name without `-cli` → e.g., `litellm`, `cherry-studio`, `cc-switch`
- **Non-updating projects**: move the entire group directory to `no-update/` and note in `Source说明.md`

**Key insight:** The umbrella directory (e.g., `agent-cli/codex-cli/`) contains BOTH the zip archives AND the extracted source directory. The stable-name source directory sits alongside its zip files. When a new zip arrives, it goes into the same umbrella directory, then the extract-overwrite-sync workflow runs on the stable-name subdirectory inside.

Example layout:
```
agent-cli/codex-cli/
├── codex-rust-v0.128.0.zip    # older archive
├── codex-rust-v0.137.0.zip    # newer archive  
└── codex-cli/                  # stable-name extracted source (+ .codegraph/)
```

When a new version zip arrives for an already-indexed project, follow the **"Update & CodeGraph Sync Workflow"** section below — the full Python-based procedure with `.codegraph/` backup, directory wipe, copy-in, and `codegraph sync`.

If the directory still has a versioned name (first-time migration), rename it first. CodeGraph DBs use relative paths and survive renames — verify with `codegraph status <projectPath>`.

## Source说明.md Structure (Current)

The document is organized by CodeGraph index scope:

```
## 持续更新项目
### agent-cli
  Codex, Hermes Agent, OpenCode, Claude Code (leak, archive only)
### agent-gateway
  CC Switch, CC Switch CLI, Cherry Studio, LiteLLM

## 非持续更新项目
### 原 agent-cli（已移至 no-update）
  Gemini CLI, Goose, Pi CLI, AgentScope, OpenClaw
### 原 terminal / plugin（在 no-update 或 Sources 根目录）
  Warp, Zellij, Ghostty, Claudian, mcp-chrome, ...
### 本机部署相关（在 Services 或 no-update）
  new-api, sub2api, CLIProxyAPI, codex2api, ds2api
### 资料与实验（在 no-update）
  inchheart-ui, Memory 插件, awesome-nuwa, ...
### 已删除
  all-api-hub, obsidian-help, obsidian-excalidraw-plugin
```

Key rules for the structure:
- **持续更新项目** are grouped under `agent-cli` and `agent-gateway` — these are the only two directories that contain CodeGraph-indexed projects.
- **非持续更新项目** are moved to `no-update/` and listed by their original category.
- Each 持续更新 entry shows: `本地目录`, `本地最新包`, `上游口径`, `上游地址`.
- Non-continuous entries show: `本地目录`, `当前状态`, optionally `上游地址`.

## Rules

1. Read `Source说明.md` before making decisions.
2. Treat only the projects under `## 持续更新项目` as the default update set.
3. Do not update non-continuous archive projects unless the user explicitly asks.
4. Download source `zip` archives by default. Do not clone, pull, or unzip unless needed for inspection or explicitly requested.
5. Keep old `zip` files unless the user explicitly asks to clean them.
6. Never run long-lived services in `Sources`.
7. If a source is used for deployment, put the running copy in `/Users/mac/Repository/Services`; if it becomes the user's own maintained project, put it in `/Users/mac/Repository/Projects`.
8. When document facts conflict with the filesystem or live upstream checks, trust current checks and update the document.

## CodeGraph Query Workflow

Use this skill as the single entry for CodeGraph-backed source inspection.

1. Identify which source project the user means.
2. Resolve the concrete indexed root through `scripts/resolve_project.py` or `references/registry.json`.
3. Pass the resolved `projectPath` to CodeGraph MCP on every query.
4. Prefer `codegraph_explore` first for architecture, behavior, bug, symbol, or code-area questions. Use narrower CodeGraph tools only for follow-ups.
5. If the project is missing or paths changed, run `python3 scripts/refresh_registry.py --write`, then resolve again.

Quick checks:

```bash
python3 scripts/resolve_project.py codex --field projectPath
codegraph status --json "$(python3 scripts/resolve_project.py codex --field projectPath)"
```

### Known project paths (alias → projectPath)

These are the actively indexed source directories. Pass the `projectPath` value to CodeGraph MCP — no need to run `resolve_project.py` for these.

| Alias | projectPath |
|-------|------------|
| `codex-cli` | `/Users/mac/Repository/Sources/agent-cli/codex-cli/codex-cli` |
| `hermes-cli` | `/Users/mac/Repository/Sources/agent-cli/hermes-cli/hermes-cli` |
| `opencode-cli` | `/Users/mac/Repository/Sources/agent-cli/opencode-cli/opencode-cli` |
| `claudecode-leak` | `/Users/mac/Repository/Sources/agent-cli/claudecode-leak/claude-code-source-cli` |
| `vscode-copilot` | `/Users/mac/Repository/Sources/agent-cli/vscode-copilot/vscode-copilot-chat` |
| `gemini-cli` | `/Users/mac/Repository/Sources/agent-cli/gemini-cli/gemini-cli` |
| `pi-cli` | `/Users/mac/Repository/Sources/agent-cli/pi-cli/pi-cli` |
| `goose-cli` | `/Users/mac/Repository/Sources/agent-cli/goose-cli/goose-cli` |
| `agentscope-cli` | `/Users/mac/Repository/Sources/agent-cli/agentscope-cli/agentscope-cli` |
| `cc-switch` | `/Users/mac/Repository/Sources/agent-gateway/cc-switch/cc-switch` |
| `cc-switch-cli` | `/Users/mac/Repository/Sources/agent-gateway/cc-switch-cli/cc-switch-cli` |
| `new-api` | `/Users/mac/Repository/Sources/agent-gateway/new-api/new-api` |
| `cherry-studio` | `/Users/mac/Repository/Sources/agent-gateway/cherry-studio/cherry-studio` |
| `litellm` | `/Users/mac/Repository/Sources/agent-gateway/litellm/litellm` |
| `clash-verge` | `/Users/mac/Repository/Sources/agent-gateway/clash-verge/clash-verge` |
| `obsidian-claudian` | `/Users/mac/Repository/Sources/plugin/obsidian-claudian/claudian` |
| `nvidia-nim-provider` | `/Users/mac/Repository/Sources/plugin/nvidia-nim-provider/nvidia-nim-provider` |
| `nvidia-nim-agent` | `/Users/mac/Repository/Sources/plugin/nvidia-nim-agent/nvidia-nim-agent` |
| `pi-nim` | `/Users/mac/Repository/Sources/plugin/pi-nim/pi-nvidia-nim` |
| `vscode-nim-code` | `/Users/mac/Repository/Sources/plugin/vscode-nim-code/nim-code` |
| `zellij` | `/Users/mac/Repository/Sources/plugin/zellij/zellij` |
| `tmux` | `/Users/mac/Repository/Sources/plugin/tmux/tmux` |

CodeGraph rules:

- Always pass the mapped `projectPath`; do not pass the parent collection directory unless it contains `.codegraph/codegraph.db`.
- The real project root is the directory immediately above `.codegraph/`.
- If source files changed recently, run `codegraph status --json <projectPath>` and inspect `pendingChanges`.
- If `pendingChanges` is non-zero, run `codegraph sync <projectPath>`, then `python3 scripts/refresh_registry.py --write`.
- If the index is corrupted or badly stale, run `codegraph index <projectPath>`, then refresh the registry.

## Local State Checks

Read the index and directory state before deciding whether to inspect, download, update, or sync:

```bash
# 注意：如果文件名包含中文，sed/cat 可能因 shell 解析失败。优先用 Python 或通配符。
# 错误示例：sed -n '1,260p' /Users/mac/Repository/Sources/Source说明.md  ❌
# 正确做法：
cd /Users/mac/Repository/Sources && cat Source*.md | head -260  # 通配符绕过解析
# 或用 Python execute_code + glob 读取
find /Users/mac/Repository/Sources -maxdepth 2 -type d | sort
find /Users/mac/Repository/Sources -maxdepth 2 -type f -name '*.zip' | sort
```

## Update & CodeGraph Sync Workflow

When a new version zip is already downloaded and needs to replace the current indexed source:

### Step-by-step

1. **Extract new zip to temp directory** (Python `zipfile` or `unzip`).
2. **Backup `.codegraph/`** from the stable-name directory to a temp location.
3. **Wipe the stable-name directory** (delete all files/subdirs except `.codegraph/`). Use Python `shutil` — **do NOT use rsync** (macOS rsync has a concurrency bug: `poll: bad fd / unexpected end of file`).
4. **Copy new files into the stable-name directory** (Python `shutil.copytree` / `shutil.copy2` for each item).
5. **Restore `.codegraph/`** if it was deleted during wipe.
6. **Run `codegraph sync <projectPath>`** — incremental update, takes seconds.
7. **Run `refresh_registry.py --write`** to update the CodeGraph registry.
8. **Regenerate `source-repos.md`** from `registry.json`. The refresh script does this automatically.

### Verified clean method (Python)

```python
import zipfile, shutil, os, tempfile
from pathlib import Path

tmp_dir = tempfile.mkdtemp(prefix="codegraph_update_")

# Extract
with zipfile.ZipFile(zip_path, 'r') as zf:
    zf.extractall(tmp_dir)

# GitHub zips have one top-level directory
extracted = os.listdir(tmp_dir)
new_src = Path(tmp_dir) / extracted[0] if len(extracted) == 1 else Path(tmp_dir)

# Backup .codegraph
cg_bak = tempfile.mkdtemp(prefix="cg_bak_")
if (src_dir / ".codegraph").exists():
    shutil.copytree(src_dir / ".codegraph", Path(cg_bak), symlinks=True)

# Wipe everything except .codegraph
for item in src_dir.iterdir():
    if item.name == ".codegraph":
        continue
    if item.is_dir():
        shutil.rmtree(item, ignore_errors=True)
    else:
        item.unlink()

# Copy new files in
for item in new_src.iterdir():
    dst = src_dir / item.name
    if item.is_dir():
        shutil.copytree(item, dst, symlinks=True)
    else:
        shutil.copy2(item, dst)

# Restore .codegraph if needed
if Path(cg_bak).exists() and not (src_dir / ".codegraph").exists():
    shutil.copytree(Path(cg_bak), src_dir / ".codegraph", symlinks=True)

# Cleanup
shutil.rmtree(tmp_dir, ignore_errors=True)
shutil.rmtree(cg_bak, ignore_errors=True)
```

Then run codegraph sync and refresh:

```bash
codegraph sync /path/to/stable-name-dir
python3 scripts/refresh_registry.py --write
```

### Pitfalls

- **NEVER use rsync**: macOS bundled rsync has a race condition (`poll: bad fd / unexpected end of file`) that fails intermittently. Use Python `shutil` instead.
- **NEVER use `cp -a` directly**: It fails when overwriting directories that already exist (`Is a directory` error). Wipe first, then `shutil.copytree`.
- **Always preserve `.codegraph/`**: The CodeGraph DB lives there. If you accidentally delete it, you must run `codegraph index` (full rebuild, slow) instead of `codegraph sync`.
- **Verify after sync**: Run `codegraph status --json <path>` and check `pendingChanges` are all 0. If not, run `codegraph sync` again.
- **Registry filter**: After moving projects to `no-update/`, run `refresh_registry.py --write` then verify `registry.json` no longer contains `/no-update/` paths. Manually filter if needed.

## CodeGraph Registry Files

`references/registry.json` is the single source of truth for known CodeGraph indexes.

`references/source-repos.md` is generated from `registry.json`; do not hand-edit version-specific paths into it.

`scripts/resolve_project.py` resolves aliases such as `codex`, `litellm`, `cc-switch`, or `opencode` to a concrete `projectPath`.

`scripts/refresh_registry.py` rescans `/Users/mac/Repository/Sources` for `.codegraph/` directories, updates `registry.json`, and regenerates `source-repos.md`.

## Pitfalls

- **文件名含特殊字符**：`Source说明.md` 在文件系统中可能含不可见字符或非 ASCII 编码。直接用完整路径可能失败（`No such file or directory`）。用通配符 `Source*.md` 或先进入目录再操作更可靠。
- **路径空格处理**：Shell 命令中路径含空格时必须加引号，如 `"/Users/mac/Repository/Sources/Source说明.md"`。优先 `cd` 到目录再操作可避免引号问题。
- **macOS rsync bug**：macOS 自带 rsync 在并发操作时可能报 `poll: bad fd / unexpected end of file`。源码覆盖更新时一律用 Python `shutil`，不用 rsync。
- **`cp -a` 覆盖目录报错**：`cp -a new_src/. old_dir/` 在目标目录已有同名子目录时会报 `Is a directory`。正确做法：先清空目标（保留 `.codegraph/`），再逐项复制。

## Upstream Check Workflow

1. Extract the continuous update list from the document. For each item, note:

| Field | Meaning |
|---|---|
| 本地目录 | Where the package should be stored |
| 本地最新包 | Current newest local `zip` |
| 上游口径 | `release` or `main` branch commit |
| 上游最新 | Expected upstream version/tag/commit |
| 上游地址 | GitHub repository URL |

2. Check upstream only for continuous projects:

```bash
# Latest release tag
gh api repos/owner/repo/releases/latest --jq '.tag_name'

# Main branch commit
gh api repos/owner/repo/commits/main --jq '.sha'
```

Use `git ls-remote --tags` only when release API is unavailable or a repo has unusual release behavior.

3. If upstream is newer, download a GitHub source archive `zip` into the existing local directory:

```bash
curl -fL 'https://api.github.com/repos/owner/repo/zipball/<tag-or-sha>' \
  -o '/Users/mac/Repository/Sources/<local-dir>/<repo-version>.zip'
```

Prefer the naming style already used by that directory, for example:

| Upstream type | Local filename pattern |
|---|---|
| release tag `v1.2.3` | `project-1.2.3.zip` |
| release tag `rust-v0.137.0` | `codex-rust-v0.137.0.zip` |
| main commit `abcdef...` | `project-main-abcdef123456.zip` |

4. Validate every newly downloaded archive:

```bash
unzip -t '/path/to/new.zip' | tail -n 1
```

Accept only `No errors detected...`. If validation fails, delete only the bad file you just downloaded and report the failure.

5. Update `Source说明.md`:

| Section | Required update |
|---|---|
| `更新时间` | Current local timestamp |
| `巡检时间` | Current local timestamp |
| Updated project | `本地最新包`, `上游最新`, `本次结果` |
| Already-current project | Mark `已是最新` if the previous note implies a stale action |
| Filesystem mismatches | Correct local directory/package facts |
| New source dirs | Add as non-continuous unless the user asks to track continuously |

**注意：** 如果文件名包含中文（如 `Source说明.md`），不要用 sed/cat 直接编辑。使用 Python execute_code 读取全文，用字符串替换更新，然后 write_file 覆盖写回。见 Local State Checks 的注释。

6. Final verification:

```bash
find /Users/mac/Repository/Sources -maxdepth 2 -type f -name '*.zip' | sort
rg -n '<new-version>|<new-sha>|当前未在 `Sources`' /Users/mac/Repository/Sources/Source说明.md
```

## Document Editing Guidance

Keep the index factual and conservative:

- Use Chinese text in the document.
- Preserve the existing Markdown style.
- Do not invent "old packages retained" claims; verify with `find`.
- If an item is now in `Services` or `Projects`, write its actual path and say it is not in `Sources`.
- If a directory exists in `Sources` but is not in the continuous list, add it under `## 非持续更新项目` unless the user explicitly wants continuous tracking.
- **Moving to `no-update/`**: When the user decides a project is no longer worth tracking, move the entire group directory (e.g., `agent-cli/goose-cli` → `no-update/goose-cli`). Then update `Source说明.md` to move the entry from 持续更新 to 非持续更新, noting the new `no-update/` path. Run `refresh_registry.py --write` afterwards so CodeGraph registry picks up the path change.
- If an upstream repository redirects, record the resolved current upstream address.
- **Filename with Chinese characters:** When reading/editing `Source说明.md` or similar files with Chinese names, do NOT use `sed`, `cat`, or direct path arguments in terminal — shell parsing often fails. Use Python's `glob.glob("Source*.md")` to resolve the filename, then read/write via `execute_code`. This is a recurring pitfall on macOS with zh-CN filenames.

## Reporting

In the final answer, include:

| Item | What to report |
|---|---|
| New downloads | Project, old version/commit, new version/commit |
| No-change checks | Mention that other continuous projects were checked and remain current |
| Document updates | Mention `Source说明.md` changed |
| Validation | State whether `unzip -t` passed |
| Non-actions | State that no files were deleted, no packages were unzipped, and no services were run when true |
