# Complete Demo Video Procedure — PharmaGuard

**Total time:** ~45 minutes (setup 10 min + recording 20 min + upload 15 min)  
**Video length:** 2 minutes 45 seconds – 3 minutes  
**Deadline:** June 7, 2026, 11:59 PM PDT

---

## Part 1 — Before you record (10 min)

### 1. Start the app
```bash
cd /Users/prakashrajk/Projects/braillevision-2026/pharmaguard
source .venv/bin/activate
python agent.py
```
Open **http://localhost:7860**

### 2. Browser setup
- Zoom to **125%** (Cmd + Plus) so logs are readable on video
- Close extra tabs
- Full screen or clean window (hide bookmarks bar)
- Dark menu bar optional — app has its own header

### 3. Recording tool (pick one)
| Tool | Mac steps |
|------|-----------|
| **QuickTime** | File → New Screen Recording → select browser window |
| **OBS** | Free, add Display Capture → 1080p |
| **Loom** | Chrome extension — easiest upload |

**Settings:** 1080p, microphone ON, system sounds OFF

### 4. Test mic (say this once)
> "PharmaGuard — resilient clinical agent for the TrueFoundry hackathon."

---

## Part 2 — Record 4 scenarios (one continuous take or 4 clips)

Use the **Quick example buttons** in the UI — they load the right query for you.

---

### Scenario 1 — Normal path (0:00 – 1:00)

| Step | Action |
|------|--------|
| 1 | Show app header (pause 2 sec on badges) |
| 2 | **Uncheck both** demo checkboxes |
| 3 | Click **🩺 UTI + CrCl 45** button (or use pre-filled query) |
| 4 | Click **🚀 Run PharmaGuard Agent** |

**Say while it runs:**
> "PharmaGuard helps clinicians get antibiotic guidance. It checks guardrails, calls OpenFDA through MCP Gateway, and routes through our TrueFoundry virtual model on AWS Bedrock."

**Point at logs when done:**
- `[GUARDRAIL]` passed
- `[MCP GATEWAY]` or OpenFDA fallback
- `[OK] Primary route succeeded`

**Point at right panel:**
> "We get AWaRe category and renal dose adjustment for CrCl 45."

---

### Scenario 2 — Model failure (1:00 – 1:35)

| Step | Action |
|------|--------|
| 1 | Check **Simulate model failure** only |
| 2 | Uncheck tool failure |
| 3 | Click **Run** again |

**Say:**
> "When the primary model is unavailable, the gateway fails over to our backup model. The clinician still gets an answer — that's resilience."

**Point at logs:**
- `[OK] Primary unavailable as expected (403)`
- `[FAILOVER] Switching to virtual model`
- `[OK] Gateway fallback recovered successfully`

---

### Scenario 3 — Tool failure (1:35 – 2:05)

| Step | Action |
|------|--------|
| 1 | Uncheck model failure |
| 2 | Check **Simulate tool failure** only |
| 3 | Click **Run** |

**Say:**
> "If OpenFDA MCP fails, PharmaGuard degrades gracefully and still produces clinical guidance."

---

### Scenario 4 — PII block (2:05 – 2:35)

| Step | Action |
|------|--------|
| 1 | **Uncheck both** checkboxes |
| 2 | Click **🚫 PII block test** button |
| 3 | Click **Run** |

**Say:**
> "If patient PII like an SSN enters the prompt, guardrails block the request before any model or tool call."

**Point at:**
- `[BLOCKED]` in logs
- Blocked message in clinical panel

---

### Closing (2:35 – 3:00)

**Say:**
> "PharmaGuard — resilient clinical agents on TrueFoundry AI Gateway, MCP Gateway, and Guardrails. GitHub link in the description. Built for the Resilient Agents hackathon."

Show footer architecture flow on screen.

---

## Part 3 — Optional B-roll (30 sec each)

Record separately in TrueFoundry console (https://prakash-ai.truefoundry.cloud):

1. Virtual model `pharma-resilient-gateway/primary-nova` config
2. Guardrails registry `pharma-safety-guardrails/pii-redact-pharma`
3. MCP server `openfda-drug-server`

Cut into video or show as 2-second flashes.

---

## Part 4 — Upload (15 min)

### YouTube (recommended)
1. Upload video → **Unlisted**
2. Title: `PharmaGuard — Resilient Clinical Agent | TrueFoundry Hackathon 2026`
3. Description:
```
PharmaGuard: antibiotic stewardship agent that survives model failures, tool outages, and PII in prompts.

Built with TrueFoundry AI Gateway, MCP Gateway, Guardrails, AWS Bedrock.

GitHub: YOUR_REPO_URL
Hackathon: TrueFoundry Resilient Agents 2026

Stack:
- Virtual model: pharma-resilient-gateway/primary-nova
- Guardrails: pharma-safety-guardrails/pii-redact-pharma
- MCP: openfda-drug-server
```

### Or Loom
- Record → copy link → paste in submission

---

## Part 5 — Submit

1. Discord: https://discord.gg/7dHQAsQq66
2. Channel: `#june-1-2026-resilient-agents-online-hackathon`
3. Copy text from `docs/SUBMISSION.md`
4. Add: GitHub URL + video URL

---

## Checklist before submit

- [ ] Scenario 1 normal path recorded
- [ ] Scenario 2 model fallback recorded
- [ ] Scenario 3 tool failure recorded
- [ ] Scenario 4 PII block recorded
- [ ] GitHub pushed (no `.env` in repo)
- [ ] Video uploaded (Unlisted YouTube or Loom)
- [ ] Submission form filled on Discord
- [ ] LinkedIn post optional (`docs/LINKEDIN_POST.md`)

---

## Common mistakes to avoid

| Mistake | Fix |
|---------|-----|
| Both checkboxes ON for Scenario 1 | Uncheck all for normal demo |
| Logs unreadable | Zoom browser to 125% |
| Clinical panel empty | Wait for Run to finish |
| PII demo doesn't block | Use 🚫 PII block test button |

---

## One-line pitch (memorize)

> "PharmaGuard keeps answering when models fail, tools break, or PII leaks in — built on TrueFoundry gateway fallback, MCP, and guardrails."
