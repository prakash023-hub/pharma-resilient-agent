#!/usr/bin/env python3
"""Validate MCP URL and guardrail slugs against your TrueFoundry account."""

from __future__ import annotations

import asyncio
import json
import os
import sys

import requests

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.config import load_settings


def test_gateway(settings) -> bool:
    r = requests.post(
        f"{settings.tfy_gateway_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.tfy_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": settings.tfy_virtual_model,
            "messages": [{"role": "user", "content": "Reply OK"}],
            "max_tokens": 5,
        },
        timeout=30,
    )
    ok = r.status_code == 200
    print(f"[{'OK' if ok else 'FAIL'}] AI Gateway / virtual model ({r.status_code})")
    return ok


def test_guardrails(settings) -> bool:
    slug = settings.tfy_guardrails_llm_input.strip()
    if not slug:
        print("[SKIP] TFY_GUARDRAILS_LLM_INPUT not set")
        return False

    headers = {
        "Authorization": f"Bearer {settings.tfy_api_key}",
        "Content-Type": "application/json",
        "X-TFY-GUARDRAILS": json.dumps({"llm_input_guardrails": [slug]}),
        "X-TFY-GUARDRAILS-SCOPE": "last",
    }
    r = requests.post(
        f"{settings.tfy_gateway_url}/chat/completions",
        headers=headers,
        json={
            "model": settings.tfy_virtual_model,
            "messages": [{"role": "user", "content": "hello"}],
            "max_tokens": 5,
        },
        timeout=30,
    )
    ok = r.status_code == 200
    print(f"[{'OK' if ok else 'FAIL'}] Guardrail slug '{slug}' ({r.status_code})")
    if not ok:
        try:
            print("       ", r.json().get("error", {}).get("message", "")[:120])
        except Exception:
            pass
        print("       Fix slug in TrueFoundry Guardrails UI → copy exact slug to .env")
    return ok


async def test_mcp(settings) -> bool:
    url = settings.tfy_mcp_openfda_url.strip()
    if not url:
        print("[SKIP] TFY_MCP_OPENFDA_URL not set")
        return False

    try:
        from fastmcp import Client
        from fastmcp.client.transports import StreamableHttpTransport
    except ImportError:
        print("[FAIL] fastmcp not installed")
        return False

    try:
        transport = StreamableHttpTransport(
            url=url,
            headers={"Authorization": f"Bearer {settings.tfy_api_key}"},
        )
        async with Client(transport) as client:
            tools = await client.list_tools()
            names = [t.name for t in tools]
        print(f"[OK] MCP Gateway ({url})")
        print(f"     tools: {', '.join(names) or '(none)'}")
        return bool(names)
    except Exception as exc:
        print(f"[FAIL] MCP Gateway ({url})")
        print(f"       {exc}")
        print("       Register mcp_server/openfda_server.py in TrueFoundry → copy URL to .env")
        return False


def main() -> int:
    print("PharmaGuard TrueFoundry configuration check\n")
    settings = load_settings()

    results = [
        test_gateway(settings),
        asyncio.run(test_mcp(settings)),
        test_guardrails(settings),
    ]

    print()
    if all(results[:1]):
        print("✅ Minimum submission ready (gateway works).")
    if all(results):
        print("✅ Full stack verified (gateway + MCP + guardrails).")
    elif results[0]:
        print("⚠️  Gateway works; fix MCP/guardrail slugs in .env for max judge score.")
    else:
        print("❌ Gateway failed — check TFY_API_KEY and virtual model name.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
