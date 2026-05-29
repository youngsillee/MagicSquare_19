"""Judge result DTO for magic square evaluation."""

from __future__ import annotations

from pydantic import BaseModel, Field


class JudgeResult(BaseModel):
    """Structured outcome of a magic square judge operation.

    Attributes:
        code: Machine-readable result code (e.g. INVALID_SIZE).
        message: Human-readable explanation aligned with PRD §8.1.
    """

    code: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)
