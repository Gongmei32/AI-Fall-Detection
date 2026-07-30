import math


class FallDetector:

    def calculate_midpoint(self, point1, point2):
        x = (point1.x + point2.x) / 2
        y = (point1.y + point2.y) / 2
        return x, y

    def calculate_body_angle(self, shoulder_center, hip_center):
        dx = hip_center[0] - shoulder_center[0]
        dy = hip_center[1] - shoulder_center[1]

        angle = abs(math.degrees(math.atan2(dy, dx)))

        return angle