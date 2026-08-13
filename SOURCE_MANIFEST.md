# Source manifest

This file defines which paper version, source repository, files, and execution
changes the evidence refers to.

## Paper

| Item | Pin |
| --- | --- |
| Title | *Anytime Detection of Strategic Deviations in Multi-Agent Systems* |
| Authors | Etienne Gauthier; Francis Bach; Michael I. Jordan |
| Official record | [arXiv:2601.05427v3](https://arxiv.org/abs/2601.05427) |
| Official PDF | [arxiv.org/pdf/2601.05427](https://arxiv.org/pdf/2601.05427) |
| Competition identifier | OpenReview [hXO2OP0T4w](https://openreview.net/forum?id=hXO2OP0T4w) |
| Rendered source used by the Claim 6 audit | `https://ar5iv.labs.arxiv.org/html/2601.05427` |
| Rendered-source SHA-256 | `85f6ed063ca67bd82faf7bd0632af425e0a12e40e5eaa218482f37f4261838e1` |

The official arXiv record is the citation authority. The ar5iv checksum is
included only to make the detailed Claim 6 source extraction auditable.

## Author source

| Item | Pin |
| --- | --- |
| Canonical repository | [GauthierE/anytime-detection-deviation](https://github.com/GauthierE/anytime-detection-deviation) |
| Pinned commit | `42b8f0edfe76fb9dd006e9cab84f6cb8b75849c6` |
| Source notebooks | `normal-form.ipynb`, `soccer.ipynb`, `predator-prey.ipynb` |
| Historical source alias | `GauthierE/betting-equilibrium` resolves to the canonical repository |

The author checkout is fetched into the ignored `upstream/` directory by the
reproduction commands. It is not silently substituted with a moving default
branch.

## Executed source artifacts

The source-scale gate recorded these executed notebook hashes:

| Artifact | SHA-256 | Execution contract |
| --- | --- | --- |
| `normal-form.no-tex.executed.ipynb` | `e8691d67ac4218c3594f971d354f18bbc2dc843e2843e3c80b6ba0d24b52535b` | Pinned source with only the no-TeX fallback |
| `normal-form.repeat.no-tex.executed.ipynb` | `97b0c87cf8185dc86aa60684b5dedeb363b55440afe1b023595717089a55b0db` | Deterministic repeat |
| `soccer.no-tex.executed.ipynb` | `9987aabb5bd04af5090d22b097834f55f0748e9d7e020e24bf3c0fb83bb05ad1` | Pinned source with only the no-TeX fallback |
| `soccer.repeat.no-tex.executed.ipynb` | `437034fa13dbb18be08417c69cac4859b5e6300d71cfe71a159b3e37debead60` | Deterministic repeat |
| `predator-prey.no-tex.executed.ipynb` | `43614a343308b7d2004a53456573f25a274568e11c8e9b158836f80984e48af6` | Pinned source with only the no-TeX fallback |
| `predator-prey.repeat.no-tex.executed.ipynb` | `86673a197404c29a9b38099b15edd859c31646739af2928f45693ad98137ca44` | Deterministic repeat |

These large files are ignored in Git. The hashes remain in
`outputs/publication_gate.json`; rerunning the notebooks from a clean clone is
required to recreate them locally.

## Execution deviation

The author plotting preset requests a local `latex` executable. The execution
copies replace only
`plt.rcParams.update(bundles.icml2024())` with an equivalent update that sets
`text.usetex=False`. The gate compares every code cell against the pinned
source and fails if any other code change is present.

## Claim 6 exact protocol

The fresh exact audit follows the paper's Predator-Prey environment:

- 10x10 grid, three predators, five actions.
- Uniform random-walk null and chase weights 10, 1, and 0.1.
- Monitor mixture grid `{0.1, 0.3, 0.5, 0.7, 0.9}`.
- Detection threshold 20 and 5,000-step cutoff.
- 256 deterministic trials for each of seven true epsilon values.
- Five true values are off the monitor grid: 0.05, 0.2, 0.4, 0.6, and 0.8.
- Log wealth is used instead of a raw product only to avoid overflow; the
  calculation is algebraically equivalent.

## Provenance boundary

The source notebooks are the authors' implementation. The independent
verifier does not import them for C1–C5, while C6 explicitly includes both
source-artifact checks and a fresh exact protocol implementation. This
separation is why the README distinguishes source reproduction from
independent evidence.
