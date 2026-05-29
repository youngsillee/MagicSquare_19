"""SSOT partial grids for Solve track tests (G0~G3 from Report/02 and golden master)."""

from __future__ import annotations

# G1 — reverse_success fixture (Step B placement for this grid)
GRID_G1: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 0, 11, 8],
    [9, 6, 0, 12],
    [4, 15, 14, 1],
]

# G2 — Step B success (normal_success fixture)
GRID_G2: list[list[int]] = [
    [16, 2, 3, 13],
    [5, 11, 10, 8],
    [9, 7, 0, 12],
    [4, 14, 15, 0],
]

# G3 — no valid completion
GRID_G3: list[list[int]] = [
    [1, 2, 3, 0],
    [5, 6, 0, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 16],
]

# G0 — complete grid, zero empty cells
GRID_G0: list[list[int]] = [
    [16, 3, 2, 13],
    [5, 10, 11, 8],
    [9, 6, 7, 12],
    [4, 15, 14, 1],
]

EXPECTED_G1_SOLUTION = [2, 2, 10, 3, 3, 7]
EXPECTED_G2_SOLUTION = [3, 3, 6, 4, 4, 1]
