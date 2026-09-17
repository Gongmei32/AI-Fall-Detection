import cv2
import time
import winsound

from src.pose.pose_detector import PoseDetector
from src.detector.fall_detector import FallDetector
from src.tracking.person_tracker import PersonTracker
from src.utils.drawer import Drawer


class Webcam:

    def __init__(self, camera_index=0):

        # ------------------------------------
        # Camera
        # ------------------------------------

        self.camera = cv2.VideoCapture(camera_index)

        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

        print("Requested Resolution: 1920 x 1080")
        print(
            "Actual Width :",
            self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        )
        print(
            "Actual Height:",
            self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        if not self.camera.isOpened():
            raise Exception("Camera could not be opened")

        # ------------------------------------
        # AI Modules
        # ------------------------------------

        self.person_tracker = PersonTracker()
        self.pose_detector = PoseDetector()
        self.fall_detector = FallDetector()

        # ------------------------------------
        # Timing
        # ------------------------------------

        self.previous_time = 0

        # ------------------------------------
        # Posture
        # ------------------------------------

        self.previous_posture = "Unknown"
        self.current_posture = "Unknown"

        # ------------------------------------
        # Hip Movement
        # ------------------------------------

        self.previous_hip_y = None

        self.hip_speed = 0.0
        self.max_hip_speed = 0.0

        # ------------------------------------
        # Fall Timer
        # ------------------------------------

        self.fall_start_time = None
        self.fall_duration = 0.0

        # ------------------------------------
        # Fall Confirmation
        # ------------------------------------

        self.fall_detected = False
        self.fall_threshold = 2.0
        self.fall_confidence = 0

        # ------------------------------------
        # Transition
        # ------------------------------------

        self.transition = "None"

        # ------------------------------------
        # Mouse Selection
        # ------------------------------------

        self.people = []

        # ------------------------------------
        # Demo Alert
        # ------------------------------------

        self.sitting_alert_enabled = True
        self.last_alert_posture = "Unknown"

    # ==================================================
    # Mouse Callback
    # ==================================================

    def mouse_callback(self, event, x, y, flags, param):

        if event == cv2.EVENT_LBUTTONDOWN:

            person_id = self.person_tracker.select_person(
                x,
                y,
                self.people
            )

            if person_id is not None:

                print(
                    f"Selected Person ID: {person_id}"
                )

                # Reset posture tracking
                self.previous_hip_y = None
                self.hip_speed = 0.0
                self.max_hip_speed = 0.0

                self.previous_posture = "Unknown"
                self.current_posture = "Unknown"

                self.fall_start_time = None
                self.fall_duration = 0.0

                self.fall_detected = False
                self.fall_confidence = 0

    # ==================================================
    # Sitting Alert
    # ==================================================

    def sitting_alert(self):

        if not self.sitting_alert_enabled:
            return

        if (
            self.current_posture == "Sitting"
            and self.last_alert_posture != "Sitting"
        ):

            print("SITTING POSTURE DETECTED")

            winsound.Beep(
                800,
                400
            )

        self.last_alert_posture = self.current_posture

    # ==================================================
    # Main Camera Loop
    # ==================================================

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

        cv2.setMouseCallback(
            "AI Fall Detection - Pose",
            self.mouse_callback
        )

        while True:

            success, frame = self.camera.read()

            if not success:
                break

            # ==========================================
            # STEP 1
            # YOLO Person Detection + Tracking
            # ==========================================

            frame, self.people = (
                self.person_tracker.detect_and_track(frame)
            )

            # ==========================================
            # STEP 2
            # Get Selected Person
            # ==========================================

            selected_person = (
                self.person_tracker.get_selected_person(
                    self.people
                )
            )

            # ==========================================
            # No Person Selected
            # ==========================================

            if selected_person is None:

                cv2.putText(
                    frame,
                    "CLICK A PERSON TO SELECT",
                    (30, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    3
                )

                cv2.imshow(
                    "AI Fall Detection - Pose",
                    frame
                )

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

                continue

            # ==========================================
            # STEP 3
            # Selected Person Bounding Box
            # ==========================================

            x1, y1, x2, y2 = selected_person["bbox"]

            # Add a small padding around person
            padding = 20

            height, width, _ = frame.shape

            x1_crop = max(0, x1 - padding)
            y1_crop = max(0, y1 - padding)

            x2_crop = min(width, x2 + padding)
            y2_crop = min(height, y2 + padding)

            person_crop = frame[
                y1_crop:y2_crop,
                x1_crop:x2_crop
            ]

            # ==========================================
            # STEP 4
            # MediaPipe Pose on Selected Person
            # ==========================================

            pose_frame, landmarks = (
                self.pose_detector.detect(
                    person_crop.copy()
                )
            )

            # ==========================================
            # Convert Landmarks to Full-Frame Coordinates
            # ==========================================

            if landmarks:

                left_shoulder = landmarks[11]
                right_shoulder = landmarks[12]

                left_hip = landmarks[23]
                right_hip = landmarks[24]

                left_knee = landmarks[25]
                left_ankle = landmarks[27]

                # --------------------------------------
                # Centers
                # --------------------------------------

                shoulder_center = (
                    self.fall_detector.calculate_midpoint(
                        left_shoulder,
                        right_shoulder
                    )
                )

                hip_center = (
                    self.fall_detector.calculate_midpoint(
                        left_hip,
                        right_hip
                    )
                )

                # --------------------------------------
                # Hip Speed
                # --------------------------------------

                current_hip_y = hip_center[1]

                if self.previous_hip_y is not None:

                    self.hip_speed = abs(
                        current_hip_y -
                        self.previous_hip_y
                    )

                self.previous_hip_y = current_hip_y

                if self.hip_speed > self.max_hip_speed:

                    self.max_hip_speed = self.hip_speed

                # --------------------------------------
                # Angles
                # --------------------------------------

                body_angle = (
                    self.fall_detector.calculate_body_angle(
                        shoulder_center,
                        hip_center
                    )
                )

                knee_angle = (
                    self.fall_detector.calculate_joint_angle(
                        left_hip,
                        left_knee,
                        left_ankle
                    )
                )

                # --------------------------------------
                # Posture
                # --------------------------------------

                posture, posture_color = (
                    self.fall_detector.classify_posture(
                        body_angle,
                        knee_angle
                    )
                )

                self.previous_posture = (
                    self.current_posture
                )

                self.current_posture = posture

                # --------------------------------------
                # Sitting Alert
                # --------------------------------------

                self.sitting_alert()

                # --------------------------------------
                # Fall Confidence
                # --------------------------------------

                self.fall_confidence = (
                    self.fall_detector.calculate_confidence(
                        body_angle,
                        knee_angle,
                        self.max_hip_speed,
                        posture,
                        self.fall_duration,
                    )
                )

                # ======================================
                # Fall Duration
                # ======================================

                if posture == "Lying":

                    if self.fall_start_time is None:

                        self.fall_start_time = time.time()

                    self.fall_duration = (
                        time.time() -
                        self.fall_start_time
                    )

                else:

                    self.fall_start_time = None
                    self.fall_duration = 0.0

                    self.max_hip_speed = 0.0
                    self.hip_speed = 0.0

                    self.fall_detected = False
                    self.fall_confidence = 0

                # ======================================
                # Fall Confirmation
                # ======================================

                self.fall_detected = (
                    self.fall_confidence >= 70
                    and self.max_hip_speed >= 0.005
                )

                # ======================================
                # Transition
                # ======================================

                if (
                    self.current_posture
                    != self.previous_posture
                ):

                    self.transition = (
                        f"{self.previous_posture}"
                        f" -> "
                        f"{self.current_posture}"
                    )

                    print(
                        f"Transition : {self.transition}"
                    )

                if (
                    self.transition
                    == "Sitting -> Standing"
                ):

                    print(
                        "Recovery Detected!"
                    )

                # ======================================
                # Convert Pose Crop Back to Frame
                # ======================================

                pose_height, pose_width, _ = (
                    pose_frame.shape
                )

                # Resize if necessary
                pose_frame = cv2.resize(
                    pose_frame,
                    (
                        x2_crop - x1_crop,
                        y2_crop - y1_crop
                    )
                )

                frame[
                    y1_crop:y2_crop,
                    x1_crop:x2_crop
                ] = pose_frame

                # ======================================
                # Selected Person Box
                # ======================================

                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 255, 255),
                    4
                )

                cv2.putText(
                    frame,
                    f"TRACKING PERSON "
                    f"{selected_person['id']}",
                    (x1, max(y1 - 15, 30)),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 255),
                    2
                )

                # ======================================
                # FPS
                # ======================================

                current_time = time.time()

                fps = (
                    1 /
                    (current_time - self.previous_time)
                    if self.previous_time
                    else 0
                )

                self.previous_time = current_time

                # ======================================
                # Draw Information
                # ======================================

                Drawer.draw_info(
                    frame,
                    fps,
                    left_shoulder,
                    right_hip,
                    body_angle,
                    knee_angle,
                    self.max_hip_speed,
                    posture,
                    posture_color,
                    self.fall_duration,
                    self.fall_detected,
                    self.fall_confidence,
                    self.transition,
                )

            else:

                cv2.putText(
                    frame,
                    "POSE NOT DETECTED",
                    (30, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )

            # ==========================================
            # Show Window
            # ==========================================

            cv2.imshow(
                "AI Fall Detection - Pose",
                frame
            )

            # ==========================================
            # Quit
            # ==========================================

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        # ==============================================
        # Cleanup
        # ==============================================

        self.camera.release()

        cv2.destroyAllWindows()