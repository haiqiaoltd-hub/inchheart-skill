#!/usr/bin/env python3
import argparse
import json
import os
import ssl
import sys
import time
import socket
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


TARGETS = [
    {
        "provider": "deepseek-official",
        "base_url": "https://api.deepseek.com",
        "path": "/chat/completions",
        "env": "DEEPSEEK_API_KEY",
        "models": ["deepseek-v4-flash", "deepseek-v4-pro"],
    },
    {
        "provider": "nvidia-nim",
        "base_url": "https://integrate.api.nvidia.com",
        "path": "/v1/chat/completions",
        "env": "NVIDIA_API_KEY",
        "models": ["deepseek-ai/deepseek-v4-flash", "deepseek-ai/deepseek-v4-pro"],
    },
]


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe_name(value: str) -> str:
    return value.replace("/", "__").replace(":", "_")


def request_json(
    url: str,
    key: str,
    payload: dict[str, Any],
    timeout: int,
    context: ssl.SSLContext | None,
) -> tuple[int, dict[str, str], bytes]:
    req = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )
    try:
        with urlopen(req, timeout=timeout, context=context) as resp:
            return resp.status, dict(resp.headers.items()), resp.read()
    except HTTPError as exc:
        return exc.code, dict(exc.headers.items()), exc.read()
    except (TimeoutError, socket.timeout) as exc:
        return 0, {}, f"timeout: {exc}".encode("utf-8", "replace")
    except URLError as exc:
        return 0, {}, str(exc).encode("utf-8", "replace")


def request_stream(
    url: str,
    key: str,
    payload: dict[str, Any],
    timeout: int,
    context: ssl.SSLContext | None,
) -> tuple[int, dict[str, str], bytes, list[Any]]:
    req = Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        method="POST",
    )
    raw = bytearray()
    events: list[Any] = []
    try:
        with urlopen(req, timeout=timeout, context=context) as resp:
            headers = dict(resp.headers.items())
            while True:
                line = resp.readline()
                if not line:
                    break
                raw.extend(line)
                stripped = line.decode("utf-8", "replace").strip()
                if not stripped.startswith("data:"):
                    continue
                data = stripped[5:].strip()
                if data == "[DONE]":
                    events.append("[DONE]")
                    continue
                try:
                    events.append(json.loads(data))
                except json.JSONDecodeError:
                    events.append({"_parse_error": data})
            return resp.status, headers, bytes(raw), events
    except HTTPError as exc:
        body = exc.read()
        return exc.code, dict(exc.headers.items()), body, []
    except (TimeoutError, socket.timeout) as exc:
        return 0, {}, f"timeout: {exc}".encode("utf-8", "replace"), []
    except URLError as exc:
        return 0, {}, str(exc).encode("utf-8", "replace"), []


def summarize_nonstream(status: int, body: bytes) -> dict[str, Any]:
    text = body.decode("utf-8", "replace")
    summary: dict[str, Any] = {"status": status, "body_bytes": len(body)}
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        summary["json"] = False
        summary["text_head"] = text[:500]
        return summary

    summary["json"] = True
    summary["top_keys"] = sorted(data.keys()) if isinstance(data, dict) else None
    if isinstance(data, dict):
        choices = data.get("choices")
        summary["choices_len"] = len(choices) if isinstance(choices, list) else None
        if isinstance(choices, list) and choices:
            choice = choices[0]
            summary["choice_keys"] = sorted(choice.keys()) if isinstance(choice, dict) else None
            msg = choice.get("message") if isinstance(choice, dict) else None
            if isinstance(msg, dict):
                summary["message_keys"] = sorted(msg.keys())
                summary["message_content_len"] = len(msg.get("content") or "")
                summary["has_reasoning_content"] = "reasoning_content" in msg
                summary["has_tool_calls"] = "tool_calls" in msg
        usage = data.get("usage")
        summary["usage_keys"] = sorted(usage.keys()) if isinstance(usage, dict) else None
        if isinstance(data.get("error"), dict):
            summary["error_keys"] = sorted(data["error"].keys())
            summary["error_type"] = data["error"].get("type")
            summary["error_code"] = data["error"].get("code")
        elif "message" in data and "code" in data:
            summary["error_type"] = data.get("type")
            summary["error_code"] = data.get("code")
    return summary


