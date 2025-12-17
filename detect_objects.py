import os
import cv2
import json
import subprocess
from utilities.load_model import load_model
from utilities.video_utilities import convert_to_mp4, open_video, get_frame_size, get_fps, get_frame_count, get_video_writer
from utilities.general_utilities import log_progress





def detect_objects(model_path, input_video_path, output_video_path, output_json_path):
    try:
        model, device = load_model(model_path)

        # Open video
        cap = open_video(input_video_path)
        
        # Get video properties
        frame_width, frame_height = get_frame_size(cap)
        fps = get_fps(cap)
        frame_count = get_frame_count(cap)

        # Video writer
        out = get_video_writer(output_video_path, fps, frame_width, frame_height, 'mp4v')

        # Initialize JSON structure
        tracked_data = {}

        for frame_index in range(0, frame_count):
            ret, frame = cap.read()
            if not ret:
                break

            # Process frame
            results = model.track(frame, persist=True, conf=0.5, verbose=False)

            # Annotate the frame using YOLO's built-in plot function
            annotated_frame = results[0].plot()

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

            # Save data and write video
            tracked_data[frame_index] = frame_objects
            out.write(annotated_frame)

            log_progress(frame_index)

        # Save JSON
        with open(output_json_path, 'w') as json_file:
            json.dump(tracked_data, json_file, indent=4)

        # Release resources
        cap.release()
        out.release()


        
        convert_to_mp4(output_video_path, "./frontend/app/public/videos/tracked_video.mp4")
        # Return structured response
        return {
            "success": True,
            "message": "Object detection completed successfully.",
            "total_frames_processed": len(tracked_data),
            "output_video_path": output_video_path,
            "tracked_data": tracked_data
        }

    except Exception as e:
            print(e);
            return {"success": False, "message": str(e)}