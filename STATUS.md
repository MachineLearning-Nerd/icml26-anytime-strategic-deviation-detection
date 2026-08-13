# Status — hXO2OP0T4w

## Current result

The evidence-release gate is **PASSED** and the six claim groups are
**VERIFIED_SCOPED**. The strict universal paper-claim gate is **NOT_READY**:
the evidence covers the pinned source protocols and finite independent checks,
not every theorem quantifier, environment, or asymptotic regime.

The canonical collection target is
`MachineLearning-Nerd/icml26-anytime-strategic-deviation-detection`, with one
public `main` branch.

## Source contract

- Paper: [arXiv:2601.05427v3](https://arxiv.org/abs/2601.05427).
- OpenReview: `hXO2OP0T4w`.
- Authors: Etienne Gauthier, Francis Bach, and Michael I. Jordan.
- Author repository:
  `GauthierE/anytime-detection-deviation`.
- Pinned commit:
  `42b8f0edfe76fb9dd006e9cab84f6cb8b75849c6`.
- Released source protocols: `normal-form.ipynb`, `soccer.ipynb`, and
  `predator-prey.ipynb`.
- Execution environment: Python 3.12 CPU with NumPy, SciPy, NashPy,
  Matplotlib, Tueplots, Jupyter, nbclient, and pytest.

## Completed evidence

- The three released author notebooks were executed at their recorded source
  scale, with deterministic repeat copies.
- The only execution deviation is the documented `text.usetex=False`
  rendering fallback because the local environment does not provide a system
  `latex` executable. Numerical cells, seeds, algorithms, and trial counts
  are unchanged.
- The independent verifier checks exact C1 e-value identities, a 20,000-run
  null FWER calibration, the C3–C4 stopping-time comparison, the C5 mixture
  likelihood-ratio identity, and released C6 stochastic-game curves.
- The exact C6 audit independently fits the source curves, reruns the
  paper's 10x10 Predator-Prey mixture protocol with 256 trials per epsilon,
  tests five true magnitudes outside the monitor grid, and rejects scrambled
  and inverse-linear controls.
- The fail-closed source-scale gate record reports both complete notebook runs,
  the repeat verifier, four passing verifier tests, and a clean secret scan.
- Compact machine-readable records are committed in `outputs/`. The larger
  upstream checkout and executed notebooks remain ignored; their hashes are
  recorded by the gate and can be regenerated from the source contract.

## Claim vector

| Claim | Verdict | Evidence producer |
| --- | --- | --- |
| C1 | `VERIFIED_SCOPED` | `verify_claims.py::normal_form_identity` |
| C2 | `VERIFIED_SCOPED` | `verify_claims.py::fwer_control` |
| C3 | `VERIFIED_SCOPED` | `verify_claims.py::detection_rate_and_fdr` |
| C4 | `VERIFIED_SCOPED` | `verify_claims.py::detection_rate_and_fdr` plus the source normal-form notebook |
| C5 | `VERIFIED_SCOPED` | `verify_claims.py::mixture_identity` |
| C6 | `VERIFIED_SCOPED` | `verify_claims.py::released_scalings`, `verify_claim6_scaling_exact.py`, and `audit_claim6_scaling_exact.py` |

## Limitations

- Numerical agreement on finite runs is evidence for the declared protocols,
  not a proof of the paper's universal statements.
- The independent verifier is deliberately small and does not replace a
  second complete implementation of every author notebook.
- The Grid Soccer and Predator-Prey source runs emit the paper's empirical
  curves; the exact Claim 6 fresh run uses an algebraically equivalent
  log-wealth calculation to avoid terminal floating-point overflow.
- No multi-hardware, GPU, broader game-family, or production deployment study
  is claimed.
- The author source and raw executed notebooks are fetched/generated locally
  rather than stored in this repository, so the full gate must be rerun after
  a clean checkout.

## Publication and branch state

The repository is intended to be published as
`icml26-anytime-strategic-deviation-detection`. The final public ref policy is
one default `main` branch, no `master` or `orx/*` refs, and reachable commits
attributed to `MachineLearning-Nerd`. See [BRANCH_AUDIT.md](BRANCH_AUDIT.md)
and [SOURCE_MANIFEST.md](SOURCE_MANIFEST.md).
