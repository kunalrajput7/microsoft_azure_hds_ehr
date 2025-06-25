
# 🏥 EHR & DICOM Pneumonia Detection using AI

An end-to-end machine learning project using FastAPI, React, PostgreSQL, and Deep Learning (ResNet18)


## 🔧 Project Overview

This project combines Electronic Health Records (EHR) data and DICOM imaging to provide insightful analytics and real-time AI-based predictions for:

- 🧪 Glucose Anomalies
- 🩺 Diabetes Detection
- ♻️ Readmission Risk
- 🌫️ Pneumonia Detection (DICOM)

The system uses FastAPI as the backend, PostgreSQL as the database, React for the frontend, and trained machine learning & deep learning models for prediction
## 🔌Rest API Endpoints (Sample):

| Endpoint            | Description                                                                |
| ----------------- | ------------------------------------------------------------------ |
| /patients	 | Get list of all patients |
| /patient-fhir-stats/{id} | Get charts and vitals for a selected patient |
| /predict-glucose/{id} | 	Glucose anomaly prediction |
| /predict-diabetes/{id}| Diabetes prediction with confidence |
| /predict-readmission/{id}| Readmission risk classification |
| /predict-pneumonia{img}| Upload DICOM image to predict Pneumonia |


## 🤖 Machine Learning Models

    1. Glucose Model
        Type: Regression
        Output: Glucose values + anomaly detection (Normal / High)
        File: ml/glucose_model.py

    2. Diabetes Model
        Type: Classifier
        Features: Glucose, BMI, Age, Blood Pressure
        Output: Diabetic / Non-diabetic
        File: ml/diabetes_model.py

    3. Readmission Model
        Type: Classifier
        Features: Age, Chronic Conditions, Vitals, Encounter History
        Output: Low-risk / High-risk + Probability
        File: ml/readmission_model.py

    4. Pneumonia Detection (DICOM)
        Model: ResNet18
        Dataset: RSNA Pneumonia Challenge
        Input: .dcm image file
        Output: Pneumonia / Normal + Confidence
        Training: train/dicom_training.ipynb
        Serving: ml/dicom_model.py
## 📊 Frontend Features

Built using React, Chart.js, and SCSS.

#### Home Page (Main Dashboard)
- Global Statistics of all the patients.
- Displaying various charts using all the data fetched from PostgresSQL. 

#### FHIR Page
- Patient selection
- Patient info panel (demographics)
- AI Prediction cards:
    - Glucose Anomaly
    - Diabetes Risk
    - Readmission Probability

#### DICOM Page
- DICOM Upload for Pneumonia test
- Model output + confidence
- Image preview
- DICOM metadata (Patient ID, Modality, Dimensions)
- Option to reset and test another image


## 📌 Key UI Features
- Responsive layout (Flex + Grid)
- Vertical and horizontal centering
- SCSS-based theming and styling
- Loading states and error handling
- Reusable chart components

## 🔍 Why ResNet18 (Deep Learning Model) for DICOM?
- Lightweight CNN perfect for medical image classification
- Pretrained weights for better feature extraction
- Efficient on both GPU and CPU
- Easy to fine-tune on domain-specific images



#### Training Summary:

| Parameter           | Value                                                                |
| ----------------- | ------------------------------------------------------------------ |
| Model | ResNet18 |
| Epochs | 5 |
| Optimizer | 	Adam|
| Loss| Binary Cross Entropy |
| Dataset| RSNA DICOM (annotated with Pneumonia presence) |
| Output| train/models/dicom_model.pth |


## ✅ Completion Checklist

- ✅ PostgreSQL + SQLAlchemy + FastAPI backend
- ✅ Trained 4 AI models (Glucose, Diabetes, Readmission, Pneumonia)
- ✅ Full FHIR data ingestion and analytics
- ✅ REST APIs for all models and stats
- ✅ Responsive React frontend
- ✅ DICOM file upload with AI diagnosis
- ✅ Beautiful charts and dashboards
- ✅ Real-time ML inference

## 📄 Detailed Documentation
- [Link](https://drive.google.com/file/d/18ahzMWclU8nTGtnJYR71O69vL_Lhv2If/view?usp=sharing)

## 👨 Author

- [Kunal Rajput](https://www.linkedin.com/in/kunalrajput1/)
