// src/components/Charts/VitalsChart.js
import React from 'react';
import { Bar } from 'react-chartjs-2';

const VitalsChart = ({ data }) => {
  const labels = ['Glucose', 'BMI', 'Systolic BP', 'Diastolic BP'];
  const values = [
    data.avg_glucose || 0,
    data.avg_bmi || 0,
    data.avg_systolic || 0,
    data.avg_diastolic || 0,
  ];

  const chartData = {
    labels,
    datasets: [
      {
        label: 'Average Vitals',
        data: values,
        backgroundColor: '#00d4ff',
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: { legend: { display: false } },
  };

  return (
    <div className="chart-card">
      <h3>Vitals Summary</h3>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default VitalsChart;
