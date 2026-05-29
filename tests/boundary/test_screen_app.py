"""Boundary tests for PyQt screen entry (CLI verify path, no display required)."""

from __future__ import annotations

import pytest

from boundary.screen.app import run_verify_none_grid
from boundary.screen.presentation import format_judge_result
from entity.models.judge_result import JudgeResult
from tests.conftest import EXPECTED_INVALID_SIZE_CODE, EXPECTED_INVALID_SIZE_MESSAGE

pytestmark = pytest.mark.ac_fr_01_01


class TestScreenVerifyNoneGrid:
    """AC-FR-01-01 anchor via ``python -m boundary.screen.app --verify``."""

    def test_verify_none_grid_returns_invalid_size(self, capsys) -> None:
        """grid=None through screen CLI helper returns INVALID_SIZE."""
        result = run_verify_none_grid()
        assert result.code == EXPECTED_INVALID_SIZE_CODE
        assert result.message == EXPECTED_INVALID_SIZE_MESSAGE

    def test_verify_none_grid_prints_envelope(self, capsys) -> None:
        """CLI helper prints code and message for manual inspection."""
        run_verify_none_grid()
        captured = capsys.readouterr().out
        assert f"code={EXPECTED_INVALID_SIZE_CODE}" in captured
        assert f"message={EXPECTED_INVALID_SIZE_MESSAGE}" in captured


class TestFormatJudgeResult:
    """Screen presentation helper for judge outcomes."""

    def test_format_judge_result_includes_code_and_message(self) -> None:
        """Formatted text exposes both machine code and human message."""
        result = JudgeResult(
            code=EXPECTED_INVALID_SIZE_CODE,
            message=EXPECTED_INVALID_SIZE_MESSAGE,
        )
        text = format_judge_result(result)
        assert EXPECTED_INVALID_SIZE_CODE in text
        assert EXPECTED_INVALID_SIZE_MESSAGE in text
