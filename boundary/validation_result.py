"""Explicit validation outcome for Boundary input checks (replaces NotImplementedError flow)."""

from __future__ import annotations

from dataclasses import dataclass

from boundary.schemas import FailureResponse


@dataclass(frozen=True)
class ValidationOk:
    """Marker: grid passed Boundary validation and may proceed to Control."""


ValidationResult = FailureResponse | ValidationOk

VALIDATION_OK = ValidationOk()
