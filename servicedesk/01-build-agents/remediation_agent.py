"""
Remediation agent.

Accepts a Triage decision via stdin (JSON). Only acts when the category is
on the safe allowlist AND confidence is above the threshold. Everything
else is refused and should be routed to the Escalation agent instead.

Usage:
    python triage_agent.py --ticket INC0010235 | python remediation_agent.py
"""
import json
import sys
from datetime import datetime, timezone

CONFIDENCE_THRESHOLD = 0.85
SAFE_ALLOWLIST = {"scep_certificate", "wifi_profile"}


def sync_device(device_id: str) -> str:
    """Mock Graph API call: trigger an Intune device sync."""
    return f"[mock] Triggered device sync for {device_id}"


def redeploy_profile(device_id: str) -> str:
    """Mock Graph API call: force redeploy of the affected configuration profile."""
    return f"[mock] Redeployed profile for {device_id}"


ACTIONS = {
    "scep_certificate": sync_device,
    "wifi_profile": redeploy_profile,
}


def remediate(payload: dict) -> dict:
    ticket = payload["ticket"]
    decision = payload["decision"]
    category = decision["category"]
    confidence = decision["confidence"]
    device_id = ticket["device_id"]

    if category not in SAFE_ALLOWLIST or confidence < CONFIDENCE_THRESHOLD:
        return {
            "ticket_id": ticket["ticket_id"],
            "status": "refused",
            "reason": (
                f"category='{category}' confidence={confidence} "
                f"does not meet auto-remediation policy "
                f"(allowlist={sorted(SAFE_ALLOWLIST)}, threshold={CONFIDENCE_THRESHOLD}). "
                "Route to Escalation & Knowledge agent."
            ),
        }

    action_fn = ACTIONS[category]
    result = action_fn(device_id)

    return {
        "ticket_id": ticket["ticket_id"],
        "status": "remediated",
        "action_taken": result,
        "logged_at": datetime.now(timezone.utc).isoformat(),
    }


def main():
    payload = json.load(sys.stdin)
    outcome = remediate(payload)
    print(json.dumps(outcome, indent=2))


if __name__ == "__main__":
    main()
