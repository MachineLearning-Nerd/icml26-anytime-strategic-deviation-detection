# Reproduction: Anytime Detection of Strategic Deviations in Multi-Agent Systems

OpenReview ID: `hXO2OP0T4w`

arXiv: `2601.05427`
Pinned author source: `GauthierE/anytime-detection-deviation@42b8f0edfe76fb9dd006e9cab84f6cb8b75849c6`

This reproduction executes the author-released CPU notebooks for normal-form,
Grid Soccer, and Predator-Prey experiments, then adds independent numerical
checks and negative controls. No result is considered publishable until the
complete source protocol and independent gate both pass.

## Reproduce locally

The author source is intentionally fetched separately so its exact upstream
commit remains auditable:

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
python repro/src/publication_gate.py
```

`--disable-tex` changes only the unavailable Matplotlib text renderer in the
execution copy; it leaves the author algorithms, seeds, numerical cells, and
trial counts untouched. The published Trackio logbook contains the executed
notebooks, source CSVs, independent verdict, and gate proof as artifacts.

Current state: see [STATUS.md](STATUS.md) and [docs/EVIDENCE.md](docs/EVIDENCE.md).
