"""Boundary flow isolation tests (U-FLOW-02)."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from boundary.ui_boundary import UIBoundary
from control.solve_partial_magic_square import SolvePartialMagicSquare

pytestmark = pytest.mark.solve_track


class TestInvalidInputNeverCallsExecute:
    """U-FLOW-02 — invalid input must not invoke Control resolve."""

    @pytest.mark.parametrize("grid", [None, []])
    def test_invalid_input_never_calls_resolve(self, grid: object) -> None:
        """U-FLOW-02: None or empty grid → resolve() call count 0."""
        mock_use_case = MagicMock(spec=SolvePartialMagicSquare)
        boundary = UIBoundary(solve_use_case=mock_use_case)
        boundary.solve(grid)  # type: ignore[arg-type]
        mock_use_case.resolve.assert_not_called()
