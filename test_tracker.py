import cv2

from src.tracking.person_tracker import PersonTracker


def main():

    camera = cv2.VideoCapture(1)

    if not camera.isOpened():
        print("Camera could not be opened.")
        return

    tracker = PersonTracker()

    print("Camera started.")
    print("Click on a person to select them.")
    print("Press Q to quit.")

    selected = False

    def mouse_callback(event, x, y, flags, param):

        nonlocal selected

        if event == cv2.EVENT_LBUTTONDOWN:

            people = param["people"]
            tracker = param["tracker"]

            person_id = tracker.select_person(
                x,
                y,
                people
            )

            if person_id is not None:
                selected = True
                print(f"Tracking Person {person_id}")

    cv2.namedWindow("Person Tracking")

    while True:

        success, frame = camera.read()

        if not success:
            break

        frame, people = tracker.detect_and_track(frame)

        mouse_data = {
            "people": people,
            "tracker": tracker
        }

        cv2.setMouseCallback(
            "Person Tracking",
            mouse_callback,
            mouse_data
        )

        # -----------------------------
        # Display tracking status
        # -----------------------------

        if tracker.selected_id is not None:

            cv2.putText(
                frame,
                f"TRACKING PERSON {tracker.selected_id}",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                3
            )

        else:

            cv2.putText(
                frame,
                "CLICK A PERSON TO SELECT",
                (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 255, 255),
                2
            )

        cv2.imshow(
            "Person Tracking",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()