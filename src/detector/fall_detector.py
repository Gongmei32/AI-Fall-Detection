import math


class FallDetector:

    def calculate_joint_angle(self, point1, point2, point3):
        """
        Calculate the angle formed by three body landmarks.
        """

        a = (point1.x, point1.y)
        b = (point2.x, point2.y)
        c = (point3.x, point3.y)

        radians = (
            math.atan2(c[1] - b[1], c[0] - b[0]) -
            math.atan2(a[1] - b[1], a[0] - b[0])
        )

        angle = abs(math.degrees(radians))

        if angle > 180:
            angle = 360 - angle

        return angle

    def calculate_confidence(
        self,
        body_angle,
        knee_angle,
        max_hip_speed,
        posture,
        fall_duration,
    ):
        """
        Calculate an overall fall confidence score (0–100%).
        """

        confidence = 0

        # -------------------------
        # Body Angle
        # -------------------------
        if body_angle >= 170:
            confidence += 25
        elif body_angle >= 150:
            confidence += 20
        elif body_angle >= 120:
            confidence += 10

        # -------------------------
        # Knee Angle
        # -------------------------
        if knee_angle >= 170:
            confidence += 20
        elif knee_angle >= 150:
            confidence += 15

        # -------------------------
        # Hip Speed
        # -------------------------
        if max_hip_speed >= 0.010:
            confidence += 20
        elif max_hip_speed >= 0.005:
            confidence += 10
        elif max_hip_speed >= 0.002:
            confidence += 5

        # -------------------------
        # Posture
        # -------------------------
        if posture == "Lying":
            confidence += 20

        # -------------------------
        # Fall Duration
        # -------------------------
        if fall_duration >= 2:
            confidence += 15

        return min(confidence, 100)

    def calculate_midpoint(self, point1, point2):
        """
        Calculate the midpoint between two pose landmarks.
        """

        x = (point1.x + point2.x) / 2
        y = (point1.y + point2.y) / 2

        return (x, y)

    def calculate_body_angle(self, shoulder_center, hip_center):
        """
        Calculate the body angle using the shoulder and hip centers.
        """

        dx = hip_center[0] - shoulder_center[0]
        dy = hip_center[1] - shoulder_center[1]

        angle = abs(math.degrees(math.atan2(dy, dx)))

        return angle

    def classify_posture(self, body_angle, knee_angle):
        """
        Classify the person's posture.
        """

        if body_angle > 150:
            return "Lying", (255, 0, 0)

        elif knee_angle > 150:
            return "Standing", (0, 255, 0)

        else:
            return "Sitting", (0, 255, 255)