// src/components/Charts/MedicationChart.js
import React from 'react';
import { Bar } from 'react-chartjs-2';

const MedicationChart = ({ data }) => {
  const labels = data.map(item => item.medication);
  const counts = data.map(item => item.count);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Top Medications',
        data: counts,
        backgroundColor: '#FF6384',
      },
    ],
  };

  const options = {
    indexAxis: 'y',
    responsive: true,
    plugins: { legend: { display: false } },
  };

  return (
    <div className="chart-card">
      <h3>Top Medications</h3>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default MedicationChart;
