"""
Triage & Diagnostic agent.

Reads a ticket + device context, classifies it against the known issue
taxonomy, and returns a structured decision for the Remediation or
Escalation agent to act on.

Usage:
    python triage_agent.py --ticket INC0010234
"""
import argparse
import json
import os
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

SYSTEM_PROMPT = """You are the Triage & Diagnostic agent for EndpointOps Inc.'s
service desk. Given a ticket and its device context, classify the issue
against the known taxonomy categories: scep_certificate, wifi_profile,
compliance_policy, autopilot_enrollment, or unknown.

Return ONLY valid JSON with this exact shape:
{
  "category": "<one of the taxonomy categories>",
  "confidence": <float 0.0-1.0>,
  "reasoning": "<one or two sentences>",
  "recommended_action": "<remediate | escalate>"
}

Rules:
- Never return confidence above 0.85 unless the signal clearly matches
  a single known category with no contradictions.
- If device context shows conflicting or unrecognized signals, category
  MUST be "unknown" and recommended_action MUST be "escalate".
"""


def load_json(filename: str) -> dict:
    with open(DATA_DIR / filename) as f:
        return json.load(f)


def get_ticket(ticket_id: str) -> dict:
    tickets = load_json("sample_tickets.json")
    for t in tickets:
        if t["ticket_id"] == ticket_id:
            return t
    raise ValueError(f"Ticket {ticket_id} not found")


def get_device_context(device_id: str) -> dict:
    devices = load_json("device_context.json")
    return devices.get(device_id, {})


def classify(ticket: dict, device_context: dict) -> dict:
    """
    Calls the Foundry-deployed model with SYSTEM_PROMPT + ticket/device
    context and returns the parsed JSON decision.

    Replace the stub below with an azure-ai-projects chat completion call,
    e.g.:

        from azure.ai.projects import AIProjectClient
        from azure.identity import DefaultAzureCredential

        client = AIProjectClient(
            endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
            credential=DefaultAzureCredential(),
        )
        response = client.inference.get_chat_completions_client().complete(
            model=os.environ["FOUNDRY_MODEL_DEPLOYMENT"],
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(
                    {"ticket": ticket, "device_context": device_context}
                )},
            ],
        )
        return json.loads(response.choices[0].message.content)
    """
    raise NotImplementedError(
        "Wire this up to your Foundry model deployment. "
        "See the docstring for the azure-ai-projects call pattern."
    )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--ticket", required=True, help="Ticket ID, e.g. INC0010234")
    args = parser.parse_args()

    ticket = get_ticket(args.ticket)
    device_context = get_device_context(ticket["device_id"])
    decision = classify(ticket, device_context)

    print(json.dumps({"ticket": ticket, "decision": decision}, indent=2))


if __name__ == "__main__":
    main()
