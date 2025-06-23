import React from 'react';
import { Pie } from 'react-chartjs-2';

const ImagingPieChart = ({ data }) => {
  if (!data || Object.keys(data).length === 0) return <p>No imaging modality data available.</p>;

  const chartData = {
    labels: Object.keys(data),
    datasets: [{
      data: Object.values(data),
      backgroundColor: ['#8e24aa', '#ff7043', '#26a69a', '#ec407a', '#5c6bc0']
    }]
  };

  return (
    <div>
      <h3>Imaging Modalities</h3>
      <Pie data={chartData} />
    </div>
  );
};

export default ImagingPieChart;
