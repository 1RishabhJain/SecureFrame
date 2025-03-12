import json

def load_json_data(json_path):
    with open(json_path, 'r') as json_file:
        return json.load(json_file)
    
def log_progress(frame_index, batch_size=10):
    if frame_index % batch_size == 0:
        print(f"Processed {frame_index} frames...")

def get_frame_data(tracked_data, frame_index):
    frame_key = str(frame_index)
    return tracked_data.get(frame_key, [])

def get_objects_in_frame(tracked_data, frame_index, selected_ids):
    frame_tracked_data = get_frame_data(tracked_data, frame_index)
    objects_in_frame = [
        {
            "track_id": obj["track_id"],
            "object_type": obj["object_type"],
            "confidence": obj["confidence"],
            "bounding_box": {
                "x1": obj["bounding_box"]["x1"],
                "y1": obj["bounding_box"]["y1"],
                "x2": obj["bounding_box"]["x2"],
                "y2": obj["bounding_box"]["y2"]
            }
        }
        for obj in frame_tracked_data if obj["track_id"] in selected_ids
    ]
    
    return objects_in_frame

def validate_coordinates(frame, bounding_box):
    """
    Validates that bounding box coordinates exist and are within frame bounds
    """
    height, width, _ = frame.shape  # Get frame dimensions

    # Ensure all required keys exist and contain valid numeric values
    required_keys = ["x1", "y1", "x2", "y2"]
    for key in required_keys:
        if key not in bounding_box or bounding_box[key] is None:
            raise ValueError(f"Missing or None value for '{key}' in bounding box: {bounding_box}")

    # Convert values to integers
    try:
        x1 = int(bounding_box["x1"])
        y1 = int(bounding_box["y1"])
        x2 = int(bounding_box["x2"])
        y2 = int(bounding_box["y2"])
    except (ValueError, TypeError):
        raise ValueError(f"Invalid coordinate types in bounding box: {bounding_box}")

    # Ensure coordinates are within valid frame bounds
    if not (0 <= x1 <= width and 0 <= x2 <= width and 0 <= y1 <= height and 0 <= y2 <= height):
        raise ValueError(f"Bounding box out of frame bounds: {bounding_box} (Frame size: {width}x{height})")

    # Ensure x1 < x2 and y1 < y2 (otherwise it's an invalid bounding box)
    if x1 >= x2 or y1 >= y2:
        raise ValueError(f"Invalid bounding box dimensions (x1 >= x2 or y1 >= y2): {bounding_box}")

    return (x1, y1, x2, y2)

def get_unique_track_ids(tracked_data):
    unique_track_ids = set()
    
    for key, entries in tracked_data.items():
        for entry in entries:
            if "track_id" in entry:
                unique_track_ids.add(entry["track_id"])
    
    return list(unique_track_ids)