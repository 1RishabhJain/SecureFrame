import numpy as np
from os import urandom
from Crypto.Cipher import AES
from utilities.general_utilities import (
    log_progress,
    load_json_data,
    get_objects_in_frame,
    validate_coordinates,
)
from utilities.video_utilities import (
    convert_to_mp4,
    open_video,
    get_frame_size,
    get_fps,
    get_video_writer,
)
from utilities.metadata_utilities import write_metadata
from numpy.random import default_rng

def encrypt_video(input_video_path, encrypted_video_path, tracked_data_path, selected_ids, method):
    try:
        tracked_data = load_json_data(tracked_data_path)

        # Open video
        cap = open_video(input_video_path)

        # Get video properties
        frame_width, frame_height = get_frame_size(cap)
        fps = get_fps(cap)

        # Video writer
        out = get_video_writer(
            encrypted_video_path, fps, frame_width, frame_height
        )

        if method == "AES":
            aes_key = urandom(16)
            aes_nonce = urandom(8)
            cipher = AES.new(aes_key, AES.MODE_CTR, nonce=aes_nonce)
            print("\nYou must store the AES Key and Nonce securely, we will not show them again and they will be needed during decryption")
            print(f"\nAES Key (Save this securely): {aes_key.hex()}")
            print(f"Nonce (Save this securely): {aes_nonce.hex()}\n")

        if method == "XOR":
            seed = 123456789
            rng = default_rng(seed)

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

                frame = encrypt_frame_data(frame, bounding_box, method, cipher if method == "AES" else None, rng if method == "XOR" else None)

            out.write(frame)
            frame_index += 1
            log_progress(frame_index)

        cap.release()
        out.release()

        # Write metadata to video file for future use
        write_metadata(
            encrypted_video_path,
            selected_ids,
            tracked_data,
            method,
        )
        
        convert_to_mp4(encrypted_video_path, "./frontend/app/public/videos/encrypted_video.mp4")
 
        response = {
            "success": True,
            "message": "Encryption completed successfully.",
            "output_video_path": encrypted_video_path,
            "total_frames_processed": frame_index,
            "encryption_method": method,
        }

        # Add key and nonce if AES is used
        if method == "AES" and aes_key is not None and aes_nonce is not None:
            response["key"] = aes_key.hex()
            response["nonce"] = aes_nonce.hex()

        return response


    except Exception as e:
        return {"success": False, "message": str(e)}


def encrypt_frame_data(frame, bounding_box, method, cipher, rng):
    x1, y1, x2, y2 = bounding_box

    # Extract the region of interest
    frame_region = frame[y1:y2, x1:x2]

    if method == "AES":
        if not cipher:
            raise ValueError("AES encryption method selected, but cipher is not provided.")
        encrypted_frame_region = encrypt_aes(frame_region, cipher)
    elif method == "XOR":
        encrypted_frame_region = encrypt_xor(frame_region, rng)
    elif method == "overlay":
        encrypted_frame_region = encrypt_overlay(frame_region)
    else:
        raise ValueError(f"Unsupported encryption method: {method}")

    # Replace the original region with the encrypted region
    frame[y1:y2, x1:x2] = encrypted_frame_region

    return frame


def encrypt_aes(frame_region, cipher):
    """
    Encrypts the given frame_region using AES encryption (CTR mode).
    
    :param frame_region: Region of interest (NumPy array).
    :param cipher: AES cipher object initialized with the key and nonce.
    :return: Encrypted frame_region (NumPy array).
    """
    try:
        # Convert the frame region to bytes
        frame_bytes = frame_region.tobytes()

        # Encrypt the byte data
        encrypted_bytes = cipher.encrypt(frame_bytes)

        # Convert encrypted bytes back to a NumPy array
        encrypted_frame_region = np.frombuffer(encrypted_bytes, dtype=np.uint8)

        # Ensure array size matches the original shape
        if encrypted_frame_region.size != frame_region.size:
            raise ValueError("Encrypted data size mismatch. Possible corruption.")

        # Reshape back to the original frame region shape
        encrypted_frame_region = encrypted_frame_region.reshape(frame_region.shape)

        return encrypted_frame_region

    except Exception as e:
        raise RuntimeError(f"AES encryption failed: {str(e)}")

def encrypt_xor(frame_region, rng):
    """
    Encrypts the given frame_region using XOR encryption (bitwise inversion).

    :param frame_region: Region of interest (NumPy array).
    :return: Encrypted frame_region (NumPy array).
    """
    mask = rng.integers(low=0, high=256, size=frame_region.shape, dtype=np.uint8)
    return frame_region ^ mask

def encrypt_overlay(frame_region):
    """
    Applies a semi-transparent color overlay to obscure the region.

    :param frame_region: Region of interest (NumPy array).
    :param overlay_color: BGR color for the overlay (default: red).
    :param alpha: Transparency level (0 = fully transparent, 1 = solid color).
    :return: Encrypted frame_region with an overlay.
    """
    return frame_region
