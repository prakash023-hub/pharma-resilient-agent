"""
PharmaGuard Resilient Agent — TrueFoundry Hackathon Demo
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import gradio as gr

from src.agent_core import run_pharma_agent
from src.formatting import format_clinical_answer, empty_clinical_panel

CSS = """
/* ── Page ── */
.gradio-container {
    max-width: 1100px !important;
    background: #f1f5f9 !important;
    font-family: "Segoe UI", Inter, system-ui, sans-serif !important;
}
footer { display: none !important; }

/* ── All labels & checkbox text — force dark ── */
.gradio-container label,
.gradio-container label span,
.gradio-container .label-wrap span,
.gradio-container .form-checkbox-label,
.gradio-container fieldset span {
    color: #1e293b !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* ── Checkboxes — visible box + dark label ── */
.gradio-container input[type="checkbox"] {
    width: 18px !important;
    height: 18px !important;
    accent-color: #2563eb !important;
    cursor: pointer !important;
}
.gradio-container .form-checkbox,
.gradio-container .form-checkbox-label {
    background: #ffffff !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    margin: 4px 0 !important;
}

/* ── Text inputs ── */
.gradio-container textarea,
.gradio-container input[type="text"] {
    color: #1e293b !important;
    background: #ffffff !important;
    border: 1px solid #94a3b8 !important;
    border-radius: 6px !important;
    font-size: 14px !important;
}

/* ── Logs panel ── */
#pg-logs textarea {
    font-family: "Courier New", Courier, monospace !important;
    font-size: 12.5px !important;
    line-height: 1.55 !important;
    background: #ffffff !important;
    color: #1e293b !important;
    border: 1px solid #94a3b8 !important;
    border-top: 3px solid #059669 !important;
    border-radius: 0 0 8px 8px !important;
    min-height: 380px !important;
}

/* ── Clinical panel ── */
#pg-answer textarea {
    font-family: "Segoe UI", Inter, sans-serif !important;
    font-size: 14.5px !important;
    line-height: 1.65 !important;
    background: #ffffff !important;
    color: #1e3a8a !important;
    border: 1px solid #94a3b8 !important;
    border-top: 3px solid #2563eb !important;
    border-radius: 0 0 8px 8px !important;
    min-height: 380px !important;
    font-weight: 500 !important;
}

/* ── Primary button ── */
.gradio-container button.primary {
    background: #1d4ed8 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    border-radius: 8px !important;
    padding: 10px 24px !important;
}
.gradio-container button.primary:hover {
    background: #1e40af !important;
}

