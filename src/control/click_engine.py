"""Click engine supporting dwell-time and blink-based click mechanisms."""

import math
from typing import Tuple, Optional, Callable
from enum import Enum


class ClickMode(Enum):
    DWELL = "dwell"
    BLINK = "blink"
    BOTH = "both"


class DwellClickDetector:

    def __init__(
        self,
        dwell_time_ms: int = 1000,
        dwell_radius: float = 30.0,
    ) -> None:
        self.dwell_time_ms = dwell_time_ms
        self.dwell_radius = dwell_radius
        self._dwell_start_time: Optional[float] = None
        self._dwell_center: Optional[Tuple[float, float]] = None
        self._progress: float = 0.0

    def update(
        self, position: Tuple[float, float], timestamp_ms: float
    ) -> bool:
        if self._dwell_center is None:
            self._dwell_center = position
            self._dwell_start_time = timestamp_ms
            self._progress = 0.0
            return False

        dx = position[0] - self._dwell_center[0]
        dy = position[1] - self._dwell_center[1]
        distance = math.sqrt(dx * dx + dy * dy)

        if distance > self.dwell_radius:
            self._dwell_center = position
            self._dwell_start_time = timestamp_ms
            self._progress = 0.0
            return False

        elapsed = timestamp_ms - self._dwell_start_time
        self._progress = min(elapsed / self.dwell_time_ms, 1.0)

        if elapsed >= self.dwell_time_ms:
            self.reset()
            return True

        return False

    def get_progress(self) -> float:
        return self._progress

    def reset(self) -> None:
        self._dwell_start_time = None
        self._dwell_center = None
        self._progress = 0.0


class BlinkClickDetector:

    def __init__(
        self,
        ear_threshold: float = 0.21,
        consecutive_frames: int = 3,
    ) -> None:
        self.ear_threshold = ear_threshold
        self.consecutive_frames = consecutive_frames
        self._frame_counter: int = 0
        self._blink_detected: bool = False

    def update(self, ear: float) -> bool:
        if ear < self.ear_threshold:
            self._frame_counter += 1
        else:
            if self._frame_counter >= self.consecutive_frames:
                self._frame_counter = 0
                return True
            self._frame_counter = 0
        return False

    def reset(self) -> None:
        self._frame_counter = 0


class ClickEngine:

    def __init__(
        self,
        mode: ClickMode = ClickMode.BOTH,
        dwell_time_ms: int = 1000,
        dwell_radius: float = 30.0,
        ear_threshold: float = 0.21,
        consecutive_frames: int = 3,
    ) -> None:
        self.mode = mode
        self.on_click: Optional[Callable[[], None]] = None
        self._dwell_detector: Optional[DwellClickDetector] = None
        self._blink_detector: Optional[BlinkClickDetector] = None

        if mode in (ClickMode.DWELL, ClickMode.BOTH):
            self._dwell_detector = DwellClickDetector(dwell_time_ms, dwell_radius)
        if mode in (ClickMode.BLINK, ClickMode.BOTH):
            self._blink_detector = BlinkClickDetector(ear_threshold, consecutive_frames)

    def update(
        self,
        position: Tuple[float, float],
        timestamp_ms: float,
        ear: Optional[float] = None,
    ) -> bool:
        clicked = False

        if self._dwell_detector is not None and self.mode in (ClickMode.DWELL, ClickMode.BOTH):
            if self._dwell_detector.update(position, timestamp_ms):
                clicked = True

        if self._blink_detector is not None and self.mode in (ClickMode.BLINK, ClickMode.BOTH) and ear is not None:
            if self._blink_detector.update(ear):
                clicked = True

        if clicked and self.on_click:
            self.on_click()

        return clicked

    def get_dwell_progress(self) -> float:
        if self._dwell_detector is not None:
            return self._dwell_detector.get_progress()
        return 0.0

    def set_mode(self, mode: ClickMode) -> None:
        self.mode = mode

    def reset(self) -> None:
        if self._dwell_detector is not None:
            self._dwell_detector.reset()
        if self._blink_detector is not None:
            self._blink_detector.reset()


if __name__ == "__main__":
    import time as _time
    print("ClickEngine module -- standalone test")

    print("\n--- Dwell Click Test ---")
    dwell = DwellClickDetector(dwell_time_ms=500, dwell_radius=20.0)
    base_time = 0.0
    for i in range(20):
        t = base_time + i * 50
        pos = (100.0 + (i % 3), 200.0 + (i % 2))
        result = dwell.update(pos, t)
        print(f"  t={t:.0f}ms pos={pos} progress={dwell.get_progress():.2f} click={result}")
        if result:
            print("  >>> DWELL CLICK DETECTED!")
            break

    print("\n--- Blink Click Test ---")
    blink = BlinkClickDetector(ear_threshold=0.21, consecutive_frames=3)
    ear_sequence = [0.30, 0.28, 0.15, 0.12, 0.10, 0.25, 0.30]
    for i, ear in enumerate(ear_sequence):
        result = blink.update(ear)
        print(f"  frame={i} ear={ear:.2f} click={result}")
        if result:
            print("  >>> BLINK CLICK DETECTED!")

    print("\n--- Unified ClickEngine Test ---")
    engine = ClickEngine(mode=ClickMode.BOTH, dwell_time_ms=300, dwell_radius=25.0)
    _click_count = [0]
    def on_click() -> None:
        _click_count[0] += 1
    engine.on_click = on_click

    for i in range(15):
        t = i * 50
        result = engine.update((100.0, 200.0), t, ear=0.30)
        if result:
            print(f"  Click at t={t}ms!")
    print(f"  Total clicks: {_click_count[0]}")
    print("\nClickEngine test completed.")
