# PharmaGuard Resilient Agent

[![Hackathon](https://img.shields.io/badge/Hackathon-TrueFoundry%20Resilient%20Agents-0066cc)](https://luma.com/tfy-resilient-agents-online-hack)
[![Stack](https://img.shields.io/badge/AWS-Bedrock-orange)](https://aws.amazon.com/bedrock/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)

**Resilient clinical antibiotic agent** for the [TrueFoundry Resilient Agents Hackathon](https://luma.com/tfy-resilient-agents-online-hack).

An antibiotic stewardship agent that **keeps working** when models fail, tools break, or unsafe patient data appears in the prompt.

**Author:** Prakash Raj  
**Repo:** https://github.com/prakash023-hub/pharma-resilient-agent

---

## Demo video

Add your link after recording:

`https://youtu.be/YOUR_VIDEO_ID`

Recording guide: [docs/DEMO_VIDEO_PROCEDURE.md](docs/DEMO_VIDEO_PROCEDURE.md)

---

## Problem

Clinical teams need fast antibiotic guidance, but production agents crash when:

- LLM providers rate-limit or time out
- FDA / tool APIs fail mid-request
- PII accidentally enters the prompt

## Solution

PharmaGuard uses **TrueFoundry AI Gateway**, **MCP Gateway**, and **Guardrails** with graceful degradation at every step.

```
Gradio UI
   │
   ├─► Guardrails (local + pharma-safety-guardrails/pii-redact-pharma)
   ├─► MCP Gateway (openfda-drug-server) → OpenFDA HTTP fallback
   └─► AI Gateway Virtual Model (Nova Micro → Llama4-Scout fallback)
          └─► AWaRe clinical recommendation + renal dosing
```

## TrueFoundry stack (configured)

| Component | Implementation |
|-----------|----------------|
| **AI Gateway** | AWS Bedrock us-east-1 |
| **Virtual Model** | `pharma-resilient-gateway/primary-nova` |
| **Fallback** | Amazon Nova Micro → Meta Llama4-Scout |
| **MCP Gateway** | `openfda-drug-server` → `https://mcp.openfda.gov/mcp` |
| **Guardrails** | `pharma-safety-guardrails/pii-redact-pharma` |

## Resilience demos

| Scenario | How to trigger | Result |
|----------|----------------|--------|
| Normal | Run without checkboxes | Full clinical answer |
| Model failure | "Simulate model failure" checkbox | 403 → virtual model recovers |
| Tool failure | "Simulate tool failure" checkbox | AWaRe guidance without FDA |
| PII block | Query with SSN | Blocked before LLM/MCP |
| Total outage | All retries fail | WHO AWaRe fallback link |

## Quick start

```bash
git clone https://github.com/prakash023-hub/pharma-resilient-agent.git
cd pharma-resilient-agent
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Add TFY_API_KEY and other values to .env
python agent.py
```

Open **http://localhost:7860**

### Verify TrueFoundry config

```bash
python scripts/configure_tfy.py
```

## Example queries

```
Amoxicillin for UTI in 65yo patient with CrCl 45
```

```
Amoxicillin for UTI, patient SSN 123-45-6789
```

## Project structure

```
├── agent.py              # Gradio UI
├── src/
│   ├── agent_core.py     # Agent orchestration
│   ├── gateway.py        # AI Gateway client
│   ├── mcp_tools.py      # MCP + OpenFDA fallback
│   ├── guardrails.py     # Safety checks
│   └── formatting.py     # UI formatting
├── mcp_server/           # Optional local MCP server
├── docs/                 # Submission + demo guides
└── scripts/              # Setup verification
```

## Documentation

| Doc | Purpose |
|-----|---------|
| [DEMO_VIDEO_PROCEDURE.md](docs/DEMO_VIDEO_PROCEDURE.md) | Full video recording guide |
| [SUBMISSION.md](docs/SUBMISSION.md) | Hackathon submission text |
| [SUBMIT_NOW.md](docs/SUBMIT_NOW.md) | Copy-paste Discord submission |
| [SETUP_TRUEFOUNDRY.md](docs/SETUP_TRUEFOUNDRY.md) | TrueFoundry console setup |

## Security

- Never commit `.env` or API keys
- Rotate tokens if exposed
- Use TrueFoundry service account tokens for demos

## Hackathon

- **Event:** [Resilient Agents - Online Hackathon](https://luma.com/tfy-resilient-agents-online-hack)
- **Deadline:** June 7, 2026, 11:59 PM PDT
- **Discord:** https://discord.gg/7dHQAsQq66

## License

MIT — built for the TrueFoundry Resilient Agents hackathon.
