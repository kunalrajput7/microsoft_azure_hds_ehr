// ConditionFrequencyChart.js
import React from 'react';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';

const ConditionFrequencyChart = ({ conditions }) => {
  if (!conditions || conditions.length === 0) return <p>No conditions found.</p>;

  const data = {
    labels: conditions.map(c => c.condition),
    datasets: [
      {
        label: 'Frequency',
        data: conditions.map(c => c.count),
        backgroundColor: '#ef5350',
      },
    ],
  };

  const options = {
    indexAxis: 'y',
    plugins: {
      legend: { display: false },
    },
  };

  return (
    <div>
      <h3>🦠 Top Diagnosed Conditions</h3>
      <Bar data={data} options={options} />
    </div>
  );
};

export default ConditionFrequencyChart;
