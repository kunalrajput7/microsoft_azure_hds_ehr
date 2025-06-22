// src/pages/Fhir/FhirPage.js

import React, { useEffect, useState } from 'react';
import './FhirPage.scss';
import axios from 'axios';

const FhirPage = () => {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [predictions, setPredictions] = useState({});

  useEffect(() => {
    axios.get('http://localhost:8000/patients')
      .then(res => setPatients(res.data))
      .catch(err => console.error('Failed to fetch patients', err));
  }, []);

  const handleSelectPatient = (id) => {
    const patient = patients.find(p => p.id === id);
    setSelectedPatient(patient);
    fetchPredictions(id);
  };

  const fetchPredictions = async (id) => {
    try {
      const [glucose, diabetes, readmission] = await Promise.all([
        axios.get(`http://localhost:8000/predict-glucose/${id}`).then(r => r.data),
        axios.get(`http://localhost:8000/predict-diabetes/${id}`).then(r => r.data),
        axios.get(`http://localhost:8000/predict-readmission/${id}`).then(r => r.data),
      ]);
      setPredictions({ glucose, diabetes, readmission });
    } catch (err) {
      console.error("Prediction error:", err);
    }
  };

  return (
    <div className="fhir-page">
      <div className="left-panel">
        <h2>Select a patient to view FHIR records</h2>
        <div className="selector">
          <select onChange={(e) => handleSelectPatient(e.target.value)}>
            <option value="">Select a patient</option>
            {patients.map(p => (
              <option key={p.id} value={p.id}>{p.full_name}</option>
            ))}
          </select>
        </div>

        {selectedPatient && (
          <div className="patient-info">
            <h3>🧍 Patient Details</h3>
            <div className="grid">
              <p><strong>Name:</strong> {selectedPatient.full_name}</p>
              <p><strong>Gender:</strong> {selectedPatient.gender}</p>
              <p><strong>DOB:</strong> {selectedPatient.birth_date}</p>
              <p><strong>Race:</strong> {selectedPatient.race}</p>
              <p><strong>Marital Status:</strong> {selectedPatient.marital_status}</p>
              <p><strong>Language:</strong> {selectedPatient.language}</p>
              <p><strong>Phone:</strong> {selectedPatient.phone}</p>
              <p><strong>Address:</strong> {selectedPatient.address_line}, {selectedPatient.city}</p>
              <p><strong>State:</strong> {selectedPatient.state}</p>
              <p><strong>Country:</strong> {selectedPatient.country}</p>
            </div>
          </div>
        )}
      </div>

      {selectedPatient && (
        <div className="right-panel">
          <h3>⚙️ AI Predictions</h3>
          <div className="prediction-cards">
            <div className="card">
              <h4>Glucose Anomaly</h4>
              <p>Status: {predictions.glucose?.status}</p>
              {predictions.glucose?.value && <p>Value: {predictions.glucose.value}</p>}
            </div>
            <div className="card">
              <h4>Diabetes</h4>
              <p>Status: {predictions.diabetes?.status}</p>
              {predictions.diabetes?.confidence && (
                <p>Confidence: {predictions.diabetes.confidence}</p>
              )}
            </div>
            <div className="card">
              <h4>Readmission</h4>
              <p>Status: {predictions.readmission?.risk}</p>
              {predictions.readmission?.probability && (
                <p>Probability: {predictions.readmission.probability}</p>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FhirPage;
