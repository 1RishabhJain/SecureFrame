import "./TextboxDecrypt.css"
import { useState } from "react";

function TextboxDecrypt() {
    const [val, setVal] = useState("");
    const clickLPR = () => {
        alert([val,"LPR Video"])
    }

    const clickCCTV = () => {
        alert([val,"CCTV"])
    }

    const change = event => { 
        setVal(event.target.value)
    }

    return (
        <div className="text-wrapper">
            <input 
            className="text"
            onChange= {change}
            value={val}
            placeholder="Enter Decryption Key(s)"
            />
            <div className="all-buttons">
                <button className="lpr-btn" onClick={clickLPR}>Key: XXXX</button>
                <button className="cctv-btn" onClick={clickCCTV}>Key: XXXXXX</button>
            </div>
        </div>
    )
}

export default TextboxDecrypt;