---
name: inchheart-zellij-explain
description: "inchheart-zellij MCP 说明与排障技能：用于把任务发送给 Zellij 中运行的 Claude Code、OpenAI Codex CLI、OpenCode 或 Gemini CLI，控制 agent 会话，排查 pane/session 路由问题，并理解桥接工具用法。"
---

# InchHeart Zellij Agent Bridge

Use this skill when routing work to interactive agent CLIs running inside Zellij.

Ghostty is only the host terminal. Do not treat Ghostty itself as the automation target. The bridge controls Zellij panes.

## Core Rule

Prefer the MCP tools from `inchheart-zellij` when available:

- `send_to_claude_code` for Claude Code
- `send_to_codex` for OpenAI Codex CLI
- `send_to_opencode` for OpenCode
- `send_to_gemini` for Gemini CLI
- `zellij_kill_session` to stop a background Zellij session cleanly
- `zellij_delete_session` to remove saved Zellij session history
- `zellij_bridge_health` to summarize Zellij availability, active sessions, defaults, recent jobs, and agent roster
- `zellij_list_sessions`, `zellij_list_panes`, and `zellij_dump_screen` for diagnosis

The MCP tools actually execute `zellij` actions. This skill only tells you how to choose and verify targets.

The `send_to_*` tools can auto-start a missing agent session. When no verified target exists, they create an independent background Zellij session by default, start the CLI, wait for the UI to become recognizable, and then send the prompt. They do not open Ghostty unless `openGhostty=true` is explicitly passed.

Safety behavior:

- The bridge sends directly to the target pane with `--pane-id`.
- Agent-specific send tools queue the whole resolve/start/send workflow by default and return immediately.
- The bridge does not focus panes before sending.
- The Zellij session that invoked the MCP server is excluded by default.
- Keep `allowInvokerSession=false` unless the user explicitly wants to type into the current calling session.
- Do not use `send_to_codex` to target the same Codex pane that is currently answering.
- `send_to_*` returns a `jobId`; use `bridge_job_status` or `bridge_job_status(persisted=true)` for delivery status.
- A completed job only means the message reached the pane; the receiving agent can still fail internally.
- When using `collect_agent_responses` with a marker that appears in the prompt text, set `ignorePromptEcho=true` or `minMarkerCount=2` so the prompt echo is not mistaken for the response.

In a shared multi-tab session, the bridge prefers panes whose `tab_name`, pane title, or launch command match the requested agent. If the user keeps one visible Ghostty window, recommend naming the tabs `Claude`, `Codex`, `OpenCode`, and `Gemini`.

## Current Session Map

- Claude Code: `claude_session`, pane `terminal_0`
- Codex CLI: `verdant-mouse`, pane `terminal_0`
- OpenCode: `implacable-peach`, pane `terminal_0`
- Gemini CLI: `gemini_session`, pane `terminal_0`
- `triangular-yak` has been observed as Claude Code, not Codex.

If the user later creates a stable Codex automation session, prefer:

```bash
zellij --session codex_session
codex --dangerously-bypass-approvals-and-sandbox
```

Then call `send_to_codex` with `session: "codex_session"`.

If the user later creates a stable OpenCode automation session, prefer:

```bash
zellij --session opencode_session
opencode
```

Then call `send_to_opencode` with `session: "opencode_session"`.

For one-shot non-interactive work outside the bridge's persistent TUI flow, `opencode run --dangerously-skip-permissions "..."` is valid. Do not replace the bridge's default persistent startup command with that `run` form unless the user explicitly wants one-shot execution.

If the user later creates a stable Gemini automation session, prefer:

```bash
zellij --session gemini_session
gemini --yolo
```

Then call `send_to_gemini` with `session: "gemini_session"`.

## Sending Workflow

Before sending to an uncertain target during diagnosis:

1. Call `zellij_list_sessions`.
2. Call `zellij_list_panes` for the likely session.
3. Call `zellij_dump_screen` on `terminal_0`.
4. Confirm the screen looks like the intended agent.
5. Send with the matching `send_to_*` tool only if the target is not the current calling session.

The MCP tools clear the input with `Ctrl-u`, paste the prompt, then press Enter.
If a session is missing, prefer the high-level send tool with its default `autoStart=true` instead of trying to boot the session manually with raw shell commands.

If the user asks to stop, close, or clean up a background agent session, do not send random keys into the terminal. Prefer:

1. `zellij_kill_session` to stop a running session.
2. `zellij_delete_session(force=true)` if the user wants the session cleaned up as well.

## Zellij Cheat Sheet

Use these commands when you need to reason about the user's session state or explain recovery steps:

```bash
zellij -s claude_session
zellij attach claude_session
zellij attach --create-background claude_session
zellij list-sessions
zellij ls
zellij kill-session claude_session
zellij kill-all-sessions
zellij delete-session claude_session
zellij delete-session --force claude_session
zellij delete-all-sessions
```

Useful built-in UI note:

- `Ctrl o` then `w` opens the session manager in the default preset.

## Error Handling

- `Pane Terminal(0) is already focused`: normal; bridge should continue.
- `Session not found`: ask the user to start or attach the intended session.
- Target does not look like Codex/Claude: list sessions and dump screens; do not blindly send.
- Target does not look like OpenCode: verify the session shows the OpenCode TUI prompt.
- Target does not look like Gemini: verify the session shows the Gemini CLI header or footer before sending.
- No action after sending: the agent may be busy, not at an input prompt, or awaiting confirmation.

## Recognition Hints

- Claude Code usually shows `Claude Code`, model names like `Haiku` or `Sonnet`, and `⏺` output markers.
- Codex usually shows `Codex` or model info in the lower status area.
- OpenCode usually shows `ctrl+p commands` in the footer; the first-screen layout can differ from the post-message layout.
- Gemini usually shows `Gemini CLI` in the header and `/model` plus sandbox info in the footer.

## User-Facing Advice

For stable long-term use, recommend fixed session names:

```bash
zellij --session claude_session
claude --dangerously-skip-permissions
```

```bash
zellij --session codex_session
codex --dangerously-bypass-approvals-and-sandbox
```

```bash
zellij --session opencode_session
opencode
```

```bash
zellij --session gemini_session
gemini --yolo
```

When the user wants a one-shot instruction such as "go do this in Claude Code", prefer calling the matching `send_to_*` tool directly and let it auto-start the session if needed. Do not first ask the user to open Ghostty or run Zellij unless the launcher actually fails.
