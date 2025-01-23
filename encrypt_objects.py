import cv2
import numpy as np
import json

def encrypt_object(frame, coordinates, key):
    """
    Encrypts a rectangular region in a single frame using XOR operation.
    """
    x1, y1 = map(int, coordinates[0])
    x2, y2 = map(int, coordinates[1])
    height, width, _ = frame.shape

    # Ensure coordinates are within bounds
    x1, x2 = max(0, x1), min(width, x2 + 1)
    y1, y2 = max(0, y1), min(height, y2 + 1)

    # Encrypt using vectorized operations
    print("Object Box Coords %d %d %d %d", x1, x2, y1, y2)
    frame[y1:y2, x1:x2] ^= np.array(key, dtype=np.uint8);

def encrypt_video(input_path, output_path, json_path, selected_ids, key=(128, 64, 32)):
    """
    Encrypts specified objects based on their IDs from JSON in each frame of a video.
    """
    # Validate key length
    assert len(key) == 3, "Encryption key must have exactly 3 values for RGB channels."

    # Load and preprocess JSON data
    with open(json_path, 'r') as json_file:
        tracked_data = {int(k): v for k, v in json.load(json_file).items()}

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise ValueError(f"Cannot open video file: {input_path}")

    # Video properties
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Get objects for this frame
        frame_objects = tracked_data.get(frame_idx, [])
        objects_to_encrypt = [
            [(obj["bounding_box"]["x1"], obj["bounding_box"]["y1"]),
             (obj["bounding_box"]["x2"], obj["bounding_box"]["y2"])]
            for obj in frame_objects if obj["track_id"] in selected_ids
            
        ]

        # Encrypt objects
        for obj_coords in objects_to_encrypt:
            encrypt_object(frame, obj_coords, key)

        out.write(frame)
        frame_idx += 1

        # Log progress every 10 frames
        if frame_idx % 10 == 0:
            print(f"Processed {frame_idx} frames...")

    cap.release()
    out.release()
    print(f"Encrypted video saved to {output_path}")


# User specifies the track IDs they want encrypted
selected_ids = [1]

# Paths to video and JSON
input_video_path = "resources/media/sample_video.mp4"
output_video_path = "output/encrypted_video.mp4"
json_path = "output/tracked_objects.json"

# Process the video
encrypt_video(input_video_path, output_video_path, json_path, selected_ids)
