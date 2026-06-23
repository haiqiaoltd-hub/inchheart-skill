# inchheart-zellij

## What It Does

`inchheart-zellij` is the MCP bridge for sending work to agent CLIs running in Zellij panes.

## Main Actions

- `send_to_claude_code`
- `send_to_codex`
- `send_to_opencode`
- `send_to_gemini`
- `zellij_list_sessions`
- `zellij_list_panes`
- `zellij_dump_screen`
- `zellij_bridge_health`
- `zellij_kill_session`
- `zellij_delete_session`

## Rule

- Use the bridge for routing and diagnosis.
- Do not treat Ghostty as the automation target.
- Prefer stable session names for long-running agents.
