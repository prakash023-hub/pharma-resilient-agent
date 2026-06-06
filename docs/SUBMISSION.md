# Hackathon Submission — PharmaGuard Resilient Agent

---

## Project name

**PharmaGuard Resilient Agent**

## Tagline

Resilient clinical antibiotic agent — survives model outages, tool failures, and unsafe patient input.

## Links

- **GitHub:** https://github.com/prakash023-hub/pharma-resilient-agent
- **Demo video:** YOUR_VIDEO_URL (add after recording)

## Problem

Antibiotic stewardship AI breaks in production when:

- Bedrock / LLM providers rate-limit or timeout
- OpenFDA or other tools fail mid-request
- PII accidentally enters the clinical prompt

## Solution

PharmaGuard is a production-style resilient agent that:

1. **Guardrails** — blocks PII/PHI (local pre-check + TrueFoundry guardrails)
2. **MCP Gateway** — OpenFDA drug lookup with HTTP fallback
3. **AI Gateway** — virtual model with priority fallback (Nova → Llama)
4. **Graceful degradation** — AWaRe guidelines when tools or models fail

## TrueFoundry stack

| Component | Implementation |
|-----------|----------------|
| **AI Gateway** | AWS Bedrock us-east-1 — Nova Micro + Llama4-Scout |
| **Virtual Model** | `pharma-resilient-gateway/primary-nova` |
| **MCP Gateway** | `openfda-drug-server` → `https://mcp.openfda.gov/mcp` |
| **Guardrails** | `pharma-safety-guardrails/pii-redact-pharma` |

## Resilience demos

| Scenario | Trigger | Result |
|----------|---------|--------|
| Normal | No checkboxes | Full clinical answer |
| Model failure | Model checkbox | Fallback recovers |
| Tool failure | Tool checkbox | AWaRe-only answer |
| PII block | SSN in query | Blocked before LLM |

## Team

Prakash Raj

## Built with

Python · Gradio · TrueFoundry AI Gateway · MCP Gateway · Guardrails · AWS Bedrock · OpenFDA · WHO AWaRe 2023
