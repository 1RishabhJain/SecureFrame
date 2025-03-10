import { Link } from "react-router-dom";
import React, { useState } from "react";
import "./upload.css";
import DragDropFiles from "../components/dragdrop/DragDropFiles";
import Textbox from "../components/textbox-encrypt/Textbox";

export function Upload() {
    const [videos, setVideos] = useState([]);
    const [videoDetails, setVideoDetails] = useState([]);

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

                // Ensure state updates after metadata is loaded for all videos
                if (details.length === files.length) {
                    setVideoDetails(details);
                }
            };
        });
    };

    return (
        <>
        <div className="top">
            <h1 className="title">Upload Your Video</h1>
            <Textbox></Textbox>
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
                    <Link className="next-button" to="/encrypt">NEXT</Link>
                </div>
            )}
        </div>
        </>
        
    );
}
