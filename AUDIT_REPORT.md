# Audit report

## Scope and decision rule

This report evaluates the six claim groups for [arXiv:2601.05427v3](https://arxiv.org/abs/2601.05427).
The audit separates three questions:

1. Did the pinned author protocol execute without an unrecorded code change?
2. Does an independent calculation reproduce the numerical direction or
   identity being checked?
3. Does that evidence justify the paper's full universal statement?

The first two questions pass within the declared scope. The third remains
`NOT_READY` because finite experiments and compact independent checkers do not
replace a complete proof or broad replication.

## Claim 1 — e-value calibration

- **Paper object:** the per-round e-values used to bet against the equilibrium
  null have the required expectation bound.
- **Producer:** `repro/src/verify_claims.py::normal_form_identity`.
- **Method:** exact enumeration over the stated 2x2 Nash distribution and all
  four player/deviation combinations.
- **Recorded result:** maximum absolute mean error `0`.
- **Verdict:** **VERIFIED_SCOPED**.
- **Boundary:** this is an exact check for the declared finite game and
  construction, not a re-proof for every game in the paper.

## Claim 2 — anytime false-alarm control

- **Paper object:** sequential monitoring controls the false discovery/false
  alarm event under the null.
- **Producer:** `repro/src/verify_claims.py::fwer_control`, plus the pinned
  normal-form source notebook.
- **Method:** 20,000 independent null trajectories, 1,000 rounds,
  `lambda=.4`, and `alpha=.05`.
- **Recorded result:** FWER `0.0303`, below `0.05`.
- **Verdict:** **VERIFIED_SCOPED**.
- **Boundary:** one finite Monte Carlo calibration does not establish the
  asymptotic or all-distribution guarantee.

## Claims 3–4 — FDR detection comparison

- **Paper object:** the FDR/BH-style monitor improves detection relative to the
  FWER monitor in the normal-form setting.
- **Producer:** `repro/src/verify_claims.py::detection_rate_and_fdr`, checked
  against the pinned `normal-form.ipynb`.
- **Method:** an independent 250-trajectory alternative simulation compares
  the first stopping times. The author source run retains its released
  300-run by 4,000-round protocol.
- **Recorded result:** independent FDR mean stop `1527.844` versus FWER
  `1747.104`, a `1.144x` speedup. The source run records `1545.4` versus
  `1765.4`.
- **Verdict:** **VERIFIED_SCOPED**.
- **Boundary:** the checker verifies the direction and finite stopping-time
  comparison; it does not re-prove the full FDR theorem or claim universal
  power improvement.

## Claim 5 — mixture likelihood-ratio monitor

- **Paper object:** a mixture monitor has unit null mean and positive growth
  under a declared alternative.
- **Producer:** `repro/src/verify_claims.py::mixture_identity`.
- **Method:** direct finite-action construction of the baseline, alternative,
  five-point mixture, and likelihood ratio without importing the author
  notebook implementation.
- **Recorded result:** null likelihood-ratio mean `1.0` to machine precision;
  alternative log-growth `0.236456`.
- **Verdict:** **VERIFIED_SCOPED**.
- **Boundary:** this checks the declared finite construction, not every
  unknown-magnitude or stochastic-game configuration.

## Claim 6 — stochastic-game detection scaling

- **Paper object:** Grid Soccer and unknown-magnitude Predator-Prey
  detection times follow the predicted `O(1/epsilon^2)` scaling.
- **Source-artifact producer:** `repro/src/verify_claims.py::released_scalings`.
- **Exact producer:** `repro/src/verify_claim6_scaling_exact.py`.
- **Independent auditor:** `repro/src/audit_claim6_scaling_exact.py`.
- **Method:** source artifacts are checked for the released epsilon grids;
  separate log-log fits test the exponent; a fresh 10x10 Predator-Prey
  implementation uses the paper's environment, five off-grid true magnitudes,
  256 deterministic trials per magnitude, and a five-point monitor mixture.
- **Recorded results:** source Grid Soccer slope `-1.855`, `R²=.99399`;
  source Predator-Prey slope `-1.994`, `R²=.99961`; fresh mixture slope
  `-2.030`, `R²=.99830`.
- **Negative controls:** reversed time pairing and constant-time controls fail
  the preregistered exponent direction; the standard-library audit also
  rejects scrambled pairing and an inverse-linear trend.
- **Verdict:** **VERIFIED_SCOPED**.
- **Boundary:** the fresh implementation uses algebraically equivalent
  log-wealth updates to avoid terminal overflow. It does not establish the
  universal rate over all Markov games.

## Gate and integrity

The recorded source-scale gate in
`outputs/publication_gate.json` checks:

- six executed notebook copies against the pinned source;
- only the documented no-TeX rendering fallback;
- no code-cell errors;
- the repeat-required independent verifier;
- the exact Claim 6 audit;
- four verifier tests; and
- the secret scan.

The gate is **PASSED** for the recorded run. Because raw notebooks and the
fetched `upstream/` checkout are ignored, a clean clone must regenerate those
inputs before rerunning the full gate.

## Overall decision

| Scope | Decision |
| --- | --- |
| Six declared finite claim checks | `6/6 VERIFIED_SCOPED` |
| Evidence-release gate | `PASSED` |
| Strict universal paper-claim gate | `NOT_READY` |
| Overall repository status | `VERIFIED_SCOPED` |

No claim is made that this audit reproduces every theorem proof, every
asymptotic regime, or every downstream application result.
