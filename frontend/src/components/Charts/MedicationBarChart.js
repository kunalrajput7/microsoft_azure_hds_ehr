import React from 'react';
import { Bar } from 'react-chartjs-2';

const MedicationBarChart = ({ data }) => {
  if (!data || data.length === 0) return <p>No medications found.</p>;

  const chartData = {
    labels: data.map(item => item.medication),
    datasets: [{
      label: 'Count',
      data: data.map(item => item.count),
      backgroundColor: '#66bb6a'
    }]
  };

  return (
    <div>
      <h3>Top Medications</h3>
      <Bar data={chartData} />
    </div>
  );
};

export default MedicationBarChart;
