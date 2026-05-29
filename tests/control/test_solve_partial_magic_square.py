"""Control-layer tests for partial magic square solve use case (D-SOL-01~04)."""

from __future__ import annotations

import pytest

from control.solve_partial_magic_square import SolvePartialMagicSquare
from entity.exceptions.domain_errors import UnsolvableDomainError
from tests.solve_grids import (
    EXPECTED_G1_SOLUTION,
    EXPECTED_G2_SOLUTION,
    GRID_G1,
    GRID_G2,
    GRID_G3,
)

pytestmark = pytest.mark.solve_track


class TestSolutionG1Fixture:
    """D-SOL-01 — G1 fixture matches TwoCellSolver output (no domain mocks)."""

    def test_solution_g1_matches_domain_solver(self) -> None:
        """D-SOL-01: G1 resolves to domain solver placement [2,2,10,3,3,7]."""
        use_case = SolvePartialMagicSquare()
        assert use_case.resolve(GRID_G1) == EXPECTED_G1_SOLUTION


class TestSolutionG2Fixture:
    """D-SOL-02 — G2 fixture matches TwoCellSolver output."""

    def test_solution_g2_matches_domain_solver(self) -> None:
        """D-SOL-02: G2 resolves via Step B to [3,3,6,4,4,1]."""
        use_case = SolvePartialMagicSquare()
        assert use_case.resolve(GRID_G2) == EXPECTED_G2_SOLUTION


class TestSolutionG3Unsolvable:
    """D-SOL-03 — G3 raises domain error when no completion exists."""

    def test_solution_g3_unsolvable_raises_domain_error(self) -> None:
        """D-SOL-03: G3 raises UnsolvableDomainError."""
        use_case = SolvePartialMagicSquare()
        with pytest.raises(UnsolvableDomainError):
            use_case.resolve(GRID_G3)


class TestSolutionReturnShape:
    """D-SOL-04 — output contract: len 6, 1-index coords, values in range."""

    def test_solution_return_shape_one_indexed(self) -> None:
        """D-SOL-04: G1 output has six elements with 1-index coordinates."""
        result = SolvePartialMagicSquare().resolve(GRID_G1)
        assert len(result) == 6
        rows = (result[0], result[3])
        cols = (result[1], result[4])
        nums = (result[2], result[5])
        assert all(1 <= value <= 4 for value in rows + cols)
        assert all(1 <= value <= 16 for value in nums)
