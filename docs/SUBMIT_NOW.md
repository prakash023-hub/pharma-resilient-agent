# Submit Now — Copy/Paste for Discord

**Deadline:** June 7, 2026, 11:59 PM PDT  
**Discord:** https://discord.gg/7dHQAsQq66  
**Channel:** `#june-1-2026-resilient-agents-online-hackathon`

---

## Before you paste — fill in ONE line

Replace `YOUR_VIDEO_URL` with your YouTube or Loom link after recording.

---

## Submission text (copy everything below)

**Project name:** PharmaGuard Resilient Agent

**Tagline:** Resilient clinical antibiotic agent — survives model outages, tool failures, and unsafe patient input.

**GitHub:** https://github.com/prakash023-hub/pharma-resilient-agent

**Demo video:** YOUR_VIDEO_URL

**Problem:**
Antibiotic stewardship agents crash in production when LLMs timeout, OpenFDA tools fail, or PII enters clinical prompts. Clinicians need reliable guidance, not fragile demos.

**Solution:**
PharmaGuard is a resilient clinical agent built on TrueFoundry AI Gateway, MCP Gateway, and Guardrails. It blocks unsafe input, fetches FDA context via MCP (with HTTP fallback), routes through a virtual model on AWS Bedrock, and degrades gracefully when components fail.

**TrueFoundry stack:**
- AI Gateway: AWS Bedrock us-east-1 (Nova Micro + Llama4-Scout fallback)
- Virtual Model: `pharma-resilient-gateway/primary-nova` (priority routing)
- MCP Gateway: `openfda-drug-server` → `https://mcp.openfda.gov/mcp`
- Guardrails: `pharma-safety-guardrails/pii-redact-pharma` (PII/PHI MUTATE)

**Resilience demonstrated (4 scenarios):**
1. Normal path — guardrails → MCP/OpenFDA → gateway → AWaRe clinical answer with renal dosing
2. Model failure — broken primary model (403) → virtual model fallback recovers
3. Tool failure — OpenFDA unavailable → agent continues with AWaRe guidance
4. PII block — SSN in query blocked before LLM/MCP execution

**Example query:**
`Amoxicillin for UTI in 65yo patient with CrCl 45`

**Built with:**
Python · Gradio · TrueFoundry AI Gateway · MCP Gateway · Guardrails · AWS Bedrock · OpenFDA · WHO AWaRe 2023

**Team:** Prakash Raj

---

## Only 2 steps left

1. **Record video** — follow [DEMO_VIDEO_PROCEDURE.md](DEMO_VIDEO_PROCEDURE.md) (~20 min)
2. **Paste above** into Discord submission form + add video URL

Optional: LinkedIn post → [LINKEDIN_POST.md](LINKEDIN_POST.md) ($1k social prize)
