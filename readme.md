# SecureFrame Application

This project is built to run on **Python 3.11.5**.

## Requirements
- **Python**: Version 3.11.5
- **Virtual Environment**: Recommended to isolate dependencies

## Setup Instructions

### 1. Create a Virtual Environment
Open a terminal in the project directory and run:
```sh
python3.11 -m venv venv
```

### 2. Activate the Virtual Environment
- **On macOS/Linux:**
  ```sh
  source venv/bin/activate
  ```
- **On Windows (Command Prompt):**
  ```sh
  venv\Scripts\activate
  ```
- **On Windows (PowerShell):**
  ```sh
  .\venv\Scripts\Activate.ps1
  ```

### 3. Install Dependencies
Run:
```sh
pip install -r requirements.txt
```

### 4. Configure Your Project
Ensure the folder structure is correct and that the model, sample input video, etc., are in their respective folders.

### 5. Run the Application
Start the Flask server by running:
```sh
python server.py
```
You should see output similar to:
```
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

### 6. Open the Frontend Interface
Open your browser and navigate to:
```
http://127.0.0.1:5000/
```
From here, you can use the interface to run detection, encryption, and decryption.

## Usage Instructions

### Detection
- Use the file picker under the **“Detection”** section to select a video file and click **Start Detection**.
- This will process the video and generate tracking metadata.

### Encryption
- In the **“Video Encryption”** section, select a video file using the file picker.
- Enter the object IDs (comma-separated) and choose an encryption method (**AES, XOR, etc.**).
- Click **Start Encryption**.
- If using **AES**, the system will display the **AES key and nonce**—please save these securely for decryption.

### Decryption
- In the **“Video Decryption”** section, select the encrypted video file using the file picker.
- If the encryption method is **AES**, enter the key and nonce.
- Click **Start Decryption**.
- For other methods (e.g., **XOR**), the key and nonce fields can be left blank.

## Debugging
- Check the terminal (Flask console) for debug messages.
- Use the browser’s Developer Tools (**Console and Network** tabs) to inspect requests and responses.

## Shutting Down
To stop the application, press **CTRL+C** in the terminal where the Flask server is running.