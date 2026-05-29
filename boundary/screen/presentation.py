"""Presentation helpers for screen-layer judge output."""

from __future__ import annotations

from entity.models.judge_result import JudgeResult


def format_judge_result(result: JudgeResult) -> str:
    """Format a judge result for on-screen or CLI display."""
    return f"[{result.code}] {result.message}"