def summarize_stream(status: int, raw: bytes, events: list[Any]) -> dict[str, Any]:
    summary: dict[str, Any] = {
        "status": status,
        "raw_bytes": len(raw),
        "events_len": len(events),
        "done_seen": any(event == "[DONE]" for event in events),
    }
    json_events = [event for event in events if isinstance(event, dict)]
    summary["json_events_len"] = len(json_events)
    empty_choices = 0
    content_chunks: list[str] = []
    reasoning_chunks: list[str] = []
    usage_chunks = 0
    finish_reasons: list[Any] = []
    delta_key_sets: list[list[str]] = []
    top_key_sets: list[list[str]] = []
    errors: list[Any] = []

    for event in json_events:
        top_key_sets.append(sorted(event.keys()))
        if isinstance(event.get("error"), dict):
            errors.append(event["error"])
        choices = event.get("choices")
        if isinstance(choices, list):
            if not choices:
                empty_choices += 1
            for choice in choices:
                if not isinstance(choice, dict):
                    continue
                finish_reasons.append(choice.get("finish_reason"))
                delta = choice.get("delta")
                if isinstance(delta, dict):
                    delta_key_sets.append(sorted(delta.keys()))
                    if isinstance(delta.get("content"), str):
                        content_chunks.append(delta["content"])
                    rc = delta.get("reasoning_content")
                    if isinstance(rc, str):
                        reasoning_chunks.append(rc)
        if isinstance(event.get("usage"), dict):
            usage_chunks += 1

    summary["empty_choices_events"] = empty_choices
    summary["usage_chunks"] = usage_chunks
    summary["finish_reasons"] = finish_reasons
    summary["delta_key_sets_unique"] = sorted({json.dumps(v) for v in delta_key_sets})
    summary["top_key_sets_unique"] = sorted({json.dumps(v) for v in top_key_sets})
    summary["content_chunks"] = {
        "count": len(content_chunks),
        "lengths": [len(v) for v in content_chunks],
        "joined_len": len("".join(content_chunks)),
        "first": content_chunks[0] if content_chunks else "",
        "last": content_chunks[-1] if content_chunks else "",
        "possible_cumulative_prefix": any(
            content_chunks[i].startswith(content_chunks[i - 1])
            for i in range(1, len(content_chunks))
            if content_chunks[i - 1]
        ),
    }
    summary["reasoning_chunks"] = {
        "count": len(reasoning_chunks),
        "lengths": [len(v) for v in reasoning_chunks],
        "joined_len": len("".join(reasoning_chunks)),
        "possible_cumulative_prefix": any(
            reasoning_chunks[i].startswith(reasoning_chunks[i - 1])
            for i in range(1, len(reasoning_chunks))
            if reasoning_chunks[i - 1]
        ),
    }
    if errors:
        summary["errors"] = errors
    if not events and raw:
        summary["raw_head"] = raw.decode("utf-8", "replace")[:500]
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True)
    parser.add_argument("--timeout", type=int, default=90)
    parser.add_argument("--insecure", action="store_true")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    context = ssl._create_unverified_context() if args.insecure else None

    prompt_messages = [
        {"role": "system", "content": "You are a response format probe. Keep the answer short."},
        {"role": "user", "content": "请只回复两个字：通过"},
    ]
    all_summaries: list[dict[str, Any]] = []

    for target in TARGETS:
        key = os.environ.get(target["env"])
        if not key:
            print(f"missing env {target['env']}", file=sys.stderr)
            return 2
        url = target["base_url"].rstrip("/") + target["path"]
        for model in target["models"]:
            model_dir = out_dir / target["provider"] / safe_name(model)
            model_dir.mkdir(parents=True, exist_ok=True)

            base_payload = {
                "model": model,
                "messages": prompt_messages,
                "temperature": 0,
                "max_tokens": 64,
            }
            write_json(
                model_dir / "request.redacted.json",
                {
                    "provider": target["provider"],
                    "url": url,
                    "model": model,
                    "headers": {"Authorization": "Bearer ***", "Content-Type": "application/json"},
                    "payload": base_payload,
                },
            )

            nonstream_payload = {**base_payload, "stream": False}
            started = time.time()
            ns_status, ns_headers, ns_body = request_json(
                url,
                key,
                nonstream_payload,
                args.timeout,
                context,
            )
            ns_elapsed = round(time.time() - started, 3)
            (model_dir / "nonstream.raw").write_bytes(ns_body)
            write_json(model_dir / "nonstream.headers.json", ns_headers)
            ns_summary = summarize_nonstream(ns_status, ns_body)
            ns_summary["elapsed_sec"] = ns_elapsed
            write_json(model_dir / "nonstream.summary.json", ns_summary)

            stream_payload = {
                **base_payload,
                "stream": True,
                "stream_options": {"include_usage": True},
            }
            started = time.time()
            s_status, s_headers, s_raw, s_events = request_stream(
                url,
                key,
                stream_payload,
                args.timeout,
                context,
            )
            s_elapsed = round(time.time() - started, 3)
            (model_dir / "stream.raw.sse").write_bytes(s_raw)
            with (model_dir / "stream.events.jsonl").open("w", encoding="utf-8") as fh:
                for event in s_events:
                    fh.write(json.dumps(event, ensure_ascii=False) + "\n")
            write_json(model_dir / "stream.headers.json", s_headers)
            s_summary = summarize_stream(s_status, s_raw, s_events)
            s_summary["elapsed_sec"] = s_elapsed
            write_json(model_dir / "stream.summary.json", s_summary)

            all_summaries.append(
                {
                    "provider": target["provider"],
                    "model": model,
                    "nonstream": ns_summary,
                    "stream": s_summary,
                }
            )
            print(f"{target['provider']} {model}: nonstream={ns_status}, stream={s_status}")

    write_json(out_dir / "summary.json", all_summaries)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
