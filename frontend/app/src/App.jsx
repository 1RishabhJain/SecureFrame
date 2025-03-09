import { useState } from 'react'
import './App.css'
import Navbar from './components/Navbar/Navbar.jsx'
import {HashRouter as Router, Routes, Route} from 'react-router-dom'
import { Home } from './Pages/home.jsx'
import { Upload } from './Pages/upload.jsx'
import { Decrypt } from './Pages/decrypt.jsx'
import { Encrypt } from './Pages/encrypt.jsx'
import Background from './components/background/background'

function App() {
  return (
    <Router>
      <Background />
      <div className="app-container">
        <Navbar />
        <div className="content-container">
          <Routes>
            <Route path="/" element={<Home/>}/>
            <Route path="/upload" element={<Upload/>}/>
            <Route path="/decrypt" element={<Decrypt/>}/>
            <Route path="/encrypt" element={<Encrypt/>}/>
          </Routes>
        </div>
      </div>
    </Router>
  )
}

export default App
