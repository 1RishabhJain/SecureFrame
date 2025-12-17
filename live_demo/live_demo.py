from ultralytics import YOLO
from numpy.random import default_rng
import threading
import time
import cv2
from flask import Flask, render_template, Response, redirect, url_for, request

from webcam_demo_utilities import initialize_webcam, extract_tracking_results, encrypt_region

app = Flask(__name__)

# Initialize webcam capture
cap = initialize_webcam()

model = YOLO("yolov8n.pt")

flip_stream = False
global_original_frame = None
global_annotated_frame = None
global_encrypted_frame = None

# Generate RNG for XOR encryption
seed = 123456789
rng = default_rng(seed)

# Global list for objects to encrypt
selected_objects = []

def update_frames():
    """Capture a frame, run detection once, and update global frames."""
    global global_original_frame, global_annotated_frame, global_encrypted_frame, flip_stream
    while True:
        success, frame = cap.read()
        if not success:
            continue

        if flip_stream:
            frame = cv2.flip(frame, 1)

        # Store the base original frame
        global_original_frame = frame.copy()

        """
        # Run YOLO detection
        results = model.track(frame, persist=True, conf=0.5, verbose=False)
        
        # Create the annotated frame using detection results
        if results and results[0].boxes:
            annotated = results[0].plot()
        else:
            annotated = frame.copy()
        global_annotated_frame = annotated

        # Create the encrypted frame by starting with a copy of the original frame
        encrypted = frame.copy()
        frame_objects = extract_tracking_results(results, model)
        for obj in frame_objects:
            if obj["object_type"] in selected_objects:
                x1 = int(obj["bounding_box"]["x1"])
                y1 = int(obj["bounding_box"]["y1"])
                x2 = int(obj["bounding_box"]["x2"])
                y2 = int(obj["bounding_box"]["y2"])
                encrypted = encrypt_region(encrypted, x1, y1, x2, y2, rng)
        global_encrypted_frame = encrypted
        """
        
        time.sleep(0.03)

# Start the background thread to update frames
threading.Thread(target=update_frames, daemon=True).start()

def generate_stream(frame_getter):
    """Generator that yields JPEG-encoded frames.
    
    frame_getter: a callable that returns the current frame.
    """
    while True:
        frame = frame_getter()
        if frame is None:
            continue
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.05)

@app.route('/')
def index():
    """Render the main HTML page."""
    return render_template('index.html', flip=flip_stream, selected_objects=selected_objects)

@app.route('/video_feed/original')
def video_feed_original():
    print("hello")
    """Stream the original video."""
    return Response(generate_stream(lambda: global_original_frame),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed/annotated')
def video_feed_annotated():
    """Stream the annotated video."""
    return Response(generate_stream(lambda: global_annotated_frame),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed/encrypted')
def video_feed_encrypted():
    """Stream the encrypted video."""
    return Response(generate_stream(lambda: global_encrypted_frame),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/toggle_flip', methods=['POST'])
def toggle_flip():
    """Toggle the flip_stream flag and redirect back to the index page."""
    global flip_stream
    flip_stream = not flip_stream
    return redirect(url_for('index'))

@app.route('/update_objects', methods=['POST'])
def update_objects():
    """Update the selected objects list from checkboxes."""
    global selected_objects
    # Get list of object types from form; it returns an empty list if nothing is selected.
    selected_objects = request.form.getlist('objects')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)