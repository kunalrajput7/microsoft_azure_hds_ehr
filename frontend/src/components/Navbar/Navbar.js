// src/components/Navbar/Navbar.js

import React from "react";
import { NavLink } from "react-router-dom";
import "./Navbar.scss";

const Navbar = () => {
  return (
    <div className="navbar">
      <div className="logo">
        <img src="/logo.png" alt="Logo" />
      </div>

      <div className="nav-icons">
        <NavLink to="/" className={({ isActive }) => isActive ? "active" : ""}>
            <img src="/home.png" alt="Home" />
        </NavLink>
        <NavLink to="/fhir" activeclassname="active">
          <img src="/fhir.png" alt="FHIR" />
        </NavLink>
        <NavLink to="/dicom" activeclassname="active">
          <img src="/dicom.png" alt="DICOM" />
        </NavLink>
      </div>
    </div>
  );
};

export default Navbar;
