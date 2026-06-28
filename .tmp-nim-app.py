from __future__ import annotations

import asyncio
import hashlib
import json
import os
import random
import re
import time
from pathlib import Path
from typing import Any, AsyncIterator

import httpx
import yaml
from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse


NVIDIA_BASE_URL = os.getenv("NIM_PROXY_NVIDIA_BASE_URL", "https://integrate.api.nvidia.com/v1")
CONFIG_PATH = Path(os.getenv("NIM_PROXY_CONFIG", "/opt/nim-copilot-proxy/config.yaml"))
ENV_PATH = Path(os.getenv("NIM_PROXY_ENV_FILE", "/etc/nim-copilot-proxy.env"))
HOST_MODEL_PREFIX = "openai/"
DEFAULT_MAX_TOKENS = int(os.getenv("NIM_PROXY_DEFAULT_MAX_TOKENS", "8192"))
REQUEST_TIMEOUT = float(os.getenv("NIM_PROXY_REQUEST_TIMEOUT", "180"))
CONNECT_TIMEOUT = float(os.getenv("NIM_PROXY_CONNECT_TIMEOUT", "20"))
COOLDOWN_SECONDS = int(os.getenv("NIM_PROXY_KEY_COOLDOWN_SECONDS", "3600"))
MAX_UPSTREAM_ATTEMPTS = int(os.getenv("NIM_PROXY_MAX_UPSTREAM_ATTEMPTS", "4"))
KEY_SELECTION = os.getenv("NIM_PROXY_KEY_SELECTION", "affinity").lower()


app = FastAPI(title="NVIDIA NIM Copilot Proxy", version="0.1.0")
_cooldowns: dict[tuple[str, int], float] = {}
_cooldowns_lock = asyncio.Lock()


def _load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def _load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _load_state() -> tuple[dict[str, str], list[str], str | None]:
    env = _load_env(ENV_PATH)
    config = _load_config(CONFIG_PATH)
    models: dict[str, str] = {}
    for item in config.get("model_list", []) or []:
        model_name = item.get("model_name")
        params = item.get("litellm_params") or {}
        upstream = params.get("model") or model_name
        if isinstance(upstream, str) and upstream.startswith(HOST_MODEL_PREFIX):
            upstream = upstream[len(HOST_MODEL_PREFIX):]
        if isinstance(model_name, str) and isinstance(upstream, str):
            models.setdefault(model_name, upstream)
            models.setdefault(upstream, upstream)
            short = upstream.split("/")[-1]
            models.setdefault(short, upstream)

    keys: list[str] = []
    for name in ["NVIDIA_API_KEY", *[f"NVIDIA_API_KEY_{i}" for i in range(1, 101)]]:
        value = env.get(name)
        if value and value not in keys:
            keys.append(value)

    master_key = (config.get("general_settings") or {}).get("master_key")
    if not isinstance(master_key, str) or not master_key:
        master_key = os.getenv("NIM_PROXY_MASTER_KEY")
    return models, keys, master_key


MODEL_MAP, NVIDIA_KEYS, MASTER_KEY = _load_state()


def _model_id(model: str) -> str:
    return MODEL_MAP.get(model, model)


def _short_model(model: str) -> str:
    return model.split("/")[-1]


def _pattern(model: str, name: str) -> bool:
    return bool(re.search(rf"(^|[/_-]){re.escape(name)}([/_-]|$)", model, re.I))


def _is_kimi(model: str) -> bool:
    return _pattern(model, "kimi")


def _is_deepseek(model: str) -> bool:
    return _pattern(model, "deepseek")


def _is_glm(model: str) -> bool:
    return _pattern(model, "glm")


def _has_tools(body: dict[str, Any]) -> bool:
    return isinstance(body.get("tools"), list) and bool(body["tools"])


def _has_tool_history(body: dict[str, Any]) -> bool:
    messages = body.get("messages")
    if not isinstance(messages, list):
        return False
    for msg in messages:
        if not isinstance(msg, dict):
            continue
        if msg.get("role") == "tool" or msg.get("tool_calls"):
            return True
    return False


