"""Map head gestures (nod, shake, tilt) to system actions."""

from typing import Dict, Callable, Optional, List
from enum import Enum


class Gesture(Enum):
    """Recognised head gestures."""
    NOD = "nod"
    SHAKE = "shake"
    TILT_LEFT = "tilt_left"
    TILT_RIGHT = "tilt_right"
    NONE = "none"


class GestureMapper:
    """Detects head gestures from pose angles and maps them to actions.

    Monitors the history of yaw, pitch, and roll to recognise
    intentional gestures such as nodding, shaking, and tilting.

    Attributes:
        nod_threshold: Minimum pitch change to detect a nod (degrees).
        shake_threshold: Minimum yaw change to detect a shake (degrees).
        tilt_threshold: Minimum roll change to detect a tilt (degrees).
        cooldown_ms: Minimum time between gesture triggers (milliseconds).
    """

    def __init__(
        self,
        nod_threshold: float = 15.0,
        shake_threshold: float = 20.0,
        tilt_threshold: float = 15.0,
        cooldown_ms: int = 1000,
    ) -> None:
        """Initialize the gesture mapper.

        Args:
            nod_threshold: Pitch threshold for nod detection.
            shake_threshold: Yaw threshold for shake detection.
            tilt_threshold: Roll threshold for tilt detection.
            cooldown_ms: Cooldown period between gestures.
        """
        self.nod_threshold = nod_threshold
        self.shake_threshold = shake_threshold
        self.tilt_threshold = tilt_threshold
        self.cooldown_ms = cooldown_ms
        self._action_map: Dict[Gesture, Optional[Callable[[], None]]] = {g: None for g in Gesture}
        self._history: List[Dict[str, float]] = []
        self._last_gesture_time: float = 0.0
        self._history_max: int = 15

    def register_action(
        self, gesture: Gesture, action: Callable[[], None]
    ) -> None:
        """Bind a callable action to a gesture.

        Args:
            gesture: The gesture to bind.
            action: Callable to invoke when the gesture is detected.
        """
        self._action_map[gesture] = action

    def update(
        self,
        yaw: float,
        pitch: float,
        roll: float,
        timestamp_ms: float,
    ) -> Gesture:
        """Feed new head-pose data and return the detected gesture, if any.

        Args:
            yaw: Current head yaw in degrees.
            pitch: Current head pitch in degrees.
            roll: Current head roll in degrees.
            timestamp_ms: Current timestamp in milliseconds.

        Returns:
            The detected Gesture, or Gesture.NONE.
        """
        self._history.append({"yaw": yaw, "pitch": pitch, "roll": roll, "time": timestamp_ms})
        self._history = self._history[-self._history_max:]

        if timestamp_ms - self._last_gesture_time < self.cooldown_ms:
            return Gesture.NONE

        if self._detect_shake():
            detected = Gesture.SHAKE
        elif self._detect_nod():
            detected = Gesture.NOD
        else:
            tilt_result = self._detect_tilt()
            if tilt_result is not None:
                detected = tilt_result
            else:
                return Gesture.NONE

        self._last_gesture_time = timestamp_ms
        self._history = []
        action = self._action_map.get(detected)
        if action is not None:
            action()
        return detected

    def _detect_nod(self) -> bool:
        """Check the recent pitch history for a nod pattern.

        Returns:
            True if a nod is detected.
        """
        if len(self._history) < 5:
            return False
        pitches: List[float] = [h["pitch"] for h in self._history]
        min_pitch = min(pitches)
        max_pitch = max(pitches)
        if (max_pitch - min_pitch) < self.nod_threshold:
            return False
        min_idx = pitches.index(min_pitch)
        max_idx = pitches.index(max_pitch)
        extremum_idx = min_idx if abs(min_pitch) > abs(max_pitch) else max_idx
        if extremum_idx == 0 or extremum_idx == len(pitches) - 1:
            return False
        return True

    def _detect_shake(self) -> bool:
        """Check the recent yaw history for a shake pattern.

        Returns:
            True if a shake is detected.
        """
        if len(self._history) < 5:
            return False
        yaws: List[float] = [h["yaw"] for h in self._history]
        min_yaw = min(yaws)
        max_yaw = max(yaws)
        if (max_yaw - min_yaw) < self.shake_threshold:
            return False
        min_idx = yaws.index(min_yaw)
        max_idx = yaws.index(max_yaw)
        extremum_idx = min_idx if abs(min_yaw) > abs(max_yaw) else max_idx
        if extremum_idx == 0 or extremum_idx == len(yaws) - 1:
            return False
        return True

    def _detect_tilt(self) -> Optional[Gesture]:
        """Check the recent roll history for a tilt.

        Returns:
            Gesture.TILT_LEFT, Gesture.TILT_RIGHT, or None.
        """
        recent = self._history[-5:]
        if not recent:
            return None
        avg_roll: float = sum(h["roll"] for h in recent) / len(recent)
        if avg_roll > self.tilt_threshold:
            return Gesture.TILT_RIGHT
        if avg_roll < -self.tilt_threshold:
            return Gesture.TILT_LEFT
        return None

    def reset(self) -> None:
        """Clear gesture history and reset state."""
        self._history = []
        self._last_gesture_time = 0.0


if __name__ == "__main__":
    print("GestureMapper module -- standalone test")
    mapper = GestureMapper(nod_threshold=15.0, shake_threshold=20.0, tilt_threshold=15.0, cooldown_ms=500)

    detected: List[str] = []
    def on_nod() -> None: detected.append("NOD")
    def on_shake() -> None: detected.append("SHAKE")
    def on_tilt_l() -> None: detected.append("TILT_LEFT")
    def on_tilt_r() -> None: detected.append("TILT_RIGHT")

    mapper.register_action(Gesture.NOD, on_nod)
    mapper.register_action(Gesture.SHAKE, on_shake)
    mapper.register_action(Gesture.TILT_LEFT, on_tilt_l)
    mapper.register_action(Gesture.TILT_RIGHT, on_tilt_r)

    print("\n--- Simulating Nod ---")
    t = 0
    for pitch in [0, -5, -10, -18, -10, -5, 0, 5, 10]:
        result = mapper.update(0.0, pitch, 0.0, t)
        if result != Gesture.NONE:
            print(f"  Detected: {result.value} at t={t}")
        t += 33

    t += 600

    print("\n--- Simulating Shake ---")
    for yaw in [0, 10, 22, 15, 0, -10, -22, -15, 0]:
        result = mapper.update(yaw, 0.0, 0.0, t)
        if result != Gesture.NONE:
            print(f"  Detected: {result.value} at t={t}")
        t += 33

    t += 600

    print("\n--- Simulating Tilt Right ---")
    for roll in [0, 5, 10, 18, 20, 22]:
        result = mapper.update(0.0, 0.0, roll, t)
        if result != Gesture.NONE:
            print(f"  Detected: {result.value} at t={t}")
        t += 33

    print(f"\nAll detected gestures: {detected}")
    print("GestureMapper test completed.")
