"""Environment configuration for PharmaGuard."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    tfy_api_key: str
    tfy_gateway_url: str
    tfy_virtual_model: str
    tfy_broken_model: str
    tfy_fallback_model: str
    tfy_mcp_openfda_url: str
    tfy_guardrails_llm_input: str
    tfy_guardrails_mcp_pre: str
    tfy_guardrails_mcp_post: str
    max_retries: int
    retry_backoff_seconds: float


def _require(name: str, default: str = "") -> str:
    value = os.getenv(name, default)
    if value is None:
        return default
    return value.strip().strip('"').strip("'")


def load_settings() -> Settings:
    api_key = _require("TFY_API_KEY")
    if not api_key:
        raise ValueError(
            "TFY_API_KEY is not set. Copy .env.example to .env and add your TrueFoundry token."
        )

    return Settings(
        tfy_api_key=api_key,
        tfy_gateway_url=_require(
            "TFY_GATEWAY_URL",
            "https://gateway.truefoundry.ai/api/inference/openai",
        ).rstrip("/"),
        tfy_virtual_model=_require(
            "TFY_VIRTUAL_MODEL",
            "pharma-resilient-gateway/primary-nova",
        ),
        tfy_broken_model=_require(
            "TFY_BROKEN_MODEL",
            "pharma-resilient-gateway/intentionally-broken-model",
        ),
        tfy_fallback_model=_require(
            "TFY_FALLBACK_MODEL",
            "pharma-resilient-gateway/fallback-llama",
        ),
        tfy_mcp_openfda_url=_require("TFY_MCP_OPENFDA_URL"),
        tfy_guardrails_llm_input=_require("TFY_GUARDRAILS_LLM_INPUT"),
        tfy_guardrails_mcp_pre=_require("TFY_GUARDRAILS_MCP_PRE"),
        tfy_guardrails_mcp_post=_require("TFY_GUARDRAILS_MCP_POST"),
        max_retries=int(_require("TFY_MAX_RETRIES", "3")),
        retry_backoff_seconds=float(_require("TFY_RETRY_BACKOFF_SECONDS", "2")),
    )
