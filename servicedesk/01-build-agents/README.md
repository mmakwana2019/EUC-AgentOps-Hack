# Build Agents

**Duration:** ~40 minutes

## Goal

Build the three agents that make up the service desk workflow: Triage & Diagnostic, Remediation, and Escalation & Knowledge. Each has its own system prompt, tool set, and data access — deliberately kept separate (see repo root README for why).

## Steps

1. **Review the taxonomy and mock data** the agents will reason over: `../data/known_issue_taxonomy.md`, `../data/sample_tickets.json`, `../data/device_context.json`.

2. **Build the Triage & Diagnostic agent** — open `triage_agent.py`. It:
   - Reads a ticket + device context
   - Classifies against the taxonomy
   - Returns a structured JSON: `{category, confidence, reasoning, recommended_action}`

   Run it:
   ```bash
   python triage_agent.py --ticket INC0010234
   ```

3. **Build the Remediation agent** — open `remediation_agent.py`. It:
   - Accepts only `category` + `confidence` above a safe threshold (default 0.85) and a category on the allowlist (`scep_certificate`, `wifi_profile`)
   - Calls a mocked Graph action (`sync_device()`, `redeploy_profile()`)
   - Logs the action and returns a closure message

4. **Build the Escalation & Knowledge agent** — open `escalation_agent.py`. It:
   - Handles anything below the confidence threshold or outside the allowlist
   - Drafts a structured L2/L3 handoff summary
   - Appends resolved novel patterns back to `known_issue_taxonomy.md`

5. **Wire the three together locally** (before the full Foundry workflow in stage 4):
   ```bash
   python triage_agent.py --ticket INC0010236 | python remediation_agent.py
   python triage_agent.py --ticket INC0010238 | python escalation_agent.py
   ```

## Checkpoint

- [ ] Triage agent correctly classifies all 5 sample tickets
- [ ] Remediation agent refuses to act on the `unknown` category ticket
- [ ] Escalation agent produces a readable handoff summary for INC0010238

Next: [`02-monitor/`](../02-monitor/README.md)
