import cv2
import time


class Webcam:

    def __init__(self, camera_index=0):
        self.camera = cv2.VideoCapture(camera_index)

        if not self.camera.isOpened():
            raise Exception("Camera could not be opened")

        self.previous_time = 0


    def start(self):

        while True:

            success, frame = self.camera.read()

            if not success:
                print("Failed to read camera")
                break


            # FPS calculation
            current_time = time.time()

            fps = 1 / (current_time - self.previous_time) if self.previous_time else 0

            self.previous_time = current_time


            # Display FPS
            cv2.putText(
                frame,
                f"FPS: {int(fps)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 0),
                2
            )


            cv2.imshow(
                "AI Fall Detection - Camera",
                frame
            )


            # Press Q to exit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break


        self.camera.release()
        cv2.destroyAllWindows()