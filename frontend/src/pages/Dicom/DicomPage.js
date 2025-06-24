// src/pages/Dicom/DicomPage.js

import React, { useState } from 'react';
import './DicomPage.scss';
import axios from 'axios';

const DicomPage = () => {
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await axios.post('http://localhost:8000/predict-pneumonia', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      setPrediction(res.data);
    } catch (err) {
      console.error('Upload failed:', err);
      setPrediction({ prediction: 'Error', confidence: 0 });
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setPrediction(null);
    setLoading(false);
  };

  return (
    <div className="dicom-page">
      {/* LEFT PANEL */}
      <div className="left-panel">
        <div className="upload-container">
          <h2>
            Upload your DICOM Image to do a{' '}
            <span className="highlight">Pneumonia Test</span>
          </h2>

          {!prediction && (
            <div className="upload-box">
              <img src="/upload.png" alt="upload" className="upload-image" />
              <label htmlFor="upload-button" className="upload-label">
                Upload DICOM Image
              </label>
              <input
                type="file"
                accept=".dcm"
                id="upload-button"
                onChange={handleUpload}
                disabled={loading}
                hidden
              />
              {loading && <p className="loading">Analyzing DICOM Image...</p>}
            </div>
          )}

          {prediction && (
            <div className="result">
              <h3>🧠 Model Prediction</h3>
              <p>
                <strong>Result:</strong>{' '}
                <span className={prediction.prediction === 'Pneumonia' ? 'danger' : 'normal'}>
                  {prediction.prediction}
                </span>
              </p>
              <p>
                <strong>Confidence:</strong> {prediction.confidence}
              </p>

              {/* DICOM Image */}
              {prediction.image_base64 && (
                <img
                  src={`data:image/png;base64,${prediction.image_base64}`}
                  alt="DICOM Preview"
                  className="dicom-preview"
                />
              )}

              {/* Metadata */}
              {prediction.metadata && (
                <div className="metadata">
                  <p><strong>Patient ID:</strong> {prediction.metadata.PatientID}</p>
                  <p><strong>Modality:</strong> {prediction.metadata.Modality}</p>
                  <p><strong>Study Date:</strong> {prediction.metadata.StudyDate}</p>
                  <p><strong>Body Part:</strong> {prediction.metadata.BodyPartExamined}</p>
                  <p><strong>Resolution:</strong> {prediction.metadata.Rows} × {prediction.metadata.Columns}</p>
                </div>
              )}

              <button className="reset-button" onClick={handleReset}>
                Upload New Image
              </button>
            </div>
          )}
        </div>
      </div>

      {/* RIGHT PANEL */}
      <div className="right-panel">
        <div className="info-container">
          <img src="/dicom_image.png" alt="dicom model" className="model-image" />
          <h3>
            This is a demonstration of how we used original DICOM Images in our
            ResNet18 Convolutional Neural Network Model to predict Pneumonia.
          </h3>
        </div>
      </div>
    </div>
  );
};

export default DicomPage;
