# Baseline Analysis: Head-Tracking Studies Comparison

## 1. Study Summary Table

| # | Study | Year | Platform | Tracking Method | Click Method | Participants | Target Users | Key Metrics |
|---|-------|------|----------|----------------|-------------|-------------|-------------|-------------|
| 1 | Camera Mouse (Betke et al.) | 2002 | Desktop (2-PC) | Template correlation on visible-light video (nose/lip/eye) | Dwell-time (0.5s, 30px radius) | 20 able-bodied + 12 with disabilities | Quadriplegic, CP, TBI | Spelling time factor: 2.1x slower than mouse; 9/12 disabled users succeeded |
| 2 | Gaze-Based Adaptation (Tong & Chan) | 2024 | Desktop (Tobii 5) | Eye tracker + head pose monitor (HMDSA algorithm) | Gaze dwell on icon | 2 with involuntary head movement | Dyskinetic CP, post-stroke | Selection time: 4.79s (adapted) vs 7.72s (control); Accuracy: 92% vs 51% |
| 3 | IOM Low-Cost Device (Rodrigues et al.) | 2017 | Desktop (wearable glasses) | Gyroscope + accelerometer on glasses frame (~$40) | Dwell-time (750ms) | 10 able-bodied | Motor disabled users | Speed: 359–509 px/s; Accuracy: 100% (0% error); Cost: ~$40 |
| 4 | Fitts Head-Tracker Evaluation (Guness et al.) | 2012 | Desktop (3 systems) | Vision-based (SmartNav IR, CameraMouse, custom HeadTracker) | Dwell-time (500ms) | Not specified (single user demo) | Neuro-disabilities (ALS, CP, MS, stroke) | MT range: 0.98s (mouse) to 12.4s (HeadTracker) at ID=4.99; Fitts throughput compared |
| 5 | 3M-HCI (Quan et al.) | 2025 | Desktop (webcam) | MediaPipe Face Mesh (478 landmarks) + 1€ adaptive filter + sigmoid acceleration | 13 facial expressions + voice + eye gaze | 8 able-bodied | Upper-limb impaired | Jitter: <10px (vs 120px CameraMouseAI); Latency: 2–3s per target; Accuracy: best among compared |
| 6 | Multi-Monitor Head Tracking (Ashdown et al.) | 2005 | Desktop (3 monitors) | Stereo cameras + particle filter (6-DOF head pose) | Mouse click (head selects monitor only) | 8 able-bodied | General multi-monitor users | Mouse distance reduced 32%; Task time increased 24%; 7/8 preferred head tracker |
| 7 | Mobile HBP (Cicek et al.) | 2020 | Android smartphone | ML Kit face detection, nose tip tracking, calibration-free | Dwell (0.8s) / Blink / Smile | 42 able-bodied + 16 with motor impairments | Motor impaired users | TP: 0.90 bps (able-bodied), 0.61 bps (impaired); 0.96 bps mild, 0.20 bps moderate |
| 8 | Faceboard (Schwarz) | 2025 | Android smartphone | ML Kit face detection, multi-landmark averaging, gesture-based swipe | Blink to start/stop gesture recording | 16 able-bodied | Motor impaired (text entry) | WPM: 5.98; KSPC: 1.67; SUS: 59.1/100; NASA-TLX: 58 (high workload) |

---

## 2. Technical Comparison

| Aspect | Study 1 | Study 2 | Study 3 | Study 4 | Study 5 | Study 6 | Study 7 | Study 8 |
|--------|---------|---------|---------|---------|---------|---------|---------|---------|
| **Face/Head Detection** | Template correlation | Tobii eye tracker + head pose | Gyro + accelerometer | Vision-based (multiple systems) | MediaPipe 478 landmarks | Stereo cameras + particle filter | ML Kit Firebase | ML Kit Firebase |
| **Pose Estimation** | None (2D tracking) | Euler angles (y-axis) | IMU sensors | N/A (commercial systems) | MediaPipe blendshapes | solvePnP-like (6-DOF) | Nose tip pixel coords | Multi-landmark averaging |
| **Smoothing/Filtering** | Exponential smoothing | Moving average + speed controller | None mentioned | N/A | 1€ adaptive filter | Particle filter | Mean filter (window=3) + motion threshold | Delta-based with scaling factor |
| **Calibration** | Click-to-select feature | Pre-calibrated eye tracker | Sensor calibration | Per-device | None (calibration-free) | 3-point look calibration | Calibration-free (edge clipping) | Calibration-free (edge clipping) |
| **Coordinate Mapping** | Gain factor scaling | Head pose → gaze adjustment | Direct sensor mapping | Direct mapping | Medial canthi midpoint + sigmoid acceleration | Head direction → monitor selection | Nose pixel delta → gain scaling | Landmark delta → cursor position |
| **Cost** | Webcam + 2 PCs | Tobii 5 (~$200+) | ~$40 glasses | SmartNav ~$400; CameraMouse free | Free (webcam) | 2 cameras + mount | Free (phone camera) | Free (phone camera) |
| **Frame Rate** | 30 fps | N/A (Tobii dependent) | N/A | 30 fps | 30+ fps | 30 fps | ~40 fps | 15–28 fps |

