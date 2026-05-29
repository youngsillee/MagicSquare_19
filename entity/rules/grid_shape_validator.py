"""Grid shape validation — I-Shape (4×4) pre-check for FR-01.

Judge-track SSOT for INVALID_SIZE (AC-FR-01-01). Solve-track uses
``boundary.input_validator`` at UIBoundary.
"""

from __future__ import annotations

from entity.models.judge_result import JudgeResult

GRID_SIZE = 4
INVALID_SIZE_CODE = "INVALID_SIZE"
INVALID_SIZE_MESSAGE = "Grid must be 4x4."


def validate_grid_shape(grid: object) -> JudgeResult | None:
    """Validate that grid is a 4×4 list-of-lists.

    Args:
        grid: Candidate grid input (may be None or malformed).

    Returns:
        JudgeResult with INVALID_SIZE when shape is invalid; None when shape is valid.
    """
    if _has_invalid_shape(grid):
        return JudgeResult(code=INVALID_SIZE_CODE, message=INVALID_SIZE_MESSAGE)
    return None


def _has_invalid_shape(grid: object) -> bool:
    """Return True when grid is not a 4×4 list-of-lists."""
    if grid is None:
        return True
    if not isinstance(grid, list):
        return True
    if len(grid) != GRID_SIZE:
        return True
    for row in grid:
        if row is None or not isinstance(row, list):
            return True
        if len(row) != GRID_SIZE:
            return True
    return False
