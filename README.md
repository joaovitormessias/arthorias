# Arthorias — Gesture-Controlled Robotic Hand

**Translate camera-detected hand landmarks into servo commands.**

A final-year academic project by João Vitor Messias da Cruz Damasio at Instituto Federal Catarinense, Campus Fraiburgo. The main entry point tracks one hand with MediaPipe and OpenCV, classifies finger positions using landmark distances, and drives five servos through Firmata.

**Python · OpenCV · MediaPipe Hands · PyFirmata · Arduino**

## Main workflow

Camera frame → RGB conversion → 21 hand landmarks → finger-distance rules → servo angles.

The main script implements discrete open/close commands. Additional experimental scripts exist, but advanced arm rotation, smoothing, and universal RP2040 compatibility are not established by this entry point.

## Hardware mapping

| Finger | Digital pin | Open angle | Closed angle in abrir_fechar |
| --- | --- | --- | --- |
| Thumb | 7 | 0° | 100° |
| Index | 6 | 0° | 120° |
| Middle | 5 | 0° | 120° |
| Ring | 4 | 0° | 120° |
| Little | 3 | 0° | 120° |

These values describe the code, not calibrated limits for another mechanism. Review power, wiring, common ground, and safe mechanical travel before connecting servos. No hardware movement was performed during this review.

## Setup

Use a camera, a compatible Arduino running servo-capable Firmata firmware, and Python/dependencies compatible with the legacy MediaPipe Solutions and PyFirmata APIs.

```bash
git clone https://github.com/joaovitormessias/arthorias.git
cd arthorias
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export ARDUINO_PORT=/dev/ttyACM0
python main.py
```

Set `ARDUINO_PORT` to your actual device (for example `COM5` on Windows). Camera index is currently 0. Press Q to exit. Dependencies are unpinned; hardware/API compatibility has not been validated in this review environment.

## Code walkthrough

- [main.py](main.py): acquisition, landmarks, finger rules, and OpenCV display. Selects DirectShow only on Windows.
- [servo.py](servo.py): serial board setup and finger-to-pin mapping; board connection happens on import.
- [mediapipe_demo.py](mediapipe_demo.py): renamed experiment, previously `mediapipe.py`. The previous name shadowed the installed MediaPipe package.
- [braco.py](braco.py): separate arm experiment; do not assume identical behavior to main.py.

## Verification and limits

Python compilation and the mocked servo test pass without hardware. Run `python -m unittest discover -s tests` from the repository root. They do not validate camera detection, serial timing, power requirements, or mechanical safety. Existing `teste*.py` files are hardware experiments, not a dependable isolated test suite.

The main algorithm uses image-space thresholds and can be sensitive to distance, lighting, occlusion, and hand orientation. It sends repeated commands and does not implement a calibrated fail-safe on tracking loss. Next steps: measured gesture accuracy, a camera-only mode, dependency pinning, and a recorded hardware demonstration.

[License](LICENSE) · [Maintainer](https://github.com/joaovitormessias)
