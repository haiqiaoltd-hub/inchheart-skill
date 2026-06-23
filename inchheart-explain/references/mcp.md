# MCP Overview

## What MCP Is

MCP servers expose tools to agents. They are not the same as shell CLIs.

## Local Patterns

| Service | Role |
|---|---|
| `codegraph` | code graph MCP and CLI |
| `context7` | docs lookup MCP |
| `node_repl` | JavaScript execution MCP |
| `inchheart-zellij` | Zellij agent bridge MCP |

## Configuration Notes

- CLI config is usually in `~/.codex/config.toml`.
- CC Switch may mirror the same MCP server list in `~/.cc-switch/cc-switch.db`.
- HTTP MCPs commonly use `url` plus headers or auth.
- stdio MCPs usually use `command` plus `args`.

## Split Guidance

- CLI questions usually belong in the tool's CLI reference.
- "How do I wire this into Codex/Claude/OpenCode?" usually belongs here.