def _sanitize_tools(body: dict[str, Any]) -> None:
    tools = body.get("tools")
    if not isinstance(tools, list):
        return
    cleaned = []
    for tool in tools:
        if not isinstance(tool, dict) or tool.get("type") != "function":
            continue
        fn = tool.get("function")
        if not isinstance(fn, dict):
            continue
        if fn.get("description") is None:
            fn["description"] = ""
        elif not isinstance(fn.get("description"), str):
            fn["description"] = str(fn.get("description"))
        params = fn.get("parameters")
        if params is None:
            fn["parameters"] = {"type": "object", "properties": {}}
        elif isinstance(params, dict) and "type" not in params:
            params["type"] = "object"
        cleaned.append(tool)
    if cleaned:
        body["tools"] = cleaned
    else:
        body.pop("tools", None)


def _prepend_system(body: dict[str, Any], text: str) -> None:
    messages = body.get("messages")
    if not isinstance(messages, list):
        return
    if messages and isinstance(messages[0], dict) and messages[0].get("role") == "system":
        current = messages[0].get("content") or ""
        if isinstance(current, str) and text not in current:
            messages[0]["content"] = f"{text}\n\n{current}" if current else text
        return
    messages.insert(0, {"role": "system", "content": text})


def _tool_prompt(model: str) -> str | None:
    if _is_kimi(model):
        return (
            "You are an expert AI programming assistant. Provide correct, concise, production-ready code. "
            "When tools are available, answer with concise user-facing text or a native tool call. "
            "Only emit tool calls through the designated tool_calls field; never write JSON arguments inline "
            "as markdown, backtick fences, or plain text. Every tool call must include ALL required arguments "
            "with correct types. Do not reveal chain-of-thought, reasoning scratchpads, or internal reasoning markers."
        )
    if _is_deepseek(model):
        return (
            "You are an expert AI programming assistant. Use native tool_calls only. "
            "Do not emit inline tool markers, JSON fences, planning text, or protocol tokens."
        )
    if _is_glm(model):
        return (
            "You are an expert AI programming assistant. When calling tools, emit strict JSON arguments only. "
            "Do not wrap tool arguments in markdown fences, backticks, or explanatory prose."
        )
    return None


def _apply_model_defaults(body: dict[str, Any], model: str) -> None:
    if body.get("max_tokens") in (None, 0):
        body["max_tokens"] = DEFAULT_MAX_TOKENS

    if "temperature" not in body:
        if _is_deepseek(model):
            body["temperature"] = 0.0
        elif _is_glm(model):
            body["temperature"] = 0.05 if _has_tools(body) else 0.1
        elif _is_kimi(model):
            body["temperature"] = 0.1 if _has_tools(body) else 0.2
        elif _pattern(model, "qwen"):
            body["temperature"] = 0.05 if _has_tools(body) else 0.1
        else:
            body["temperature"] = 0.2 if _has_tools(body) else 0.3

    if _is_kimi(model):
        body["enable_thinking"] = False

    if (_is_kimi(model) or _is_deepseek(model) or _is_glm(model)) and isinstance(body.get("messages"), list):
        for msg in body["messages"]:
            if isinstance(msg, dict) and msg.get("role") == "assistant" and "reasoning_content" not in msg:
                msg["reasoning_content"] = " "

    prompt = _tool_prompt(model)
    if prompt and _has_tools(body):
        _prepend_system(body, prompt)


def _prepare_body(body: dict[str, Any]) -> dict[str, Any]:
    prepared = json.loads(json.dumps(body))
    model = _model_id(str(prepared.get("model") or ""))
    prepared["model"] = model
    if prepared.get("stream") is True:
        prepared["stream_options"] = {"include_usage": False}
    _sanitize_tools(prepared)
    _apply_model_defaults(prepared, model)
    return prepared


