"""Entity domain service tests (D-LOC-01, D-MIS-01, solver contract)."""

from __future__ import annotations

import pytest

from entity.services.empty_cell_locator import EmptyCellLocator
from entity.services.missing_number_finder import MissingNumberFinder
from entity.services.two_cell_solver import TwoCellSolver
from tests.solve_grids import EXPECTED_G1_SOLUTION, GRID_G1

pytestmark = pytest.mark.solve_track


class TestFindBlankCoordsG1:
    """D-LOC-01 — blank coordinates in row-major 1-index order."""

    def test_find_blank_coords_g1_row_major(self) -> None:
        """D-LOC-01: G1 empty cells are (2,2) and (3,3) in scan order."""
        pair = EmptyCellLocator().locate(GRID_G1)
        assert (pair.first.row, pair.first.col) == (2, 2)
        assert (pair.second.row, pair.second.col) == (3, 3)


class TestFindNotExistNumsG1:
    """D-MIS-01 — missing values sorted ascending."""

    def test_find_not_exist_nums_g1_sorted(self) -> None:
        """D-MIS-01: G1 missing numbers are 7 and 10."""
        pair = MissingNumberFinder().find(GRID_G1)
        assert pair.smaller == 7
        assert pair.larger == 10


class TestTwoCellSolverG1:
    """Solver returns placement order from successful step."""

    def test_two_cell_solver_g1_matches_expected(self) -> None:
        """TwoCellSolver output matches control-layer G1 contract."""
        assert TwoCellSolver().solve(GRID_G1).values == EXPECTED_G1_SOLUTION
