from __future__ import annotations

import unittest

from camera.camera_config import CameraConfig
from main import parse_camera_source
from ui.overlay import FpsCounter


class CameraConfigTests(unittest.TestCase):
    def test_rejects_non_positive_dimensions(self) -> None:
        with self.assertRaises(ValueError):
            CameraConfig(width=0)

    def test_rejects_empty_string_source(self) -> None:
        with self.assertRaises(ValueError):
            CameraConfig(source="  ")


class CameraArgumentTests(unittest.TestCase):
    def test_parses_camera_index(self) -> None:
        self.assertEqual(parse_camera_source("2"), 2)

    def test_preserves_stream_url(self) -> None:
        url = "http://192.168.0.10:8080/video"
        self.assertEqual(parse_camera_source(url), url)


class FpsCounterTests(unittest.TestCase):
    def test_rejects_too_small_sample(self) -> None:
        with self.assertRaises(ValueError):
            FpsCounter(sample_count=1)


if __name__ == "__main__":
    unittest.main()