def _normalize_choice(choice: dict[str, Any]) -> dict[str, Any]:
    for key in ("message", "delta"):
        part = choice.get(key)
        if not isinstance(part, dict):
            continue
        if part.get("tool_calls") == []:
            part.pop("tool_calls", None)
        content = part.get("content")
        reasoning = part.get("reasoning_content") or part.get("reasoning")
        if (content is None or content == "") and isinstance(reasoning, str) and reasoning:
            part["content"] = reasoning
        if key == "delta" and "reasoning_content" in part and "content" in part:
            part.pop("reasoning_content", None)
    finish = choice.get("finish_reason")
    if finish in ("length", "repetition") or (finish is not None and finish not in {"stop", "tool_calls", "content_filter", "function_call"}):
        choice["finish_reason"] = "stop"
    if choice.get("stop_reason") == "repetition_detected" and choice.get("finish_reason") is None:
        choice["finish_reason"] = "stop"
    return choice


def _has_valid_choices(data: dict[str, Any]) -> bool:
    choices = data.get("choices")
    return isinstance(choices, list) and any(isinstance(choice, dict) for choice in choices)


def _request_affinity(body: dict[str, Any]) -> str:
    model = str(body.get("model") or "")
    messages = body.get("messages")
    stable_messages: list[dict[str, Any]] = []
    if isinstance(messages, list):
        for msg in messages:
            if not isinstance(msg, dict):
                continue
            role = msg.get("role")
            if role in {"system", "developer"}:
                stable_messages.append({
                    "role": role,
                    "content": msg.get("content"),
                })
            if len(stable_messages) >= 4:
                break

    tools = body.get("tools")
    stable_tools: list[str] = []
    if isinstance(tools, list):
        for tool in tools:
            if not isinstance(tool, dict):
                continue
            fn = tool.get("function")
            if isinstance(fn, dict) and isinstance(fn.get("name"), str):
                stable_tools.append(fn["name"])

    payload = {
        "model": model,
        "messages": stable_messages,
        "tools": sorted(stable_tools),
    }
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _normalize_response(data: dict[str, Any]) -> dict[str, Any]:
    for choice in data.get("choices") or []:
        if isinstance(choice, dict):
            _normalize_choice(choice)
    return data


def _auth_ok(authorization: str | None) -> bool:
    if not MASTER_KEY:
        return True
    if not authorization:
        return False
    scheme, _, token = authorization.partition(" ")
    return scheme.lower() == "bearer" and token == MASTER_KEY


async def _choose_key(model: str, affinity: str | None = None, exclude: set[int] | None = None) -> tuple[int, str]:
    if not NVIDIA_KEYS:
        raise HTTPException(status_code=500, detail="No NVIDIA API keys configured")
    now = time.time()
    exclude = exclude or set()
    async with _cooldowns_lock:
        live = [
            (idx, key)
            for idx, key in enumerate(NVIDIA_KEYS)
            if idx not in exclude and _cooldowns.get((model, idx), 0) <= now
        ]
    if not live:
        live = [(idx, key) for idx, key in enumerate(NVIDIA_KEYS) if idx not in exclude]
    if not live:
        live = list(enumerate(NVIDIA_KEYS))
    if KEY_SELECTION == "random" or not affinity:
        return random.choice(live)
    digest = hashlib.sha256(f"{model}\n{affinity}".encode("utf-8")).digest()
    return live[int.from_bytes(digest[:8], "big") % len(live)]


async def _cooldown_key(model: str, idx: int) -> None:
    async with _cooldowns_lock:
        _cooldowns[(model, idx)] = time.time() + COOLDOWN_SECONDS


async def _post_upstream_json(body: dict[str, Any]) -> dict[str, Any]:
    model = str(body["model"])
    affinity = _request_affinity(body)
    last_error: Exception | None = None
    attempted: set[int] = set()
    for _ in range(min(MAX_UPSTREAM_ATTEMPTS, max(1, len(NVIDIA_KEYS)))):
        idx, key = await _choose_key(model, affinity, attempted)
        if idx in attempted and len(attempted) < len(NVIDIA_KEYS):
            continue
        attempted.add(idx)
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(REQUEST_TIMEOUT, connect=CONNECT_TIMEOUT)) as client:
                res = await client.post(
                    f"{NVIDIA_BASE_URL}/chat/completions",
                    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
                    json=body,
                )
            if res.status_code in {429, 500, 502, 503, 504}:
                await _cooldown_key(model, idx)
                last_error = HTTPException(status_code=res.status_code, detail=res.text[:500])
                continue
            if res.status_code >= 400:
                raise HTTPException(status_code=res.status_code, detail=res.text[:1000])
            data = _normalize_response(res.json())
            if _has_valid_choices(data):
                return data
            last_error = HTTPException(status_code=502, detail="Upstream response contained no choices")
            await _cooldown_key(model, idx)
            continue
        except HTTPException:
            raise
        except Exception as exc:
            await _cooldown_key(model, idx)
            last_error = exc
    if isinstance(last_error, HTTPException):
        raise last_error
    raise HTTPException(status_code=502, detail=str(last_error or "Upstream request failed"))


