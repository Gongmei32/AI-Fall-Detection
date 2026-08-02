from pydoc import text
from tkinter import font
from tkinter import font

import cv2


class Drawer:
    @staticmethod
    def draw_info(
        frame,
        fps,
        left_shoulder,
        right_hip,
        body_angle,
        knee_angle,
        max_hip_speed,
        posture,
        posture_color,
        fall_duration,
        fall_detected,
        fall_confidence,
        transition,
    ):

        font = cv2.FONT_HERSHEY_SIMPLEX

        cv2.putText(
            frame,
            f"FPS             : {int(fps)}",
            (20, 50),
            font,
            1,
            (0, 255, 0),
            2,
        )

        cv2.putText(
            frame,
            f"Left Shoulder   : ({left_shoulder.x:.2f}, {left_shoulder.y:.2f})",
            (20, 100),
            font,
            1,
            (255, 255, 0),
            2,
        )

        cv2.putText(
            frame,
            f"Right Hip       : ({right_hip.x:.2f}, {right_hip.y:.2f})",
            (20, 145),
            font,
            1,
            (255, 255, 0),
            2,
        )

        cv2.putText(
            frame,
            f"Body Angle      : {body_angle:.1f}°",
            (20, 190),
            font,
            1,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"Knee Angle      : {knee_angle:.1f}°",
            (20, 235),
            font,
            1,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"Hip Speed   : {max_hip_speed:.3f}",
            (20, 280),
            font,
            1,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"Fall Time       : {fall_duration:.1f} s",
            (20, 325),
            font,
            1,
            (0, 165, 255),
            2,
        )

        cv2.putText(
            frame,
            f"Confidence     : {fall_confidence:.0f}%",
            (20, 370),
            font,
            1,
            (255, 255, 0),
            2,
        )

        cv2.putText(
            frame,
            f"Posture         : {posture}",
            (20, 400),
            font,
            1.2,
            posture_color,
            3,
        )

        text = f"Transition : {transition}"

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 2

        (text_width, text_height), _ = cv2.getTextSize(
            text,
            font,
            font_scale,
            thickness
        )

        frame_height, frame_width = frame.shape[:2]

        x = (frame_width - text_width) // 2
        y = 40

        cv2.rectangle(
            frame,
            (x - 15, y - text_height - 10),
            (x + text_width + 15, y + 10),
            (0, 0, 0),
            -1,
        )

        cv2.putText(
            frame,
            text,
            (x, y),
            font,
            font_scale,
            (255, 255, 255),
            thickness,
        )

        if fall_detected:

            cv2.putText(
                frame,
                "FALL DETECTED",
                (20, 420),
                font,
                1.4,
                (0, 0, 255),
                3,
            )

        else:

            cv2.putText(
                frame,
                "System Normal",
                (20, 460),
                font,
                1.2,
                (0, 255, 0),
                2,
            )