from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CameraConfig:
    """Settings used to open and configure one video source."""

    source: int | str = 0
    width: int = 1280
    height: int = 720

    def __post_init__(self) -> None:
        if isinstance(self.source, str) and not self.source.strip():
            raise ValueError("A fonte da camera nao pode ser vazia.")
        if self.width <= 0 or self.height <= 0:
            raise ValueError("A largura e a altura da camera devem ser positivas.")

