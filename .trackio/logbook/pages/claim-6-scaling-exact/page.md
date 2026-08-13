# Claim 6 — exact scaling audit

The exact Claim 6 audit tests the paper's `O(1/epsilon^2)` detection-time
claim rather than only checking that detection time decreases.

- Source Grid Soccer fit: slope `-1.855`, `R²=.99399`.
- Source Predator-Prey fit: slope `-1.994`, `R²=.99961`.
- Fresh paper-environment mixture fit: slope `-2.030`, `R²=.99830`.
- Five true epsilon values are off the monitor grid.
- Scrambled, reversed, constant-time, and inverse-linear controls fail.

The primary implementation is
`repro/src/verify_claim6_scaling_exact.py`; the separate standard-library
auditor is `repro/src/audit_claim6_scaling_exact.py`. The compact result is
`outputs/claim6_scaling_audit.json`.
