"""Entity-layer tests for grid shape validation.

AC-FR-01-01, PRD §8.1 INVALID_SIZE — grid format pre-check before domain judge.
"""

from __future__ import annotations

import pytest

from entity.models.judge_result import JudgeResult
from entity.rules.grid_shape_validator import validate_grid_shape
from tests.conftest import EXPECTED_INVALID_SIZE_CODE, EXPECTED_INVALID_SIZE_MESSAGE
from tests.solve_grids import GRID_G0

pytestmark = pytest.mark.ac_fr_01_01


class TestNormalFailureReturn:
    """정상 실패 반환 — invalid grid must yield structured INVALID_SIZE."""

    def test_none_grid_returns_invalid_size_code(self, invalid_size_none: None) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — None grid returns failure code."""
        # AC-FR-01-01
        # Given: grid is explicitly None
        grid = invalid_size_none
        # When: shape validation runs
        result = validate_grid_shape(grid)
        # Then: code is INVALID_SIZE
        assert result.code == EXPECTED_INVALID_SIZE_CODE

    def test_none_grid_returns_judge_result_type(self, invalid_size_none: None) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — None grid returns JudgeResult."""
        # AC-FR-01-01
        # Given: grid is None
        grid = invalid_size_none
        # When: shape validation runs
        result = validate_grid_shape(grid)
        # Then: result is a JudgeResult instance
        assert isinstance(result, JudgeResult)

    def test_none_grid_does_not_raise_exception(self, invalid_size_none: None) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — None grid must not propagate exception."""
        # AC-FR-01-01
        # Given: grid is None
        grid = invalid_size_none
        # When: shape validation runs
        # Then: no exception is raised
        result = validate_grid_shape(grid)
        assert result.code == EXPECTED_INVALID_SIZE_CODE

    def test_none_grid_returns_non_success_indicator(
        self, invalid_size_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — None grid is a failure outcome."""
        # AC-FR-01-01
        # Given: grid is None
        grid = invalid_size_none
        # When: shape validation runs
        result = validate_grid_shape(grid)
        # Then: outcome is failure (not a valid magic square acceptance)
        assert result.code != "VALID"
        assert result.code != "SUCCESS"

    def test_none_grid_happy_path_of_failure_message(
        self, invalid_size_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — None grid returns expected message."""
        # AC-FR-01-01
        # Given: grid is None (happy path of failure)
        grid = invalid_size_none
        # When: shape validation runs
        result = validate_grid_shape(grid)
        # Then: message matches PRD contract
        assert result.message == EXPECTED_INVALID_SIZE_MESSAGE


class TestBoundaryValues:
    """경계값 — malformed grids must all return INVALID_SIZE."""

    def test_empty_list_returns_invalid_size_code(
        self, invalid_size_empty: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — empty list returns failure code."""
        # AC-FR-01-01
        # Given: grid is an empty list
        grid = invalid_size_empty
        # When: shape validation runs
        result = validate_grid_shape(grid)
        # Then: code is INVALID_SIZE
        assert result.code == EXPECTED_INVALID_SIZE_CODE

    def test_zero_column_rows_returns_invalid_size_code(
        self, invalid_size_zero_cols: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — [[]]*4 returns failure code."""
        # AC-FR-01-01
        # Given: grid has four rows with zero columns
        grid = invalid_size_zero_cols
        assert all(len(row) == 0 for row in grid)
        # When: shape validation runs
        result = validate_grid_shape(grid)
        # Then: code is INVALID_SIZE
        assert result.code == EXPECTED_INVALID_SIZE_CODE

    def test_3x4_grid_returns_invalid_size_code(
        self, invalid_size_3x4: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 3×4 grid returns failure code."""
        # AC-FR-01-01
        # Given: grid is 3 rows by 4 columns
        grid = invalid_size_3x4
        assert len(grid) == 3
        assert all(len(row) == 4 for row in grid)
        # When: shape validation runs
        result = validate_grid_shape(grid)
        # Then: code is INVALID_SIZE
        assert result.code == EXPECTED_INVALID_SIZE_CODE

    def test_4x3_grid_returns_invalid_size_code(
        self, invalid_size_4x3: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 4×3 grid returns failure code."""
        # AC-FR-01-01
        # Given: grid is 4 rows by 3 columns
        grid = invalid_size_4x3
        assert len(grid) == 4
        assert all(len(row) == 3 for row in grid)
        # When: shape validation runs
        result = validate_grid_shape(grid)
        # Then: code is INVALID_SIZE
        assert result.code == EXPECTED_INVALID_SIZE_CODE

    def test_5x5_grid_returns_invalid_size_code(
        self, invalid_size_5x5: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 5×5 grid returns failure code."""
        # AC-FR-01-01
        # Given: grid is 5 rows by 5 columns
        grid = invalid_size_5x5
        assert len(grid) == 5
        assert all(len(row) == 5 for row in grid)
        # When: shape validation runs
        result = validate_grid_shape(grid)
        # Then: code is INVALID_SIZE
        assert result.code == EXPECTED_INVALID_SIZE_CODE


class TestMessageExactMatch:
    """메시지 동일성 — PRD §8.1 wording must match character-for-character."""

    def test_none_grid_message_exact_match_prd_8_1(
        self, invalid_size_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — None message exact match."""
        # AC-FR-01-01
        # Given: PRD §8.1 expected message string
        expected = "Grid must be 4x4."
        grid = invalid_size_none
        # When: shape validation runs
        result = validate_grid_shape(grid)
        # Then: message matches character-for-character
        assert result.message == expected

    def test_empty_list_message_exact_match_prd_8_1(
        self, invalid_size_empty: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — empty list message exact match."""
        # AC-FR-01-01
        # Given: empty grid and PRD §8.1 message
        expected = EXPECTED_INVALID_SIZE_MESSAGE
        grid = invalid_size_empty
        # When: shape validation runs
        result = validate_grid_shape(grid)
        # Then: message is byte-identical to PRD wording
        assert result.message == expected

    def test_3x4_grid_message_exact_match_prd_8_1(
        self, invalid_size_3x4: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — 3×4 message exact match."""
        # AC-FR-01-01
        # Given: 3×4 grid and PRD §8.1 message
        expected = EXPECTED_INVALID_SIZE_MESSAGE
        grid = invalid_size_3x4
        # When: shape validation runs
        result = validate_grid_shape(grid)
        # Then: message matches PRD §8.1 exactly
        assert result.message == expected

    def test_message_has_no_leading_or_trailing_whitespace(
        self, invalid_size_none: None
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — message has no extra whitespace."""
        # AC-FR-01-01
        # Given: grid is None
        grid = invalid_size_none
        # When: shape validation runs
        result = validate_grid_shape(grid)
        # Then: message equals stripped form (no padding)
        assert result.message == result.message.strip()
        assert result.message == EXPECTED_INVALID_SIZE_MESSAGE

    def test_message_and_code_pair_consistency(
        self, invalid_size_zero_cols: list[list[int]]
    ) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — code/message pair is consistent."""
        # AC-FR-01-01
        # Given: zero-column grid
        grid = invalid_size_zero_cols
        # When: shape validation runs
        result = validate_grid_shape(grid)
        # Then: INVALID_SIZE always pairs with PRD §8.1 message
        assert result.code == EXPECTED_INVALID_SIZE_CODE
        assert result.message == EXPECTED_INVALID_SIZE_MESSAGE


class TestValidGridShape:
    """Valid 4×4 grid passes shape pre-check (DEF-004 coverage)."""

    def test_complete_grid_shape_passes_pre_check(self) -> None:
        """AC-FR-01-01 — complete 4×4 grid has no INVALID_SIZE result."""
        assert validate_grid_shape(GRID_G0) is None
