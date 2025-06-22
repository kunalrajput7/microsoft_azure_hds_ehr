// src/pages/Home/HomePage.js
import React, { useEffect, useState } from 'react';
import './HomePage.scss';
import axios from 'axios';
import GenderChart from '../../components/Charts/GenderChart';
import RaceChart from '../../components/Charts/RaceChart';
import ConditionChart from '../../components/Charts/ConditionChart';
import MedicationChart from '../../components/Charts/MedicationChart';
import EncounterChart from '../../components/Charts/EncounterChart';
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
      <h1>📊 EHR Global Statistics</h1>
      <div className="chart-grid">
        <div className="chart-card card-gender">
          <GenderChart data={stats.gender_distribution} />
        </div>
        <div className="chart-card card-race">
          <RaceChart data={stats.race_distribution} />
        </div>
        <div className="chart-card card-condition">
          <ConditionChart data={stats.top_conditions} />
        </div>
        <div className="chart-card card-medication">
          <MedicationChart data={stats.top_medications} />
        </div>
        <div className="chart-card card-encounter">
          <EncounterChart data={stats.encounter_types} />
        </div>
        <div className="chart-card card-imaging">
          <ImagingChart data={stats.imaging_modalities} />
        </div>
        <div className="chart-card card-vitals">
          <VitalsChart data={stats.vitals_summary} />
        </div>
      </div>
    </div>
  );
};

export default HomePage;