# TrueFoundry Setup Guide for PharmaGuard

Complete these steps in the TrueFoundry console before recording your demo.

## 1. Rotate your API key (if exposed)

If your token appeared in code or chat:

1. TrueFoundry → **Settings → API Keys**
2. Revoke the old token
3. Create a new **Personal Access Token** or **Virtual Account Token**
4. Put it in `.env` as `TFY_API_KEY`

## 2. AI Gateway — Virtual Model with fallback

Create a **priority-based virtual model**:

| Field | Suggested value |
|-------|-----------------|
| Name | `pharma-resilient-gateway/primary-nova` |
| Strategy | Priority-based routing |
| Target 0 (primary) | Amazon Nova Micro on Bedrock |
| Target 1 (fallback) | Meta Llama4-Scout (or your backup model) |
| Retries | Enable on transient errors |

Also create a **broken model** entry for the failure demo:

- Name: `pharma-resilient-gateway/intentionally-broken-model`
- Point to a non-existent or disabled target so the demo checkbox produces a real HTTP error before fallback.

Update `.env`:

```env
TFY_VIRTUAL_MODEL=pharma-resilient-gateway/primary-nova
TFY_BROKEN_MODEL=pharma-resilient-gateway/intentionally-broken-model
```

## 3. MCP Gateway — OpenFDA tool

### Option A: Register the included MCP server

```bash
cd pharmaguard
pip install fastmcp requests
python mcp_server/openfda_server.py
```

Deploy or register the server in TrueFoundry MCP Registry, then copy the gateway URL from the UI.

Example format:

```
https://gateway.truefoundry.ai/mcp/<your-group>/openfda-drug-label/server
```

Set in `.env`:

```env
TFY_MCP_OPENFDA_URL=https://gateway.truefoundry.ai/mcp/your-group/openfda-drug-label/server
```

### Option B: Use a public MCP server

If TrueFoundry provides a pre-registered OpenFDA / web tool, paste that gateway URL instead.

> Without `TFY_MCP_OPENFDA_URL`, the agent degrades to direct OpenFDA HTTP (works, but weaker MCP story for judges).

## 4. Guardrails

In TrueFoundry Guardrails, create or enable:

- **LLM input guardrail** — block PII / PHI (SSN, credit card, passwords)
- **MCP pre-tool guardrail** — validate tool arguments
- **MCP post-tool guardrail** — inspect tool output (optional)

Copy the slugs into `.env`:

```env
TFY_GUARDRAILS_LLM_INPUT=your-group/pii-block
TFY_GUARDRAILS_MCP_PRE=your-group/mcp-input-check
TFY_GUARDRAILS_MCP_POST=your-group/mcp-output-check
```

Test PII block with:

```
Amoxicillin for UTI, patient SSN 123-45-6789
```

## 5. Observability screenshots (for submission)

Capture from TrueFoundry dashboard:

1. Virtual model routing config (primary + fallback targets)
2. One successful gateway request log
3. One fallback or retry event (use the model-failure demo checkbox)
4. MCP tool call audit entry
5. Guardrail block event (PII query)

Add screenshots to your README or submission doc.

## 6. Verify locally

```bash
python scripts/verify_setup.py
python agent.py
```

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `TFY_API_KEY is not set` | Create `.env` from `.env.example` |
| HTTP 401 | Rotate token, check bearer format |
| MCP connection fails | Confirm URL ends with `/server` and token has MCP access |
| Guardrail never triggers | Confirm slugs in `.env` match TrueFoundry UI exactly |
| Fallback demo doesn't show recovery | Ensure broken model actually 404s/500s, virtual model has fallback target |
