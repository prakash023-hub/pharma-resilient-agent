#!/usr/bin/env python3
"""Quick connectivity check for PharmaGuard configuration."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.config import load_settings
from src.guardrails import local_pii_check


def main() -> int:
    print("PharmaGuard setup verification\n")

    try:
        settings = load_settings()
    except ValueError as exc:
        print(f"❌ {exc}")
        return 1

    print("✅ TFY_API_KEY is set")

    key = settings.tfy_api_key
    if not key.startswith("eyJ") or key.count(".") != 2:
        print(
            "❌ TFY_API_KEY does not look like a valid TrueFoundry JWT.\n"
            "   Expected: starts with 'eyJ' and contains exactly 2 dots (header.payload.signature).\n"
            "   Fix: TrueFoundry → Settings → API Keys → create/copy the FULL token into .env"
        )
        return 1

    print(f"✅ Token format looks valid ({len(key)} chars)")
    print(f"✅ Gateway URL: {settings.tfy_gateway_url}")
    print(f"✅ Virtual model: {settings.tfy_virtual_model}")

    if settings.tfy_mcp_openfda_url:
        print(f"✅ MCP URL configured: {settings.tfy_mcp_openfda_url}")
    else:
        print("⚠️  TFY_MCP_OPENFDA_URL not set — will use direct OpenFDA fallback")

    if settings.tfy_guardrails_llm_input:
        print(f"✅ LLM guardrails: {settings.tfy_guardrails_llm_input}")
    else:
        print("⚠️  TFY_GUARDRAILS_LLM_INPUT not set — only local PII pre-check active")

    pii = local_pii_check("patient SSN 123-45-6789")
    print(f"✅ Local PII check works: {pii is not None}")

    print("\nNext steps:")
    print("  python scripts/configure_tfy.py   # verify MCP + guardrails")
    print("  python agent.py                   # launch demo")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
