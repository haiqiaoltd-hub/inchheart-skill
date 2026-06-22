# Local Files And Commands

## Current Service Shape

The local proxy is a LaunchAgent-managed LiteLLM service:

```text
VS Code Copilot / Claude / CLI
  -> http://127.0.0.1:4000/v1...
  -> LiteLLM local proxy
  -> upstream provider
```

Primary paths:

| Path | Meaning |
| --- | --- |
| `/Users/mac/litellm_config.yaml` | Model deployments and provider keys by environment variable |
| `/Users/mac/start-litellm-nvidia.sh` | Loads YAML environment variables and starts LiteLLM |
| `/Users/mac/copilot_compat_callbacks.py` | Compatibility callback |
| `/Users/mac/Library/LaunchAgents/com.inchheart.litellm-nvidia.plist` | Service definition |
| `/Users/mac/Library/Application Support/Code/User/chatLanguageModels.json` | VS Code Copilot custom models |
| `/Users/mac/litellm.log` | Normal LiteLLM log |
| `/Users/mac/litellm.err.log` | Error log |

## Safe Inspection

Avoid printing raw keys. Prefer summaries:

```bash
python3 - <<'PY'
from pathlib import Path
import yaml
data = yaml.safe_load(Path('/Users/mac/litellm_config.yaml').read_text())
models = data.get('model_list', [])
print('deployments:', len(models))
print('visible_model_names:', len({m.get('model_name') for m in models}))
print('env_names:', sorted((data.get('environment_variables') or {}).keys()))
PY
```

Check service:

```bash
launchctl print "gui/$(id -u)/com.inchheart.litellm-nvidia" | rg "state =|pid =|last exit code"
curl -sS http://127.0.0.1:4000/v1/models | jq '{count:(.data|length), models:[.data[].id]}'
```

Check VS Code custom models without secrets:

```bash
python3 - <<'PY'
from pathlib import Path
import json
p = Path('/Users/mac/Library/Application Support/Code/User/chatLanguageModels.json')
for provider in json.loads(p.read_text()):
    print(provider.get('name'), provider.get('apiType'), len(provider.get('models', [])))
    for m in provider.get('models', []):
        print(' ', {k: m.get(k) for k in ['id','url','maxInputTokens','maxOutputTokens','toolCalling','vision']})
PY
```

## Restart

```bash
python3 -m py_compile /Users/mac/copilot_compat_callbacks.py
zsh -n /Users/mac/start-litellm-nvidia.sh
launchctl kickstart -k "gui/$(id -u)/com.inchheart.litellm-nvidia"
sleep 8
curl -sS http://127.0.0.1:4000/v1/models | jq '{count:(.data|length)}'
```

The port often needs several seconds after LaunchAgent restart; retry before assuming failure.

