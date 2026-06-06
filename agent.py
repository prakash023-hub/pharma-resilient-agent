"""
PharmaGuard Resilient Agent — Gradio demo for TrueFoundry hackathon.

Run:
    cd pharmaguard
    cp .env.example .env   # add your TFY_API_KEY
    pip install -r requirements.txt
    python agent.py
"""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

import gradio as gr

from src.agent_core import run_pharma_agent

CSS = """
.gradio-container { max-width: 1200px !important; font-family: 'Inter', sans-serif !important; }
footer { display: none !important; }
"""


def safe_run(query: str, simulate_model_failure: bool, simulate_tool_failure: bool):
    try:
        return run_pharma_agent(
            query,
            simulate_model_failure=simulate_model_failure,
            simulate_tool_failure=simulate_tool_failure,
        )
    except ValueError as exc:
        return str(exc), (
            "⚠️ Configuration error.\n\n"
            "Copy `.env.example` to `.env` and set `TFY_API_KEY`.\n"
            "See `docs/SETUP_TRUEFOUNDRY.md` for gateway, MCP, and guardrail setup."
        )
    except Exception as exc:
        return f"Unexpected error: {exc}", (
            "⚠️ Agent failed unexpectedly. Check logs and TrueFoundry connectivity."
        )


with gr.Blocks(css=CSS, title="PharmaGuard Resilient Agent") as demo:
    gr.HTML(
        """
    <div style="background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                border-radius: 16px; padding: 32px; margin-bottom: 24px;
                text-align: center; border: 1px solid #e94560;">
        <h1 style="color: #ffffff; font-size: 2.2em; margin: 0; font-weight: 700;">
            💊 PharmaGuard Resilient Agent
        </h1>
        <p style="color: #a0aec0; margin: 8px 0 0 0; font-size: 1.1em;">
            Clinical Antibiotic Stewardship · WHO AWaRe 2023 · TrueFoundry + AWS Bedrock
        </p>
        <div style="display: flex; justify-content: center; gap: 16px; margin-top: 16px; flex-wrap: wrap;">
            <span style="background: #1a472a; color: #68d391; padding: 4px 12px; border-radius: 20px; font-size: 0.85em;">✅ AI Gateway</span>
            <span style="background: #1a365d; color: #63b3ed; padding: 4px 12px; border-radius: 20px; font-size: 0.85em;">✅ MCP Gateway</span>
            <span style="background: #44337a; color: #b794f4; padding: 4px 12px; border-radius: 20px; font-size: 0.85em;">✅ Guardrails</span>
            <span style="background: #742a2a; color: #fc8181; padding: 4px 12px; border-radius: 20px; font-size: 0.85em;">✅ Fallback + Retries</span>
        </div>
    </div>
    """
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML('<h3 style="color:#e2e8f0; margin-bottom:8px;">📋 Patient Query</h3>')
            query_input = gr.Textbox(
                label="",
                placeholder=(
                    "e.g. Amoxicillin for UTI in 65yo patient with CrCl 45\n"
                    "e.g. Best antibiotic for pneumonia in penicillin-allergic patient"
                ),
                lines=4,
            )
            simulate_model_cb = gr.Checkbox(
                label="🔴 Demo: Primary model failure → gateway fallback",
                value=False,
            )
            simulate_tool_cb = gr.Checkbox(
                label="🔴 Demo: OpenFDA tool failure → graceful degradation",
                value=False,
            )
            gr.HTML(
                '<p style="color:#718096; font-size:0.85em;">'
                "Demo checkboxes trigger <b>real</b> failure paths — not fake log messages."
                "</p>"
            )
            submit_btn = gr.Button("🚀 Run PharmaGuard Agent", variant="primary", size="lg")

    gr.HTML('<hr style="border-color: #2d3748; margin: 16px 0;">')

    with gr.Row():
        with gr.Column(scale=1):
            gr.HTML('<h3 style="color:#e2e8f0;">📊 Agent Execution Logs</h3>')
            logs_output = gr.Textbox(label="", lines=18, max_lines=24)
        with gr.Column(scale=1):
            gr.HTML('<h3 style="color:#e2e8f0;">💡 Clinical Recommendation</h3>')
            answer_output = gr.Textbox(label="", lines=18, max_lines=24)

    gr.HTML(
        """
    <div style="background:#1a1a2e; border-radius:12px; padding:16px; margin-top:16px;
                border: 1px solid #2d3748; display:flex; gap:32px; flex-wrap:wrap;">
        <div>
            <p style="color:#718096; font-size:0.8em; margin:0;">ARCHITECTURE</p>
            <p style="color:#a0aec0; font-size:0.85em; margin:4px 0 0 0;">
                Gradio UI → Guardrails → MCP Gateway (OpenFDA)<br>
                → AI Gateway Virtual Model → AWS Bedrock
            </p>
        </div>
        <div>
            <p style="color:#718096; font-size:0.8em; margin:0;">RESILIENCE</p>
            <p style="color:#a0aec0; font-size:0.85em; margin:4px 0 0 0;">
                3 retries with backoff · virtual-model fallback<br>
                MCP failure → direct OpenFDA fallback · AWaRe safety message
            </p>
        </div>
        <div>
            <p style="color:#718096; font-size:0.8em; margin:0;">DEMO SCENARIOS</p>
            <p style="color:#a0aec0; font-size:0.85em; margin:4px 0 0 0;">
                1) Normal path · 2) Model failure recovery<br>
                3) Tool failure recovery · 4) PII block (type SSN in query)
            </p>
        </div>
    </div>
    """
    )

    submit_btn.click(
        fn=safe_run,
        inputs=[query_input, simulate_model_cb, simulate_tool_cb],
        outputs=[logs_output, answer_output],
    )

if __name__ == "__main__":
    demo.launch(share=False)
