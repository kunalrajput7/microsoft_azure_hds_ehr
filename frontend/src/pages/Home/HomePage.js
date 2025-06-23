// src/pages/Home/HomePage.js
import React, { useEffect, useState } from 'react';
import './HomePage.scss';
import axios from 'axios';
import GenderChart from '../../components/Charts/GenderChart';
import RaceChart from '../../components/Charts/RaceChart';
import ConditionChart from '../../components/Charts/ConditionChart';
import MedicationChart from '../../components/Charts/MedicationChart';
import EncounterChart from '../../components/Charts/EncounterPieChart';
import ImagingChart from '../../components/Charts/ImagingChart';
import VitalsChart from '../../components/Charts/VitalsChart';

const HomePage = () => {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    axios.get('http://localhost:8000/global-stats')
      .then(res => setStats(res.data))
      .catch(err => console.error('Failed to fetch stats', err));
  }, []);

  if (!stats) return <div className="loading">Loading dashboard...</div>;

  return (
    <div className="homepage">
      <h1>Welcome Dr. Kunal, here’s your EHR dashboard overview:</h1>
      <div className="chart-grid">
        <GenderChart data={stats.gender_distribution} />
        <RaceChart data={stats.race_distribution} />
        <div className="combined">
          <ConditionChart data={stats.top_conditions} />
          <div className="divider" />
          <MedicationChart data={stats.top_medications} />
        </div>
        <EncounterChart data={stats.encounter_types} />
        <ImagingChart data={stats.imaging_modalities} />
        <VitalsChart data={stats.vitals_summary} />
      </div>
    </div>
  );
};

export default HomePage;
