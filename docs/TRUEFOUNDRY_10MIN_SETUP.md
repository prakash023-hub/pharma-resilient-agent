# TrueFoundry 10-Minute Setup (MCP + Guardrails)

Do this once in the TrueFoundry console to get **full judge score**.

## A. Register OpenFDA MCP Server (5 min)

1. Open TrueFoundry → **MCP Gateway** → **Add MCP Server**
2. Deploy or register the included server:
   ```bash
   cd pharmaguard
   pip install fastmcp requests
   python mcp_server/openfda_server.py
   ```
3. Register URL (cloud deploy or tunnel) with name: `openfda-drug-label`
4. Copy the gateway URL from the UI — looks like:
   ```
   https://gateway.truefoundry.ai/mcp/pharma-resilient-gateway/openfda-drug-label/server
   ```
5. Paste into `.env`:
   ```env
   TFY_MCP_OPENFDA_URL=<paste exact URL>
   ```

## B. Create PII Guardrail (5 min)

1. TrueFoundry → **Guardrails** → **Create Integration**
2. Choose a PII / prompt safety template (or custom guardrail)
3. Name it: `pii-block` under provider group `pharma-resilient-gateway`
4. Copy the **exact slug** shown in the playground code snippet
5. Paste into `.env`:
   ```env
   TFY_GUARDRAILS_LLM_INPUT=<exact-slug-from-ui>
   ```

## C. Verify

```bash
python scripts/configure_tfy.py
```

You want all three `[OK]` lines.

## D. Re-test app

```bash
python agent.py
```

Normal query (no checkboxes) should show:
- `✅ MCP tool call succeeded` OR `✅ OpenFDA data retrieved`
- `✅ Primary route succeeded`
