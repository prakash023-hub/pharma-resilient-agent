"""
PharmaGuard Resilient Agent — Gradio demo for TrueFoundry hackathon.
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import gradio as gr

from src.agent_core import run_pharma_agent
from src.formatting import format_clinical_answer, empty_clinical_panel

# RULE: never white/light text on light background — dark text + colored panels
CSS = """
.gradio-container {
    max-width: 1240px !important;
    background: #e2e8f0 !important;
}
footer { display: none !important; }

/* All form labels — dark */
.gradio-container label span,
.gradio-container .block label {
    color: #0f172a !important;
    font-weight: 600 !important;
}

/* Query input */
.gradio-container textarea,
.gradio-container input[type="text"] {
    color: #0f172a !important;
    background: #fef3c7 !important;
    border: 2px solid #d97706 !important;
}

/* Logs — light green panel, dark text */
#pg-logs textarea, #pg-logs input {
    font-family: Menlo, Monaco, Consolas, monospace !important;
    font-size: 13px !important;
    line-height: 1.6 !important;
    background: #ecfdf5 !important;
    color: #064e3b !important;
    border: 2px solid #059669 !important;
    border-radius: 0 0 8px 8px !important;
    min-height: 400px !important;
}

/* Clinical answer — light blue panel, dark text */
#pg-answer textarea, #pg-answer input {
    font-family: Inter, Arial, sans-serif !important;
    font-size: 15px !important;
    line-height: 1.7 !important;
    background: #dbeafe !important;
    color: #1e3a8a !important;
    border: 2px solid #2563eb !important;
    border-radius: 0 0 8px 8px !important;
    min-height: 400px !important;
    font-weight: 500 !important;
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
        return (
            str(exc),
            "CONFIGURATION ERROR\n-------------------\n\nSet TFY_API_KEY in your .env file.",
        )
    except Exception as exc:
        return (
            f"Unexpected error: {exc}",
            "ERROR\n-----\n\nAgent failed. Check logs and TrueFoundry connectivity.",
        )


with gr.Blocks(title="PharmaGuard | TrueFoundry Hackathon") as demo:
    gr.HTML(
        """
        <div style="background:linear-gradient(135deg,#1e3a8a,#2563eb);
                    border-radius:14px;padding:22px;margin-bottom:14px;
                    border:3px solid #1d4ed8;">
            <h1 style="color:#fef08a;font-size:1.9rem;margin:0;font-weight:800;">
                PharmaGuard Resilient Agent
            </h1>
            <p style="color:#bfdbfe;margin:8px 0 0;font-size:0.95rem;">
                TrueFoundry Hackathon 2026 | AWaRe 2023 | AWS Bedrock
            </p>
            <div style="display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;">
                <span style="background:#166534;color:#bbf7d0;padding:5px 12px;border-radius:20px;font-size:0.8rem;font-weight:700;">AI Gateway</span>
                <span style="background:#7c2d12;color:#fed7aa;padding:5px 12px;border-radius:20px;font-size:0.8rem;font-weight:700;">MCP Gateway</span>
                <span style="background:#581c87;color:#e9d5ff;padding:5px 12px;border-radius:20px;font-size:0.8rem;font-weight:700;">Guardrails</span>
                <span style="background:#991b1b;color:#fecaca;padding:5px 12px;border-radius:20px;font-size:0.8rem;font-weight:700;">Fallback</span>
            </div>
        </div>
        """
    )

    with gr.Row():
        with gr.Column(scale=5):
            gr.HTML(
                '<p style="color:#0f172a;font-size:1.1rem;font-weight:800;margin:0 0 6px;">'
                "Patient Clinical Query</p>"
            )
            query_input = gr.Textbox(
                label="Clinical query",
                value=EXAMPLE_UTI,
                lines=3,
            )

            gr.HTML(
                '<p style="color:#92400e;font-size:0.9rem;font-weight:700;margin:10px 0 6px;">'
                "Quick examples (click button):</p>"
            )
            with gr.Row():
                btn_ex1 = gr.Button("1. UTI + CrCl 45", size="sm")
                btn_ex2 = gr.Button("2. Pneumonia", size="sm")
                btn_ex3 = gr.Button("3. PII block", size="sm", variant="stop")

            gr.HTML(
                '<p style="color:#0f172a;font-size:1.1rem;font-weight:800;margin:14px 0 6px;">'
                "Resilience Demo Modes</p>"
            )
            with gr.Row():
                simulate_model_cb = gr.Checkbox(
                    label="2. Model fail — first checkbox",
                    value=False,
                )
                simulate_tool_cb = gr.Checkbox(
                    label="3. Tool fail — second checkbox",
                    value=False,
                )

            submit_btn = gr.Button("Run PharmaGuard Agent", variant="primary", size="lg")

        with gr.Column(scale=2):
            gr.HTML(
                """
                <div style="background:#fce7f3;border:3px solid #db2777;
                            border-radius:12px;padding:16px;">
                    <p style="color:#831843;font-size:1rem;font-weight:800;margin:0 0 10px;">
                        Demo Scenarios
                    </p>
                    <p style="color:#9d174d;font-size:0.9rem;line-height:1.7;margin:0;">
                        <b style="color:#500724;">1. Normal</b> — no checkboxes<br>
                        <b style="color:#500724;">2. Model fail</b> — first checkbox<br>
                        <b style="color:#500724;">3. Tool fail</b> — second checkbox<br>
                        <b style="color:#500724;">4. PII block</b> — PII button
                    </p>
                </div>
                """
            )

    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML(
                '<div style="background:#065f46;color:#a7f3d0;font-weight:800;'
                'padding:10px 14px;border-radius:8px 8px 0 0;font-size:0.95rem;">'
                "Agent Execution Logs</div>"
            )
            logs_output = gr.Textbox(
                label="Logs",
                lines=22,
                max_lines=30,
                buttons=["copy"],
                elem_id="pg-logs",
                interactive=False,
                value="Logs appear here after you click Run PharmaGuard Agent...",
            )
        with gr.Column(scale=1):
            gr.HTML(
                '<div style="background:#1e40af;color:#bfdbfe;font-weight:800;'
                'padding:10px 14px;border-radius:8px 8px 0 0;font-size:0.95rem;">'
                "Clinical Recommendation</div>"
            )
            answer_output = gr.Textbox(
                label="Clinical answer",
                lines=22,
                max_lines=30,
                buttons=["copy"],
                elem_id="pg-answer",
                interactive=False,
                value=empty_clinical_panel(),
            )

    gr.HTML(
        """
        <div style="background:#fef9c3;border:3px solid #ca8a04;
                    border-radius:12px;padding:16px;margin-top:14px;">
            <p style="color:#713f12;font-size:0.85rem;font-weight:800;margin:0;
                      text-transform:uppercase;letter-spacing:0.05em;">
                Architecture
            </p>
            <p style="color:#422006;font-size:0.95rem;margin:8px 0 0;line-height:1.6;">
                <b>Flow:</b> Gradio UI → Guardrails → MCP OpenFDA → AI Gateway → Bedrock → Clinical Answer
            </p>
            <p style="color:#422006;font-size:0.95rem;margin:8px 0 0;">
                <b>Resilience:</b> retries, fallback, MCP degradation, AWaRe safety net
            </p>
        </div>
        """
    )

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
