# Baseline Analysis: Head-Tracking Studies Comparison

## Study Summary Table

| # | Study | Year | Platform | Tracking Method | Click Method | Participants | Key Metrics |
|---|-------|------|----------|----------------|--------------|-------------|-------------|
| 1 | Camera Mouse (Betke et al.) | 2002 | Desktop (2-PC) | Template correlation on visible-light video | Dwell-time (0.5s, 30px radius) + exponential smoothing | 20 able-bodied + 12 disabled | Camera Mouse 1.6x slower than standard mouse; 9/12 disabled users succeeded |
| 2 | Gaze Adaptation (Tong & Chan) | 2024 | Desktop + Tobii 5 | Eye-tracker + head pose monitor (HMDSA algorithm) | Gaze-based icon selection | 2 participants with involuntary head movement | Selection time: 4.79s (adapted) vs 7.72s (control); Accuracy: 92% vs 51% |
| 3 | IOM Head-Tracking (Rodrigues et al.) | 2017 | Desktop | Gyroscope + accelerometer glasses (~$40) | Dwell-time (750ms) | 10 able-bodied | Speed: 359-509 px/s; Accuracy: 100% (0% error rate); comparable to HMAGIC |
| 4 | Fitts Test Head-Trackers (Guness et al.) | 2012 | Desktop | Vision-based (HeadTracker, CameraMouse, SmartNav) | Dwell-time (500ms) | Not specified (single user) | SmartNav best at high ID; CameraMouse best at low ID; HeadTracker slowest |
| 5 | 3M-HCI Multimodal (Quan et al.) | 2025 | Desktop (Windows) | MediaPipe Face Mesh (478 landmarks) + 1€ filter + voice + eye gaze | Facial expressions (13 gestures) + voice commands | 8 able-bodied | Jitter: <10px (vs 80-120px others); Latency: 2-3s per target; Accuracy best among compared systems |
| 6 | Multi-Monitor Head Tracking (Ashdown et al.) | 2005 | Desktop (3 monitors) | Stereo camera particle filter (6-DOF head pose) | Mouse + head-based monitor switching | 8 able-bodied | Mouse movement reduced 32%; task time increased 24%; 1mm position / 1° orientation accuracy |
| 7 | Faceboard (Schwarz) | 2025 | Mobile (Android) | ML Kit for Firebase (face landmarks + blink detection) | Blink-triggered swipe gestures | 16 able-bodied (2 with minor impairments) | 5.98 WPM; KSPC: 1.67; CER: 18.9%; SUS: 59.1; NASA-TLX: 58 |
| 8 | Mobile HBP (Cicek et al.) | 2020 | Mobile (Android) | ML Kit for Firebase (nose tip tracking) | Dwell + blink + smile | 42 able-bodied + 15 with motor impairments | TP: 0.90 bps (able-bodied), 0.61 bps (impaired); calibration-free; outperforms EVA Facial Mouse |

---

## Detailed Technical Comparison

### Tracking Technology

| Study | Face Detection | Landmarks | Pose Estimation | Filtering/Smoothing |
|-------|---------------|-----------|-----------------|---------------------|
| 1 - Camera Mouse | Template correlation (normalized) | Single feature (nose tip) | None (2D tracking) | Exponential smoothing filter |
| 2 - HMDSA | Eye tracker (Tobii 5) | Eye + head position | 3D head position + y-axis Euler angle | Moving average + speed controller |
| 3 - IOM | Gyroscope + accelerometer | N/A (sensor-based) | Inclination from sensors | None mentioned |
| 4 - Fitts Eval | Various (per device) | Varies by device | SmartNav: IR; CameraMouse: template; HeadTracker: face/skin/motion | Not specified |
| 5 - 3M-HCI | **MediaPipe Face Mesh** | **478 landmarks** | Medial canthi midpoint tracking | **1€ adaptive filter + sigmoid acceleration** |
| 6 - Multi-Monitor | Stereo cameras + OKAO face detector | 10 feature points | **Particle filter (6-DOF)** | Adaptive diffusion in particle filter |
| 7 - Faceboard | ML Kit for Firebase | Eyebrows, nose, lower lip | 2D position from face landmarks | Edge-clipping calibration |
| 8 - Mobile HBP | ML Kit for Firebase | Nose tip only | 2D relative change mapping | **Mean filter (window=3) + motion threshold** |

### Click/Selection Mechanisms

| Study | Primary Click | Secondary Click | Configurable |
|-------|-------------|-----------------|-------------|
| 1 - Camera Mouse | Dwell-time (0.5s, 30px radius) | Physical switch | Radius + timing adjustable |
| 2 - HMDSA | Gaze-based selection | N/A | Window timeframe, speed threshold |
| 3 - IOM | Dwell-time (750ms) | N/A | Dwell time adjustable |
| 4 - Fitts Eval | Dwell-time (500ms) | N/A | Not specified |
| 5 - 3M-HCI | Facial expressions (13 options) | Voice commands | User-defined thresholds + priority |
| 6 - Multi-Monitor | Standard mouse click | Head-based monitor switch | Hysteresis threshold |
| 7 - Faceboard | Blink (long blink) | N/A | Not configurable |
| 8 - Mobile HBP | Dwell (0.8s, 20px) | Blink + Smile | Multiple selection methods |

### Evaluation Metrics Reported

