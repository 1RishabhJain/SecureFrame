import React from 'react';
import { Link } from 'react-router-dom'
import './home.css';
import logo from '../assets/ECUREFRAME.svg';
import homepagePic from '../assets/homepagepic.png';

export function Home() {
  return (
    <div className="main-container">
      <div className="hero-section">
        <div className="logo-container">
          <img src={logo} alt="AES-256 Object Vault" className="main-logo" />
        </div>
        
        <p className="subtitle">AES-256 Encryption ✦ Military Grade Security ✦ Quantum Safe</p>
        
        {/* <button className="cta-button">
          Start Encrypting Now
        </button> */}
        <Link to="/upload" className="cta-button">Start Encrypting Now</Link>
        
        <div className="image-section">
          <img src={homepagePic} alt="Homepage Visualization" className="visualization-image" />
        </div>
      </div>
    </div>
  );
}
