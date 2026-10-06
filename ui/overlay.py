from __future__ import annotations

from collections import deque
from time import perf_counter

import cv2
from numpy.typing import NDArray


class FpsCounter:
    """Calculates a stable rolling FPS value without retaining video frames."""

    def __init__(self, sample_count: int = 30) -> None:
        if sample_count < 2:
            raise ValueError("sample_count deve ser pelo menos 2.")
        self._timestamps: deque[float] = deque(maxlen=sample_count)

    def tick(self) -> float:
        self._timestamps.append(perf_counter())
        if len(self._timestamps) < 2:
            return 0.0

        elapsed = self._timestamps[-1] - self._timestamps[0]
        if elapsed <= 0:
            return 0.0
        return (len(self._timestamps) - 1) / elapsed


def draw_fps(frame: NDArray, fps: float) -> None:
    """Draw the current FPS in place, avoiding an additional frame copy."""
    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (16, 32),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (40, 220, 40),
        2,
        cv2.LINE_AA,
    )

