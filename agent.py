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

CSS = """
.gradio-container {
    max-width: 1240px !important;
    font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif !important;
}
footer { display: none !important; }

.pg-header {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 55%, #0f3460 100%);
    border-radius: 18px;
    padding: 30px 28px 24px;
    margin-bottom: 18px;
    border: 1px solid #3b82f6;
    box-shadow: 0 8px 32px rgba(15, 23, 42, 0.25);
}
.pg-title { color: #fff; font-size: 2.1rem; margin: 0; font-weight: 800; letter-spacing: -0.02em; }
.pg-subtitle { color: #cbd5e1; margin: 10px 0 0; font-size: 1rem; }
.pg-badges { display: flex; justify-content: center; gap: 8px; margin-top: 16px; flex-wrap: wrap; }
.pg-badge {
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 0.78rem;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.12);
}
.pg-cards {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin: 14px 0 6px;
}
@media (max-width: 900px) { .pg-cards { grid-template-columns: repeat(2, 1fr); } }
.pg-card {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    padding: 12px 14px;
    text-align: left;
}
.pg-card .icon { font-size: 1.3rem; margin-bottom: 4px; }
.pg-card .name { color: #f8fafc; font-weight: 700; font-size: 0.82rem; }
.pg-card .desc { color: #94a3b8; font-size: 0.72rem; margin-top: 2px; line-height: 1.35; }

.pg-section-title {
    color: #0f172a !important;
    font-size: 1.05rem;
    font-weight: 700;
    margin: 0 0 10px 0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.pg-hint {
    color: #64748b;
    font-size: 0.84rem;
    margin: 8px 0 0;
    line-height: 1.45;
}
.pg-panel-label {
    background: #f1f5f9;
    border: 1px solid #e2e8f0;
    border-radius: 10px 10px 0 0;
    padding: 10px 14px;
    color: #334155;
    font-weight: 600;
    font-size: 0.9rem;
    margin-bottom: -1px;
}

#pg-logs textarea {
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace !important;
    font-size: 12.5px !important;
    line-height: 1.55 !important;
    background: #0f172a !important;
    color: #e2e8f0 !important;
    border-radius: 0 0 10px 10px !important;
    border: 1px solid #334155 !important;
    min-height: 420px !important;
}

.pg-footer {
    background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    border-radius: 14px;
    padding: 18px 20px;
    margin-top: 18px;
    border: 1px solid #e2e8f0;
}
.pg-footer .label {
    color: #475569;
    font-size: 0.72rem;
    margin: 0;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 700;
}
.pg-footer p { margin: 6px 0 0; color: #334155; font-size: 0.86rem; line-height: 1.5; }
.pg-flow {
    display: flex; flex-wrap: wrap; gap: 6px; align-items: center;
    margin-top: 8px; font-size: 0.8rem; color: #475569;
}
.pg-flow span {
    background: #fff; border: 1px solid #cbd5e1;
    border-radius: 8px; padding: 4px 10px; font-weight: 600;
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
            '<div style="color:#1e293b;padding:16px;"><strong>Configuration Error</strong><br>'
            "Set <code>TFY_API_KEY</code> in your <code>.env</code> file.</div>",
        )
    except Exception as exc:
        return (
            f"Unexpected error: {exc}",
            '<div style="color:#1e293b;padding:16px;"><strong>Error</strong><br>'
            "Check logs and TrueFoundry connectivity.</div>",
        )


def load_example(text: str):
    return text


with gr.Blocks(title="PharmaGuard | TrueFoundry Hackathon") as demo:
    gr.HTML(
        """
        <div class="pg-header">
            <h1 class="pg-title">💊 PharmaGuard Resilient Agent</h1>
            <p class="pg-subtitle">
                Clinical antibiotic stewardship · WHO AWaRe 2023 ·
                TrueFoundry AI Gateway + MCP + Guardrails · AWS Bedrock
            </p>
            <div class="pg-badges">
                <span class="pg-badge" style="background:#14532d;color:#86efac;">✅ AI Gateway</span>
                <span class="pg-badge" style="background:#1e3a8a;color:#93c5fd;">✅ MCP Gateway</span>
                <span class="pg-badge" style="background:#4c1d95;color:#c4b5fd;">✅ Guardrails</span>
                <span class="pg-badge" style="background:#7f1d1d;color:#fca5a5;">✅ Fallback</span>
            </div>
            <div class="pg-cards">
                <div class="pg-card">
                    <div class="icon">🛡️</div>
                    <div class="name">Guardrails</div>
                    <div class="desc">PII/PHI block · pharma-safety-guardrails</div>
                </div>
                <div class="pg-card">
                    <div class="icon">🔧</div>
                    <div class="name">MCP Tool</div>
                    <div class="desc">openfda-drug-server · HTTP fallback</div>
                </div>
                <div class="pg-card">
                    <div class="icon">🤖</div>
                    <div class="name">Virtual Model</div>
                    <div class="desc">Nova Micro → Llama4-Scout fallback</div>
                </div>
                <div class="pg-card">
                    <div class="icon">🏥</div>
                    <div class="name">Clinical AI</div>
                    <div class="desc">AWaRe dosing · renal adjustment (CrCl)</div>
                </div>
            </div>
        </div>
        """
    )

    with gr.Row():
        with gr.Column(scale=5):
            gr.HTML('<p class="pg-section-title">📋 Patient Clinical Query</p>')
            query_input = gr.Textbox(
                label="",
                value=EXAMPLE_UTI,
                lines=3,
                show_label=False,
                placeholder="Enter antibiotic question with patient context...",
            )

            gr.HTML('<p class="pg-hint"><b>Quick examples</b> — click to load for demo video:</p>')
            with gr.Row():
                btn_ex1 = gr.Button("🩺 UTI + CrCl 45", size="sm")
                btn_ex2 = gr.Button("🫁 Pneumonia allergy", size="sm")
                btn_ex3 = gr.Button("🚫 PII block test", size="sm", variant="stop")

            gr.HTML('<p class="pg-section-title" style="margin-top:14px;">🎬 Resilience Demo Modes</p>')
            with gr.Row():
                simulate_model_cb = gr.Checkbox(
                    label="Simulate model failure (gateway fallback)",
                    value=False,
                )
                simulate_tool_cb = gr.Checkbox(
                    label="Simulate tool failure (OpenFDA down)",
                    value=False,
                )

            gr.HTML(
                '<p class="pg-hint">'
                "💡 <b>Video tip:</b> Run Scenario 1 with both boxes <b>unchecked</b>. "
                "Then enable one checkbox at a time for failure demos."
                "</p>"
            )
            submit_btn = gr.Button("🚀 Run PharmaGuard Agent", variant="primary", size="lg")

        with gr.Column(scale=2):
            gr.HTML(
                """
                <div style="background:#eff6ff;border:1px solid #bfdbfe;border-radius:12px;padding:16px;">
                    <p style="margin:0 0 8px;font-weight:700;color:#1e40af;">📹 Demo Scenarios</p>
                    <p style="margin:0 0 6px;color:#334155;font-size:0.85rem;">
                        <b>1. Normal</b> — no checkboxes<br>
                        <b>2. Model fail</b> — first checkbox<br>
                        <b>3. Tool fail</b> — second checkbox<br>
                        <b>4. PII block</b> — SSN example button
                    </p>
                    <p style="margin:10px 0 0;color:#64748b;font-size:0.78rem;">
                        TrueFoundry Resilient Agents Hackathon 2026
                    </p>
                </div>
                """
            )

    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML('<div class="pg-panel-label">📊 Agent Execution Logs</div>')
            logs_output = gr.Textbox(
                label="",
                lines=22,
                max_lines=30,
                show_label=False,
                buttons=["copy"],
                elem_id="pg-logs",
                interactive=False,
                value="Logs will appear here after you run the agent...",
            )
        with gr.Column(scale=1):
            gr.HTML('<div class="pg-panel-label">💡 Clinical Recommendation</div>')
            answer_output = gr.HTML(value=empty_clinical_panel())

    gr.HTML(
        """
        <div class="pg-footer">
            <p class="label">Architecture Flow</p>
            <div class="pg-flow">
                <span>Gradio UI</span> →
                <span>Guardrails</span> →
                <span>MCP OpenFDA</span> →
                <span>AI Gateway</span> →
                <span>Bedrock Nova/Llama</span> →
                <span>Clinical Answer</span>
            </div>
            <p style="margin-top:12px;">
                <b>Resilience:</b> 3 retries · priority fallback · MCP/OpenFDA degradation · AWaRe safety net
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
    demo.launch(share=False, css=CSS, theme=gr.themes.Soft())
