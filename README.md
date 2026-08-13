# ICML 2026 reproduction: Anytime Detection of Strategic Deviations

This repository is an independent reproduction audit of [*Anytime Detection of
Strategic Deviations in Multi-Agent Systems*](https://arxiv.org/abs/2601.05427)
by Etienne Gauthier, Francis Bach, and Michael I. Jordan. It preserves the
released normal-form, Grid Soccer, and Predator-Prey protocols, then checks the
paper's six claim groups with independent calculations and negative controls.

## Paper and result

- Paper: [arXiv:2601.05427v3](https://arxiv.org/abs/2601.05427) ·
  [official PDF](https://arxiv.org/pdf/2601.05427)
- OpenReview: [hXO2OP0T4w](https://openreview.net/forum?id=hXO2OP0T4w)
- Authors: Etienne Gauthier, Francis Bach, and Michael I. Jordan
- Author code: [GauthierE/anytime-detection-deviation](https://github.com/GauthierE/anytime-detection-deviation)
- Pinned author commit:
  `42b8f0edfe76fb9dd006e9cab84f6cb8b75849c6`
- Evidence status: **VERIFIED_SCOPED** — all six claim groups have passing
  evidence at the declared finite protocol scope.
- Evidence-release gate: **PASSED**.
- Strict universal paper-claim gate: **NOT_READY**. Finite experiments,
  source checks, and independent numerical tests do not prove every theorem
  statement or guarantee behavior outside the tested contracts.

This is a reproduction audit, not an author release or an endorsement by the
paper authors. The committed gate record summarizes completed source-scale
runs; the large upstream checkout and executed notebooks are intentionally
ignored, so a clean clone must fetch the pinned source and rerun the protocol
before regenerating those artifacts.

## Claim ledger

| Claim | What the paper claims | How this repository produces the evidence | Current verdict |
| --- | --- | --- | --- |
| C1 | The per-round e-values have the required null expectation under the declared equilibrium. | `repro/src/verify_claims.py::normal_form_identity` exactly enumerates all four deviation e-values on the stated Nash distribution. | **VERIFIED_SCOPED** — maximum mean error `0`. |
| C2 | Anytime monitoring controls false alarms under the null. | `repro/src/verify_claims.py::fwer_control` runs 20,000 independent null trajectories for 1,000 rounds at `lambda=.4`, `alpha=.05`. | **VERIFIED_SCOPED** — FWER `0.0303 <= .05`; this is one finite calibration. |
| C3–C4 | The FDR/BH-style procedure improves detection over the FWER procedure in the normal-form experiment while preserving the paper's monitoring setup. | `repro/src/verify_claims.py::detection_rate_and_fdr` independently simulates 250 alternative trajectories and compares stopping times; the author notebook is checked separately at its released `300 x 4,000` scale. | **VERIFIED_SCOPED** — independent mean stop `1527.844` versus `1747.104`, a `1.144x` speedup. The universal FDR theorem is not re-proved here. |
| C5 | A finite-action mixture likelihood-ratio monitor is mean-one under the null and grows under the alternative. | `repro/src/verify_claims.py::mixture_identity` constructs the mixture directly without importing author notebook code. | **VERIFIED_SCOPED** — null mean `1.0` to machine precision and alternative log-growth `0.236456`. |
| C6 | In the stochastic games, detection time follows the theoretical `O(1/epsilon^2)` scaling, including an unknown-magnitude Predator-Prey mixture. | `verify_claims.py` checks the released source curves; `repro/src/verify_claim6_scaling_exact.py` reruns the paper's 10x10 Predator-Prey protocol with five off-grid true magnitudes; `audit_claim6_scaling_exact.py` independently fits the source curves and runs negative controls. | **VERIFIED_SCOPED** — source slopes `-1.855` and `-1.994`; fresh mixture slope `-2.030`, `R²=.9983`. |

The authoritative compact results are
[outputs/independent_verdict.json](outputs/independent_verdict.json) and
[outputs/claim6_scaling_audit.json](outputs/claim6_scaling_audit.json).
The source-scale gate record is
[outputs/publication_gate.json](outputs/publication_gate.json).

## Reproduce

Use Python 3.12 and a CPU environment:

```bash
git clone https://github.com/GauthierE/anytime-detection-deviation.git upstream
git -C upstream checkout 42b8f0edfe76fb9dd006e9cab84f6cb8b75849c6

uv venv --python 3.12
source .venv/bin/activate
uv pip install numpy scipy matplotlib nashpy tueplots jupyter nbclient pytest

python repro/src/execute_notebook.py upstream/normal-form.ipynb outputs/executed/normal-form.no-tex.executed.ipynb --disable-tex
python repro/src/execute_notebook.py upstream/soccer.ipynb outputs/executed/soccer.no-tex.executed.ipynb --disable-tex
python repro/src/execute_notebook.py upstream/predator-prey.ipynb outputs/executed/predator-prey.no-tex.executed.ipynb --disable-tex
python repro/src/verify_claims.py --require-repeat
python repro/src/verify_claim6_scaling_exact.py
python repro/src/audit_claim6_scaling_exact.py
python -m pytest -q repro/tests/test_verifier.py
```

`--disable-tex` changes only the unavailable Matplotlib text renderer in the
execution copy. It does not change the author algorithms, seeds, numerical
cells, or trial counts. `repro/src/publication_gate.py` is the fail-closed
source-scale gate; it additionally checks both repeated notebook runs, the
independent verifier, the exact Claim 6 audit, tests, and the secret scan.

## Branch guide

The canonical public branch is
[`main`](https://github.com/MachineLearning-Nerd/icml26-anytime-strategic-deviation-detection/tree/main).
It contains the reader-facing README, claim ledger, source manifest, audit
report, gate metadata, verifier code, exact Claim 6 audit, and Trackio logbook.

The original repository had only `main`; there are no `orx/*` or `master`
branches to interpret. Branch cleanup therefore means retaining one readable
`main` branch, setting it as the default, and keeping all reachable commit
identity under `MachineLearning-Nerd`.

## Repository map

- `repro/src/verify_claims.py` — independent C1–C5 checks and released C6 curve checks.
- `repro/src/verify_claim6_scaling_exact.py` — exact fresh C6 Predator-Prey mixture protocol.
- `repro/src/audit_claim6_scaling_exact.py` — separate standard-library C6 audit and negative controls.
- `repro/src/execute_notebook.py` — pinned author-notebook execution with the documented no-TeX fallback.
- `repro/src/publication_gate.py` — fail-closed source-scale evidence gate.
- `repro/tests/` — small regression checks for the independent verifier.
- `pages/claim-6-scaling-exact/` — detailed source, protocol, hash, and exponent audit.
- `docs/EVIDENCE.md` — source-run measurements, controls, and limitations.
- `SOURCE_MANIFEST.md` — paper/source/version provenance.
- `AUDIT_REPORT.md` — claim-by-claim interpretation and evidence boundary.
- `.trackio/logbook/` — experiment narrative and recorded commands.
- `outputs/` — compact verdicts and reproducible evidence summaries. Raw
  notebooks and the fetched upstream checkout are ignored because of size and
  provenance boundaries.

## Citation

```bibtex
@article{gauthier2026anytime,
  title   = {Anytime Detection of Strategic Deviations in Multi-Agent Systems},
  author  = {Gauthier, Etienne and Bach, Francis and Jordan, Michael I.},
  journal = {arXiv preprint arXiv:2601.05427},
  year    = {2026},
  url     = {https://arxiv.org/abs/2601.05427}
}
```

## Thank you

Thank you to Etienne Gauthier, Francis Bach, and Michael I. Jordan for making
the paper, source notebooks, and experimental protocol available for
independent study. This repository is maintained by `MachineLearning-Nerd` as
a transparent reproduction audit and is not affiliated with or endorsed by
the authors.
