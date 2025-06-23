import React from 'react';

const VitalsSummaryCard = ({ vitals }) => {
  if (!vitals) return <p>No vitals available.</p>;

  return (
    <div className="vitals-card">
      <h3>Vitals Summary</h3>
      <p><strong>Glucose:</strong> {vitals.glucose ?? 'N/A'}</p>
      <p><strong>BMI:</strong> {vitals.bmi ?? 'N/A'}</p>
      <p><strong>Systolic BP:</strong> {vitals.systolic_bp ?? 'N/A'}</p>
      <p><strong>Diastolic BP:</strong> {vitals.diastolic_bp ?? 'N/A'}</p>
    </div>
  );
};

export default VitalsSummaryCard;
