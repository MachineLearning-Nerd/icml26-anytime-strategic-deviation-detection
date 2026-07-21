# Conclusion


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_4f640850f497", "created_at": "2026-07-21T14:19:42+00:00", "title": "Executive summary"}
-->
All three released CPU notebook protocols have completed at source scale, and an independent six-claim verifier with negative controls passes. A repeat is still required before this result is made public.

## Scope & cost

| | This reproduction | Full replication |
|---|---|---|
| Scope | Released normal-form, Grid Soccer, and Predator-Prey protocols; independent numerical checks | New independent implementation and broader seed/hardware study |
| Hardware | Local CPU (4 vCPU) | Multi-environment replication not performed |
| Time | First source suite: 1,742.891 seconds | Not measured |
| Cost | Local CPU only | Not estimated |
| Outcome | First source run and independent gate pass; final repeat pending | Not claimed |


---
<!-- trackio-cell
{"type": "code", "id": "cell_a5713a08d76e", "created_at": "2026-07-21T14:56:35+00:00", "title": "Fail-closed publication gate", "command": ["python", "repro/src/publication_gate.py"], "exit_code": 0, "duration_s": 34.347}
-->
````bash
$ python repro/src/publication_gate.py
````

exit 0 · 34.3s


````python title=publication_gate.py
"""Fail-closed publication gate for the pinned full-source reproduction."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import nbformat


ROOT = Path(__file__).resolve().parents[2]
EXECUTED = ROOT / "outputs" / "executed"
GATE = ROOT / "outputs" / "publication_gate.json"
MARKER = ROOT / "PUBLICATION_READY.md"
RUNS = (
    ("normal-form.ipynb", "normal-form.no-tex.executed.ipynb"),
    ("normal-form.ipynb", "normal-form.repeat.no-tex.executed.ipynb"),
    ("soccer.ipynb", "soccer.no-tex.executed.ipynb"),
    ("soccer.ipynb", "soccer.repeat.no-tex.executed.ipynb"),
    ("predator-prey.ipynb", "predator-prey.no-tex.executed.ipynb"),
    ("predator-prey.ipynb", "predator-prey.repeat.no-tex.executed.ipynb"),
)
SECRET_PATTERNS = (
    re.compile(r"hf_[A-Za-z0-9]{20,}"),
    re.compile(r"sk-[A-Za-z0-9]{20,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
)


def expected_source(source: str) -> str:
    return source.replace(
        "plt.rcParams.update(bundles.icml2024())",
        'plt.rcParams.update({**bundles.icml2024(), "text.usetex": False})',
    )


def notebook_checks() -> dict[str, object]:
    results: dict[str, object] = {}
    passed = True
    for source_name, executed_name in RUNS:
        source = nbformat.read(ROOT / "upstream" / source_name, as_version=4)
        executed = nbformat.read(EXECUTED / executed_name, as_version=4)
        source_code = [cell.source for cell in source.cells if cell.cell_type == "code"]
        executed_code = [cell.source for cell in executed.cells if cell.cell_type == "code"]
        errors = [
            (index, output.get("ename", "unknown"))
            for index, cell in enumerate(executed.cells)
            for output in cell.get("outputs", [])
            if output.output_type == "error"
        ]
        code_matches = source_code == executed_code or [expected_source(text) for text in source_code] == executed_code
        executed_every_cell = all(
            cell.execution_count is not None for cell in executed.cells if cell.cell_type == "code"
        )
        ok = bool(code_matches and executed_every_cell and not errors)
        results[executed_name] = {
            "code_matches_pinned_source_with_only_tex_fallback": code_matches,
            "all_code_cells_executed": executed_every_cell,
            "code_cell_errors": errors,
            "sha256": hashlib.sha256((EXECUTED / executed_name).read_bytes()).hexdigest(),
            "pass": ok,
        }
        passed &= ok
    results["pass"] = passed
    return results


def no_secrets() -> dict[str, object]:
    hits: list[str] = []
    excluded = {".venv", ".git", ".pytest_cache", "outputs"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or excluded.intersection(path.relative_to(ROOT).parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        if any(pattern.search(text) for pattern in SECRET_PATTERNS):
            hits.append(str(path.relative_to(ROOT)))
    return {"hits": hits, "pass": not hits}


def command_passes(command: list[str]) -> bool:
    return subprocess.run(command, cwd=ROOT, check=False).returncode == 0


def main() -> None:
    notebooks = notebook_checks()
    verifier = command_passes([sys.executable, "repro/src/verify_claims.py", "--require-repeat"])
    tests = command_passes([sys.executable, "-m", "pytest", "-q", "repro/tests/test_verifier.py"])
    secrets = no_secrets()
    passed = bool(notebooks["pass"] and verifier and tests and secrets["pass"])
    payload = {
        "paper": "hXO2OP0T4w",
        "pinned_source": "GauthierE/anytime-detection-deviation@42b8f0edfe76fb9dd006e9cab84f6cb8b75849c6",
        "expected_claims": 6,
        "full_source_runs": notebooks,
        "repeat_verifier_passed": verifier,
        "tests_passed": tests,
        "secret_scan": secrets,
        "publication_gate_passed": passed,
    }
    GATE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if not passed:
        raise SystemExit("publication gate failed")
    MARKER.write_text(
        "# Publication ready\n\nFULL_GATE_READY: hXO2OP0T4w\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()

````


````output
{
  "c1_evalue_identity": {
    "max_abs_evalue_mean_error": 0.0,
    "pass": true
  },
  "c2_fwer_control": {
    "runs": 20000,
    "horizon": 1000,
    "fwer": 0.0303,
    "pass": true
  },
  "c3_c4_detection_and_fdr": {
    "runs": 250,
    "fwer_mean_stop": 1747.104,
    "fdr_mean_stop": 1527.844,
    "fdr_speedup": 1.1435094158827734,
    "pass": true
  },
  "c5_mixture_identity": {
    "null_lr_mean": 0.9999999999999999,
    "alternative_log_growth": 0.23645627415367648,
    "pass": true
  },
  "stochastic_scalings": {
    "soccer_monotone": true,
    "predator_monotone": true,
    "repeat_exists": true,
    "repeat_equal": true,
    "source_artifacts_checked": 2,
    "pass": true
  },
  "pass": true
}
....                                                                     [100%]
4 passed in 15.22s
{
  "paper": "hXO2OP0T4w",
  "pinned_source": "GauthierE/anytime-detection-deviation@42b8f0edfe76fb9dd006e9cab84f6cb8b75849c6",
  "expected_claims": 6,
  "full_source_runs": {
    "normal-form.no-tex.executed.ipynb": {
      "code_matches_pinned_source_with_only_tex_fallback": true,
      "all_code_cells_executed": true,
      "code_cell_errors": [],
      "sha256": "e8691d67ac4218c3594f971d354f18bbc2dc843e2843e3c80b6ba0d24b52535b",
      "pass": true
    },
    "normal-form.repeat.no-tex.executed.ipynb": {
      "code_matches_pinned_source_with_only_tex_fallback": true,
      "all_code_cells_executed": true,
      "code_cell_errors": [],
      "sha256": "97b0c87cf8185dc86aa60684b5dedeb363b55440afe1b023595717089a55b0db",
      "pass": true
    },
    "soccer.no-tex.executed.ipynb": {
      "code_matches_pinned_source_with_only_tex_fallback": true,
      "all_code_cells_executed": true,
      "code_cell_errors": [],
      "sha256": "9987aabb5bd04af5090d22b097834f55f0748e9d7e020e24bf3c0fb83bb05ad1",
      "pass": true
    },
    "soccer.repeat.no-tex.executed.ipynb": {
      "code_matches_pinned_source_with_only_tex_fallback": true,
      "all_code_cells_executed": true,
      "code_cell_errors": [],
      "sha256": "437034fa13dbb18be08417c69cac4859b5e6300d71cfe71a159b3e37debead60",
      "pass": true
    },
    "predator-prey.no-tex.executed.ipynb": {
      "code_matches_pinned_source_with_only_tex_fallback": true,
      "all_code_cells_executed": true,
      "code_cell_errors": [],
      "sha256": "43614a343308b7d2004a53456573f25a274568e11c8e9b158836f80984e48af6",
      "pass": true
    },
    "predator-prey.repeat.no-tex.executed.ipynb": {
      "code_matches_pinned_source_with_only_tex_fallback": true,
      "all_code_cells_executed": true,
      "code_cell_errors": [],
      "sha256": "86673a197404c29a9b38099b15edd859c31646739af2928f45693ad98137ca44",
      "pass": true
    },
    "pass": true
  },
  "repeat_verifier_passed": true,
  "tests_passed": true,
  "secret_scan": {
    "hits": [],
    "pass": true
  },
  "publication_gate_passed": true
}

````


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_dc85cad4e612", "created_at": "2026-07-21T14:57:59+00:00", "title": "Retained execution artifacts"}
-->
The executed source notebooks, independent verdict, and publication-gate proof are retained as local-path artifacts for promotion with this logbook. Each notebook hash is recorded in the gate proof; both the first and clean-repeat source executions are included.
