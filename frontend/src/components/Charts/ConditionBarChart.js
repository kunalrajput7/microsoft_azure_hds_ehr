import React from 'react';
import { Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend
} from 'chart.js';

ChartJS.register(BarElement, CategoryScale, LinearScale, Title, Tooltip, Legend);

const ConditionBarChart = ({ data }) => {
  if (!data || data.length === 0) return <p>No conditions found.</p>;

  const chartData = {
    labels: data.map(item => item.condition.length > 30
      ? item.condition.slice(0, 30) + '...'
      : item.condition
    ),
    datasets: [{
      label: 'Condition Count',
      data: data.map(item => item.count),
      backgroundColor: '#42a5f5',
      borderRadius: 4,
      barPercentage: 0.6
    }]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    indexAxis: 'y',
    scales: {
      x: {
        title: {
          display: true,
          text: 'Number of Occurrences',
          font: { size: 14 }
        },
        ticks: {
          beginAtZero: true,
          precision: 0
        }
      },
      y: {
        title: {
          display: true,
          text: 'Condition',
          font: { size: 1 }
        }
      }
    },
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          label: (tooltipItem) => `Count: ${tooltipItem.raw}`
        }
      },
      title: {
        display: true,
        text: 'Top Conditions',
        font: { size: 16 }
      }
    }
  };

  return (
    <div style={{ height: '400px' }}>
      <Bar data={chartData} options={options} />
    </div>
  );
};

export default ConditionBarChart;
