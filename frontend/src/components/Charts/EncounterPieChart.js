import React from 'react';
import { Pie } from 'react-chartjs-2';

const EncounterPieChart = ({ data }) => {
  if (!data || Object.keys(data).length === 0) return <p>No encounter data available.</p>;

  const chartData = {
    labels: Object.keys(data),
    datasets: [{
      data: Object.values(data),
      backgroundColor: ['#42a5f5', '#66bb6a', '#ffca28', '#ef5350', '#ab47bc']
    }]
  };

  return (
    <div>
      <h3>Encounter Type Distribution</h3>
      <Pie data={chartData} />
    </div>
  );
};

export default EncounterPieChart;
