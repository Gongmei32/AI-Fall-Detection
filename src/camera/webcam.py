import cv2
import time

from src.pose.pose_detector import PoseDetector
from src.detector.fall_detector import FallDetector
from src.utils.drawer import Drawer


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

        self.previous_posture = "Unknown"
        self.current_posture = "Unknown"

        self.previous_hip_y = None
        self.hip_speed = 0.0

        # Fall Timer
        self.fall_start_time = None
        self.fall_duration = 0.0

    def start(self):

        cv2.namedWindow(
            "AI Fall Detection - Pose",
            cv2.WINDOW_NORMAL
        )

        cv2.resizeWindow(
            "AI Fall Detection - Pose",
            1920,
            1080
        )

        while True:

            success, frame = self.camera.read()

            if not success:
                break

            # Pose Detection
            frame, landmarks = self.pose_detector.detect(frame)

            if landmarks:

                # -----------------------------
                # Landmarks
                # -----------------------------

                left_shoulder = landmarks[11]
                right_shoulder = landmarks[12]

                left_hip = landmarks[23]
                right_hip = landmarks[24]

                left_knee = landmarks[25]
                left_ankle = landmarks[27]

                # -----------------------------
                # Centers
                # -----------------------------

                shoulder_center = self.fall_detector.calculate_midpoint(
                    left_shoulder,
                    right_shoulder
                )

                hip_center = self.fall_detector.calculate_midpoint(
                    left_hip,
                    right_hip
                )

                # -----------------------------
                # Hip Speed
                # -----------------------------

                current_hip_y = hip_center[1]

                if self.previous_hip_y is not None:
                    self.hip_speed = abs(
                        current_hip_y - self.previous_hip_y
                    )

                self.previous_hip_y = current_hip_y

                # -----------------------------
                # Frame Size
                # -----------------------------

                height, width, _ = frame.shape

                # -----------------------------
                # Angles
                # -----------------------------

                body_angle = self.fall_detector.calculate_body_angle(
                    shoulder_center,
                    hip_center
                )

                knee_angle = self.fall_detector.calculate_joint_angle(
                    left_hip,
                    left_knee,
                    left_ankle
                )

                # -----------------------------
                # Posture
                # -----------------------------

                posture, posture_color = (
                    self.fall_detector.classify_posture(
                        body_angle,
                        knee_angle
                    )
                )

                self.current_posture = posture

                # ------------------------------------
                # Fall Duration Timer
                # ------------------------------------

                if posture == "Lying":

                    if self.fall_start_time is None:
                        self.fall_start_time = time.time()

                    self.fall_duration = (
                        time.time() - self.fall_start_time
                    )

                else:

                    self.fall_start_time = None
                    self.fall_duration = 0.0

                if self.current_posture != self.previous_posture:

                    print(
                        f"Posture changed: "
                        f"{self.previous_posture} -> "
                        f"{self.current_posture}"
                    )

                    self.previous_posture = self.current_posture

                # -----------------------------
                # Draw Body Centers
                # -----------------------------

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

                # -----------------------------
                # FPS
                # -----------------------------

                current_time = time.time()

                fps = (
                    1 / (current_time - self.previous_time)
                    if self.previous_time else 0
                )

                self.previous_time = current_time

                # -----------------------------
                # Draw Information
                # -----------------------------

                Drawer.draw_info(
                    frame,
                    fps,
                    left_shoulder,
                    right_hip,
                    body_angle,
                    knee_angle,
                    self.hip_speed,
                    posture,
                    posture_color,
                    self.fall_duration,
                )

            else:

                cv2.putText(
                    frame,
                    "No Pose Detected",
                    (20, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2
                )

            # -----------------------------
            # Show Window
            # -----------------------------

            cv2.imshow(
                "AI Fall Detection - Pose",
                frame
            )

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.camera.release()
        cv2.destroyAllWindows()