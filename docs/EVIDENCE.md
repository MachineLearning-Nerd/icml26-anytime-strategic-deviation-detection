# Evidence — hXO2OP0T4w

## Pinned source and source-scale execution

The author source is pinned at
`GauthierE/anytime-detection-deviation@42b8f0edfe76fb9dd006e9cab84f6cb8b75849c6`.
The three released notebooks were executed on CPU and repeated:

| Notebook | Recorded source result | Wall CPU execution |
| --- | --- | ---: |
| `normal-form.ipynb` | FWER control grid; FDR mean stop `1545.4` vs FWER `1765.4` | `575.696 s` |
| `soccer.ipynb` | epsilon `.05/.10/.20/.30/.50` mean stops `1431.8/369.7/140.1/62.6/18.0` | `1088.916 s` |
| `predator-prey.ipynb` | epsilon `.05/.10/.20/.30/.40/.60/.80` mean stops `2413.6/636.7/156.4/66.6/41.8/16.7/9.8` | `78.279 s` |

The six deterministic copies are hashed in
`SOURCE_MANIFEST.md` and `outputs/publication_gate.json`.

The author plotting preset requests a system `latex` executable that is absent
from the CPU environment. Execution copies therefore set only
`matplotlib.rcParams['text.usetex']=False`; algorithms, seeds, trial counts,
and numerical cells are unchanged. This is a rendering fallback, not an
algorithmic modification.

## Independent checks and controls

`repro/src/verify_claims.py` is independent from the author notebooks. Its
recorded result is `outputs/independent_verdict.json`.

| Claim group | Independent evidence | Recorded outcome |
| --- | --- | --- |
| C1 | Exact expectation of all four per-round e-values under the stated Nash equilibrium | Maximum error `0` |
| C2 | 20,000 independent null trajectories, horizon 1,000, lambda `.4`, alpha `.05` | FWER `.0303 <= .05` |
| C3–C4 | 250 independent alternative trajectories | FDR mean stop `1527.844` < FWER `1747.104`; `1.144x` speedup |
| C5 | Independent finite-action mixture likelihood-ratio calculation | Null mean `1.0`; alternative log-growth `.236456` |
| C6 | Executed source Grid Soccer and Predator-Prey outputs | Both detection-time sequences decrease with epsilon |

The independent verifier includes negative controls for null false-alarm
control, alternative directionality, and stochastic-game curve direction.

## Exact Claim 6 evidence

`repro/src/verify_claim6_scaling_exact.py` checks:

- source Grid Soccer slope `-1.855`, `R²=.99399`;
- source Predator-Prey slope `-1.994`, `R²=.99961`;
- a fresh paper-environment Predator-Prey mixture run with slope `-2.030`,
  `R²=.99830`;
- five true epsilon values absent from the monitor grid; and
- negative controls for reversed and constant detection-time trends.

`repro/src/audit_claim6_scaling_exact.py` is a separate standard-library
implementation. It derives the least-squares fit independently, checks the
scaled `tau * epsilon²` values, and rejects scrambled pairing and an
inverse-linear control. Its compact result is
`outputs/claim6_scaling_audit.json`.

## Gate status

Two complete deterministic source executions, the repeat-required independent
verifier, four tests, the exact Claim 6 audit, and the secret scan are recorded
as passing in `outputs/publication_gate.json`.

This is an evidence-release gate, not a universal theorem gate. Raw source
checkouts and executed notebooks are ignored and must be regenerated before
the gate can be run from a clean clone.
