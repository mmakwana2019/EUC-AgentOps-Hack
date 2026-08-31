"""
Escalation & Knowledge agent.

Accepts a Triage decision via stdin (JSON) for anything Remediation refused
or that Triage already flagged for escalation. Drafts a structured L2/L3
handoff and (for genuinely novel patterns) appends a new entry to the
known issue taxonomy so future Triage runs recognize it.

Usage:
    python triage_agent.py --ticket INC0010238 | python escalation_agent.py
"""
import json
import sys
from pathlib import Path

TAXONOMY_PATH = Path(__file__).resolve().parent.parent / "data" / "known_issue_taxonomy.md"


def draft_handoff(payload: dict) -> str:
    ticket = payload["ticket"]
    decision = payload["decision"]

    return (
        f"## Escalation: {ticket['ticket_id']}\n\n"
        f"**Device:** {ticket['device_id']}\n"
        f"**Subject:** {ticket['subject']}\n\n"
        f"**Triage classification:** {decision['category']} "
        f"(confidence: {decision['confidence']})\n"
        f"**Triage reasoning:** {decision['reasoning']}\n\n"
        f"**Why this needs a human:** confidence below the auto-remediation "
        f"threshold, or the category falls outside the safe-action allowlist.\n\n"
        f"**Suggested starting point for L2/L3:** review device context and "
        f"policy assignments for conflicting or stale state before taking action.\n"
    )


def append_novel_pattern(category_name: str, description: str) -> None:
    """
    Called by an engineer once a genuinely new pattern (category='unknown')
    has been resolved, to feed the learning back into Triage's taxonomy.
    Kept as an explicit, human-triggered step rather than automatic —
    escalation agent drafts the entry, a person approves it.
    """
    entry = f"\n## {category_name}\n\n{description}\n"
    with open(TAXONOMY_PATH, "a") as f:
        f.write(entry)


def main():
    payload = json.load(sys.stdin)
    handoff = draft_handoff(payload)
    print(handoff)


if __name__ == "__main__":
    main()