/* ── Secondary buttons ── */
.gradio-container button.secondary {
    color: #1e293b !important;
    background: #e2e8f0 !important;
    border: 1px solid #94a3b8 !important;
    font-weight: 600 !important;
}
"""

EXAMPLE_UTI = "Amoxicillin for UTI in 65yo patient with CrCl 45"
EXAMPLE_PNEUMONIA = "Best antibiotic for pneumonia in penicillin-allergic patient"
EXAMPLE_PII = "Amoxicillin for UTI, patient SSN 123-45-6789"


def safe_run(query: str, simulate_model_failure: bool, simulate_tool_failure: bool):
    try:
        logs, answer = run_pharma_agent(
            query,
            simulate_model_failure=simulate_model_failure,
            simulate_tool_failure=simulate_tool_failure,
        )
        return logs, format_clinical_answer(answer)
    except ValueError as exc:
        return str(exc), "CONFIGURATION ERROR\n\nSet TFY_API_KEY in your .env file."
    except Exception as exc:
        return f"Error: {exc}", "AGENT ERROR\n\nCheck logs and TrueFoundry connectivity."


def panel_header(title: str, accent: str) -> str:
    return (
        f'<div style="background:{accent};color:#ffffff;font-weight:700;'
        f'font-size:0.9rem;padding:10px 16px;border-radius:8px 8px 0 0;'
        f'letter-spacing:0.03em;">{title}</div>'
    )


with gr.Blocks(title="PharmaGuard — TrueFoundry Hackathon") as demo:

    # ── HEADER ──────────────────────────────────────────────────────────
    gr.HTML("""
    <div style="background:#0f2744;border-radius:12px;padding:28px 32px;
                margin-bottom:20px;border-left:5px solid #3b82f6;">
        <p style="color:#93c5fd;font-size:0.8rem;font-weight:600;
                  margin:0 0 6px 0;letter-spacing:0.08em;text-transform:uppercase;">
            TrueFoundry Resilient Agents Hackathon 2026
        </p>
        <h1 style="color:#ffffff;font-size:1.85rem;font-weight:800;
                   margin:0 0 8px 0;letter-spacing:-0.01em;">
            PharmaGuard Resilient Agent
        </h1>
        <p style="color:#cbd5e1;font-size:0.95rem;margin:0 0 16px 0;line-height:1.5;">
            Clinical antibiotic stewardship powered by TrueFoundry AI Gateway,
            MCP Gateway, Guardrails, and AWS Bedrock.
        </p>
        <div style="display:flex;gap:10px;flex-wrap:wrap;">
            <span style="background:#1e3a5f;color:#7dd3fc;padding:5px 14px;
                         border-radius:20px;font-size:0.78rem;font-weight:600;
                         border:1px solid #3b82f6;">AI Gateway</span>
            <span style="background:#1e3a5f;color:#7dd3fc;padding:5px 14px;
                         border-radius:20px;font-size:0.78rem;font-weight:600;
                         border:1px solid #3b82f6;">MCP Gateway</span>
            <span style="background:#1e3a5f;color:#7dd3fc;padding:5px 14px;
                         border-radius:20px;font-size:0.78rem;font-weight:600;
                         border:1px solid #3b82f6;">Guardrails</span>
            <span style="background:#1e3a5f;color:#7dd3fc;padding:5px 14px;
                         border-radius:20px;font-size:0.78rem;font-weight:600;
                         border:1px solid #3b82f6;">Fallback + Retries</span>
        </div>
    </div>
    """)

    # ── INPUT ROW ───────────────────────────────────────────────────────
    with gr.Row(equal_height=True):

        with gr.Column(scale=3):
            gr.HTML("""
            <p style="color:#0f2744;font-size:1rem;font-weight:700;
                      margin:0 0 8px 0;border-bottom:2px solid #3b82f6;
                      padding-bottom:6px;display:inline-block;">
                Clinical Query
            </p>
            """)
            query_input = gr.Textbox(
                label="Enter patient antibiotic question",
                value=EXAMPLE_UTI,
                lines=3,
                placeholder="e.g. Amoxicillin for UTI in 65yo patient with CrCl 45",
            )

            gr.HTML("""
            <p style="color:#475569;font-size:0.85rem;font-weight:600;
                      margin:12px 0 6px 0;">Load example query:</p>
            """)
            with gr.Row():
                btn_ex1 = gr.Button("Scenario 1 — Normal", size="sm")
                btn_ex2 = gr.Button("Scenario 2 — Pneumonia", size="sm")
                btn_ex3 = gr.Button("Scenario 4 — PII Block", size="sm", variant="stop")

            gr.HTML("""
            <p style="color:#0f2744;font-size:1rem;font-weight:700;
                      margin:16px 0 8px 0;border-bottom:2px solid #3b82f6;
                      padding-bottom:6px;display:inline-block;">
                Resilience Demo Modes
            </p>
            <p style="color:#64748b;font-size:0.82rem;margin:0 0 8px 0;">
                Enable one checkbox at a time for failure demos (Scenarios 2 &amp; 3).
            </p>
            """)

            simulate_model_cb = gr.Checkbox(
                label="Scenario 2 — Simulate primary model failure (gateway fallback)",
                value=False,
            )
            simulate_tool_cb = gr.Checkbox(
                label="Scenario 3 — Simulate OpenFDA tool failure (graceful degradation)",
                value=False,
            )

            submit_btn = gr.Button("Run PharmaGuard Agent", variant="primary", size="lg")

        with gr.Column(scale=2):
            gr.HTML("""
            <div style="background:#ffffff;border:1px solid #cbd5e1;
                        border-radius:10px;padding:20px;height:100%;
                        box-shadow:0 1px 4px rgba(0,0,0,0.06);">
                <p style="color:#0f2744;font-size:1rem;font-weight:700;
                          margin:0 0 14px 0;border-bottom:2px solid #e2e8f0;
                          padding-bottom:8px;">
                    Demo Scenarios for Judges
                </p>
                <table style="width:100%;border-collapse:collapse;font-size:0.88rem;">
                    <tr style="background:#eff6ff;">
                        <td style="padding:8px 10px;color:#1d4ed8;font-weight:700;
                                   border:1px solid #bfdbfe;width:30px;">1</td>
                        <td style="padding:8px 10px;color:#1e293b;border:1px solid #bfdbfe;">
                            <b>Normal path</b> — no checkboxes, click Run
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:8px 10px;color:#1d4ed8;font-weight:700;
                                   border:1px solid #bfdbfe;">2</td>
                        <td style="padding:8px 10px;color:#1e293b;border:1px solid #bfdbfe;">
                            <b>Model failure</b> — enable first checkbox
                        </td>
                    </tr>
                    <tr style="background:#f8fafc;">
                        <td style="padding:8px 10px;color:#1d4ed8;font-weight:700;
                                   border:1px solid #bfdbfe;">3</td>
                        <td style="padding:8px 10px;color:#1e293b;border:1px solid #bfdbfe;">
                            <b>Tool failure</b> — enable second checkbox
                        </td>
                    </tr>
                    <tr>
                        <td style="padding:8px 10px;color:#1d4ed8;font-weight:700;
                                   border:1px solid #bfdbfe;">4</td>
                        <td style="padding:8px 10px;color:#1e293b;border:1px solid #bfdbfe;">
                            <b>PII block</b> — click PII button, no checkboxes
                        </td>
                    </tr>
                </table>
                <p style="color:#64748b;font-size:0.8rem;margin:14px 0 0;
                          line-height:1.5;border-top:1px solid #e2e8f0;padding-top:12px;">
                    Built by <b style="color:#1e293b;">Prakash Raj</b><br>
                    Stack: TrueFoundry + AWS Bedrock + OpenFDA
                </p>
            </div>
            """)

    # ── OUTPUT ROW ──────────────────────────────────────────────────────
    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML(panel_header("Agent Execution Logs", "#065f46"))
            logs_output = gr.Textbox(
                label="",
                show_label=False,
                lines=20,
                max_lines=30,
                buttons=["copy"],
                elem_id="pg-logs",
                interactive=False,
                value="Logs will appear here after you click Run PharmaGuard Agent.",
            )
        with gr.Column(scale=1):
            gr.HTML(panel_header("Clinical Recommendation", "#1d4ed8"))
            answer_output = gr.Textbox(
                label="",
                show_label=False,
                lines=20,
                max_lines=30,
                buttons=["copy"],
                elem_id="pg-answer",
                interactive=False,
                value=empty_clinical_panel(),
            )

    # ── FOOTER — dark bg, light text (high contrast) ────────────────────
    gr.HTML("""
    <div style="background:#0f2744;border-radius:10px;padding:20px 24px;
                margin-top:16px;border:1px solid #1e3a5f;">
        <p style="color:#93c5fd;font-size:0.75rem;font-weight:700;margin:0 0 10px 0;
                  letter-spacing:0.08em;text-transform:uppercase;">
            Architecture
        </p>
        <p style="color:#e2e8f0;font-size:0.92rem;margin:0 0 6px 0;line-height:1.6;">
            <b style="color:#ffffff;">Flow:</b>
            Gradio UI &rarr; Guardrails &rarr; MCP OpenFDA &rarr; AI Gateway &rarr; Bedrock &rarr; Clinical Answer
        </p>
        <p style="color:#e2e8f0;font-size:0.92rem;margin:0;line-height:1.6;">
            <b style="color:#ffffff;">Resilience:</b>
            3 retries with backoff &bull; priority model fallback &bull;
            MCP/OpenFDA degradation &bull; AWaRe safety net
        </p>
    </div>
    """)

    # ── WIRING ──────────────────────────────────────────────────────────
    btn_ex1.click(lambda: EXAMPLE_UTI, outputs=query_input)
    btn_ex2.click(lambda: EXAMPLE_PNEUMONIA, outputs=query_input)
    btn_ex3.click(lambda: EXAMPLE_PII, outputs=query_input)

    submit_btn.click(
        fn=safe_run,
        inputs=[query_input, simulate_model_cb, simulate_tool_cb],
        outputs=[logs_output, answer_output],
    )

if __name__ == "__main__":
    demo.launch(share=False, css=CSS, theme=gr.themes.Base())
