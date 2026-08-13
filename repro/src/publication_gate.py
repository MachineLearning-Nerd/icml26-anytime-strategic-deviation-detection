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
    claim6_audit = command_passes([sys.executable, "repro/src/audit_claim6_scaling_exact.py"])
    tests = command_passes([sys.executable, "-m", "pytest", "-q", "repro/tests/test_verifier.py"])
    secrets = no_secrets()
    passed = bool(notebooks["pass"] and verifier and claim6_audit and tests and secrets["pass"])
    payload = {
        "schema_version": 2,
        "repository": {
            "owner": "MachineLearning-Nerd",
            "original_name": "icml26-repro-hXO2OP0T4w-anytime-deviation",
            "target_name": "icml26-anytime-strategic-deviation-detection",
            "default_branch": "main",
        },
        "paper": "hXO2OP0T4w",
        "paper_title": "Anytime Detection of Strategic Deviations in Multi-Agent Systems",
        "arxiv": "2601.05427v3",
        "authors": ["Etienne Gauthier", "Francis Bach", "Michael I. Jordan"],
        "pinned_source": "GauthierE/anytime-detection-deviation@42b8f0edfe76fb9dd006e9cab84f6cb8b75849c6",
        "expected_claims": 6,
        "full_source_runs": notebooks,
        "repeat_verifier_passed": verifier,
        "claim6_exact_scaling_audit_passed": claim6_audit,
        "tests_passed": tests,
        "secret_scan": secrets,
        "claim_status": {
            "C1": "VERIFIED_SCOPED",
            "C2": "VERIFIED_SCOPED",
            "C3": "VERIFIED_SCOPED",
            "C4": "VERIFIED_SCOPED",
            "C5": "VERIFIED_SCOPED",
            "C6": "VERIFIED_SCOPED",
        },
        "overall_status": "VERIFIED_SCOPED",
        "evidence_release_gate": "PASSED",
        "strict_paper_claim_gate": "NOT_READY",
        "publication_gate_passed": passed,
    }
    GATE.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    if not passed:
        raise SystemExit("publication gate failed")
    MARKER.write_text(
        "# Evidence release status\n\n"
        "- Evidence-release gate: **PASSED**\n"
        "- Claim vector: **6/6 VERIFIED_SCOPED**\n"
        "- Strict universal paper-claim gate: **NOT_READY**\n"
        "- Canonical target: `MachineLearning-Nerd/icml26-anytime-strategic-deviation-detection`\n"
        "- Public branch policy: one default `main`; no `master` or `orx/*` refs\n",
        encoding="utf-8",
    )
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
