// src/components/Charts/EncounterChart.js
import React from 'react';
import { Radar } from 'react-chartjs-2';

const EncounterChart = ({ data }) => {
  const labels = Object.keys(data);
  const counts = Object.values(data);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Encounter Types',
        data: counts,
        backgroundColor: 'rgba(75,192,192,0.2)',
        borderColor: '#4bc0c0',
        borderWidth: 2,
      },
    ],
  };

  return (
    <div className="chart-card">
      <h3>Encounter Types</h3>
      <Radar data={chartData} />
    </div>
  );
};

export default EncounterChart;
