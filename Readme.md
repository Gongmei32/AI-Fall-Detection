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

The system can now recognize three fundamental human postures in real time, providing the foundation for fall event detection in the next milestone.