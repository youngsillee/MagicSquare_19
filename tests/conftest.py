"""Shared fixtures and constants for AC-FR-01-01 tests."""

from __future__ import annotations

import pytest

# PRD §8.1 — INVALID_SIZE contract (AC-FR-01-01)
EXPECTED_INVALID_SIZE_CODE = "INVALID_SIZE"
EXPECTED_INVALID_SIZE_MESSAGE = "Grid must be 4x4."


@pytest.fixture
def invalid_size_none() -> None:
    """Explicit None grid input (BV-01)."""
    return None


@pytest.fixture
def invalid_size_empty() -> list[list[int]]:
    """Empty list grid — zero rows (BV-02)."""
    return []


@pytest.fixture
def invalid_size_zero_cols() -> list[list[int]]:
    """Four rows with zero columns each (BV-03)."""
    return [[]] * 4


@pytest.fixture
def invalid_size_3x4() -> list[list[int]]:
    """Three rows by four columns — row count mismatch (BV-04)."""
    return [[0] * 4 for _ in range(3)]


@pytest.fixture
def invalid_size_4x3() -> list[list[int]]:
    """Four rows by three columns — column count mismatch (BV-05)."""
    return [[0] * 3 for _ in range(4)]


@pytest.fixture
def invalid_size_5x5() -> list[list[int]]:
    """Five rows by five columns — both dimensions exceed (BV-08)."""
    return [[0] * 5 for _ in range(5)]
