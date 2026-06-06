# 3-Minute Demo Video Script

Record your screen with the Gradio app + optionally TrueFoundry dashboard.

**Total length:** 2:45 – 3:00

---

## 0:00 – 0:20 | Hook

> "Most clinical AI agents crash when the model times out, FDA tools fail, or someone accidentally pastes patient PII. PharmaGuard is a resilient antibiotic stewardship agent built on TrueFoundry AI Gateway, MCP Gateway, and Guardrails — and it keeps working."

Show title screen / app header.

---

## 0:20 – 1:00 | Happy path

**Type:**

```
Amoxicillin for UTI in 65yo patient with CrCl 45
```

**Click:** Run PharmaGuard Agent (no checkboxes)

**Narrate while logs appear:**

> "The agent runs a guardrail check, calls OpenFDA through MCP Gateway, then routes the request through our virtual model on AWS Bedrock. We get a clinical answer with renal dosing context."

Point at: guardrail pass → MCP logs → gateway success → clinical answer.

---

## 1:00 – 1:40 | Model failure recovery

**Check:** "Primary model failure → gateway fallback"

**Click:** Run again (same query)

**Narrate:**

> "Here we deliberately hit a broken model first. The gateway fails, then our virtual model fallback kicks in. The clinician still gets an answer — that's resilience."

Optional: flash TrueFoundry dashboard showing the fallback request.

---

## 1:40 – 2:10 | Tool failure recovery

**Uncheck** model failure. **Check:** "OpenFDA tool failure"

**Click:** Run

**Narrate:**

> "Now the FDA tool is down. PharmaGuard degrades gracefully and still returns AWaRe-aligned guidance instead of crashing."

---

## 2:10 – 2:35 | PII guardrail

**Uncheck all boxes.**

**Type:**

```
Amoxicillin for UTI, patient SSN 123-45-6789
```

**Click:** Run

**Narrate:**

> "If PII enters the prompt, guardrails block the request before any model or tool call. Patient safety is enforced at the gateway."

---

## 2:35 – 3:00 | Close

> "PharmaGuard — resilient clinical agents on TrueFoundry. GitHub and architecture in the description. Built for the Resilient Agents hackathon."

Show: architecture footer in app + GitHub URL overlay.

---

## Recording tips

- Use **QuickTime** (Mac) or **OBS** — 1080p, mic on
- Zoom browser to 125% so logs are readable
- Upload **Unlisted YouTube** or **Loom**
- Add GitHub link in video description

## B-roll to capture separately

- TrueFoundry virtual model config screen (5 sec)
- Gateway request log with fallback (5 sec)
- MCP tool audit entry (5 sec)
