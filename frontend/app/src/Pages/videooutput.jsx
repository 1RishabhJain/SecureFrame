import React, { useState } from "react";
import ReactPlayer from "react-player";
import "./videooutput.css";

const VideoOutput = () => {
    const [videoUrl, setVideoUrl] = useState(null); // Define video URL

    return (
      <div className="video-output-container">
        <h1>Video Output</h1>
        <div className="video-container">
            <ReactPlayer 
                url={videoUrl||"youtu.be/8DlU58Yi3Ww?si=aW31QL_ZAb4zRYoF"}
                controls 
                width="100%"
                height="550px"
            />
        </div>
      </div>
    );
};

export default VideoOutput;

  