| Study | Speed/Time | Accuracy | Error Rate | Throughput (Fitts) | Usability Score | Fatigue |
|-------|-----------|----------|------------|-------------------|----------------|---------|
| 1 - Camera Mouse | 1.6x slower than mouse | Qualitative | Not quantified | N/A | N/A | N/A |
| 2 - HMDSA | 4.79s selection time | 92% with adaptation | N/A | N/A | N/A | N/A |
| 3 - IOM | 359-509 px/s | 100% | 0% | N/A | N/A | N/A |
| 4 - Fitts Eval | MT: 0.98-12.4s | Via Fitts effective width | N/A | Computed per ID | N/A | N/A |
| 5 - 3M-HCI | 2-3s per target | Best among 3 systems | N/A | N/A | 8.88/10 responsiveness | 7.25/10 |
| 6 - Multi-Monitor | 24% slower with tracking | 1mm / 1° | N/A | N/A | 7/8 preferred tracker | N/A |
| 7 - Faceboard | 5.98 WPM | N/A | CER: 18.9% | N/A | SUS: 59.1 | TLX: 58 |
| 8 - Mobile HBP | MT: 1.89-4.57s | Via Fitts effective width | N/A | 0.90 bps (able) / 0.61 bps (impaired) | Minor dry eyes | N/A |

---

## Baseline Study Selection

### Recommended Baseline: **Study 5 — 3M-HCI (Quan et al., 2025)**

**Rationale:**

1. **Most relevant technology stack**: Uses MediaPipe Face Mesh (478 landmarks), which is the same technology specified in our project requirements. This makes it the most directly comparable and replicable baseline.

2. **Comprehensive metrics**: Reports jitter deviation (<10px), movement latency (2-3s), accuracy (path deviation), and user survey scores — providing multiple dimensions to compare against.

3. **State-of-the-art comparison**: Already benchmarked against CameraMouseAI and Google Project GameFace, giving us a three-way reference point.

4. **Advanced filtering**: Uses the 1€ adaptive filter, which is a well-documented, proven approach we can replicate and improve upon.

5. **Desktop Windows platform**: Same target platform as our project.

6. **Recent publication (2025)**: Represents the current state-of-the-art in camera-based hands-free interaction.

### Secondary Reference: **Study 8 — Mobile HBP (Cicek et al., 2020)**

**Why secondary**: Provides the most rigorous Fitts' Law evaluation with motor-impaired users (n=15), giving us the best real-world performance targets for our target user group. Key insight: throughput of 0.61 bps for impaired users establishes a lower-bound expectation.

### Additional References for Specific Components:
- **Study 1 (Camera Mouse)**: Foundation reference for dwell-time click design
- **Study 2 (HMDSA)**: Reference for head movement adaptation algorithms
- **Study 4 (Fitts Eval)**: Methodology reference for evaluation using modified Fitts' Test

---

## Proposed Improvements Over Baseline (Study 5)

| # | Improvement | Baseline (3M-HCI) | Our Approach | Expected Gain |
|---|------------|-------------------|-------------|---------------|
| 1 | **Pose estimation** | 2D medial canthi midpoint | cv2.solvePnP with 6 stable 3D landmarks (nose tip, chin, eye corners, mouth corners) yielding yaw/pitch/roll | More robust to depth changes; enables roll-based gestures |
| 2 | **Smoothing pipeline** | 1€ filter on displacement magnitude | Kalman Filter (primary) + EMA fallback + configurable deadzone | Better noise rejection with predictive capability; ~30% jitter reduction expected |
| 3 | **Calibration** | None (calibration-free) | 9-point calibration routine with per-user adaptive sensitivity mapping | Personalized angle-to-pixel mapping; improved accuracy at screen edges |
| 4 | **Click mechanism** | 13 facial expressions + voice | Dwell-time (configurable 0.5-2.0s) + blink detection (EAR-based) | Simpler, less fatiguing for quadriplegic users; fewer false positives |
| 5 | **Screen mapping** | Linear gain with sigmoid acceleration | Adaptive sensitivity zones (center vs edges) with configurable gain curves | Better precision in center; full reach at edges without extreme head rotation |
| 6 | **Gesture recognition** | Not implemented | Head gestures mapped to OS actions (nod=confirm, shake=cancel, tilt=scroll) | Enables richer interaction beyond pointing |
| 7 | **Virtual keyboard** | Not included | Full AR/EN virtual keyboard with dwell-select | Complete text input solution for quadriplegic users |
| 8 | **Emergency panel** | Not included | Large icon-based emergency communication panel with audio | Critical safety feature for medical/care context |
| 9 | **Evaluation rigor** | 8 participants, custom tasks | RMSE, accuracy %, latency ms, task completion time, Fitts throughput, fatigue index | Publication-ready metrics matching thesis requirements |

---

## Metrics We Will Replicate and Report

From the baseline and reference studies, our evaluation module will compute:

1. **RMSE** (Root Mean Square Error): Deviation of cursor from target path (pixels)
2. **Pointing Accuracy (%)**: Successful target selections / total attempts
3. **Movement Latency (ms)**: Time from target appearance to cursor reaching target
4. **Task Completion Time (s)**: Total time for a pointing-and-clicking task sequence
5. **Throughput (bits/s)**: Fitts' Law throughput using effective ID
6. **Jitter Deviation (px)**: Cursor movement when user is stationary
7. **Dwell Click Accuracy (%)**: Correct dwell activations / total dwell attempts
8. **Fatigue Index**: Performance degradation over extended use sessions
9. **Comparison vs Baseline**: Side-by-side with 3M-HCI reported values

---

## Conclusion

Study 5 (3M-HCI) is the optimal baseline because it shares our core technology (MediaPipe), targets the same platform (Windows desktop), and provides the most comprehensive recent benchmarks. Our system will replicate their tracking pipeline as a starting point, then apply improvements in pose estimation (solvePnP), filtering (Kalman), calibration (9-point), and interaction design (dwell+blink click, virtual keyboard, emergency panel) to create a production-grade assistive system specifically optimized for quadriplegic users.

**Awaiting approval before proceeding to Phase 1 (project scaffolding).**
