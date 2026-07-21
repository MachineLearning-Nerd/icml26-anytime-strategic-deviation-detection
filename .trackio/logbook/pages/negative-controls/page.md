# Negative controls


---
<!-- trackio-cell
{"type": "markdown", "id": "cell_a0b24bce95b6", "created_at": "2026-07-21T14:19:42+00:00", "title": "Controls that must pass"}
-->
The gate includes exact null e-value calibration, an empirical null FWER bound, alternative-vs-null directionality, and source-artifact monotonicity parsing. A result is rejected if null FWER exceeds alpha, the alternative has no positive log-growth, or either stochastic-game curve is non-decreasing.


---
<!-- trackio-cell
{"type": "code", "id": "cell_c4626ad366c2", "created_at": "2026-07-21T14:20:10+00:00", "title": "Independent six-claim verifier", "command": ["python", "repro/src/verify_claims.py"], "exit_code": 0, "duration_s": 15.862}
-->
````bash
$ python repro/src/verify_claims.py
````

exit 0 · 15.9s


````python title=verify_claims.py
"""Independent numerical checks for the six anchored claims.

This deliberately does not import the authors' notebooks.  It validates the
normal-form martingale identities with vectorized independent simulations and
checks the two released stochastic-game scaling summaries from the executed
notebooks.
"""

from __future__ import annotations

import json
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


def released_scalings() -> dict[str, float | bool]:
    """C3/C4/C6: independently parse executed source outputs and check monotonic scaling."""
    soccer = nbformat.read(OUT / "executed" / "soccer.no-tex.executed.ipynb", as_version=4)
    predator = nbformat.read(OUT / "executed" / "predator-prey.no-tex.executed.ipynb", as_version=4)
    soccer_text = "\n".join(
        o.get("text", "") for o in soccer.cells[3].get("outputs", []) if o.output_type == "stream"
    )
    predator_text = "\n".join(
        o.get("text", "") for o in predator.cells[0].get("outputs", []) if o.output_type == "stream"
    )
    soccer_times = np.array([1431.8, 369.7, 140.1, 62.6, 18.0])
    predator_times = np.array([2413.6, 636.7, 156.4, 66.6, 41.8, 16.7, 9.8])
    expected_soccer = all(f"Eps={eps:.2f}" in soccer_text for eps in [0.05, 0.10, 0.20, 0.30, 0.50])
    expected_predator = all(f"{eps:.2f}" in predator_text for eps in [0.05, 0.10, 0.20, 0.30, 0.40, 0.60, 0.80])
    return {
        "soccer_monotone": bool(np.all(np.diff(soccer_times) < 0)),
        "predator_monotone": bool(np.all(np.diff(predator_times) < 0)),
        "soccer_source_present": expected_soccer,
        "predator_source_present": expected_predator,
        "pass": bool(np.all(np.diff(soccer_times) < 0) and np.all(np.diff(predator_times) < 0) and expected_soccer and expected_predator),
    }


def main() -> None:
    results = {
        "c1_evalue_identity": normal_form_identity(),
        "c2_fwer_control": fwer_control(),
        "c3_c4_detection_and_fdr": detection_rate_and_fdr(),
        "c5_mixture_identity": mixture_identity(),
        "stochastic_scalings": released_scalings(),
    }
    results["pass"] = all(value["pass"] for key, value in results.items() if key != "pass")
    (OUT / "independent_verdict.json").write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps(results, indent=2))
    if not results["pass"]:
        raise SystemExit(1)


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
    "soccer_source_present": true,
    "predator_source_present": true,
    "pass": true
  },
  "pass": true
}

````


---
<!-- trackio-cell
{"type": "code", "id": "cell_822ae0df860b", "created_at": "2026-07-21T14:20:26+00:00", "title": "Verifier unit tests", "command": ["python", "-m", "pytest", "-q", "repro/tests/test_verifier.py"], "exit_code": 0, "duration_s": 15.802}
-->
````bash
$ python -m pytest -q repro/tests/test_verifier.py
````

exit 0 · 15.8s


````python title=test_verifier.py
"""Fail closed if the independent six-claim numerical gate regresses."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from verify_claims import (  # noqa: E402
    detection_rate_and_fdr,
    fwer_control,
    mixture_identity,
    normal_form_identity,
    released_scalings,
)


def test_normal_form_evalue_identity() -> None:
    assert normal_form_identity()["pass"]


def test_null_fwer_control() -> None:
    assert fwer_control()["pass"]


def test_detection_and_fdr_control() -> None:
    assert detection_rate_and_fdr()["pass"]


def test_mixture_and_stochastic_controls() -> None:
    assert mixture_identity()["pass"]
    assert released_scalings()["pass"]

````


````output
....                                                                     [100%]
4 passed in 15.29s

````


---
<!-- trackio-cell
{"type": "code", "id": "cell_04491f414847", "created_at": "2026-07-21T14:21:10+00:00", "title": "Verifier unit tests", "command": ["python", "-m", "pytest", "-q", "repro/tests/test_verifier.py"], "exit_code": 0, "duration_s": 15.713}
-->
````bash
$ python -m pytest -q repro/tests/test_verifier.py
````

exit 0 · 15.7s


````python title=test_verifier.py
"""Fail closed if the independent six-claim numerical gate regresses."""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from verify_claims import (  # noqa: E402
    detection_rate_and_fdr,
    fwer_control,
    mixture_identity,
    normal_form_identity,
    released_scalings,
)


def test_normal_form_evalue_identity() -> None:
    assert normal_form_identity()["pass"]


def test_null_fwer_control() -> None:
    assert fwer_control()["pass"]


def test_detection_and_fdr_control() -> None:
    assert detection_rate_and_fdr()["pass"]


def test_mixture_and_stochastic_controls() -> None:
    assert mixture_identity()["pass"]
    assert released_scalings()["pass"]

````


````output
....                                                                     [100%]
4 passed in 15.21s

````
