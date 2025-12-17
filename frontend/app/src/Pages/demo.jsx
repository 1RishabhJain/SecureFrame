import { useState, useEffect } from 'react';
import './demo.css';

function Demo() {
  const [selectedObjects, setSelectedObjects] = useState([]);
  const [flip, setFlip] = useState(false);
  const availableObjects = ["person", "cell phone", "phone", "paper"];

  // Function to update selected objects on the backend
  const updateBackendObjects = async (objects) => {
    try {
      const formData = new FormData();
      objects.forEach(obj => {
        formData.append('objects', obj);
      });
      
      await fetch('http://localhost:5000/update_objects', {
        method: 'POST',
        body: formData
      });
    } catch (error) {
      console.error('Error updating objects:', error);
    }
  };

  // Function to toggle flip on the backend
  const toggleFlip = async () => {
    try {
      await fetch('http://localhost:5000/toggle_flip', {
        method: 'POST'
      });
      setFlip(!flip);
    } catch (error) {
      console.error('Error toggling flip:', error);
    }
  };

  // Toggle object selection
  const toggleObject = (object) => {
    const newSelectedObjects = selectedObjects.includes(object)
      ? selectedObjects.filter(obj => obj !== object)
      : [...selectedObjects, object];
    
    setSelectedObjects(newSelectedObjects);
    updateBackendObjects(newSelectedObjects);
  };

  return (
    <div className="demo-container">
      <h1>Webcam Streams</h1>
      
      <div className="streams-container">
        <div className="stream">
          <h3>Original Video</h3>
          <img src="http://localhost:5000/video_feed/original" alt="Original Video" />
        </div>
        <div className="stream">
          <h3>Annotated Video</h3>
          <img src="http://localhost:5000/video_feed/annotated" alt="Annotated Video" />
        </div>
        <div className="stream">
          <h3>Encrypted Video</h3>
          <img src="http://localhost:5000/video_feed/encrypted" alt="Encrypted Video" />
        </div>
      </div>
      
      {/* Toggle flip button */}
      <div className="controls">
        <button onClick={toggleFlip}>Toggle Flip</button>
        <p>Flip is currently: {flip ? 'On' : 'Off'}</p>
      </div>
      
      {/* Object selection section */}
      <div className="object-selection">
        <h3>Select Objects to Encrypt:</h3>
        <div className="checklist-container">
          {availableObjects.map(obj => (
            <label key={obj} className="checkbox-label">
              <input
                type="checkbox"
                checked={selectedObjects.includes(obj)}
                onChange={() => toggleObject(obj)}
                value={obj}
              />
              {obj.charAt(0).toUpperCase() + obj.slice(1)}
            </label>
          ))}
        </div>
        <p>Currently encrypting: {selectedObjects.length > 0 ? selectedObjects.join(', ') : "None"}</p>
      </div>
    </div>
  );
}

export default Demo;