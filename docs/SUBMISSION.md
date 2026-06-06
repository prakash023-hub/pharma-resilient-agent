# Hackathon Submission — PharmaGuard Resilient Agent

---

## Project name

**PharmaGuard Resilient Agent**

## Tagline

Resilient clinical antibiotic agent — survives model outages, tool failures, and unsafe patient input.

## Problem

Antibiotic stewardship AI breaks in production when:

- Bedrock / LLM providers rate-limit or timeout
- OpenFDA or other tools fail mid-request
- PII accidentally enters the clinical prompt

Clinicians need **reliable** guidance, not demos that crash on the first failure.

## Solution

PharmaGuard is a production-style resilient agent that:

1. **Guardrails** — blocks PII/PHI (local pre-check + TrueFoundry LLM input guardrails)
2. **MCP Gateway** — fetches FDA drug labels via governed OpenFDA tool
3. **AI Gateway** — routes through virtual model with priority fallback (Nova → Llama)
4. **Graceful degradation** — continues with AWaRe guidelines when tools or models fail

## TrueFoundry stack

| Component | Implementation |
|-----------|----------------|
| **AI Gateway** | Virtual model `pharma-resilient-gateway/primary-nova`, retries, priority fallback |
| **MCP Gateway** | `lookup_drug_label` OpenFDA tool via streamable HTTP MCP proxy |
| **Guardrails** | LLM input + MCP pre/post hooks via `X-TFY-GUARDRAILS` |
| **Observability** | Gateway request logs, routing events, tool audit trail |

## Resilience demos (all real — not simulated log text)

| Scenario | Trigger | Result |
|----------|---------|--------|
| Normal | Standard clinical query | MCP + gateway → renal-adjusted recommendation |
| Model failure | Demo checkbox | Broken model unavailable → virtual model recovers |
| Tool failure | Demo checkbox | FDA unavailable → AWaRe-only answer |
| PII block | Query with SSN | Blocked before model/tool execution |
| Total outage | All retries fail | WHO AWaRe fallback link |

## Example queries

```
Amoxicillin for UTI in 65yo patient with CrCl 45
```

```
Best antibiotic for pneumonia in penicillin-allergic patient
```

PII test:

```
Amoxicillin for UTI, patient SSN 123-45-6789
```

## Architecture

```
Gradio UI
  → Guardrails (local + TrueFoundry)
  → MCP Gateway (OpenFDA lookup_drug_label)
  → AI Gateway Virtual Model (Bedrock Nova → Llama fallback)
  → Clinical recommendation + AWaRe degradation path
```

## Links

- **GitHub**: `<ADD YOUR REPO URL>`
- **Demo video**: `<ADD YOUTUBE/LOOM URL>`
- **Live demo**: `<OPTIONAL GRADIO SHARE URL>`

## Team

Prakash Raj

## Built with

Python · Gradio · TrueFoundry AI Gateway · MCP Gateway · Guardrails · AWS Bedrock · OpenFDA · WHO AWaRe 2023
