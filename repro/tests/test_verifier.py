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
