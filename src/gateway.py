"""TrueFoundry AI Gateway client with retries and virtual-model fallback."""

from __future__ import annotations

import time
from typing import Any

import requests

from src.config import Settings
from src.guardrails import build_guardrail_headers, parse_guardrail_error


SYSTEM_PROMPT = (
    "You are a clinical pharmacist AI. Provide concise antibiotic recommendations "
    "based on WHO AWaRe 2023 guidelines. Include dose adjustments for renal "
    "impairment when CrCl is mentioned. Keep answers practical for clinicians."
)

_NO_RETRY_STATUSES = {401, 403, 404, 422}


class GatewayResult:
    def __init__(
        self,
        success: bool,
        content: str,
        logs: list[str],
        blocked_by_guardrail: bool = False,
    ):
        self.success = success
        self.content = content
        self.logs = logs
        self.blocked_by_guardrail = blocked_by_guardrail


def call_chat_completion(
    settings: Settings,
    user_content: str,
    simulate_model_failure: bool = False,
) -> GatewayResult:
    """Call the TrueFoundry gateway with retries and optional failure demo."""
    logs: list[str] = []
    guardrail_header = build_guardrail_headers(
        llm_input=_split_csv(settings.tfy_guardrails_llm_input),
    )

    models_to_try: list[tuple[str, str]] = []
    if simulate_model_failure:
        logs.append("  [DEMO] Primary model failure simulation")
        logs.append(f"  Probing unavailable model: {settings.tfy_broken_model}")
        models_to_try.append(
            (settings.tfy_broken_model, "intentional primary failure for demo")
        )

    models_to_try.append(
        (settings.tfy_virtual_model, "virtual model with configured gateway fallback")
    )

    base_headers = {
        "Authorization": f"Bearer {settings.tfy_api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.tfy_virtual_model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
        "max_tokens": 400,
        "stream": False,
    }

    for model_name, reason in models_to_try:
        payload["model"] = model_name
        is_demo_broken = model_name == settings.tfy_broken_model
        max_attempts = 1 if is_demo_broken else settings.max_retries

        logs.append(f"  Route: {model_name} ({reason})")

        header_variants = [base_headers | guardrail_header]
        if guardrail_header:
            header_variants.append(base_headers)

        for attempt in range(1, max_attempts + 1):
            if not is_demo_broken:
                logs.append(f"  Attempt {attempt}/{max_attempts}")

            response = None
            for header_idx, headers in enumerate(header_variants):
                try:
                    response = requests.post(
                        f"{settings.tfy_gateway_url}/chat/completions",
                        headers=headers,
                        json=payload,
                        timeout=45,
                    )
                except requests.RequestException as exc:
                    logs.append(f"  [ERR] Network error: {exc}")
                    response = None
                    break

                if response is None:
                    continue

                if (
                    guardrail_header
                    and header_idx == 0
                    and _is_guardrail_config_error(response)
                ):
                    logs.append("  [WARN] Guardrail slug not found — retrying without header")
                    continue

                break

            if response is None:
                if attempt < max_attempts:
                    time.sleep(settings.retry_backoff_seconds * attempt)
                continue

            if response.status_code == 200:
                answer = response.json()["choices"][0]["message"]["content"]
                if is_demo_broken:
                    logs.append("  [OK] Unexpected success on broken model")
                elif simulate_model_failure and model_name == settings.tfy_virtual_model:
                    logs.append("  [OK] Gateway fallback recovered successfully")
                else:
                    logs.append("  [OK] Primary route succeeded")
                return GatewayResult(True, answer, logs)

            body = _safe_json(response)
            if _is_guardrail_block(response.status_code, body):
                message = parse_guardrail_error(body)
                logs.append(f"  [BLOCKED] {message}")
                return GatewayResult(False, message, logs, blocked_by_guardrail=True)

            err_msg = body.get("error", {}).get("message", response.text[:180])
            if is_demo_broken:
                logs.append(f"  [OK] Primary unavailable as expected ({response.status_code})")
                logs.append("  [FAILOVER] Switching to virtual model")
                break

            logs.append(f"  [ERR] HTTP {response.status_code}: {err_msg}")

            if response.status_code in _NO_RETRY_STATUSES:
                break

            if attempt < max_attempts:
                sleep_for = settings.retry_backoff_seconds * attempt
                logs.append(f"  [WAIT] Backing off {sleep_for:.1f}s")
                time.sleep(sleep_for)

    logs.append("[ERR] All gateway attempts failed — graceful degradation")
    fallback_text = (
        "Service temporarily unavailable.\n"
        "Please consult WHO AWaRe guidelines: https://aware.essentialmeds.org"
    )
    return GatewayResult(False, fallback_text, logs)


def _split_csv(value: str) -> list[str] | None:
    items = [item.strip() for item in value.split(",") if item.strip()]
    return items or None


def _safe_json(response: requests.Response) -> dict[str, Any]:
    try:
        return response.json()
    except ValueError:
        return {}


def _is_guardrail_block(status_code: int, body: dict[str, Any]) -> bool:
    if status_code != 400:
        return False
    return body.get("error", {}).get("type") == "guardrail_checks_failed"


def _is_guardrail_config_error(response: requests.Response) -> bool:
    if response.status_code not in {400, 404, 422}:
        return False
    body = _safe_json(response)
    message = body.get("error", {}).get("message", response.text).lower()
    return "guardrail" in message and "not found" in message
