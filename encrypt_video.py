import numpy as np
import os
from utilities.general_utilities import (
    log_progress,
    load_json_data,
    get_objects_in_frame,
    validate_coordinates,
)
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from utilities.video_utilities import (
    open_video,
    get_frame_size,
    get_fps,
    get_video_writer,
)
from utilities.metadata_utilities import write_metadata


int
def encrypt_video(
    input_video_path, encrypted_video_path, tracked_data_path, selected_ids, method
):
    try:
        tracked_data = load_json_data(tracked_data_path)

        # Open video
        cap = open_video(input_video_path)

        # Get video properties
        frame_width, frame_height = get_frame_size(cap)
        fps = get_fps(cap)

        # Video writer
        out = get_video_writer(
            encrypted_video_path, fps, frame_width, frame_height, "FFV1"
        )


        frame_index = 0
        key = os.urandom(16)
        iv = os.urandom(16)
        byteDifference = []
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
                
                
                frame = encrypt_frame_data(frame, bounding_box, method, key, iv, byteDifference, frame_index)

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
       
        return {
            "success": True,
            "message": "Encryption completed successfully.",
            "output_video_path": encrypted_video_path,
            "total_frames_processed": frame_index,
            "encryption_method": method,
            "byteDifference": byteDifference,
            "key": key,
            "iv": iv
        }

    except Exception as e:
        return {"success": False, "message": str(e)}


def encrypt_frame_data(frame, bounding_box, method, key, iv, byteDifference, frameIndex):
    x1, y1, x2, y2 = bounding_box

    # Extract the region of interest
    frame_region = frame[y1:y2, x1:x2]
    
    
    if method == "AES":
        encrypted_frame_region, data = encrypt_aes(frame_region, key, iv, frameIndex)
        byteDifference.append([frameIndex, data])
    elif method == "XOR":
        encrypted_frame_region = encrypt_xor(frame_region)
    elif method == "overlay":
        encrypted_frame_region = encrypt_overlay(frame_region)
    else:
        raise ValueError(f"Unsupported encryption method: {method}")

    # Replace the original region with the encrypted region
    frame[y1:y2, x1:x2] = encrypted_frame_region

    return frame


def encrypt_aes(frame_region, key, iv, frameIndex):
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()  # Create encryptor once for reuse

    block_data = frame_region.flatten()

    # Pad the block data to be a multiple of 16 bytes
    padder = padding.PKCS7(128).padder()
    padded_block_data = padder.update(block_data.tobytes()) + padder.finalize()
    
   
    # Encrypt the padded block
    encrypted_data = encryptor.update(padded_block_data)
    
    frame_region = np.frombuffer(encrypted_data, dtype=np.uint8)[:frame_region.size].reshape(frame_region.shape)
    
    bytesFramed = frame_region.tobytes();
    difference = len(encrypted_data) - len(bytesFramed);
    differenceBytes = encrypted_data[-difference:]
  
    """
   
    
     
      
       
   
    if (frameIndex == 0):
        with open('output.txt', 'w') as file:
          
            file.write(str(encrypted_data))
            print("run1")
        print(key)
        print(iv)
        print(len(encrypted_data))

    frame_region = np.frombuffer(encrypted_data, dtype=np.uint8)[:frame_region.size].reshape(frame_region.shape)
    
    decryptor = cipher.decryptor()
    bytesFramed += differenceBytes
    decrypted_bytes = decryptor.update(bytesFramed) + decryptor.finalize()
    if (frameIndex == 0):
        with open('outputDecrytpedSame.txt', 'w') as file:
          
            file.write(str(decrypted_bytes))
            print("run1")
        print(key)
        print(iv)
        print(len(encrypted_data))
    """
    
    
    """
    Encrypts the given frame_region using AES encryption.

    :param frame_region: Region of interest (NumPy array).
    :return: Encrypted frame_region (NumPy array).
    """
    # encrypted_data = cipher.encrypt(frame_region.tobytes())
    # return np.frombuffer(encrypted_data, dtype=frame_region.dtype).reshape(frame_region.shape)
    return frame_region, differenceBytes


def encrypt_xor(frame_region):
    """
    Encrypts the given frame_region using XOR encryption (bitwise inversion).

    :param frame_region: Region of interest (NumPy array).
    :return: Encrypted frame_region (NumPy array).
    """
    return frame_region


def encrypt_overlay(frame_region):
    """
    Applies a color overlay to obscure the region.

    :param frame_region: Region of interest (NumPy array).
    :return: Encrypted frame_region with an overlay.
    """
    ## get inputs for following from user:
    # overlay_color: The BGR color for the overlay
    # alpha: Transparency level (0 = fully transparent, 1 = solid color).

    return frame_region
