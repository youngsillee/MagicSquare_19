"""Domain judge for magic square resolution (post shape-validation)."""

from __future__ import annotations

from entity.models.judge_result import JudgeResult


class MagicSquareJudge:
    """Resolve whether a 4×4 grid satisfies magic square rules."""

    @classmethod
    def resolve(cls, grid: list[list[int]]) -> JudgeResult:
        """Evaluate a shape-valid 4×4 grid.

        Args:
            grid: A 4×4 grid that passed shape validation.

        Returns:
            JudgeResult for the grid (value/line checks — later ACs).

        Raises:
            NotImplementedError: Value and line validation are out of AC-FR-01-01 scope.
        """
        raise NotImplementedError(
            "Magic square value/line resolution is not implemented (AC-FR-01-02+)."
        )
