# Known issue taxonomy

The Triage & Diagnostic agent classifies every ticket against this taxonomy. Each category has a typical root cause, a confidence signal to look for, and a default remediation risk tier.

## 1. SCEP certificate failure (`scep_certificate`)
- **Signal**: `scep_status: failed`, error codes in the `0x8009xxxx` range, dependent Wi-Fi/VPN profiles also failing
- **Typical root cause**: NDES connector unreachable, expired CA template, device clock skew
- **Default risk tier**: Low (safe to auto-remediate via device sync + cert redeploy)

## 2. Wi-Fi profile issue (`wifi_profile`)
- **Signal**: profile version mismatch between device and latest assigned policy
- **Typical root cause**: stale profile cached on device after a policy update
- **Default risk tier**: Low (safe to auto-remediate via profile redeploy)

## 3. Compliance policy conflict / stale report (`compliance_policy`)
- **Signal**: device meets requirements locally but Intune reports noncompliant; `compliance_report_stale: true`
- **Typical root cause**: stale compliance report, or genuine conflicting policy assignment from overlapping dynamic groups
- **Default risk tier**: Medium — auto-remediate only the "stale report" case (force compliance re-evaluation); conflicting-policy cases require escalation

## 4. Autopilot enrollment stall (`autopilot_enrollment`)
- **Signal**: `enrollment_stalled_minutes` above threshold (typically >45 min) at a known ESP stage
- **Typical root cause**: app/policy blocking ESP, network timeout during provisioning
- **Default risk tier**: Medium (remediation possible but time-sensitive; escalate if stalled >90 min)

## 5. Unknown / novel pattern (`unknown`)
- **Signal**: doesn't match an existing category, or matches multiple categories with contradictory signals
- **Default risk tier**: Always escalate — never auto-remediate an unrecognized pattern

> New patterns resolved by L2/L3 should be added back here by the Escalation & Knowledge agent so Triage can recognize them next time.
