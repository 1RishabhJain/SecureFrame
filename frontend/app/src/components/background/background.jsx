import React from "react";
import "./background.css";
import backgroundImage from "../../assets/Background Sample.svg";
import visualImage from "../../assets/Visual.svg";

const Background = () => {
  return (
    <>
      <div 
        className="background" 
        style={{ backgroundImage: `url(${backgroundImage})` }}
      ></div>
      <img src={visualImage} alt="" className="visual" />
    </>
  );
};

export default Background;