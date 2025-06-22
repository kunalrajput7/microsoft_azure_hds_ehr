// src/chartConfig.js
import {
  Chart,
  ArcElement,
  BarElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  RadialLinearScale,
  Tooltip,
  Legend,
  Title
} from 'chart.js';

Chart.register(
  ArcElement,
  BarElement,
  LineElement,
  PointElement,
  CategoryScale,
  LinearScale,
  RadialLinearScale,
  Tooltip,
  Legend,
  Title
);
