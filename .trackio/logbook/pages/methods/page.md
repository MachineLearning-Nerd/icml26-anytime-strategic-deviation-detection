# Methods


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_39086762c0a0", "created_at": "2026-07-21T14:19:41+00:00", "title": "CPU source protocol"}
-->
The author notebooks are executed from the pinned repository with Python 3.12 and CPU NumPy/SciPy/NashPy dependencies. The author ICML plotting preset requires a local latex executable; execution copies disable only matplotlib text.usetex. Algorithms, seeds, state spaces, trial counts, and numerical cells are unchanged.


---
<!-- trackio-cell
{"type": "code", "id": "cell_d034287a19fd", "created_at": "2026-07-21T14:34:07+00:00", "title": "Clean repeat: normal-form source notebook", "command": ["python", "repro/src/execute_notebook.py", "upstream/normal-form.ipynb", "outputs/executed/normal-form.repeat.no-tex.executed.ipynb", "--disable-tex"], "exit_code": 0, "duration_s": 617.437}
-->
````bash
$ python repro/src/execute_notebook.py upstream/normal-form.ipynb outputs/executed/normal-form.repeat.no-tex.executed.ipynb --disable-tex
````

exit 0 · 617.4s


````python title=execute_notebook.py
"""Execute one released notebook while retaining partial evidence on failure."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook")
    parser.add_argument("output")
    parser.add_argument(
        "--disable-tex",
        action="store_true",
        help="Disable only the unavailable LaTeX renderer in an execution copy.",
    )
    args = parser.parse_args()
    source = Path(args.notebook)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    notebook = nbformat.read(source, as_version=4)
    if args.disable_tex:
        for cell in notebook.cells:
            if cell.cell_type != "code":
                continue
            source_text = cell.source
            cell.source = source_text.replace(
                "plt.rcParams.update(bundles.icml2024())",
                'plt.rcParams.update({**bundles.icml2024(), "text.usetex": False})',
            )
    client = NotebookClient(notebook, timeout=3600, kernel_name="python3")
    started = time.monotonic()
    try:
        with client.setup_kernel(cwd=str(source.parent)):
            for index, cell in enumerate(notebook.cells):
                if cell.cell_type != "code":
                    continue
                print(f"EXECUTING_CELL={index}", flush=True)
                client.execute_cell(cell, index, store_history=True)
                nbformat.write(notebook, output)
    except Exception as exc:
        nbformat.write(notebook, output)
        print(f"EXECUTION_FAILED={type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(f"EXECUTION_SECONDS={time.monotonic() - started:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

````


````output
[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.
EXECUTING_CELL=0
EXECUTING_CELL=1
EXECUTING_CELL=2
EXECUTING_CELL=3
EXECUTING_CELL=4
EXECUTION_SECONDS=615.918

````


---
<!-- trackio-cell
{"type": "code", "id": "cell_fa77144c6a3d", "created_at": "2026-07-21T14:52:01+00:00", "title": "Clean repeat: Grid Soccer source notebook", "command": ["python", "repro/src/execute_notebook.py", "upstream/soccer.ipynb", "outputs/executed/soccer.repeat.no-tex.executed.ipynb", "--disable-tex"], "exit_code": 0, "duration_s": 1048.418}
-->
````bash
$ python repro/src/execute_notebook.py upstream/soccer.ipynb outputs/executed/soccer.repeat.no-tex.executed.ipynb --disable-tex
````

exit 0 · 1048.4s


````python title=execute_notebook.py
"""Execute one released notebook while retaining partial evidence on failure."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook")
    parser.add_argument("output")
    parser.add_argument(
        "--disable-tex",
        action="store_true",
        help="Disable only the unavailable LaTeX renderer in an execution copy.",
    )
    args = parser.parse_args()
    source = Path(args.notebook)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    notebook = nbformat.read(source, as_version=4)
    if args.disable_tex:
        for cell in notebook.cells:
            if cell.cell_type != "code":
                continue
            source_text = cell.source
            cell.source = source_text.replace(
                "plt.rcParams.update(bundles.icml2024())",
                'plt.rcParams.update({**bundles.icml2024(), "text.usetex": False})',
            )
    client = NotebookClient(notebook, timeout=3600, kernel_name="python3")
    started = time.monotonic()
    try:
        with client.setup_kernel(cwd=str(source.parent)):
            for index, cell in enumerate(notebook.cells):
                if cell.cell_type != "code":
                    continue
                print(f"EXECUTING_CELL={index}", flush=True)
                client.execute_cell(cell, index, store_history=True)
                nbformat.write(notebook, output)
    except Exception as exc:
        nbformat.write(notebook, output)
        print(f"EXECUTION_FAILED={type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(f"EXECUTION_SECONDS={time.monotonic() - started:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

````


````output
[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.
EXECUTING_CELL=0
EXECUTING_CELL=1
EXECUTING_CELL=2
EXECUTING_CELL=3
EXECUTION_SECONDS=1046.858

````


---
<!-- trackio-cell
{"type": "artifact", "id": "cell_63cb088708f6", "created_at": "2026-07-21T14:52:01+00:00", "title": "Artifact: nash_history.csv", "path": "upstream/results/soccer/nash_history.csv", "size": 2582, "artifact_type": "dataset", "auto": true}
-->
**📦 Artifact** `upstream/results/soccer/nash_history.csv` · dataset · 2.6 kB

trackio-local-path://upstream/results/soccer/nash_history.csv


---
<!-- trackio-cell
{"type": "artifact", "id": "cell_1a23e2da7e15", "created_at": "2026-07-21T14:52:01+00:00", "title": "Artifact: afraid_history.csv", "path": "upstream/results/soccer/afraid_history.csv", "size": 2556, "artifact_type": "dataset", "auto": true}
-->
**📦 Artifact** `upstream/results/soccer/afraid_history.csv` · dataset · 2.6 kB

trackio-local-path://upstream/results/soccer/afraid_history.csv


---
<!-- trackio-cell
{"type": "code", "id": "cell_357a97a5012a", "created_at": "2026-07-21T14:53:26+00:00", "title": "Clean repeat: Predator-Prey source notebook", "command": ["python", "repro/src/execute_notebook.py", "upstream/predator-prey.ipynb", "outputs/executed/predator-prey.repeat.no-tex.executed.ipynb", "--disable-tex"], "exit_code": 0, "duration_s": 72.002}
-->
````bash
$ python repro/src/execute_notebook.py upstream/predator-prey.ipynb outputs/executed/predator-prey.repeat.no-tex.executed.ipynb --disable-tex
````

exit 0 · 72.0s


````python title=execute_notebook.py
"""Execute one released notebook while retaining partial evidence on failure."""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

import nbformat
from nbclient import NotebookClient


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("notebook")
    parser.add_argument("output")
    parser.add_argument(
        "--disable-tex",
        action="store_true",
        help="Disable only the unavailable LaTeX renderer in an execution copy.",
    )
    args = parser.parse_args()
    source = Path(args.notebook)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    notebook = nbformat.read(source, as_version=4)
    if args.disable_tex:
        for cell in notebook.cells:
            if cell.cell_type != "code":
                continue
            source_text = cell.source
            cell.source = source_text.replace(
                "plt.rcParams.update(bundles.icml2024())",
                'plt.rcParams.update({**bundles.icml2024(), "text.usetex": False})',
            )
    client = NotebookClient(notebook, timeout=3600, kernel_name="python3")
    started = time.monotonic()
    try:
        with client.setup_kernel(cwd=str(source.parent)):
            for index, cell in enumerate(notebook.cells):
                if cell.cell_type != "code":
                    continue
                print(f"EXECUTING_CELL={index}", flush=True)
                client.execute_cell(cell, index, store_history=True)
                nbformat.write(notebook, output)
    except Exception as exc:
        nbformat.write(notebook, output)
        print(f"EXECUTION_FAILED={type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    print(f"EXECUTION_SECONDS={time.monotonic() - started:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

````


````output
[IPKernelApp] WARNING | Kernel is running over TCP without encryption. All communication (including code and outputs) is sent in plain text and is susceptible to eavesdropping. Use IPC transport or launch with kernel manager-provisioned CurveZMQ keys to enable transport encryption.
EXECUTING_CELL=0
EXECUTING_CELL=1
EXECUTION_SECONDS=70.454

````


---
<!-- trackio-cell
{"type": "artifact", "id": "cell_677f1c21d86e", "created_at": "2026-07-21T14:53:26+00:00", "title": "Artifact: history.csv", "path": "upstream/results/predator-prey/history.csv", "size": 1609, "artifact_type": "dataset", "auto": true}
-->
**📦 Artifact** `upstream/results/predator-prey/history.csv` · dataset · 1.6 kB

trackio-local-path://upstream/results/predator-prey/history.csv