---

## 3. Metrics Comparison

| Metric | Study 1 | Study 2 | Study 3 | Study 4 | Study 5 | Study 6 | Study 7 | Study 8 |
|--------|---------|---------|---------|---------|---------|---------|---------|---------|
| **Pointing Accuracy** | Qualitative (9/12 success) | 92% selection accuracy | 100% (0% error) | Fitts throughput curves | Best path deviation of 3 systems | N/A | TP: 0.90 bps | N/A (text entry) |
| **Movement Speed** | 1.6x slower than mouse | 4.79s vs 7.72s selection | 359–509 px/s | MT: 1.5–12.4s | 2–3s per target | Mouse dist. -32% | MT: 1.89–4.57s | 5.98 WPM |
| **Latency** | Real-time (33ms/frame) | N/A | N/A | N/A | 2–3s per target transition | ~33ms (1 frame) | N/A | N/A |
| **Jitter** | Not measured | N/A | Low (small SD) | N/A | <10 px | N/A | N/A | Issue noted in testing |
| **Fatigue** | Not formally measured | N/A | N/A | N/A | Survey: 7.25/10 | N/A | Minor dry eyes | NASA-TLX: 58 (high) |
| **Fitts Throughput** | N/A | N/A | N/A | Yes (multiple IDs) | N/A | N/A | 0.61–0.96 bps | N/A |
| **Error Rate** | Dwell-related misclicks | 51% (control) → 92% (adapted) | 0% | Varied by device/ID | Minimal overshooting | N/A | N/A | KSPC: 1.67 |
| **User Satisfaction** | Anecdotal (positive) | N/A | N/A | N/A | 7.85/10 applicability | 7/8 preferred | Qualitative (positive) | SUS: 59.1 |

---

## 4. Baseline Study Selection

### Recommended Baseline: **Study 5 — 3M-HCI (Quan et al., 2025)**

**Justification:**

1. **Most relevant technology stack**: Uses MediaPipe Face Mesh (478 landmarks) — the same library specified in our project requirements. This makes direct replication feasible.

2. **Comprehensive metrics**: Reports jitter (<10px), latency (2–3s), path accuracy, and user satisfaction (7.85/10) — covering the exact metrics our evaluation module needs.

3. **Modern and state-of-the-art**: Published in 2025, it benchmarks against CameraMouseAI and Google Project GameFace, providing current baselines.

4. **Proven filtering approach**: Uses 1€ adaptive filter which dynamically adjusts cutoff frequency based on signal speed — superior to fixed low-pass filters for the smoothness-vs-responsiveness tradeoff.

5. **Cross-modal design**: Integrates facial expressions + voice + eye gaze, aligning with our virtual keyboard and emergency panel requirements.

6. **Desktop + webcam**: Matches our target environment (Windows PC with single webcam).

7. **Open source**: Code available on GitHub for reference implementation.

### Secondary References:
- **Study 1 (Camera Mouse)**: Foundational work; dwell-click baseline; tested with 12 disabled users
- **Study 7 (Mobile HBP)**: Best Fitts' Law methodology with impaired users; calibration-free design principles
- **Study 4 (Guness)**: Modified Fitts' test methodology for our evaluation module

---

## 5. Proposed Improvements Over Baseline (Study 5)

