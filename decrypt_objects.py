import sys
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from utilities.general_utilities import (
    log_progress,
    get_objects_in_frame,
    validate_coordinates,
    load_json_data
)
from utilities.video_utilities import (
    open_video,
    get_frame_size,
    get_fps,
    get_video_writer,
)
from utilities.metadata_utilities import read_metadata





def decrypt_video(encrypted_video_path, decrypted_video_path, tracked_data_path, key, iv, byteDifference, selected_ids, method):
    print("test")
    try:
        # Open video
        cap = open_video(encrypted_video_path)

        # Get video properties
        frame_width, frame_height = get_frame_size(cap)
        fps = get_fps(cap)

        # Video writer
        out = get_video_writer(
            decrypted_video_path, fps, frame_width, frame_height, "FFV1"
        )

        
        # Read metadata from the video file

        
        
        
        print(method)
        tracked_data = load_json_data(tracked_data_path)

        frame_index = 0
        # Iterate through frames
        while True:
            read_successful, frame = cap.read()
            if not read_successful:
                break
            
            objects_in_frame = get_objects_in_frame(
                tracked_data, frame_index, selected_ids
            )

            for object_data in objects_in_frame:
                track_id = object_data["track_id"]
                coordinates = object_data["bounding_box"]

                # Validate bounding box before encryption
                try:
                    bounding_box = validate_coordinates(frame, coordinates)
                except ValueError as e:
                    print(
                        f"Skipping object {track_id} due to invalid bounding box: {e}"
                    )
                    continue

                frame = decrypt_frame_data(frame, bounding_box, method, key, iv, byteDifference, frame_index)

            out.write(frame)
            frame_index += 1
            log_progress(frame_index)

        cap.release()
        out.release()

        return {
            "success": True,
            "message": "Decryption completed successfully.",
            "output_video_path": decrypted_video_path,
            "total_frames_processed": frame_index,
            "decryption_method": method,
        }

    except Exception as e:
        return {"success": False, "message": str(e)}


def decrypt_frame_data(frame, bounding_box, method, key, iv, byteDifference, frameIndex):
    x1, y1, x2, y2 = bounding_box

    # Extract the region of interest
    frame_region = frame[y1:y2, x1:x2] 


    if method == "AES":
        decrypted_frame_region = decrypt_aes(frame_region, key, iv, byteDifference, frameIndex)
    elif method == "XOR":
        decrypted_frame_region = decrypt_xor(frame_region)
    elif method == "overlay":
        decrypted_frame_region = decrypt_overlay(frame_region)
    else:
        raise ValueError(f"Unsupported encryption method: {method}")

    # Replace the original region with the encrypted region
    frame[y1:y2, x1:x2] = decrypted_frame_region

    return frame


def decrypt_aes(frame_region, key, iv, byteDifference, frameIndex):
    if (byteDifference[0][0] == frameIndex):
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        data = byteDifference.pop(0)
        bytes = frame_region.tobytes();
        byteDifference = bytes + data[1]
        
        decrypted_bytes = decryptor.update(byteDifference) + decryptor.finalize()
        frame_region = np.frombuffer(decrypted_bytes, dtype=np.uint8)[:frame_region.size].reshape(frame_region.shape)
    return frame_region

def decrypt_xor(frame_region):
    return frame_region


def decrypt_overlay(frame_region):
    return frame_region
