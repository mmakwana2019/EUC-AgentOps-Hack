# Workflow

**Duration:** ~25 minutes

## Goal

Orchestrate the three agents into a single end-to-end pipeline — the branch from Triage into Remediation *or* Escalation, converging into ticket update & reporting — using the Foundry portal's workflow builder plus `workflow_definition.yaml` as the code-first source of truth.

## Steps

1. **Review `workflow_definition.yaml`** — it declares the three agents as nodes, the branch condition out of Triage, and the convergence point.

2. **Import the workflow** in the Foundry portal: *Workflows → Import → select `workflow_definition.yaml`*.

3. **Wire the branch condition**: `recommended_action == "remediate"` routes to the Remediation node; anything else (including `"escalate"` or a parse failure) routes to Escalation & Knowledge. This mirrors the safety-first default from the agent design — when in doubt, escalate rather than act.

4. **Add the convergence step**: both branches write to a shared "Ticket update & reporting" step that updates the ServiceNow ticket and logs a row for the metrics dashboard (auto-resolution rate, MTTR, top root causes).

5. **Test end to end** with all five sample tickets and confirm:
   - INC0010234, INC0010235, INC0010236 → auto-remediated and ticket closed
   - INC0010237, INC0010238 → escalated with a handoff summary attached

6. **Review traces** from stage 2 for the full pipeline run — you should see one end-to-end trace per ticket spanning all agents involved.

## Checkpoint

- [ ] Workflow imported and visible in the Foundry portal
- [ ] Branch condition correctly routes all 5 sample tickets
- [ ] End-to-end trace visible per ticket, spanning Triage → (Remediation | Escalation) → Ticket update

## Wrap-up

You've now built, traced, evaluated, and orchestrated a multi-agent service desk workflow — the same pattern that generalizes to claims processing, manufacturing diagnostics, or any operational domain with a triage → act/escalate → report shape.
