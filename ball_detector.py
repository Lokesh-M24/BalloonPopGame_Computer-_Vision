from ultralytics import YOLO
import cv2

class BallDetector:
    def __init__(self, model_path="models/yolov8n.pt", conf_threshold=0.5):
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold

    def detect_balls(self, frame):
        results = self.model(frame, conf=self.conf_threshold)
        balls = []

        for r in results:
            boxes = r.boxes
            for box in boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                if conf >= self.conf_threshold:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    center_x = int((x1 + x2) / 2)
                    center_y = int((y1 + y2) / 2)
                    balls.append({
                        "bbox": (x1, y1, x2, y2),
                        "center": (center_x, center_y),
                        "confidence": conf,
                        "class_id": cls_id
                    })

        return balls
