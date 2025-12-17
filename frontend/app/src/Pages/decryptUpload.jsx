import { useNavigate } from "react-router-dom";
import React, { useState, useEffect } from "react";
import "./upload.css";
import DragDropFiles from "../components/dragdrop/DragDropFiles";
import axios from "axios";
export function DecryptUpload() {
    const [method, setMethod] = useState("")
    const [videos, setVideos] = useState([]);
    const [videoDetails, setVideoDetails] = useState([]);
    const [keyBox,setKeyBox] = useState(false);
    const navigate = useNavigate(); // Hook for navigation
    const [loading, setLoading] = useState(false);
    const [dots, setDots] = useState("");
    const [key, setKey] = useState("");  // Separate state for key
    const [nonce, setNonce] = useState("");  // Separate state for nonce

    useEffect(()=> {
        let interval;
        if (loading){
            interval = setInterval(()=>{
                setDots((prev) => (prev.length<3 ? prev +".":""));
            }, 500); // update every 500ms
        }else{
            setDots("");
        }
        return () => clearInterval(interval);
    }, [loading]);


     async function getMethod() {
        try {
            const response = await axios.get("http://localhost:5000/method");
            setMethod(response.data);
        } catch (error) {
            console.error("Error fetching method:", error);
        }
    }
    
    useEffect(() => {
        if (method === "AES") {
            setKeyBox(true);
        } else if (method === "XOR") {
            setKeyBox(false);
        }
    }, [method]);


    // Function to handle video metadata extraction
    const handleVideos = (files) => {
        setVideos(files);
        const details = [];
        getMethod();
        files.forEach((file) => {
            const videoURL = URL.createObjectURL(file);
            const video = document.createElement("video");

            video.src = videoURL;
            video.preload = "metadata"; // Preload metadata only

            video.onloadedmetadata = () => {
                const duration = video.duration;
                const minutes = Math.floor(duration / 60);
                const seconds = Math.floor(duration % 60);
                const formattedDuration = `${minutes}:${seconds < 10 ? "0" : ""}${seconds}`;
                if (method == "AES"){
                    setKeyBox(true)
                }else if (method == "XOR") {
                    setKeyBox(false)
                }

                details.push({
                    name: file.name,
                    duration: formattedDuration,
                });

                // Ensure state updates after metadata is loaded for all videos
                if (details.length === files.length) {
                    setVideoDetails(details);
                }
            };
        });
    };

    const handleNext = async () => {
        console.log("videos array", videos)
        console.log("video inside", videos[0])
        if (videos.length === 0) {
            alert("Please upload a video before proceeding.");
            return;
        }

        setLoading(true);


        const formData = new FormData();

        formData.append(`video`, videos[0])

        if (keyBox){
            formData.append(`decryptKey`, key)
            formData.append(`decryptNonce`, nonce)
        }

        try {
            const response = await fetch("http://127.0.0.1:5000/decrypt", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();
            if (data.success) {
                console.log("Video uploaded successfully:", data);
                navigate("/decrypt");
            } else {
                setLoading(false);
                alert("Upload failed:", data.message);
                console.error("Upload failed:", data.message);
            }
        } catch (error) {
            setLoading(false);
            alert("Error uploading video:",error);
            console.error("Error uploading video:", error);
        }
    };

    return (
        <>
        <div className="top">
            <h1 className="title">Upload Your Video</h1>
            {keyBox && 
            <>
                <div className="all-wrapper">
                <div className="text-wrapperD">
                    <input 
                        className="text"
                        onChange={(event) => setKey(event.target.value)}
                        value={key}
                        placeholder="Enter Decryption Key(s)"
                    />
                </div>
                <div className="text-wrapperD">   
                    <input 
                        className="text"
                        onChange={(event) => setNonce(event.target.value)}
                        value={nonce}
                        placeholder="Enter Decryption Nonce(s)"
                    />
                </div>
                <button className="btn" onClick={handleNext}>NEXT</button>
                </div>
            </>
            }
        </div>
        <div className="dragdrop-page">
            <DragDropFiles setFiles={handleVideos} accepts="video/mp4,video/avi,video/mkv" />

            {/* Display video name and duration */}
            {videoDetails.length > 0 && (
                <div className="video-info">
                    <h3>Uploaded Videos:</h3>
                    <ul>
                        {videoDetails.map((video, index) => (
                            <li key={index}>
                                <strong>{video.name}</strong> - {video.duration}
                            </li>
                        ))}
                    </ul>
                {!keyBox &&
                    (loading ? (
                        <p className="loading-text">Detecting Objects{dots}</p>
                    ) : (
                        <button className="next-button" onClick={handleNext}>NEXT</button>
                    ))
                }
                </div>
            )}
        </div>
        </>
        
    );
}