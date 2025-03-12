import React, { useState } from "react";
import ReactPlayer from "react-player";
import Select from "react-select";
import axios from "axios"; // Import axios for API calls
import "./objectselection.css";
import { useEffect } from "react";
import { Navigate, useNavigate } from "react-router-dom"; // Import for navigation




const ObjectSelection = () => {
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [videoUrl, setVideoUrl] = useState(null);

  const navigate = useNavigate(); // Initialize navigation hook
    // this is a function that is calling a route that does not exist yet because i need the video, not the video path
  const getDetectedVideo = async () => {
    try {
        const response = await axios.get("http://127.0.0.1:5000/get_detected_video", { responseType: "blob" });
        const videoUrl = URL.createObjectURL(response.data);
        setVideoUrl(videoUrl);
    } catch (error) {
        console.error("Error fetching video:", error);
    }
};

//GET AVAIALBE ID'S API CALL

useEffect(() => {
    getDetectedVideo();
    //put the available id's api call in here as well
  }, []);





  const options = [
    { value: "1", label: "ID 1" },
    { value: "2", label: "Id 2" },
    { value: "3", label: "ID 3" },
    { value: "4", label: "ID 4" },
    { value: "5", label: "ID 5" },
    { value: "6", label: "ID 6" },
    { value: "7", label: "ID 7" },
    { value: "8", label: "ID 8" },
    { value: "9", label: "ID 9" },
    { value: "10", label: "ID 10" },
    { value: "11", label: "ID 11" },
    { value: "12", label: "ID 12" },
    { value: "13", label: "ID 13" },
    { value: "14", label: "ID 14" },
    { value: "15", label: "ID 15" },
    { value: "16", label: "ID 16" },
  ];

  const handleSubmit = async () => {

    if (!selectedOptions.length) {
      alert("Please select at least one object to encrypt.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("selected_ids", JSON.stringify(selectedOptions.map(option => option.value)));
      formData.append("method", "AES"); // Default to AES encryption (change if needed)

      // Send request to Flask backend
      const response = await axios.post("http://127.0.0.1:5000/encrypt", formData);

      if (response.data.success) {
        navigate("/videooutput");
        
      } else {
        alert("Encryption failed: " + response.data.message);
        
      }
    } catch (error) {
      console.error("Error sending data:", error);
      alert("An error occurred while encrypting the video.");
    }
  };

  return (
    <>
      <div className="object-selection-header">
        <h1>Object Selection</h1>
        <p>Select the objects you want to encrypt</p>
      </div>

      <div className="object-selection-container">
        {/* Video Player */}
        <div className="video-container">
          <ReactPlayer 
            url={videoUrl}
            controls 
            width="100%"
            height="550px"
          />
        </div>

        {/* Selector & Button */}
        <div className="selector-container">
          <Select
            options={options}
            value={selectedOptions}
            onChange={setSelectedOptions}
            placeholder="Select objects..."
            isMulti
            className="custom-select"
            styles={{
              control: (base) => ({ ...base, width: "200px", color: "black" }),
              singleValue: (base) => ({ ...base, color: "black" }),
              multiValueLabel: (base) => ({ ...base, color: "black" }),
              option: (base) => ({ ...base, color: "black" }),
            }}    
          />
          <button onClick={handleSubmit}>Next</button>
        </div>
      </div>
    </>
  );
};

export default ObjectSelection;




