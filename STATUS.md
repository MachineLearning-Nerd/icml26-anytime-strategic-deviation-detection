# Status — hXO2OP0T4w

## Current step

Finalize the local evidence record, then repeat the complete pinned source
protocol once from a clean execution-output directory before the publication
gate.

## Source contract

- Paper: arXiv `2601.05427`.
- Author repository: `GauthierE/anytime-detection-deviation` at
  `42b8f0edfe76fb9dd006e9cab84f6cb8b75849c6`.
- Released protocol: `normal-form.ipynb`, `soccer.ipynb`, and
  `predator-prey.ipynb`. The repository states these are the three experiments
  used for the paper figures.
- Compute audit: finite NumPy/SciPy simulations; normal-form uses 300 runs by
  4,000 rounds; Predator-Prey uses 100 trials per epsilon; no CUDA dependency.

## Completed

- Read-only source, code, data, and compute audit completed.
- Claimed in the shared registry; no DineshAI Space, GitHub repository, or
  backlog entry exists.
- Pinned upstream source was vendored as `upstream/`.
- Built an isolated Python 3.12 CPU environment with NumPy, SciPy, NashPy,
  Matplotlib, Tueplots, and Jupyter.
- The first unmodified normal-form execution reached only figure rendering and
  failed because the author ICML plot preset requests a system `latex` binary.
  Successful execution copies set only `text.usetex=False`; numerical cells,
  parameters, seeds, trial counts, and source files are unchanged. Partial and
  successful executed notebooks plus stdout/stderr logs are retained in
  `outputs/`.
- The full no-TeX execution copy of `normal-form.ipynb` then completed in
  `575.696` CPU seconds with no code-cell error. It retained the released
  300-run/4,000-round controls and alternative grid; its source output records
  FDR mean stopping time `1545.4` versus FWER `1765.4` (1.15× speedup).
- The full no-TeX execution copy of `soccer.ipynb` completed in `1088.916` CPU
  seconds with no code-cell error. It retained the released 800-state,
  100-trial protocol and records mean stopping times
  `1431.8/369.7/140.1/62.6/18.0` for ε=`.05/.10/.20/.30/.50`.
- The full no-TeX execution copy of `predator-prey.ipynb` completed in `78.279`
  CPU seconds with no code-cell error. It retained all seven released epsilon
  conditions and records a strictly decreasing detection-time curve.
- An independent six-claim verifier and its negative controls pass: exact
  e-value calibration, a 20,000-trajectory null FWER check, independent
  alternative stopping-time comparison, mixture-LR identity, and parsing of
  both full source stochastic-game curves. `pytest` reports four passing tests.
- The local Trackio logbook was opened and its metadata now declares arXiv
  `2601.05427` and the required `icml2026-repro` / `paper-hXO2OP0T4w` tags.

## Next action

The complete clean repeat, Trackio evidence capture, independent verifier,
four unit tests, secret scan, and fail-closed publication gate now pass. Next:
create/push the public GitHub repository, atomically enqueue this one
gate-complete paper, and wait for the shared drain to publish and verify the
DineshAI/hXO2OP0T4w Space. Do not select another paper afterward: the user
explicitly requested a pause once this paper is published.

## Publication guard

Do not publish, create a public GitHub repository, or enqueue until every
anchored claim has full-scale evidence, independent verification, negative
controls, and a clean repeat run.
