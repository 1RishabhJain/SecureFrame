import "./Textbox.css"
import { useState } from "react";

function Textbox() {
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
            placeholder="Enter license plate # to identify"
            />
            <div className="all-buttons">
                <button className="lpr-btn" onClick={clickLPR}>LPR Video</button>
                <button className="cctv-btn" onClick={clickCCTV}>CCTV</button>
            </div>
        </div>
    )
}

export default Textbox;