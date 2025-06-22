// src/App.js
import React from 'react';
import { BrowserRouter as Router } from 'react-router-dom';
import Navbar from './components/Navbar/Navbar';
import './App.css'; // optional global styling

const App = () => {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <div className="main-content">
          {/* Add routes here */}
          <h1>Welcome to the Home Page</h1>
        </div>
      </div>
    </Router>
  );
};

export default App;
