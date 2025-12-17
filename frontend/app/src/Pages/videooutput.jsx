import React, { useState,useEffect } from "react";
import ReactPlayer from "react-player";
import "./videooutput.css";

const VideoOutput = () => {
    const [videoUrl, setVideoUrl] = useState("/videos/encrypted_video.mp4");
    const [showPopup, setShowPopup] = useState(false);
    const [isCopied, setIsCopied] = useState(false);
    const [key, setKey] = useState();
    const [nonce, setNonce] = useState();

    useEffect(() => {
        setKey(localStorage.getItem("key") || "No key found");
        setNonce(localStorage.getItem("nonce") || "No nonce found");
    }, []);

    const handleDecryptionKeyClick = () => {
        setShowPopup(true);
    };

    const closePopup = () => {
        setShowPopup(false);
    };

    const handleCopyClick = async () => {
        try {
            await navigator.clipboard.writeText("http://bit.ly/sec1234");
            setIsCopied(true);
            setTimeout(() => setIsCopied(false), 2000);
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
    };

    return (
      <div className="video-output-container">
        <h1>Video Output</h1>
        
        <div className="content-wrapper">
            <div className="video-container">
                <ReactPlayer 
                    url={videoUrl}
                    controls={true}
                    width="100%"
                    height="100%"
                    playing={false}
                    light={false}
                    pip={true}
                    style={{ position: 'absolute', top: 0, left: 0 }}
                    config={{
                        youtube: {
                            playerVars: {
                                modestbranding: 1,
                                controls: 1,
                                rel: 0
                            }
                        }
                    }}
                />
            </div>

            <div className="download-section">
                <button 
                    className="decryption-key-btn"
                    onClick={handleDecryptionKeyClick}
                >
                    Decryption Key Package
                    <i className="fas fa-download"></i>
                </button>

                <h2>DOWNLOAD & SHARE</h2>
                
                <div className="share-link-container">
                    <input 
                        type="text" 
                        className="share-link" 
                        value="http://bit.ly/sec1234" 
                        readOnly 
                    />
                    <button 
                        className={`copy-link-btn ${isCopied ? 'copied' : ''}`}
                        onClick={handleCopyClick}
                    >
                        <i className={`fas ${isCopied ? 'fa-check' : 'fa-link'}`}></i>
                    </button>
                </div>

                <div className="social-icons">
                    <button className="social-icon twitter">
                        <i className="fab fa-twitter"></i>
                    </button>
                    <button className="social-icon facebook">
                        <i className="fab fa-facebook-f"></i>
                    </button>
                    <button className="social-icon instagram">
                        <i className="fab fa-instagram"></i>
                    </button>
                    <button className="social-icon linkedin">
                        <i className="fab fa-linkedin-in"></i>
                    </button>
                </div>
            </div>
        </div>

        {showPopup && (
            <div className="popup-overlay">
                <div className="popup-content">
                    <button className="popup-close" onClick={closePopup}>
                        <i className="fas fa-times"></i>
                    </button>
                    <h3>
                        <i className="fas fa-key"></i>
                        Decryption Key Package
                    </h3>
                    <div className="key-info">
                        <p><strong>Key:</strong> {key}</p>
                        <p><strong>Nonce:</strong> {nonce}</p>
                    </div>
                </div>
            </div>
        )}
      </div>
    );
};

export default VideoOutput;

  