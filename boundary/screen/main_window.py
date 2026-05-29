"""PyQt main window for Magic Square 4×4 judge."""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from boundary.cli.judge_handler import JudgeHandler
from boundary.screen.presentation import format_judge_result
from entity.models.judge_result import JudgeResult
from entity.rules.grid_shape_validator import GRID_SIZE

_SPIN_MIN = 1
_SPIN_MAX = 16

DEFAULT_GRID: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

_NOT_IMPLEMENTED_MESSAGE = (
    "값·선 판정은 아직 구현되지 않았습니다 (AC-FR-01-02 이후)."
)


class MagicSquareMainWindow(QMainWindow):
    """4×4 spinbox grid with judge action wired to ``JudgeHandler``."""

    def __init__(self, handler: JudgeHandler) -> None:
        """Initialize the window with an injected judge handler.

        Args:
            handler: Adapts grid input to the judge use case.
        """
        super().__init__()
        self._handler = handler
        self._spinboxes: list[list[QSpinBox]] = []
        self._result_label = QLabel("")
        self._init_ui()

    def _init_ui(self) -> None:
        """Build grid spinboxes, judge button, and result label."""
        self.setWindowTitle("Magic Square 4×4 — 판정")
        self.setMinimumWidth(320)

        central = QWidget()
        self.setCentralWidget(central)
        root_layout = QVBoxLayout(central)

        grid_layout = QGridLayout()
        for row in range(GRID_SIZE):
            row_boxes: list[QSpinBox] = []
            for col in range(GRID_SIZE):
                spinbox = QSpinBox()
                spinbox.setRange(_SPIN_MIN, _SPIN_MAX)
                spinbox.setValue(DEFAULT_GRID[row][col])
                grid_layout.addWidget(spinbox, row, col)
                row_boxes.append(spinbox)
            self._spinboxes.append(row_boxes)

        judge_button = QPushButton("판정")
        judge_button.clicked.connect(self._on_judge)

        root_layout.addLayout(grid_layout)
        root_layout.addWidget(judge_button)
        root_layout.addWidget(self._result_label)

    def _read_grid(self) -> list[list[int]]:
        """Read current spinbox values as a 4×4 integer matrix."""
        return [
            [spinbox.value() for spinbox in row_boxes]
            for row_boxes in self._spinboxes
        ]

    def _on_judge(self) -> None:
        """Invoke ``JudgeHandler.handle`` and render the structured result."""
        grid = self._read_grid()
        try:
            result = self._handler.handle(grid)
        except NotImplementedError:
            self._result_label.setText(_NOT_IMPLEMENTED_MESSAGE)
            return

        if isinstance(result, JudgeResult):
            self._result_label.setText(format_judge_result(result))
