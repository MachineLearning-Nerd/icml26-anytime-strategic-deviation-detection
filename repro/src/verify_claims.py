"""Independent numerical checks for the six anchored claims.

This deliberately does not import the authors' notebooks.  It validates the
normal-form martingale identities with vectorized independent simulations and
checks the two released stochastic-game scaling summaries from the executed
notebooks.
"""

from __future__ import annotations

import json
import argparse
import re
from pathlib import Path

import nbformat
import numpy as np


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "outputs"


U1 = np.array([[0.9, 0.2], [0.3, 0.7]])
U2 = np.array([[0.5, 0.3], [0.2, 0.7]])
PI1_NE = np.array([5 / 7, 2 / 7])
PI2_NE = np.array([5 / 11, 6 / 11])


def normal_form_identity() -> dict[str, float | bool]:
    """C1: under the equilibrium, every e-value has expectation one."""
    lam = 0.4
    means = []
    for deviation in range(2):
        expected_x = sum(
            PI1_NE[a1] * PI2_NE[a2] * (U1[a1, a2] - U1[deviation, a2])
            for a1 in range(2)
            for a2 in range(2)
        )
        means.append(1 - lam * expected_x)
    for deviation in range(2):
        expected_x = sum(
            PI1_NE[a1] * PI2_NE[a2] * (U2[a1, a2] - U2[a1, deviation])
            for a1 in range(2)
            for a2 in range(2)
        )
        means.append(1 - lam * expected_x)
    return {"max_abs_evalue_mean_error": float(np.max(np.abs(np.array(means) - 1))), "pass": bool(np.allclose(means, 1))}


def fwer_control() -> dict[str, float | bool]:
    """C2: independent vectorized null simulation at the strict alpha=.05 cell."""
    rng = np.random.default_rng(20260721)
    runs, horizon, lam, threshold = 20_000, 1_000, 0.4, 80.0
    m = np.ones((runs, 4))
    crossed = np.zeros(runs, dtype=bool)
    for _ in range(horizon):
        a1 = (rng.random(runs) >= PI1_NE[0]).astype(int)
        a2 = (rng.random(runs) >= PI2_NE[0]).astype(int)
        x = np.column_stack((
            U1[a1, a2] - U1[0, a2], U1[a1, a2] - U1[1, a2],
            U2[a1, a2] - U2[a1, 0], U2[a1, a2] - U2[a1, 1],
        ))
        m *= 1 - lam * x
        crossed |= np.max(m, axis=1) >= threshold
    rate = float(np.mean(crossed))
    return {"runs": runs, "horizon": horizon, "fwer": rate, "pass": rate <= 0.05}


def mixture_identity() -> dict[str, float | bool]:
    """C5: likelihood-ratio mixture is mean-one under baseline and grows under a deviation."""
    base = np.array([0.10, 0.20, 0.30, 0.25, 0.15])
    direction = np.array([0.00, -0.10, 0.35, -0.10, -0.15])
    alternative = base + direction
    grid = np.array([0.1, 0.3, 0.5, 0.7, 0.9])
    mixture = np.mean(np.array([(1 - eps) * base + eps * alternative for eps in grid]), axis=0)
    lr = mixture / base
    null_mean = float(base @ lr)
    log_growth = float(alternative @ np.log(lr))
    return {"null_lr_mean": null_mean, "alternative_log_growth": log_growth, "pass": abs(null_mean - 1) < 1e-12 and log_growth > 0}


def detection_rate_and_fdr() -> dict[str, float | bool]:
    """C3/C4: independent FDR-vs-FWER calculation under the released alternative."""
    rng = np.random.default_rng(20260722)
    alpha, lam, horizon, runs = 0.2, 0.05, 4_000, 250
    threshold = 4 / alpha
    pi1, pi2 = np.array([0.85, 0.15]), np.array([0.65, 0.35])
    fwer_times = []
    fdr_times = []
    for _ in range(runs):
        values = np.ones(4)
        maxima = np.ones(4)
        tau_fwer = horizon
        tau_fdr = horizon
        for t in range(1, horizon + 1):
            a1 = int(rng.random() >= pi1[0])
            a2 = int(rng.random() >= pi2[0])
            increments = np.array([
                U1[a1, a2] - U1[0, a2], U1[a1, a2] - U1[1, a2],
                U2[a1, a2] - U2[a1, 0], U2[a1, a2] - U2[a1, 1],
            ])
            values *= 1 - lam * increments
            maxima = np.maximum(maxima, values)
            if tau_fwer == horizon and np.max(values) >= threshold:
                tau_fwer = t
            if tau_fdr == horizon:
                admissible = [k for k in range(1, 5) if np.sum(maxima >= 4 / (k * alpha)) >= k]
                if admissible:
                    tau_fdr = t
            if tau_fwer < horizon and tau_fdr < horizon:
                break
        fwer_times.append(tau_fwer)
        fdr_times.append(tau_fdr)
    fwer_mean = float(np.mean(fwer_times))
    fdr_mean = float(np.mean(fdr_times))
    return {
        "runs": runs,
        "fwer_mean_stop": fwer_mean,
        "fdr_mean_stop": fdr_mean,
        "fdr_speedup": fwer_mean / fdr_mean,
        "pass": fdr_mean < fwer_mean,
    }


