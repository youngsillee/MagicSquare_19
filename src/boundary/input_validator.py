"""Boundary input validation for MagicSquare grid contract."""

from __future__ import annotations

from boundary.schemas import ErrorDetail, FailureResponse

_INVALID_SIZE_CODE = "INVALID_SIZE"
_INVALID_SIZE_MESSAGE = "Grid must be 4x4."


class InputValidator:
    """Validates incoming grid input at the Boundary layer."""

    def validate(self, grid: list[list[int]] | None) -> FailureResponse:
        """Validate grid input; AC-FR-01-01 handles ``grid is None`` only."""
        if grid is None:
            return FailureResponse(
                type="ERROR",
                error=ErrorDetail(
                    code=_INVALID_SIZE_CODE,
                    message=_INVALID_SIZE_MESSAGE,
                ),
            )
        raise NotImplementedError