| # | Improvement | Source Inspiration | Expected Metric Gain |
|---|------------|-------------------|---------------------|
| 1 | **Replace 1€ filter with Kalman Filter + EMA hybrid** | Project requirement + Study 6 (particle filter concept) | Reduce jitter from <10px to <5px while maintaining <50ms latency |
| 2 | **Use cv2.solvePnP for 6-DOF head pose** instead of relying solely on landmark pixel coordinates | Study 6 (6-DOF pose), Study 2 (Euler angles) | More robust angle-to-coordinate mapping; better handles depth/rotation changes |
| 3 | **9-point calibration routine** instead of calibration-free | Study 4 (Fitts-based calibration), Study 6 (3-point calibration) | Improve pointing accuracy by 15–20% via personalized mapping |
| 4 | **Adaptive sensitivity curves** using sigmoid acceleration | Study 5 (already uses sigmoid), Study 7 (gain factor) | Fine-tune K, slope, offset per user during calibration for better control |
| 5 | **Dual click engine: Dwell-time + Blink detection** | Study 1 (dwell), Study 7 (dwell/blink/smile), Study 8 (blink) | Configurable 0.5–2.0s dwell; blink as alternative for users with involuntary movements |
| 6 | **Dedicated virtual keyboard with Arabic+English** | Study 8 (Faceboard swipe keyboard concept) | Purpose-built large-target keyboard avoids small-target accuracy issues; serves Arabic-speaking quadriplegic patients |
| 7 | **Emergency panel with image-based icons** | Novel (not in any study) | One-click access to needs/pain communication; critical for non-verbal patients |
| 8 | **Real-time CSV logging for experiment reproducibility** | Study 5 (GitHub data), Study 7 (Fitts protocol) | Enable exact metric replication: RMSE, accuracy %, latency ms, task completion time |
| 9 | **Fatigue-aware sensitivity adjustment** | Study 8 (high NASA-TLX fatigue), Study 2 (involuntary movement adaptation) | Auto-reduce sensitivity after N minutes; periodic rest prompts to reduce strain |
| 10 | **Multi-landmark anchor (medial canthi)** instead of nose tip | Study 5 (inner eye corners as anchor) | Eliminates cursor drift during facial expressions (nose/mouth movements) |

---

## 6. Replication Targets

Before applying improvements, we must first replicate the baseline (Study 5) metrics:

| Metric | Study 5 Reported Value | Our Replication Target |
|--------|----------------------|----------------------|
| Cursor jitter (idle) | <10 pixels | <10 pixels |
| Target transition latency | 2–3 seconds | <3 seconds |
| Path deviation from optimal | Best among 3 systems tested | Measure and report |
| Click accuracy (facial expression) | No overshooting observed | 0% unintended clicks |
| System responsiveness rating | 8.88/10 | ≥8.0/10 |
| Precision rating | 8.37/10 | ≥8.0/10 |
| CPU usage | 6.1–52.8% (varies by hardware) | <30% on target hardware |

After replication is confirmed, improvements will be applied incrementally and each metric re-measured.

---

## 7. Evaluation Framework (from Studies)

Based on the methodologies across all 8 studies, our evaluation module should implement:

1. **Fitts' Law Test** (Studies 3, 4, 7): Multi-directional tapping with varying ID (1.5–5.2 bits)
2. **Target Selection Task** (Studies 2, 5): Move cursor to predefined targets, measure time and deviation
3. **Text Entry Test** (Study 8): WPM, KSPC, error rates using virtual keyboard
4. **Jitter Measurement** (Study 5): Keep head still, measure cursor deviation over 30 seconds
5. **Fatigue Assessment** (Study 8): NASA-TLX after extended use
6. **Comparison Protocol**: Baseline (mouse) vs head-tracking, same as Study 1 methodology
7. **ISO 9241-9 Compliance** (Studies 3, 4, 7): Standardized throughput calculation

---

## 8. Risk Analysis

| Risk | Mitigation | Source Study |
|------|-----------|-------------|
| MediaPipe fails in low light | Ensure adequate lighting; test in multiple conditions | Study 5, Study 8 |
| Involuntary movements cause false clicks | Implement speed controller (Study 2) + priority-based expression triggering (Study 5) | Studies 2, 5 |
| Calibration too difficult for quadriplegic patients | Offer both calibration-free (edge clipping) and assisted 9-point calibration | Studies 7, 8 |
| High CPU usage on patient's computer | Optimize frame rate; process at 320x240 as in Study 1 | Studies 1, 5 |
| Neck fatigue from extended use | Auto-rest prompts; fatigue-aware sensitivity | Study 8 |
| Arabic keyboard layout complexity | Dedicated grid layout with large targets (≥60px) | Study 8 |