def _sse(data: dict[str, Any] | str) -> bytes:
    if isinstance(data, str):
        payload = data
    else:
        payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return f"data: {payload}\n\n".encode("utf-8")


def _synthetic_stream(data: dict[str, Any]) -> AsyncIterator[bytes]:
    async def gen() -> AsyncIterator[bytes]:
        response_id = data.get("id") or f"chatcmpl-proxy-{int(time.time() * 1000)}"
        created = data.get("created") or int(time.time())
        model = data.get("model")
        yield _sse({
            "id": response_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": model,
            "choices": [{"index": 0, "delta": {"role": "assistant"}}],
        })
        choice = (data.get("choices") or [{}])[0]
        msg = choice.get("message") or {}
        content = msg.get("content")
        tool_calls = msg.get("tool_calls")
        if isinstance(content, str) and content:
            yield _sse({
                "id": response_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": model,
                "choices": [{"index": 0, "delta": {"content": content}}],
            })
        if tool_calls:
            yield _sse({
                "id": response_id,
                "object": "chat.completion.chunk",
                "created": created,
                "model": model,
                "choices": [{"index": 0, "delta": {"tool_calls": tool_calls}}],
            })
        yield _sse({
            "id": response_id,
            "object": "chat.completion.chunk",
            "created": created,
            "model": model,
            "choices": [{"index": 0, "delta": {}, "finish_reason": choice.get("finish_reason") or "stop"}],
        })
        yield _sse("[DONE]")
    return gen()


def _chunk(
    response_id: str,
    created: int,
    model: str,
    delta: dict[str, Any],
    finish_reason: str | None = None,
) -> dict[str, Any]:
    choice: dict[str, Any] = {"index": 0, "delta": delta}
    if finish_reason is not None:
        choice["finish_reason"] = finish_reason
    return {
        "id": response_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": model,
        "choices": [choice],
    }


def _error_stream(model: str, message: str) -> AsyncIterator[bytes]:
    async def gen() -> AsyncIterator[bytes]:
        response_id = f"chatcmpl-proxy-error-{int(time.time() * 1000)}"
        created = int(time.time())
        yield _sse(_chunk(response_id, created, model, {"role": "assistant"}))
        yield _sse(_chunk(response_id, created, model, {"content": message}))
        yield _sse(_chunk(response_id, created, model, {}, "stop"))
        yield _sse("[DONE]")
    return gen()


