from ultralytics import YOLO
import cv2
import json
import torch
import os

# Ensure GPU is available
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} for YOLO inference")

# Load YOLO model
model = YOLO('models/yolov8n.pt').to(device)

# Paths
input_video_path = 'resources/media/sample_video.mp4'
output_video_path = 'output/tracked_output.mp4'
output_json_path = 'output/tracked_objects.json'

# Ensure the output directories exist
os.makedirs(os.path.dirname(output_video_path), exist_ok=True)
os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

# Video capture
cap = cv2.VideoCapture(input_video_path)
if not cap.isOpened():
    raise FileNotFoundError(f"Cannot open video file: {input_video_path}")

# Video properties
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(cap.get(cv2.CAP_PROP_FPS))
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

# Initialize JSON structure
tracked_data = {}

# Specify number of frames to iterate by
frame_skip = 1

for frame_index in range(0, frame_count, frame_skip):
    print(frame_index)
    ret, frame = cap.read()
    if not ret:
        break

    print(frame_index)

    # Process frame
    results = model.track(frame, persist=True, conf=0.5)

    # Annotate the frame using YOLO's built-in plot function
    annotated_frame = results[0].plot()

    # Extract object data from YOLO results
    frame_objects = []
    if len(results[0].boxes) > 0:  # Ensure there are detections
        print(frame_index)
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


    # Save data and write video
    tracked_data[frame_index] = frame_objects
    out.write(annotated_frame)

# Save JSON
with open(output_json_path, 'w') as json_file:
    json.dump(tracked_data, json_file, indent=4)

# Release resources
cap.release()
out.release()
print(f"Tracked video saved at {output_video_path}")
print(f"Tracking data saved at {output_json_path}")
