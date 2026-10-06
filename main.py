from __future__ import annotations

import argparse
import logging
import sys

import cv2

from camera.camera_config import CameraConfig
from camera.camera_source import CameraError, CameraSource
from config import settings
from ui.overlay import FpsCounter, draw_fps


def parse_camera_source(value: str) -> int | str:
    """Convert numeric CLI values to device indexes and preserve URLs/paths."""
    normalized = value.strip()
    try:
        return int(normalized)
    except ValueError:
        return normalized


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Visualiza uma camera para o projeto Molecular AR."
    )
    parser.add_argument(
        "--camera",
        type=parse_camera_source,
        default=settings.CAMERA_SOURCE,
        help="Indice da camera (ex.: 0 ou 1) ou URL de stream.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=settings.FRAME_WIDTH,
        help="Largura solicitada para os frames.",
    )
    parser.add_argument(
        "--height",
        type=int,
        default=settings.FRAME_HEIGHT,
        help="Altura solicitada para os frames.",
    )
    parser.add_argument(
        "--show-fps",
        action="store_true",
        default=settings.SHOW_FPS,
        help="Exibe a taxa de quadros no video.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=settings.DEBUG_MODE,
        help="Habilita logs de diagnostico.",
    )
    return parser


def run(config: CameraConfig, show_fps: bool) -> None:
    fps_counter = FpsCounter()

    with CameraSource(config) as camera:
        logging.info(
            "Camera aberta: source=%r, resolucao=%dx%d",
            config.source,
            camera.frame_width,
            camera.frame_height,
        )

        while True:
            frame = camera.read()

            if show_fps:
                draw_fps(frame, fps_counter.tick())

            cv2.imshow(settings.WINDOW_NAME, frame)
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), ord("Q"), 27):
                break


def main() -> int:
    args = build_parser().parse_args()
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    try:
        config = CameraConfig(
            source=args.camera,
            width=args.width,
            height=args.height,
        )
        run(config, show_fps=args.show_fps)
    except (CameraError, ValueError) as error:
        logging.error("%s", error)
        return 1
    except KeyboardInterrupt:
        logging.info("Encerrado pelo usuario.")
    finally:
        cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    sys.exit(main())

