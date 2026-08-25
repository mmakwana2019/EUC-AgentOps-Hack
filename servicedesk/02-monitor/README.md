# Monitor

**Duration:** ~20 minutes

## Goal

Instrument all three agents with OpenTelemetry GenAI tracing so every classification, remediation action, and escalation is visible in Application Insights — essential once Remediation has write access to production devices.

## Steps

1. **Install tracing dependencies** (already in `requirements.txt`):
   ```
   azure-monitor-opentelemetry
   opentelemetry-sdk
   ```

2. **Get your Application Insights connection string** from the Foundry project's linked resource (*Foundry portal → Tracing → connection string*).

3. **Enable tracing** — see `tracing_setup.py` for the setup call. Import and call `configure_tracing()` at the top of each agent script before any model or Graph calls.

4. **Re-run the three agents** from stage 1 and confirm traces appear:
   ```bash
   python ../01-build-agents/triage_agent.py --ticket INC0010234
   ```
   Then check *Foundry portal → Tracing* for a trace showing the classification call, latency, and token usage.

5. **Add custom spans** around the Remediation agent's action calls (`sync_device`, `redeploy_profile`) so every auto-remediation is individually traceable and auditable — this is the audit trail referenced in the multi-agent design rationale.

## Checkpoint

- [ ] Traces for Triage classification calls appear in the portal
- [ ] Remediation actions show as distinct spans with device ID attached
- [ ] Escalation handoffs are traceable back to the originating ticket

Next: [`03-evaluate/`](../03-evaluate/README.md)
