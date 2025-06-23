// src/pages/Fhir/FhirPage.js

import React, { useEffect, useState } from 'react';
import './FhirPage.scss';
import axios from 'axios';

import EncounterPieChart from '../../components/Charts/EncounterPieChart';
import VitalsSummaryCard from '../../components/Charts/VitalsSummaryCard';
import ConditionBarChart from '../../components/Charts/ConditionBarChart';
import MedicationBarChart from '../../components/Charts/MedicationBarChart';
import ImagingPieChart from '../../components/Charts/ImagingPieChart';
import TimelineChart from '../../components/Charts/TimelineChart';

const FhirPage = () => {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [predictions, setPredictions] = useState({});
  const [fhirStats, setFhirStats] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/patients')
      .then(res => setPatients(res.data))
      .catch(err => console.error('Failed to fetch patients', err));
  }, []);

  const handleSelectPatient = async (id) => {
    const patient = patients.find(p => p.id === id);
    setSelectedPatient(patient);
    await fetchPredictions(id);
    await fetchFhirStats(id);
  };

  const fetchPredictions = async (id) => {
    try {
      const [glucoseRes, diabetes, readmission] = await Promise.all([
        axios.get(`http://localhost:8000/predict-glucose/${id}`).then(r => r.data),
        axios.get(`http://localhost:8000/predict-diabetes/${id}`).then(r => r.data),
        axios.get(`http://localhost:8000/predict-readmission/${id}`).then(r => r.data),
      ]);

      // Glucose predictions: extract latest + average
      const glucoseReadings = glucoseRes.predictions || [];
      const latestGlucose = glucoseReadings.length > 0 ? glucoseReadings[0] : null;
      const avgGlucose = glucoseReadings.length > 0
        ? (glucoseReadings.reduce((sum, g) => sum + g.value, 0) / glucoseReadings.length).toFixed(2)
        : null;

      setPredictions({
        glucose: {
          latest: latestGlucose,
          average: avgGlucose
        },
        diabetes,
        readmission
      });
    } catch (err) {
      console.error("Prediction error:", err);
    }
  };

  const fetchFhirStats = async (id) => {
    try {
      const res = await axios.get(`http://localhost:8000/patient-fhir-stats/${id}`);
      setFhirStats(res.data);
    } catch (err) {
      console.error("FHIR stats error:", err);
    }
  };

  return (
    <div className="fhir-page">
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
        <>
          <div className="top-section">
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

            <div className="ai-predictions">
              <h3>⚙️ AI Predictions</h3>
              <div className="prediction-cards">
                <div className="card">
                  <h4>Glucose Anomaly</h4>
                  {predictions.glucose?.latest ? (
                    <>
                      <p><b>Status:</b> {predictions.glucose.latest.status}</p>
                      <p><b>Latest Value:</b> {predictions.glucose.latest.value}</p>
                      <p><b>Average Value:</b> {predictions.glucose.average}</p>
                    </>
                  ) : <p>No glucose data.</p>}
                </div>

                <div className="card">
                  <h4>Diabetes</h4>
                  {predictions.diabetes?.status ? (
                    <>
                      <p><b>Status:</b> {predictions.diabetes.status}</p>
                      <p><b>Confidence:</b> {Math.round(predictions.diabetes.confidence * 100)}%</p>
                    </>
                  ) : <p>No diabetes data.</p>}
                </div>

                <div className="card">
                  <h4>Readmission</h4>
                  {predictions.readmission?.status ? (
                    <>
                      <p><b>Risk:</b> {predictions.readmission.status}</p>
                      <p><b>Confidence:</b> {Math.round(predictions.readmission.confidence * 100)}%</p>
                    </>
                  ) : <p>No readmission data.</p>}
                </div>
              </div>
            </div>
          </div>

          {fhirStats && (
            <div className="patient-charts">
              <div className="chart-grid">
                <EncounterPieChart data={fhirStats.encounter_types} />
                <ImagingPieChart data={fhirStats.imaging_modalities} />
                <TimelineChart data={fhirStats.encounter_timeline} />
                <VitalsSummaryCard vitals={fhirStats.vitals_summary} />
                <ConditionBarChart data={fhirStats.conditions} />
                <MedicationBarChart data={fhirStats.medications} />
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default FhirPage;
