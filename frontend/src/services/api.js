import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

export const getAllPatients = () => axios.get(`${API_BASE}/patients`);
export const getPatientDetails = (id) => axios.get(`${API_BASE}/patient/${id}`);
export const getGlucosePrediction = (id) => axios.get(`${API_BASE}/predict-glucose/${id}`);
export const getDiabetesPrediction = (id) => axios.get(`${API_BASE}/predict-diabetes/${id}`);
export const getReadmissionPrediction = (id) => axios.get(`${API_BASE}/predict-readmission/${id}`);
