import React, { useState } from "react";
import ReactPlayer from "react-player";
import Select from "react-select";
import axios from "axios"; // Import axios for API calls
import "./objectselection.css";
import { useEffect } from "react";
import { Navigate, useNavigate } from "react-router-dom"; // Import for navigation


const ObjectSelection = () => {
  const [options, setOptions] = useState([]);
  const [selectedOptions, setSelectedOptions] = useState([]);
  const [videoUrl, setVideoUrl] = useState(null);

  const navigate = useNavigate(); // Initialize navigation hook
    // this is a function that is calling a route that does not exist yet because i need the video, not the video path
  const getDetectedVideo = () => {
    const storedVideoPath = localStorage.getItem("videoPath");
    if (storedVideoPath) {
      setVideoUrl(storedVideoPath);
    }
  };

  const getAvailableIds = async () => {
    try {
        const response = await axios.get("http://127.0.0.1:5000/ids/encrypt", )
        const formattedOptions = response.data.map(id => ({
          value: id,
          label: `ID ${id}`
        }));
        setOptions(formattedOptions); //  Store options in state
    }
    catch (error) {
    console.error("Error fetching available IDs:", error);
    }
  };

  //GET AVAIALBE ID'S API CALL

  useEffect(() => {
    getDetectedVideo();
    getAvailableIds();
    console.log("here")
    //put the available id's api call in here as well
  }, []);

  const handleSubmit = async () => {

    if (!selectedOptions.length) {
      alert("Please select at least one object to encrypt.");
      return;
    }

    navigate("/progress");

    try {
      const formData = new FormData();
      formData.append("selected_ids", JSON.stringify(selectedOptions.map(option => option.value)));
      formData.append("method", "AES"); // Default to AES encryption (change if needed)

      // Send request to Flask backend
      const response = await axios.post("http://127.0.0.1:5000/encrypt", formData);

      if (response.data.success) {
        if (response.data.encryption_method == "AES"){
          localStorage.setItem("key", response.data.key);
          localStorage.setItem("nonce", response.data.nonce);
          console.log(response.data)
        }
         // Navigate to videooutput page
        
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
            className="video"
            url={videoUrl}
            controls
            height="100%"
            width="100%"
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
          <button className = "next-button" onClick={handleSubmit}>Next</button>
        </div>
      </div>
    </>
  );
};

export default ObjectSelection;