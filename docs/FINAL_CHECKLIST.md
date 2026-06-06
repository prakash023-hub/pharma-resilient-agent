# PharmaGuard — Final Submission Checklist

Deadline: **June 7, 2026, 11:59 PM PDT**

## 1. Verify full stack (5 min)

```bash
cd /Users/prakashrajk/Projects/braillevision-2026/pharmaguard
source .venv/bin/activate
python scripts/configure_tfy.py
python agent.py
```

Target output from `configure_tfy.py`:

```
[OK] AI Gateway / virtual model (200)
[OK] MCP Gateway (...)
[OK] Guardrail slug '...' (200)
✅ Full stack verified
```

If MCP or guardrails show `[FAIL]`, open TrueFoundry UI and copy the **exact** URL/slug into `.env`, then re-run.

## 2. Record demo video (30 min)

Follow `docs/DEMO_SCRIPT.md` — four scenarios:

- [ ] Normal path (no checkboxes)
- [ ] Model failure checkbox
- [ ] Tool failure checkbox
- [ ] PII block query

Upload to YouTube (Unlisted) or Loom.

## 3. Push GitHub (10 min)

Follow `docs/GITHUB.md`. Confirm `.env` is **not** in the repo.

## 4. Submit (10 min)

- [ ] Join Discord: https://discord.gg/7dHQAsQq66
- [ ] Get submission link from `#june-1-2026-resilient-agents-online-hackathon`
- [ ] Paste content from `docs/SUBMISSION.md`
- [ ] Add GitHub + video links

## 5. LinkedIn (optional — $1k social prize)

Post using `docs/LINKEDIN_POST.md` with video + repo links.

## Judge scorecard — what you now demonstrate

| Criteria | Evidence |
|----------|----------|
| AI Gateway | Virtual model + real fallback demo |
| MCP Gateway | OpenFDA tool via gateway URL |
| Guardrails | LLM input slug + local PII block |
| Resilience | Model fail, tool fail, graceful degradation |
| Usefulness | AWaRe antibiotic + renal dosing |
| Demo clarity | Clean logs, no noisy 403 retries |

## If someone asks "what problem does this solve?"

> Nurses, pharmacists, and caregivers need fast antibiotic guidance, but production agents crash when LLMs timeout, FDA tools fail, or PII leaks into prompts. PharmaGuard keeps answering safely using TrueFoundry gateway fallback, MCP tool degradation, and guardrails.
