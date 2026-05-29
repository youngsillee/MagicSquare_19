"""Magic Square 4×4 PyQt screen entry point.

Run from project root after installing GUI dependencies:

    pip install -r requirements-gui.txt
    python -m boundary.screen.app

Optional AC-FR-01-01 grid=None verification (CLI):

    python -m boundary.screen.app --verify
"""

from __future__ import annotations

import sys

from boundary.cli.judge_handler import JudgeHandler
from entity.models.judge_result import JudgeResult
from entity.rules.grid_shape_validator import INVALID_SIZE_CODE

_HANDLER = JudgeHandler()


def create_handler() -> JudgeHandler:
    """Composition root — default judge handler for screen and CLI."""
    return _HANDLER


def run_verify_none_grid(handler: JudgeHandler | None = None) -> JudgeResult:
    """Run AC-FR-01-01 anchor check (grid=None) and print the result envelope."""
    judge = handler if handler is not None else create_handler()
    result = judge.handle(None)
    print(f"code={result.code}")
    print(f"message={result.message}")
    return result


def main() -> int:
    """Launch the main window or ``--verify`` CLI check.

    Returns:
        Process exit code (0 on success).
    """
    if "--verify" in sys.argv:
        result = run_verify_none_grid()
        return 0 if result.code == INVALID_SIZE_CODE else 1

    from PyQt6.QtWidgets import QApplication

    from boundary.screen.main_window import MagicSquareMainWindow

    app = QApplication(sys.argv)
    window = MagicSquareMainWindow(create_handler())
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
