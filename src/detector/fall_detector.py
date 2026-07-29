import math


class FallDetector:

    def calculate_angle(self, shoulder, hip):

        dx = hip.x - shoulder.x
        dy = hip.y - shoulder.y

        angle = abs(math.degrees(math.atan2(dy, dx)))

        return angle