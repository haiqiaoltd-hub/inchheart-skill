# Server Access

Use this reference for connecting to the GCP server, diagnosing `api.eastart.asia`, checking Cloudflare/Caddy, or verifying native service reachability.

## Server Map

| Field | Value |
| --- | --- |
| Provider | Google Cloud Platform |
| Public IPv4 | `35.212.249.116` |
| SSH user | `haiqiaoltd` |
| SSH key path | `~/.ssh/gcp_sub2api` |
| Hostname observed | `instance-20260528-100419` |
| Domain | `api.eastart.asia` |
| Reverse proxy | Caddy |
| New API service | `new-api-native.service` on `127.0.0.1:8090` / `*:8090` |
| LiteLLM service | `litellm-native.service` on `127.0.0.1:4000` |
| Docker state | Disabled/inactive after native migration |

SSH command:

```bash
ssh -i ~/.ssh/gcp_sub2api -o IdentitiesOnly=yes haiqiaoltd@35.212.249.116
```

The key is passphrase-protected. A `BatchMode=yes` failure can happen before passphrase entry and is not proof that the key is invalid.

For repeated non-interactive checks, ask the user to preload the key:

```bash
ssh-add --apple-use-keychain ~/.ssh/gcp_sub2api
```

## First Checks

Run read-only checks before editing:

```bash
hostname
date -u
systemctl is-active new-api-native litellm-native caddy
systemctl is-enabled new-api-native litellm-native caddy
sudo ss -lntp | grep -E ':(80|443|8090|4000)\b' || true
curl -sSI --max-time 8 http://127.0.0.1:8090/ | grep -i 'HTTP/\|X-New-Api-Version'
curl -sS --max-time 10 http://127.0.0.1:4000/v1/models | jq '{count:(.data|length), models:[.data[].id]}'
curl -sSI --max-time 20 https://api.eastart.asia/ | grep -i 'HTTP/\|X-New-Api-Version\|server'
```

## DNS And HTTPS

Check DNS from public resolvers:

```bash
dig +short api.eastart.asia A
dig +short api.eastart.asia AAAA
dig @1.1.1.1 +short api.eastart.asia A
dig @8.8.8.8 +short api.eastart.asia A
```

Known good final state:

```text
api.eastart.asia A 35.212.249.116 proxied
api.eastart.asia AAAA empty
Cloudflare SSL/TLS mode: Full (strict)
```

When Caddy needs to issue or renew a public certificate and ACME is failing through Cloudflare, set `api.eastart.asia` DNS-only until origin HTTPS works, then enable proxying again.

## Caddy

Expected Caddyfile shape:

```caddyfile
api.eastart.asia {
    reverse_proxy 127.0.0.1:8090
}
```

Validate before restart:

```bash
sudo caddy validate --config /etc/caddy/Caddyfile
sudo sed -n '1,220p' /etc/caddy/Caddyfile
sudo systemctl status caddy --no-pager -l
sudo journalctl -u caddy -n 120 --no-pager
```

## Safety

Do not print private key contents, Cloudflare credentials, New API secrets, LiteLLM keys, or raw environment files. It is safe to show service names, public IPs, domains, ports, and secret file paths.

Do not restart the old `/opt/litellm-nvidia` Docker Compose stack. That Docker stack previously made the free-tier host sluggish/unresponsive.
