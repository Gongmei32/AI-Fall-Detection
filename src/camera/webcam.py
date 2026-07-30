import cv2
import time

from src.pose.pose_detector import PoseDetector
from src.detector.fall_detector import FallDetector


class Webcam:

    def __init__(self, camera_index=0):

        self.camera = cv2.VideoCapture(camera_index)

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        print("Requested Resolution: 1920 x 1080")
        print("Actual Width :", self.camera.get(cv2.CAP_PROP_FRAME_WIDTH))
        print("Actual Height:", self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if not self.camera.isOpened():
            raise Exception("Camera could not be opened")

        self.pose_detector = PoseDetector()
        self.fall_detector = FallDetector()

        self.previous_time = 0

    def start(self):
        cv2.namedWindow(
            "AI Fall Detection - Pose",
            cv2.WINDOW_NORMAL
            )

        while True:

            success, frame = self.camera.read()

            if not success:
                break

            # Pose Detection
            frame, landmarks = self.pose_detector.detect(frame)

            if landmarks:

                left_shoulder = landmarks[11]
                right_shoulder = landmarks[12]

                left_hip = landmarks[23]
                right_hip = landmarks[24]

                shoulder_center = self.fall_detector.calculate_midpoint(
                    left_shoulder,
                    right_shoulder
                )

                hip_center = self.fall_detector.calculate_midpoint(
                    left_hip,
                    right_hip
                )

                angle = self.fall_detector.calculate_body_angle(
                    shoulder_center,
                    hip_center
                )

                height, width, _ = frame.shape

                cv2.circle(
                    frame,
                    (
                        int(shoulder_center[0] * width),
                        int(shoulder_center[1] * height)
                    ),
                    10,
                    (0, 255, 255),
                    -1
                )

                cv2.circle(
                    frame,
                    (
                        int(hip_center[0] * width),
                        int(hip_center[1] * height)
                    ),
                    10,
                    (255, 0, 255),
                    -1
                )

                cv2.putText(
                    frame,
                    f"Left Shoulder: ({left_shoulder.x:.2f}, {left_shoulder.y:.2f})",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (255, 255, 0),
                    3
                )

                cv2.putText(
                    frame,
                    f"Right Hip: ({right_hip.x:.2f}, {right_hip.y:.2f})",
                    (20, 110),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (255, 255, 0),
                    3
                )

                cv2.putText(
                    frame,
                    f"Body Angle: {angle:.1f}",
                    (20, 140),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.0,
                    (0, 255, 255),
                    3
                )

            # FPS
            current_time = time.time()

            fps = 1 / (current_time - self.previous_time) if self.previous_time else 0

            self.previous_time = current_time

            cv2.putText(
                frame,
                f"FPS: {int(fps)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

            cv2.imshow(
                "AI Fall Detection - Pose",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.camera.release()
        cv2.destroyAllWindows()