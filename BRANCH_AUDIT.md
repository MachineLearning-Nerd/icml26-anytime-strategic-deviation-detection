# Branch audit

## Final branch policy

| Historical ref | Final ref | Purpose |
| --- | --- | --- |
| `main` | `main` | Canonical README, evidence ledger, source manifest, audit report, verifier code, and release metadata |

The original repository had one branch only: `main`. There are no historical
`master`, `orx/*`, or experiment branches to preserve or reinterpret.

## Branch responsibilities

`main` is the complete public reading and reproduction surface. It documents
the six claim paths, the pinned author source, the exact Claim 6 audit,
limitations, citation, thank-you note, and the evidence-release gate.

The fetched author checkout and generated source notebooks live outside Git
under the ignored `upstream/` and `outputs/executed/` paths. They are inputs to
the reproduction, not hidden alternate branches.

## Identity policy

All reachable commits are normalized to:

`MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>`

The paper authors are credited in `README.md` and `SOURCE_MANIFEST.md`; they
are not represented as commit authors.

## Remote cleanup checks

The final remote should satisfy all of the following:

- default branch is `main`;
- exactly one remote branch exists: `main`;
- no `master` or `orx/*` refs remain;
- repository owner is `MachineLearning-Nerd`;
- repository name is `icml26-anytime-strategic-deviation-detection`;
- homepage points to the official arXiv record; and
- the remote tip contains this README, gate metadata, claim ledger, and audit
  files.

Commit history is preserved; only public branch vocabulary and attribution are
normalized for this collection.
