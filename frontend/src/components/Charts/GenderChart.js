// src/components/Charts/GenderChart.js
import React from 'react';
import { Pie } from 'react-chartjs-2';

const GenderChart = ({ data }) => {
  const chartData = {
    labels: Object.keys(data),
    datasets: [
      {
        data: Object.values(data),
        backgroundColor: ['#4bc0c0', '#ff6384'],
      },
    ],
  };

  return (
    <div className="chart-card">
      <h3>Gender Distribution</h3>
      <Pie data={chartData} />
    </div>
  );
};

export default GenderChart;
