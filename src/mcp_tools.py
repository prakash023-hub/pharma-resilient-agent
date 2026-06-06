"""OpenFDA access via TrueFoundry MCP Gateway with direct HTTP fallback."""

from __future__ import annotations

import asyncio
import re
from typing import Any

import requests

from src.config import Settings
from src.guardrails import build_guardrail_headers


def extract_drug_name(query: str) -> str:
    """Pick the first plausible drug token from a free-text clinical query."""
    tokens = re.findall(r"[A-Za-z][A-Za-z-]{2,}", query)
    for token in tokens:
        if token.lower() not in {
            "for",
            "with",
            "patient",
            "best",
            "antibiotic",
            "pneumonia",
            "uti",
            "renal",
            "impairment",
            "penicillin",
            "allergic",
            "dose",
            "adjustment",
        }:
            return token
    return tokens[0] if tokens else "amoxicillin"


def _direct_openfda_lookup(drug_name: str, timeout: int = 5) -> str:
    url = (
        "https://api.fda.gov/drug/label.json"
        f"?search=openfda.brand_name:{drug_name}&limit=1"
    )
    response = requests.get(url, timeout=timeout)
    if response.status_code != 200:
        return "No FDA data found"

    data = response.json()
    results = data.get("results", [])
    if not results:
        return "No FDA data found"

    indications = results[0].get("indications_and_usage", ["No data"])
    return str(indications[0])[:500]


async def _mcp_openfda_lookup(
    settings: Settings,
    drug_name: str,
    tool_name: str = "lookup_drug_label",
) -> tuple[str, list[str]]:
    """Call OpenFDA through TrueFoundry MCP Gateway."""
    logs: list[str] = []

    if not settings.tfy_mcp_openfda_url:
        logs.append("  [INFO] MCP URL not set — using OpenFDA HTTP fallback")
        text = _direct_openfda_lookup(drug_name)
        logs.append("  [OK] OpenFDA data retrieved (direct HTTP)")
        return text, logs

    try:
        from fastmcp import Client
        from fastmcp.client.transports import StreamableHttpTransport
    except ImportError as exc:
        logs.append(f"  [WARN] fastmcp not installed ({exc})")
        return _direct_openfda_lookup(drug_name), logs

    headers = {"Authorization": f"Bearer {settings.tfy_api_key}"}
    headers.update(
        build_guardrail_headers(
            mcp_pre=_split_csv(settings.tfy_guardrails_mcp_pre),
            mcp_post=_split_csv(settings.tfy_guardrails_mcp_post),
        )
    )

    transport = StreamableHttpTransport(
        url=settings.tfy_mcp_openfda_url,
        headers=headers,
    )

    logs.append(f"  MCP URL: {settings.tfy_mcp_openfda_url}")

    async with Client(transport) as client:
        tools = await client.list_tools()
        available = [tool.name for tool in tools]
        logs.append(f"  Tools: {', '.join(available) or '(none)'}")

        chosen_tool = tool_name if tool_name in available else (available[0] if available else "")
        if not chosen_tool:
            logs.append("  [WARN] No MCP tools — degrading to direct OpenFDA HTTP")
            return _direct_openfda_lookup(drug_name), logs

        result = await client.call_tool(chosen_tool, {"drug_name": drug_name})
        text = _stringify_mcp_result(result)
        logs.append("  [OK] MCP tool call succeeded")
        return text[:500], logs


def _run_async(coro):
    """Run async MCP client code from Gradio's synchronous callback."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    import concurrent.futures

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, coro).result()


def lookup_openfda(
    settings: Settings,
    drug_name: str,
    simulate_tool_failure: bool = False,
) -> tuple[str, list[str]]:
    """Synchronous wrapper used by the Gradio agent."""
    logs: list[str] = []

    if simulate_tool_failure:
        logs.append("  [DEMO] Tool failure simulated — OpenFDA unavailable")
        return "FDA tool unavailable (simulated failure)", logs

    try:
        text, mcp_logs = _run_async(
            _mcp_openfda_lookup(settings, drug_name)
        )
        logs.extend(mcp_logs)
        return text, logs
    except Exception as exc:
        short_err = str(exc).split("\n")[0][:120]
        logs.append(f"  [ERR] MCP Gateway: {short_err}")
        logs.append("  [FAILOVER] Direct OpenFDA HTTP fallback")
        try:
            text = _direct_openfda_lookup(drug_name)
            logs.append("  [OK] Direct OpenFDA fallback succeeded")
            return text, logs
        except Exception as fallback_exc:
            logs.append(f"  [ERR] OpenFDA fallback failed: {fallback_exc}")
            return "FDA data unavailable — continuing with AWaRe guidelines only", logs


def _split_csv(value: str) -> list[str] | None:
    items = [item.strip() for item in value.split(",") if item.strip()]
    return items or None


def _stringify_mcp_result(result: Any) -> str:
    if result is None:
        return "No data"
    if isinstance(result, str):
        return result
    if hasattr(result, "data"):
        data = result.data
        if isinstance(data, list) and data:
            first = data[0]
            if hasattr(first, "text"):
                return str(first.text)
            return str(first)
        return str(data)
    if isinstance(result, dict):
        return str(result.get("text") or result.get("content") or result)
    return str(result)
