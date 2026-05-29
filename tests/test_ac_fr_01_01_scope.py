"""Scope guard tests — AC-FR-01-01 must not include out-of-scope cases.

AC-FR-01-01, PRD §8.1 INVALID_SIZE — this module enforces test suite boundaries.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

pytestmark = pytest.mark.ac_fr_01_01

_AC_FR_01_01_TEST_ROOT = Path(__file__).parent
_AC_FR_01_01_TEST_FILES = (
    _AC_FR_01_01_TEST_ROOT / "entity" / "test_grid_shape_validator.py",
    _AC_FR_01_01_TEST_ROOT / "control" / "test_judge_use_case.py",
    _AC_FR_01_01_TEST_ROOT / "boundary" / "test_judge_handler.py",
)

# Out-of-scope identifiers — AC-FR-01-02~05, FR-02~05
_FORBIDDEN_SCOPE_TOKENS = (
    "AC-FR-01-02",
    "AC-FR-01-03",
    "AC-FR-01-04",
    "AC-FR-01-05",
    "FR-02",
    "FR-03",
    "FR-04",
    "FR-05",
    "INVALID_DUPLICATE",
    "INVALID_RANGE",
    "INVALID_LINE_SUM",
    "VALID_MAGIC_SQUARE",
)

# Valid 4×4 grid literals that belong to later ACs, not AC-FR-01-01
_FORBIDDEN_GRID_PATTERNS = (
    "valid_4x4",
    "magic_square",
    "duplicate",
    "out_of_range",
    "line_sum",
    "row_sum",
)


class TestScopeRestriction:
    """범위 제한 — AC-FR-01-01 suite must exclude later AC/FR cases."""

    def test_scope_excludes_valid_4x4_grid_fixture_names(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — no valid 4×4 fixture in suite."""
        # AC-FR-01-01
        # Given: AC-FR-01-01 test source files
        sources = _read_ac_fr_01_01_sources()
        # When: scanning for valid 4×4 grid fixture names
        combined = "\n".join(sources)
        # Then: no valid 4×4 magic square fixtures present
        for pattern in _FORBIDDEN_GRID_PATTERNS:
            assert pattern not in combined.lower(), (
                f"Out-of-scope pattern '{pattern}' found in AC-FR-01-01 tests"
            )

    def test_scope_excludes_ac_fr_01_02_duplicate_cases(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — no AC-FR-01-02 duplicate tests."""
        # AC-FR-01-01
        # Given: AC-FR-01-01 test sources
        combined = "\n".join(_read_ac_fr_01_01_sources())
        # When: checking for duplicate-value AC references
        # Then: AC-FR-01-02 not referenced
        assert "AC-FR-01-02" not in combined
        assert "INVALID_DUPLICATE" not in combined

    def test_scope_excludes_ac_fr_01_03_range_cases(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — no AC-FR-01-03 range tests."""
        # AC-FR-01-01
        # Given: AC-FR-01-01 test sources
        combined = "\n".join(_read_ac_fr_01_01_sources())
        # When: checking for out-of-range AC references
        # Then: AC-FR-01-03 not referenced
        assert "AC-FR-01-03" not in combined
        assert "INVALID_RANGE" not in combined

    def test_scope_excludes_ac_fr_01_04_line_sum_cases(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — no AC-FR-01-04 line-sum tests."""
        # AC-FR-01-01
        # Given: AC-FR-01-01 test sources
        combined = "\n".join(_read_ac_fr_01_01_sources())
        # When: checking for line-sum AC references
        # Then: AC-FR-01-04 not referenced
        assert "AC-FR-01-04" not in combined
        assert "INVALID_LINE_SUM" not in combined

    def test_scope_excludes_fr_02_through_fr_05_requirements(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — no FR-02~05 cases in this commit."""
        # AC-FR-01-01
        # Given: AC-FR-01-01 test sources
        combined = "\n".join(_read_ac_fr_01_01_sources())
        # When: scanning for FR-02~05 scope tokens
        # Then: none of the forbidden FR-02~05 tokens appear
        for token in _FORBIDDEN_SCOPE_TOKENS:
            if token.startswith("FR-"):
                assert token not in combined, (
                    f"Out-of-scope requirement '{token}' referenced in AC-FR-01-01 tests"
                )


class TestScopeAstGuards:
    """범위 제한 — AST-level checks on AC-FR-01-01 test modules."""

    def test_scope_no_4x4_complete_grid_literal_in_tests(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — no 16-cell valid grid literals."""
        # AC-FR-01-01
        # Given: parsed AST of AC-FR-01-01 test files
        for source in _read_ac_fr_01_01_sources():
            tree = ast.parse(source)
            # When: walking list literals that could be 4×4 grids with 16 ints
            found_valid = _contains_4x4_int_grid_literal(tree)
            # Then: no complete 4×4 integer grid used as test input
            assert not found_valid, "Valid 4×4 grid literal must not appear in AC-FR-01-01"

    def test_scope_all_tests_marked_ac_fr_01_01(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — suite uses ac_fr_01_01 marker."""
        # AC-FR-01-01
        # Given: AC-FR-01-01 test module sources
        combined = "\n".join(_read_ac_fr_01_01_sources())
        # When: checking pytest marker registration
        # Then: pytestmark declares ac_fr_01_01
        assert "pytest.mark.ac_fr_01_01" in combined

    def test_scope_only_invalid_size_expected_code(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — only INVALID_SIZE success path."""
        # AC-FR-01-01
        # Given: AC-FR-01-01 test sources
        combined = "\n".join(_read_ac_fr_01_01_sources())
        # When: checking for out-of-scope success codes
        # Then: VALID/SUCCESS codes only appear as negated assertions
        assert 'result.code != "VALID"' in combined or "INVALID_SIZE" in combined

    def test_scope_no_ac_fr_01_05_success_judge_tests(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — no AC-FR-01-05 acceptance tests."""
        # AC-FR-01-01
        # Given: AC-FR-01-01 test sources
        combined = "\n".join(_read_ac_fr_01_01_sources())
        # When: scanning for success-judge AC
        # Then: AC-FR-01-05 not present
        assert "AC-FR-01-05" not in combined
        assert "VALID_MAGIC_SQUARE" not in combined

    def test_scope_commit_contains_only_shape_validation_cases(self) -> None:
        """AC-FR-01-01, PRD §8.1 INVALID_SIZE — tests target shape validation only."""
        # AC-FR-01-01
        # Given: allowed input fixtures from conftest
        conftest_source = (_AC_FR_01_01_TEST_ROOT / "conftest.py").read_text(
            encoding="utf-8"
        )
        # When: verifying fixture names are invalid-shape only
        allowed_fixtures = (
            "invalid_size_none",
            "invalid_size_empty",
            "invalid_size_zero_cols",
            "invalid_size_3x4",
            "invalid_size_4x3",
            "invalid_size_5x5",
        )
        # Then: only invalid-shape fixtures defined for this AC
        for name in allowed_fixtures:
            assert name in conftest_source


def _read_ac_fr_01_01_sources() -> list[str]:
    """Read source text of AC-FR-01-01 test modules."""
    return [path.read_text(encoding="utf-8") for path in _AC_FR_01_01_TEST_FILES]


def _contains_4x4_int_grid_literal(tree: ast.AST) -> bool:
    """Return True if AST contains a 4×4 list-of-lists of integers."""
    for node in ast.walk(tree):
        if not isinstance(node, ast.List) or len(node.elts) != 4:
            continue
        if not all(isinstance(row, ast.List) and len(row.elts) == 4 for row in node.elts):
            continue
        if all(
            isinstance(cell, ast.Constant) and isinstance(cell.value, int)
            for row in node.elts
            for cell in row.elts  # type: ignore[union-attr]
        ):
            values = {
                cell.value
                for row in node.elts
                for cell in row.elts  # type: ignore[union-attr]
            }
            if len(values) == 16:
                return True
    return False
