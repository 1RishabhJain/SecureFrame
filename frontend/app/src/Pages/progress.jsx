import { Link, useNavigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import './progress.css'

// Renamed from Decrypt to Progress for clarity
export function Progress() {
    const [progress, setProgress] = useState(0);
    const [isComplete, setIsComplete] = useState(false);
    const [isPaused, setIsPaused] = useState(false);
    const navigate = useNavigate();


    //Api call to get the encrypted frames
    const getEncryptedFrames = async () => {
        try {
            const response = await axios.get("http://127.0.0.1:5000/encrypt", ) 
            if (response.data.success) {
                setIsComplete(true);
            }
        }
        catch (error) {
            console.error("Error fetching encrypted frames:", error);
        }
    }


    
    // Add animation for the progress bar
    useEffect(() => {
        let currentProgress = 0;
        const interval = setInterval(() => {
            if (!isPaused && currentProgress < 4) {
                currentProgress += 1;
                setProgress(currentProgress);
                
                // Check if encryption is complete
                if (currentProgress === 5) {
                    setIsComplete(true);
                }
            } else if (currentProgress >= 5) {
                clearInterval(interval);
            }
        }, 1500);
        
        return () => clearInterval(interval);
    }, [isPaused]);
    
    // Handle button clicks
    const handleBack = () => {
        navigate('/'); // Navigate back to home page
    };
    
    const handleNext = () => {
        if (isComplete) {
            navigate('/videooutput'); // Navigate to encryptor page when complete
        }
    };
    
    const togglePause = () => {
        setIsPaused(!isPaused);
    };
    
    return (
        <div className="progress-container">
            <h1 className="progress-title">{progress}/5 Objects Encrypted</h1>
            
            <div className="progress-bar-container">
                <div 
                    className="progress-bar" 
                    style={{width: `${(progress/5) * 100}%`}}
                >
                    <div className="progress-indicator"></div>
                </div>
            </div>
            
            <div className={`encryption-status ${isComplete ? 'complete' : ''}`}>
                {isComplete ? '✦ Encryption Complete ✦' : 'Encryption Ongoing...'}
            </div>
            
            <div className="purple-glow"></div>
            
            <div className="action-buttons">
                <button className="back-btn" onClick={handleBack}>
                    Back
                </button>
                <button 
                    className={`next-btn ${isComplete ? 'active' : ''}`} 
                    onClick={handleNext}
                    disabled={!isComplete}
                >
                    Next
                </button>
            </div>
        </div>
    )
}

// Also export with the original name for backward compatibility
export { Progress as Decrypt };