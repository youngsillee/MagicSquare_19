"""Judge use case — orchestrates shape check then domain resolve."""

from __future__ import annotations

from entity.models.judge_result import JudgeResult
from entity.rules.grid_shape_validator import validate_grid_shape
from entity.rules.magic_square_judge import MagicSquareJudge


class JudgeUseCase:
    """Coordinate grid shape validation and domain judgment."""

    def execute(self, grid: object) -> JudgeResult:
        """Run judge flow for the given grid input.

        Invalid shape returns INVALID_SIZE without invoking domain resolve().

        Args:
            grid: Raw grid input from boundary layer.

        Returns:
            JudgeResult describing acceptance or structured failure.
        """
        shape_error = validate_grid_shape(grid)
        if shape_error is not None:
            return shape_error
        return MagicSquareJudge.resolve(grid)  # type: ignore[arg-type]
