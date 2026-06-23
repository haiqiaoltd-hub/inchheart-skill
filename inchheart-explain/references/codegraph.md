# CodeGraph

## What It Does

CodeGraph is for indexed code understanding, file structure maps, symbol search, callers/callees, and impact analysis.

## CLI

- `codegraph files`
- `codegraph query <search>`
- `codegraph callers <symbol>`
- `codegraph callees <symbol>`
- `codegraph impact <symbol>`
- `codegraph status <path>`
- `codegraph sync <path>`

## MCP

- `codegraph serve --mcp`

## Rule

- Use `projectPath` or a resolved project root when asking the MCP tools about a concrete repo.
