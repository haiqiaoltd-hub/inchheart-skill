# Sources CodeGraph Indexes

Last verified: 2026-06-28T21:51:54+08:00.

Use the directory shown in `projectPath` as the CodeGraph MCP `projectPath`. The parent collection directory is usually not initialized; the concrete extracted repository directory is initialized.

Release versions and commit hashes embedded in directory names change with every update — **do not hard-code them here**. The `projectPath` column comes from `registry.json` (auto-refreshed); the `Alias` column is the stable identifier.

| Alias | Also Match | `projectPath` | Files | Nodes | DB |
| --- | --- | --- | ---: | ---: | ---: |
| agentscope-cli |  | `/Users/mac/Repository/Sources/agent-cli/agentscope-cli/agentscope-cli` | 533 | 7242 | 12.97 MB |
| cc-switch |  | `/Users/mac/Repository/Sources/agent-gateway/cc-switch/cc-switch` | 597 | 11620 | 33.33 MB |
| cc-switch-cli |  | `/Users/mac/Repository/Sources/agent-gateway/cc-switch-cli/cc-switch-cli` | 372 | 15917 | 54.62 MB |
| cherry-studio |  | `/Users/mac/Repository/Sources/agent-gateway/cherry-studio/cherry-studio` | 1889 | 28925 | 57.43 MB |
| clash-verge |  | `/Users/mac/Repository/Sources/agent-gateway/clash-verge/clash-verge` | 392 | 5114 | 10.94 MB |
| claudecode-leak |  | `/Users/mac/Repository/Sources/agent-cli/claudecode-leak/claude-code-source-cli` | 2154 | 46059 | 81.71 MB |
| codex-cli |  | `/Users/mac/Repository/Sources/agent-cli/codex-cli/codex-cli` | 3157 | 100876 | 251.03 MB |
| gemini-cli |  | `/Users/mac/Repository/Sources/agent-cli/gemini-cli/gemini-cli` | 2258 | 29504 | 53.16 MB |
| goose-cli |  | `/Users/mac/Repository/Sources/agent-cli/goose-cli/goose-cli` | 1270 | 25196 | 64.25 MB |
| hermes-cli |  | `/Users/mac/Repository/Sources/agent-cli/hermes-cli/hermes-cli` | 3969 | 107630 | 221.89 MB |
| litellm |  | `/Users/mac/Repository/Sources/agent-gateway/litellm/litellm` | 5881 | 111189 | 227.43 MB |
| new-api |  | `/Users/mac/Repository/Sources/agent-gateway/new-api/new-api` | 1956 | 29195 | 59.29 MB |
| nvidia-nim-agent |  | `/Users/mac/Repository/Sources/plugin/nvidia-nim-agent/nvidia-nim-agent` | 44 | 520 | 1.13 MB |
| nvidia-nim-provider |  | `/Users/mac/Repository/Sources/plugin/nvidia-nim-provider/nvidia-nim-provider` | 27 | 436 | 0.89 MB |
| obsidian-claudian |  | `/Users/mac/Repository/Sources/plugin/obsidian-claudian/claudian` | 603 | 9282 | 19.43 MB |
| opencode-cli |  | `/Users/mac/Repository/Sources/agent-cli/opencode-cli/opencode-cli` | 2851 | 50197 | 105.62 MB |
| pi-cli |  | `/Users/mac/Repository/Sources/agent-cli/pi-cli/pi-cli` | 810 | 12809 | 31.18 MB |
| pi-nim |  | `/Users/mac/Repository/Sources/plugin/pi-nim/pi-nvidia-nim` | 3 | 68 | 0.23 MB |
| tmux |  | `/Users/mac/Repository/Sources/plugin/tmux/tmux` | 203 | 4952 | 8.84 MB |
| vscode-copilot |  | `/Users/mac/Repository/Sources/agent-cli/vscode-copilot/vscode-copilot-chat` | 2897 | 66021 | 129.33 MB |
| vscode-nim-code |  | `/Users/mac/Repository/Sources/plugin/vscode-nim-code/nim-code` | ? | ? | 0.13 MB |
| zellij |  | `/Users/mac/Repository/Sources/plugin/zellij/zellij` | 348 | 15614 | 49.21 MB |

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
