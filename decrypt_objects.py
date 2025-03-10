import numpy as np
from Crypto.Cipher import AES
from utilities.general_utilities import (
    log_progress,
    get_objects_in_frame,
    validate_coordinates,
)
from utilities.video_utilities import (
    open_video,
    get_frame_size,
    get_fps,
    get_video_writer,
)
from utilities.metadata_utilities import read_metadata
from numpy.random import default_rng

def generate_cipher(key_hex, nonce_hex):
    key = bytes.fromhex(key_hex)
    nonce = bytes.fromhex(nonce_hex)
    return AES.new(key, AES.MODE_CTR, nonce=nonce)

def decrypt_video(encrypted_video_path, decrypted_video_path, key_hex = None, nonce_hex = None):
    try:
        # Open video
        cap = open_video(encrypted_video_path)

        # Get video properties
        frame_width, frame_height = get_frame_size(cap)
        fps = get_fps(cap)

        # Video writer
        out = get_video_writer(
            decrypted_video_path, fps, frame_width, frame_height
        )
        # Read metadata from the video file
        metadata = read_metadata(encrypted_video_path)
        method = metadata["method"]
        selected_ids = metadata["selected_ids"]
        tracked_data = metadata["tracked_objects"]

        frame_index = 0

        if method == "AES":
            cipher = generate_cipher(key_hex, nonce_hex)
        elif method == "XOR":
            seed = 123456789
            rng = default_rng(seed)

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

                frame = decrypt_frame_data(frame, bounding_box, method, cipher if method == "AES" else None, rng if method == "XOR" else None)

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


def decrypt_frame_data(frame, bounding_box, method, cipher, rng):
    x1, y1, x2, y2 = bounding_box

    # Extract the region of interest
    frame_region = frame[y1:y2, x1:x2]

    if method == "AES":
        if not cipher:
            raise ValueError("AES decryption method selected, but cipher is not provided.")
        decrypted_frame_region = decrypt_aes(frame_region, cipher)
    elif method == "XOR":
        decrypted_frame_region = decrypt_xor(frame_region, rng)
    elif method == "overlay":
        decrypted_frame_region = decrypt_overlay(frame_region)
    else:
        raise ValueError(f"Unsupported encryption method: {method}")

    # Replace the original region with the encrypted region
    frame[y1:y2, x1:x2] = decrypted_frame_region

    return frame


def decrypt_aes(encrypted_frame_region, cipher):
    try:
        # Convert encrypted region to bytes
        encrypted_bytes = encrypted_frame_region.tobytes()

        # Perform decryption (CTR mode uses the same method for encryption and decryption)
        decrypted_bytes = cipher.decrypt(encrypted_bytes)

        # Convert decrypted bytes back to a NumPy array
        decrypted_frame_region = np.frombuffer(decrypted_bytes, dtype=np.uint8)

        # Ensure size matches the original frame region
        if decrypted_frame_region.size != encrypted_frame_region.size:
            raise ValueError(
                f"Decrypted data size mismatch: expected {encrypted_frame_region.size}, got {decrypted_frame_region.size}."
            )

        # Reshape to original bounding box shape
        decrypted_frame_region = decrypted_frame_region.reshape(encrypted_frame_region.shape)

        return decrypted_frame_region

    except Exception as e:
        raise RuntimeError(f"AES decryption failed: {str(e)}")

def decrypt_xor(frame_region, rng):
    mask = rng.integers(low=0, high=256, size=frame_region.shape, dtype=np.uint8)
    return frame_region ^ mask

def decrypt_overlay(frame_region):
    return frame_region
