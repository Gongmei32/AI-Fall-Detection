import cv2
from ultralytics import YOLO


class PersonTracker:

    def __init__(self, model_path="yolo11n.pt"):
        self.model = YOLO(model_path)
        self.selected_id = None

    def detect_and_track(self, frame):

        results = self.model.track(
            frame,
            persist=True,
            classes=[0],
            verbose=False
        )

        people = []

        if not results:
            return frame, people

        result = results[0]

        if result.boxes is None:
            return frame, people

        for box in result.boxes:

            if box.id is None:
                continue

            person_id = int(box.id[0])

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0].tolist()
            )

            people.append({
                "id": person_id,
                "bbox": (x1, y1, x2, y2)
            })

            if person_id == self.selected_id:
                color = (0, 255, 255)
                thickness = 4
                label = f"SELECTED Person {person_id}"
            else:
                color = (255, 255, 255)
                thickness = 2
                label = f"Person {person_id}"

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                color,
                thickness
            )

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 30)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

        return frame, people

    def select_person(self, x, y, people):

        for person in people:

            x1, y1, x2, y2 = person["bbox"]

            if x1 <= x <= x2 and y1 <= y <= y2:

                self.selected_id = person["id"]

                print(
                    f"Selected Person ID: {self.selected_id}"
                )

                return self.selected_id

        return None

    def get_selected_person(self, people):

        if self.selected_id is None:
            return None

        for person in people:

            if person["id"] == self.selected_id:
                return person

        return None