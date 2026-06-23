# GitHub Workflow

## What It Does

Use this section for GitHub auth, PRs, issues, code review, repository management, and release/secrets tasks.

## Core Rule

- Prefer `gh` CLI when available.
- Fall back to `git` + `curl` + GitHub REST API when needed.

## Typical Tasks

- Check auth: `gh auth status`
- Create PR: `gh pr create`
- Review PR: `gh pr review`
- Manage issues: `gh issue list|view|create|edit|comment|close`
- Repo admin: `gh repo clone|create|fork|view`
- Releases: `gh release create|list`
- Secrets: `gh secret set|list`

## Local Flow

1. Detect whether `gh` is installed and authenticated.
2. Extract owner/repo from the remote when needed.
3. Use `gh` for the common path.
4. Use `git` + `curl` only when `gh` is unavailable or headless access is required.
