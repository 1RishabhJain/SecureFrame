import "./TextboxDecrypt.css"
import { useState } from "react";
import { useNavigate } from "react-router-dom";


function TextboxDecrypt() {
    const [key, setKey] = useState("");  // Separate state for key
    const [nonce, setNonce] = useState("");  // Separate state for nonce
    const navigate = useNavigate(); // Hook for navigation
    

    const clickNext = () => {
        alert(["key: ", key," nonce: ",nonce])
        navigate("/decrypt");
    }

    return (
        <div className="all-wrapper">
            <div className="text-wrapperD">
                <input 
                    className="text"
                    onChange={(event) => setKey(event.target.value)}
                    value={key}
                    placeholder="Enter Decryption Key(s)"
                />
            </div>
            <div className="text-wrapperD">   
                <input 
                    className="text"
                    onChange={(event) => setNonce(event.target.value)}
                    value={nonce}
                    placeholder="Enter Decryption Nonce(s)"
                />
            </div>
            <button className="btn" onClick={clickNext}>NEXT</button>
        </div>
    )
}

export default TextboxDecrypt;
