import cv2
import mediapipe as mp


class PoseDetector:

    def __init__(self):

        self.mp_pose = mp.solutions.pose

        self.pose = self.mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.mp_draw = mp.solutions.drawing_utils

    def detect(self, frame):

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = self.pose.process(rgb_frame)

        if results.pose_landmarks:

            drawing_spec = self.mp_draw.DrawingSpec(
                color=(0, 255, 0),
                thickness=4,
                circle_radius=4
            )

            connection_spec = self.mp_draw.DrawingSpec(
                color=(255, 255, 255),
                thickness=3
            )

            self.mp_draw.draw_landmarks(
                frame,
                results.pose_landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                drawing_spec,
                connection_spec
            )

            return frame, results.pose_landmarks.landmark

        return frame, None