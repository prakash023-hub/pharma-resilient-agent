"""PharmaGuard resilient agent orchestration."""

from __future__ import annotations

from src.config import Settings, load_settings
from src.formatting import DIVIDER
from src.gateway import call_chat_completion
from src.guardrails import local_pii_check
from src.mcp_tools import extract_drug_name, lookup_openfda


def run_pharma_agent(
    patient_query: str,
    simulate_model_failure: bool = False,
    simulate_tool_failure: bool = False,
    settings: Settings | None = None,
) -> tuple[str, str]:
    """Execute the full agent loop and return (logs, clinical_answer)."""
    settings = settings or load_settings()
    logs: list[str] = []

    logs.append(DIVIDER)
    logs.append("PHARMAGUARD RESILIENT AGENT")
    logs.append(DIVIDER)
    logs.append(f"Input: {patient_query.strip()}")
    logs.append("")

    if not patient_query.strip():
        return "\n".join(logs), "Please enter a clinical query."

    logs.append("[GUARDRAIL] Local pre-filter")
    local_block = local_pii_check(patient_query)
    if local_block:
        logs.append(f"[BLOCKED] {local_block}")
        logs.append(DIVIDER)
        return (
            "\n".join(logs),
            "BLOCKED\n\nPII detected in input. Patient data protection enforced "
            "before any model or tool call.",
        )
    logs.append("[OK] Local pre-check passed — forwarding to TrueFoundry Guardrails")
    logs.append("")

    logs.append("[MCP GATEWAY] OpenFDA Tool")
    drug_name = extract_drug_name(patient_query)
    logs.append(f"  Drug hint: {drug_name}")
    fda_info, tool_logs = lookup_openfda(
        settings,
        drug_name,
        simulate_tool_failure=simulate_tool_failure,
    )
    logs.extend(tool_logs)
    logs.append("")

    logs.append("[AI GATEWAY] Virtual Model Routing")
    if simulate_model_failure:
        logs.append("  Demo mode: primary failure -> gateway fallback recovery")
    else:
        logs.append(f"  Virtual model: {settings.tfy_virtual_model}")

    llm_prompt = (
        f"Clinical query: {patient_query.strip()}\n"
        f"FDA reference: {fda_info[:300]}\n"
        "Provide a concise recommendation with AWaRe category and renal dosing if relevant."
    )

    gateway_result = call_chat_completion(
        settings,
        llm_prompt,
        simulate_model_failure=simulate_model_failure,
    )
    logs.extend(gateway_result.logs)
    logs.append("")

    if gateway_result.blocked_by_guardrail:
        logs.append(DIVIDER)
        logs.append("[BLOCKED] TrueFoundry Guardrails")
        logs.append(DIVIDER)
        return "\n".join(logs), gateway_result.content

    if gateway_result.success:
        logs.append(DIVIDER)
        logs.append("[SUCCESS] Agent completed")
        logs.append(DIVIDER)
        return "\n".join(logs), gateway_result.content

    logs.append(DIVIDER)
    logs.append("[DEGRADED] Graceful fallback active")
    logs.append(DIVIDER)
    return "\n".join(logs), gateway_result.content
