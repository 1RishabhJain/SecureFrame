import React, { useState } from "react";
import ReactPlayer from "react-player";
import Select from "react-select";
import axios from "axios"; // Import axios for API calls
import "./objectselection.css";
import { useEffect } from "react";
import { Navigate, useNavigate } from "react-router-dom"; // Import for navigation


const VideoOutput = () => {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen bg-gray-900 text-white">
        <h1 className="text-2xl font-bold mb-4">Video Output</h1>
        <video controls className="w-3/4 max-w-2xl rounded-lg shadow-lg">
          <source src="" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>
    );
  };
  
  export default VideoOutput;
  