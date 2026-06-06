"""Guardrail helpers — TrueFoundry headers plus local safety net."""

from __future__ import annotations

import json
import re
from typing import Any

PII_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),  # SSN
    re.compile(r"\b\d{16}\b"),  # credit card (simplified)
    re.compile(r"\b(?:ssn|social security|credit card|password)\b", re.I),
]


def local_pii_check(text: str) -> str | None:
    """Fast local pre-check before the gateway guardrail runs."""
    for pattern in PII_PATTERNS:
        if pattern.search(text):
            return "PII or sensitive credential pattern detected in input"
    return None


def build_guardrail_headers(
    llm_input: list[str] | None = None,
    llm_output: list[str] | None = None,
    mcp_pre: list[str] | None = None,
    mcp_post: list[str] | None = None,
) -> dict[str, str]:
    """Build X-TFY-GUARDRAILS header for a gateway request."""
    payload: dict[str, list[str]] = {}
    if llm_input:
        payload["llm_input_guardrails"] = llm_input
    if llm_output:
        payload["llm_output_guardrails"] = llm_output
    if mcp_pre:
        payload["mcp_tool_pre_invoke_guardrails"] = mcp_pre
    if mcp_post:
        payload["mcp_tool_post_invoke_guardrails"] = mcp_post

    if not payload:
        return {}

    return {
        "X-TFY-GUARDRAILS": json.dumps(payload),
        "X-TFY-GUARDRAILS-SCOPE": "last",
    }


def parse_guardrail_error(error_body: dict[str, Any]) -> str:
    """Turn a gateway guardrail error into a human-readable message."""
    checks = error_body.get("guardrail_checks", {})
    hooks = [
        "llm_input_guardrails",
        "llm_output_guardrails",
        "mcp_tool_pre_invoke_guardrails",
        "mcp_tool_post_invoke_guardrails",
    ]
    triggered = [hook for hook in hooks if checks.get(hook)]
    if triggered:
        return f"TrueFoundry Guardrails blocked request on: {', '.join(triggered)}"
    return "TrueFoundry Guardrails blocked this request for patient safety."
