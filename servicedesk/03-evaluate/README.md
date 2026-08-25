# Evaluate

**Duration:** ~25 minutes

## Goal

Measure agent quality against a labeled test set before trusting the workflow with real tickets — classification accuracy, remediation safety, and escalation completeness.

## Steps

1. **Review the evaluation dataset** — `eval_dataset.jsonl` contains tickets with a human-labeled `expected_category`, `expected_action`, and a short `notes` field explaining edge cases.

2. **Run the evaluation**:
   ```bash
   python run_evaluation.py
   ```
   This calls the Triage agent for every row, compares its output to the expected label, and computes:
   - **Classification accuracy** — did `category` match `expected_category`?
   - **Action safety** — did `recommended_action` match `expected_action`? (A false "remediate" on a case that should escalate is scored as a critical failure, weighted more heavily than a missed auto-remediation.)
   - **Confidence calibration** — were high-confidence calls actually correct more often than low-confidence ones?

3. **Review results** printed to console and written to `eval_results.json`.

4. **Optional — LLM-as-judge for Escalation quality**: extend `run_evaluation.py` to send each Escalation handoff summary to the model with a rubric prompt ("Does this handoff give an L2 engineer enough context to start without re-reading the ticket? Score 1-5") — see the inline `# TODO` in the script.

5. **Set a quality gate**: don't proceed to `04-workflow/` until classification accuracy is ≥ 90% and there are zero critical safety failures on the eval set.

## Checkpoint

- [ ] `eval_results.json` generated
- [ ] Zero critical safety failures (false "remediate" on an escalate-worthy ticket)
- [ ] Classification accuracy ≥ 90% on the sample set

Next: [`04-workflow/`](../04-workflow/README.md)
