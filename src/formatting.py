"""Display formatting for Gradio UI — plain text, always readable."""

from __future__ import annotations

import re

DIVIDER = "=" * 42


def _strip_markdown(text: str) -> str:
    """Remove markdown bold markers for plain textbox display."""
    cleaned = text.strip()
    cleaned = re.sub(r"\*\*(.+?)\*\*", r"\1", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned


def empty_clinical_panel() -> str:
    return (
        "CLINICAL RECOMMENDATION\n"
        "------------------------\n"
        "Click [Run PharmaGuard Agent] to generate an AWaRe-aligned answer.\n\n"
        "Example loaded: UTI + CrCl 45 (Demo Scenario 1)."
    )


def format_clinical_answer(text: str) -> str:
    """Plain text for Gradio textbox — dark text, no HTML."""
    if not text or not text.strip():
        return empty_clinical_panel()

    cleaned = _strip_markdown(text)

    if cleaned.upper().startswith("BLOCKED") or "BLOCKED" in cleaned[:40].upper():
        return "REQUEST BLOCKED\n-----------------\n\n" + cleaned

    if cleaned.startswith("Service temporarily unavailable"):
        return "SERVICE DEGRADED\n----------------\n\n" + cleaned

    return "CLINICAL RECOMMENDATION\n------------------------\n\n" + cleaned
