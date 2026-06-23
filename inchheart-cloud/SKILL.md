---
name: inchheart-cloud
description: "InchHeart 云服务与部署运维技能：用于连接 GCP Ubuntu 服务器、检查 Cloudflare DNS/SSL、诊断 api.eastart.asia、Caddy 自动 HTTPS、反向代理、525/522 源站证书错误、New API 中转站配置、请求参数兼容、原生 LiteLLM 服务器代理、NVIDIA NIM 多账号路由、模型增删、429/冷却、embedding/chat 区分，以及 InchHeart API 服务可达性。"
---

# InchHeart Cloud

## Overview

Use this skill when the user asks about InchHeart cloud infrastructure, the `eastart.asia` domain, the GCP server, Caddy, Cloudflare proxy/SSL, native New API, or the server-side LiteLLM proxy.

Read only the reference needed for the task:

| Task | Read |
| --- | --- |
| Connect to the GCP server, diagnose DNS/Cloudflare/Caddy/SSH, or check service reachability | `references/server-access.md` |
| Work on New API channels, groups, registration defaults, logo/SMTP, model lists, request passthrough, or non-image model compatibility | `references/new-api.md` |
| Work on server LiteLLM, NVIDIA NIM keys/routes, model add/remove, Copilot compatibility callbacks, 429/cooldown, embeddings, VS Code model lists, or `/v1/models` | `references/litellm-native.md` |
| Need the full historical server snapshot or incident notes | `references/servers.md` |

Treat `inchheart-cloud` as the primary skill for the current server-side LiteLLM. Do not modify old Mac local LiteLLM files unless the user explicitly asks about local LiteLLM.

## Safety

- Do not expose private key contents, tokens, Cloudflare credentials, or service secrets.
- It is acceptable to show private key paths and SSH command syntax.
- Prefer read-only checks first: `systemctl status`, `journalctl`, `dig`, `curl`, `ss`.
- Before changing Cloudflare DNS, SSL mode, firewall rules, Caddyfile, or service processes, explain the exact change and why it is needed.
- Avoid destructive server commands unless the user explicitly asks.

## Connection Workflow

1. Read `references/server-access.md`.
2. Confirm which host/domain the user means.
3. If SSH is needed, use the recorded key path and `IdentitiesOnly=yes`.
4. For a passphrase-protected SSH key, prefer an interactive login first. Do not treat a `BatchMode=yes` failure as proof that the key is wrong, because it can fail before the user enters the passphrase.
5. If repeated non-interactive checks are needed, ask the user to preload the key into `ssh-agent` first:

```bash
ssh-add --apple-use-keychain ~/.ssh/gcp_sub2api
```

6. First-login command pattern:

```bash
ssh -i ~/.ssh/gcp_sub2api -o IdentitiesOnly=yes haiqiaoltd@35.212.249.116
```

7. After connecting, capture the current state before editing:

```bash
hostname
date -u
ip -brief addr
sudo systemctl status caddy --no-pager -l
sudo journalctl -u caddy -n 120 --no-pager
sudo ss -lntp
```

## DNS and HTTPS Workflow

For `api.eastart.asia`, separate DNS, Cloudflare proxying, Caddy ACME, and backend reachability:

1. Check DNS resolution:

```bash
dig +short api.eastart.asia A
dig +short api.eastart.asia AAAA
dig @1.1.1.1 +short api.eastart.asia A
dig @8.8.8.8 +short api.eastart.asia A
```

2. If Caddy needs to obtain a public certificate, keep the Cloudflare DNS record as DNS-only until HTTPS works directly at the origin.
3. When origin HTTPS works, Cloudflare can proxy the record and SSL/TLS mode should be `Full (strict)`.
4. Do not use Cloudflare `Flexible` mode for this API.
5. Diagnose Cloudflare errors by layer:

| Error | Likely layer | First checks |
|---|---|---|
| 522 | Cloudflare cannot reach origin | DNS target, firewall, Caddy listening on 80/443 |
| 525 | Cloudflare to origin TLS handshake failed | Caddy certificate, SSL mode, origin HTTPS |
| ACME unauthorized with `2606:4700...` | Let's Encrypt hit Cloudflare, not origin | Set `api` record to DNS-only while issuing |
| Browser works but CLI resolves `198.18.*` | Local proxy/VPN DNS interception | Check from server and public resolvers |

## Caddy Checks

Use this bundle first:

```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo sed -n '1,220p' /etc/caddy/Caddyfile
sudo systemctl status caddy --no-pager -l
sudo journalctl -u caddy -n 120 --no-pager
sudo ss -lntp | grep -E ':(80|443|8090|4000)\b' || true
```

Expected minimal site pattern:

```caddyfile
api.eastart.asia {
    reverse_proxy 127.0.0.1:8090
}
```

The current known backend is the native `new-api-native.service` listening on `127.0.0.1:8090` / `*:8090`. Verify with `ss -lntp` and `references/servers.md` before editing the reverse proxy target.

## Native Service Checks

The current low-memory GCP deployment intentionally avoids Docker for New API and LiteLLM. Prefer these checks before any restart:

```bash
systemctl is-active new-api-native litellm-native caddy
systemctl is-enabled new-api-native litellm-native caddy
sudo systemctl status new-api-native litellm-native caddy --no-pager -l
sudo ss -lntp | grep -E ':(80|443|8090|4000)\b' || true
curl -sSI --max-time 8 http://127.0.0.1:8090/ | grep -i 'HTTP/\|X-New-Api-Version'
curl -sS --max-time 10 http://127.0.0.1:4000/v1/models | jq '{count:(.data|length), models:[.data[].id]}'
curl -sSI --max-time 20 https://api.eastart.asia/ | grep -i 'HTTP/\|X-New-Api-Version\|server'
```

Docker should normally be inactive and disabled on this machine:

```bash
systemctl is-active docker.socket docker.service containerd.service 2>/dev/null || true
systemctl is-enabled docker.socket docker.service containerd.service 2>/dev/null || true
```

Do not restart the old `/opt/litellm-nvidia` Docker Compose stack. A LiteLLM Docker attempt, even reduced to 10 NVIDIA deployments, made SSH and New API unresponsive on this free-tier host.

## Service Boundaries

- Server LiteLLM lives in `/opt/litellm-native` and is the source of truth for upstream NVIDIA routing.
- New API lives in `/opt/new-api-native` and is treated as the public model configuration and token site for `api.eastart.asia`.
- Do not update New API channel model lists or `channels.models` automatically unless the user explicitly asks; the user often maintains those manually.
- Do not modify the old Mac local LiteLLM unless the user explicitly asks for local LiteLLM work.

## User Guidance Style

When guiding the user through a live console:

- Give one small command batch at a time.
- Explain what result to look for.
- Treat screenshots as current state and update the diagnosis from the latest evidence.
- If the user reports "it opens now", move to the next layer: Cloudflare proxy, SSL mode, and final browser/curl verification.
