"""CLI handler for magic square judge requests."""

from __future__ import annotations

from control.services.judge_use_case import JudgeUseCase
from entity.models.judge_result import JudgeResult


class JudgeHandler:
    """Adapt external grid input to the judge use case."""

    def __init__(self, use_case: JudgeUseCase | None = None) -> None:
        """Initialize handler with optional use-case injection.

        Args:
            use_case: Judge use case; defaults to a new JudgeUseCase instance.
        """
        self._use_case = use_case if use_case is not None else JudgeUseCase()

    def handle(self, grid: object) -> JudgeResult:
        """Handle a judge request for the given grid.

        Args:
            grid: Grid input from CLI or API layer.

        Returns:
            JudgeResult from the use case.
        """
        return self._use_case.execute(grid)
