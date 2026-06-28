---
name: inchheart-explain
description: "本机 CLI 与 MCP 参考书技能：用于解释本机常用命令行工具、CodeGraph、Context7、node_repl、inchheart-zellij、GitHub workflow、各 CLI（OpenCode/Hermes 等）自建中转模型参数配置，以及其他 MCP 的用途、配置、启用范围和排障方式。"
---

# InchHeart Explain

Use this skill when the user asks how the local CLI or MCP stack works, how the servers are configured, which tool to use, or how to troubleshoot the machine's utility layer.

## Read First

- `references/cli.md` for local CLI overview
- `references/mcp.md` for MCP overview and configuration patterns
- `references/codegraph.md` for CodeGraph
- `references/context7.md` for Context7
- `references/node-repl.md` for Node REPL
- `references/zellij.md` for `inchheart-zellij`
- `references/github-workflow.md` for GitHub PR / issue / review / repo operations
- `references/cli-model-config.md` for configuring self-hosted relay model params (context / reasoning / modalities) in OpenCode, Hermes, and other CLIs

## Rules

- Keep answers grounded in the current machine state and local config files.
- Prefer the simplest tool that fits the task.
- If a tool has both CLI and MCP forms, explain the split clearly.
- If the user asks for a specific tool, follow that tool's reference file.
- If the user asks about GitHub workflow, prefer `gh` CLI and read `references/github-workflow.md`.
