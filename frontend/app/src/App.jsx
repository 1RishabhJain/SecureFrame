import { useState } from 'react'
import './App.css'
import Navbar from './components/Navbar/Navbar.jsx'
import { BrowserRouter, Routes, Route } from 'react-router-dom'
import { Home } from './Pages/home.jsx'
import { Upload } from './Pages/upload.jsx'
import { DecryptUpload } from './Pages/decryptUpload.jsx'
import {Encrypt} from './Pages/encrypt.jsx'
import { Decrypt } from './Pages/decrypt.jsx'
import { Progress } from './Pages/progress.jsx'
import Background from './components/background/background'
import Demo from './Pages/demo'

import ObjectSelection from "./Pages/objectselection.jsx";
import VideoOutput from './Pages/videooutput.jsx'


function App() {
  return (
    <BrowserRouter>
      <Background />
      <div className="app-container">
        <Navbar />
        <div className="content-container">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/decryptUpload" element={<DecryptUpload />} />
            <Route path="/decrypt" element={<Decrypt />} />
            <Route path="/encrypt" element={<Encrypt />} />
            <Route path="/progress" element={<Progress />} />
            <Route path="/demo" element={<Demo />} /> 
            <Route path="/objectselection" element={<ObjectSelection />} />
            <Route path="/videooutput" element={<VideoOutput/>} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  )
}

export default App
