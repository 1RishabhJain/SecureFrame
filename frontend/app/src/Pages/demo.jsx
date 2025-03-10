import { useState, useEffect, useRef } from 'react';
import './demo.css';

function Demo() {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);
  const [selectedObjects, setSelectedObjects] = useState({
    person: false,
    alert: true, // Default selected
    car: false
  });
  
  // Initialize webcam
  useEffect(() => {
    const startWebcam = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
          video: { width: 640, height: 480 } 
        });
        
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
          
          // When video is playing, copy to canvas
          videoRef.current.onloadedmetadata = () => {
            videoRef.current.play();
            
            // Set canvas dimensions
            if (canvasRef.current) {
              canvasRef.current.width = videoRef.current.videoWidth;
              canvasRef.current.height = videoRef.current.videoHeight;
              
              // Copy video to canvas
              const ctx = canvasRef.current.getContext('2d');
              const drawFrame = () => {
                if (videoRef.current && canvasRef.current) {
                  ctx.drawImage(videoRef.current, 0, 0, canvasRef.current.width, canvasRef.current.height);
                }
                requestAnimationFrame(drawFrame);
              };
              
              drawFrame();
            }
          };
        }
      } catch (err) {
        console.error("Error accessing webcam:", err);
      }
    };
    
    startWebcam();
    
    // Cleanup function to stop webcam when component unmounts
    return () => {
      if (videoRef.current && videoRef.current.srcObject) {
        const tracks = videoRef.current.srcObject.getTracks();
        tracks.forEach(track => track.stop());
      }
    };
  }, []);
  
  // Toggle object selection
  const toggleObject = (object) => {
    setSelectedObjects({
      ...selectedObjects,
      [object]: !selectedObjects[object]
    });
  };
  
  return (
    <div className="demo-container">
      <h1 className="demo-title">Live Demo</h1>
      
      <div className="webcam-container">
        <div className="webcam-box">
          <h2 className="webcam-title">Object Detection</h2>
          <div className="webcam-frame">
            <video 
              ref={videoRef} 
              autoPlay 
              playsInline 
              muted
            />
            <div className="detection-overlay">
              {/* Simulated detection boxes */}
              <div className="detection-box" style={{top: '20%', left: '30%', width: '15%', height: '20%'}}></div>
              <div className="detection-box" style={{top: '40%', left: '60%', width: '20%', height: '15%'}}></div>
              <div className="detection-box" style={{top: '60%', left: '20%', width: '25%', height: '15%'}}></div>
            </div>
          </div>
        </div>
        
        <div className="webcam-box">
          <h2 className="webcam-title">Object Encryption</h2>
          <div className="webcam-frame">
            <canvas ref={canvasRef} />
            <div className="encryption-overlay">
              {/* Simulated encryption effects */}
              <div className="encryption-box" style={{top: '20%', left: '30%', width: '15%', height: '20%'}}></div>
              <div className="encryption-box" style={{top: '40%', left: '60%', width: '20%', height: '15%'}}></div>
              <div className="encryption-box" style={{top: '60%', left: '20%', width: '25%', height: '15%'}}></div>
            </div>
          </div>
        </div>
      </div>
      
      {/* Object selection section */}
      <div className="object-selection-container">
        <div className="object-selection-label">Select Objects to Encrypt:</div>
        <div className="object-selection-buttons">
          <button 
            className={`object-button ${selectedObjects.alert ? 'selected' : ''}`}
            onClick={() => toggleObject('alert')}
          >
            {/* Alert icon SVG */}
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 22C6.477 22 2 17.523 2 12C2 6.477 6.477 2 12 2C17.523 2 22 6.477 22 12C22 17.523 17.523 22 12 22ZM12 20C16.418 20 20 16.418 20 12C20 7.582 16.418 4 12 4C7.582 4 4 7.582 4 12C4 16.418 7.582 20 12 20ZM11 15H13V17H11V15ZM11 7H13V13H11V7Z" fill="white"/>
            </svg>
          </button>
          <button 
            className={`object-button ${selectedObjects.car ? 'selected' : ''}`}
            onClick={() => toggleObject('car')}
          >
            {/* Car icon SVG */}
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 20H5V21C5 21.5523 4.55228 22 4 22H3C2.44772 22 2 21.5523 2 21V12L4.5 5C4.77679 4.37584 5.29988 4 6 4H18C18.7001 4 19.2232 4.37584 19.5 5L22 12V21C22 21.5523 21.5523 22 21 22H20C19.4477 22 19 21.5523 19 21V20ZM20 13H4V18H20V13ZM4.76 11H19.24L17.5 6H6.5L4.76 11ZM6.5 14C7.32843 14 8 14.6716 8 15.5C8 16.3284 7.32843 17 6.5 17C5.67157 17 5 16.3284 5 15.5C5 14.6716 5.67157 14 6.5 14ZM17.5 14C18.3284 14 19 14.6716 19 15.5C19 16.3284 18.3284 17 17.5 17C16.6716 17 16 16.3284 16 15.5C16 14.6716 16.6716 14 17.5 14Z" fill="white"/>
            </svg>
          </button>
          <button 
            className={`object-button ${selectedObjects.person ? 'selected' : ''}`}
            onClick={() => toggleObject('person')}
          >
            {/* Person icon SVG */}
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M12 2C9.79086 2 8 3.79086 8 6C8 8.20914 9.79086 10 12 10C14.2091 10 16 8.20914 16 6C16 3.79086 14.2091 2 12 2ZM10 6C10 4.89543 10.8954 4 12 4C13.1046 4 14 4.89543 14 6C14 7.10457 13.1046 8 12 8C10.8954 8 10 7.10457 10 6ZM4 20C4 17.6324 6.4686 14 12 14C17.5314 14 20 17.6324 20 20V22H4V20ZM6 20H18C18 18.4023 16.5314 16 12 16C7.4686 16 6 18.4023 6 20Z" fill="white"/>
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}

export default Demo;
