"""Display formatting for Gradio UI."""

from __future__ import annotations

import html
import re

DIVIDER = "=" * 42

_PANEL_STYLE = (
    "background:#ffffff;"
    "color:#1e293b;"
    "border:1px solid #cbd5e1;"
    "border-radius:10px;"
    "padding:18px 20px;"
    "min-height:380px;"
    "font-family:Inter,-apple-system,sans-serif;"
    "font-size:15px;"
    "line-height:1.65;"
)
_TITLE_STYLE = "color:#1d4ed8;font-size:1.15rem;font-weight:700;margin:0 0 12px 0;"
_BODY_STYLE = "color:#334155;margin:0 0 10px 0;"
_WARN_STYLE = "color:#b45309;font-weight:600;"


def _markdown_to_html(text: str) -> str:
    """Convert simple markdown bold and paragraphs to HTML."""
    escaped = html.escape(text.strip())
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    paragraphs = [p.strip() for p in escaped.split("\n\n") if p.strip()]
    if not paragraphs:
        return f'<p style="{_BODY_STYLE}">{escaped}</p>'

    parts = []
    for para in paragraphs:
        lines = [ln.strip() for ln in para.split("\n") if ln.strip()]
        if len(lines) == 1:
            parts.append(f'<p style="{_BODY_STYLE}">{lines[0]}</p>')
        else:
            items = "".join(f"<li>{ln}</li>" for ln in lines)
            parts.append(f'<ul style="{_BODY_STYLE} margin-left:18px;">{items}</ul>')
    return "\n".join(parts)


def empty_clinical_panel() -> str:
    """Placeholder panel before first run."""
    return (
        f'<div style="{_PANEL_STYLE}">'
        f'<p style="{_TITLE_STYLE}">Clinical Recommendation</p>'
        f'<p style="{_BODY_STYLE}">Click <b>Run PharmaGuard Agent</b> to generate an '
        "AWaRe-aligned antibiotic recommendation with renal dosing guidance.</p>"
        f'<p style="{_BODY_STYLE} color:#64748b;font-size:0.9rem;">'
        "Example loaded: UTI + CrCl 45 — ready for demo video Scenario 1.</p>"
        "</div>"
    )


def format_clinical_answer(text: str) -> str:
    """Render clinical output as styled HTML for reliable Gradio display."""
    if not text or not text.strip():
        return empty_clinical_panel()

    cleaned = text.strip()

    if cleaned.startswith("BLOCKED") or cleaned.upper().startswith("BLOCKED"):
        body = _markdown_to_html(cleaned)
        return (
            f'<div style="{_PANEL_STYLE}">'
            f'<p style="{_TITLE_STYLE} {_WARN_STYLE}">Request Blocked</p>'
            f"{body}</div>"
        )

    if cleaned.startswith("Service temporarily unavailable"):
        body = _markdown_to_html(cleaned)
        return (
            f'<div style="{_PANEL_STYLE}">'
            f'<p style="{_TITLE_STYLE} {_WARN_STYLE}">Service Degraded</p>'
            f"{body}</div>"
        )

    body = _markdown_to_html(cleaned)
    return (
        f'<div style="{_PANEL_STYLE}">'
        f'<p style="{_TITLE_STYLE}">Clinical Recommendation</p>'
        f"{body}</div>"
    )
