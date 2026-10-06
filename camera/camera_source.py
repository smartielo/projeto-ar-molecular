from __future__ import annotations

import cv2
from numpy.typing import NDArray

from camera.camera_config import CameraConfig


class CameraError(RuntimeError):
    """Raised when a video source cannot be opened or read."""


class CameraSource:
    """Owns an OpenCV video capture for a device index, URL, or video path."""

    def __init__(self, config: CameraConfig) -> None:
        self.config = config
        self._capture: cv2.VideoCapture | None = None

    @property
    def is_opened(self) -> bool:
        return self._capture is not None and self._capture.isOpened()

    @property
    def frame_width(self) -> int:
        return self._get_property(cv2.CAP_PROP_FRAME_WIDTH)

    @property
    def frame_height(self) -> int:
        return self._get_property(cv2.CAP_PROP_FRAME_HEIGHT)

    def open(self) -> None:
        if self.is_opened:
            return

        self.release()
        capture = cv2.VideoCapture(self.config.source)
        if not capture.isOpened():
            capture.release()
            raise CameraError(
                f"Nao foi possivel abrir a camera {self.config.source!r}. "
                "Verifique o indice/URL e feche outros aplicativos que usam a camera."
            )

        capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.width)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.height)
        self._capture = capture

    def read(self) -> NDArray:
        if not self.is_opened or self._capture is None:
            raise CameraError("A camera precisa ser aberta antes da leitura.")

        success, frame = self._capture.read()
        if not success or frame is None:
            raise CameraError(
                f"Falha ao ler um frame da camera {self.config.source!r}."
            )
        return frame

    def release(self) -> None:
        if self._capture is not None:
            self._capture.release()
            self._capture = None

    def _get_property(self, property_id: int) -> int:
        if not self.is_opened or self._capture is None:
            return 0
        return int(self._capture.get(property_id))

    def __enter__(self) -> "CameraSource":
        self.open()
        return self

    def __exit__(self, exc_type: object, exc_value: object, traceback: object) -> None:
        self.release()

