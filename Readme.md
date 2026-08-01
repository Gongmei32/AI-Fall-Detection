# AI Fall Detection System

A real-time computer vision project for detecting human falls using deep learning and pose estimation.

## Features
- Real-time webcam detection
- Pose estimation
- Fall detection
- Event logging
- Multi-person support
- Research-ready architecture

## Tech Stack
- Python
- OpenCV
- MediaPipe
- YOLO
- PyTorch

## Status
🚧 Under Development

## Title
"An Explainable Multi-Modal Real-Time Human Fall Detection System Using Pose Estimation and Vision Transformers"

## Milestone 1-3 missed writing

## Milestone 4 – Body Center & Stable Angle Calculation ✅
### Features
- Calculated shoulder center using left and right shoulders.
- Calculated hip center using left and right hips.
- Implemented stable body angle calculation.
- Displayed body angle in real time.
- Improved skeleton visualization with thicker landmarks.
- Increased camera resolution support for Full HD (1920×1080).

## Milestone 5 – Real-Time Posture Classification ✅

### Objective
Implement a posture classification system using human pose landmarks extracted with MediaPipe.

### Features Implemented
- Calculated body angle using the shoulder and hip center points.
- Calculated knee angle using the hip, knee, and ankle landmarks.
- Combined body angle and knee angle for improved posture classification.
- Classified posture into:
  - 🟢 Standing
  - 🟡 Sitting
  - 🔵 Lying
- Displayed body angle, knee angle, FPS, and posture in real time.
- Increased camera resolution support to Full HD (1920 × 1080).
- Enhanced pose visualization with larger center markers and thicker skeleton drawing.

### Current Classification Logic

Standing
- Body Angle ≈ 90°
- Knee Angle > 150°

Sitting
- Body Angle ≈ 90°
- Knee Angle ≈ 90–100°

Lying
- Body Angle > 150°

### Technologies Used
- Python
- OpenCV
- MediaPipe Tasks
- Object-Oriented Programming

### Project Status
✅ Milestone 5 Completed

The system can now recognize three fundamental human postures in real time, providing the foundation for fall event detection in the next milestone

## Milestone 6.1 – Posture Transition Tracking 🔄

### Objective
Introduce temporal state tracking to monitor changes in human posture across consecutive video frames. This serves as the first step toward real-time fall event detection.

### Features Implemented
- Added previous posture memory.
- Added current posture tracking.
- Detected posture transitions in real time.
- Displayed posture changes through terminal output.
- Established the foundation for event-based fall detection.

## Milestone 6.2 – Hip Movement Speed Analysis

### Objective
Implemented hip movement speed tracking to improve fall detection accuracy. The system now monitors the vertical movement of the body's hip center between consecutive frames.

### Features Added
- Calculates the midpoint of both hips.
- Tracks the previous hip position.
- Computes hip movement speed using frame-to-frame displacement.
- Displays Hip Speed in real time.
- Continues tracking posture transitions.
- Modularized the user interface using a dedicated `Drawer` class.
- Improved code organization and readability.

### Technical Details
- Hip center is calculated from the left and right hip landmarks.
- Hip speed is computed as:

Hip Speed = |Current Hip Y − Previous Hip Y|

- Higher values indicate faster body movement.
- This metric will be used in later milestones to distinguish normal posture changes from actual falls.

## Milestone 6.3 – Fall Duration Timer

### Objective
Implemented a real-time fall duration timer to monitor how long a person remains in a lying posture. This helps distinguish normal activities from potential falls.

### Features Added
- Introduced a fall timer that starts when the posture is classified as **Lying**.
- Automatically resets the timer when the user returns to **Standing** or **Sitting**.
- Displays the elapsed fall duration in real time.
- Integrated the timer into the information panel.

### Technical Details
- Uses `time.time()` to record the timestamp when the lying posture begins.
- Calculates the elapsed duration each frame.
- Resets the timer whenever the posture changes away from **Lying**.

## Milestone 6.4 – Fall Confirmation Logic

### Objective
Implemented intelligent fall confirmation logic to reduce false alarms by verifying that a person remains in a lying posture for a predefined duration before declaring a fall.

### Features Added
- Added a configurable fall detection threshold.
- Introduced a real-time fall confirmation flag.
- Combined posture classification with fall duration to determine whether a fall has occurred.
- Displays the current system status ("System Normal" or "FALL DETECTED") on the interface.
- Improved the reliability of fall detection by avoiding immediate alerts when a person first lies down.

### Technical Details
The system continuously monitors the detected posture and the elapsed fall duration.

A fall is confirmed only when:

```
Posture == "Lying"
AND
Fall Duration >= 3.0 seconds
```

When these conditions are satisfied:

- `fall_detected` is set to `True`.
- A **FALL DETECTED** warning is displayed.

Otherwise:

- `fall_detected` remains `False`.
- The interface displays **System Normal**.