import React from 'react';

const PatientInfoCard = ({ patient }) => {
  if (!patient) return <p>No patient selected.</p>;

  return (
    <div className="patient-info">
      <h3>Patient Information</h3>
      <p><strong>Name:</strong> {patient.full_name}</p>
      <p><strong>Gender:</strong> {patient.gender}</p>
      <p><strong>Date of Birth:</strong> {patient.birth_date}</p>
      <p><strong>Race:</strong> {patient.race}</p>
      <p><strong>Ethnicity:</strong> {patient.ethnicity}</p>
      <p><strong>Language:</strong> {patient.language}</p>
      <p><strong>Phone:</strong> {patient.phone}</p>
      <p><strong>Address:</strong> {patient.address_line}, {patient.city}, {patient.state}</p>
    </div>
  );
};

export default PatientInfoCard;
