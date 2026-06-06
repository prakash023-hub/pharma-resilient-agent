# PharmaGuard Resilient Agent

**TrueFoundry Resilient Agents Hackathon submission**

An antibiotic stewardship agent that keeps working when models fail, tools break, or unsafe patient data appears in the prompt.

## Problem

Clinical teams need fast antibiotic guidance, but production agents crash when:

- LLM providers rate-limit or time out
- FDA / tool APIs fail mid-request
- PII accidentally enters the prompt

PharmaGuard demonstrates **real resilience** using TrueFoundry AI Gateway, MCP Gateway, and Guardrails.

## Architecture

```
Gradio UI
   │
   ├─► Local PII pre-check
   ├─► TrueFoundry Guardrails (LLM input + MCP hooks)
   ├─► MCP Gateway → OpenFDA drug label tool
   │      └─► fallback: direct OpenFDA HTTP
   └─► AI Gateway Virtual Model (Nova primary → Llama fallback)
          └─► retries + graceful AWaRe degradation message
```

## Resilience scenarios (demo)

| Scenario | How to trigger | Expected behavior |
|----------|----------------|-------------------|
| Normal path | Run without checkboxes | MCP + gateway answer |
| Model failure | Check "Primary model failure" | Broken model fails → virtual model recovers |
| Tool failure | Check "OpenFDA tool failure" | Agent continues with AWaRe-only guidance |
| PII block | Query with `SSN 123-45-6789` | Blocked before model/tool calls |
| All gateway attempts fail | Disconnect network / bad key | WHO AWaRe fallback message |

## Quick start

```bash
cd pharmaguard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env — add TFY_API_KEY and optional MCP/guardrail slugs
python agent.py
```

Open http://localhost:7860

## TrueFoundry setup

See **[docs/SETUP_TRUEFOUNDRY.md](docs/SETUP_TRUEFOUNDRY.md)** for:

- Virtual model with priority-based fallback
- MCP server registration
- Guardrail configuration
- Observability screenshots for your demo

## Project structure

```
pharmaguard/
├── agent.py                 # Gradio demo app
├── src/
│   ├── agent_core.py        # Agent orchestration
│   ├── gateway.py           # AI Gateway client
│   ├── mcp_tools.py         # MCP Gateway + OpenFDA fallback
│   ├── guardrails.py        # Guardrail headers + local pre-check
│   └── config.py            # Environment config
├── mcp_server/
│   └── openfda_server.py    # MCP server to register in TrueFoundry
├── docs/
│   ├── SETUP_TRUEFOUNDRY.md
│   ├── SUBMISSION.md
│   ├── DEMO_SCRIPT.md
│   └── LINKEDIN_POST.md
└── scripts/
    └── verify_setup.py
```

## Security

- **Never commit `.env` or API keys**
- If your token was pasted in chat or hardcoded earlier, **rotate it in TrueFoundry immediately**
- Use a service account / virtual account token for demos

## Hackathon

- Event: [Resilient Agents - Online Hackathon](https://luma.com/tfy-resilient-agents-online-hack)
- Deadline: **June 7, 2026, 11:59 PM PDT**
- Discord: https://discord.gg/7dHQAsQq66

## Stack

| Layer | Technology |
|-------|------------|
| UI | Gradio |
| LLM routing | TrueFoundry AI Gateway + AWS Bedrock |
| Tools | TrueFoundry MCP Gateway + OpenFDA |
| Safety | TrueFoundry Guardrails |
| Language | Python 3.9+ |

## License

MIT — built for the TrueFoundry Resilient Agents hackathon.
