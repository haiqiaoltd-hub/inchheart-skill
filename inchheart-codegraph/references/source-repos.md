# Sources CodeGraph Indexes

Last verified: 2026-06-22T14:17:24+08:00.

Use the directory shown in `projectPath` as the CodeGraph MCP `projectPath`. The parent collection directory is usually not initialized; the concrete extracted repository directory is initialized.

Release versions and commit hashes embedded in directory names change with every update — **do not hard-code them here**. The `projectPath` column comes from `registry.json` (auto-refreshed); the `Alias` column is the stable identifier.

| Alias | Also Match | `projectPath` | Files | Nodes | DB |
| --- | --- | --- | ---: | ---: | ---: |
| agent-gateway |  | `/Users/mac/Repository/Sources/agent-gateway/new-api` | 1919 | 27978 | 59.29 MB |
| agentscope-cli |  | `/Users/mac/Repository/Sources/no-update/agentscope-cli/agentscope-cli` | 489 | 6599 | 12.97 MB |
| cc-switch |  | `/Users/mac/Repository/Sources/agent-gateway/cc-switch/cc-switch` | 587 | 11378 | 30.88 MB |
| cc-switch-cli |  | `/Users/mac/Repository/Sources/agent-gateway/cc-switch-cli/cc-switch-cli` | 369 | 15881 | 54.62 MB |
| cherry-studio |  | `/Users/mac/Repository/Sources/agent-gateway/cherry-studio/cherry-studio` | 1889 | 28925 | 57.43 MB |
| claudecode-leak |  | `/Users/mac/Repository/Sources/agent-cli/claudecode-leak/claude-code-source-cli` | 2154 | 46059 | 81.71 MB |
| codex-cli |  | `/Users/mac/Repository/Sources/agent-cli/codex-cli/codex-cli` | 3055 | 97085 | 228.65 MB |
| gemini-cli |  | `/Users/mac/Repository/Sources/no-update/gemini-cli/gemini-cli` | 2245 | 29362 | 53.16 MB |
| goose-cli |  | `/Users/mac/Repository/Sources/no-update/goose-cli/goose-cli` | 1174 | 22604 | 54.39 MB |
| hermes-cli |  | `/Users/mac/Repository/Sources/agent-cli/hermes-cli/hermes-cli` | 3636 | 99740 | 218.35 MB |
| litellm |  | `/Users/mac/Repository/Sources/agent-gateway/litellm/litellm` | 5682 | 104927 | 227.43 MB |
| openclaw-cli |  | `/Users/mac/Repository/Sources/no-update/openclaw-cli/openclaw-cli` | 17393 | 302080 | 562.15 MB |
| opencode-cli |  | `/Users/mac/Repository/Sources/agent-cli/opencode-cli/opencode-cli` | 2660 | 47482 | 94.34 MB |
| pi-cli |  | `/Users/mac/Repository/Sources/no-update/pi-cli/pi-cli` | 672 | 11353 | 25.41 MB |
| vscode-copilot |  | `/Users/mac/Repository/Sources/agent-cli/vscode-copilot/vscode-copilot-chat` | 2897 | 66021 | 129.33 MB |

## Quick Checks

Check one repository:

```bash
codegraph status "$(python3 scripts/resolve_project.py codex --field projectPath)"
```

Find all CodeGraph indexes:

```bash
find /Users/mac/Repository/Sources -name .codegraph -type d -prune -print 2>/dev/null | sort
```

Use a mapped repository with MCP:

```bash
projectPath="$(python3 scripts/resolve_project.py litellm --field projectPath)"
```

Refresh the registry after re-indexing or adding new source repositories:

```bash
python3 scripts/refresh_registry.py --write
```
