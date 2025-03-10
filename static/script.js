function startDetection() {
    const fileInput = document.getElementById("videoFile");
    const file = fileInput.files[0];
    if (!file) {
        document.getElementById("status").innerText = "Please select a video file.";
        return;
    }
    
    let formData = new FormData();
    formData.append("video", file);

    document.getElementById("status").innerText = "Detection in progress...";

    fetch("http://127.0.0.1:5000/detect", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("status").innerText = "Detection successful! Tracked video saved at: " + data.output_video_path;
        } else {
            document.getElementById("status").innerText = "Error: " + data.message;
        }
    })
    .catch(error => {
        document.getElementById("status").innerText = "Failed to start detection.";
        console.error("Detection error:", error);
    });
}


function startEncryption() {
    const fileInput = document.getElementById("encryptVideoFile");
    const file = fileInput.files[0];
    if (!file) {
        document.getElementById("status").innerText = "Please select a video file.";
        return;
    }
    const objectIds = document.getElementById("objectIds").value.split(",").map(id => parseInt(id.trim()));
    const encryptionMethod = document.getElementById("encryptionMethod").value;

    let formData = new FormData();
    formData.append("video", file);
    formData.append("selected_ids", JSON.stringify(objectIds)); 
    formData.append("method", encryptionMethod);

    document.getElementById("status").innerText = "Encryption in progress...";

    fetch("http://127.0.0.1:5000/encrypt", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            let msg = "Encryption successful! Video saved at: " + data.output_video_path;
            // If AES, show the key and nonce
            if (encryptionMethod.toUpperCase() === "AES" && data.key && data.nonce) {
                msg += "\nPlease save this key: " + data.key + "\nand nonce: " + data.nonce;
            }
            document.getElementById("status").innerText = msg;
        } else {
            document.getElementById("status").innerText = "Error: " + data.message;
        }
    })
    .catch(error => {
        document.getElementById("status").innerText = "Failed to start encryption.";
        console.error("Encryption error:", error);
    });

    // Debug log
    console.log("Sending encryption request with object IDs:", objectIds, "method:", encryptionMethod);
}

function startDecryption() {
    const fileInput = document.getElementById("decryptVideoFile");
    const file = fileInput.files[0];
    if (!file) {
        document.getElementById("status").innerText = "Please select a video file.";
        return;
    }

    const key = document.getElementById("decryptKey").value.trim();
    const nonce = document.getElementById("decryptNonce").value.trim();

    let formData = new FormData();
    formData.append("video", file);
    if (key !== "" && nonce !== "") {
        formData.append("decryptKey", key);
        formData.append("decryptNonce", nonce);
    }

    document.getElementById("status").innerText = "Decryption in progress...";

    fetch("http://127.0.0.1:5000/decrypt", { 
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            document.getElementById("status").innerText = "Decryption successful! Video saved at: " + data.output_video_path;
        } else {
            document.getElementById("status").innerText = "Error: " + data.message;
        }
    })
    .catch(error => {
        document.getElementById("status").innerText = "Failed to start decryption.";
        console.error("Decryption error:", error);
    });
    
    console.log("Sending decryption request with key:", key, "and nonce:", nonce);
}