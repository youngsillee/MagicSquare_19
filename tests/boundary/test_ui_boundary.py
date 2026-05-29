"""Boundary solve orchestration tests (U-OUT-01~03)."""

from __future__ import annotations

import pytest

from boundary.schemas import FailureResponse, SuccessResponse
from boundary.ui_boundary import UIBoundary
from control.solve_partial_magic_square import SolvePartialMagicSquare
from tests.solve_grids import (
    EXPECTED_G1_SOLUTION,
    GRID_G1,
    GRID_G3,
)

pytestmark = pytest.mark.solve_track

_E006_CODE = "E006"


@pytest.fixture
def boundary() -> UIBoundary:
    """UIBoundary wired to real solve use case."""
    return UIBoundary(solve_use_case=SolvePartialMagicSquare())


class TestSolveValidPartial:
    """U-OUT-01 — successful solve returns six integers."""

    def test_solve_valid_partial_returns_six_ints(self, boundary: UIBoundary) -> None:
        """U-OUT-01: G1 success returns int[6]."""
        result = boundary.solve(GRID_G1)
        assert isinstance(result, SuccessResponse)
        assert result.type == "OK"
        assert len(result.data) == 6
        assert all(isinstance(value, int) for value in result.data)


class TestSolveOneIndexedCoordinates:
    """U-OUT-02 — coordinates are 1-indexed."""

    def test_solve_success_coordinates_are_one_indexed(
        self, boundary: UIBoundary
    ) -> None:
        """U-OUT-02: G1 matches expected 1-index solution."""
        result = boundary.solve(GRID_G1)
        assert isinstance(result, SuccessResponse)
        assert result.data == EXPECTED_G1_SOLUTION
        rows = (result.data[0], result.data[3])
        cols = (result.data[1], result.data[4])
        assert all(1 <= value <= 4 for value in rows + cols)


class TestSolveNoValidSolution:
    """U-OUT-03 — unsolvable grid returns E006 envelope."""

    def test_solve_no_valid_solution_returns_e006(self, boundary: UIBoundary) -> None:
        """U-OUT-03: G3 returns E006 FailureResponse, not an exception."""
        result = boundary.solve(GRID_G3)
        assert isinstance(result, FailureResponse)
        assert result.error.code == _E006_CODE
