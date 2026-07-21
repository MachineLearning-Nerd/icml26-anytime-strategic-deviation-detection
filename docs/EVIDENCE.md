# Evidence — hXO2OP0T4w

## Pinned source and full-scale execution

The author source is pinned at `GauthierE/anytime-detection-deviation`
commit `42b8f0edfe76fb9dd006e9cab84f6cb8b75849c6`. All three released notebooks
were executed on CPU and retained in `outputs/executed/`:

| Notebook | Full source result | Wall CPU execution |
|---|---|---:|
| `normal-form.ipynb` | FWER control grid; FDR mean stop 1545.4 vs FWER 1765.4 | 575.696 s |
| `soccer.ipynb` | ε=.05/.10/.20/.30/.50 mean stops 1431.8/369.7/140.1/62.6/18.0 | 1088.916 s |
| `predator-prey.ipynb` | ε=.05/.10/.20/.30/.40/.60/.80 mean stops 2413.6/636.7/156.4/66.6/41.8/16.7/9.8 | 78.279 s |

The author plotting preset requires a system `latex` executable that is absent
from the CPU environment. Execution copies therefore set only
`matplotlib.rcParams['text.usetex']=False`; algorithms, seeds, trial counts,
and numerical cells are unchanged. The first attempt and the successful
no-TeX copy are both retained.

## Independent checks and controls

`repro/src/verify_claims.py` is independent from the author notebooks. Its
recorded result is `outputs/independent_verdict.json`.

| Claim group | Independent evidence | Control / outcome |
|---|---|---|
| C1 | Exact expectation of all four per-round e-values under the stated NE | Maximum error 0 |
| C2 | 20,000 independent null trajectories, 1,000 rounds, λ=.4, α=.05 | FWER .0303 ≤ .05 |
| C3–C4 | 250 independent alternative trajectories | FDR mean stop 1527.844 < FWER 1747.104; 1.144× speedup |
| C5 | Independent finite-action mixture likelihood-ratio calculation | Null mean 1 to machine precision; alternative log growth .236456 > 0 |
| C6 | Executed source Grid Soccer and Predator-Prey results parsed from notebook artifacts | Both detection-time sequences strictly decrease with ε |

The author Grid Soccer source emits a floating-point overflow warning after a
likelihood ratio has already crossed the detection threshold. The recorded
stopping time remains valid for the source run, and the independent verifier
does not rely on that overflowed terminal value.

## Gate status

Two complete deterministic source executions now pass. The fail-closed gate
checks all six execution notebooks against the pinned source (allowing only
the documented no-TeX rendering fallback), requires every code cell to have
executed without an error, reruns the independent verifier in repeat-required
mode, reruns all four tests, and scans for secrets. Its proof is retained at
`outputs/publication_gate.json`; it passed on 2026-07-21. The corresponding
executed notebooks, source CSVs, independent verdict, and gate proof are
registered as Trackio artifacts for publication.
