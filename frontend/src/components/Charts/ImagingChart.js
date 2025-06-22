// src/components/Charts/ImagingChart.js
import React from 'react';
import { PolarArea } from 'react-chartjs-2';

const ImagingChart = ({ data }) => {
  const labels = Object.keys(data);
  const counts = Object.values(data);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Imaging Modalities',
        data: counts,
        backgroundColor: [
          '#FF6384', '#36A2EB', '#FFCE56', '#9966FF', '#4BC0C0', '#FF9F40',
        ],
      },
    ],
  };

  return (
    <div className="chart-card">
      <h3>Imaging Modalities</h3>
      <PolarArea data={chartData} />
    </div>
  );
};

export default ImagingChart;
