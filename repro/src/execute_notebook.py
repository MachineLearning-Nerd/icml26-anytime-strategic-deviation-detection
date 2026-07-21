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
