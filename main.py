import json
from detect_objects import detect_objects
from encrypt_video import encrypt_video
from decrypt_objects import decrypt_video

model_path = 'models/yolov8n.pt'
input_video_path = 'input/sample_video.avi'
tracked_data_path = 'output/tracked_objects.json'
tracked_video_path = 'output/tracked_video.avi'
encrypted_video_path = 'output/encrypted_video.avi'
decrypted_video_path = 'output/decrypted_video.avi'

"""
## you can comment out from here...
# Detect Objects
result_detect_objects = detect_objects(model_path, input_video_path, tracked_video_path, tracked_data_path)

if result_detect_objects["success"]:
    # Save the JSON file
    with open(tracked_data_path, 'w') as json_file: 
        json.dump(result_detect_objects["tracked_data"], json_file, indent=4)

    print(f"Tracked video saved at {result_detect_objects['output_video_path']}")
    print(f"Tracking data saved at {tracked_data_path}")
else:
    print(f"Error: {result_detect_objects['message']}")
## till here, to avoid it running detect objects each time during testing

"""
selected_ids = [1,2,5,11,9,3]

# Encrypt video
try:
    result_encrypt = encrypt_video(input_video_path, encrypted_video_path, tracked_data_path, selected_ids, method="AES")

    if result_encrypt["success"]:
        print(f"Encryption successful!")
        print(f"Encrypted video saved at: {result_encrypt['output_video_path']}")
        print(f"Total frames processed: {result_encrypt['total_frames_processed']}")
        print(f"Encryption method used: {result_encrypt['encryption_method']}")
       

except Exception as e:
    print(f"Error occurred during encryption: {str(e)}")



# Decrypt video
try:
    result_decrypt = decrypt_video(encrypted_video_path, decrypted_video_path, tracked_data_path, result_encrypt["key"], result_encrypt["iv"], result_encrypt["byteDifference"], selected_ids, method="AES")
    if result_decrypt["success"]:
        print(f"Decryption successful!")
        print(f"Decrypted video saved at: {result_decrypt['output_video_path']}")
        print(f"Total frames processed: {result_decrypt['total_frames_processed']}")
        print(f"Decryption method used: {result_decrypt['decryption_method']}")
    else:
        print(f"Decryption failed: {result_decrypt['message']}")

except Exception as e:
    print(f"Error occurred during decryption: {str(e)}")

   