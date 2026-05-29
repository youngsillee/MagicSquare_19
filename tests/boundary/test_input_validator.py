"""Boundary input validation tests (U-IN-01~05)."""

from __future__ import annotations

import copy

import pytest

from boundary.input_validator import InputValidator
from boundary.schemas import FailureResponse
from boundary.validation_result import ValidationOk
from tests.conftest import EXPECTED_INVALID_SIZE_CODE, EXPECTED_INVALID_SIZE_MESSAGE
from tests.solve_grids import GRID_G0, GRID_G1

pytestmark = pytest.mark.solve_track

_E002_CODE = "E002"
_E002_MESSAGE = "INVALID_EMPTY_COUNT: expected exactly 2 empty cells (0)"
_E004_CODE = "E004"
_E004_MESSAGE = "INVALID_CELL_VALUE: each cell must be 0 or 1..16"
_E005_CODE = "E005"
_E005_MESSAGE = "DUPLICATE_VALUE: non-zero values must be unique"


@pytest.fixture
def validator() -> InputValidator:
    """Fresh InputValidator instance."""
    return InputValidator()


class TestValidateMatrixNull:
    """U-IN-01 — null input (implementation SSOT: INVALID_SIZE)."""

    def test_validate_matrix_null_returns_invalid_size(
        self, validator: InputValidator
    ) -> None:
        """U-IN-01: None grid returns INVALID_SIZE failure envelope."""
        result = validator.validate(None)
        assert isinstance(result, FailureResponse)
        assert result.error.code == EXPECTED_INVALID_SIZE_CODE
        assert result.error.message == EXPECTED_INVALID_SIZE_MESSAGE


class TestValidateInvalidSize:
    """U-IN-02 — non-4×4 shapes (INVALID_SIZE per AC-FR-01-01 alignment)."""

    @pytest.mark.parametrize(
        "grid",
        [
            [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],
            [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]],
            [[0] * 4 for _ in range(5)],
            [],
        ],
    )
    def test_validate_invalid_size_returns_invalid_size(
        self, validator: InputValidator, grid: list[list[int]]
    ) -> None:
        """U-IN-02: wrong row/column count returns INVALID_SIZE."""
        result = validator.validate(grid)
        assert isinstance(result, FailureResponse)
        assert result.error.code == EXPECTED_INVALID_SIZE_CODE


class TestValidateEmptyCellCount:
    """U-IN-03a/b — empty cell count must be exactly two."""

    def test_validate_zero_empty_cells_returns_e002(
        self, validator: InputValidator
    ) -> None:
        """U-IN-03a: G0 (no blanks) returns E002."""
        result = validator.validate(GRID_G0)
        assert isinstance(result, FailureResponse)
        assert result.error.code == _E002_CODE
        assert result.error.message == _E002_MESSAGE

    def test_validate_three_empty_cells_returns_e002(
        self, validator: InputValidator
    ) -> None:
        """U-IN-03b: three zeros returns E002."""
        grid = copy.deepcopy(GRID_G1)
        grid[0][1] = 0
        result = validator.validate(grid)
        assert isinstance(result, FailureResponse)
        assert result.error.code == _E002_CODE


class TestValidateOutOfRange:
    """U-IN-04 — cell values must be 0 or 1..16."""

    def test_validate_negative_value_returns_e004(
        self, validator: InputValidator
    ) -> None:
        """U-IN-04a: -1 returns E004."""
        grid = copy.deepcopy(GRID_G1)
        grid[0][0] = -1
        result = validator.validate(grid)
        assert isinstance(result, FailureResponse)
        assert result.error.code == _E004_CODE
        assert result.error.message == _E004_MESSAGE

    def test_validate_value_17_returns_e004(self, validator: InputValidator) -> None:
        """U-IN-04b: 17 returns E004."""
        grid = copy.deepcopy(GRID_G1)
        grid[0][0] = 17
        result = validator.validate(grid)
        assert isinstance(result, FailureResponse)
        assert result.error.code == _E004_CODE


class TestValidateDuplicateNonzero:
    """U-IN-05 — duplicate non-zero values."""

    def test_validate_duplicate_nonzero_returns_e005(
        self, validator: InputValidator
    ) -> None:
        """U-IN-05: duplicate non-zero returns E005."""
        grid = copy.deepcopy(GRID_G1)
        grid[3][3] = grid[3][2]
        result = validator.validate(grid)
        assert isinstance(result, FailureResponse)
        assert result.error.code == _E005_CODE
        assert result.error.message == _E005_MESSAGE


class TestValidateSuccess:
    """Valid partial grid passes validation."""

    def test_validate_g1_returns_ok(self, validator: InputValidator) -> None:
        """G1 passes all Boundary input checks."""
        assert isinstance(validator.validate(GRID_G1), ValidationOk)
