from __future__ import annotations

import json
from typing import AsyncIterator

import httpx
from fastapi import FastAPI, Request
from fastapi.responses import Response, StreamingResponse


UPSTREAM = "http://127.0.0.1:8090"
HOP_BY_HOP_HEADERS = {
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
}

app = FastAPI(title="New API Stream Compatibility Filter", version="0.1.0")


def _forward_headers(headers: httpx.Headers) -> dict[str, str]:
    result: dict[str, str] = {}
    for key, value in headers.items():
        lower = key.lower()
        if lower in HOP_BY_HOP_HEADERS:
            continue
        if lower in {"content-length", "content-encoding"}:
            continue
        result[key] = value
    return result


def _should_drop_sse_event(raw: str) -> bool:
    data_lines = [line[5:].strip() for line in raw.splitlines() if line.startswith("data:")]
    if not data_lines:
        return False
    payload = "".join(data_lines)
    if payload == "[DONE]":
        return False
    try:
        obj = json.loads(payload)
    except json.JSONDecodeError:
        return False
    return obj.get("choices") == []


async def _filtered_sse(resp: httpx.Response) -> AsyncIterator[bytes]:
    buffer = ""
    async for text in resp.aiter_text():
        buffer += text
        while "\n\n" in buffer:
            raw, buffer = buffer.split("\n\n", 1)
            if _should_drop_sse_event(raw):
                continue
            yield f"{raw}\n\n".encode("utf-8")
    if buffer and not _should_drop_sse_event(buffer):
        yield buffer.encode("utf-8")


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
async def proxy(path: str, request: Request):
    url = f"{UPSTREAM}/{path}"
    if request.url.query:
        url = f"{url}?{request.url.query}"

    headers = {
        key: value
        for key, value in request.headers.items()
        if key.lower() not in HOP_BY_HOP_HEADERS | {"host", "content-length"}
    }
    body = await request.body()

    client = httpx.AsyncClient(timeout=httpx.Timeout(300.0, connect=20.0))
    req = client.build_request(request.method, url, headers=headers, content=body)
    resp = await client.send(req, stream=True)
    response_headers = _forward_headers(resp.headers)
    content_type = resp.headers.get("content-type", "")

    if "text/event-stream" in content_type.lower():
        async def gen() -> AsyncIterator[bytes]:
            try:
                async for chunk in _filtered_sse(resp):
                    yield chunk
            finally:
                await resp.aclose()
                await client.aclose()

        return StreamingResponse(
            gen(),
            status_code=resp.status_code,
            headers=response_headers,
            media_type="text/event-stream",
        )

    try:
        content = await resp.aread()
        return Response(
            content=content,
            status_code=resp.status_code,
            headers=response_headers,
            media_type=resp.headers.get("content-type"),
        )
    finally:
        await resp.aclose()
        await client.aclose()
