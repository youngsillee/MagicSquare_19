"""Pydantic schemas for Boundary failure responses."""

from __future__ import annotations

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    """Error payload nested inside a failure response envelope."""

    code: str
    message: str


class FailureResponse(BaseModel):
    """Standard failure envelope returned by Boundary on contract violation."""

    type: str
    error: ErrorDetail
