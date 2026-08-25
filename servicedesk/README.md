# Scenario: EndpointOps Inc. — AI-powered service desk

## The business problem

EndpointOps Inc. runs a ~6,000-device enterprise estate on Intune, Entra ID, and Microsoft 365. L1 is saturated with repetitive endpoint incidents — SCEP certificate failures, Wi-Fi profile drops, compliance policy conflicts, Autopilot enrollment stalls — each requiring a human to pull device/log context, diagnose root cause, and apply a known fix. MTTR is high, engineers burn time on routine work, and genuinely novel issues get under-investigated.

## The design

Three specialized agents, each with a distinct responsibility, tool access, and risk profile:

| Agent | Responsibility | Key tools / data |
|---|---|---|
| **Triage & Diagnostic** | Classifies incoming tickets against a known issue taxonomy, pulls device/log context, proposes root cause + confidence score | ServiceNow ticket API (read), Microsoft Graph (Intune device/compliance, Entra sign-in logs), Log Analytics/Tanium telemetry, known-issue taxonomy |
| **Remediation** | Executes low-risk, high-confidence fixes directly and logs the action | Microsoft Graph (write-scoped device actions), risk-tiered action allowlist, audit log store |
| **Escalation & Knowledge** | Drafts structured L2/L3 handoffs for low-confidence/novel cases, and writes resolved novel patterns back into the shared knowledge base | ServiceNow escalation queue, knowledge base (write), engineer resolution notes |

Information flow: **Ticket ingestion → Triage & Diagnostic → (branch) Remediation *or* Escalation & Knowledge → Ticket update & reporting**, with a feedback loop from Escalation back into Triage's knowledge base.

See the top-level repo README for the full rationale on why this is a multi-agent design rather than a single agent (safety separation, auditability, specialization, failure isolation, continuous improvement loop).

## Data

- `data/sample_tickets.json` — synthetic tickets across the SCEP/Wi-Fi/compliance/Autopilot categories
- `data/device_context.json` — mock Intune/Entra device and compliance records referenced by ticket `device_id`
- `data/known_issue_taxonomy.md` — the classification taxonomy the Triage agent reasons against

## Path through the lab

1. [`00-setup/`](../00-setup/README.md) — provision your environment
2. [`01-build-agents/`](../01-build-agents/README.md) — build all three agents
3. [`02-monitor/`](../02-monitor/README.md) — add tracing
4. [`03-evaluate/`](../03-evaluate/README.md) — measure quality
5. [`04-workflow/`](../04-workflow/README.md) — orchestrate end to end
