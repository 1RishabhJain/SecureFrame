import { useNavigate } from "react-router-dom";
import React, { useState } from "react";
import "./upload.css";
import DragDropFiles from "../components/dragdrop/DragDropFiles";
import Textbox from "../components/textbox-encrypt/Textbox";
import { useEffect } from "react";

export function Upload() {
    const [videos, setVideos] = useState([]);
    const [videoDetails, setVideoDetails] = useState([]);
    const navigate = useNavigate(); // Hook for navigation
    const [loading, setLoading] = useState(false);
    const [dots, setDots] = useState("");


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

    

    // Function to handle video metadata extraction
    const handleVideos = (files) => {
        setVideos(files);
        const details = [];

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

                details.push({
                    name: file.name,
                    duration: formattedDuration,
                });

                if (details.length === files.length) {
                    setVideoDetails(details);
                }
            };
        });
    };

    // Function to send video to backend
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

        // videos.forEach((video, index) => {
        //     formData.append(`video${index}`, video);
        // });

        try {
            const response = await fetch("http://127.0.0.1:5000/detect", {
                method: "POST",
                body: formData,
            });

            const data = await response.json();
            if (data.success) {
                console.log("Video uploaded successfully:", data);

                //Store video path in localStorage
                localStorage.setItem("videoPath", data.output_video_path);
                navigate("/objectSelection");
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
                <Textbox />
            </div>
            <div className="dragdrop-page">
                <DragDropFiles setFiles={handleVideos} accepts="video/mp4,video/avi,video/mkv" />

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
                        {loading ? (
                            <p className="loading-text">Detecting Objects{dots}</p>
                        ) : (
                            <button className="next-button" onClick={handleNext}>NEXT</button>
                        )}
                    </div>
                )}
            </div>
        </>
    );
}
