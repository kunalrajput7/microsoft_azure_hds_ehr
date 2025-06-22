// src/App.js
import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import './App.css'; // optional global styling
import HomePage from './pages/Home/HomePage';

const App = () => {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <div className="main-content">
          {/* Add routes here */}
          <HomePage />
        </div>
      </div>
    </Router>
  );
};

export default App;
