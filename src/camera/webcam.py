import cv2
import time

from src.pose.pose_detector import PoseDetector
from src.detector.fall_detector import FallDetector


class Webcam:

    def __init__(self, camera_index=0):

        self.camera = cv2.VideoCapture(camera_index)

        if not self.camera.isOpened():
            raise Exception("Camera could not be opened")

        self.pose_detector = PoseDetector()
        self.fall_detector = FallDetector()
        self.previous_time = 0

    def start(self):

        while True:

            success, frame = self.camera.read()

            if not success:
                break

            # Pose detection
            frame, landmarks = self.pose_detector.detect(frame)

            # Display landmark coordinates
            if landmarks:

                left_shoulder = landmarks[11]
                right_shoulder = landmarks[12]

                left_hip = landmarks[23]
                right_hip = landmarks[24]
                angle = self.fall_detector.calculate_angle(
                    left_shoulder,
                    left_hip
               )

                cv2.putText(
                    frame,
                    f"Left Shoulder: ({left_shoulder.x:.2f}, {left_shoulder.y:.2f})",
                    (20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    f"Right Hip: ({right_hip.x:.2f}, {right_hip.y:.2f})",
                    (20, 110),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (255, 255, 0),
                    2
                )
                cv2.putText(
                    frame,
                    f"Body Angle: {angle:.1f}",
                    (20, 140),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 255),
                    2
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