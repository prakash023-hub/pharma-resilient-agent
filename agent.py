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

PHARMA_THEME = gr.themes.Base(primary_hue="blue").set(
    body_background_fill="#f1f5f9",
    body_text_color="#1e293b",
    block_background_fill="#ffffff",
    block_border_color="#cbd5e1",
    block_label_text_color="#1e293b",
    block_title_text_color="#0f2744",
    input_background_fill="#ffffff",
    button_primary_background_fill="#1d4ed8",
    button_primary_text_color="#ffffff",
)

CSS = """
/* ── Page — full width / full screen ── */
html, body {
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    background: #f1f5f9 !important;
}
.gradio-container {
    max-width: 100% !important;
    width: 100% !important;
    padding: 12px 20px 20px !important;
    background: #f1f5f9 !important;
    font-family: "Segoe UI", Inter, system-ui, sans-serif !important;
}
.gradio-container .wrap,
.gradio-container .contain,
.gradio-container main {
    max-width: 100% !important;
    width: 100% !important;
}
footer { display: none !important; }

/* ── Gradio 6 form blocks — force light panels ── */
.gradio-container .form,
.gradio-container .form .block,
.gradio-container .block {
    background: #ffffff !important;
    color: #1e293b !important;
    border-color: #cbd5e1 !important;
}

/* ── All labels & checkbox text — force dark ── */
.gradio-container label,
.gradio-container label span,
.gradio-container .label-wrap span,
.gradio-container .label-text,
.gradio-container .form-checkbox-label,
.gradio-container .checkbox-container,
.gradio-container fieldset span {
    color: #1e293b !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
}

/* ── Checkboxes — visible box + light card ── */
.gradio-container input[type="checkbox"] {
    width: 18px !important;
    height: 18px !important;
    accent-color: #2563eb !important;
    cursor: pointer !important;
}
.gradio-container .checkbox-container {
    background: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 8px !important;
    padding: 10px 14px !important;
    margin: 4px 0 !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
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
    min-height: calc(100vh - 560px) !important;
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
    min-height: calc(100vh - 560px) !important;
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

/* ── Four demo scenario buttons — bold colors for judges ── */
#btn-scenario-1 {
    background: #1d4ed8 !important;
    color: #ffffff !important;
    border: 2px solid #1e3a8a !important;
    font-weight: 700 !important;
}
#btn-scenario-2 {
    background: #b45309 !important;
    color: #ffffff !important;
    border: 2px solid #92400e !important;
    font-weight: 700 !important;
}
#btn-scenario-3 {
    background: #6d28d9 !important;
    color: #ffffff !important;
    border: 2px solid #5b21b6 !important;
    font-weight: 700 !important;
}
#btn-scenario-4 {
    background: #b91c1c !important;
    color: #ffffff !important;
    border: 2px solid #991b1b !important;
    font-weight: 700 !important;
}
#btn-scenario-1:hover { background: #1e40af !important; }
#btn-scenario-2:hover { background: #92400e !important; }
#btn-scenario-3:hover { background: #5b21b6 !important; }
#btn-scenario-4:hover { background: #991b1b !important; }

/* ── Scenario status banner ── */
#pg-scenario-status textarea {
    background: #eff6ff !important;
    color: #1e3a8a !important;
    border: 2px solid #3b82f6 !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    text-align: center !important;
}
"""

EXAMPLE_UTI = "Amoxicillin for UTI in 65yo patient with CrCl 45"
EXAMPLE_PII = "Amoxicillin for UTI, patient SSN 123-45-6789"

SCENARIO_STATUS = {
    1: "SCENARIO 1 — Normal path loaded. No failure modes. Click [Run PharmaGuard Agent].",
    2: "SCENARIO 2 — Model failure mode ON. Gateway will failover to backup model. Click Run.",
    3: "SCENARIO 3 — Tool failure mode ON. OpenFDA will degrade gracefully. Click Run.",
    4: "SCENARIO 4 — PII block query loaded. Guardrails should block before model call. Click Run.",
}


def load_scenario_1():
    return EXAMPLE_UTI, False, False, SCENARIO_STATUS[1]


def load_scenario_2():
    return EXAMPLE_UTI, True, False, SCENARIO_STATUS[2]


