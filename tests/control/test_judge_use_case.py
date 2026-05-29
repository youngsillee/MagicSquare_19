"""Control-layer tests for judge use-case early termination.

AC-FR-01-01, PRD §8.1 INVALID_SIZE — shape check before domain resolve().
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from control.services.judge_use_case import JudgeUseCase
from tests.conftest import EXPECTED_INVALID_SIZE_CODE, EXPECTED_INVALID_SIZE_MESSAGE

pytestmark = pytest.mark.ac_fr_01_01

_RESOLVE_PATCH = "control.services.judge_use_case.MagicSquareJudge.resolve"


class TestIsolationResolveZeroCalls:
    """격리 검증 — resolve() must not be invoked for invalid shape inputs."""

    def test_none_grid_resolve_zero_calls(self, invalid_size_none: None) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — None grid: resolve() 0 calls."""
        # AC-FR-01-01
        # Given: use case and spied domain resolve()
        use_case = JudgeUseCase()
        grid = invalid_size_none
        # When: execute with None grid
        with patch(_RESOLVE_PATCH, autospec=True) as mock_resolve:
            result = use_case.execute(grid)
            # Then: resolve() never called; INVALID_SIZE returned
            mock_resolve.assert_not_called()
            assert result.code == EXPECTED_INVALID_SIZE_CODE

    def test_empty_list_resolve_zero_calls(
        self, invalid_size_empty: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — empty grid: resolve() 0 calls."""
        # AC-FR-01-01
        # Given: use case and spied resolve()
        use_case = JudgeUseCase()
        grid = invalid_size_empty
        # When: execute with empty grid
        with patch(_RESOLVE_PATCH, autospec=True) as mock_resolve:
            result = use_case.execute(grid)
            # Then: resolve() never called
            mock_resolve.assert_not_called()
            assert result.code == EXPECTED_INVALID_SIZE_CODE

    def test_zero_column_grid_resolve_zero_calls(
        self, invalid_size_zero_cols: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — [[]]*4: resolve() 0 calls."""
        # AC-FR-01-01
        # Given: use case and spied resolve()
        use_case = JudgeUseCase()
        grid = invalid_size_zero_cols
        # When: execute with zero-column grid
        with patch(_RESOLVE_PATCH, autospec=True) as mock_resolve:
            result = use_case.execute(grid)
            # Then: resolve() never called
            mock_resolve.assert_not_called()
            assert result.message == EXPECTED_INVALID_SIZE_MESSAGE

    def test_3x4_grid_resolve_zero_calls(
        self, invalid_size_3x4: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 3×4 grid: resolve() 0 calls."""
        # AC-FR-01-01
        # Given: use case and spied resolve()
        use_case = JudgeUseCase()
        grid = invalid_size_3x4
        # When: execute with size-mismatch grid
        with patch(_RESOLVE_PATCH, autospec=True) as mock_resolve:
            use_case.execute(grid)
            # Then: domain resolve() is not reached
            mock_resolve.assert_not_called()

    def test_resolve_mock_called_once_fails_test_contract(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — spy detects erroneous resolve() call."""
        # AC-FR-01-01
        # Given: use case; resolve() incorrectly invoked once (simulated bug)
        use_case = JudgeUseCase()
        grid = None
        # When: execute under spy
        with patch(_RESOLVE_PATCH, autospec=True) as mock_resolve:
            use_case.execute(grid)
            # Then: assert_not_called passes only when resolve() stays at 0
            assert mock_resolve.call_count == 0, (
                "resolve() must not be called when grid is None (AC-FR-01-01)"
            )


class TestNormalFailureReturnControl:
    """정상 실패 반환 — Control layer returns INVALID_SIZE for None grid."""

    def test_none_grid_returns_invalid_size_code_control(
        self, invalid_size_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Control returns failure code."""
        # AC-FR-01-01
        # Given: JudgeUseCase and None grid
        use_case = JudgeUseCase()
        grid = invalid_size_none
        # When: execute is called
        with patch(_RESOLVE_PATCH, autospec=True):
            result = use_case.execute(grid)
        # Then: structured failure code returned
        assert result.code == EXPECTED_INVALID_SIZE_CODE

    def test_none_grid_returns_invalid_size_message_control(
        self, invalid_size_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Control returns PRD message."""
        # AC-FR-01-01
        # Given: JudgeUseCase and None grid
        use_case = JudgeUseCase()
        grid = invalid_size_none
        # When: execute is called
        with patch(_RESOLVE_PATCH, autospec=True):
            result = use_case.execute(grid)
        # Then: message matches PRD §8.1
        assert result.message == EXPECTED_INVALID_SIZE_MESSAGE

    def test_empty_list_returns_invalid_size_control(
        self, invalid_size_empty: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Control rejects empty grid."""
        # AC-FR-01-01
        # Given: empty grid
        use_case = JudgeUseCase()
        grid = invalid_size_empty
        # When: execute is called
        with patch(_RESOLVE_PATCH, autospec=True) as mock_resolve:
            result = use_case.execute(grid)
        # Then: INVALID_SIZE without domain call
        mock_resolve.assert_not_called()
        assert result.code == EXPECTED_INVALID_SIZE_CODE

    def test_3x4_grid_returns_invalid_size_control(
        self, invalid_size_3x4: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Control rejects 3×4 grid."""
        # AC-FR-01-01
        # Given: 3×4 grid
        use_case = JudgeUseCase()
        grid = invalid_size_3x4
        # When: execute is called
        with patch(_RESOLVE_PATCH, autospec=True):
            result = use_case.execute(grid)
        # Then: INVALID_SIZE returned
        assert result.code == EXPECTED_INVALID_SIZE_CODE

    def test_none_grid_control_does_not_raise(self, invalid_size_none: None) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Control must not raise on None."""
        # AC-FR-01-01
        # Given: None grid
        use_case = JudgeUseCase()
        grid = invalid_size_none
        # When: execute is called
        with patch(_RESOLVE_PATCH, autospec=True):
            result = use_case.execute(grid)
        # Then: structured result instead of exception
        assert result.code == EXPECTED_INVALID_SIZE_CODE