async def _stream_upstream(body: dict[str, Any]) -> AsyncIterator[bytes]:
    model = str(body["model"])
    affinity = _request_affinity(body)
    attempted: set[int] = set()
    last_error = "Upstream request failed"
    max_attempts = min(MAX_UPSTREAM_ATTEMPTS, max(1, len(NVIDIA_KEYS)))
    retry_statuses = {429, 500, 502, 503, 504}

    for _ in range(max_attempts):
        idx, key = await _choose_key(model, affinity, attempted)
        attempted.add(idx)
        headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json", "Accept": "text/event-stream"}
        timeout = httpx.Timeout(REQUEST_TIMEOUT, connect=CONNECT_TIMEOUT)
        yielded_any = False
        previous_content_by_index: dict[int, str] = {}
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                async with client.stream("POST", f"{NVIDIA_BASE_URL}/chat/completions", headers=headers, json=body) as res:
                    if res.status_code in retry_statuses:
                        await _cooldown_key(model, idx)
                        last_error = (await res.aread()).decode("utf-8", "ignore")[:500] or f"HTTP {res.status_code}"
                        if not yielded_any:
                            continue
                    if res.status_code >= 400:
                        last_error = (await res.aread()).decode("utf-8", "ignore")[:1000] or f"HTTP {res.status_code}"
                        break
                    buffer = ""
                    async for text in res.aiter_text():
                        buffer += text
                        while "\n\n" in buffer:
                            raw, buffer = buffer.split("\n\n", 1)
                            data_lines = [line[5:].strip() for line in raw.splitlines() if line.startswith("data:")]
                            if not data_lines:
                                continue
                            payload = "".join(data_lines)
                            if payload == "[DONE]":
                                yield _sse("[DONE]")
                                return
                            try:
                                obj = json.loads(payload)
                            except json.JSONDecodeError:
                                continue
                            obj = _normalize_response(obj)
                            choices = obj.get("choices")
                            if not isinstance(choices, list) or not choices:
                                continue
                            filtered: list[dict[str, Any]] = []
                            for choice in choices:
                                if not isinstance(choice, dict):
                                    continue
                                delta = choice.get("delta")
                                if isinstance(delta, dict) and isinstance(delta.get("content"), str):
                                    choice_index = int(choice.get("index") or 0)
                                    content = delta["content"]
                                    previous = previous_content_by_index.get(choice_index, "")
                                    if previous and content.startswith(previous):
                                        delta["content"] = content[len(previous):]
                                    previous_content_by_index[choice_index] = content if content.startswith(previous) else previous + content
                                    if delta["content"] == "" and not delta.get("tool_calls") and choice.get("finish_reason") is None:
                                        continue
                                filtered.append(choice)
                            if not filtered:
                                continue
                            obj["choices"] = filtered
                            yielded_any = True
                            yield _sse(obj)
                    if yielded_any:
                        yield _sse("[DONE]")
                        return
        except Exception as exc:
            await _cooldown_key(model, idx)
            last_error = str(exc)
            if yielded_any:
                yield _sse(_chunk(f"chatcmpl-proxy-error-{int(time.time() * 1000)}", int(time.time()), model, {}, "stop"))
                yield _sse("[DONE]")
                return

    async for item in _error_stream(model, f"NVIDIA NIM upstream error: {last_error}"):
        yield item


@app.get("/health")
async def health() -> dict[str, Any]:
    return {"ok": True, "models": len({v for v in MODEL_MAP.values()}), "keys": len(NVIDIA_KEYS)}


@app.get("/v1/models")
async def models(authorization: str | None = Header(default=None)) -> JSONResponse:
    if not _auth_ok(authorization):
        raise HTTPException(status_code=401, detail="Unauthorized")
    unique = sorted({v for v in MODEL_MAP.values()})
    return JSONResponse({"object": "list", "data": [{"id": m, "object": "model", "owned_by": "nvidia"} for m in unique]})


@app.post("/v1/chat/completions")
async def chat_completions(request: Request, authorization: str | None = Header(default=None)):
    if not _auth_ok(authorization):
        raise HTTPException(status_code=401, detail="Unauthorized")
    body = await request.json()
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="Body must be a JSON object")
    prepared = _prepare_body(body)
    model = str(prepared["model"])
    wants_stream = bool(prepared.get("stream"))

    # Kimi's NVIDIA streaming tool path is unstable. Use non-stream upstream and
    # synthesize OpenAI SSE so Copilot still gets text/tool parts.
    should_buffer = wants_stream and _is_kimi(model) and (_has_tools(prepared) or _has_tool_history(prepared))
    if wants_stream and should_buffer:
        upstream_body = dict(prepared)
        upstream_body["stream"] = False
        upstream_body.pop("stream_options", None)
        data = await _post_upstream_json(upstream_body)
        return StreamingResponse(_synthetic_stream(data), media_type="text/event-stream")

    if wants_stream:
        return StreamingResponse(_stream_upstream(prepared), media_type="text/event-stream")

    prepared["stream"] = False
    return JSONResponse(await _post_upstream_json(prepared))
