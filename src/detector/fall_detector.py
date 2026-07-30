import math


class FallDetector:

    def calculate_joint_angle(self, point1, point2, point3):

        import math
 
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

    def calculate_midpoint(self, point1, point2):
        """
        Calculate the midpoint between two pose landmarks.
        """
        x = (point1.x + point2.x) / 2
        y = (point1.y + point2.y) / 2
        return (x, y)

    def calculate_body_angle(self, shoulder_center, hip_center):
        """
        Calculate the angle of the body using the
        shoulder and hip center points.
        """
        dx = hip_center[0] - shoulder_center[0]
        dy = hip_center[1] - shoulder_center[1]

        angle = abs(math.degrees(math.atan2(dy, dx)))

        return angle

    def classify_posture(self, body_angle, knee_angle):
        """
        Classify the body posture based on body angle.
        """

        if body_angle > 150:
            return "Lying", (255, 0, 0)

        elif knee_angle > 150:
            return "Standing", (0, 255, 0)

        else:
            return "Sitting", (0, 255, 255)