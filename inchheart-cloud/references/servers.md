# InchHeart Cloud Server Reference

Last updated: 2026-06-22.

This file records operational facts that are safe to store. It intentionally excludes private key contents, Cloudflare credentials, API keys, and application secrets.

## Primary GCP API Server

Purpose: Origin server for `api.eastart.asia`.

Known facts:

| Field | Value |
|---|---|
| Provider | Google Cloud Platform |
| Public IPv4 | `35.212.249.116` |
| SSH user | `haiqiaoltd` |
| SSH key path | `~/.ssh/gcp_sub2api` |
| OS observed | Ubuntu 24.04.4 LTS |
| Kernel observed | Linux 6.17.0-1016-gcp x86_64 |
| Internal IPv4 observed | `10.138.0.2` on `ens4` |
| Hostname observed | `instance-20260528-100419` |
| Primary reverse proxy | Caddy |
| Primary domain | `api.eastart.asia` |
| New API deploy path | `/opt/new-api-native` |
| New API service | `new-api-native.service` |
| New API public origin port | `127.0.0.1:8090` / `*:8090` |
| LiteLLM deploy path | `/opt/litellm-native` |
| LiteLLM service | `litellm-native.service` |
| LiteLLM local port | `127.0.0.1:4000` |
| Docker state | Disabled and inactive after native migration |

SSH command:

```bash
ssh -i ~/.ssh/gcp_sub2api -o IdentitiesOnly=yes haiqiaoltd@35.212.249.116
```

Authentication note:

- This key is passphrase-protected.
- A non-interactive probe such as `ssh -o BatchMode=yes ...` can fail before passphrase entry and should not be treated as proof that the server rejected the key.
- When automation or repeated checks are needed on this Mac, preload the key first:

```bash
ssh-add --apple-use-keychain ~/.ssh/gcp_sub2api
```

- A successful interactive login was observed on 2026-06-16 from source IP `45.192.200.74`.

Known SSH host key fingerprint observed:

```text
ED25519 SHA256:q+BJNrNuOJ0IFtYmb1DHzzspVg5BNeZTrEBAALFyZHk
```

The same host key was previously known for:

```text
35.212.247.82
```

Treat host key continuity as useful context, not as proof of current infrastructure intent. Re-check with the user if the IP changes unexpectedly.

## Cloudflare DNS

Current domain: `eastart.asia`.

Known records from the 2026-06-15 migration:

| Name | Type | Content | Proxy |
|---|---|---|---|
| `api.eastart.asia` | A | `35.212.249.116` | Proxied after origin HTTPS succeeded |
| `hk.eastart.asia` | A | `35.215.159.235` | DNS only |
| `send.eastart.asia` | MX | `feedback-smtp.ap-northeast-1.amazonses.com` | DNS only |
| `_dmarc.eastart.asia` | TXT | `v=DMARC1; p=none;` | DNS only |
| `send.eastart.asia` | TXT | `v=spf1 include:amazonses.com ~all` | DNS only |
| `resend._domainkey.eastart.asia` | TXT | DKIM value redacted/truncated in screenshots | DNS only |

For `api.eastart.asia`, the known good final state is:

```text
api.eastart.asia A 35.212.249.116 proxied
api.eastart.asia AAAA empty
Cloudflare SSL/TLS mode: Full (strict)
```

During Caddy/Let's Encrypt certificate issuance, temporarily use DNS-only for `api.eastart.asia`; after `https://api.eastart.asia/` works at the origin, enable proxying again.

## Caddy and HTTPS Incident Pattern

On 2026-06-15, Caddy could not obtain a certificate while Cloudflare proxying was enabled.

Log symptoms:

```text
Cannot negotiate ALPN protocol "acme-tls/1" for tls-alpn-01 challenge
Invalid response from https://api.eastart.asia/.well-known/acme-challenge/...
2606:4700:... Invalid response
```

Interpretation:

- `2606:4700:*` is Cloudflare IPv6.
- Let's Encrypt reached Cloudflare instead of the GCP origin.
- HTTP-01/TLS-ALPN-01 validation failed until `api.eastart.asia` was set to DNS-only and AAAA records were absent.

Good DNS during issuance:

```bash
dig +short api.eastart.asia A
# 35.212.249.116

dig +short api.eastart.asia AAAA
# no output
```

After DNS-only was in place, Caddy was able to serve `https://api.eastart.asia/`; then Cloudflare proxying was re-enabled and SSL/TLS mode was set to `Full (strict)`.

## Standard Diagnostics

Run these from the server:

```bash
systemctl is-active new-api-native litellm-native caddy
systemctl is-enabled new-api-native litellm-native caddy
sudo systemctl status new-api-native litellm-native caddy --no-pager -l
sudo journalctl -u caddy -n 120 --no-pager
sudo caddy validate --config /etc/caddy/Caddyfile
sudo sed -n '1,220p' /etc/caddy/Caddyfile
sudo ss -lntp | grep -E ':(80|443|8090|4000)\b' || true
curl -sSI --max-time 8 http://127.0.0.1:8090/ | grep -i 'HTTP/\|X-New-Api-Version'
curl -sS --max-time 10 http://127.0.0.1:4000/v1/models | jq '{count:(.data|length), models:[.data[].id]}'
curl -I http://api.eastart.asia
curl -I https://api.eastart.asia
```

Run these from any machine with normal public DNS:

```bash
dig +short api.eastart.asia A
dig +short api.eastart.asia AAAA
dig @1.1.1.1 +short api.eastart.asia A
dig @8.8.8.8 +short api.eastart.asia A
```

