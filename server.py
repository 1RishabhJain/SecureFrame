from flask import Flask, request, jsonify
import json
from encrypt_video import encrypt_video
from decrypt_objects import decrypt_video
from detect_objects import detect_objects
import os

from flask_cors import CORS

from utilities.general_utilities import get_unique_track_ids, load_json_data
from utilities.metadata_utilities import read_metadata
app = Flask(__name__)
CORS(app,resources={"/*": {"origins": "http://localhost:5173"}})

model_path = 'models/yolov8n.pt'
tracked_data_path = "output/tracked_objects.json"
tracked_video_path = 'output/tracked_video.mp4'
encrypted_video_path = "output/encrypted_video.avi"
decrypted_video_path = "output/decrypted_video.avi"

# Temporary working directory for uploaded files
TEMP_FOLDER = "temp/"
if not os.path.exists(TEMP_FOLDER):
    os.makedirs(TEMP_FOLDER)


@app.route("/")
def serve_ui():
    """ Serve the frontend UI. """
    return app.send_static_file("index.html")


@app.route('/detect', methods=['POST'])
def detect_route():
    try:
        # Retrieve the uploaded file from request.files instead of JSON
        video_file = request.files.get("video")
        if not video_file:
            return jsonify({"success": False, "message": "No video file provided"}), 400

        # Save the uploaded file to the temporary working directory
        video_filename = video_file.filename
        input_video_path = os.path.join(TEMP_FOLDER, video_filename)
        video_file.save(input_video_path)

        # Run detection on the copied video file
        result_detect = detect_objects(model_path, input_video_path, tracked_video_path, tracked_data_path)
        
        if result_detect["success"]:
            return jsonify({
                "success": True,
                "message": "Detection successful!",
                "output_video_path": result_detect["output_video_path"],
                "total_frames_processed": result_detect["total_frames_processed"]
            })
        else:
            return jsonify({"success": False, "message": result_detect["message"]}), 500
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


@app.route('/encrypt', methods=['POST'])
def encrypt():
    try:
        print("DEBUG: /encrypt endpoint called.")  # Debug line
        
        # Retrieve other fields from request.form
        selected_ids_str = request.form.get("selected_ids")
        encryption_method = request.form.get("method")
        
        print(f"DEBUG: selected_ids_str = {selected_ids_str}, method = {encryption_method}")
        
        # if not video_file:
        #     return jsonify({
        #         "success": False,
        #         "message": "No video file provided",
        #         "debug_info": "File missing in request.files"
        #     }), 400

        if not selected_ids_str:
            return jsonify({
                "success": False,
                "message": "No object IDs provided",
                "debug_info": "selected_ids not found in request.form"
            }), 400

        # Convert selected_ids from JSON string to Python list
        try:
            selected_ids = json.loads(selected_ids_str)
        except json.JSONDecodeError as e:
            return jsonify({
                "success": False,
                "message": "Invalid selected_ids format",
                "debug_info": str(e)
            }), 400

        # # Save file to a temporary directory
        # video_filename = video_file.filename
        # saved_video_path = os.path.join("temp", video_filename)
        # print(f"DEBUG: Saving uploaded file to {saved_video_path}")
        # video_file.save(saved_video_path)

        saved_video_path = "./output/tracked_video.mp4"

        # Call encrypt_video
        print(f"DEBUG: Calling encrypt_video with {saved_video_path}, {selected_ids}, method={encryption_method}")
        result_encrypt = encrypt_video(
            saved_video_path,
            encrypted_video_path,
            tracked_data_path,
            selected_ids,
            method=encryption_method
        )
        print(f"DEBUG: encrypt_video result: {result_encrypt}")

        if result_encrypt["success"]:
            response = {
                "success": True,
                "message": "Encryption successful!",
                "output_video_path": result_encrypt["output_video_path"],
                "total_frames_processed": result_encrypt["total_frames_processed"],
                "encryption_method": result_encrypt["encryption_method"]
            }
            # If AES add key/nonce
            if encryption_method and encryption_method.upper() == "AES":
                if "key" in result_encrypt:
                    response["key"] = result_encrypt["key"]
                if "nonce" in result_encrypt:
                    response["nonce"] = result_encrypt["nonce"]
            return jsonify(response)
        else:
            return jsonify({
                "success": False,
                "message": "Encryption failed",
                "debug_info": result_encrypt.get("message", "No error message provided by encrypt_video")
            }), 500

    except Exception as e:
        # Print traceback to the console
        import traceback
        traceback.print_exc()

        # Return debug info in JSON
        return jsonify({
            "success": False,
            "message": str(e),
            "debug_info": "See server console for full traceback"
        }), 500
    

@app.route('/decrypt', methods=['POST'])
def decrypt():
    try:
        print("DEBUG: /decrypt endpoint called.")
        # Retrieve the uploaded file from FormData ---
        video_file = request.files.get("video")
        if video_file:
            print(f"DEBUG: Received file: {video_file.filename}")
        else:
            print("DEBUG: No file found in request.files['video']")

        # Retrieve other fields from request.form ---
        key_hex = request.form.get("decryptKey", "")
        nonce_hex = request.form.get("decryptNonce", "")

        if not video_file:
            return jsonify({
                "success": False,
                "message": "No video file provided",
                "debug_info": "File missing in request.files"
            }), 400
    
        # Save the file to a temporary directory for local processing ---
        video_filename = video_file.filename
        encrypted_video_path = os.path.join(TEMP_FOLDER, video_filename)
        print(f"DEBUG: Saving uploaded file to {encrypted_video_path}")
        video_file.save(encrypted_video_path)

        # Call decrypt_video using the saved file
        print(f"DEBUG: Calling decrypt_video with {encrypted_video_path}, key {key_hex}, and nonce {nonce_hex}")
        result_decrypt = decrypt_video(encrypted_video_path, decrypted_video_path, key_hex, nonce_hex)
        print(f"DEBUG: decrypt_video result: {result_decrypt}")

        if result_decrypt["success"]:
            return jsonify({
                "success": True,
                "message": "Decryption successful!",
                "output_video_path": result_decrypt["output_video_path"],
                "total_frames_processed": result_decrypt["total_frames_processed"],
                "decryption_method": result_decrypt["decryption_method"]
            })
        else:
            return jsonify({
                "success": False,
                "message": "Decryption failed",
                "debug_info": result_decrypt.get("message", "No error message provided by decrypt_video")
            }), 500

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "message": str(e),
            "debug_info": "See server console for full traceback"
        }), 500

@app.route('/ids/encrypt', methods = ['GET'])
def getIds(): 
    tracked_data = load_json_data('./output/tracked_objects.json')
    data = get_unique_track_ids(tracked_data)
    return jsonify(data)

@app.route('/ids/decrypt', methods = ['GET'])
def getIdsDecrypt(): 
    try:
        metadata = read_metadata("")
        selected_ids = metadata["selected_ids"]
        return jsonify(selected_ids)
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e),
            "debug_info": "See server console for full traceback"
        }), 500

 
@app.route('/method', methods = ['GET']) 
def getMethod(): 
    try:
        metadata = read_metadata("")
        method = metadata['method']
        return jsonify(method)
    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e),
            "debug_info": "See server console for full traceback"
        }), 500

if __name__ == '__main__':
    app.run(debug=True)