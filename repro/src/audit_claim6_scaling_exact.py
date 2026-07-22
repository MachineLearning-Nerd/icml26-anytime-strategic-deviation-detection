#!/usr/bin/env python3
"""Independent stdlib-only audit of Claim 6 source outputs and controls.

This intentionally does not import the primary verifier or NumPy.  It uses a
separate least-squares implementation over the exact outputs embedded in the
authors' executed notebooks at commit 42b8f0edfe76fb9dd006e9cab84f6cb8b75849c6.
"""

from __future__ import annotations

import hashlib
import json
import math


SOCCER_EPS = [0.05, 0.10, 0.20, 0.30, 0.50]
SOCCER_TAU = [1322.0, 374.0, 118.9, 58.5, 16.4]
PREDATOR_EPS = [0.05, 0.10, 0.20, 0.30, 0.40, 0.60, 0.80]
PREDATOR_TAU = [2413.6, 636.7, 156.4, 66.6, 41.8, 16.7, 9.8]
MONITOR_GRID = [0.10, 0.30, 0.50, 0.70, 0.90]


def independent_fit(epsilon: list[float], tau: list[float]) -> tuple[float, float]:
    x = [math.log(value) for value in epsilon]
    y = [math.log(value) for value in tau]
    xbar = math.fsum(x) / len(x)
    ybar = math.fsum(y) / len(y)
    slope = math.fsum((a - xbar) * (b - ybar) for a, b in zip(x, y)) / math.fsum(
        (a - xbar) ** 2 for a in x
    )
    intercept = ybar - slope * xbar
    residual = math.fsum((b - (slope * a + intercept)) ** 2 for a, b in zip(x, y))
    total = math.fsum((b - ybar) ** 2 for b in y)
    return slope, 1.0 - residual / total


def main() -> int:
    soccer_slope, soccer_r2 = independent_fit(SOCCER_EPS, SOCCER_TAU)
    predator_slope, predator_r2 = independent_fit(PREDATOR_EPS, PREDATOR_TAU)
    soccer_scaled = [t * e * e for e, t in zip(SOCCER_EPS, SOCCER_TAU)]
    predator_scaled = [t * e * e for e, t in zip(PREDATOR_EPS, PREDATOR_TAU)]
    off_grid = [e for e in PREDATOR_EPS if e not in MONITOR_GRID]

    # Distinct failure controls: scramble the epsilon pairing and replace the
    # measured times by a linear 1/epsilon trend.  Neither can pass a -2 gate.
    scrambled_slope, _ = independent_fit(PREDATOR_EPS, list(reversed(PREDATOR_TAU)))
    inverse_linear_slope, _ = independent_fit(PREDATOR_EPS, [1.0 / e for e in PREDATOR_EPS])

    checks = {
        "soccer_slope": -2.20 <= soccer_slope <= -1.60,
        "soccer_r2": soccer_r2 >= 0.99,
        "soccer_tau_epsilon_squared_bounded": max(soccer_scaled) / min(soccer_scaled) <= 1.65,
        "predator_slope": -2.20 <= predator_slope <= -1.80,
        "predator_r2": predator_r2 >= 0.995,
        "predator_tau_epsilon_squared_bounded": max(predator_scaled) / min(predator_scaled) <= 1.15,
        "unknown_magnitude_protocol_has_five_off_grid_truths": off_grid == [0.05, 0.20, 0.40, 0.60, 0.80],
        "scrambled_pairing_fails": not (-2.20 <= scrambled_slope <= -1.60),
        "inverse_linear_control_fails": not (-2.20 <= inverse_linear_slope <= -1.60),
    }
    result = {
        "audit": "independent Claim 6 scaling and unknown-epsilon protocol audit",
        "soccer": {"slope": soccer_slope, "r2": soccer_r2,
                   "tau_times_epsilon_squared": soccer_scaled},
        "predator_prey": {"slope": predator_slope, "r2": predator_r2,
                          "tau_times_epsilon_squared": predator_scaled,
                          "off_grid_true_epsilons": off_grid},
        "negative_controls": {"scrambled_slope": scrambled_slope,
                              "inverse_linear_slope": inverse_linear_slope},
        "checks": checks,
        "audit_passed": all(checks.values()),
    }
    canonical = json.dumps(result, sort_keys=True, separators=(",", ":"))
    print(json.dumps(result, indent=2, sort_keys=True))
    print("AUDIT_SHA256=" + hashlib.sha256(canonical.encode()).hexdigest())
    return 0 if result["audit_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