If local DNS returns `198.18.*`, suspect local proxy/VPN interception. Prefer server-side `dig`, public resolvers, and browser tests in a clean profile.

## Caddyfile Shape

Current known domain block:

```caddyfile
api.eastart.asia {
    reverse_proxy 127.0.0.1:8090
}
```

Verify the backend port before changing this.

## Native New API Deployment

Current deployment after the 2026-06-22 low-memory migration:

```text
/opt/new-api-native/new-api
/opt/new-api-native/data/one-api.db
/opt/new-api-native/logs
/etc/new-api-native.env
/etc/systemd/system/new-api-native.service
```

The service is intentionally native, not Docker:

| Field | Value |
|---|---|
| Binary source | Copied from the known-good `calciumion/new-api:latest` container image |
| Version observed | `v1.0.0-rc.14` |
| Service user | `newapi` |
| Listen port | `8090` |
| Database | SQLite at `/opt/new-api-native/data/one-api.db` |
| Redis | Disabled |
| PostgreSQL | Disabled |

Useful checks:

```bash
sudo systemctl status new-api-native --no-pager -l
sudo journalctl -u new-api-native -n 120 --no-pager
curl -sSI --max-time 8 http://127.0.0.1:8090/ | grep -i 'HTTP/\|X-New-Api-Version'
sudo ls -lh /opt/new-api-native/data/one-api.db
```

Secret handling:

```text
SESSION_SECRET is stored in /etc/new-api-native.env. Do not print it.
```

## Native LiteLLM Deployment

Current deployment after the 2026-06-22 low-memory migration:

```text
/opt/litellm-native/venv
/opt/litellm-native/config.yaml
/opt/litellm-native/logs
/etc/litellm-native.env
/etc/systemd/system/litellm-native.service
```

The service is intentionally native, not Docker:

| Field | Value |
|---|---|
| Service user | `litellm` |
| Listen port | `127.0.0.1:4000` |
| Python environment | `/opt/litellm-native/venv` |
| LiteLLM version installed | `1.89.3` |
| NVIDIA endpoint | `https://integrate.api.nvidia.com/v1` |
| Exposed models | `z-ai/glm-5.1`, `stepfun-ai/step-3.7-flash`, `minimaxai/minimax-m3`, `moonshotai/kimi-k2.6`, `deepseek-ai/deepseek-v4-pro` |
| Deployments | 50 total, 10 NVIDIA API keys per model group |
| Per-deployment limit | `rpm: 20` |
| Router cooldown | `cooldown_time: 3600` |

Useful checks:

```bash
sudo systemctl status litellm-native --no-pager -l
sudo journalctl -u litellm-native -n 120 --no-pager
curl -sS --max-time 10 http://127.0.0.1:4000/v1/models | jq '{count:(.data|length), models:[.data[].id]}'
curl -sS --max-time 70 http://127.0.0.1:4000/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -d '{"model":"z-ai/glm-5.1","messages":[{"role":"user","content":"Reply OK only."}],"max_tokens":8,"stream":false}' \
  | jq '{id, model, content:(.choices[0].message.content // null), error:(.error // null)}'
```

Secret handling:

```text
NVIDIA_API_KEY_1 ... NVIDIA_API_KEY_10 are stored in /etc/litellm-native.env. Do not print them.
```

New API channel configuration for this local LiteLLM proxy:

| Field | Value |
|---|---|
| Base URL in New API UI | `http://127.0.0.1:4000` |
| Effective OpenAI-compatible API root | `http://127.0.0.1:4000/v1` |
| Models | `z-ai/glm-5.1`, `stepfun-ai/step-3.7-flash`, `minimaxai/minimax-m3`, `moonshotai/kimi-k2.6`, `deepseek-ai/deepseek-v4-pro` |
| Key | LiteLLM currently has no master key; use a placeholder only if New API requires a value |

## Docker Migration Note

On 2026-06-22, the server was migrated away from Docker because this free-tier host was too memory-constrained for the container stack.

Observed failure pattern:

| Attempt | Result |
|---|---|
| New API + PostgreSQL + Redis in Docker | Worked, but consumed avoidable memory |
| LiteLLM Docker with 180 NVIDIA deployments | Started poorly; `/health` and `/v1/models` reset; SSH/Caddy became sluggish |
| LiteLLM Docker reduced to `z-ai/glm-5.1` with 10 deployments | Still made SSH and New API unresponsive |

Recovery pattern used successfully:

```bash
#!/bin/bash
cd /opt/litellm-nvidia || exit 0
docker compose stop litellm-nvidia || true
docker stop litellm-nvidia || true
docker update --restart=no litellm-nvidia || true
```

This rescue script was temporarily added through the GCP startup script field, then removed after the machine recovered.

Current Docker expectation:

```bash
systemctl is-active docker.socket docker.service containerd.service 2>/dev/null || true
systemctl is-enabled docker.socket docker.service containerd.service 2>/dev/null || true
```

Expected output is inactive/disabled. Do not restart the old `/opt/litellm-nvidia` Docker Compose stack on this machine.

The native migration also added a 1 GB swapfile:

```bash
swapon --show
free -h
```

## New API Settings Snapshot

Observed after native SQLite initialization on 2026-06-22:

```text
New API version: v1.0.0-rc.14
Database: SQLite
Redis: disabled
System initialization: fresh native database; previous Docker/PostgreSQL data was not migrated because the user said the New API instance was effectively empty.
```

Do not query or print `channels.key`, `tokens.key`, `users.password`, `users.access_token`, `SESSION_SECRET`, NVIDIA keys, or secret-bearing environment variables unless the user explicitly asks and the output is redacted.
