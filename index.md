# EUC AgentOps Hack

**Hands-on Microsoft Foundry labs to build, monitor, evaluate, and deploy a multi-agent AI workflow for enterprise endpoint service desk operations.**

## The Endpoint Service Desk learning path

Welcome to a hands-on lab where you build a real, enterprise-ready multi-agent system for IT service desk automation. You'll design and wire together three specialized agents that triage, remediate, and escalate endpoint incidents — the kind of SCEP certificate failures, Wi-Fi profile drops, and compliance policy conflicts that flood L1 queues in any large device estate.

By the end, you won't just understand how multi-agent systems work — you'll have built one you can trace, evaluate, and deploy.

All lab instructions are also available at the published docs site (see `mkdocs.yml`).

## What you'll learn

This lab walks you through the full lifecycle of building a production-ready multi-agent workflow with [Microsoft Foundry](https://learn.microsoft.com/azure/ai-foundry/):

- **Agent design** — Build three purpose-built agents (Triage & Diagnostic, Remediation, Escalation & Knowledge), each with its own system prompt, tools, and data access
- **Observability** — Instrument agents with OpenTelemetry-based GenAI tracing via Application Insights
- **Quality evaluation** — Run LLM-as-judge evaluations to measure classification accuracy, remediation safety, and escalation quality
- **Multi-agent orchestration** — Wire the three agents into an automated pipeline using the Python SDK and the Foundry portal

This is a **code-first hackathon** — you'll write and run Python throughout. Several steps also have you work in the **Microsoft Foundry portal** to deploy models, review traces, inspect evaluations, and build the workflow visually. Expect to move between your IDE and the portal regularly.

## The scenario

**EndpointOps Inc.** manages a ~6,000-device enterprise estate (Windows, Android, iOS) using Intune, Entra ID, and Microsoft 365. Their L1 service desk is drowning in repetitive tickets — SCEP cert failures, Wi-Fi profile drops, compliance policy conflicts, Autopilot enrollment stalls. You're building the multi-agent system that triages, auto-remediates the safe cases, and escalates the rest with a clean handoff.

Start here: [`servicedesk/README.md`](servicedesk/README.md)

## Lab structure

| # | Stage | Duration | What you'll learn |
|---|---|---|---|
| 0 | **Setup** | 20 min | Provision a Foundry project, deploy a model, verify Graph/Intune auth |
| 1 | **Build Agents** | 40 min | Build the Triage, Remediation, and Escalation agents with tools and system prompts |
| 2 | **Monitor** | 20 min | Enable GenAI tracing with Application Insights |
| 3 | **Evaluate** | 25 min | Run LLM-as-judge evaluations against a test ticket dataset |
| 4 | **Workflow** | 25 min | Orchestrate all three agents into an end-to-end pipeline |

## Prerequisites

- **Azure subscription** with **Contributor** and **Foundry User** access
- A **GitHub account**
- **Python 3.10+** installed locally (pre-installed when using Codespaces)
- **Azure CLI** (`az`) installed (pre-installed when using Codespaces)

## Go deeper

- [What is Microsoft Foundry?](https://learn.microsoft.com/azure/foundry/what-is-foundry)
- [Foundry Agent Service overview](https://learn.microsoft.com/azure/foundry/agents/overview)
- [Trace your agents with Microsoft Foundry](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-setup)
- [Evaluate agentic workflows](https://learn.microsoft.com/azure/foundry/observability/how-to/evaluate-agent)
- [azure-ai-projects SDK Reference](https://learn.microsoft.com/python/api/azure-ai-projects/)

## About

Built by Mayur Makwana (365 Training Lab) as a portfolio / internal-enablement lab for Digital Workplace & EUC AI practice work.

### License

See [LICENSE](LICENSE).
