"""Boundary-layer tests for judge I/O handling.

AC-FR-01-01, PRD §8.1 INVALID_SIZE — Boundary handles None before domain resolve().
"""

from __future__ import annotations

from unittest.mock import patch

import pytest

from boundary.cli.judge_handler import JudgeHandler
from entity.models.judge_result import JudgeResult
from tests.conftest import EXPECTED_INVALID_SIZE_CODE, EXPECTED_INVALID_SIZE_MESSAGE

pytestmark = pytest.mark.ac_fr_01_01

_RESOLVE_PATCH = "control.services.judge_use_case.MagicSquareJudge.resolve"


class TestBoundaryNormalFailureReturn:
    """정상 실패 반환 — Boundary returns INVALID_SIZE for None input."""

    def test_none_grid_returns_invalid_size_code_boundary(
        self, invalid_size_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Boundary returns failure code."""
        # AC-FR-01-01
        # Given: handler and None grid
        handler = JudgeHandler()
        grid = invalid_size_none
        # When: handle is invoked
        with patch(_RESOLVE_PATCH, autospec=True):
            result = handler.handle(grid)
        # Then: code is INVALID_SIZE
        assert result.code == EXPECTED_INVALID_SIZE_CODE

    def test_none_grid_returns_judge_result_boundary(
        self, invalid_size_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Boundary returns JudgeResult DTO."""
        # AC-FR-01-01
        # Given: handler and None grid
        handler = JudgeHandler()
        grid = invalid_size_none
        # When: handle is invoked
        with patch(_RESOLVE_PATCH, autospec=True):
            result = handler.handle(grid)
        # Then: typed failure result structure
        assert isinstance(result, JudgeResult)

    def test_empty_list_returns_invalid_size_boundary(
        self, invalid_size_empty: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Boundary rejects empty list."""
        # AC-FR-01-01
        # Given: empty grid
        handler = JudgeHandler()
        grid = invalid_size_empty
        # When: handle is invoked
        with patch(_RESOLVE_PATCH, autospec=True):
            result = handler.handle(grid)
        # Then: INVALID_SIZE returned
        assert result.code == EXPECTED_INVALID_SIZE_CODE

    def test_3x4_grid_returns_invalid_size_boundary(
        self, invalid_size_3x4: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Boundary rejects 3×4 grid."""
        # AC-FR-01-01
        # Given: 3×4 grid
        handler = JudgeHandler()
        grid = invalid_size_3x4
        # When: handle is invoked
        with patch(_RESOLVE_PATCH, autospec=True):
            result = handler.handle(grid)
        # Then: INVALID_SIZE returned
        assert result.message == EXPECTED_INVALID_SIZE_MESSAGE

    def test_none_grid_boundary_does_not_raise(
        self, invalid_size_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Boundary must not raise on None."""
        # AC-FR-01-01
        # Given: None grid
        handler = JudgeHandler()
        grid = invalid_size_none
        # When: handle is invoked
        with patch(_RESOLVE_PATCH, autospec=True):
            result = handler.handle(grid)
        # Then: structured failure, no exception
        assert result.code == EXPECTED_INVALID_SIZE_CODE


class TestBoundaryIsolationResolveZeroCalls:
    """격리 검증 — Boundary path must not invoke domain resolve()."""

    def test_none_grid_resolve_zero_calls_boundary(
        self, invalid_size_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Boundary None: resolve() 0 calls."""
        # AC-FR-01-01
        # Given: handler and spied resolve()
        handler = JudgeHandler()
        grid = invalid_size_none
        # When: handle processes None
        with patch(_RESOLVE_PATCH, autospec=True) as mock_resolve:
            handler.handle(grid)
            # Then: domain resolve() never reached
            mock_resolve.assert_not_called()

    def test_empty_list_resolve_zero_calls_boundary(
        self, invalid_size_empty: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Boundary empty: resolve() 0 calls."""
        # AC-FR-01-01
        # Given: handler and empty grid
        handler = JudgeHandler()
        grid = invalid_size_empty
        # When: handle processes empty grid
        with patch(_RESOLVE_PATCH, autospec=True) as mock_resolve:
            handler.handle(grid)
            # Then: resolve() not invoked
            mock_resolve.assert_not_called()

    def test_zero_cols_resolve_zero_calls_boundary(
        self, invalid_size_zero_cols: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Boundary [[]]*4: resolve() 0 calls."""
        # AC-FR-01-01
        # Given: handler and zero-column grid
        handler = JudgeHandler()
        grid = invalid_size_zero_cols
        # When: handle processes grid
        with patch(_RESOLVE_PATCH, autospec=True) as mock_resolve:
            handler.handle(grid)
            # Then: resolve() stays at zero
            mock_resolve.assert_not_called()

    def test_3x4_resolve_zero_calls_boundary(
        self, invalid_size_3x4: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Boundary 3×4: resolve() 0 calls."""
        # AC-FR-01-01
        # Given: handler and 3×4 grid
        handler = JudgeHandler()
        grid = invalid_size_3x4
        # When: handle processes size mismatch
        with patch(_RESOLVE_PATCH, autospec=True) as mock_resolve:
            handler.handle(grid)
            # Then: early exit before resolve()
            mock_resolve.assert_not_called()

    def test_boundary_none_branch_skips_resolve(
        self, invalid_size_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — None branch handled before resolve()."""
        # AC-FR-01-01
        # Given: Boundary receives None (Track B: resolve must not see None)
        handler = JudgeHandler()
        grid = invalid_size_none
        # When: full Boundary stack executes
        with patch(_RESOLVE_PATCH, autospec=True) as mock_resolve:
            result = handler.handle(grid)
            # Then: None handled at boundary/control; resolve() count is 0
            assert mock_resolve.call_count == 0
            assert result.code == EXPECTED_INVALID_SIZE_CODE


class TestBoundaryMessageExactMatch:
    """메시지 동일성 — Boundary serializes PRD §8.1 message exactly."""

    def test_none_message_exact_match_boundary(self, invalid_size_none: None) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Boundary None message exact match."""
        # AC-FR-01-01
        # Given: PRD §8.1 message and None grid
        expected = EXPECTED_INVALID_SIZE_MESSAGE
        handler = JudgeHandler()
        # When: handle returns failure
        with patch(_RESOLVE_PATCH, autospec=True):
            result = handler.handle(invalid_size_none)
        # Then: character-level match
        assert result.message == expected

    def test_empty_message_exact_match_boundary(
        self, invalid_size_empty: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Boundary empty message exact match."""
        # AC-FR-01-01
        # Given: empty grid
        handler = JudgeHandler()
        # When: handle returns failure
        with patch(_RESOLVE_PATCH, autospec=True):
            result = handler.handle(invalid_size_empty)
        # Then: PRD §8.1 wording preserved
        assert result.message == "Grid must be 4x4."

    def test_3x4_message_exact_match_boundary(
        self, invalid_size_3x4: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — Boundary 3×4 message exact match."""
        # AC-FR-01-01
        # Given: 3×4 grid
        handler = JudgeHandler()
        # When: handle returns failure
        with patch(_RESOLVE_PATCH, autospec=True):
            result = handler.handle(invalid_size_3x4)
        # Then: exact PRD message
        assert result.message == EXPECTED_INVALID_SIZE_MESSAGE

    def test_code_string_type_boundary(self, invalid_size_none: None) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — code is exact str INVALID_SIZE."""
        # AC-FR-01-01
        # Given: None grid
        handler = JudgeHandler()
        # When: handle returns failure
        with patch(_RESOLVE_PATCH, autospec=True):
            result = handler.handle(invalid_size_none)
        # Then: code is str and equals INVALID_SIZE exactly
        assert isinstance(result.code, str)
        assert result.code == "INVALID_SIZE"

    def test_message_string_type_boundary(self, invalid_size_none: None) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — message is exact str per PRD."""
        # AC-FR-01-01
        # Given: None grid
        handler = JudgeHandler()
        # When: handle returns failure
        with patch(_RESOLVE_PATCH, autospec=True):
            result = handler.handle(invalid_size_none)
        # Then: message is str matching PRD §8.1
        assert isinstance(result.message, str)
        assert result.message == "Grid must be 4x4."
