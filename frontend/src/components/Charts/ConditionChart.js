// src/components/Charts/ConditionChart.js
import React from 'react';
import { Bar } from 'react-chartjs-2';

const ConditionChart = ({ data }) => {
  const labels = data.map(item => item.condition);
  const counts = data.map(item => item.count);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Top Conditions',
        data: counts,
        backgroundColor: '#36A2EB',
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
      <h3>Top Conditions</h3>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default ConditionChart;
