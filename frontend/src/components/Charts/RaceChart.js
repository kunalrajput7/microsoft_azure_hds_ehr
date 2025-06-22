// src/components/Charts/RaceChart.js
import React from 'react';
import { Doughnut } from 'react-chartjs-2';

const RaceChart = ({ data }) => {
  const chartData = {
    labels: Object.keys(data),
    datasets: [
      {
        data: Object.values(data),
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40',
        ],
      },
    ],
  };

  return (
    <div className="chart-card">
      <h3>Race Distribution</h3>
      <Doughnut data={chartData} />
    </div>
  );
};

export default RaceChart;
