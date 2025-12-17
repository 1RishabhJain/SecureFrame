import cv2
import numpy as np

def initialize_webcam():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Cannot open webcam")
    
    # Reduce resolution, FPS, and buffer size
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    cap.set(cv2.CAP_PROP_FPS, 10)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

    return cap


def extract_tracking_results(results, model):
    # Extract object data from YOLO results
    frame_objects = []
    if len(results[0].boxes) > 0:  # Ensure there are detections
        for box in results[0].boxes:
            if box.id is None:  # Skip untracked objects
                continue

            track_id = int(box.id[0])
            bbox = box.xyxy[0].cpu().numpy().tolist()
            confidence = float(box.conf[0])
            object_type = model.names[int(box.cls[0])]

            frame_objects.append({
                "track_id": track_id,
                "object_type": object_type,
                "confidence": confidence,
                "bounding_box": {
                    "x1": bbox[0],
                    "y1": bbox[1],
                    "x2": bbox[2],
                    "y2": bbox[3]
                }
            })

    return frame_objects


# XOR encryption function
def encrypt_region(frame, x1, y1, x2, y2, rng):
    """Applies XOR encryption to the specified region in the frame."""
    object_region = frame[y1:y2, x1:x2]
    
    # Apply XOR operation
    mask = rng.integers(low=0, high=256, size=object_region.shape, dtype=np.uint8)
    encrypted_region = object_region ^ mask

    # Replace original with encrypted region
    frame[y1:y2, x1:x2] = encrypted_region

    return frame