def load_scenario_3():
    return EXAMPLE_UTI, False, True, SCENARIO_STATUS[3]


def load_scenario_4():
    return EXAMPLE_PII, False, False, SCENARIO_STATUS[4]


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


with gr.Blocks(
    title="PharmaGuard — TrueFoundry Hackathon",
    fill_width=True,
    fill_height=True,
) as demo:

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
            <p style="color:#0f2744;font-size:1rem;font-weight:700;
                      margin:12px 0 10px 0;border-bottom:2px solid #3b82f6;
                      padding-bottom:6px;display:inline-block;">
                Demo Scenarios — Click One, Then Run
            </p>
            """)
            with gr.Row():
                btn_s1 = gr.Button(
                    "1 — Normal Path",
                    size="lg",
                    elem_id="btn-scenario-1",
                )
                btn_s2 = gr.Button(
                    "2 — Model Failure",
                    size="lg",
                    elem_id="btn-scenario-2",
                )
            with gr.Row():
                btn_s3 = gr.Button(
                    "3 — Tool Failure",
                    size="lg",
                    elem_id="btn-scenario-3",
                )
                btn_s4 = gr.Button(
                    "4 — PII Block",
                    size="lg",
                    elem_id="btn-scenario-4",
                )

            scenario_status = gr.Textbox(
                label="",
                show_label=False,
                value=SCENARIO_STATUS[1],
                interactive=False,
                elem_id="pg-scenario-status",
                lines=2,
            )

            gr.HTML("""
            <p style="color:#0f2744;font-size:1rem;font-weight:700;
                      margin:16px 0 8px 0;border-bottom:2px solid #3b82f6;
                      padding-bottom:6px;display:inline-block;">
                Active Failure Modes
            </p>
            <p style="color:#64748b;font-size:0.82rem;margin:0 0 8px 0;">
                Auto-set by scenario buttons above. Scenario 2 = model failure. Scenario 3 = tool failure.
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
                    <tr style="background:#dbeafe;">
                        <td style="padding:8px 10px;color:#1e3a8a;font-weight:800;
                                   border:1px solid #93c5fd;width:36px;">1</td>
                        <td style="padding:8px 10px;color:#0f172a;border:1px solid #93c5fd;">
                            <b style="color:#1d4ed8;">Normal path</b> — blue button, then Run
                        </td>
                    </tr>
                    <tr style="background:#ffedd5;">
                        <td style="padding:8px 10px;color:#9a3412;font-weight:800;
                                   border:1px solid #fdba74;">2</td>
                        <td style="padding:8px 10px;color:#0f172a;border:1px solid #fdba74;">
                            <b style="color:#c2410c;">Model failure</b> — orange button, then Run
                        </td>
                    </tr>
                    <tr style="background:#ede9fe;">
                        <td style="padding:8px 10px;color:#5b21b6;font-weight:800;
                                   border:1px solid #c4b5fd;">3</td>
                        <td style="padding:8px 10px;color:#0f172a;border:1px solid #c4b5fd;">
                            <b style="color:#6d28d9;">Tool failure</b> — purple button, then Run
                        </td>
                    </tr>
                    <tr style="background:#fee2e2;">
                        <td style="padding:8px 10px;color:#991b1b;font-weight:800;
                                   border:1px solid #fca5a5;">4</td>
                        <td style="padding:8px 10px;color:#0f172a;border:1px solid #fca5a5;">
                            <b style="color:#b91c1c;">PII block</b> — red button, then Run
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
    scenario_outputs = [query_input, simulate_model_cb, simulate_tool_cb, scenario_status]
    btn_s1.click(load_scenario_1, outputs=scenario_outputs)
    btn_s2.click(load_scenario_2, outputs=scenario_outputs)
    btn_s3.click(load_scenario_3, outputs=scenario_outputs)
    btn_s4.click(load_scenario_4, outputs=scenario_outputs)

    submit_btn.click(
        fn=safe_run,
        inputs=[query_input, simulate_model_cb, simulate_tool_cb],
        outputs=[logs_output, answer_output],
    )

if __name__ == "__main__":
    demo.launch(share=False, css=CSS, theme=PHARMA_THEME)
