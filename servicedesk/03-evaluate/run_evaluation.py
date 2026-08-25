"""
Runs the Triage & Diagnostic agent against the labeled eval set and reports
classification accuracy, action safety, and confidence calibration.

Usage:
    python run_evaluation.py
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "01-build-agents"))
from triage_agent import get_ticket, get_device_context, classify  # noqa: E402

EVAL_PATH = Path(__file__).resolve().parent / "eval_dataset.jsonl"
RESULTS_PATH = Path(__file__).resolve().parent / "eval_results.json"


def load_eval_set() -> list[dict]:
    rows = []
    with open(EVAL_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def run() -> dict:
    rows = load_eval_set()
    results = []
    correct_category = 0
    critical_safety_failures = 0

    for row in rows:
        ticket = get_ticket(row["ticket_id"])
        device_context = get_device_context(ticket["device_id"])
        decision = classify(ticket, device_context)

        category_match = decision["category"] == row["expected_category"]
        action_match = decision["recommended_action"] == row["expected_action"]
        is_critical_failure = (
            row["expected_action"] == "escalate"
            and decision["recommended_action"] == "remediate"
        )

        if category_match:
            correct_category += 1
        if is_critical_failure:
            critical_safety_failures += 1

        results.append({
            "ticket_id": row["ticket_id"],
            "expected_category": row["expected_category"],
            "actual_category": decision["category"],
            "category_match": category_match,
            "expected_action": row["expected_action"],
            "actual_action": decision["recommended_action"],
            "action_match": action_match,
            "critical_safety_failure": is_critical_failure,
            "confidence": decision["confidence"],
        })

    summary = {
        "total_tickets": len(rows),
        "classification_accuracy": round(correct_category / len(rows), 3),
        "critical_safety_failures": critical_safety_failures,
        "results": results,
    }

    # TODO: extend this with an LLM-as-judge pass over Escalation handoff
    # summaries, scoring completeness on a 1-5 rubric. See 03-evaluate/README.md.

    return summary


def main():
    summary = run()
    with open(RESULTS_PATH, "w") as f:
        json.dump(summary, f, indent=2)

    print(f"Classification accuracy: {summary['classification_accuracy']:.1%}")
    print(f"Critical safety failures: {summary['critical_safety_failures']}")
    print(f"Full results written to {RESULTS_PATH}")


if __name__ == "__main__":
    main()
