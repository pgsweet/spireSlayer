from dataclasses import dataclass
from typing import Any

import mss
import numpy as np
import pygetwindow
from PIL import Image


class WindowNotFoundError(RuntimeError):
    pass


@dataclass
class ScreenCapture:
    monitor_index: int = 1
    window_title: str | None = None

    def get_image(self) -> Image.Image:
        """Capture the selected monitor or window as a Pillow image."""
        with mss.mss() as screen_capture:
            region = self._get_capture_region(screen_capture)
            screenshot = screen_capture.grab(region)

        return Image.frombytes("RGB", screenshot.size, screenshot.rgb)

    def get_frame(self) -> np.ndarray:
        """Capture the selected monitor or window as an OpenCV-style BGR frame."""
        with mss.mss() as screen_capture:
            region = self._get_capture_region(screen_capture)
            screenshot = screen_capture.grab(region)

        frame = np.asarray(screenshot)
        return frame[:, :, :3].copy()

    def _get_capture_region(self, screen_capture: mss.mss) -> dict[str, Any]:
        if self.window_title:
            return self._get_window_region()

        return self._get_monitor(screen_capture)

    def _get_monitor(self, screen_capture: mss.mss) -> dict[str, Any]:
        monitors = screen_capture.monitors

        if self.monitor_index < 0 or self.monitor_index >= len(monitors):
            raise ValueError(
                f"Monitor index {self.monitor_index} is not available. "
                f"Available indexes: 0-{len(monitors) - 1}."
            )

        return monitors[self.monitor_index]

    def _get_window_region(self) -> dict[str, int]:
        windows = pygetwindow.getWindowsWithTitle(self.window_title)
        visible_windows = [
            window
            for window in windows
            if not window.isMinimized and window.width > 0 and window.height > 0
        ]

        if not visible_windows:
            raise WindowNotFoundError(
                f'Could not find an open window named "{self.window_title}".'
            )

        window = visible_windows[0]
        return {
            "left": window.left,
            "top": window.top,
            "width": window.width,
            "height": window.height,
        }
