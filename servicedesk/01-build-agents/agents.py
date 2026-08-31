"""
agents.py — orchestrates the Triage & Diagnostic agent's decision into
either the Remediation agent or the Escalation & Knowledge agent, without
needing to pipe JSON between separate process invocations.

This is the local (pre-Foundry-workflow) equivalent of the branch described
in 04-workflow/workflow_definition.yaml: Triage runs first, then the
decision's `recommended_action` (and Remediation's own allowlist/confidence
check) determines which downstream agent handles the ticket.

Usage:
    python agents.py --ticket INC0010234
    python agents.py --ticket INC0010238
    python agents.py --all          # run every sample ticket
"""
import argparse
import json

from triage_agent import get_ticket, get_device_context, classify
from remediation_agent import remediate
from escalation_agent import draft_handoff


def run_ticket(ticket_id: str) -> dict:
    """Runs the full Triage -> (Remediation | Escalation) pipeline for one ticket."""
    ticket = get_ticket(ticket_id)
    device_context = get_device_context(ticket["device_id"])
    decision = classify(ticket, device_context)

    payload = {"ticket": ticket, "decision": decision}

    if decision.get("recommended_action") == "remediate":
        outcome = remediate(payload)

        # Remediation applies its own allowlist/confidence check independently
        # of Triage's recommendation. If it refuses, fall through to
        # Escalation rather than silently dropping the ticket — this mirrors
        # the "when in doubt, escalate" default in the workflow definition.
        if outcome.get("status") == "refused":
            handoff = draft_handoff(payload)
            return {
                "ticket_id": ticket_id,
                "path": "triage -> remediation (refused) -> escalation",
                "decision": decision,
                "remediation_result": outcome,
                "handoff_summary": handoff,
            }

        return {
            "ticket_id": ticket_id,
            "path": "triage -> remediation",
            "decision": decision,
            "remediation_result": outcome,
        }

    handoff = draft_handoff(payload)
    return {
        "ticket_id": ticket_id,
        "path": "triage -> escalation",
        "decision": decision,
        "handoff_summary": handoff,
    }


def run_all() -> list[dict]:
    import json as _json
    from pathlib import Path

    data_dir = Path(__file__).resolve().parent.parent / "data"
    with open(data_dir / "sample_tickets.json") as f:
        tickets = _json.load(f)

    return [run_ticket(t["ticket_id"]) for t in tickets]


def main():
    parser = argparse.ArgumentParser(description="Run the service desk agent pipeline.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ticket", help="Run the pipeline for a single ticket ID, e.g. INC0010234")
    group.add_argument("--all", action="store_true", help="Run the pipeline for every sample ticket")
    args = parser.parse_args()

    if args.all:
        results = run_all()
        print(json.dumps(results, indent=2))
    else:
        result = run_ticket(args.ticket)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
