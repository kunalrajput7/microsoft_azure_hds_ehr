// src/components/Charts/TimelineChart.js
import React from 'react';
import { Chart } from 'react-chartjs-2';
import 'chartjs-adapter-moment';
import moment from 'moment';
import {
  Chart as ChartJS,
  TimeScale,
  LinearScale,
  PointElement,
  Tooltip,
  Title
} from 'chart.js';

ChartJS.register(TimeScale, LinearScale, PointElement, Tooltip, Title);

const TimelineChart = ({ data }) => {
  if (!data || data.length === 0) return <p>No timeline data available.</p>;

  const chartData = {
    datasets: [
      {
        label: 'Patient Encounters',
        data: data.map(item => ({
          y: item.start,
          x: item.reason || 'Encounter',
        })),
        backgroundColor: '#007acc',
        pointRadius: 2,
        pointHoverRadius: 8,
      }
    ]
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      tooltip: {
        callbacks: {
          title: (tooltipItems) =>
            moment(tooltipItems[0].parsed.y).format('YYYY-MM-DD HH:mm'),
          label: (tooltipItem) => `Reason: ${tooltipItem.raw.x}`,
        }
      },
      title: {
        display: true,
        text: 'Patient Encounter Timeline',
        font: { size: 18 }
      }
    },
    scales: {
      y: {
        type: 'time',
        time: {
          unit: 'month',
          tooltipFormat: 'YYYY-MM-DD',
        },
        title: {
          display: true,
          text: 'Encounter Date'
        }
      },
      x: {
        type: 'category',
        title: {
          display: true,
          text: 'Reason for Encounter'
        },
        offset: true
      }
    }
  };

  return (
    <div style={{ height: '500px' }}>
      <Chart type="scatter" data={chartData} options={options} />
    </div>
  );
};

export default TimelineChart;
