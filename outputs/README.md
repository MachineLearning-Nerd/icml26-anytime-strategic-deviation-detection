# Output provenance

This directory contains the compact evidence records intended to remain
reviewable in a fresh clone.

| File | Meaning |
| --- | --- |
| `independent_verdict.json` | Independent C1–C5 numerical checks plus released C6 curve checks |
| `claim6_scaling_audit.json` | Exact Claim 6 source fits, fresh off-grid mixture run, and negative controls |
| `publication_gate.json` | Fail-closed source-scale gate record, notebook hashes, and claim-status vector |
| `*.log` | Captured command output for the independent verifier |

The raw upstream checkout and executed notebooks are deliberately ignored by
the repository's `.gitignore`. They are not replaced with unpinned snapshots:
the reproduction commands fetch the author repository and check out the
explicit source commit from `SOURCE_MANIFEST.md`.

The source-scale gate hashes each executed notebook and requires regeneration
of those files before a clean clone can rerun the complete gate. The compact
JSON files are evidence summaries, not a substitute for the source notebook
outputs.

Do not interpret any historical `pass: true` field as a universal theorem
proof. Read the claim verdicts, source pin, and limitations in
`AUDIT_REPORT.md`.