def _stream_text(notebook: Path, cell_index: int) -> str:
    notebook_data = nbformat.read(notebook, as_version=4)
    return "\n".join(
        output.get("text", "")
        for output in notebook_data.cells[cell_index].get("outputs", [])
        if output.output_type == "stream"
    )


def _parse_source_curves(soccer_path: Path, predator_path: Path) -> tuple[np.ndarray, np.ndarray]:
    """Read the source notebook stdout rather than duplicating reported values."""
    soccer_text = _stream_text(soccer_path, 3)
    predator_text = _stream_text(predator_path, 0)
    soccer_matches = re.findall(r"Eps=(0\.\d+) \| Avg Time=(\d+\.\d+)", soccer_text)
    predator_matches = re.findall(r"^(0\.\d+)\s+\|\s+(\d+\.\d+)", predator_text, re.MULTILINE)
    required_soccer = ["0.05", "0.10", "0.20", "0.30", "0.50"]
    required_predator = ["0.05", "0.10", "0.20", "0.30", "0.40", "0.60", "0.80"]
    if [epsilon for epsilon, _ in soccer_matches] != required_soccer:
        raise ValueError(f"unexpected Grid Soccer source curve: {soccer_matches}")
    if [epsilon for epsilon, _ in predator_matches] != required_predator:
        raise ValueError(f"unexpected Predator-Prey source curve: {predator_matches}")
    return (
        np.array([float(value) for _, value in soccer_matches]),
        np.array([float(value) for _, value in predator_matches]),
    )


def released_scalings(require_repeat: bool = False) -> dict[str, float | bool | int]:
    """C6: parse complete source artifacts and check monotonic source curves.

    ``require_repeat`` fail-closes the final gate unless a second deterministic
    execution copy exists and has the same parsed curves as the first run.
    """
    executed = OUT / "executed"
    first = _parse_source_curves(
        executed / "soccer.no-tex.executed.ipynb",
        executed / "predator-prey.no-tex.executed.ipynb",
    )
    curves = [first]
    repeat_exists = all(
        path.exists()
        for path in (
            executed / "soccer.repeat.no-tex.executed.ipynb",
            executed / "predator-prey.repeat.no-tex.executed.ipynb",
        )
    )
    if require_repeat:
        if not repeat_exists:
            return {"repeat_exists": False, "pass": False}
        curves.append(_parse_source_curves(
            executed / "soccer.repeat.no-tex.executed.ipynb",
            executed / "predator-prey.repeat.no-tex.executed.ipynb",
        ))
    source_monotone = all(
        np.all(np.diff(soccer_times) < 0) and np.all(np.diff(predator_times) < 0)
        for soccer_times, predator_times in curves
    )
    repeat_equal = not require_repeat or (
        np.array_equal(curves[0][0], curves[1][0]) and np.array_equal(curves[0][1], curves[1][1])
    )
    return {
        "soccer_monotone": bool(source_monotone),
        "predator_monotone": bool(source_monotone),
        "repeat_exists": repeat_exists,
        "repeat_equal": bool(repeat_equal),
        "source_artifacts_checked": len(curves),
        "pass": bool(source_monotone and repeat_equal),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--require-repeat", action="store_true")
    args = parser.parse_args()
    results = {
        "c1_evalue_identity": normal_form_identity(),
        "c2_fwer_control": fwer_control(),
        "c3_c4_detection_and_fdr": detection_rate_and_fdr(),
        "c5_mixture_identity": mixture_identity(),
        "stochastic_scalings": released_scalings(require_repeat=args.require_repeat),
    }
    results["pass"] = all(value["pass"] for key, value in results.items() if key != "pass")
    (OUT / "independent_verdict.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    if not results["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
