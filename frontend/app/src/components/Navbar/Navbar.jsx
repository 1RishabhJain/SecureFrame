import { useState } from 'react'
import './Navbar.css';
import { Link } from 'react-router-dom'
import logo from '../../assets/minilogo.svg';

function Navbar() {
  return (
    <div className='navbar'>
      <div className="navbar-section logo-section">
        <Link to="/" className="logo-container">
          <img src={logo} alt="AES-256 Object Vault" className="main-logo" />
        </Link>
      </div>
      
      <div className="navbar-section nav-section">
        <Link to="/upload" className="nav-link">Encryptor</Link>
        <Link to="/decryptUpload" className="nav-link">Decryptor</Link>
        <Link to="/demo" className="nav-link">Live Demo</Link>
      </div>
      
      <div className="navbar-section button-section">
        <Link to="/progress" className="login-btn">Log in</Link>
        <Link to="/videooutput" className="signup-btn">
          <span>Sign up</span>
          <div className="animated-border"></div>
        </Link>
      </div>
    </div>
  )
}

export default Navbar
