# InchHeart Skill

Personal InchHeart skills for Codex, Claude, OpenCode, Hermes, and CC Switch.

This repository is organized as one skill per directory. Each skill directory contains a `SKILL.md` file, plus optional `references/`, `scripts/`, or other support files.

## Skills

- `inchheart-sort`
- `inchheart-cloud`
- `inchheart-epub`
- `inchheart-gem`
- `inchheart-search` - local SearXNG search plus Obscura/Camoufox web scraping and browser workflow
- `inchheart-source` - source archive updates plus CodeGraph registry and sync workflow
- `inchheart-wisdom`
- `inchheart-explain`

## CC Switch

CC Switch can discover these skills by scanning for `SKILL.md` files in this repository.

Recommended local workflow:

1. Edit skills in this repository.
2. Push changes to GitHub.
3. Use CC Switch to update skills from the GitHub repository.
4. Keep CC Switch skill sync mode set to `copy`.

Do not commit private API keys, tokens, local credentials, or machine-specific runtime config.
