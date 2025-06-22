// src/App.js
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import './App.css'; // optional global styling
import HomePage from './pages/Home/HomePage';
import FhirPage from './pages/Fhir/FhirPage'; // 👈 import FHIR page

const App = () => {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <div className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/fhir" element={<FhirPage />} />
            {/* Add more pages like <Route path="/dicom" ...> here later */}
          </Routes>
        </div>
      </div>
    </Router>
  );
};

export default App;
